from crawler import Crawler
from searcher import Searcher
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])

def crawlnquery():
    # from importlib import reload
    pagelist=['https://en.wikipedia.org/wiki/Programming_language']
    # crawler=Crawler('searchindex.db')
    crawler=Crawler('pdfdb.db')

    pagelist=['https://tapendrapandey.com.np/category/education/books-and-resources', 'https://www.ioenotes.edu.np', 'https://ioe.promod.com.np', 'https://ioesolutions.esign.com.np', 'https://ioenotes.bikrampparajuli.com.np', 'https://www.biofamous.com', 'https://ioeguides.blogspot.com', 'https://notepulchowkcampus.blogspot.com', 'https://ioereader.blogspot.com', 'https://ioengineeringbooks.blogspot.com', 'http://somes.ioe.edu.np', 'https://abhashacharya.com.np', 'https://www.aayushwagle.com.np', 'https://www.nepalshovit.com.np', 'https://pdfcoffee.com']
    pagelist.extend(['https://acem.edu.np/pages/downloads', 'https://edunepal.info'])
    pagelist.extend(['http://pulchowknotes.blogspot.com', 'http://www.ioenotes.edu.np'])   # ioe notes and syllabus
    pagelist.extend(['https://ioesyllabus.com', 'https://ioesyllabus.com/app/Formula', 'https://ioesyllabus.com/app/syllabus', 'https://ioesyllabus.com/app/notes', 'https://ioesyllabus.com/app/Formula', 'https://ioesyllabus.com/app/MSc', 'https://ioesyllabus.com/app/loksewasyllabus'])   # ioe syllabus
    
    # ---------------
    # crawl
    # ---------------
    crawler=Crawler('pdfdb.db')
    try:
        crawler.createindextables()
        print('\ncreated table index\n') # create table if not already is created
    except Exception as ex:
        print(f'--- exception : {ex} ')
    # crawler.crawl(pagelist[:1])         # uncomment to crawls pages

    continue_search = True
    
    # ------------
    # searchcer
    # -------------
    while continue_search != False:
        search_text = input('please enter the word to be searched:\t')

        search=Searcher('pdfdb.db')     # searchindex.db
        # search=searcher('searchindex.db')
        print('\n ------------- getmatchrows: ----------------')
        # search.getmatchrows(search_text)

        # context based search
        print('\n ------------- query <context based>: ----------------')
        search.calculatepagerank()    # initialize page rank score
        search.query(search_text)
        continue_search = input('cotinue?')
    
    # --------------
    # page rank
    # --------------
    

    from importlib import reload
    reload(engine)
    crawler=engine.crawler('pdfdb.db')    # searchindex.db

    # --------------------- 
    # highest page rank
    # --------------------- 
    cur=crawler.con.execute('select * from pagerank order by score desc')
    for i in range(3): print(cur.next())

if __name__=='__main__':
    crawlnquery()
# Try calling this function with your first multiple-word search:
# reload(searchengine)


# e.con.execute('''select w0.urlid,w0.location,w1.location
# from wordlocation w0,wordlocation w1
# where w0.urlid=w1.urlid
# and w0.wordid=10
# and w1.wordid=17''')

'''
# imports
import engine
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import re

reload(hengine)
e=searcher('searchindex.db')
e.getmatchrows('functional programming')
'''

# import urllib3
# c=urllib3.urlopen('http://kiwitobes.com/wiki/Programming_language.html')
# contents=c.read( )
# print(contents[0:50])

# Used to make requests


# content = urllib.request.urlopen('http://kiwitobes.com/wiki/Programming_language.html')
# print(x.read())
'''
import engine
# pagelist=['http://kiwitobes.com/wiki/Perl.html']
pagelist=['https://en.wikipedia.org/wiki/Programming_language']

crawler=engine.Crawler('searchindex.db')
# crawler.createindextables()     # creates index tables


crawler.crawl(pagelist)         # crawls pages

# checking the entries for a word by querying the database
[row for row in crawler.con.execute(
 'select rowid from wordlocation where wordid=1')]


# querying
select w0.urlid,w0.location,w1.location
from wordlocation w0,wordlocation w1
where w0.urlid=w1.urlid
and w0.wordid=10
and w1.wordid=17

# Try calling this function with your first multiple-word search:
# reload(searchengine)
import engine
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3

import re
e=engine.searcher('searchindex.db')
e.getmatchrows('functional programming')

# context based search
import engine
e=engine.searcher('searchindex.db')
e.query('functional programming')
'''