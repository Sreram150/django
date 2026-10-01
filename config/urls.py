from django.contrib import admin
from django.urls import path, include

from accounts.views import login_page

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home page → Login page
    path("", login_page, name="home"),

    # Accounts URLs
    path("", include("accounts.urls")),
]