from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer
from .models import Product


# =========================================================
# SIGNUP API
# =========================================================

class SignupView(APIView):

    def post(self, request):

        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "Account created successfully",
                    "username": user.username,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# LOGIN API
# =========================================================

class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:

            return Response(
                {
                    "error": "Invalid username or password"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # =================================================
        # ADMIN LOGIN
        # =================================================

        if role == "admin":

            if not user.is_superuser:

                return Response(
                    {
                        "error": "You are not an admin"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        # =================================================
        # USER LOGIN
        # =================================================

        elif role == "user":

            if user.is_superuser:

                return Response(
                    {
                        "error": "Admin accounts must login as admin"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        else:

            return Response(
                {
                    "error": "Invalid role"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =================================================
        # CREATE DJANGO LOGIN SESSION
        # =================================================

        login(request, user)

        # =================================================
        # CREATE JWT TOKENS
        # =================================================

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful",

                "role": role,

                "access": str(
                    refresh.access_token
                ),

                "refresh": str(
                    refresh
                )
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# PROFILE API
# =========================================================

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(
            {
                "message": "You are authenticated!",

                "username": request.user.username,

                "email": request.user.email,

                "is_admin": request.user.is_superuser
            }
        )


# =========================================================
# SIGNUP PAGE
# =========================================================

def signup_page(request):

    return render(
        request,
        "signup.html"
    )


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page(request):

    return render(
        request,
        "login.html"
    )


# =========================================================
# USER DASHBOARD
# =========================================================

def user_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("/login/")

    products = Product.objects.all().order_by("-created_at")

    return render(
        request,
        "user_dashboard.html",
        {
            "products": products
        }
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("/login/")

    if not request.user.is_superuser:
        return redirect("/user-dashboard/")

    products = Product.objects.all().order_by("-created_at")

    return render(
        request,
        "admin_dashboard.html",
        {
            "products": products
        }
    )


# =========================================================
# ADD PRODUCT
# =========================================================

def add_product(request):

    if not request.user.is_authenticated:
        return redirect("/login/")

    if not request.user.is_superuser:
        return redirect("/user-dashboard/")

    if request.method == "POST":

        Product.objects.create(
            name=request.POST.get("name"),
            category=request.POST.get("category"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            description=request.POST.get("description"),
        )

        return redirect("/admin-dashboard/")

    return render(
        request,
        "add_product.html"
    )


# =========================================================
# EDIT PRODUCT
# =========================================================

def edit_product(request, product_id):

    if not request.user.is_authenticated:
        return redirect("/login/")

    if not request.user.is_superuser:
        return redirect("/user-dashboard/")

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        product.name = request.POST.get("name")
        product.category = request.POST.get("category")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.description = request.POST.get("description")

        product.save()

        return redirect("/admin-dashboard/")

    return render(
        request,
        "edit_product.html",
        {
            "product": product
        }
    )


# =========================================================
# DELETE PRODUCT
# =========================================================

def delete_product(request, product_id):

    if not request.user.is_authenticated:
        return redirect("/login/")

    if not request.user.is_superuser:
        return redirect("/user-dashboard/")

    product = get_object_or_404(
        Product,
        id=product_id
    )

    product.delete()

    return redirect("/admin-dashboard/")