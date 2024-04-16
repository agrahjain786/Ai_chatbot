from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name = 'home'),
    path('login/',views.login , name = 'login'),
    path('logout/',views.logout_user, name = 'logout'),
    path('doubt_assistant/',views.doubt_assistant, name = 'doubt_assistant'),
    path('doubt_assistant_login/',views.doubt_assistant_login, name = 'doubt_assistant_login'),
    path('doubt_assistant_logout/', views.doubt_assistant_logout, name='doubt_assistant_logout'),
]