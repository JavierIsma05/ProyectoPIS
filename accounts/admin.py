from django.contrib import admin
from .models import Profile

# Register your models here.
#profile detallado
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','address','location','telephone','user_group')
    search_fields = ('location','user__name','user__groups__name')
    list_filter = ('user__groups','location')

    def user_group(self,obj):
        return " - ".join([t.name for t in obj.user.groups.all().order_by('name')])

admin.site.register(Profile,ProfileAdmin)