from django.urls import path

from .views import login, sign_up, logout


urlpatterns = [
    path('login/', login),
    path('signup/', sign_up),
    path('logout/', logout)
]
