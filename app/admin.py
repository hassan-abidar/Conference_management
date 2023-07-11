from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserModel(UserAdmin):
    list_display = ['username', 'user_type']


admin.site.register(CustomUser, UserModel)

admin.site.register(Department)
admin.site.register(Session_Year)
admin.site.register(Participant)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Staff_Notification)
admin.site.register(Staff_Leave)
admin.site.register(Participant_Notification)
admin.site.register(Participant_Leave)
admin.site.register(Attendance)
admin.site.register(Attendance_Report)

