from django.contrib import admin


from glucose.models import Device, GlucoseLevel, User


admin.site.register(GlucoseLevel)
admin.site.register(User)
admin.site.register(Device)

