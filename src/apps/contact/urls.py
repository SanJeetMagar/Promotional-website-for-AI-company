from .views import ContactMessageCreateView, SocialMediaLinkListView
from django.urls import path    

urlpatterns = [
    path('', ContactMessageCreateView.as_view(), name='contact-message-create'),
    path('social-media/', SocialMediaLinkListView.as_view(), name='social-media-links'),
]