#!/bin/bash

# Size limit passed as an argument or defaults to 400
SIZE_LIMIT_KB=${1:-400}
# Calculate size limit in bytes safely using bc for floating precision if supplied
SIZE_LIMIT_BYTES=$(echo "$SIZE_LIMIT_KB * 1024" | bc | awk '{print int($1)}')

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
IMAGES_DIR="$BASE_DIR/images_orig"
OUTPUT_DIR="$BASE_DIR/images"

mkdir -p "$OUTPUT_DIR"

echo "Reading from: $IMAGES_DIR"
echo "Output to: $OUTPUT_DIR"
echo "Compression Threshold: $SIZE_LIMIT_KB KB"

if [ ! -d "$IMAGES_DIR" ]; then
    echo "Images directory not found at $IMAGES_DIR!"
    exit 1
fi

find "$IMAGES_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read -r filepath; do
    filename=$(basename "$filepath")
    
    filename_lower=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
    filesize=$(stat -f%z "$filepath")
    filesize_kb=$(echo "scale=2; $filesize/1024" | bc)
    
    # Check if logo prefix exists OR if size <= limit
    if [[ "$filename_lower" == logo* ]] || [ "$filesize" -le "$SIZE_LIMIT_BYTES" ]; then
        # Copy as it is without modifying
        cp -p "$filepath" "$OUTPUT_DIR/$filename"
        echo "Copied   -> $filename (Size: $filesize_kb KB) without modification."
    else
        # Compress
        echo "Compress -> $filename (Original: $filesize_kb KB)..."
        
        stem="${filename%.*}"
        out_name="${stem}.jpg"
        out_path="$OUTPUT_DIR/$out_name"
        
        sips -s format jpeg -s formatOptions 80 "$filepath" --out "$out_path" > /dev/null
        
        new_size=$(stat -f%z "$out_path")
        new_size_kb=$(echo "scale=2; $new_size/1024" | bc)
        echo "            Saved as $out_name (New Size: $new_size_kb KB)"
    fi
done

echo ""
echo "Done executing bash script!"
