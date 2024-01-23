
NUM_NODES=10
python src/util.py $NUM_NODES topologies/election.yaml election
docker compose build
docker compose up