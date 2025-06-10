#!/bin/bash

# Configuration
input_file="NP.pdb"
output_file="extracted_columns.pdb"
replace_file="test.txt"

# Validate input files
for file in "$input_file" "$replace_file"; do
    if [[ ! -f "$file" ]]; then
        echo "Error: File '$file' not found." >&2
        exit 1
    fi
    if [[ ! -s "$file" ]]; then
        echo "Error: File '$file' is empty." >&2
        exit 1
    fi
done

# Count ATOM/HETATM lines
input_lines=$(grep -c -E '^(ATOM  |HETATM)' "$input_file")
replace_lines=$(wc -l < "$replace_file")

if [[ "$input_lines" -ne "$replace_lines" ]]; then
    echo "Error: Line count mismatch. Input ATOM/HETATM: $input_lines, Replacement: $replace_lines" >&2
    exit 1
fi

# Validate that replacement file has 3 columns
replace_cols=$(awk '{print NF; exit}' "$replace_file")
if [[ "$replace_cols" -ne 3 ]]; then
    echo "Error: Replacement file must have exactly 3 columns (x y z)" >&2
    exit 1
fi

# Process file
awk '
    # Load new coordinates
    NR==FNR {
        if (NF != 3) {
            print "Error: Line " NR " in replacement file does not have 3 columns" > "/dev/stderr"
            exit 1
        }
        x[NR] = sprintf("%8.3f", $1)
        y[NR] = sprintf("%8.3f", $2)
        z[NR] = sprintf("%8.3f", $3)
        next
    }

    # Format atom name (always left-justify within 4 chars)
    function format_atom_name(raw) {
        gsub(/^[ \t]+|[ \t]+$/, "", raw)
        return sprintf("%-4s", raw)
    }

    # Main processing
    {
        if ($0 ~ /^(ATOM  |HETATM)/) {
            count++
            atom_name_raw = substr($0,13,4)
            atom_name = format_atom_name(atom_name_raw)

            printf "%-6s%5s %-4s%1s%3s %1s%4s%1s   %s%s%s%6s%6s          %2s%2s\n",
                substr($0,1,6),      # Record name
                substr($0,7,5),      # Atom serial
                atom_name,           # Atom name (left-aligned)
                substr($0,17,1),     # Alternate location indicator
                substr($0,18,3),     # Residue name
                substr($0,22,1),     # Chain ID
                substr($0,23,4),     # Residue sequence number
                substr($0,27,1),     # Insertion code
                x[count],            # New X
                y[count],            # New Y
                z[count],            # New Z
                substr($0,55,6),     # Occupancy
                substr($0,61,6),     # Temp factor
                substr($0,77,2),     # Element
                substr($0,79,2)      # Charge
        } else {
            print
        }
    }
' "$replace_file" "$input_file" > "$output_file"

# Verify output
if [[ $? -ne 0 ]]; then
    echo "Error: Processing failed." >&2
    exit 1
fi

if [[ ! -s "$output_file" ]]; then
    echo "Error: Output file is empty." >&2
    exit 1
fi

echo "✅ Success: Coordinates replaced with left-justified atom names"
echo "📄 Output saved to $output_file"
