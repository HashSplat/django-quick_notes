from django import forms

import paste_image


from .models import QuickNotes, Attachment


class QuickNotesForm(forms.ModelForm):
    attachments = paste_image.PasteImageFormField(multiple=True)

    class Meta:
        model = QuickNotes
        exclude = ["content_type", "object_id",]

    def save(self, *args, **kwargs):
        obj = super(QuickNotesForm, self).save(*args, **kwargs)
        for file in self.cleaned_data["attachments"]:
            Attachment.objects.create(note=obj, file=file)
        return obj
