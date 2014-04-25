import re
    
def get_field_name_from_tag(current_tag):
    field_name = current_tag.split("_")[0:-1]
    return_name = "_".join(str(tag) for tag in field_name)
    return return_name


def get_pattern(current_tag):
    tag_start_pattern = "\\%\\% " + str(current_tag['name']) + " \\%\\%"
    tag_end_pattern = "\\%\\% endtag "+ str(current_tag['name']) + " \\%\\%"
    final_pattern = tag_start_pattern + "(.*?)" + tag_end_pattern
    return final_pattern


def parse_content(db_object, tag):
    final_pattern = self.get_pattern(tag)
    patt = re.compile(final_pattern)
    result = patt.search(db_object.content)
    return result.group(1)
