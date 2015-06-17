
class ArticleForm(forms.Form):
	Body =  forms.CharField(widget = CKEditorWidget())
	title = forms.CharField(max_length = 100)
	tags = TagField()
	section = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),Q(children=None)),required=True,empty_label=None, label = "Select Section" )
	pid_count = forms.IntegerField(required=False)
	def __init__(self,action, *args, **kwargs):
		self.helper = FormHelper()
		
		self.helper.form_id = 'id-ArticleForm'
#		self.helper.form_class = 'blueForms'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-8'
		self.helper.form_method = 'post'
# 		self.helper.form_action = reverse('blogging:create-post')
		self.helper.form_action = action
		self.helper.layout = Layout(
				Fieldset(
                'Create Content of Type Article',
                'title',
				'Body',
				'section',
				Field('pid_count', type="hidden"),
                'tags',
            ),
			
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ),
			
			)
		super(ArticleForm, self).__init__(*args, **kwargs)

	
	def save(self,post):
		post.pop('section')
		post.pop('tags')
		post.pop('title')
		post.pop('csrfmiddlewaretoken')
		post.pop('submit')

		for k,v in post.iteritems():
			if str(k) != 'pid_count' :
				tmp = {}
				tmp = tag_lib.insert_tag_id(str(v),self.cleaned_data["pid_count"])
				post[k] = tmp['content']
				post['pid_count'] = tmp['pid_count']
			
		return json.dumps(post.dict())