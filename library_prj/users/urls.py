from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view
from library_prj.views import user_dashboard
from library_prj.views import admin_dashboard
from .views import admin_user_list_view
from .views import user_profile
from .views import edit_profile

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("dashboard/", user_dashboard, name="dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path("dashboard/users/", admin_user_list_view, name="admin_user_list"),
    path("profile/", user_profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
]
