import time
from django.core.management.base import BaseCommand, CommandError
from dag.models import Apps, Models, Fields, FieldTypes
from termcolor import colored


def import_apps(data_list):
    fields = ['id','title','slug','verbose_name']
    for d in data_list:
        if len(d):
            dic = {}
            for f in range(len(fields)):
                dic[fields[f]] = d[f]
            obj = Apps(**dic)
            obj.save()


def import_models(data_list):

    fields = [
        'id', 'title', 'verbose_name',
        'verbose_name_plural', 'django_modeladmin', 'django_inline_models',
        'app_slug', 'is_empty', 'quant']

    for d in data_list:
        if len(d):
            dic = {}
            for f in range(len(fields)):
                dic[fields[f]] = d[f]
            
            try:
                dic['app_id'] = Apps.objects.get(slug=dic['app_slug']).id
            except:
                print(colored('Erro ao tentar localizar um App com o "slug" igual a %s' % dic['app_slug'], 'red'))
                return None

            obj = Models(**dic)
            obj.save()


def import_fieldtypes(data_list):
    fields = ['id','title','model_code']
    for d in data_list:
        if len(d):
            dic = {}
            for f in range(len(fields)):
                dic[fields[f]] = d[f]
            obj = FieldTypes(**dic)
            obj.save()


def import_fields(data_list):
    fields = [
        'id', 'model_title', 'slug', 'verbose_name', 'help_text', 'max_length',
        'bootstrap_columns', 'default_value', 'is_null', 'is_blank',
        'is_unique', 'is_readonly', 'is_editable', 'is_db_index',
        'is_ordering', 'is_model_title', 'in_search_fields', 'in_list_filter', 'in_list_display',
        'in_field_model', 'choices', 'fieldtype_title', 'foreignkey_model_title', 'order'
    ]
    for d in data_list:
        if len(d):
            dic = {}
            for f in range(len(fields)):
                if d[f] and d[f] != 'NULL':
                    dic[fields[f]] = d[f]

            try:
                dic['model_id'] = Models.objects.get(title=dic['model_title']).id
            except:
                print(colored('Erro ao tentar localizar um Model com o "title" igual a %s' % dic['model_title'], 'red'))
                return None
            
            try:
                dic['fieldtype_id'] = FieldTypes.objects.get(title=dic['fieldtype_title']).id
            except:
                print(colored('Erro ao tentar localizar um FieldType com o "title" igual a %s' % dic['fieldtype_title'], 'red'))
                return None

            if 'foreignkey_model_title' in dic:

                try:
                    dic['foreignkey_id'] = Models.objects.get(title=dic['foreignkey_model_title']).id
                except:
                    print(colored('Erro ao tentar localizar um Model com o "title" igual a %s' % dic['foreignkey_model_title'], 'red'))
                    return None

            obj = Fields(**dic)
            obj.save()


def import_ods():
    from pyexcel_ods3 import get_data
    import json

    Fields.objects.all().delete()
    Models.objects.all().delete()
    Apps.objects.all().delete()

    data = get_data("plan.ods")
    import_apps(data['dag_apps'][1:])
    import_models(data['dag_models'][1:])
    import_fieldtypes(data['dag_fieldtypes'][1:])
    import_fields(data['dag_fields'][1:])


class Command(BaseCommand):
    help = 'Importar planilha ODS'

    def handle(self, *args, **options):
        import_ods()
