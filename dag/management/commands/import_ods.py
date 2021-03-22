import time
from django.core.management.base import BaseCommand, CommandError
from dag.models import Apps, Models, Fields, FieldTypes
from termcolor import colored


def import_apps(data_list):
    fields = ['id', 'title', 'slug', 'verbose_name']
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
        'django_inline_type',
        'app_slug', 'is_empty', 'quant']

    for d in data_list:
        if len(d):
            dic = {}
            for f in range(len(fields)):
                dic[fields[f]] = d[f]
                if d[f] and d[f] == 'TRUE':
                    dic[fields[f]] = True
                elif d[f] and d[f] == 'FALSE':
                    dic[fields[f]] = False
                elif d[f] and d[f] != 'NULL':
                    dic[fields[f]] = d[f]
            try:
                dic['app_id'] = Apps.objects.get(slug=dic['app_slug']).id
            except:
                print(colored(
                    'Erro ao tentar localizar um App com o "slug" igual a %s' % dic['app_slug'], 'red'))
                return None

            obj = Models(**dic)
            obj.save()


def import_fieldtypes(data_list):
    fields = ['id', 'title', 'model_code']
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
                if d[f] and d[f] == 'TRUE':
                    dic[fields[f]] = True
                elif d[f] and d[f] == 'FALSE':
                    dic[fields[f]] = False
                elif d[f] and d[f] != 'NULL':
                    dic[fields[f]] = d[f]

            try:
                dic['model_id'] = Models.objects.get(
                    title=dic['model_title']).id
            except:
                print(colored('Erro ao tentar localizar um Model com o "title" igual a %s' %
                              dic['model_title'], 'red'))
                return None

            try:
                dic['fieldtype_id'] = FieldTypes.objects.get(
                    title=dic['fieldtype_title']).id
            except:
                print(colored('Erro ao tentar localizar um FieldType com o "title" igual a %s' %
                              dic['fieldtype_title'], 'red'))
                return None

            if 'foreignkey_model_title' in dic:

                try:
                    dic['foreignkey_id'] = Models.objects.get(
                        title=dic['foreignkey_model_title']).id
                except:
                    print(colored('Erro ao tentar localizar um Model com o "title" igual a %s' %
                                  dic['foreignkey_model_title'], 'red'))
                    return None

            obj = Fields(**dic)
            obj.save()


def update_inline_models():
    models = Models.objects.filter(django_inline_models__isnull=False).all()
    for m in models:
        if m.django_inline_models.strip():
            inline_models = m.django_inline_models.split(',')
            for i in inline_models:
                i = i.strip()
                print(i)
                model_inline = Models.objects.get(title=i)
                m.inline_models.add(model_inline)


def import_ods(plan_file):
    from pyexcel_ods3 import get_data
    import json

    Fields.objects.all().delete()
    Models.objects.all().delete()
    Apps.objects.all().delete()

    data = get_data(plan_file)
    import_apps(data['dag_apps'][1:])
    import_models(data['dag_models'][1:])
    import_fieldtypes(data['dag_fieldtypes'][1:])
    import_fields(data['dag_fields'][1:])
    update_inline_models()


class Command(BaseCommand):
    help = 'Importar planilha ODS'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, *args, **options):
        print(f'DAG File loading: {options["file"]}') if options["file"] else None
        file_argument = options["file"] or "plan.ods"
        import_ods(file_argument)
