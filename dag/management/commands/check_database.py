from django.core.management.base import BaseCommand, CommandError
import time
from dag.views import create_apps_function
from dag.management.commands.import_ods import import_ods
from dag.models import Apps, Models, Fields, FieldTypes
from termcolor import colored


def verify_special_chars(lista, campo):
    esp = 'áàâãäåÁÂÃÄÅÀéèêëÉÈìíîïìÌÍÎÏÌóôõöòÒÓÔÕÖùúûüÙÚÛÜçÇñÑýÝ -,!@#$%ˆ&*()}{[]\|;:"''.<>/?'
    return_list = []
    for a in lista:
        for e in esp:
            if e in a[campo] and a[campo] not in return_list:
                return_list.append(a[campo])
    return return_list


def col_dict_to_list(lista, campo):
    return_list = []
    for a in lista:
        if a[campo] not in return_list:
            return_list.append(a[campo])
    return return_list


def check_database():

    errors = 0

    # Verificar se tem algum caractere especial nos campos de título.
    apps = Apps.objects.order_by('slug').values('slug').distinct()
    return_list = verify_special_chars(apps, 'slug')
    if return_list:
        print("Verificando a existência de caractere especial nos campos 'slug' nos Apps...")
        print(colored("Existem %s Apps que possuem caractere especial inseridos, por favor corrija-os, na planilha." %
                      len(return_list), "red"))
        for a in return_list:
            print('- %s' % a)
            errors += 1
#    else:
#        print(colored(
#            "Não existe nenhum App com caractere especial no campo 'slug'.", "green"))

    print()

    models = Models.objects.order_by('title').values('title').distinct()
    return_list = verify_special_chars(models, 'title')
    if return_list:
        print("Verificando a existência de caractere especial nos campos 'title' nos Models...")
        print(colored("Existem %s Models que possuem caractere especial inseridos, por favor corrija-os, na planilha." %
                      len(return_list), "red"))
        for a in return_list:
            print('- %s' % a)
            errors += 1
#    else:
#        print(colored(
#            "Não existe nenhum Model com caractere especial no campo 'title'.", "green"))

    print()

    fields = Fields.objects.order_by('slug').values('slug').distinct()
    return_list = verify_special_chars(fields, 'slug')
    if return_list:
        print("Verificando a existência de caractere especial nos campos 'slug' nos Fields...")
        print(colored("Existem %s Fields que possuem caractere especial inseridos, por favor corrija-os, na planilha." %
                      len(return_list), "red"))
        for a in return_list:
            print('- %s' % a)
            errors += 1
#   else:
#       print(colored(
#            "Não existe nenhum Field com caractere especial no campo 'slug'.", "green"))

    print()

    # Verificar se todos os campos de CharField possuem o campo "max_length" preenchido.
    # Por padrao atribui aos CharFields 255 caracteres caso venha nulos
    fields = Fields.objects.order_by('slug').filter(
        fieldtype_title='CharField', max_length__isnull=True).update(max_length="255")
    fields = Fields.objects.order_by('slug').filter(
        fieldtype_title='CharField', max_length__isnull=True).all()
    if fields:
        print("Verificando se todos os campos de CharField possuem o campo 'max_length' preenchido...")
        print(colored("Existem %s Fields 'CharField' sem o campo 'max_length' preenchido, por favor corrija, na planilha." % len(fields), "red"))
        for field in fields:
            if not field.max_length:
                print(field.slug, field.max_length)
            errors += 1
#    else:
#        print(colored(
#            "Não existe nenhum Field 'CharField' sem o campo 'max_length' preenchido.", "green"))

    print()

    # Contar o mostrar Modelos sem nenhum campo inserido.
    
    fields = Fields.objects.values('model_title').distinct()
    return_list = col_dict_to_list(fields, 'model_title')
    models = Models.objects.order_by(
        'title').exclude(title__in=return_list).all()
    if models:
        print("Verificando a existência Models sem nenhum campo inserido...")
        print(colored("Existem %s Models sem nenhum campo inserido, corrija-os na planilha." % len(models), "red"))
        for a in models:
            print('- %s' % a.title)
#    else:
#        print(colored("Não existe nenhum Model sem nenhum campo inserido.", "green"))

    print()

    # Contar o mostrar Modelos não referenciados por ForeignKey.

    fields = Fields.objects.values('foreignkey_model_title').distinct()
    return_list = col_dict_to_list(fields, 'foreignkey_model_title')
    models = Models.objects.order_by(
        'title').exclude(title__in=return_list).all()
    if models:
        print("Verificando a existência Models não referenciados por ForeignKey...")
        print(colored("Existem %s Models não referenciados por ForeignKey, CASO NECESSÁRIO, corrija-os na planilha." % len(models), "red"))
        for a in models:
            print('- %s' % a.title)
#    else:
#        print("Não existe nenhum Model não referenciados por ForeignKey.")

    print()

    # Contar e mostrar Modelos sem nenhum campo "in_search_fields" preenchido.

    fields = Fields.objects.filter(
        in_search_fields=True).values('model_title').distinct()
    return_list = col_dict_to_list(fields, 'model_title')
    models = Models.objects.order_by(
        'title').exclude(title__in=return_list).all()
    if models:
        print("Verificando a existência Models sem nenhum campo 'in_search_fields' preenchido...")
        print(colored("Existem %s Models sem nenhum campo 'in_search_fields' preenchido, corrija-os na planilha." % len(models),'red'))
        for a in models:
            print('- %s' % a.title)
#    else:
#        print("Não existe nenhum Model sem nenhum campo 'in_search_fields' preenchido.")

    print()

    # Contar e mostrar Modelos sem nenhum campo "in_list_filter" preenchido.

    fields = Fields.objects.filter(
        in_list_filter=True).values('model_title').distinct()
    return_list = col_dict_to_list(fields, 'model_title')
    models = Models.objects.order_by(
        'title').exclude(title__in=return_list).all()
    if models:
        print("Verificando a existência Models sem nenhum campo 'in_list_filter' preenchido...")
        print(colored("Existem %s Models sem nenhum campo 'in_list_filter' preenchido, corrija-os na planilha." % len(models),'red'))
        for a in models:
            print('- %s' % a.title)
#    else:
#        print("Não existe nenhum Model sem nenhum campo 'in_list_filter' preenchido.")

    print()

    # Contar e mostrar Modelos sem nenhum campo "in_list_display" preenchido.

    fields = Fields.objects.filter(
        in_list_display=True).values('model_title').distinct()
    return_list = col_dict_to_list(fields, 'model_title')
    models = Models.objects.order_by(
        'title').exclude(title__in=return_list).all()
    if models:
        print("Verificando a existência Models sem nenhum campo 'in_list_display' preenchido...")
        print(colored("Existem %s Models sem nenhum campo 'in_list_display' preenchido, corrija-os na planilha." % len(models),'red'))
        for a in models:
            print('- %s' % a.title)
#    else:
#        print("Não existe nenhum Model sem nenhum campo 'in_list_display' preenchido.")

    print()

    # Contar e mostrar Modelos sem nenhum campo "is_ordering" preenchido.

    fields = Fields.objects.filter(
        is_ordering=True).values('model_title').distinct()
    return_list = col_dict_to_list(fields, 'model_title')
    models = Models.objects.order_by(
        'title').exclude(title__in=return_list).all()
    if models:
        print("Verificando a existência Models sem nenhum campo 'is_ordering' preenchido...")
        print(colored("Existem %s Models sem nenhum campo 'is_ordering' preenchido, corrija-os na planilha." % len(models),'red'))
        for a in models:
            print('- %s' % a.title)
#    else:
#        print("Não existe nenhum Model sem nenhum campo 'is_ordering' preenchido.")

    print()

    # Exibir totais
    print("Totais:")
    apps = Apps.objects.all()
    models = Models.objects.all()
    fields = Fields.objects.all()
    print("Apps: %s" % len(apps))
    print("Models: %s" % len(models))
    print("Fields: %s" % len(fields))
    print()
    return errors


class Command(BaseCommand):
    help = 'Check database'

    def handle(self, *args, **options):
        check_database()
