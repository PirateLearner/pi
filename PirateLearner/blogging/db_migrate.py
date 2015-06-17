from blogging.tag_lib import parse_content
from blogging.models import BlogContent
import json
import os


def convert_tags(blog,tag_name,fd):
    tag = {}
    tag['name'] = tag_name + '_tag'
    content = parse_content(blog,tag)
    fd.write("\nConverting "+ blog.title + "\n")
    if len(content) > 0:
        tmp = {}
        tmp[tag_name] = content
        tag['name'] = 'pid_count_tag'
        content = parse_content(blog,tag)           
        if len(content) > 0:
            tmp['pid_count'] = content
        fd.write(json.dumps(tmp) + "\n")
        return True
    else:
        return False



def migrate():
    blogs = BlogContent.objects.all()
    form_filename = os.path.abspath(os.path.dirname(__file__))+"/custom/"+"migrate_articles.txt"
    fd = os.fdopen(os.open(form_filename,os.O_CREAT| os.O_RDWR , 0555),'w')
    
    for blog in blogs:

        if(convert_tags(blog, 'Body', fd)):
            continue
        elif (convert_tags(blog, 'content', fd)):
            continue
        elif(convert_tags(blog, 'Content', fd)):
            continue
        elif(convert_tags(blog, 'Summary', fd)):
            continue
        elif(convert_tags(blog, 'Preface', fd)):
            continue        
        else:
            print "NO TAGs FOUND in " + blog.title
            tmp = {}
            tmp['content'] = blog.data
            fd.write(json.dumps(tmp) + "\n")
    fd.close()
            
if __name__ == "__main__":
    migrate()
        
