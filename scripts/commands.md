# Frequent Commands

### Image Compression (Incremental) - Recommended
Compresses all images larger than X KB (e.g. 400), skipping images already in `images` and skipping any file starting with `logo`.
```bash
./scripts/compress_incremental.sh 400
```

### Image Compression (Full Bash)
Compresses all images from scratch, overwriting/processing everything.
```bash
./scripts/compress_images.sh 400
```

### Image Compression (Python Alternative)
Same functionality, using Python (requires `Pillow` library).
```bash
python scripts/compress_images.py 400
```
