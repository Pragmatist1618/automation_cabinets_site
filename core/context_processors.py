from django.conf import settings

def site_settings(request):
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Шкафы автоматики"),
        "SITE_DESCRIPTION": getattr(settings, "SITE_DESCRIPTION", ""),
        "YANDEX_VERIFICATION_CODE": getattr(settings, "YANDEX_VERIFICATION_CODE", ""),
        "YANDEX_MAP_EMBED_URL": getattr(settings, "YANDEX_MAP_EMBED_URL", ""),
    }
