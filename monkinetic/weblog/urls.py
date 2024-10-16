from django.urls import path

from . import views

app_name = "weblog"

urlpatterns = [
    path("", views.index, name="index"),
    path("<year>/<month>/<day>/<slug>", views.view_entry, name="view_entry"),
    path("_post", views.add_entry, name="add_entry"),
    path("feed/", views.BlogFeed()),
]
