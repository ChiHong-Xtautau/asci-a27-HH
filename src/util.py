import yaml
import copy
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Scale the docker-compose file',
        description='Scale the number of nodes',
        epilog='Designed for A27 Fundamentals and Design of Blockchain-based Systems')
    parser.add_argument('num_nodes', type=int)
    parser.add_argument('gossip_degree', type=int)
    parser.add_argument('topology_file', type=str, nargs='?', default='topologies/ring.yaml')
    parser.add_argument('algorithm', type=str, nargs='?', default='echo')
    parser.add_argument('template_file', type=str, nargs='?', default='docker-compose.template.yml')
    args = parser.parse_args()

    with open(args.template_file, 'r') as f:
        content = yaml.safe_load(f)

        node = content['services']['node0']
        content['x-common-variables']['TOPOLOGY'] = args.topology_file

        nodes = {}
        baseport = 9090
        connections = {}

        for i in range(args.num_nodes):
            n = copy.deepcopy(node)
            n['ports'] = [f'{baseport + i}:{baseport + i}']
            n['networks']['vpcbr']['ipv4_address'] = f'192.168.55.{10 + i}'
            n['environment']['PID'] = i
            n['environment']['TOPOLOGY'] = args.topology_file
            n['environment']['ALGORITHM'] = args.algorithm
            nodes[f'node{i}'] = n

            # Create a ring topology
            if args.algorithm == "election":
                connections[i] = [(i+1) % args.num_nodes, (i-1) % args.num_nodes]

            # Create a connected topology of different gossip degree
            if args.algorithm == "blockchain":
                if i < 5:
                    connections[i] = [j for j in range(args.num_nodes) if j != i]
                else:
                    if args.gossip_degree == 4:
                        connections[i] = [j for j in range(args.num_nodes) if j != i]
                    elif args.gossip_degree == 1:
                        connections[i] = [(i+5)%args.num_nodes]
                    elif args.gossip_degree == 2:
                        connections[i] = [(i-1) % 5 +5, (i+1) % 5 +5]
                    elif args.gossip_degree == 3:
                        connections[i] = [(i-1) % 5 +5, (i+1) % 5 +5, (i+2) % 5 +5]
        content['services'] = nodes

        with open('docker-compose.yml', 'w') as f2:
            yaml.safe_dump(content, f2)
            print(f'Output written to docker-compose.yml')

        with open(args.topology_file, 'w') as f3:
            yaml.safe_dump(connections, f3)
            print(f'Output written to {args.topology_file}')
