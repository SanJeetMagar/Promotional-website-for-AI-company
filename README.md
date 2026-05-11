# VioTech Website Backend

VioTech Website Backend is a Django REST Framework API for the VioTech technology website. It provides the public data and forms used by the frontend, including services, products, careers, blog content, FAQs, testimonials, team information, contact submissions, newsletters, and brand assets.

The project also ships with Swagger and ReDoc documentation, JWT authentication support, PostgreSQL, Celery, Redis, and WhiteNoise for static file serving.

## Features

- REST API built with Django and Django REST Framework
- OpenAPI schema, Swagger UI, and ReDoc documentation
- JWT authentication support
- PostgreSQL database integration
- Celery task processing with Redis as the broker
- Contact form and newsletter submission flows
- Blog, career, product, service, team, testimonial, logo, and FAQ endpoints

## Project Apps

The following apps are exposed through the API routes in this project:

- blog
- career
- contact
- faq
- logo
- newsletter
- product
- services
- team
- testimonials

## API Routes

The main API is mounted under `v1/api/`.

### Documentation

- `/` - Swagger UI
- `/schema/` - OpenAPI schema
- `/redoc/` - ReDoc documentation

### Endpoints

- `/v1/api/team/team-members/` - team member list
- `/v1/api/team/ceo-messages/` - CEO message list
- `/v1/api/contact/` - create contact message
- `/v1/api/contact/social-media/` - social media links
- `/v1/api/testimonials/` - testimonials list
- `/v1/api/logo/` - logo list
- `/v1/api/newsletter/` - newsletter subscription
- `/v1/api/services/` - expertise list
- `/v1/api/product/` - product dropdown list
- `/v1/api/product/<slug>/` - product detail
- `/v1/api/faq/` - FAQ list
- `/v1/api/career/jobs/` - job posting list
- `/v1/api/career/jobs/<slug>/` - job posting detail
- `/v1/api/career/cv/` - CV upload
- `/v1/api/career/jobs/<slug>/cv/` - CV upload for a specific job
- `/v1/api/blog/` - blog post list
- `/v1/api/blog/<slug>/` - blog post detail
- `/v1/api/blog/<slug>/comments/` - create blog comment

## Requirements

- Python 3.12 or newer recommended
- PostgreSQL
- Redis

## Local Setup

1. Create and activate a virtual environment.

	```bash
	python -m venv venv
	source venv/bin/activate
	```

2. Install dependencies.

	```bash
	pip install -r requirements.txt
	```

3. Create a `.env` file in the project root and add the required values.

4. Run database migrations.

	```bash
	python manage.py migrate
	```

5. Create a superuser if you want to use the admin site.

	```bash
	python manage.py createsuperuser
	```

6. Start the development server.

	```bash
	python manage.py runserver
	```

## Environment Variables

The project reads configuration from `.env`.

Required or commonly used values:

- `SECRET_KEY`
- `DEBUG`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `REDIS_URL`
- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`
- `SERVER_EMAIL`
- `CONTACT_ADMIN_EMAIL`
- `ADMIN_EMAIL`

## Celery

Celery is configured to use Redis for both the broker and result backend. Start a worker when you need background tasks such as email-related jobs.

```bash
celery -A config worker -l info
```

## Docker

If you prefer Docker, the repository includes a `docker-compose.yml` and `Dockerfile`. Use them to run the application with the database and any supporting services defined in the compose file.

## Admin and Static Files

- Admin panel: `/admin/`
- Static files are collected into `staticfiles/`
- Media files are served from `media/`

## Notes

- The API uses DRF pagination and filtering.
- The default schema class is configured for drf-spectacular.
- CORS is enabled for the deployed frontend and common local development origins.

