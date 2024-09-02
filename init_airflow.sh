# Comando que cria as pastas de dags, plugins e logs
mkdir -p ./airflow/logs
mkdir -p ./docker/dbt

# Caminho do arquivo .env e importando variaveis do arquivo .env
ENV_FILE="$(dirname "$0")/.env"
. "$ENV_FILE"

# Clonando o repositório 
cd docker/dbt && git clone git@github.com:${GITHUB_USER}/${GITHUB_REPO}.git

# Retornando a pasta anterior
cd ../..

# Start do container airflow 
docker compose -f docker-compose.airflow.yaml up airflow-init && \
docker compose -f docker-compose.airflow.yaml up -d