from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, Hod_views
from .Conerence_management import Staff_views, Participant_Views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('base/', views.BASE, name='base'),
                  path('login/', views.LOGIN, name='login'),
                  path('', views.LOGIN, name='login'),
                  path('doLogin', views.doLogin, name='doLogin'),
                  path('Hod/Home', Hod_views.HOME, name='hod_home'),
                  path('Profile', views.PROFILE, name='profile'),
                  path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
                  path('doLogout', views.doLogout, name='logout'),

                  path('Hod/Student/Download', Hod_views.download_participants, name='download_participants'),
                  path('Hod/Student/Add', Hod_views.ADD_STUDENT, name='add_student'),
                  path('Hod/Student/View', Hod_views.VIEW_STUDENT, name='view_student'),
                  path('Hod/Student/Edit/<str:id>', Hod_views.EDIT_STUDENT, name='edit_student'),
                  path('Hod/Student/Update', Hod_views.UPDATE_STUDENT, name='update_student'),
                  path('Hod/Student/Delete/<str:admin>', Hod_views.DELETE_STUDENT, name='delete_student'),

                  path('Hod/Department/Download', Hod_views.download_departments, name='download_departments'),
                  path('Hod/Department/Add', Hod_views.ADD_DEPARTMENT, name='add_department'),
                  path('Hod/Department/View', Hod_views.VIEW_DEPARTMENT, name='view_department'),
                  path('Hod/Department/Edit/<str:id>', Hod_views.EDIT_DEPARTMENT, name='edit_department'),
                  path('Hod/Department/Update', Hod_views.UPDATE_DEPARTMENT, name='update_department'),
                  path('Hod/Department/Delete/<str:id>', Hod_views.DELETE_DEPARTMENT, name='delete_department'),

                  path('Hod/Staff/Download', Hod_views.download_staff, name='download_staff'),
                  path('Hod/Staff/Add', Hod_views.ADD_STAFF, name='add_staff'),
                  path('Hod/Staff/View', Hod_views.VIEW_STAFF, name='view_staff'),
                  path('Hod/Staff/Edit/<str:id>', Hod_views.EDIT_STAFF, name='edit_staff'),
                  path('Hod/Staff/Update', Hod_views.UPDATE_STAFF, name='update_staff'),
                  path('Hod/Staff/Delete/<str:admin>', Hod_views.DELETE_STAFF, name='delete_staff'),
                  path('Hod/Staff/Send_Notification', Hod_views.STAFF_SEND_NOTIFICATION,
                       name='staff_send_notification'),
                  path('Hod/Staff/Save_Notification', Hod_views.STAFF_SAVE_NOTIFICATION,
                       name='staff_save_notification'),
                  path('Hod/Participant/Send_Notification', Hod_views.PART_SEND_NOTIFICATION,
                       name='participant_send_notification'),
                  path('Hod/Participant/Save_Notification', Hod_views.PART_SAVE_NOTIFICATION,
                       name='participant_save_notification'),
                  path('Hod/Subject/Download', Hod_views.download_subjects, name='download_subjects'),
                  path('Hod/Subject/Add', Hod_views.ADD_SUBJECT, name='add_subject'),
                  path('Hod/Subject/View', Hod_views.VIEW_SUBJECT, name='hod_view_subject'),
                  path('Hod/Subject/Edit/<str:id>', Hod_views.EDIT_SUBJECT, name='edit_subject'),
                  path('Hod/Subject/Update', Hod_views.UPDATE_SUBJECT, name='update_subject'),
                  path('Hod/Subject/Delete/<str:id>', Hod_views.DELETE_SUBJECT, name='delete_subject'),
                  path('Staff/hod_view_attendance', Hod_views.HOD_VIEW_ATTENDANCE, name='hod_view_attendance'),
                  path('Hod/Session/Add', Hod_views.ADD_SESSION, name='add_session'),
                  path('Hod/Session/View', Hod_views.VIEW_SESSION, name='view_session'),
                  path('Hod/Session/Edit/<str:id>', Hod_views.EDIT_SESSION, name='edit_session'),
                  path('Hod/Session/Update', Hod_views.UPDATE_SESSION, name='update_session'),
                  path('Hod/Session/Delete/<str:id>', Hod_views.DELETE_SESSION, name='delete_session'),
                  path('Hod/Staff/Leave_view', Hod_views.Staff_Leave_view, name='staff_leave_view'),
                  path('Hod/Staff/Staff_approve_leave/<str:id>/', Hod_views.Staff_approve_leave,
                       name='staff_approve_leave'),
                  path('Hod/Staff/Staff_decline_leave/<str:id>/', Hod_views.Staff_decline_leave,
                       name='staff_decline_leave'),
                  path('Hod/Participant/Leave_view', Hod_views.Participant_Leave_view, name='participant_leave_view'),
                  path('Hod/Participant/Participant_approve_leave/<str:id>/', Hod_views.Participant_approve_leave,
                       name='participant_approve_leave'),
                  path('Hod/Participant/Participant_decline_leave/<str:id>/', Hod_views.Participant_decline_leave,
                       name='participant_decline_leave'),
                  path('Staff/Home', Staff_views.HOME, name='staff_home'),
                  path('Staff/Notifications', Staff_views.NOTIFICATIONS, name='staff_notifications'),
                  path('Staff/apply_leave', Staff_views.APPLY_LEAVE, name='apply_leave'),
                  path('Staff/apply_leave_save', Staff_views.APPLY_LEAVE_SAVE, name='apply_leave_save'),
                  path('mark_as_seen/<str:status>/', Staff_views.mark_as_seen, name='mark_as_seen'),
                  path('Staff/staff_take_attendance', Staff_views.STAFF_TAKE_ATTENDANCE, name='staff_take_attendance'),
                  path('Staff/staff_save_attendance', Staff_views.STAFF_SAVE_ATTENDANCE, name='staff_save_attendance'),
                  path('Staff/staff_view_attendance', Staff_views.STAFF_VIEW_ATTENDANCE, name='staff_view_attendance'),
                  path('Staff/staff_view_subject', Staff_views.STAFF_VIEW_SUBJECT, name='staff_view_subject'),
                  path('Participant/Home', Participant_Views.HOME, name='participant_home'),
                  path('Participant/Notifications', Participant_Views.NOTIFICATIONS, name='participant_notifications'),
                  path('part_mark_as_seen/<str:status>/', Participant_Views.part_mark_as_seen,
                       name='part_mark_as_seen'),
                  path('Participant/part_apply_leave', Participant_Views.PART_APPLY_LEAVE, name='part_apply_leave'),
                  path('Participant/part_apply_leave_save', Participant_Views.PART_APPLY_LEAVE_SAVE,
                       name='part_apply_leave_save'),
                  path('Participant/view_attendance', Participant_Views.VIEW_ATTENDANCE, name='view_attendance'),
                  path('Participant/view_subject', Participant_Views.VIEW_SUBJECT, name='view_subject'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
