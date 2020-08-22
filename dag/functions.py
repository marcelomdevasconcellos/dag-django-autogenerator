from dag.models import *


def save_file(filename, content):
    file = open(filename, "w")
    file.write(content)
    file.close()


def read_file(filename):
    import codecs
    file = codecs.open(filename, "r", "utf-8")
    content = file.read()
    file.close()
    return content


def render_fields_obj(field):
    from django.template import Template, Context
    context = {
        'f': field,
    }
    template = '{% load templatetags %}{% autoescape off %}' + field.type.model_code + '{% endautoescape %}'
    t = Template(template)
    context = Context(context)
    rendered_model_django = t.render(context)
    Fields.objects.\
        filter(id=field.id).\
        update(rendered_model_django=rendered_model_django)


def render_models_admins_obj(model):

    from django.template import Template, Context
    from .variables import MODEL_CLASS, ADMIN_CLASS

    fields = Fields.objects.filter(model=model).order_by('order').all()
    context = {
        'fields': fields,
        'm': model,
    }

    template_model = '{% load templatetags %}{% autoescape off %}' + MODEL_CLASS + '{% endautoescape %}'
    t = Template(template_model)
    context_model = Context(context)
    rendered_model = t.render(context_model)

    template_admin = '{% load templatetags %}{% autoescape off %}' + ADMIN_CLASS + '{% endautoescape %}'
    t = Template(template_admin)
    context_admin = Context(context)
    rendered_admin = t.render(context_admin)

    Models.objects.\
        filter(id=model.id).\
        update(
            rendered_model=rendered_model,
            rendered_admin=rendered_admin,
        )

