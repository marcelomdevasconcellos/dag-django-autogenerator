import os
from django.shortcuts import render
from django.http import HttpResponse
from dag.variables import (
    APP_CONTENT,
    INSTALLED_APPS,
    MODEL_CONTENT,
    ADMIN_CONTENT,
    CHOICES_CONTENT,
    MODEL_CLASS,
    ADMIN_CLASS,
    FIELD_CHARFIELD,
    FIELD_TEXTFIELD,
    FIELD_DECIMALFIELD,
    FIELD_INTEGERFIELD,
    FIELD_DATEFIELD,
    FIELD_FOREIGNKEY,
    FIELD_TYPES,)
from dag.models import Apps, Models, Fields, FieldTypes
from dag.functions import render_fields_obj, render_models_admins_obj, save_file, read_file
from termcolor import colored

# Create your views here.
# python manage.py graph_models -a -o filename.png


def create_apps_function(for_print=True):

    from django.template import Template, Context
    from dag.models import Apps, Models, Fields
    from config.settings import BASE_DIR
    import os.path

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

    template_model = '{% load templatetags %}{% autoescape off %}' + INSTALLED_APPS + '{% endautoescape %}'
    t = Template(template_model)
    context_apps = Context(context)
    rendered_apps = t.render(context_apps)
    save_file(
        '%s/config/installed_apps.py' % BASE_DIR,
        rendered_apps)

    for app in apps:
        if not os.path.isdir('%s/%s' % (BASE_DIR, app.slug)):
            os.system('mkdir %s/%s' % (BASE_DIR, app.slug))
        if not os.path.isdir('%s/%s/migrations' % (BASE_DIR, app.slug)):
            os.system('mkdir %s/%s/migrations' % (BASE_DIR, app.slug))
        save_file('%s/%s/__init__.py' % (BASE_DIR, app.slug), '')
        save_file('%s/%s/migrations/__init__.py' % (BASE_DIR, app.slug), '')
        save_file('%s/%s/choices.py' % (BASE_DIR, app.slug), '')
        save_file(
            '%s/%s/apps.py' % (BASE_DIR, app.slug),
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

        template_choices = '{% load templatetags %}{% autoescape off %}' + CHOICES_CONTENT + '{% endautoescape %}'
        t = Template(template_choices)
        context_choices = Context(context)
        rendered_choices = t.render(context_choices)
        save_file(
            '%s/%s/choices.py' % (BASE_DIR, app.slug),
            rendered_choices)
        if for_print:
            print(colored("%s ... OK" % app.verbose_name, "green"))



def create_apps(request):
    create_apps_function(for_print=False)
    return HttpResponse("")