from django.urls import path

from .views import (
    SignupView,
    LoginView,
    ProfileView,

    signup_page,
    login_page,

    user_dashboard,
    admin_dashboard,

    add_product,
    edit_product,
    delete_product,
)


urlpatterns = [

    # =====================================================
    # API
    # =====================================================

    path(
        "api/signup/",
        SignupView.as_view(),
        name="signup"
    ),

    path(
        "api/login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "api/profile/",
        ProfileView.as_view(),
        name="profile"
    ),


    # =====================================================
    # AUTH PAGES
    # =====================================================

    path(
        "signup/",
        signup_page,
        name="signup_page"
    ),

    path(
        "login/",
        login_page,
        name="login_page"
    ),


    # =====================================================
    # DASHBOARDS
    # =====================================================

    path(
        "user-dashboard/",
        user_dashboard,
        name="user_dashboard"
    ),

    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin_dashboard"
    ),


    # =====================================================
    # PRODUCT MANAGEMENT
    # =====================================================

    path(
        "add-product/",
        add_product,
        name="add_product"
    ),

    path(
        "edit-product/<int:product_id>/",
        edit_product,
        name="edit_product"
    ),

    path(
        "delete-product/<int:product_id>/",
        delete_product,
        name="delete_product"
    ),

]