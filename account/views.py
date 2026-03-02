from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Account


# ================= TOKEN FUNCTION =================
def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
    }


# ================= HTML SIGNUP =================
def signup_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return render(request, "UI/signup.html", {
                "error": "Vui lòng nhập đầy đủ thông tin"
            })

        if Account.objects.filter(email=email).exists():
            return render(request, "UI/signup.html", {
                "error": "Email đã tồn tại"
            })

        user = Account.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("dashboard")

    return render(request, "UI/signup.html")


# ================= HTML LOGIN =================
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return render(request, "UI/login.html", {
                "error": "Vui lòng nhập đầy đủ thông tin"
            })

        try:
            user_obj = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return render(request, "UI/login.html", {
                "error": "Sai email hoặc mật khẩu"
            })

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is not None and user.is_active:
            login(request, user)
            request.session.save()
            return redirect("dashboard")

        return render(request, "UI/login.html", {
            "error": "Sai email hoặc mật khẩu"
        })

    return render(request, "UI/login.html")


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect("login")


# ================= API AUTH (JWT) =================
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def auth(request):

    mode = request.data.get('mode')
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {"message": "Thiếu email hoặc mật khẩu"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if mode == "register":
        if Account.objects.filter(email=email).exists():
            return Response(
                {"message": "Email đã tồn tại"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = Account.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        tokens = get_tokens(user)

        return Response({
            "message": "Đăng ký thành công",
            "type": "register",
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
        }, status=status.HTTP_201_CREATED)

    elif mode == "login":
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {"message": "Sai email hoặc mật khẩu"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tokens = get_tokens(user)

        return Response({
            "message": "Đăng nhập thành công",
            "type": "login",
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
        }, status=status.HTTP_200_OK)

    return Response(
        {"message": "Mode không hợp lệ"},
        status=status.HTTP_400_BAD_REQUEST
    )


# ================= PROJECTS PAGE =================
@login_required
def projects_view(request):
    return render(request, "UI/projects.html")


# ================= VOICE LIBRARY PAGE =================
@login_required
def library_view(request):
    return render(request, "UI/voice-library.html")


# ================= VOICE CLONING PAGE =================
@login_required
def clone_view(request):
    if request.user.plan != "pro":
        return redirect("pricing")
    return render(request, "UI/clone.html")


# ================= PRICING PAGE =================
@login_required
def pricing_view(request):
    return render(request, "UI/pricing.html")


# ================= UPDATE PLAN =================
@login_required
def update_plan(request):
    if request.method == "POST":
        plan = request.POST.get("plan")

        if plan in ["basic", "pro"]:
            request.user.plan = plan
            request.user.save()

            return JsonResponse({
                "status": "success",
                "plan": plan
            })

    return JsonResponse({"status": "error"})