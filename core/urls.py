from django.urls import path
from .views import *
urlpatterns = [
   path('register/' , register_view , name="register"),
   path("" , login_view , name="login"),
   path('logout/', logout_view , name="logout" ),

   # ======== Path-Dashboard ===============
   path('citizen-dashboard/',citizen_dashboard,name='citizen_dashboard'),

   path('volunteer-dashboard/',volunteer_dashboard,name='volunteer_dashboard'),

   path('staff-dashboard/',staff_dashboard , name='staff_dashboard'),

   path('admin-dashboard/',admin_dashboard,name='admin_dashboard'),

   path('issue/<int:issue_id>' , issue_detail , name='issue_detail'),

   path('my-issues/',my_issues,name='my_issues'),

   path('admin-dashboard/',admin_dashboard,name='admin_dashboard'),

   path('assign-staff/',assign_staff,name='assign_staff'),

   path(
    'create-staff/',create_staff,name='create_staff'
),

path(
    'staff-dashboard/',
    staff_dashboard,
    name='staff_dashboard'
),


path(

    'change-status/<int:issue_id>/',

    change_status,

    name='change_status'

),
]
