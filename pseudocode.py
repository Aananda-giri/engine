# english pseudocode

def storepdf(pdf_url, parent, link_text):
   - get_url_id(pdf_url): add to url_list if not exist
   - add link from parent to pdf_url
   - linkword: using link_text
   - 


# crawl the page
def crawl(pages, depth):
   for i  in range(depth)
      for page in pages:   # pages = url_list
         index page <addindex> if not already indexed
         links = get links of page
         for link in links:
            if not already indexed:
               index link 
               newpages.add(url)
         Add link between two pages ini database: from:page to:url with text:linktext
      pages=newpages

# index the url 
def addtoindex(url, soup):
   if not indexed:
      for word in words of page:
         store to table 'wordlocation' values: url, wordid, location
      store pdf url to seperate database <storepdf>

# store to database: 'pdfs' <if link is pdf>
def storepdf(url):
   if (url is drive link) or (link ends with 'pdf' or 'pdf/' or any other document format):
      add url id to database: 'pdfs'
   

# get id of word
def getentryid():
   if not stored:
      store to table 'urllist' values: 'word' -> word
   else:
      get id of stored word

# links between pages
def addlinkref(fromurl, tourl, linktext):
   words = separatewords(linkText)
   fromid = getentryid('urllist','url',urlFrom)
   toid = getentryid('urllist','url',urlTo)
   if fromid==toid: return # i.e. fromurl_id == tourl_id
   insert to table: 'link(fromid,toid)' values: fromid,toid
   
   
   for word in words:
      if word not in ignorewords:
         insert to table 'linkwords(linkid,wordid)' values: linkid, wordid
         ;where linkid=cur.lastrowid

# seperator
source: https://www.pythontutorial.net/python-regex/python-regex-split/
def separatewords(self, text):
        # source: https://www.pythontutorial.net/python-regex/python-regex-split/
        
        # splitter = re.compile('\W*')
        # return [s.lower() for s in splitter.split(text) if s != '']
        splitter = r'\W+'
        return [s.lower() for s in re.split(splitter, text) if s != '']


## searcher
def getmatchrows(query_string):
   # returns 
   # searches the page containg all the words in the string
   query_string = 'hello world'
   
   wordids = ['hello', 'world']      # list of words from given string
   fieldlist = 'w0.urlid, w0.location, w1.location'
   tablelist = 'wordlocation w0,wordlocation w1'    # list of tables
   clauselist = 'w0.wordid=1077 and w0.urlid=w1.urlid and w1.wordid=329'   # list of calues

   # search pages containing all the words
   rows = database_query -> 'select `fieldlist` from `tablelist` where `clauselist`'
   # conn.execute('select w0.urlid,w0.location,w1.location from  wordlocation w0,wordlocation w1 where w0.wordid=1077 and w0.urlid=w1.urlid and w1.wordid=329')
   # rows = [(url_id, location_of_word_1, location_of_word_2, ..)]
   return rows, wordids

def getscoredlist(self,rows,wordids):
        # context-based ranking
         # initialize with score zero
        totalscores=dict([(row[0],0) for row in rows])
        # This is where you'll later put the scoring functions
        weights=[]
        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]
        return totalscores

def geturlname(self,id):
        # returns url from urlid
        # context-based ranking
        return self.con.execute(
            "select url from urllist where rowid=%d" % id).fetchone( )[0]

def query(self,q):
        
        rows,wordids=self.getmatchrows(q)
        scores=self.getscoredlist(rows,wordids)
        rankedscores=sorted([(score,url) for (url,score) in scores.items( )],reverse=1)
        for (score,urlid) in rankedscores[0:10]:
            print ('%f\t%s' % (score,self.geturlname(urlid)))