import urllib.request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import re 
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
class Crawler:
   # iniitialize the Crawler with the name database
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

   # Auxilary function for getting an <entry: word_of_wordlist, url_of_urllist> id and adding
   # if it's not present
    def getentryid(self, table, field, value, createnew=True):
        # table = 'wordlist', field='word', value = word whose id is to be fetchd
        # table = 'urllist', field='url', value = url whose id is to be fetchd
        current_record = self.con.execute(
            "select rowid from %s where %s='%s'" % (table, field, value))
        res = current_record.fetchone()
        if res == None:
            current_record = self.con.execute(
                "insert into %s (%s) values ('%s')" % (table, field, value))
            return current_record.lastrowid
        else:
            return res[0]

    # index an individual page
    def addtoindex(self, url, soup):
        if self.isindexed(url):
            return
        print('Indexing ' + url)

        # Get the individual words
        text = self.gettextonly(soup)
        words = self.separatewords(text)

        # Get the URL id
        urlid = self.getentryid('urllist', 'url', url)

        # Link each word to this url
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords:
                continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) \
                values (%d,%d,%d)" % (urlid, wordid, i))
        self.storepdf(url, urlid)
    
    
    
    # Extract the text from an HTML page (no tags)
    def gettextonly(self, soup):
        # Finding the Words on a Page
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext+'\n'
            return resulttext
        else:
            return v.strip()

    # Seperate the words by any non-whitespace character
    def separatewords(self, text):
        # source: https://www.pythontutorial.net/python-regex/python-regex-split/
        
        # splitter = re.compile('\W*')
        # return [s.lower() for s in splitter.split(text) if s != '']
        splitter = r'\W+'
        return [s.lower() for s in re.split(splitter, text) if s != '']
        

    # Return True if this url is already indexed
    def isindexed(self, url):
        u = self.con.execute(
            "select rowid from urllist where url='%s'" % url).fetchone()
        if u != None:
            # Check if it has actually been crawled
            v = self.con.execute(
                'select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v != None:
                return True
        return False

    # Add link between two pages
    def addlinkref(self, urlFrom, urlTo, linkText):
        words=self.separatewords(linkText)
        fromid=self.getentryid('urllist','url',urlFrom)
        toid=self.getentryid('urllist','url',urlTo)
        if fromid==toid: return  # i.e. fromurl_id == tourl_id
        cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
        linkid=cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))

    # Starting with a list of pages, do breadth first search
    # to the given depth, indexing pages as we go
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:  # pages = url_list
                try:
                    # c = urllib.request.urlopen(page)
                    c = requests.get(page)
                except:
                    print(f"cound not open {page}")
                    continue
                # soup = BeautifulSoup(c.read())
                soup = BeautifulSoup(c.text)
                self.addtoindex(page, soup)

                links = soup('a')
                for link in links:
                    if('href' in dict(link.attrs)):
                        # if <a> has a link
                        url = urljoin(page, link['href'])
                        if url.find("\'") != -1:    # ignore url with quote
                            continue
                        url = url.split('#')[0]   # remove location portion
                        if url[:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)   # strange links e.g. 
                        self.addlinkref(page, url, linkText)    # # Add link between two pages: 
                self.dbcommit()
            pages = newpages

    # Create the database tables
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create table pdfs(urlid)')

        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.con.execute('create index pdfurl on pdfs(urlid)')  #  creating index of each  pdf_url
        self.dbcommit()
    
    def storepdf(self, url, url_id):
        # store to database: pdfs <if link is pdf>
        document_prefixes = ['https://drive.google.com/', ]
        document_suffixes = ['pdf', 'epub', 'doc', 'docx', 'odt', 'xls', 'xlsx', 'ppt', 'pptx']
        if True in [url.startswith(document_prefix) for document_prefix in document_prefixes] + [url.endswith(document_suffix) for document_suffix in document_suffixes]:
            print(f'pdf:{url}, {url_id}')
            self.conn.execute("insert into pdfs(urlid) values (%d)" % (url_id))
        else:
            print(f'not_: {url} {url_id}')
