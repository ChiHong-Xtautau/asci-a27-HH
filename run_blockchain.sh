NUM_NODES=10
GOSSIP_DEGREE=3
python src/util.py $NUM_NODES $GOSSIP_DEGREE topologies/blockchain.yaml blockchain
docker compose build
docker compose up