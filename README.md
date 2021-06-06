# DAG - Django AutoGenerator

### O que é? ###

Este repositório visa ajudar os desenvolvedores a criar um projeto completo utilizando django admin, aonde é possível cadastrar todos os modelos e campos em uma planilha e através da execução de poucos comandos são criados todos os arquivos .py necessários para o projeto, depois é só executar as migrações (makemigrations e migrate) e o sistema estará pronto para uso!

### Como instalar para desenvolvimento? ###

1. Clone o repositório: ```git clone https://github.com/marcelomdevasconcellos/dag-django-autogenerator.git ```

2. Crie o virtualenv: ```python3 -m venv venv_dag ```

3. Acesse o virtualenv:

- No windows: ```venv_dag\Scripts\activate```
- No Linux ou Mac: ```source venv_dag/bin/activate```

4. Acesse o diretório do projeto: ```cd dag-django-autogenerator```

3. Instale os requirements: ```pip install -r requirements.txt ```

4. Copie o arquivo `config/.env_example` para `config/.env`:

- No Windows: ```cd config && copy .env_example .env && cd ..```
- No Linux ou Mac: ```cp config/.env_example config/.env ```

5. Crie o banco de dados em postgres com os dados abaixo ou altere os dados do banco de dados contidos no arquivo `config/.env`:

```
HOST: localhost
DATABASE: dag_django_autogenerator
USER: postgres
PASSWORD: postgres
PORT: 5432
```

6. Execute as migrações: ```python manage.py migrate ```

7. Crie o usuário administrador: ```python manage.py createsuperuser ```

8. Execute o projeto: ```python manage.py runserver ```

### Como usar? ###
1. Acesse a planilha 'plan.ods' no diretório raiz e preencha os campos exatamente como deseja que os modelos sejam criados. Visualize a planilha original no Google Sheets através do link ```https://docs.google.com/spreadsheets/d/1uN7JyCSBc48a_opuZ-0MmugiEgjFmJ-E3B_P3pQcxBQ/edit?usp=sharing```


2. Execute a função abaixo para importar os dados da planilha para o banco de dados: ```python manage.py import_ods ```

3. Execute a função abaixo para criar os arquivos: ```python manage.py create_apps  ```

4. Execute a função abaixo para criar as migrações: ```python manage.py makemigrations  ```

5. Execute a função abaixo para executar as migrações: ```python manage.py migrate  ```

6. Acesse a url ```http://localhost:8000/admin/```


### Dica: Consulta SQL que ajudará a extrair informações de um banco de dados Postgres existente ###
```
WITH dag AS (

WITH foreignkeys AS (

    SELECT tc.table_schema, tc.constraint_name,
           tc.table_name, kcu.column_name,
           ccu.table_schema AS foreign_table_schema,
           ccu.table_name AS foreign_table_name,
           ccu.column_name AS foreign_column_name
      FROM information_schema.table_constraints AS tc
      JOIN information_schema.key_column_usage AS kcu 
        ON tc.constraint_name = kcu.constraint_name 
       AND tc.table_schema = kcu.table_schema
      JOIN information_schema.constraint_column_usage AS ccu 
        ON ccu.constraint_name = tc.constraint_name 
       AND ccu.table_schema = tc.table_schema
     WHERE tc.constraint_type = 'FOREIGN KEY')
     
SELECT DISTINCT 
       c.table_schema, c.table_name, 
       REPLACE(INITCAP(REPLACE(c.table_name, '_', ' ')), ' ', '') AS model_title,
       c.column_name, 
       c.ordinal_position, c.is_nullable,
       c.data_type, 
       COALESCE(c.character_maximum_length::TEXT, '') AS character_maximum_length, 
       c.numeric_precision, 
       c.numeric_scale,
       COALESCE(f.foreign_table_name, '') AS foreign_table_name,
       REPLACE(INITCAP(REPLACE(COALESCE(f.foreign_table_name, ''), '_', ' ')), ' ', '') AS foreign_model_title
  FROM information_schema.columns c
  LEFT JOIN foreignkeys f ON c.table_name = f.table_name 
   AND c.column_name = f.column_name
 ORDER BY c.table_schema, c.table_name, c.ordinal_position)
 
   SELECT * FROM dag
    WHERE table_schema='public'
 ORDER BY table_schema, 
          table_name, 
          ordinal_position;
```

### Backlog ###

- Geração de forms;
- Inclusão de regras de negócio;
- Inclusão do tipo de inline na planilha e geração (TabularInline/StackedInline);
- Inclusão de autocomplete;
- Inclusão de range date nos filtros de data;
- Inclusão de geração do django restframework;
- Inclusão de classe para páginas especiais;
- Salvar um arquivo com saidas das sugestões de correção;
- Incluir parâmetro do caminho e nome do arquivo em import_ods;
- Transformar em um extensão do python/django;

### Requisitos de Sistema

- Python (versão 3.8.5);
- Django (versão 3.2);
- Postgres 12;
- outros requisitos no arquivo requirements.txt

### Obrigado!

- [AdminLTE](https://github.com/ColorlibHQ/AdminLTE)
- [django](https://github.com/django/django)
- [DjangoAdminUI](https://github.com/wuyue92tree/django-adminlte-ui)



