from django.db import models
from django.conf import settings


class TTSRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tts_records"
    )

    # Cho phép null để tránh lỗi migration
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    text = models.TextField()

    # Cho phép null để tránh lỗi migration
    voice = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    audio_file = models.FileField(upload_to='tts/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or 'Untitled'} - {self.user}"


class SpeechToText(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="speech_to_texts"
    )

    data = models.TextField()
    type = models.CharField(max_length=10)  # text | file

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SpeechToText {self.id} - {self.user}"


class SpeechUrl(models.Model):
    speech_to_text = models.ForeignKey(
        SpeechToText,
        related_name="speech_urls",
        on_delete=models.CASCADE
    )

    url = models.TextField()
    voice = models.CharField(max_length=100)
    language = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SpeechUrl {self.id}"


# ================================
#  THÊM CHỨC NĂNG TẢI ÂM THANH LÊN
# ================================

class UploadedAudio(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_audios"
    )

    audio_file = models.FileField(upload_to='uploaded_audio/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"UploadedAudio {self.id} - {self.user}"
# ================================
#  VOICE LIBRARY (THƯ VIỆN GIỌNG)
# ================================

class Voice(models.Model):

    GENDER_CHOICES = (
        ("Nam", "Nam"),
        ("Nữ", "Nữ"),
    )

    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # Ảnh đại diện giọng đọc
    image = models.ImageField(upload_to="voices/")

    # File audio nghe thử
    sample_audio = models.FileField(upload_to="voice_samples/")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name