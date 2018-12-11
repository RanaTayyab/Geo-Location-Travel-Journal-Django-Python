from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text =None
        self.fields['email'].help_text =None
        self.fields['password1'].help_text =None
        self.fields['password2'].help_text =None

class EditProfileForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username','password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text =None
        self.fields['email'].help_text =None
        self.fields['password'].help_text =None
        del self.fields['password']
