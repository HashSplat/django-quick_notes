from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

import datetime

from django.db import models

from taggit.managers import TaggableManager
import paste_image

from django.conf import settings
from . import settings as quick_notes_settings


def make_choice_tuple(value, data_type_conversion=str):
    if isinstance(value, (list, tuple)):
        if len(value) >= 2:
            return value
        return str(value[0]), data_type_conversion(value[0])
    else:
        return str(value), data_type_conversion(value)

# Get/Set default settings
settings.TAGGIT_CASE_INSENSITIVE = getattr(settings, "TAGGIT_CASE_INSENSITIVE",
                                           quick_notes_settings.TAGGIT_CASE_INSENSITIVE)

# ========== Quick Notes settings ==========
QUICK_NOTES_CATEGORIES = getattr(settings, "QUICK_NOTES_CATEGORIES", quick_notes_settings.QUICK_NOTES_CATEGORIES)
QUICK_NOTES_CATEGORY_TYPE = getattr(settings, "QUICK_NOTES_CATEGORY_TYPE",
                                    quick_notes_settings.QUICK_NOTES_CATEGORY_TYPE)

QUICK_NOTES_CATEGORY_FIELD = models.CharField
QUICK_NOTES_CATEGORY_FIELD_KWARGS = {"max_length": 100}
if QUICK_NOTES_CATEGORY_TYPE == str:
    QUICK_NOTES_CATEGORY_FIELD = models.CharField
    QUICK_NOTES_CATEGORY_FIELD_KWARGS = {"max_length": 100}
elif QUICK_NOTES_CATEGORY_TYPE == int:
    QUICK_NOTES_CATEGORY_FIELD = models.IntegerField
    QUICK_NOTES_CATEGORY_FIELD_KWARGS = {}
QUICK_NOTES_CATEGORIES = [make_choice_tuple(value, QUICK_NOTES_CATEGORY_TYPE) for value in QUICK_NOTES_CATEGORIES]
# ========== END Quick Notes settings ==========


class QuickNotes(models.Model):
    """QuickNotes generic model.

    Example:
        from django.contrib.contenttypes.fields import GenericRelation

        class MyModel(models.Model):
            notes = GenericRelation("quick_notes.QuickNote")
    """
    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    # Main fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(default=datetime.datetime.utcnow, editable=False)
    modified = models.DateTimeField(auto_now=True)

    category = QUICK_NOTES_CATEGORY_FIELD(choices=QUICK_NOTES_CATEGORIES, default=QUICK_NOTES_CATEGORIES[0],
                                          **QUICK_NOTES_CATEGORY_FIELD_KWARGS)

    description = models.TextField(blank=True, default="")

    tags = TaggableManager()

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created = datetime.datetime.utcnow()
        self.modified = datetime.datetime.utcnow()
        return super(QuickNotes, self).save(*args, **kwargs)


class Attachment(models.Model):
    note = models.ForeignKey(QuickNotes, on_delete=models.CASCADE, related_name="attachments")
    file = paste_image.PasteImageField(upload_to="quick_notes/%Y/%m/%d/")
