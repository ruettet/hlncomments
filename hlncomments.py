import urllib2
import sys
import re


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


def generate_reaction_urls(article_id):
    return ['http://www.hln.be/hln/reaction/listContent.do?componentId=' + article_id + '&language=nl&page=' + str(i)
            for i in range(0, 100, 1)]


def get_reactions_from_reaction_page(html):
    out = []
    reaction_regex = re.compile('<li class=".+?">(.+?)</li>', re.DOTALL)
    user_name_regex = re.compile('<cite>(.+?)</cite>', re.DOTALL)
    timestamp_regex = re.compile('<span class="time right">(.+?)</span>', re.DOTALL)
    content_regex = re.compile('<blockquote>(.+?)</blockquote>', re.DOTALL)
    for hit in reaction_regex.findall(html):
        out.append({'user_name': user_name_regex.findall(hit)[0].replace('\n', ' ').replace('\r', ' ').strip(),
                    'timestamp': timestamp_regex.findall(hit)[0].replace('\n', ' ').replace('\r', ' ').strip(),
                    'content': content_regex.findall(hit)[0].replace('\n', ' ').replace('\r', ' ').strip()
        })
    return out


def main():
    lines = []
    article_url = sys.argv[1]
    article_id = generate_article_id(article_url)
    article_title = generate_article_title(article_url)
    article_publication_date = generate_article_publication_date(article_url)
    reaction_urls = generate_reaction_urls(article_id)
    for reaction_url in reaction_urls:
        reaction_page = get_html(reaction_url)
        reactions = get_reactions_from_reaction_page(reaction_page)
        for reaction in reactions:
            reaction_user_name = reaction['user_name']
            reaction_timestamp = reaction['timestamp']
            reaction_content = reaction['content']
            line = [article_id, article_url, article_title, article_publication_date, reaction_user_name,
                    reaction_timestamp, reaction_content]
            lines.append('\t'.join(line))
    file_out = open(article_id + '.tsv', 'w')
    file_out.write('\n'.join(lines))
    file_out.close()


if __name__ == "__main__":
    main()
