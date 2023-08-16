from django.contrib import admin
from .models import *
# Register your models here.

class TutoriaAdmin(admin.ModelAdmin):
    list_display = ('date','description','teacher','status','time_quantity','modalidad','firma')
    list_filter = ('teacher',)

admin.site.register(Tutoria,TutoriaAdmin)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('tuto','student','enabled')
    list_filter = ('tuto','student','enabled')
admin.site.register(Registration,RegistrationAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display=('tuto','student','present')
    list_filter=('tuto','student','present')
    
admin.site.register(Attendance,AttendanceAdmin)

class MarkAdmin(admin.ModelAdmin):
    list_display=('tuto','student','mark_1','mark_2','mark_3','average')
    list_filter=('tuto',)
admin.site.register(Mark,MarkAdmin)

