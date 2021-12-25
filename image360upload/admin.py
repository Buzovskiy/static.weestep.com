# https://adriennedomingus.com/blog/adding-custom-views-and-templates-to-django-admin

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Image360, Image360Archive, Website, RemoteUpdateImages360Url
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.template.response import TemplateResponse
from .management.commands import import_archives, create_photos_360
from django.contrib import messages
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
import urllib.request
from urllib.error import URLError


@admin.register(Image360Archive)
class Model3dArchiveAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'file_path', 'archive_size']
    list_display_links = ['__str__']
    actions = ['create_photos_360']
    ordering = ['size']

    @admin.display(description=_('Archive size'))
    def archive_size(self, obj):
        return filesizeformat(obj.archive.size)

    @admin.display(description=_('Path to file'))
    def file_path(self, obj):
        return obj.archive.name

    @admin.action(description=_('Create photos 360'))
    def create_photos_360(self, request, queryset):
        create_photos_360.Command().handle(outer_queryset=queryset, request=request)
        messages.success(request, _('Models 360 are created'))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-archives/', self.process_import, name="import_archives"),
        ]
        return my_urls + urls

    def process_import(self, request):
        status = import_archives.Command().handle()
        if status == 'error':
            messages.warning(request, _('Archives no found. Download them on the server'))
        elif status == 'success':
            messages.success(request, _('Archives imported successfully'))
        return HttpResponseRedirect("../")


@admin.register(Image360)
class Image360Admin(admin.ModelAdmin):
    list_display = ['id', 'vendor_code', 'iframe', 'date']
    list_display_links = ['vendor_code']
    fields = ['vendor_code', 'iframe', 'model360', 'date']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.my_request = request
        return qs

    @admin.display(description=_('Image 360'))
    def model360(self, obj):
        url = self.my_request.build_absolute_uri(settings.MEDIA_URL + obj.iframe.name)
        context = {'url': url}
        content = TemplateResponse(self.my_request, 'admin/image360upload/image360/iframe.html', context)
        return mark_safe(content.render().content.decode("utf-8"))

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class RemoteUpdateImages360UrlInline(admin.TabularInline):
    model = RemoteUpdateImages360Url
    extra = 0


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['website', 'api_key']
    inlines = [RemoteUpdateImages360UrlInline]
    actions = ['send_images_on_sites']

    @admin.action(description=_('Send images 360 on chosen websites'))
    def send_images_on_sites(self, request, queryset):
        # websites = RemoteUpdateImages360Url.objects.select_related('website').filter(website__in=queryset)
        websites = queryset.select_related('remoteupdateimages360url')
        for website in websites:
            try:
                print(website.remoteupdateimages360url.url)
                urllib.request.urlopen(website.remoteupdateimages360url.url)
            except (ObjectDoesNotExist, URLError) as e:
                messages.warning(request, mark_safe(f'<b>{website.website}</b>: {e}'))
            else:
                messages.success(
                    request,
                    mark_safe(f'<b>{website.website}</b>: {_("Images 360 are successfully sent")}')
                )

# @admin.register(Unpack3dModel)
# class Unpack3dModelAdmin(admin.ModelAdmin):
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('', self.admin_site.admin_view(self.unpack_view)),
#         ]
#         return my_urls + urls
#
#     # def has_add_permission(self, request, obj=None):
#     #     return False
#
#     def unpack_view(self, request):
#         if request.method == 'POST':
#             form = Unpack3dForm(request.POST)
#             if form.is_valid():
#                 from .management.commands import unpack3d
#                 unpack3d.Command().handle()
#                 return HttpResponseRedirect(request.path_info)
#         else:
#             form = Unpack3dForm()
#         context = dict(
#             self.admin_site.each_context(request),
#             opts=self.model._meta,
#             form=form,
#         )
#         return TemplateResponse(request, "admin/unpack_3d_models.html", context)


# @admin.register(Image360)
# class Unpack3dModelAdmin(admin.ModelAdmin):
#     def get_urls(self):
#
#         # get the default urls
#         urls = super(Unpack3dModelAdmin, self).get_urls()
#         print('hello')
#         # define security urls
#         security_urls = [
#             path('configuration/', self.admin_site.admin_view(self.security_configuration))
#             # Add here more urls if you want following same logic
#         ]
#
#         # Make sure here you place your added urls first than the admin default urls
#         return security_urls + urls
#
#     # Your view definition fn
#     def security_configuration(self, request):
#         context = dict(
#             self.admin_site.each_context(request), # Include common variables for rendering the admin template.
#             something="test",
#         )
#         return TemplateResponse(request, "change_list.html", context)


# class MyAdminSite(AdminSite):
#     site_header = 'Monty Python'
#
#


# def my_custom_view(request):
#     # return HttpResponse('Admin Custom View', )
#     # return render(request, template_name='admin/unpack3dmodels.html')


# @admin.register(Unpack3dModel)
# class DummyModelAdmin(admin.ModelAdmin):
#     def get_urls(self):
#         # view_name = '{}_{}_changelist'.format(
#         #     self.model._meta.app_label, self.model._meta.model_name)
#         # # view_name = 'Upload 3d models'
#         # return [
#         #     path('', self.my_view, name=view_name),
#         # ]
#         urls = super().get_urls()
#         opts = self.model._meta
#         # context = dict(
#         #     # Include common variables for rendering the admin template.
#         #     self.admin_site.each_context(self.get_request()),
#         #     # Anything else you want in the context...
#         #     # opts=Unpack3dModel._meta,
#         # )
#         # print(self.get_request())
#         my_urls = [
#             path('', self.admin_site.admin_view(self.my_view)),
#         ]
#         return my_urls + urls
#
#
#     def my_view(self, request):
#         # ...
#         # cl = self.get_changelist_instance(request)
#         context = dict(
#             # Include common variables for rendering the admin template.
#             self.admin_site.each_context(request),
#             # Anything else you want in the context...
#             opts=self.model._meta,
#
#         )
#         print(self.model._meta.app_label)
#         return TemplateResponse(request, "admin/sometemplate.html", context)


# admin.site.register(Unpack3dModel, DummyModelAdmin)
# admin.site.register(DummyModel, DummyModelAdmin)
# admin.site.register(DummyModel)

# myadminsite = MyAdminSite(name='rrr')
# myadminsite.register(DummyModel)


# class Unpack3dAdmin(admin.ModelAdmin):
#     change_form_template = 'admin/unpack3dmodels.html'
