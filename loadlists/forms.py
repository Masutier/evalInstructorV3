from django import forms


class UploadFilesForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
