#!/bin/bash

# Configuration
input_file="atom_type"
output_file="extracted_columns.txt"
replace_file="test.txt"
target_column=7

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

# Verify line counts match
input_lines=$(wc -l < "$input_file")
replace_lines=$(wc -l < "$replace_file")

if [[ "$input_lines" -ne "$replace_lines" ]]; then
    echo "Error: Line count mismatch. Input: $input_lines, Replace: $replace_lines" >&2
    exit 1
fi

# Verify target column exists
num_columns=$(awk '{print NF; exit}' "$input_file")
if [[ "$target_column" -gt "$num_columns" ]]; then
    echo "Error: Target column $target_column exceeds input file's $num_columns columns" >&2
    exit 1
fi

# Process files while preserving formatting
awk -v col="$target_column" '
    # Read replacement values first
    NR==FNR {
        replace[NR] = $1
        next
    }
    {
        # Split line into fields while keeping whitespace
        original = $0
        n = split(original, fields, FS, seps)
        
        # Replace the target column
        if (col <= n) {
            fields[col] = replace[FNR]
        }
        
        # Reconstruct the line with original spacing
        output = seps[0]  # leading space before first field
        for (i = 1; i <= n; i++) {
            output = output fields[i] seps[i]
        }
        print output
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

echo "Success: Replaced column $target_column while preserving original formatting"
echo "Output saved to $output_file"