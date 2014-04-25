from models import *

def show_content(current_section = None):
    list_content = []
    if current_section is not None:
        find_children(current_section,list_content)
    else:
        list_all_content(list_content)
    print list_content

    return list_content

def list_all_content(list_content = []):
    section = BlogParent.objects.filter(parent_id = None)
    for s in section:
        find_children(s.name,list_content)

def find_children(current_section,list_content = []):
    #section = Section.objects.get(name = current_section)
    section = get_object_or_404(BlogSection,name=current_section)
    if section is None:
        return []
#    list_section.append(section)
    if section.is_last:
        list_children = section.content_set.all()
        if list_children:
            list_content.extend(list_children)
    else:
        list_sub_section = section.subsection.all()
        for sub_section in list_sub_section:
            list_sub_section_objects = find_children(sub_section.name,list_content)
            if list_sub_section_objects:
                list_content.append(list_sub_section_objects)


