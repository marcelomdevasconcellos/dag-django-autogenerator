from django.db import models
from django.db.models import Sum
from django.db.models import Count
from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import CurrentUserDefault
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from config.mixins import BaseModel
from .choices import *
from django.db import models
import jsonfield


get_model = apps.get_model


class Apps(BaseModel):

    title = models.CharField(max_length=5000)
    slug = models.CharField(max_length=5000)
    verbose_name = models.CharField(max_length=50)
    is_check = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('App')
        verbose_name_plural = _('Apps')
        ordering = ['title']


class Models(BaseModel):

    app = models.ForeignKey(
        'Apps',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_models'
    )
    inline_models = models.ManyToManyField(
        'Models',
        related_name='%(class)s_models',
        blank=True,
    )

    title = models.CharField(max_length=200, unique=True)
    verbose_name = models.CharField(max_length=200)
    verbose_name_plural = models.CharField(max_length=200)

    django_modeladmin = models.BooleanField(default=True)

    rendered_model = models.TextField(blank=True, null=True)
    rendered_form = models.TextField(blank=True, null=True)
    rendered_admin = models.TextField(blank=True, null=True)
    is_empty = models.BooleanField(default=True)
    is_check = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.app, self.title)

    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')
        ordering = ['app', 'title']
        unique_together = ['app', 'title']


class Fields(BaseModel):

    model = models.ForeignKey(
        'Models',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_models',
    )
    foreignkey = models.ForeignKey(
        'Models',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_foreignkey',
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=50, )
    help_text = models.TextField(null=True, blank=True)
    verbose_name = models.CharField(max_length=200, null=True, blank=True)
    field_type = models.CharField(max_length=20, choices=FIELDTYPES)
    choices = models.TextField(
        'Choices (separated by "|" and breaklines)',
        null=True, blank=True)

    max_length = models.IntegerField(blank=True, null=True)
    default_value = models.CharField(max_length=50, blank=True, null=True)

    is_null = models.BooleanField(default=False)
    is_blank = models.BooleanField(default=False)
    is_unique = models.BooleanField(default=False)
    is_readonly = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=False)
    is_db_index = models.BooleanField(default=False)

    is_ordering = models.BooleanField(default=False)
    order = models.IntegerField()
    is_check = models.BooleanField(default=False)

    is_model_title = models.BooleanField(default=False)
    in_search_fields = models.BooleanField(default=False)
    in_list_filter = models.BooleanField(default=False)
    in_list_display = models.BooleanField(default=False)
    in_field_model = models.BooleanField(default=False)

    rendered_model_django = models.TextField(blank=True, null=True)
    rendered_form_django = models.TextField(blank=True, null=True)
    rendered_table_html = models.TextField(blank=True, null=True)
    rendered_form_html = models.TextField(blank=True, null=True)
    rendered_filter_html = models.TextField(blank=True, null=True)
    rendered_filter_dict = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.model, self.title)

    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')
        ordering = ['model', 'order']
        unique_together = ['model', 'title']


class FieldTypes(BaseModel):

    title = models.CharField(max_length=100, unique=True)
    model_code = models.TextField(blank=True, null=True)
    is_check = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Field Type')
        verbose_name_plural = _('Field Type')
        ordering = ['title']


class CustomModels(BaseModel):
    app = models.ForeignKey(
        'Apps',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_app',
    )
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    model_code = models.TextField(blank=True, null=True)
    admin_code = models.TextField(blank=True, null=True)
    form_code = models.TextField(blank=True, null=True)
    is_check = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Custom Model')
        verbose_name_plural = _('Custom Models')
        ordering = ['app', 'title']


class ModelFunctions(BaseModel):
    model = models.ForeignKey(
        'Models',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_model',
    )
    title = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)
    code = models.TextField()
    is_check = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Model Function')
        verbose_name_plural = _('Model Functions')
        ordering = ['model', 'title']


class Variables(BaseModel):
    title = models.CharField(max_length=200)
    key = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    is_check = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Variable')
        verbose_name_plural = _('Variables')
        ordering = ['title']
