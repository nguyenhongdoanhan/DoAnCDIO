from rest_framework import serializers
from .models import TTSRecord


class TTSCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=20000)
    voice = serializers.CharField(required=False, allow_blank=True)
    rate = serializers.IntegerField(required=False)
    pitch = serializers.IntegerField(required=False)


class TTSDetailSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()

    class Meta:
        model = TTSRecord
        fields = ['id', 'text', 'audio_url', 'created_at']

    def get_audio_url(self, obj):
        if not obj.audio_file:
            return None

        request = self.context.get('request')

        if request:
            return request.build_absolute_uri(obj.audio_file.url)

        return obj.audio_file.url