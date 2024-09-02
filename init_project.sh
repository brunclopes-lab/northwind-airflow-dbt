# Criando a rede datalake-network
sh init_network.sh

# Iniciando o projeto do postgres
sh init_db.sh

# Atraso de 10 segundos
sleep 10

# Iniciando o projeto do Airflow
sh init_airflow.sh 