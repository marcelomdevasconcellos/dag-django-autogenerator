APP_CONTENT = """from django.apps import AppConfig


class %sConfig(AppConfig):
    name = '%s'
"""

INSTALLED_APPS = """INSTALLED_APPS = [{% for a in apps %}
    '{{a.slug}}.apps.{{a.title_unicode}}Config',{% endfor %}
]
"""


MODEL_CONTENT = """from django.db import models
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import CurrentUserDefault
from .choices import *{% for m in models %}
{{m.rendered_model}}{% endfor %}"""


ADMIN_CONTENT = """from datetime import datetime
import requests

from django.contrib import admin
from django.forms import Select, Textarea
from django.utils.html import format_html

from .models import *{% for m in models %}
{{m.rendered_admin}}{% endfor %}"""


MODEL_CLASS = """


class {{m.title}}(models.Model):

    {% for f in fields %}{{f.rendered_model_django}}
    {% endfor %}

    class Meta:
        verbose_name = '{{m.verbose_name}}'
        verbose_name_plural = '{{m.verbose_name_plural}}'"""


ADMIN_CLASS = """


@admin.register({{m.title}})
class {{m.title}}Admin(admin.ModelAdmin):
    actions = []
    search_fields = ({% for f in fields %}{% if f.in_search_fields %}
        '{{f.slug}}',{% endif %}{% endfor %}
    )
    list_filter = ({% for f in fields %}{% if f.in_list_filter %}
        '{{f.slug}}',{% endif %}{% endfor %}
    )
    list_display = ({% for f in fields %}{% if f.in_list_display %}
        '{{f.slug}}',{% endif %}{% endfor %}
    )
    readonly_fields = ({% for f in fields %}{% if f.is_readonly %}
        '{{f.slug}}',{% endif %}{% endfor %}
    )"""
