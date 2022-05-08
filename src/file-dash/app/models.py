from email.policy import default
from django.db import models
from django.conf import settings
from django.utils.html import mark_safe


class FileType(models.TextChoices):
    MODEL = "Model"
    IMAGE = "Image"
    MP3 = "MP3"
    OTHER = "Other"


class AbstractFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=120)
    type =models.CharField(
        max_length=5,
        choices=FileType.choices,
        default=FileType.OTHER,
    )

    def _str_(self):
        return self.title


class Model(AbstractFile):
    object = models.FileField(upload_to='models', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    parameters = models.JSONField(default={})
    
    class Meta:
        verbose_name_plural = "Models"

    def _str_(self):
        return self.title


class File(AbstractFile):
    is_original = models.BooleanField(default=False)
    object = models.ImageField(upload_to='files', null=True, blank=True)

    original = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    selected_model =  models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, blank=True)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.object))

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name_plural = "Files"

    def _str_(self):
        return self.title 

    def change(self):
        raise NotImplementedError()
