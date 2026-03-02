import os
import uuid
import asyncio
import edge_tts
import whisper

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from docx import Document
from PyPDF2 import PdfReader

from .models import TTSRecord, UploadedAudio
from .serializers import TTSCreateSerializer, TTSDetailSerializer


# 🔥 LOAD WHISPER MODEL 1 LẦN
model = whisper.load_model("small")


class TextToSpeechAPIView(APIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    VOICES = {
        "female": "vi-VN-HoaiMyNeural",
        "male": "vi-VN-NamMinhNeural",
    }

    PLAN_LIMITS = {
        "basic": 5000,
        "pro": 20000,
    }

    def post(self, request):

        serializer = TTSCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data["text"]

        user_plan = request.user.plan or "basic"
        max_chars = self.PLAN_LIMITS.get(user_plan, 5000)

        if len(text) > max_chars:
            return Response(
                {
                    "error": f"Gói {user_plan.upper()} chỉ tối đa {max_chars} ký tự"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        voice_key = request.data.get("voice", "female")
        if voice_key not in self.VOICES:
            voice_key = "female"

        selected_voice = self.VOICES[voice_key]

        rate_raw = int(request.data.get("rate", 0))
        pitch_raw = int(request.data.get("pitch", 0))

        rate_value = f"{rate_raw:+d}%"
        pitch_value = f"{pitch_raw:+d}Hz"

        tts_dir = os.path.join(settings.MEDIA_ROOT, "tts")
        os.makedirs(tts_dir, exist_ok=True)

        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(tts_dir, filename)

        async def generate_audio():
            communicate = edge_tts.Communicate(
                text=text,
                voice=selected_voice,
                rate=rate_value,
                pitch=pitch_value,
            )
            await communicate.save(file_path)

        try:
            asyncio.run(generate_audio())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(generate_audio())
            loop.close()

        record = TTSRecord.objects.create(
            user=request.user,
            title=text[:40],
            text=text,
            voice=voice_key,
            audio_file=f"tts/{filename}",
        )

        return Response(
            TTSDetailSerializer(record, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class TTSDetailAPIView(APIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            record = TTSRecord.objects.get(pk=pk, user=request.user)
        except TTSRecord.DoesNotExist:
            return Response(
                {"detail": "Not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            TTSDetailSerializer(record, context={"request": request}).data
        )


@login_required
def project_list(request):
    projects = TTSRecord.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "tts/projects.html", {
        "projects": projects
    })


# ====================================================
# UPLOAD DOCX / PDF → TRÍCH XUẤT TEXT
# ====================================================

@csrf_exempt
def upload_text_file(request):

    if request.method != "POST":
        return JsonResponse({"error": "Chỉ hỗ trợ POST"}, status=405)

    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return JsonResponse({"error": "Không có file"}, status=400)

    file_name = uploaded_file.name
    file_ext = os.path.splitext(file_name)[1].lower()

    if file_ext not in [".docx", ".pdf"]:
        return JsonResponse({"error": "Chỉ hỗ trợ file .docx và .pdf"}, status=400)

    temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, uploaded_file.name)

    with open(temp_path, "wb+") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    extracted_text = ""

    try:
        if file_ext == ".docx":
            doc = Document(temp_path)
            for para in doc.paragraphs:
                extracted_text += para.text + "\n"

        elif file_ext == ".pdf":
            reader = PdfReader(temp_path)
            for page in reader.pages:
                extracted_text += page.extract_text() or ""

    except Exception as e:
        os.remove(temp_path)
        return JsonResponse({"error": str(e)}, status=500)

    os.remove(temp_path)

    return JsonResponse({
        "success": True,
        "text": extracted_text
    })


# ====================================================
# UPLOAD MP3 → CHUYỂN GIỌNG NÓI THÀNH TEXT (WHISPER)
# ====================================================

class UploadAudioAPIView(APIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        file = request.FILES.get("audio")

        if not file:
            return Response({"error": "Không có file"}, status=400)

        temp_path = os.path.join(settings.MEDIA_ROOT, file.name)

        with open(temp_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        result = model.transcribe(temp_path, language="vi", fp16=False)
        print("PATH:", temp_path)
        print("EXISTS:", os.path.exists(temp_path))

        if os.path.exists(temp_path):
           print("SIZE:", os.path.getsize(temp_path))
        text_result = result.get("text", "")

        os.remove(temp_path)

        return Response({
            "text": text_result
        })