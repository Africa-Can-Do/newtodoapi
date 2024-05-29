# todoApi

## Block user for 3 trials of login
1. install django-axes `pip install django-axes`
2. add `axe` to todo/settings.py
3. add `axes.middleware.AxesMiddleware` to MIDDLEWARE the todo/settings.py
4. add the following to todo/settings.py
  ```python
      AUTHENTICATION_BACKENDS = [
        'axes.backends.AxesBackend', # Axes must be first
        'django.contrib.auth.backends.ModelBackend',
     ]

      AXES_LOCKOUT_TEMPLATE = 'lockout.html'
      AXES_FAILURE_LIMIT = 3
      AXES_COOLOFF_TIME = 0.1
      AXES_RESET_ON_SUCCESS=True
      AXES_LOCKOUT_TEMPLATE = 'lockout.html'
  ```
5. Create a lockout.html file inside account/templates and paste the following code
   ```HTML
   <!-- lockout.html -->
    <html>
    <body>
        <h1>You have been blocked. Try again in 10 minutes.</h1>
    </body>
    </html>
   ```
6. Run `python manage.py check` to check for any issues or errors
7. Run `python manage.py migrate`
8. Run `python manage.py axes_reset`
8. Run `python manage.py runserver`

### How to send email using celery

1. install celery `pip install celery`

2. Update settings.py with the following
   ```python
    # set the celery broker URL 
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
      
    # set the celery result backend 
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
      
    # set the celery timezone 
    CELERY_TIMEZONE = 'UTC'

3. Install redis [([click here](https://github.com/tporadowski/redis/releases))]

4. When you are done installing, open the installed file and click on redis-cli

5. Create a celery.py file when settings.py can be found and paste this there.
  ```python
    from __future__ import absolute_import,unicode_literals
    import os
    from celery import Celery

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.settings")
    app = Celery("todo")

    #we are using asia/kolkata time so we are making it False
    app.conf.enable_utc=True
    app.conf.update(timezone='UTC')

    app.config_from_object("django.conf:settings", namespace="CELERY")

    app.autodiscover_tasks()

    @app.task(bind=True)
    def debug_task(self):
        print(f"Request: {self.request!r}")
  ```

6. Create your task, in our case update the helpers.py file with this:
  ```python
  from django.core.mail import send_mail
  from django.template.loader import render_to_string
  from django.utils.html import strip_tags
  from django.conf import settings
  from celery import shared_task
  from account.models import CustomUser

  @shared_task
  def send_verification_email(user_id):
      user = CustomUser.objects.get(id=user_id)
      token = user.generate_verification_token()

      subject = 'Verify Your Email'
      context = {
          'user': user,
          'verification_token': token,
      }
      html_message = render_to_string('verification_email.html', context)
      plain_message = strip_tags(html_message)
      send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
  ```

7. Install redis (python package) `pip install redis`

8. Run django server `python manage.py runserver`

9. Open a different terminal and run `celery -A todo.celery worker --pool=solo -l INFO`

10. Try to register a user . Done !!!

#### Monitor your tasks
If you want to monitor your tasks. Like it is in pending state or it is successfully executed by celery then you can also see all that. So for that install django-celery-results

1. type `pip install django-celery-results` in your terminal

2. Update your settings.py with this:
  CELERY_RESULT_BACKEND = "django-db"

3. Add `'django_celery_results'` to INSTALLED_APPS in your settings.py

4. Update your __init__.py with this:
  ```python
  from .celery import app as celery_app

  __all__ = ("celery_app",)
  ```

5. Then make migrations and migrate the models to database
  python manage.py makemigrations
  python manage.py migrate
  python manage.py  createsuperuser 
  python manage.py runserver

### Using Swagger for API documentation

1. Install swagger, run in you terminal 
  pip install -U drf-yasg

2. Add `drf_yasg` to your INSTALLED_APPS in settings.py

3. Add the following to your urls.py (where settings.py can be located)

  ```python
  from django.urls import re_path
  from rest_framework import permissions
  from drf_yasg.views import get_schema_view
  from drf_yasg import openapi

  ...

  schema_view = get_schema_view(
    openapi.Info(
        title="API docs",
        default_version='v1',
        description="Todo Application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@xyz.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
  )

  urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ...
  ]
  ```
4. Start your Django server and type localhost:8000/docs/ in your browser
