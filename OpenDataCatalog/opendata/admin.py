from datetime import datetime
from OpenDataCatalog.opendata.models import *
from OpenDataCatalog.comments.models import *
from OpenDataCatalog.suggestions.models import *
from OpenDataCatalog.contest.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

from simplejson import loads, JSONDecodeError

from datetime import date


class UserAdmin(UserAdmin):
    """
    Subclassing the user admin to add password reset email functionality
    """
    actions = list(UserAdmin.actions) + ['password_reset']

    def password_reset(self, request, queryset):
        count = 0
        for user in queryset:
            # Do the password reset stuff.
            form = PasswordResetForm({'email': user.email})

            if form.is_valid():
                opts = {
                    'use_https': request.is_secure(),
                    'token_generator': default_token_generator,
                    'from_email': 'OpenData Cincy<info@opendatacincy.org>',
                    'email_template_name': 'registration/password_reset_email.html',
                    'subject_template_name': 'registration/password_reset_subject.txt',
                    'request': request,
                }

                opts = dict(opts, domain_override=request.get_host())
                form.save(**opts)

                count += 1

        if count == 1:
            message_bit = '1 user was'
        else:
            message_bit = '%s users were' % count

        self.message_user(request, '%s emailed password reset instructions' % message_bit)

    password_reset.short_description = 'Send password reset email'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class UrlImageInline(admin.TabularInline):
    model = UrlImage
    extra = 1


class UrlInline(admin.TabularInline):
    model = Url
    extra = 1
    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls'


class IdeaImageInline(admin.TabularInline):
    model = IdeaImage
    extra = 1


class ResourceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':[('name', 'is_published'), 'description', 'short_description', 'usage', 
            ('organization', 'division'), ('contact_phone', 'contact_email', 'contact_url')], 'classes':['wide']}),
        ('Metadata Fields ', {'fields':['release_date', ('time_period', 'update_frequency'), 
            'updates',
            ('data_formats', 'area_of_interest'), 'proj_coord_sys', 
            ('created_by', 'created'), ('last_updated_by', 'last_updated'),
            ('coord_sys', 'wkt_geometry'),
            'metadata_contact','metadata_notes', 'data_types', 'tags', ], 'classes':['wide']})
    ]
    readonly_fields = ['created_by', 'created', 'last_updated_by', 'last_updated']
    inlines = [UrlInline, ]
    
    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls'
    list_display = ('name', 'organization', 'release_date', 'is_published')
    search_fields = ['name', 'description', 'organization']
    list_filter = ['tags', 'is_published']
    date_heirarchy = 'release_date'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created = datetime.datetime.now()
        
        obj.last_updated_by = request.user
        obj.save()


class UrlImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    search_fields = ['image', 'title', 'description']


class UrlAdmin(admin.ModelAdmin):
    list_display = ('url_label', 'url_type', 'url')
    inlines = [UrlImageInline,]
    list_filter = ['url_type',]


class CoordSystemAdmin(admin.ModelAdmin):
    list_display = ('EPSG_code', 'name')
    search_fields = ['name', 'EPSG_code', 'description']

    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls'


class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':[('title', 'author'),  'description', ('created_by', 'created_by_date'), 
                ('updated_by', 'updated_by_date'), 'resources']})
    ]
    readonly_fields = ['created_by', 'created_by_date', 'updated_by', 'updated_by_date']
    inlines = [IdeaImageInline, ]

    list_display = ('title', 'created_by', 'created_by_date', 'updated_by', 'updated_by_date')
    search_fields = ['title',]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created_by_date = datetime.datetime.now()
        
        obj.updated_by = request.user
        obj.save()


class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'suggested_by', 'completed']
    search_fields = ['text', 'suggested_by']


class SubmissionAdmin(admin.ModelAdmin):   
    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls' 
    list_display = ['user', 'sent_date']
    search_fields = ['email_text', 'user']
    readonly_fields = ['user', ]

    actions = ['convert_to_resource', 'convert_to_nomination', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        
        obj.save()

    def convert_to_nomination(self, request, queryset):
        """
        Converts the submission to a nomination
        """
        count = 0

        for submission in queryset:
            try:
                data = loads(submission.json_text)
            except JSONDecodeError:
                data = None

            if data:
                suggestion = Suggestion()
                suggestion.text = data.get('dataset_name')[:255]
                suggestion.description = data.get('description') if data.get('description') else ''
                suggestion.suggested_by = submission.user
                # suggestion.suggested_date = submission.sent_date
                suggestion.last_modified_date = date.today()
                suggestion.save()

                count += 1

        if count == 1:
            message = '1 submission was converted to a nomination'
        else:
            message = '%s submissions were converted to nominations' % count

        self.message_user(request, message)

    def convert_to_resource(self, request, queryset):
        """
        Converts the submission to a resource
        """
        count = 0
        for submission in queryset:

            try:
                data = loads(submission.json_text)
            except JSONDecodeError:
                # No dice on this submission.
                data = None

            if data:
                # We need to build a new Resource from the submission now.

                # M2M's we need: data_types, coord_sys
                resource = Resource()
                resource.name = data.get('dataset_name')
                resource.short_description = data.get('description', 'n/a')[:255]
                resource.time_period = data.get('time_period', 'n/a')
                resource.release_date = data.get('release_date')
                resource.created_by = request.user
                resource.last_updated_by = request.user
                resource.description = data.get('description', 'n/a')
                resource.wkt_geometry = data.get('wkt_geometry', 0)
                resource.organization = data.get('organization', 'n/a')
                resource.usage = data.get('usage_limitations', 'n/a')
                resource.contact_phone = data.get('contact_phone', 'n/a')
                resource.contact_email = data.get('contact_email', 'user@example.com')
                resource.contact_url = data.get('contact_url', 'http://google.com')
                resource.area_of_interest = data.get('area_of_interest')
                resource.is_published = False
                resource.update_frequency = data.get('update_frequency', '')
                resource.data_formats = data.get('formats', '')

                resource.save()

                for t in data.get('types'):
                    try:
                        data_type = DataType.objects.get(pk=t)

                    except DataType.DoesNotExist:
                        data_type = None

                    if data_type:
                        resource.data_types.add(data_type)
                        resource.save()

                for c in data.get('coord_system'):
                    try:
                        coord = CoordSystem.objects.get(pk=c)

                    except CoordSystem.DoesNotExist:
                        coord = None

                    if coord:
                        resource.coord_sys.add(coord)
                        resource.save()

                count += 1

        if count == 1:
            message = '1 submission was converted to a resource'
        else:
            message = '%s submissions were converted to resources' % count

        self.message_user(request, message)

    convert_to_resource.short_description = 'Convert selected submission(s) to resource(s)'
    convert_to_nomination.short_description = 'Convert selected submission(s) to nomination(s)'


class ODPUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'can_notify', ]
    fieldsets = [(None, {'fields': ['user', 'organization', 'can_notify']}), ]
    readonly_fields = ['user', ]
    list_filter = ['can_notify', ]


class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'nominator', 'contest']
    search_fields = ['title', 'nominator', 'description']
    list_filter = ['contest__title', ]


class EntryInline(admin.StackedInline):
    model = Entry
    extra = 1
    verbose_name_plural = 'Entries'


class ContestAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date']
    search_fields = ['title', 'rules']
    inlines = [EntryInline, ]


class VoteAdmin(admin.ModelAdmin):
    list_display= ['entry', 'user', 'timestamp']
    search_fields = ['entry']
    list_filter = ['entry', ]

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(ODPUserProfile, ODPUserProfileAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaImage)
admin.site.register(Tag)
admin.site.register(UpdateFrequency)
admin.site.register(UrlType)
admin.site.register(CoordSystem, CoordSystemAdmin)
admin.site.register(DataType)
admin.site.register(Url, UrlAdmin)
admin.site.register(UrlImage, UrlImageAdmin)
admin.site.register(Resource, ResourceAdmin)

admin.site.register(Contest, ContestAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Vote, VoteAdmin)

admin.site.register(CommentWithRating)

