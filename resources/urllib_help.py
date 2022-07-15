#Used to make requests
# urllib python
import urllib.request

x = urllib.request.urlopen('https://www.google.com/')
print(x.read())


# urllib.request header
try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2

req = Request('http://api.company.com/items/details?country=US&language=en')
req.add_header('apikey', 'xxx')
content = urlopen(req).read()

print(content)





# urllib urlretrive python3
#In Python 3.x, the urlretrieve function is located in the urllib.request module:
from urllib.request import urlretrieve


# urllib3 python
# urllib.request.urlopen
>>> import urllib3
>>> http = urllib3.PoolManager()
>>> r = http.request('GET', 'http://httpbin.org/robots.txt')
>>> r.status
200
>>> r.data
'User-agent: *\nDisallow: /deny\n'



try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2

req = Request('http://api.company.com/items/details?country=US&language=en')
req.add_header('apikey', 'xxx')
content = urlopen(req).read()

print(content)







