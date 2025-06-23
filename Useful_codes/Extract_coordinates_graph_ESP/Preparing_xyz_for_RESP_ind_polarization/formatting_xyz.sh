#!/bin/bash

# Input and output files
INPUT_FILE="ccordinates"  # Changed to more common extension
OUTPUT_FILE="formatted_data.txt"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found!"
    echo "Please create this file or specify the correct path."
    exit 1
fi

# Clear output file
> "$OUTPUT_FILE"

# Process first 25 lines (79 au)
echo "Processing first 25 lines as '79 au'..."
head -n 25 "$INPUT_FILE" | awk '{printf "%-12s %-12s %-12s  79  au\n", $1, $2, $3}' >> "$OUTPUT_FILE"

# Atom definitions
ATOM_TYPES=("ho" "oh" "c" "o" "c3" "h1" "c3" "h1" "h1" "s" "n" "hn" "c" "o" "c3" "hc" "hc" "hc")
ATOM_WEIGHT=("1" "8" "6" "8" "6" "1" "6" "1" "1" "16" "7" "1" "6" "8" "6" "1" "1" "1")

# Get total lines
TOTAL_LINES=$(wc -l < "$INPUT_FILE")
REMAINING_LINES=$((TOTAL_LINES - 25))

echo "Processing remaining $REMAINING_LINES lines with atom patterns..."

# Process remaining lines
for ((LINE_NUM=26; LINE_NUM<=TOTAL_LINES; LINE_NUM++)); do
    CYCLE_POS=$(((LINE_NUM - 26) % 18))
    LINE=$(sed "${LINE_NUM}q;d" "$INPUT_FILE" 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo "Warning: Problem reading line $LINE_NUM"
        continue
    fi
    
    printf "%-12s %-12s %-12s %2s %-3s \n" \
           $(echo $LINE) "${ATOM_WEIGHT[$CYCLE_POS]}" "${ATOM_TYPES[$CYCLE_POS]}" >> "$OUTPUT_FILE"
done

echo "Successfully formatted $TOTAL_LINES lines"
echo "Output saved to $OUTPUT_FILE"
