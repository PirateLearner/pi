import re



def get_field_name_from_tag(current_tag):
    field_name = current_tag.split("_")[0:-1]
    return_name = "_".join(str(tag) for tag in field_name)
    return return_name


def get_pattern(current_tag):
    tag_start_pattern = "\\%\\% " + str(current_tag['name']) + " \\%\\%"
    tag_end_pattern = "\\%\\% endtag "+ str(current_tag['name']) + " \\%\\%"
    final_pattern =  tag_start_pattern + "(.*?)" + tag_end_pattern 
    return final_pattern


def parse_content(db_object, tag):
    if str(tag['name']) == 'title_tag':
        return db_object.title
    final_pattern = get_pattern(tag)
    print "pattern to be found ", final_pattern
    ## DOTALL flag for including new line also
    patt = re.compile(final_pattern,flags=re.DOTALL)
    print "pattern  ", patt
    print "data ", db_object.data
    result = patt.search(db_object.data)
    print result
    return result.group(1)

def strip_tag_from_data(data):
    p = re.compile('\\%\\% .*? \\%\\%',flags=re.DOTALL)
    print "LOGS:: Stripping tags from data"
    line = p.sub('', data)
    return line

    
    