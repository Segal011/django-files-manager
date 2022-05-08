from django import forms
from .models import File


class ActionForm(forms.Form):
    def form_action(self, file: File, user):
        raise NotImplementedError()

    def save(self, file: File, user):
        try:
            account, action = self.form_action(file, user)
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)
            raise

        return account, action


class FileForm(ActionForm):
    def form_action(self, file: File, user):
        return file