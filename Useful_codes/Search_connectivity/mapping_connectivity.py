from collections import defaultdict, deque

def build_graph_from_file(filename, max_distance=2.5):
    graph = defaultdict(set)
    with open(filename, 'r') as f:
        for line in f:
            if line.strip().startswith("Atoms") or not line.strip():
                continue  # skip header or empty lines
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            try:
                a1, a2, dist = int(parts[0]), int(parts[1]), float(parts[2])
            except ValueError:
                continue  # skip lines that can't be parsed
            if dist <= max_distance:
                graph[a1].add(a2)
                graph[a2].add(a1)
    return graph

# Step 2: Find all connected components (chains)
def find_chains(graph):
    visited = set()
    chains = []

    for node in graph:
        if node not in visited:
            chain = []
            queue = deque([node])
            visited.add(node)
            while queue:
                current = queue.popleft()
                chain.append(current)
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            chains.append(chain)
    return chains

# Main execution
if __name__ == "__main__":
    input_file = "connection_map.out"  # Replace with your filename
    max_bond_distance = 2.7      # Adjust as needed

    graph = build_graph_from_file(input_file, max_distance=max_bond_distance)
    chains = find_chains(graph)
    for i, chain in enumerate(chains, 1):
        print(f"Chain {i}: has {len(chain)} atoms")
    with open("chains_output.txt", "w") as file:
        for i, chain in enumerate(chains, 1):
            file.write(f"Chain {i}: {sorted(chain)}\n")

