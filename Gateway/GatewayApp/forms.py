from django import forms
from django.contrib.auth.models import User
#from StoriesApp.models import Storie
'''
import sys
sys.path.append("../../../Stories/StoriesApp/")
from .models import Storie
'''
'''
import sys, os.path
storie_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/Stories/StorieApp/')
sys.path.append(storie_dir)
from .models import Storie
'''

'''
class PostForm(forms.Form):
    from_user_id = forms.UUIDField(label='from_user_id', widget=forms.HiddenInput, initial="")
    to_user_id = forms.UUIDField(label='to_user_id', widget=forms.HiddenInput, initial="")
    text = forms.CharField(label="", help_text="", widget=forms.Textarea)
    back = forms.IntegerField(label="back", widget=forms.initial="")

    sticker_uuid = models.UUIDField(null=True, blank=True)
    music_uuid = models.UUIDField(null=True, blank=True)
    back = models.IntegerField(choices=[(1, 'white'), (2, 'red'), (3, 'yellow'), (4, 'green'), (5, 'black')], null=False)
'''

class AuthForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')

#class StorieForm(forms.ModelForm):
#	class Meta:
#		fields = ('from_user_id', 'to_user_id', 'text', 'sticker_uuid', 'music_uuid', 'back')
		'''
		from_user_id = forms.UUIDField(label='from_user_id', widget=forms.HiddenInput, initial="")
		to_user_id = forms.UUIDField(label='to_user_id', widget=forms.HiddenInput, initial="")
		text = forms.CharField(label="", help_text="", widget=forms.Textarea)
		back = forms.IntegerField(label="back", widget=forms.HiddenInput, initial="")
		'''