import urllib2

url = 'http://www.hln.be/hln/reaction/listContent.do?componentId=2114607&navigationItemId=957&language=nl&page=0'

req = urllib2.Request(url)
response = urllib2.urlopen(req)
the_page = response.read()

fout = open('raw/test.html', 'w')
fout.write(the_page)
fout.close()
