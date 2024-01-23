
NUM_NODES=10
python src/util.py $NUM_NODES topologies/blockchain.yaml blockchain
docker compose build
docker compose up