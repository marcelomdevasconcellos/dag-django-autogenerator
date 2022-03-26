import os

from django.http import HttpResponse
from termcolor import colored

from dag.functions import render_fields_obj, render_models_admins_obj, save_file
from dag.variables import (
    APP_CONTENT,
    INSTALLED_APPS,
    MODEL_CONTENT,
    ADMIN_CONTENT,
    CHOICES_CONTENT,
)


# Create your views here.
# python manage.py graph_models -a -o filename.png


def create_apps_function(for_print=True):

    from django.template import Template, Context
    from dag.models import Apps, Models, Fields
    from config.settings import BASE_DIR
    from os import path

    apps = Apps.objects.order_by('slug').all()
    models = Models.objects.filter(app__in=apps).order_by('id').all()
    fields = Fields.objects.filter(model__in=models).order_by('id').all()
    for f in fields:
        render_fields_obj(f)
    for m in models:
        render_models_admins_obj(m)

    context = {
        'apps': apps,
    }

    template_model = '{% load templatetags %}{% autoescape off %}' + \
        INSTALLED_APPS + '{% endautoescape %}'
    t = Template(template_model)
    context_apps = Context(context)
    rendered_apps = t.render(context_apps)
    save_file(
        path.join(BASE_DIR, 'config', 'installed_apps.py'),
        rendered_apps)

    for app in apps:
        if not path.isdir('{}'.format(path.join(BASE_DIR, app.slug))):
            os.system('mkdir {}'.format(path.join(BASE_DIR, app.slug)))
        if not path.isdir('{}'.format(path.join(BASE_DIR, app.slug, 'migrations'))):
            os.system('mkdir {}'.format(
                path.join(BASE_DIR, app.slug, 'migrations')))
        save_file(path.join(BASE_DIR, app.slug, '__init__.py'), '')
        save_file(path.join(BASE_DIR, app.slug,
                            'migrations', '__init__.py'), '')
        save_file(path.join(BASE_DIR, app.slug, 'choices.py'), '')
        save_file(
            path.join(BASE_DIR, app.slug, 'apps.py'),
            APP_CONTENT % (app.title_unicode(), app.slug))

        model = Models.objects.\
            filter(app=app).\
            order_by('id').all()

        fields = Fields.objects.\
            filter(model__in=model).\
            order_by('id').all()

        context = {
            'apps': app,
            'models': model,
            'fields': fields,
        }

        template_model = '{% load templatetags %}{% autoescape off %}' + \
            MODEL_CONTENT + '{% endautoescape %}'
        t = Template(template_model)
        context_model = Context(context)
        rendered_model = t.render(context_model)
        save_file(
            path.join(BASE_DIR, app.slug, 'models.py'),
            rendered_model)

        template_admin = '{% load templatetags %}{% autoescape off %}' + \
            ADMIN_CONTENT + '{% endautoescape %}'
        t = Template(template_admin)
        context_admin = Context(context)
        rendered_admin = t.render(context_admin)
        save_file(
            path.join(BASE_DIR, app.slug, 'admin.py'),
            rendered_admin)

        template_choices = '{% load templatetags %}{% autoescape off %}' + \
            CHOICES_CONTENT + '{% endautoescape %}'
        t = Template(template_choices)
        context_choices = Context(context)
        rendered_choices = t.render(context_choices)
        save_file(
            path.join(BASE_DIR, app.slug, 'choices.py'),
            rendered_choices)
        if for_print:
            print(colored("%s ... OK" % app.title, "green"))


def create_apps(request):
    create_apps_function(for_print=False)
    return HttpResponse("")
