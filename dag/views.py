import os
from django.shortcuts import render
from django.http import HttpResponse
from .variables import *
from .functions import render_fields_obj, render_models_admins_obj, save_file, read_file


# Create your views here.
# python manage.py graph_models -a -o filename.png


def create_apps(request):
    from django.template import Template, Context
    from dag.models import Apps, Models, Fields
    from config.settings import BASE_DIR

    fields = Fields.objects.order_by('id').all()
    for f in fields:
        render_fields_obj(f)

    models = Models.objects.order_by('id').all()
    for m in models:
        render_models_admins_obj(m)

    apps = Apps.objects.order_by('slug').all()

    context = {
        'apps': apps,
    }

    template_model = '{% load templatetags %}{% autoescape off %}' + INSTALLED_APPS + '{% endautoescape %}'
    t = Template(template_model)
    context_apps = Context(context)
    rendered_apps = t.render(context_apps)
    save_file(
        '%s/config/installed_apps.py' % BASE_DIR,
        rendered_apps)

    for app in apps:

        os.system('mkdir %s/%s' % (BASE_DIR, app.slug))
        os.system('mkdir %s/%s/migrations' % (BASE_DIR, app.slug))
        save_file('%s/%s/__init__.py' % (BASE_DIR, app.slug), '')
        save_file('%s/%s/migrations/__init__.py' % (BASE_DIR, app.slug), '')
        save_file('%s/%s/choices.py' % (BASE_DIR, app.slug), '')
        save_file(
            '%s/%s/apps.py' % (BASE_DIR, app.slug),
            APP_CONTENT % (app.title_unicode(), app.slug))

        model = Models.objects.\
            filter(app=app).\
            order_by('title').all()

        context = {
            'apps': app,
            'models': model,
        }

        template_model = '{% load templatetags %}{% autoescape off %}' + MODEL_CONTENT + '{% endautoescape %}'
        t = Template(template_model)
        context_model = Context(context)
        rendered_model = t.render(context_model)
        save_file(
            '%s/%s/models.py' % (BASE_DIR, app.slug),
            rendered_model)

        template_admin = '{% load templatetags %}{% autoescape off %}' + ADMIN_CONTENT + '{% endautoescape %}'
        t = Template(template_admin)
        context_admin = Context(context)
        rendered_admin = t.render(context_admin)
        save_file(
            '%s/%s/admin.py' % (BASE_DIR, app.slug),
            rendered_admin)

    return HttpResponse("")