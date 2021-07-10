from django.core.management.base import BaseCommand, CommandError
import time
from dag.views import create_apps_function
from dag.management.commands.import_ods import import_ods
from dag.management.commands.check_database import check_database
from termcolor import colored



class Command(BaseCommand):
    help = 'Criar APPS, MODELS, ADMINS'

    def handle(self, *args, **options):
        errors = check_database()
        if not errors:
            print(colored("Gerando os arquivos da aplicação...", "white", attrs=['bold']))
            create_apps_function()
            print(f"Run 'python manage.py makemigrations' and 'python manage.py migrate' for create migrate in your database.")
        else:
            print(colored("ATENÇÃO: CORRIJA OS ERROS ACIMA PARA QUE POSSAMOS CRIAR OS CÓDIGOS.", "red"))
        
