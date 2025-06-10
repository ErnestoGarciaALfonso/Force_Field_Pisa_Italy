# Read input file
with open('chains_output.txt', 'r') as f:
    chains_data = f.readlines()

# Parse chains into a dictionary
chains = {}
for line in chains_data:
    if line.startswith('Chain'):
        chain_num = int(line.split()[1].strip(':'))
        numbers = list(map(int, line[line.find('[')+1:line.find(']')].split(',')))
        chains[chain_num] = numbers

# Select Chain 4 (modify if needed)
selected_chain = chains[5][::-1]  # Reverse to match your example

# Format output: 8 pairs per line (16 columns)
output_lines = []
for i in range(0, len(selected_chain), 8):  # Process 8 numbers at a time
    group = selected_chain[i:i+8]
    line = "".join(f"    1 {num:4}" for num in group)
    output_lines.append(line)

# Write to output file
with open("formatted_output.txt", "w") as f:
    f.write("\n".join(output_lines))

print("Output saved to 'formatted_output.txt'")