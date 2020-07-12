from django.db import models
from django.db.models import Sum
from django.db.models import Count
from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import CurrentUserDefault
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from dag_django_autogenerate.mixins import BaseModel


get_model = apps.get_model


class Apps(BaseModel):

    title = models.CharField(max_length=5000)
    slug = models.CharField(max_length=5000)

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

    title = models.CharField(max_length=50)
    verbose_name = models.CharField(max_length=50)
    verbose_name_plural = models.CharField(max_length=50)

    django_modeladmin = models.BooleanField(default=False)
    django_tabularinline = models.BooleanField(default=False)

    rendered_model = models.TextField(blank=True, null=True)
    rendered_form = models.TextField(blank=True, null=True)
    rendered_admin = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.app, self.title)

    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')
        ordering = ['app', 'title']


class Fields(BaseModel):

    model = models.ForeignKey(
        'Models',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_models',
    )
    field_type = models.ForeignKey(
        'FieldTypes',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_field_types',
    )
    foreignkey = models.ForeignKey(
        'Models',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_foreignkey',
        blank=True,
        null=True,
    )
    choice = models.ForeignKey(
        'Choices',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_choices',
        blank=True,
        null=True,
    )

    title = models.CharField(max_length=50, )
    slug = models.CharField(max_length=50, )
    help_text = models.CharField(max_length=200, )

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


class FieldTypes(BaseModel):

    title = models.CharField(max_length=100)
    model_code = models.TextField(blank=True, null=True)

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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Model Function')
        verbose_name_plural = _('Model Functions')
        ordering = ['model', 'title']


class Choices(BaseModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')
        ordering = ['title']


class ChoicesValues(BaseModel):
    choice = models.ForeignKey(
        'Choices',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_choices'
    )
    key = models.CharField(max_length=5000)
    value = models.CharField(max_length=5000)

    def __str__(self):
        return '{} - {}'.format(self.choice, self.key)

    class Meta:
        verbose_name = _('Choice Value')
        verbose_name_plural = _('Choice Values')
        ordering = ['choice', 'key']


class Variables(BaseModel):
    title = models.CharField(max_length=200)
    key = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Variable')
        verbose_name_plural = _('Variables')
        ordering = ['title']
