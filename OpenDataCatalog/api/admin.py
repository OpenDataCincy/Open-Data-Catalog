from django.contrib import admin

from .models import ThreeOneOne, Arrest, BikeRack, GenericData, CincinnatiPolice


class BikeRackAdmin(admin.ModelAdmin):
    list_display = ['rack_number', 'description', 'street', ]


class CincinnatiPoliceAdmin(admin.ModelAdmin):
    list_display = ['anon_address', 'description', 'create_date', ]

admin.site.register(ThreeOneOne)
admin.site.register(Arrest)
admin.site.register(BikeRack, BikeRackAdmin)
admin.site.register(GenericData)
admin.site.register(CincinnatiPolice, CincinnatiPoliceAdmin)
