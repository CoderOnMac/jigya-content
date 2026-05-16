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


### Git Pull Rebase
When multiple people work on the same branch, your local commits and the remote commits can "diverge." A normal `git pull` creates an extra, often messy, "merge commit" to tie the histories together.

To cleanly fetch the remote changes and keep a straight, linear history, use:
```bash
git pull --rebase
```
**What it does:** It pulls the latest changes from the remote server, temporarily sets aside your local commits, updates your files to match the server, and then "replays" your local commits cleanly on top of the remote ones.
