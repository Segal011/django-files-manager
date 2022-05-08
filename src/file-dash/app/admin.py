from django.contrib import admin
from .models import File, Model
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django import forms
from django.utils.html import format_html
from django.urls import reverse
from django.urls import re_path as url
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from .forms import FileForm


class ModelAdminForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = "__all__"

    def validate(self):
        if self.cleaned_data["title"] == "File":
            raise forms.ValidationError("Model could not be named 'File'")

        return self.cleaned_data["title"]


def addition_action(modeladmin, request, queryset):
    raise NotImplementedError()
 

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'owner', 'files_link')
    actions = [addition_action] # TODO fix this https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/
    form = ModelAdminForm
    
    def files_link(self, obj):
        count = obj.file_set.count()
        url = (
            reverse("admin:app_file_changelist")
            + "?"
            + urlencode({"models__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Files</a>', url, count)

    files_link.short_description = "Files"
    

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'owner', 'original', 'model_title', 'file_actions', 'image_tag')
    list_filter = ("selected_model__title", )
    search_fields = ("title__startswith", )


    def model_title(self, obj):
        return format_html("<b><i>{}</i></b>", obj.selected_model.title)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["title"].label = "File name"
        return form

    model_title.short_description = "Model"

    @admin.action(
        permissions=[],
        description='Mark selected stories as published',
    )
    def function_with_permission(self, request, queryset):
        raise NotImplementedError()

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<file_id>.+)/proceed/$',
                self.admin_site.admin_view(self.process_transformation),
                name='file-proceed',
            ),
        ]
        return custom_urls + urls

    def file_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Transform</a>&nbsp;',
            reverse('admin:file-proceed', args=[obj.pk])
        )
        
    file_actions.short_description = 'Account Actions'
    file_actions.allow_tags = True

    def process_transformation(self, request, file_id, *args, **kwargs):
        return self.process_action(
            request=request,
            file_id=file_id,
            action_form=FileForm,
            action_title='Tranformation',
        )

    def process_action(
        self,
        request,
        file_id,
        action_form,
        action_title
   ):
        file = self.get_object(request, file_id)

        if request.method != 'POST':
            form = action_form()

        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    form.save(file, request.user)
                except Exception as e:
                    # If save() raised, the form will a have a non
                    # field error containing an informative message.
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse(
                        'admin:file_file_proceed',
                       args=[file.pk],
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['file'] = file
        context['title'] = action_title

        return TemplateResponse(
            request,
            'admin/file/file_action.html',
            context,
        )
