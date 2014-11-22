from bookmarks import settings
import requests
import traceback
import sys
from lxml import etree
from urllib import urlencode
from urlparse import urlparse, parse_qs, urlunparse

url = 'http://whatever.com/somepage?utm_one=3&something=4&utm_two=5&utm_blank&something_else'


def strip_url(url):
    parsed = urlparse(url)
    qd = parse_qs(parsed.query, keep_blank_values=True)
    filtered = dict( (k, v) for k, v in qd.iteritems() if not k.startswith('utm_'))
    newurl = urlunparse([
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        urlencode(filtered, doseq=True), # query string
        parsed.fragment
    ])
    print "LOGS: url after strip is: ", newurl
    return newurl





def fetch_bookmark(url):

    try:
        return_dict = {}
        r = requests.get(url,timeout=1,allow_redirects=False)
        if r.status_code == requests.codes.ok:
            for provider in settings.BOOKMARK_FETCH_PRIORITY:
                return_dict = extract_data(r.text.decode('utf-8'),provider)
                if return_dict:
                    break
            return_dict['url'] = url
            return_dict['tags'] = []
            print "LOGS: Printing the fetched bookmark dictionary--> ", return_dict
            return return_dict
        else:
            return None
    except:
        print "LOGS: Some error in parsing !!!"
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)
        return None

def is_empty(data):
    if data['title'] and data['description'] and data['image_url']:
        return False
    else:
        return True

def extract_data(data,provider):
    
    print "First parsing it with lxml "
    
    html = etree.HTML(data)
#     result = etree.tostring(html, pretty_print=True, method="html")
#     print(result)
    
    #soup = BeautifulSoup(data)
    # todo find the content from data in a order open graph, google and twitter cards
    if provider == 'facebook':
        return extarct_og_info(html)
    elif provider == 'google':
        return extarct_google_info(html)
    elif provider == 'twitter':
        return extarct_twitter_info(html)
    else:
        return extarct_para_info(html)
        
def extarct_og_info(tree):
    # extract the title, description and image from opengraph meta tags
    print 'extract the title, description and image from opengraph meta tags'
    return_dict = {}
    return_dict['title'] = tree.xpath( "//meta[@property='og:title']" )[0].get("content")
    print 'LOGS: Title is ',return_dict['title']
    return_dict['description'] = tree.xpath( "//meta[@property='og:description']" )[0].get("content")
    print 'LOGS: description is ',return_dict['description']
    return_dict['image_url'] = tree.xpath( "//meta[@property='og:image']" )[0].get("content")
    print 'LOGS: image is ',return_dict['image_url']
    return return_dict
     
    
def extarct_google_info(tree):
    # extract the title, description and image from google meta tags
    print 'extract the title, description and image from opengraph meta tags'
    return_dict = {}

    return_dict['title'] = tree.xpath( "//meta[@itemprop='name']" )[0].get("content")
    print 'LOGS: Title is ',return_dict['title']
    return_dict['description'] = tree.xpath( "//meta[@itemprop='description']" )[0].get("content")
    print 'LOGS: description is ',return_dict['description']
    return_dict['image_url'] = tree.xpath( "//meta[@itemprop='image']" )[0].get("content")
    print 'LOGS: image is ',return_dict['image_url']
    return return_dict
      
def extarct_twitter_info(tree):
    # extract the title, description and image from twitter meta tags
    print 'extract the title, description and image from opengraph meta tags'
    return_dict = {}

    return_dict['title'] = tree.xpath( "//meta[@name='twitter:title']" )[0].get("content")
    print 'LOGS: Title is ',return_dict['title']
    return_dict['description'] = tree.xpath( "//meta[@name='twitter:description']" )[0].get("content")
    print 'LOGS: description is ',return_dict['description']
    return_dict['image_url'] = tree.xpath( "//meta[@name='twitter:image']" )[0].get("content")
    print 'LOGS: image is ',return_dict['image_url']
    return return_dict

    
def extarct_para_info(soup):
    # extract the title, description and image from first paragraph
    print 'extract the title, description and image from opengraph meta tags'
    return None
    