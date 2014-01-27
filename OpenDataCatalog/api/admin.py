from django.contrib import admin

from .models import ThreeOneOne, Arrest, BikeRack


class BikeRackAdmin(admin.ModelAdmin):
    list_display = ['rack_number', 'description', 'street', ]

admin.site.register(ThreeOneOne)
admin.site.register(Arrest)
admin.site.register(BikeRack)
