from django.urls import path
from pages import views


urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
]
