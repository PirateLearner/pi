import sys

from django import forms
class CreateClass():
    """ This class will generate the required class of desired content type
    and form the string that will be written to the python script file
    """
    import_string = 'import tag_lib\nfrom django.db import models\nfrom blogging.models import *\nfrom django import forms\n' + \
    'from blogging.forms import *\nfrom ckeditor.widgets import CKEditorWidget\n' + \
    'from taggit.forms import * \nfrom django.db.models import Q \nfrom mptt.forms import TreeNodeChoiceField \n' 
    file_start = '"""\nThis is auto generated script file.\nIt defined the wrapper class for specified content type.\n"""\n'
    class_start_prifix = 'class '
    class_name = ""
    class_start_suffix = '(models.Model):\n'
    # it will be used for writing class defination
    class_string = ""
    # following will write the class member
    class_member = '\t'
    class_member_name = ''
    class_member_type = ''
    class_member_options = ''
    class_member_tag_list = "\ttag_list = [ { 'name':'title_tag' , 'type' :'CharField'}, "
    class_member_string_list = ['\ttitle = models.CharField(max_length=100)\n']
    class_strfunction_string = '\tdef __str__(self):\n'
    class_initfunction_string = ''
    class_initfunctionprot_string = '\tdef __init__(self):\n'
    class_initfunctiondef_string = ''
    class_templatefuntion_string = '\tdef render_to_template(self,db_object):\n'
    class_dbfuntion_string = '\tdef render_to_db(self,db_object):\n'
    class_formclass_string = 'class '
    class_formclass_meta_string = '\tclass Meta:\n' +'\t\tmodel = ' 
    class_formclass_save_string = '\tdef save(self):\n' + '\t\tinstance = '  
    
    def __init__(self, name, member_dict,is_leaf):
        member_dict.update({'title':'CharField'})
        self.class_name = name
        self.class_formclass_meta_string +=  self.class_name + '\n'
        self.class_formclass_save_string +=  self.class_name + '()\n'
        self.class_formclass_string += self.class_name + 'Form(forms.ModelForm):\n'
        self.class_string = self.class_start_prifix + str(self.class_name).capitalize() + self.class_start_suffix
    
        self.class_strfunction_string += '\t\treturn "' + self.class_name + '"\n\n'
        
        self.class_templatefuntion_string += '\t\tfor tag_name in self.tag_list:\n'
        self.class_templatefuntion_string += '\t\t\tcurrent_field = tag_lib.get_field_name_from_tag(str(tag_name[\'name\']))\n'
        self.class_templatefuntion_string += '\t\t\tresult_field = tag_lib.parse_content(db_object,tag_name)\n'
        
        
        self.class_dbfuntion_string += '\t\tfor tag_name in self.tag_list:\n'
        self.class_dbfuntion_string += '\t\t\tcurrent_field = tag_lib.get_field_name_from_tag(str(tag_name[\'name\']))\n'
        self.class_dbfuntion_string += '\t\t\ttag_start = "%% " + str(tag_name["name"]) + " %% " \n'
        self.class_dbfuntion_string += '\t\t\ttag_end = "%% endtag " + str(tag_name["name"]) + " %%"\n'
        
        for member_name, member_type in member_dict.iteritems():
            
            if is_leaf == True and str(member_name) == 'content_list' :
                continue
            else:
                self.class_member_name = member_name + ' = '
                self.class_member_type = 'models.' + member_type+ '()\n'
                member_string = self.class_member + self.class_member_name + self.class_member_type
                self.class_member_string_list.append(member_string)
                
                current_tag = " { 'name':'" + member_name + "_tag" + "' , 'type' :'" + member_type + "'} ,"
                self.class_member_tag_list += current_tag
                
                #self.class_initfunctionprot_string += ', ' + str(member_name)
                self.class_initfunctiondef_string += '\t\tself.' + str(member_name) + ' = " "\n'
                
                self.class_templatefuntion_string += "\t\t\tif current_field == '" + str(member_name) + "' : \n"
                #self.class_templatefuntion_string += "\t\t\t\ttagged_field = tag_start + self." +  str(member_name) + " + tag_end \n"
                self.class_templatefuntion_string += "\t\t\t\tself." + str(member_name) + " = result_field \n\n" 
                
                self.class_dbfuntion_string += "\t\t\tif current_field == '" + str(member_name) + "' : \n"
                self.class_dbfuntion_string += "\t\t\t\ttagged_field = tag_start + self."+str(member_name) + " + tag_end \n"
                if str(member_name) == 'title':
                	self.class_dbfuntion_string += "\t\t\t\tdb_object.title = self.title \n\n"
                else:
                	self.class_dbfuntion_string += "\t\t\t\tdb_object.data += tagged_field \n\n"
                ## Creating form fields in FormClass
                self.class_formclass_save_string += '\t\tinstance.' + str(member_name) + ' = self.cleaned_data["' + str(member_name) + '"]\n'
                 
                if str(member_name) != 'content_list' and str(member_name) != 'title':
                    if str(member_type) == 'TextField':
                        self.class_formclass_string += '\t' + self.class_member_name + ' forms.CharField(widget = CKEditorWidget())\n'
                    else:
                        self.class_formclass_string += '\t' + self.class_member_name + ' forms.'+ member_type + '()\n'
				
        #self.class_initfunctionprot_string += '):\n'
        self.class_initfunction_string = self.class_initfunctionprot_string + self.class_initfunctiondef_string 
        self.class_member_tag_list += "]\n\n"
        #self.class_formclass_string += '\tclass Meta:\n' +'\t\tmodel = '
        self.class_formclass_save_string += '\t\treturn instance\n'
        if is_leaf == True:
            self.class_formclass_string += '\tsection = forms.ModelChoiceField(\n' + \
                                    'queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),~Q(title="Blog"),children=None,),\n' + \
                                    'empty_label=None,\n' + \
                                    'required = True,\n' + \
                                    'label = "Select Parent")\n'
            self.class_formclass_string += '\ttags = TagField(help_text= "comma seperated fields for tags")\n'
            #self.class_formclass_string += '\t\twidgets = {"tags": PostTagWidget,"data": CKEditorWidget}\n'
        else:
            self.class_formclass_string += '\tparent = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),~Q(title="Blog")),required=True,' + \
                                            'empty_label=None, label = "Select Parent" )\n'

				
    
    def form_string(self):
        
        final_string =  self.import_string + self.file_start + self.class_string
        for member in self.class_member_string_list:
            #print final_string
            final_string += member
        final_string += self.class_member_tag_list + self.class_initfunction_string
        final_string += self.class_strfunction_string + self.class_templatefuntion_string + self.class_dbfuntion_string + self.class_formclass_string \
                        + self.class_formclass_meta_string + self.class_formclass_save_string
        
        return final_string
    

def test_fun():
    name = 'basecontent'
    member_dict = {'title': 'TextField',
                   'content': 'TextArea',
                   'Author' : 'TextField'
                   }
    
    create_class = CreateClass(name,member_dict)
    
    string =  create_class.form_string()
    print string
