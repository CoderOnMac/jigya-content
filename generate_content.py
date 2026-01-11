#!/usr/bin/env python3
"""
Jigya Content Generator v1.1 - MATCHES YOUR words.json FORMAT
"""

import json
import os
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import shutil

load_dotenv()

# ========== CONFIG ==========
REPO_ROOT = Path(__file__).parent
WORDS_JSON = REPO_ROOT / "words.json"
IMAGES_DIR = REPO_ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COMFYUI_URL = "http://127.0.0.1:8188"
if GEMINI_API_KEY:
    print("✅ Gemini key found")
else:
    print("❌ NO GEMINI KEY - add to .env")
    exit(1)

WORD_SEEDS = ["dissolute"]
BATCH_SIZE = 1

# ========== LOAD/SAVE WORDS ==========
def load_words():
    if not WORDS_JSON.exists():
        return {"version": 1, "words": []}
    
    with open(WORDS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, dict) else {"version": 1, "words": data}

def save_words(data):
    with open(WORDS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_existing_words(data):
    return {w["word_anglicized"].lower() for w in data.get("words", [])}

# ========== GEMINI TEXT GENERATION ==========
def generate_content_via_gemini(seed):
    prompt = f"""Generate vocabulary content for "{seed}" (English idiom/vocabulary). 
Respond with ONLY clean JSON, no markdown:

{{
  "definition": "1 sentence definition",
  "example_sentence": "1 vivid example sentence using the word", 
  "image_prompt": "Studio Ghibli style illustration of the EXAMPLE SENTENCE scene above, vibrant colors, detailed background, cinematic lighting, golden hour, 4:5 aspect ratio"
}}

Keep professional/educational tone."""
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3}  # NO response_mime_type
    }
    
    try:
        resp = requests.post(f"{url}?key={GEMINI_API_KEY}", json=payload, timeout=30)
        resp.raise_for_status()
        
        # Extract JSON from response (handles markdown, etc.)
        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        
        # Clean common wrappers
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        
        print(f"📝 Gemini raw: {text[:100]}...")  # Debug
        
        return json.loads(text)
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse failed: {e}")
        print(f"Raw text: {text}")
        return None
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return None

def generate_content_via_gemini(seed):
    """TEST MODE: Hardcoded → tests ComfyUI + words.json"""
    print(f"🧪 TEST MODE: {seed}")
    return {
        "definition": f"A person living a wild, unrestrained lifestyle.",
        "example_sentence": f"The dissolute students threw parties every weekend.",
        "image_prompt": "Studio Ghibli style illustration of dissolute college students partying in messy dorm, no studying, 4:5 aspect ratio"
    }

# ========== COMFYUI IMAGE ==========
def generate_image_via_comfyui(image_prompt, word_slug):
    """Generate + copy to repo images/ with clean name"""
    output_filename = f"{word_slug}"  # Clean: just "dissolute"
    
    prompt_payload = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "animagineXLV31_v31.safetensors"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": image_prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": "blurry, low quality, deformed, ugly", "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1280, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {
            "seed": int(time.time()), "steps": 25, "cfg": 7, "sampler_name": "euler", 
            "scheduler": "normal", "denoise": 1, "model": ["1", 0], "positive": ["2", 0], 
            "negative": ["3", 0], "latent_image": ["4", 0]
        }},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "temp_output", "images": ["6", 0]}}  # Temp name
    }
    
    try:
        # Submit prompt
        resp = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": prompt_payload}, timeout=120)
        resp.raise_for_status()
        prompt_id = resp.json()["prompt_id"]
        
        # Wait + find output
        for _ in range(60):
            time.sleep(5)
            history = requests.get(f"{COMFYUI_URL}/history/{prompt_id}").json()
            if prompt_id in history:
                images = history[prompt_id]["outputs"]["7"]["images"]
                if images:
                    # ComfyUI output path (StabilityMatrix default)
                    comfy_output = Path(r"C:\Users\Deepansh\Downloads\Softwares\StabilityMatrix-win-x64\Data\Images\Text2Img")
                    
                    # Find latest temp_output_*.png
                    temp_files = list(comfy_output.glob("temp_output_*.png"))
                    if temp_files:
                        latest = max(temp_files, key=os.path.getctime)
                        
                        # Copy → repo with clean name
                        target = IMAGES_DIR / f"{word_slug}.png"
                        shutil.copy2(latest, target)
                        
                        # Optional: delete temp
                        # latest.unlink()
                        
                        print(f"✅ Copied: images/{word_slug}.png")
                        return str(target)
        
        return None
        
    except Exception as e:
        print(f"❌ ComfyUI: {e}")
        return None

# ========== MAIN ==========
def main():
    print("🚀 Jigya Content Factory v1.1 (Your Format)")
    
    data = load_words()
    existing_words = get_existing_words(data)
    
    generated = 0
    words_list = data.setdefault("words", [])
    
    for i, seed in enumerate(WORD_SEEDS[:BATCH_SIZE]):
        if seed.lower() in existing_words:
            print(f"⏭️ Skipping: {seed}")
            continue
            
        print(f"\n[{i+1}/{BATCH_SIZE}] {seed}")
        
        # Gemini content
        content = generate_content_via_gemini(seed)
        if not content:
            print("❌ Gemini failed")
            continue
            
        # Generate image
        slug = seed.lower().replace(" ", "_")
        filename = f"{slug}_{int(time.time())}"
        image_path = generate_image_via_comfyui(content["image_prompt"], slug)
        if image_path:
            # Add to YOUR format
            new_entry = {
                "id": f"20260111-EN-{len(words_list)+1:03d}",
                "date": "2026-01-11",
                "category": "english",
                "type": "vocabulary",
                "tags": [seed.lower(), "english", "vocabulary"],
                "word_anglicized": seed,
                "word_native": seed,
                "image_url": f"images/{slug}.png",
                "content_payload": content
            }
            
            words_list.append(new_entry)
            save_words(data)
            existing_words.add(seed.lower())
            generated += 1
            print(f"✅ Added: {seed}")
    
    print(f"\n🎉 {generated}/{BATCH_SIZE} new words in your format!")
    print("Check words.json + images/ folder")

if __name__ == "__main__":
    main()
