from django.apps import AppConfig

class GalleryConfig(AppConfig):
    name = 'src.apps.gallery'  # was 'gallery' — wrong import path
    # WHY: Django uses name to find the app in Python's module system
    # Wrong name = app silently fails to load