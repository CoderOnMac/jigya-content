import os
import sys
import shutil
from PIL import Image

def compress_images():
    # Use specified size limit in KB or default to 400
    size_limit_kb = float(sys.argv[1]) if len(sys.argv) > 1 else 400.0
    size_limit_bytes = size_limit_kb * 1024

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(base_dir, 'images_orig')
    output_dir = os.path.join(base_dir, 'images')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Reading from: {images_dir}")
    print(f"Output to: {output_dir}")
    print(f"Compression Threshold: {size_limit_kb} KB")

    image_files = []
    if os.path.exists(images_dir):
        for f in os.listdir(images_dir):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_files.append(f)

    compressed_count = 0
    copied_count = 0

    for filename in image_files:
        filepath = os.path.join(images_dir, filename)
        file_size_bytes = os.path.getsize(filepath)
        
        # Copy 'as is' condition: file starts with 'logo' OR size is under/equal limit
        if filename.lower().startswith('logo') or file_size_bytes <= size_limit_bytes:
            out_path = os.path.join(output_dir, filename)
            shutil.copy2(filepath, out_path)
            copied_count += 1
            print(f"Copied   -> {filename} (Size: {file_size_bytes/1024:.2f} KB) without modification.")
        else:
            # Compress condition
            file_size_kb = file_size_bytes / 1024
            print(f"Compress -> {filename} (Original: {file_size_kb:.2f} KB)...")
            try:
                with Image.open(filepath) as img:
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    stem = os.path.splitext(filename)[0]
                    out_name = f"{stem}.jpg"
                    out_path = os.path.join(output_dir, out_name)
                    
                    img.save(out_path, format="JPEG", quality=80, optimize=True)
                    new_size_kb = os.path.getsize(out_path) / 1024
                    print(f"            Saved as {out_name} (New Size: {new_size_kb:.2f} KB)")
                    compressed_count += 1
            except Exception as e:
                print(f"            Error compressing {filename}: {e}")
                
    print(f"\nDone! Compressed: {compressed_count}, Copied unmodified: {copied_count} files using Python.")

if __name__ == "__main__":
    compress_images()
