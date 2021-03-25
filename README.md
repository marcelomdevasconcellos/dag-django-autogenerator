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
DATABASE: dag
USER: postgres
PASSWORD: postgres
PORT: 5432
```

6. Execute as migrações: ```python manage.py migrate ```

7. Crie o usuário administrador: ```python manage.py createsuperuser ```

8. Execute o projeto: ```python manage.py runserver ```

### Como usar? ###
1. Acesse a planilha 'plan.ods' no diretório raiz e preencha os campos exatamente como deseja que os modelos sejam criados. Visualize a planilha original no Google Sheets através do link ```https://docs.google.com/spreadsheets/d/1uN7JyCSBc48a_opuZ-0MmugiEgjFmJ-E3B_P3pQcxBQ/edit?usp=sharing```


2. Execute a função abaixo para importar os dados da planilha(dag_plan.ods) para o banco de dados: ```python manage.py import_ods ```
```sh
Para importar um arquivo com nome diferente utilize: "python manage.py import_ods --file meu_arq_plan.ods"
```

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
- Inclusão de autocomplete;
- Inclusão de range date nos filtros de data;
- Inclusão de geração do django restframework;
- Inclusão de classe para páginas especiais;
- Salvar um arquivo com saidas das sugestões de correção;
- Transformar em um extensão do python/django;

### Dica do arquivo DAG_PLAN.ods ###

Uma breve explicação sobre o preenchimento da planilha "dag_plan.ods".

Aba *dag_apps*

| title | sample_text | Explicacao |
| ----- | ----------- | ---------- |
| id | 1 | Sequencia das apps |
| title | SIC ou Diario Oficial | Descricao da aplicacao |
| slug | sistema_incricao_cadastro | Tudo minusculo e snake_case |
| verbose_name | Sistema Inscrição de Cadastro | CamelCase com espaco e acentuacao, menu da aplicação |
| is_verify | FALSE | Uso nao obrigatorio (padrao False) , Campo utilizado pelo implantador para verifcar quais apps ja validei ou implantada |

Aba *dag_models*

|title|sample_text|Explicacao|
|-----|-----------|----------|
|id|1|Sequencia das tabelas|
|title|AssinaturaVirtuais|Padrao camelCase SEM espaco entre as palavras.|
|verbose_name|Assinatura Virtual|Tabela no singular, COM espaco em branco entre as palavras.|
|verbose_name_plural|Assinaturas Virtuais|Descricao da table em CamelCase com espacos e no plural.	
|is_model_admin|FALSE|Diz se essa tabela sera vista so no admin, nao ficara disponivel para o usuario administrar, tabela auxiliar|
|is_read_only|FALSE|Diz se essa tabela sera somente leitura|
|django_inline_models|ColaboradoreslTabularInline CidadeslStackedInline|Nome das tabelas filhas, tera que ser igual ao "title" ja existentes, separado por linha, TabularInline ou StackedInline, Formato inline do django admin, StackedInline exibe o model de forma do tipo form, TabularInline em forma de linha/lista. |
|app_slug|sistema_incricao_cadastro|Texto semelhante ao cadastrado na aba dag_apps (slug). tem que existir na listagem.|
|is_empty|FALSE|Uso nao obrigatorio (padrao False) , Campo utilizado pelo implantador para verifcar quais tabelas estao vazias para remover ou nao.|
|quant|Automatico|Contabiliza quantos campos/fields estao associados a essa tabela atraves da aba dag_fields relacionando com campo "model_fields".|

Aba *dag_fields*

|title|sample_text|Explicacao|
|-----|-----------|----------|
|id|1|Sequencia dos campos|
|model_title|AssinaturaVirtuais|Vinculado com campo "title" da dag_models, assim sei que campo pertence a qual tabela|
|slug|tp_inscricao|Tudo minusculo e snake_case|
|verbose_name|Tipo de inscrição|CamelCase com espaco e acentuacao, descricao do campo na aplicacao|
|help_text|Texto explicativo do campo|Campo utilizado para esclarecer informacoes ao usuario sobre como preencher.|
|max_length|20|Tamanho do campo|
|bootstrap_columns|4|Posicao das colunas no formulario, padrao bootstrap das colunas (2,3,4,6,12)|
|default_value|Cadastro|Valor padrao preenchido no forumlario. Usuario pode alterar caso queira.|
|is_null|TRUE|Valor Boolean, se pode ser nulo. para efeito de banco de dados|
|is_blank|TRUE|Valor Boolean, se pode ser branco/vazio. para efeito de formulario|
|is_unique|FALSE|Valor Boolean, se pode ser campo unico.|
|is_readonly|FALSE|Valor Boolean, se pode ser somente leitura na exibição do form. Por exemplo ja vem por padrao os campos de auditoria|
|is_editable|TRUE|Valor Boolean, se pode ser editavel na listagem geral.|
|is_db_index|FALSE|Valor Boolean, se pode ser indice da tabela. Para efeito de BD facilita nas buscas pois poui indice|
|is_ordering|FALSE|Valor Boolean, se pode ser ordenavel na listagem e/ou combobox/tag select hmtl.|
|is_model_title|TRUE|Aparece como título do modelo, pelo menos um campo tera que ser True. Na função _str_|
|in_search_fields|TRUE|Valor Boolean, se pode ser utilizado na busca/filtro de busca de preenchimento.|
|in_list_filter|TRUE|Valor Boolean, se pode ser utilizado para filtro.|
|in_list_display|TRUE|Valor Boolean, se pode ser visivel na listagem principal.|
|in_field_model|FALSE|Valor Boolean, se pode ser ???? - sera removido em breve.|
|choices|1lCadastrado 2lAprovado|Listagem especifica (combobox) select, cada item numa linha diferente|
|fieldtype_title|CharField ou BooleanField|Tipo de campo no Python(varios tipos)|
|foreignkey_model_title|Documentos|Vinculado com campo "title" da dag_models, Chave Primaria com outra tabela.|
|order|1|Ordem do campo na tabela.|


### Obrigado!

- [AdminLTE](https://github.com/ColorlibHQ/AdminLTE)
- [django](https://github.com/django/django)
- [DjangoAdminUI](https://github.com/wuyue92tree/django-adminlte-ui)



