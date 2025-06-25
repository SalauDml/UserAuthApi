from django.urls import path,include
from .views import RegView,LoginView,ProfileView

urlpatterns = [
    path('register/',RegView.as_view()),
    path('login/',LoginView.as_view()),
    path('profile/',ProfileView.as_view(),)

]
