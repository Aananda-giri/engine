
import urllib.request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import re 

# from urlparse import urljoin
# from BeautifulSoup import *
# import urllib2
# import urllib.request

# c = urllib.request.urlopen('http://kiwitobes.com/wiki/Programming_language.html')
# c = urllib.request.urlopen(
#     'https://en.wikipedia.org/wiki/Programming_language')
# contents = c.read()

# print(contents[:50])

# Create a list of words to ignore
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
print('hi')

class Searcher:
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getmatchrows(self, q):
        # Strings to build query
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []

        # split the words by space
        words = q.split(' ')
        tablenumber = 0

        for word in words:
            # gegt the word ID
            # wordrow = e.con.execute("select * from wordlist").fetchone()
            
            # search word from table `wordlist`
            wordrow = self.con.execute("select rowid from wordlist where word='%s' " % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]     # cleaning from (1077,) -> 1077
                wordids.append(wordid)  # list word_ids to be searched
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (
                        tablenumber-1, tablenumber)
                fieldlist += ',w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' % tablenumber
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1
            else:
                print(f'\n\n can\'t find word: {word}')
                
        # Create the query from the separate parts
        # search page with all words in 
        # conn.execute('select w0.urlid,w0.location,w1.location from  wordlocation w0,wordlocation w1 where w0.wordid=1077 and w0.urlid=w1.urlid and w1.wordid=329')
        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]     # [(url_id, location_of_word_1, location_of_word_2, ..)]
        return rows, wordids            # wordids = [1077, 329] # list of ids of words
    def getscoredlist(self,rows,wordids):
        # context-based ranking
        totalscores=dict([(row[0],0) for row in rows])
        
        
        
        
        
        
        
        # This is where you'll later put the scoring functions
        # weights=[]
        frequency_weights=[(1.0,self.frequencyscore(rows))]
        location_weights=[(1.0,self.locationscore(rows))]
        distance_weights=[(1.0,self.distancescore(rows))]

        # less reliable
        inbound_weights=[(1.0,self.inboundlinkscore(rows))]
        
        # by larry page <google founder>
        page_rank_weights = self.pagerankscore(rows)

        # get mean of weights
        # weights = [(frequency_weights[i] + location_weights[i] + distance_weights[i] + inbound_weights[i])/4 for i in range(frequency_weights)]
        weights=[
                    (1.0,self.locationscore(rows)),
                    (1.0,self.frequencyscore(rows)),
                    (1.0,self.pagerankscore(rows))
                ]
        
        # weights = self.pagerankscore((1.0,self.locationscore(rows)))
        weigths = page_rank_weights # change here
        
        
        
        


        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]
        return totalscores
    def geturlname(self,id):
        # context-based ranking
        return self.con.execute(
            "select url from urllist where rowid=%d" % id).fetchone( )[0]
    # searches for query q breaing it into it's constituent words
    def query(self,q):
        rows,wordids=self.getmatchrows(q)
        scores=self.getscoredlist(rows,wordids)
        rankedscores=sorted([(score,url) for (url,score) in scores.items( )],reverse=1)
        rankedscores.sort()
        rankedscores.reverse()
        for (score,urlid) in rankedscores[0:10]:
            print ('%f\t%s' % (score,self.geturlname(urlid)))
        return wordids,[r[1] for r in rankedscores[0:10]]
    ## normalizes result and returns value between 0 and 1.
    def normalizescores(self,scores,smallIsBetter=0):
        vsmall=0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0: maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    def frequencyscore(self,rows):
        counts=dict([(row[0],0) for row in rows])
        for row in rows: counts[row[0]]+=1
        return self.normalizescores(counts)

    def locationscore(self,rows):
        locations=dict([(row[0],1000000) for row in rows])
        for row in rows:
            loc=sum(row[1:])
            if loc<locations[row[0]]: locations[row[0]]=loc
        
        return self.normalizescores(locations,smallIsBetter=1)

    def distancescore(self,rows):
        # If there's only one word, everyone wins!
        if len(rows[0])<=2: return dict([(row[0],1.0) for row in rows])

        # Initialize the dictionary with large values
        mindistance=dict([(row[0],1000000) for row in rows])

        for row in rows:
            dist=sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
            if dist<mindistance[row[0]]: mindistance[row[0]]=dist
        return self.normalizescores(mindistance,smallIsBetter=1)

    def inboundlinkscore(self,rows):
        uniqueurls=dict([(row[0],1) for row in rows])
        inboundcount=dict([(u,self.con.execute('select count(*) from link where toid=%d' % u).fetchone()[0]) for u in uniqueurls])   
        return self.normalizescores(inboundcount)

    def linktextscore(self,rows,wordids):
        linkscores=dict([(row[0],0) for row in rows])
        for wordid in wordids:
            cur=self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid=link.rowid' % wordid)
            for (fromid,toid) in cur:
                if toid in linkscores:
                    pr=self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
                    linkscores[toid]+=pr
        maxscore=max(linkscores.values())
        normalizedscores=dict([(u,float(l)/maxscore) for (u,l) in linkscores.items()])
        return normalizedscores

    def pagerankscore(self,rows):
        print(f'\n--- dict: {rows[0]} {rows[0][0]} ---\n')
        print('{}'.format(self.con.execute('select score from pagerank where urlid=%d' % 27).fetchone()[0]))

        pageranks=dict([(row[0],self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        maxrank=max(pageranks.values())
        normalizedscores=dict([(u,float(l)/maxrank) for (u,l) in pageranks.items()])
        return normalizedscores

    def nnscore(self,rows,wordids):
        # Get unique URL IDs as an ordered list
        urlids=[urlid for urlid in dict([(row[0],1) for row in rows])]
        nnres=mynet.getresult(wordids,urlids)
        scores=dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
        return self.normalizescores(scores)
    
    # page rank by larry page: proportional to inbound links
    def calculatepagerank(self,iterations=20):
        # clear out the current PageRank tables
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')
        
        # initialize every url with a PageRank of 1
        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.dbcommit( )
        for i in range(iterations):
            print("Iteration %d" % (i))
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr=0.15     # damping factor of 85%
                
                # Loop through all the pages that link to this one
                for (linker,) in self.con.execute(
                'select distinct fromid from link where toid=%d' % urlid):
                
                    # Get the PageRank of the linker
                    linkingpr=self.con.execute(
                        'select score from pagerank where urlid=%d' % linker).fetchone( )[0]
                    
                    # Get the total number of links from the linker
                    linkingcount=self.con.execute(
                        'select count(*) from link where fromid=%d' % linker).fetchone( )[0]
                    
                    pr+=0.85*(linkingpr/linkingcount)
                self.con.execute(
                    'update pagerank set score=%f where urlid=%d' % (pr,urlid))
            self.dbcommit()
    # def pagerankscore(self,rows):
    #     pageranks=dict([(row[0],self.con.execute('select score from pagerank where\
    #         urlid = %d' % row[0]).fetchone( )[0]) for row in rows])
    #     maxrank=max(pageranks.values( ))
    #     normalizedscores = dict([(u,float(l)/maxrank) for (u,l) in pageranks.items( )])
    #     return normalizedscores
