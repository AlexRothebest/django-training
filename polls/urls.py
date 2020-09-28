from django.urls import path

from .views import all_polls, poll, create_poll, poll_results


urlpatterns = [
    path('', all_polls),
    path('<int:poll_id>/', poll),
    path('<int:poll_id>/results/', poll_results),
    path('create/', create_poll)
]
