from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db import models
from django.utils import timezone
from django.forms import Select, Textarea

from django_currentuser.middleware import get_current_user
from reversion.admin import VersionAdmin
from config.helpers.admin import LIST_PER_PAGE, LIST_MAX_SHOW_ALL

class MultiFieldSortableChangeList(ChangeList):
    def get_ordering(self, request, queryset):
        ORDER_VAR = admin.views.main.ORDER_VAR
        params = self.params
        ordering = list(self.model_admin.get_ordering(
            request) or self._get_default_ordering())

        if ORDER_VAR in params:
            ordering = []
            order_params = params[ORDER_VAR].split('.')
            for p in order_params:
                try:
                    none, pfx, idx = p.rpartition('-')
                    field_name = self.list_display[int(idx)]
                    order_fields = self.get_ordering_field(field_name)

                    if type(order_fields) == str:
                        order_fields = [order_fields]

                    for order_field in order_fields:
                        if order_field:
                            ordering.append(pfx + order_field)
                except (IndexError, ValueError):
                    continue

        ordering.extend(queryset.query.order_by)

        pk_name = self.lookup_opts.pk.name
        if not (set(ordering) & set(['pk', '-pk', pk_name, '-' + pk_name])):
            ordering.append('-pk')

        return ordering


class BaseModel(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_created_by',
        blank=True,
        null=True,
        default=get_current_user()
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_update_by',
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.created_by or not self.created_at:
            self.created_by = get_current_user()
            self.created_at = timezone.now()
        else:
            self.update_by = get_current_user()
            self.update_at = timezone.now()
        super(BaseModel, self).save(force_insert=False, force_update=False, using=None,
                                    update_fields=None)


class AuditoriaAdmin(VersionAdmin):
    list_per_page = LIST_PER_PAGE
    list_max_show_all = LIST_MAX_SHOW_ALL    
    readonly_fields = (
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )



class AuditoriaAdminTabularInline(admin.TabularInline):
    list_per_page = LIST_PER_PAGE
    list_max_show_all = LIST_MAX_SHOW_ALL
    readonly_fields = (
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 4,
                'cols': 40
            })
        },
        models.ForeignKey: {
            'widget': Select(attrs={
                'style': 'width:150px'
            })
        },
    }


class AuditoriaAdminStackedInline(admin.StackedInline):
    list_per_page = LIST_PER_PAGE
    list_max_show_all = LIST_MAX_SHOW_ALL
    readonly_fields = (
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )
