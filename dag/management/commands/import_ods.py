from django.core.management.base import BaseCommand
from dag.models import Apps, Models, Fields, FieldTypes, ModelsInline
from dag.views import FIELD_TYPES
from termcolor import colored
from django.db import IntegrityError


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
        'verbose_name_plural', 'is_model_admin', 'is_read_only', 'django_inline_models',
        'app_slug', 'is_empty', 'quant']
    for d in data_list:
        if len(d) and len(d) == len(fields):
            dic = {}
            for f in range(len(fields)):
                dic[fields[f]] = d[f]
                if d[f] and d[f] in ('TRUE', 'YES', 1):
                    dic[fields[f]] = True
                elif d[f] and d[f] in ('FALSE', 'NO', 0):
                    dic[fields[f]] = False
                elif d[f] and d[f] != 'NULL':
                    dic[fields[f]] = d[f]
            try:
                dic['app_id'] = Apps.objects.get(slug=dic['app_slug']).id
            except:
                print(colored(
                    '[dag_models - Linha %s] Erro ao tentar localizar um App com o "slug" igual a %s' % (d[0], dic['app_slug']), 'red'))
                return None
            obj = Models(**dic)
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
                if d[f] and d[f] in ('TRUE', 'YES', 1):
                    dic[fields[f]] = True
                elif d[f] and d[f] in ('FALSE', 'NO', 0):
                    dic[fields[f]] = False
                elif d[f] and d[f] != 'NULL':
                    dic[fields[f]] = d[f]

            try:
                dic['model_id'] = Models.objects.get(
                    title=dic['model_title']).id
            except:
                print(colored('[dag_models - Linha %s] Erro ao tentar localizar um Model(%s) com o "title" igual a %s' %
                              (d[0], d[1], dic['model_title']) , 'red'))
                return None

            if dic['fieldtype_title'] not in FIELD_TYPES:
                print(colored('[dag_models - Linha %s] Erro ao tentar localizar um FieldType '
                              'com o "fieldtype" igual a %s' % (d[0], dic['fieldtype_title']), 'red'))
                break

            if 'foreignkey_model_title' in dic:

                try:
                    dic['foreignkey_id'] = Models.objects.get(
                        title=dic['foreignkey_model_title']).id
                except:
                    print(colored('[dag_models - Linha %s] Erro ao tentar localizar um Model(%s) com o "foreignkey" igual a %s' %
                                  (d[0], d[1], dic['foreignkey_model_title']), 'red'))
                    return None
            obj = Fields(**dic)
            try:
                obj.save()
            except IntegrityError as e:
                print(colored('[dag_models - Linha %s] Erro ao salvar o Model(%s) campo duplicado, coluna slug com nome "%s"' %
                                  (d[0], d[1], dic['slug']), 'red'))
                print(colored(f'Error: {e}', 'yellow'))
                return None



def update_inline_models():
    models = Models.objects.\
        filter(django_inline_models__isnull=False).\
        exclude(django_inline_models='').all()
    for m in models:
        for i in m.inline_list():
            try:
                mi = Models.objects.get(title=i[0])
            except:
                print(colored('[dag_models inline] Erro ao tentar localizar um Model com o "title" igual a %s' % i[0], 'red'))
                return None
            dic = {'model': m, 'model_inline': mi, 'type_inline': i[1]}
            obj = ModelsInline(**dic)
            obj.save()


def import_ods(plan_file):
    from pyexcel_ods3 import get_data

    Fields.objects.all().delete()
    ModelsInline.objects.all().delete()
    Models.objects.all().delete()
    Apps.objects.all().delete()

    data = get_data(plan_file)
    import_apps(data['dag_apps'][1:])
    import_models(data['dag_models'][1:])
    import_fields(data['dag_fields'][1:])
    update_inline_models()


class Command(BaseCommand):
    help = 'Importar planilha ODS'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, *args, **options):
        file_argument = options["file"] or "dag_plan.ods"
        print(colored(f'Ok', 'green') + f' - DAG File loading: {file_argument}')
        print(f'Run ' + colored(f'python manage.py create_apps', 'yellow') + f' for create apps in your project.')
        import_ods(file_argument)
