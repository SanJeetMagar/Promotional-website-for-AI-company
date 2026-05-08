# settings.py
from pathlib import Path
import environ

# ── 1. BASE_DIR ───────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ── 2. environ setup (ONE place, with type hints) ─────────────────────
# This replaces your old:
#   env = environ.Env()
#   environ.Env.read_env()
env = environ.Env(
    DEBUG=(bool, True),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
)
environ.Env.read_env(BASE_DIR / ".env")   # explicit path — always works

# ── 3. Core ───────────────────────────────────────────────────────────
SECRET_KEY = env("SECRET_KEY", default="unsafe-secret-key-for-dev-only")
DEBUG = env.bool("DEBUG", default=True)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ALLOWED_HOSTS = ["*"]

# ── 4. Apps ───────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "src.apps.accounts",
    "src.apps.blog",
    "src.apps.career",
    "src.apps.contact",
    "src.apps.inquiry",
    "src.apps.portfolio",
    "src.apps.services",
    "src.apps.testimonials",
    "src.apps.team",
    "src.apps.logo",
    "src.apps.common",
    "src.apps.newsletter",
    "src.apps.about",
    "src.apps.product",
    "src.apps.faq",
]

# ── 5. Middleware ─────────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",            # must be first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",        # must be 3rd
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ── 6. Templates ──────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],   # ← added so email templates work
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ── 7. Database ───────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env.int("DB_PORT"),
    }
}

# ── 8. CORS ───────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    "https://viotechtechnology.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
]

# ── 9. Auth ───────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── 10. DRF ───────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        "contact_anon": "5/hour",
        "contact_user": "20/hour",
    },
}

# ── 11. Celery ────────────────────────────────────────────────────────
CELERY_BROKER_URL = env("REDIS_URL")
CELERY_RESULT_BACKEND = env("REDIS_URL")

# ── 12. Internationalisation ──────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ── 13. Static / Media ────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ── 14. Spectacular ───────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "VioTech Technology Backend",
    "DESCRIPTION": "API for VioTech Backend service",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "CACHE_SCHEMA": False,
}

# ══════════════════════════════════════════════════════════════════════
# 15. EMAIL — fully wired, reads from .env
# ══════════════════════════════════════════════════════════════════════

# Switches between console (local) and smtp (production) via .env
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend"
)
# SMTP connection
EMAIL_HOST          = env("EMAIL_HOST",          default="smtp.gmail.com")
EMAIL_PORT          = env.int("EMAIL_PORT",      default=587)
EMAIL_USE_TLS       = env.bool("EMAIL_USE_TLS",  default=True)
EMAIL_HOST_USER     = env("EMAIL_HOST_USER",     default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

# ── Sender addresses ──────────────────────────────────
DEFAULT_FROM_EMAIL = str(env("DEFAULT_FROM_EMAIL", default="no-reply@localhost"))
SERVER_EMAIL       = str(env("SERVER_EMAIL",        default=DEFAULT_FROM_EMAIL))

# ── Contact form ──────────────────────────────────────
CONTACT_ADMIN_EMAIL = str(env("CONTACT_ADMIN_EMAIL", default="admin@localhost"))
# Who receives Django's automatic crash alert emails
ADMINS = [("SanJeet", env("ADMIN_EMAIL", default="admin@localhost"))]