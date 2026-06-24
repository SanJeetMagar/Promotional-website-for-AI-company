from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

# Import models from your apps
from src.apps.accounts.models import CustomUser
from src.apps.inquiry.models import Inquiry
from src.apps.blog.models import BlogPost, BlogStatus
from src.apps.events.models import Event, EventRegistration, EventStatus
from src.apps.career.models import JobPosting, CV
from src.apps.product.models import Product

class AdminDashboardAnalyticsView(APIView):
    """
    Provides aggregated statistics for the Custom Admin Dashboard home screen.
    Requires Admin/Staff permissions.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        # 1. Accounts Analytics
        total_users = CustomUser.objects.count()
        new_users_30d = CustomUser.objects.filter(last_login__gte=thirty_days_ago).count()

        # 2. Inquiries Analytics
        inquiries = {
            "total": Inquiry.objects.count(),
            "new": Inquiry.objects.filter(status='NEW').count(),
            "in_progress": Inquiry.objects.filter(status='IN_PROGRESS').count(),
            "resolved": Inquiry.objects.filter(status='RESOLVED').count(),
        }

        # 3. Blog Analytics
        total_views = BlogPost.objects.aggregate(Sum('view_count'))['view_count__sum'] or 0
        blogs = {
            "total_posts": BlogPost.objects.count(),
            "published": BlogPost.objects.filter(status=BlogStatus.PUBLISHED).count(),
            "total_views": total_views
        }

        # 4. Events Analytics
        events = {
            "upcoming_events": Event.objects.filter(status=EventStatus.UPCOMING).count(),
            "total_registrations": EventRegistration.objects.count(),
            "confirmed_registrations": EventRegistration.objects.filter(status='confirmed').count()
        }

        # 5. Career/HR Analytics
        careers = {
            "active_job_postings": JobPosting.objects.filter(status='published').count(),
            "total_cvs_received": CV.objects.count()
        }

        # 6. Product Analytics
        products = {
            "active_products": Product.objects.filter(is_active=True).count()
        }

        # Return the aggregated JSON payload
        return Response({
            "users": {
                "total": total_users,
                "active_last_30_days": new_users_30d
            },
            "inquiries": inquiries,
            "blogs": blogs,
            "events": events,
            "careers": careers,
            "products": products
        })