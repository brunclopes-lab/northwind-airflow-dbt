from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from cosmos.operators import DbtDocsS3Operator


POSTGRES_CONNECTION_ID = "postgres_northwind_conn"
DB_NAME = "northwind"
SCHEMA_NAME = "northwind"
REPO_GITHUB_NAME = 'dbt-northwind-rds'

ROOT_PATH = f"/opt/airflow/dbt"
REPO_PATH = f"{ROOT_PATH}/{REPO_GITHUB_NAME}" 
DBT_PROJECT_PATH = f"{REPO_PATH}/northwind"

S3_CONNECTION_ID = "s3_dbt_docs"
S3_BUCKET = "dbt-docs-datalake"

# Configuração do perfil
profile_config = ProfileConfig(
    profile_name="northwind",
    target_name="prod",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=POSTGRES_CONNECTION_ID,
        profile_args={"schema": SCHEMA_NAME},
    )
)

@dag(
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=True,
    default_args={"retries": 2, 'owner': 'airflow'}
)
def dag_northwind():
    # Task para iniciar o processo
    start_process = DummyOperator(task_id='start_process')

    # Task para transformar os dados com DBT
    transform_data = DbtTaskGroup(
        group_id="transform_data",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=profile_config,
    )

    generate_dbt_docs_aws = DbtDocsS3Operator(
        task_id="generate_dbt_docs_aws",
        project_dir="/opt/airflow/dbt/dbt-northwind-rds/northwind",
        profile_config=profile_config,
        # docs-specific arguments
        connection_id=S3_CONNECTION_ID,
        bucket_name=S3_BUCKET,
    )

    # Definindo a ordem das tasks
    start_process >> transform_data >> generate_dbt_docs_aws

# Instancia a DAG
dag_instance = dag_northwind()