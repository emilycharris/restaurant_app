# class UserCreateForm(UserCreationForm):
#     position = forms.ForeignKey(Position)
#
#     class Meta:
#         model = User
#         fields = ("username", "position", "password1", "password2")
#
#     def save(self, commit=True):
#         user = super(UserCreateForm, self).save(commit=False)
#         user.position = self.cleaned_data["position"]
#         if commit:
#             user.save()
#         return user
