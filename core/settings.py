from pathlib import Path
# from django.core.exceptions import ImproperlyConfigured
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
# if not SECRET_KEY:
#     raise ImproperlyConfigured("The DJANGO_SECRET_KEY environment variable is not set.")

from django.core.management.utils import get_random_secret_key
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = bool(os.getenv('DEBUG'))
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",  # Make sure this is installed
    "api",
    "chat_history",
    "model_config",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware", # For handling Cross-Origin Resource Sharing
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom settings
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME')
EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME')

# For ollama
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL')
LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME')
LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE'))

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.AnonRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {'anon': '1000/day'},
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'UNAUTHENTICATED_USER': None,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# For development (be very careful with this in production!)
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_CREDENTIALS = True

# SESSION_COOKIE_SECURE
CSRF_COOKIE_HTTPONLY = True  # Prevents client-side JavaScript from accessing the CSRF token cookie, mitigating XSS attacks.
# CSRF_COOKIE_SECURE = True    # Ensures the CSRF token cookie is only sent over HTTPS connections, protecting it from interception.

# Ensures the session cookie is only sent over HTTPS connections
# SESSION_COOKIE_SECURE = True

# SECURE_HSTS_SECONDS
SECURE_HSTS_SECONDS = 31536000 # 1 year in seconds
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True # Only if you want to submit your domain to the HSTS preload list (read docs carefully)

# REDIRECT HTTP TO HTTPS
# SECURE_SSL_REDIRECT = True

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # Tells Django that the proxy/load balancer is handling SSL, so Django knows the request is secure.
SECURE_CONTENT_TYPE_NOSNIFF = True # Prevents browsers from "sniffing" MIME types, reducing the risk of XSS attacks.
SECURE_BROWSER_XSS_FILTER = True # Activates the browser's XSS filter, offering a layer of defense against cross-site scripting.
X_FRAME_OPTIONS = 'DENY' # Prevents your site from being loaded in an iframe, guarding against clickjacking attacks.