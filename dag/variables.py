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


MODEL_CONTENT = """# import locale
# locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
from django.db import models
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import CurrentUserDefault
from config.mixins import BaseModel
from .choices import *{% for m in models %}
{{m.rendered_model}}{% endfor %}"""


ADMIN_CONTENT = """# import locale
# locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
from datetime import datetime
import requests

from django.contrib import admin
from django.forms import Select, Textarea
from django.utils.html import format_html
from config.mixins import AuditoriaAdmin, AuditoriaAdminTabularInline, AuditoriaAdminStackedInline

{% if models %}from .models import ({% for m in models %}
    {{m.title}},{% endfor %}
){% endif %}{% for m in models %}
{{m.rendered_admin}}{% endfor %}"""


MODEL_CLASS = """


class {{m.title}}(BaseModel):

    cols = {{% for f in fields %}
        '{{f.slug}}': {{f.bootstrap_columns}},{% endfor %}}
    
    {% for f in fields %}{{f.rendered_model_django}}
    {% endfor %}

    def __str__(self):
        return {{m.model_str}}

    class Meta:
        verbose_name = '{{m.verbose_name}}'
        verbose_name_plural = '{{m.verbose_name_plural}}'"""


ADMIN_CLASS = """


{% for mi in m.modelsinline_model.all %}
class {{mi.model_inline.title}}InlineAdmin(AuditoriaAdmin{% if mi.type_inline %}{{mi.type_inline}}{% else %}TabularInline{% endif %}):
    model = {{mi.model_inline.title}}
    list_display = ({% for f in mi.model_inline.fields %}{% if f.in_list_display %}
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
    inlines = [{% for mi in m.modelsinline_model.all %}
        {{mi.model_inline.title}}InlineAdmin,{% endfor %}
    ]{% if m.is_read_only %}
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False{% endif %}"""


FORM_CONTENT = """from datetime import datetime, date

from django import forms
from django.forms import widgets
from django.db.models import Q

from django_currentuser.middleware import get_current_user{% for m in models %}


class {{m.title}}Form(forms.ModelForm):
    class Meta:
        model = {{m.title}}
        fields = '__all__'{% endfor %}"""


FORM_CLASS = """

class {{m.title}}Form(forms.ModelForm):
    class Meta:
        model = {{m.title}}
        fields = '__all__' """


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


FIELD_BOOLEANFIELD = """{{f.slug_unicode}} = models.BooleanField(
        '{{f.verbose_name}}', {% if f.help_text %}
        help_text='{{f.help_text}}', {% endif %}{% if f.is_blank %}
        blank=True, {% endif %}{% if f.default_value or f.default_value == 0 %}
        default={% if f.default_value %}{{f.default_value}}{% endif %}, {% endif %})"""



FIELD_NULLBOOLEANFIELD = """{{f.slug_unicode}} = models.NullBooleanField(
        '{{f.verbose_name}}', {% if f.help_text %}
        help_text='{{f.help_text}}', {% endif %}{% if f.is_blank %}
        blank=True, {% endif %}{% if f.default_value or f.default_value == 0 %}
        default={% if f.default_value %}{{f.default_value}}{% endif %}, {% endif %})"""


FIELD_TYPES = {
    'IntegerField': FIELD_INTEGERFIELD,
    'CharField': FIELD_CHARFIELD,
    'DateField': FIELD_DATEFIELD,
    'DecimalField': FIELD_DECIMALFIELD,
    'ForeignKey': FIELD_FOREIGNKEY,
    'TextField': FIELD_TEXTFIELD,
    'BooleanField': FIELD_BOOLEANFIELD,
    'NullBooleanField': FIELD_NULLBOOLEANFIELD,
}
