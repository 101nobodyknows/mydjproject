from . import views
from django.urls import path

urlpatterns = [
   path('sign-up/',views.sign, name='sign'),
   path('log-in/',views.log, name='log'),
   path('profile', views.account_details, name='account_details'),
   path('', views.logout_user, name='logout'),
   path('edit_user_<int:user_id>', views.edit_user, name='edit_user'),
   path('edit_email_<int:user_id>', views.edit_email, name='edit_email'),
   path('edit_password_<int:user_id>', views.edit_user_psw, name='edit_user_psw'),
   path('delete_user_<int:user_id>', views.delete_user, name='delete_user')
]