# Bash Script Explanation: `compress_images.sh`

This guide explains how the bash script works, line by line. A Bash script is essentially a text file containing a series of commands that you could otherwise type manually into your terminal, but here they are automated.

---

### 1. The "Shebang"
```bash
#!/bin/bash
```
The very first line of almost every bash script is called the "Shebang" (`#!`). 
- **Concept**: It tells your computer's operating system exactly which program to use to run this resulting script. Here, we are telling it to use `/bin/bash` (the Bash shell).

### 2. Variables and Arguments
```bash
SIZE_LIMIT_KB=${1:-400}
SIZE_LIMIT_BYTES=$(echo "$SIZE_LIMIT_KB * 1024" | bc | awk '{print int($1)}')
```
- **Variables** are like named containers for data. `SIZE_LIMIT_KB` is a variable.
- **`$1`**: This represents the *first argument* you pass when running the script (e.g., in `./compress_images.sh 400`, the `400` is `$1`).
- **`${1:-400}`**: This is a fallback concept. It means "use argument 1, but if the user didn't provide it, default to `400`".
- **`bc` and `awk`**: Bash isn't great at complex math (like decimals). `bc` (Basic Calculator) lets us multiply the Kilobytes by 1024 to find the exact number of Bytes. `awk` just cleans up any leftover decimal points so we get a clean whole number.

### 3. Finding Directory Paths
```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
IMAGES_DIR="$BASE_DIR/images_orig"
OUTPUT_DIR="$BASE_DIR/images"
```
Instead of hardcoding a path (like `/Users/Deepak/...`), a good script figures out where it is automatically!
- **`$0`**: Refers to the name of the script itself.
- **`dirname`**: Extracts the folder path from a file. 
- **`pwd`**: Stands for "Print Working Directory", which grabs the absolute path of the current folder.
- Working together, these lines flawlessly find your `scripts` folder, navigate one folder up (`BASE_DIR`), and locate your `images_orig` and `images` folders.

### 4. Creating Directories and Adding Logic Checks
```bash
mkdir -p "$OUTPUT_DIR"
```
- **`mkdir -p`**: "Make directory". The `-p` flag tells the computer: "Create this folder, but if it already exists, just ignore this step and don't throw an error."

```bash
if [ ! -d "$IMAGES_DIR" ]; then
    echo "Images directory not found!"
    exit 1
fi
```
- **`if [ ! -d ... ]`**: This is an "If Statement". The `-d` checks if a directory exists. The `!` means "NOT". So, "If the images directory DOES NOT exist, print a warning and exit the script entirely (`exit 1`)."

### 5. Finding the Right Files
```bash
find "$IMAGES_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read -r filepath; do
```
- **`find`**: A powerful command to search for files.
- **`-type f`**: Look strictly for files (not folders).
- **`-iname`**: Case-insensitive matches (meaning it'll match `.JPG` or `.jpg`). We use `-o` (OR) to chain format checks together.
- **`|` (The Pipe)**: This takes the output list of files from `find` and *pipes* it into a `while` loop, processing files one by one.

### 6. Isolating the Filename
```bash
filename=$(basename "$filepath")
filename_lower=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
```
- **`basename`**: Strips out the long folder path and just leaves `image.jpg`.
- **`tr`** (Translate): Here, we convert all uppercase letters to lowercase. We do this to make sure `Logo.png`, `LOGO.png`, or `logo.png` are all treated equally in the next steps.

### 7. File Size Evaluation
```bash
filesize=$(stat -f%z "$filepath")
```
- **`stat`**: A command that gets detailed information about a file.
- **`-f%z`**: Specific to Macs, this extracts precisely the file size in purely *bytes*.

### 8. The Core "If/Else" Logic
```bash
if [[ "$filename_lower" == logo* ]] || [ "$filesize" -le "$SIZE_LIMIT_BYTES" ]; then
    cp -p "$filepath" "$OUTPUT_DIR/$filename"
```
- **`== logo*`**: The asterisk `*` means "anything". So, if the filename starts with "logo" followed by absolutely anything else.
- **`||`**: This means "OR".
- **`-le`**: Stands for "Less than or Equal to".
- **`cp -p`**: The copy command. The `-p` flag tells the computer to preserve the original file's creation/modified dates when saving.

```bash
else
    stem="${filename%.*}"
    out_name="${stem}.jpg"
```
If the image doesn't meet the above rule, it triggers the `else` (compress it):
- **`${filename%.*}`**: This strips the extension (e.g., `.png` or `.jpg`) off the filename, giving us the pure "stem" name so we can append `.jpg` to it.

### 9. The Compression Engines
```bash
sips -s format jpeg -s formatOptions 80 "$filepath" --out "$out_path" > /dev/null
```
- **`sips`**: ("Scriptable Image Processing System") is a command built straight into macOS for manipulating images natively.
- **`formatOptions 80`**: We force it into a JPEG format and apply an 80% compression factor. 
- **`> /dev/null`**: This acts like a digital black hole. We funnel `sips`'s loud underlying developer logs in here so they don't clutter up your terminal screen.

### 10. Counting and Looping
```bash
done
```
- This indicates the loop is over. The script will jump back to the logic block as many times as needed until it runs out of images, and then exit.
