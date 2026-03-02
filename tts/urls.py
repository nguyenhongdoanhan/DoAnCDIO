from django.urls import path
from .views import UploadAudioAPIView
from .views import (
    TextToSpeechAPIView,
    TTSDetailAPIView,
    project_list,
    upload_text_file,
    UploadAudioAPIView,
)

urlpatterns = [
    # TTS API
    path('tts/', TextToSpeechAPIView.as_view(), name='tts-create'),
    path('tts/<int:pk>/', TTSDetailAPIView.as_view(), name='tts-detail'),
    path("upload-audio/", UploadAudioAPIView.as_view(), name="upload-audio"),
    
    

    # Projects page
    path("projects/", project_list, name="projects"),

    # Upload docx/pdf
    path("upload-text/", upload_text_file, name="upload_text_file"),
]