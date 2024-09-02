# Função para remover os containers relacionados a um arquivo docker-compose
function remove_containers() {
    docker compose -f "$1" down
}

# Itera sobre os arquivos no diretório atual com o padrão docker-compose.*
for compose_file in docker-compose.*; do
    if [ -f "$compose_file" ]; then
        echo "Removendo containers do arquivo: $compose_file"
        remove_containers "$compose_file"
    fi
done

# Removendo todos os containers, redes, volumes, imagens e dados no banco de dados
docker system prune -f -a && \
docker volume rm $(docker volume ls -q) && 
docker rmi $(docker images -aq) && \
docker builder prune -f && \
docker network rm datalake-network

# Removendo as pastas logs e plugins 
sudo rm -rf ./airflow/logs 
sudo rm -rf ./airbyte
sudo rm -rf ./docker/dbt