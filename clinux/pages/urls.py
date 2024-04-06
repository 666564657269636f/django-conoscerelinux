from django.urls import path

from . import views

urlpatterns = [
    path("<slug:slug>/", views.StaticPageView.as_view(), name="static-page"),
]
