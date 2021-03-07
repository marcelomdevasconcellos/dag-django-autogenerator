# dag-django-autogenerate
DAG - Django AutoGenerate

### Como instalar para desenvolvimento? ###

1. Clone o repositório:

```git clone https://github.com/marcelomdevasconcellos/dag-django-autogenerate.git ```

2. Crie o virtualenv:

```python3 -m venv venv_dag ```

3. Acesse o virtualenv:

- No windows: ```venv_dag\Scripts\activate```

- No Linux ou Mac: ```source venv_dag/bin/activate```

4. Acesse o diretório do projeto:

```cd dag-django-autogenerate```

3. Instale os requirements:

```pip install -r requirements.txt ```

4. Copie o arquivo .env_example para .env:

- No Linux ou Mac: ```cp config/.env_example config/.env ```

5. Crie o banco de dados em postgres com os dados abaixo ou altere os dados do banco de dados contidos no arquivo `config/.env:

```
HOST: localhost
DATABASE: dag_django_autogenerate
USER: postgres
PASSWORD: postgres
PORT: 5432
```

6. Execute as migrações:

```python manage.py migrate ```

7. Crie o usuário administrador:

```python manage.py createsuperuser ```

8. Execute o projeto:

```python manage.py runserver ```

### Como usar? ###
1. Acesse a planilha 'plan.ods' no diretório raiz e preencha os campos exatamente como deseja que os modelos sejam criados.

2. Execute a função abaixo para importar os dados da planilha para o banco de dados:

```python manage.py import_ods ```

3. Execute a função abaixo para criar os arquivos:

```python manage.py create_apps  ```

4. Execute a função abaixo para criar as migrações:

```python manage.py makemigrations  ```

5. Execute a função abaixo para executar as migrações:

```python manage.py migrate  ```
