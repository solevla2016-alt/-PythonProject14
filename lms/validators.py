from urllib.parse import urlparse
from rest_framework.serializers import ValidationError


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        link = attrs.get(self.field)

        if not link:
            return

        domain = urlparse(link).netloc.lower()

        if domain not in ("youtube.com", "www.youtube.com"):
            raise ValidationError(
                "Разрешены только ссылки на youtube.com"
            )