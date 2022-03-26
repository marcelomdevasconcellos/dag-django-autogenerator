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

    def title_unicode(self):
        import unidecode
        title = self.title.replace(' ', '')
        return unidecode.unidecode(title)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('App')
        verbose_name_plural = _('Apps')
        ordering = ['title']


class Models(BaseModel):

    app = models.ForeignKey(
        'Apps',
        on_delete=models.CASCADE,
        related_name='%(class)s_models'
    )

    title = models.CharField(max_length=200, unique=True)
    verbose_name = models.CharField(max_length=200)
    verbose_name_plural = models.CharField(max_length=200)
    app_slug = models.CharField(max_length=200)
    is_model_admin = models.BooleanField(default=True)
    is_read_only = models.BooleanField(default=False)
    django_inline_models = models.TextField(blank=True, null=True)
    
    rendered_model = models.TextField(blank=True, null=True)
    rendered_form = models.TextField(blank=True, null=True)
    rendered_admin = models.TextField(blank=True, null=True)
    is_empty = models.BooleanField(default=True)
    quant = models.IntegerField(default=0)

    def inline_list(self):
        import unidecode
        inlines = []
        inl = self.django_inline_models.split('\n')
        for i in inl:
            inlines.append(i.split('|'))
        return inlines

    def fields(self):
        return Fields.objects.filter(model=self.id).all()

    def model_str(self):
        fields = Fields.objects.filter(model=self.id, is_model_title=True).all()
        var = []
        emp = []
        for f in fields:
            var.append('self.' + f.slug)
            emp.append('{}')
        return "'{}'.format({})".format(' - '.join(emp), ', '.join(var))

    def title_unicode(self):
        import unidecode
        title = self.title.replace(' ', '').replace('-', '_')
        return unidecode.unidecode(title)

    def __str__(self):
        return '{} - {}'.format(self.app, self.title)

    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')
        ordering = ['app', 'title']
        unique_together = ['app', 'title']


class ModelsInline(BaseModel):

    model = models.ForeignKey(
        'Models',
        on_delete=models.CASCADE,
        related_name='%(class)s_model',
    )

    model_inline = models.ForeignKey(
        'Models',
        on_delete=models.CASCADE,
        related_name='%(class)s_model_inline',
    )

    type_inline = models.CharField(max_length=20, default='TabularInline')

    def __str__(self):
        return '{} - {} - {}'.format(self.model, self.model_inline, self.type_inline)

    class Meta:
        verbose_name = _('Inline Model')
        verbose_name_plural = _('Inline Models')
        ordering = ['model', 'model_inline', 'type_inline']
        unique_together = ['model', 'model_inline', 'type_inline']


class Fields(BaseModel):

    model = models.ForeignKey(
        'Models',
        on_delete=models.CASCADE,
        related_name='%(class)s_models',
    )
    foreignkey = models.ForeignKey(
        'Models',
        on_delete=models.SET_NULL,
        related_name='%(class)s_foreignkey',
        blank=True,
        null=True,
    )
    slug = models.CharField(max_length=50, )
    help_text = models.TextField(null=True, blank=True)
    verbose_name = models.CharField(max_length=500, null=True, blank=True)
    field_type_txt = models.CharField(max_length=50, null=True, blank=True)
    foreignkey_txt = models.CharField(max_length=50, null=True, blank=True)
    choices = models.TextField(
        'Choices (separated by "|" and breaklines)',
        null=True, blank=True)

    max_length = models.IntegerField(blank=True, null=True)
    bootstrap_columns = models.IntegerField(default=6)
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

    model_title = models.CharField(max_length=200, blank=True, null=True)
    fieldtype_title = models.CharField(max_length=100, blank=True, null=True)
    foreignkey_model_title = models.CharField(
        max_length=200, blank=True, null=True)

    rendered_model_django = models.TextField(blank=True, null=True)
    rendered_form_django = models.TextField(blank=True, null=True)
    rendered_table_html = models.TextField(blank=True, null=True)
    rendered_form_html = models.TextField(blank=True, null=True)
    rendered_filter_html = models.TextField(blank=True, null=True)
    rendered_filter_dict = models.TextField(blank=True, null=True)

    def choices_name(self):
        import unidecode
        slug = self.slug.replace(' ', '').replace('-', '_').upper()
        return 'CHOICES_%s' % unidecode.unidecode(slug)

    def choices_value(self):
        import unidecode
        if self.fieldtype_title == 'IntegerField':
            slug = self.choices.replace('|', ",'").replace('\n', "'),\n    (")
            return "[\n    (%s'), \n]" % unidecode.unidecode(slug)
        elif self.fieldtype_title == 'CharField':
            slug = self.choices.replace(
                '|', "', '").replace('\n', "'),\n    ('")
            return "[\n    ('%s'),\n]" % unidecode.unidecode(slug)
        else:
            return "[(None,'erro'),]"

    def slug_unicode(self):
        import unidecode
        slug = self.slug.replace(' ', '').replace('-', '_')
        return unidecode.unidecode(slug)

    def __str__(self):
        return '{} - {}'.format(self.model, self.slug)

    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')
        ordering = ['model', 'order']
        unique_together = ['model', 'slug']


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


class BusinessRules(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    app_title = models.CharField(max_length=200)
    model_title = models.CharField(max_length=200)
    model = models.ForeignKey(
        'Models',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_model',
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Business Rule')
        verbose_name_plural = _('Business Rules')
        ordering = ['title']


class BusinessRulesCode(BaseModel):
    business_rule = models.ForeignKey(
        'BusinessRules',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_business_rule',
        null=True,
    )
    title = models.CharField(max_length=200)
    func = models.CharField(choices=BUSINESS_RULE_FUNCTIONS, max_length=30)
    code = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Business Rule')
        verbose_name_plural = _('Business Rules')
        ordering = ['title']
