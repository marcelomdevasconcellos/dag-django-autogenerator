APP_CONTENT = """from django.apps import AppConfig


class %sConfig(AppConfig):
    name = '%s'
"""

INSTALLED_APPS = """INSTALLED_APPS = [{% for a in apps %}
    '{{a.slug}}.apps.{{a.title_unicode}}Config',{% endfor %}
]
"""


CHOICES_CONTENT = """import os

{% for f in fields %}{% if f.choices %}
{{f.choices_name}} = {{f.choices_value}}

{% endif %}{% endfor %}"""


MODEL_CONTENT = """import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
from django.db import models
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import CurrentUserDefault
from config.mixins import BaseModel
from .choices import *{% for m in models %}
{{m.rendered_model}}{% endfor %}"""


ADMIN_CONTENT = """import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
from datetime import datetime
import requests

from django.contrib import admin
from django.forms import Select, Textarea
from django.utils.html import format_html
from config.mixins import AuditoriaAdmin, AuditoriaAdminInline, AuditoriaAdminStackedInline

from .models import ({% for m in models %}
    {{m.title}},{% endfor %}
){% for m in models %}
{{m.rendered_admin}}{% endfor %}"""


MODEL_CLASS = """


class {{m.title}}(BaseModel):

    cols = {{% for f in fields %}
        '{{f.slug}}': {{f.bootstrap_columns}},{% endfor %}}
    
    {% for f in fields %}{{f.rendered_model_django}}
    {% endfor %}

    class Meta:
        verbose_name = '{{m.verbose_name}}'
        verbose_name_plural = '{{m.verbose_name_plural}}'"""


ADMIN_CLASS = """


{% for mi in m.inline_models.all %}
class {{mi.title}}InlineAdmin(AuditoriaAdminInline):
    model = {{mi.title}}
    list_display = ({% for f in mi.fields %}{% if f.in_list_display %}
        '{{f.slug}}',{% endif %}{% endfor %}
    )


{% endfor %}@admin.register({{m.title}})
class {{m.title}}Admin(AuditoriaAdmin):
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
    readonly_fields = AuditoriaAdmin.readonly_fields + ({% for f in fields %}{% if f.is_readonly %}
        '{{f.slug}}',{% endif %}{% endfor %}
    )
    inlines = [{% for mi in m.inline_models.all %}
        {{mi.title}}InlineAdmin,{% endfor %}
    ]"""


FIELD_CHARFIELD = """{{f.slug_unicode}} = models.CharField(
        '{{f.verbose_name}}', {% if f.help_text %}
        help_text='{{f.help_text}}', {% endif %}{% if f.choices %}
        choices={{f.choices_name}}, {% endif %}
        max_length={{f.max_length|valor}}, {% if f.is_blank %}
        blank=True, {% endif %}{% if f.is_null %}
        null=True, {% endif %}{% if f.default_value or f.default_value == 0 %}
        default={% if f.default_value|is_int %}{{f.default_value}}{% else %}'{{f.default_value}}'{% endif %}, {% endif %})"""


FIELD_TEXTFIELD = """{{f.slug_unicode}} = models.TextField(
        '{{f.verbose_name}}', {% if f.help_text %}
        help_text='{{f.help_text}}', {% endif %}{% if f.is_blank %}
        blank=True, {% endif %}{% if f.is_null %}
        null=True, {% endif %}{% if f.default_value or f.default_value == 0 %}
        default={% if f.default_value|is_int %}{{f.default_value}}{% else %}'{{f.default_value}}'{% endif %}, {% endif %})"""


FIELD_DECIMALFIELD = """{{f.slug_unicode}} = models.DecimalField(
        '{{f.verbose_name}}', {% if f.help_text %}
        help_text='{{f.help_text}}', {% endif %} 
        max_digits=15, 
        decimal_places=2, {% if f.is_blank %}
        blank=True, {% endif %}{% if f.is_null %}
        null=True, {% endif %}{% if f.default_value or f.default_value == 0 %}
        default={% if f.default_value|is_int %}{{f.default_value}}{% else %}'{{f.default_value}}'{% endif %}, {% endif %})"""


FIELD_INTEGERFIELD = """{{f.slug_unicode}} = models.IntegerField(
        '{{f.verbose_name}}', {% if f.help_text %}
        help_text='{{f.help_text}}', {% endif %}{% if f.choices %}
        choices={{f.choices_name}}, {% endif %}{% if f.is_blank %}
        blank=True, {% endif %}{% if f.is_null %}
        null=True, {% endif %}{% if f.default_value or f.default_value == 0 %}
        default={% if f.default_value|is_int %}{{f.default_value}}{% else %}'{{f.default_value}}'{% endif %}, {% endif %})"""


FIELD_DATEFIELD = """{{f.slug_unicode}} = models.DateField(
        '{{f.verbose_name}}', {% if f.help_text %}
        help_text='{{f.help_text}}', {% endif %}{% if f.is_blank %}
        blank=True, {% endif %}{% if f.is_null %}
        null=True, {% endif %}{% if f.default_value or f.default_value == 0 %}
        default={% if f.default_value|is_int %}{{f.default_value}}{% else %}'{{f.default_value}}'{% endif %}, {% endif %})"""


FIELD_FOREIGNKEY = """{{f.slug_unicode}} = models.ForeignKey(
        '{{f.foreignkey.app.slug}}.{{f.foreignkey.title_unicode}}', 
        on_delete=models.PROTECT,  
        related_name='%(class)s_{{f.slug_unicode}}', {% if f.help_text %}
        help_text='{{f.help_text}}', {% endif %}{% if f.is_blank %}
        blank=True, {% endif %}{% if f.is_null %}
        null=True, {% endif %}{% if f.default_value or f.default_value == 0 %}
        default={% if f.default_value|is_int %}{{f.default_value}}{% else %}'{{f.default_value}}'{% endif %}, {% endif %})"""


FIELD_TYPES = {
    'IntegerField': FIELD_INTEGERFIELD,
    'CharField': FIELD_CHARFIELD,
    'DateField': FIELD_DATEFIELD,
    'DecimalField': FIELD_DECIMALFIELD,
    'ForeignKey': FIELD_FOREIGNKEY,
    'TextField': FIELD_TEXTFIELD,
}
