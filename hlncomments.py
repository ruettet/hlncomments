import urllib2
import sys

url = 'http://www.hln.be/hln/reaction/listContent.do?componentId=2114607&navigationItemId=957&language=nl&page=0'

def get_html(url):
  req = urllib2.Request(url)
  response = urllib2.urlopen(req)
  return response.read()

def generate_article_id(url):
  return url.split('/')[9]

def generate_article_title(url):
  return url.split('/')[13].split('.dhtml')[0].replace('-', ' ')

def generate_article_publication_date(url):
  return '-'.join(url.split('/')[10:13])

def generate_reaction_urls(url, article_id):
  return ['http://www.hln.be/hln/reaction/listContent.do?componentId=' + article_id + '&language=nl&page=' + str(i) for i in range(0,20,1)]

def get_reactions_from_reaction_page(url):
  #TODO
  return [{'user_name': 'NA',
           'timestamp': 'NA',
           'content': 'NA'
          }]

def main():
  lines = []
  article_url = ''
  #TODO to be removed, only here for testing purposes
  if len(sys.argv) == 1:
    article_url = 'http://www.hln.be/hln/nl/957/Binnenland/article/detail/2114607/2014/11/07/Abdeslam-heeft-zijn-nieuwe-auto-via-crowdfunding-al-vast.dhtml?show=react'
  else:
    article_url = sys.argv[1]
  article_id = generate_article_id(article_url)
  article_title = generate_article_title(article_url)
  article_publication_date = generate_article_publication_date(article_url)
  reaction_urls = generate_reaction_urls(article_url, article_id)
  for reaction_url in reaction_urls:
    reaction_page = get_html(reaction_url)
    reactions = get_reactions_from_reaction_page(reaction_page)
    for reaction in reactions:
      reaction_user_name = reaction['user_name']
      reaction_timestamp = reaction['timestamp']
      reaction_content = reaction['content']
      line = [article_id, article_url, article_title, article_publication_date, reaction_user_name, reaction_timestamp, reaction_content]
      lines.append('\t'.join(line))
  fout = open(article_id + '.tsv', 'w')
  fout.write('\n'.join(lines))
  fout.close()

if __name__ == "__main__":
    main()
