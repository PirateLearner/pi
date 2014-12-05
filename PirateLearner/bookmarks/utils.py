from bookmarks import settings
import requests
import traceback
import sys
from lxml import etree
from urllib import urlencode
from urlparse import urlparse, parse_qs, urlunparse
from blogging.utils import get_imageurl_from_data
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re

MAX_NO_IMAGE = 5

def count_words(str):
    return len(re.findall(r'\b\w+\b', str))

def truncate_words(mystring,numberofwords=100):
    return ' '.join(mystring.split()[:numberofwords])
    

def get_domain_from_url(url):
    parsed_uri = urlparse( url )
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    print domain
    return domain



def validate_image_url(image):
    validate = URLValidator()
    try:
        validate(image)
        return True
    except ValidationError, e:
        print e
        return False

def convert_rel_images(image_list,url):
    image_list = [image if validate_image_url(image) else get_domain_from_url(url)+image for image in image_list]
    print "LOGS: after coversion ", image_list
    return image_list


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
        r = requests.get(url,timeout=3,allow_redirects=False)
        if r.status_code == requests.codes.ok:
            return_dict = extract_data(r.text)
            if is_empty(return_dict):
                return None
            return_dict['url'] = url
            return_dict['tags'] = []
            return_dict['image_list'] = convert_rel_images(return_dict['image_list'], url)
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
    if data['title'] and data['description'] and (len(data['image_list']) > 0):
        return False
    else:
        return True

def extract_data(data):
    
    print "First parsing it with lxml "
#     html.fromstring(page.text) todo: in some site explore it
    hparser = etree.HTMLParser(encoding='utf-8')
    html = etree.HTML(data,parser=hparser)
#     result = etree.tostring(html, pretty_print=True, method="html")
#     print(result)
    
    #soup = BeautifulSoup(data)
    # todo find the content from data in a order open graph, google and twitter cards
    
    return_dict = {}

    for provider in settings.BOOKMARK_FETCH_PRIORITY:
        return_dict['title'] = parse_title(html,provider)
        if return_dict['title']:
            break
    
    for provider in settings.BOOKMARK_FETCH_PRIORITY:
        return_dict['description'] = parse_description(html,provider)
        if return_dict['description']:
            break


    for provider in settings.BOOKMARK_FETCH_PRIORITY:
        return_dict['image_list'] = parse_image(html,provider)
        if len(return_dict['image_list']) > 0:
            break

    return return_dict


def parse_title(tree,provider):
    try:
        if provider == 'facebook':
            return tree.xpath( "//meta[@property='og:title']" )[0].get("content").encode('utf-8')
        elif provider == 'google':
            return tree.xpath( "//meta[@itemprop='name']" )[0].get("content").encode('utf-8')
        elif provider == 'twitter':
            return tree.xpath( "//meta[@name='twitter:title']" )[0].get("content").encode('utf-8')
        elif provider == 'extra':
            return tree.xpath( "//meta[@name='title']" )[0].get("content").encode('utf-8')
        else:
            return extarct_para_info(tree,'title')
    except:
        print "LOGS: title not found in %(provider)s meta"%{'provider':provider}
        return None

def parse_description(tree,provider):
    try:
        if provider == 'facebook':
            return tree.xpath( "//meta[@property='og:description']" )[0].get("content").encode('utf-8')
        elif provider == 'google':
            return tree.xpath( "//meta[@itemprop='description']" )[0].get("content").encode('utf-8')
        elif provider == 'twitter':
            return tree.xpath( "//meta[@name='twitter:description']" )[0].get("content").encode('utf-8')
        elif provider == 'extra':
            return tree.xpath( "//meta[@name='description']" )[0].get("content").encode('utf-8')
        else:
            return extarct_para_info(tree,'description')
    except:
        print "LOGS: description not found in %(provider)s meta"%{'provider':provider}
        return None

def parse_image(tree,provider):
    try:
        if provider == 'facebook':
            return [tree.xpath( "//meta[@property='og:image']" )[0].get("content").encode('utf-8')]
        elif provider == 'google':
            return [tree.xpath( "//meta[@itemprop='image']" )[0].get("content").encode('utf-8')]
        elif provider == 'twitter':
            return [tree.xpath( "//meta[@name='twitter:image']" )[0].get("content").encode('utf-8')]
        elif provider == 'extra':
            return [tree.xpath( "//meta[@name='image']" )[0].get("content").encode('utf-8')]
        else:
            image =  extarct_para_info(tree,'image')
            if len(image) == 0:
                return [settings.BOOKMARK_DEFAULT_IMAGE]
            else:
                return image
    except:
        print "LOGS: image not found in %(provider)s meta"%{'provider':provider}
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)
        return []
 
    
def extarct_para_info(tree,context):
    # extract the title, description and image from first paragraph
    print 'extract the title, description and image from opengraph meta tags'
  
    try:
        if context == 'title':
            return tree.xpath("/html/head/title/text()")[0].encode('utf-8')
            
        elif context == 'description':
            
#             regexpNS = "http://exslt.org/regular-expressions"
#             para = tree.xpath("//div[re:test(@class, '^.*content*')]/text()", namespaces={'re': regexpNS})
            para = tree.xpath("/descendant-or-self::node()/child::p/descendant::text()")
            print "LOGS: printing text in body --> ", para
            final_string = " ".join(x.encode('utf-8') for x in para)
            print "LOGS: before strip --> ", final_string
            print "LOGS: No of words in para are ", count_words(final_string)
            if count_words(final_string) > 100:
                print truncate_words(final_string)
                return truncate_words(final_string)
        elif context == 'image':
            para = tree.xpath("//img")
            final_images = [image.get("src").encode('utf-8') for image in para ]
            print "LOGS: Number of images found --> ", len(final_images)
            print "LOGS: Number of images found --> ", type(final_images)
            if len(final_images) < MAX_NO_IMAGE:
                return final_images
            else:
                return final_images[:MAX_NO_IMAGE]
    except:
        print "Unexpected error:", sys.exc_info()[0]
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            fname,lineno,fn,text = frame
            print "Error in %s on line %d" % (fname, lineno)
        return None
        
    return None
    