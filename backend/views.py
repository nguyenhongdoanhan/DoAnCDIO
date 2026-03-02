from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.conf import settings
from django.contrib.auth import update_session_auth_hash

from account.models import Account
from tts.models import TTSRecord   # 🔥 thêm import này

import os
import uuid
import asyncio
import edge_tts


# ================= LOGIN =================

def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

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

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "UI/login.html", {
            "error": "Sai email hoặc mật khẩu"
        })

    return render(request, "UI/login.html")


# ================= DASHBOARD =================

@login_required
def dashboard_page(request):
    plan = getattr(request.user, "plan", "basic")
    max_chars = 20000 if plan == "pro" else 5000

    return render(request, "UI/dashboard.html", {
        "plan": plan,
        "max_chars": max_chars
    })

def logout_view(request):
    logout(request)
    return redirect("login")


# ================= SUBTITLE PAGE =================

@login_required
def subtitle_page(request):
    return render(request, "UI/subtitle.html")


# ================= PARSE SRT =================

def parse_srt(content):
    lines = content.splitlines()
    text_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue
        if line.isdigit():
            continue
        if "-->" in line:
            continue

        text_lines.append(line)

    return " ".join(text_lines)


# ================= SUBTITLE CONVERT =================

@login_required
def subtitle_convert(request):
    if request.method == "POST":
        file = request.FILES.get("subtitle_file")

        if not file:
            return redirect("subtitle")

        content = file.read().decode("utf-8")
        clean_text = parse_srt(content)

        tts_dir = os.path.join(settings.MEDIA_ROOT, "tts")
        os.makedirs(tts_dir, exist_ok=True)

        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(tts_dir, filename)

        async def generate():
            communicate = edge_tts.Communicate(
                clean_text,
                voice="vi-VN-HoaiMyNeural"
            )
            await communicate.save(filepath)

        asyncio.run(generate())

        return FileResponse(
            open(filepath, "rb"),
            as_attachment=True,
            filename=filename
        )

    return redirect("subtitle")


# ================= TASKS PAGE =================

@login_required
def tasks_page(request):
    return render(request, "UI/tasks.html")


# ================= PROJECTS PAGE =================

@login_required
def projects_page(request):
    projects = TTSRecord.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "tts/projects.html", {
        "projects": projects   # 🔥 PHẢI là projects (đúng với template của bạn)
    })


# ================= LIBRARY PAGE =================

@login_required
def library_page(request):
    return render(request, "UI/voice-library.html")


# ================= CLONE PAGE =================

@login_required
def clone_page(request):
    return render(request, "UI/clone.html")


# ================= PRICING PAGE =================

@login_required
def pricing_page(request):
    plan = getattr(request.user, "plan", "basic")
    return render(request, "UI/pricing.html", {
        "plan": plan
    })


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
    # ================= SETTINGS PAGE =================
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def settings_page(request):
    if request.method == "POST":
        user = request.user

        # Update username
        new_username = request.POST.get("username")
        if new_username:
            user.username = new_username

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if current_password and new_password:
            if not user.check_password(current_password):
                messages.error(request, "Mật khẩu hiện tại không đúng.")
            elif new_password != confirm_password:
                messages.error(request, "Mật khẩu mới không khớp.")
            else:
                user.set_password(new_password)
                user.save()

                #  Logout và về login
                logout(request)
                return redirect("login")

        user.save()

    return render(request, "UI/settings.html")