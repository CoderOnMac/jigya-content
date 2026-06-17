# Amazon KDP Manuscript Print System

This project is a pixel-perfect HTML/CSS publishing system that generates Amazon KDP-ready manuscript PDFs.

## System Architecture
This system utilizes:
- **HTML/CSS Grid & Flexbox**: For a scalable, structured layout.
- **Print CSS**: `@page` properties designed explicitly for 8.5" x 11" output without default margins.
- **Playwright**: A browser automation tool that renders the HTML perfectly and prints it to PDF using Chromium's engine.

## Prerequisites

You can use **either** Node.js or Python to generate the PDF.

### If using Node.js:
1. Ensure Node.js is installed.
2. Run `npm install playwright`
3. Run `node generate_pdf.js`

### If using Python (Virtual Environment recommended):
1. Create a venv: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install playwright && playwright install chromium`
4. Run `python generate_pdf.py`

## Understanding the Code
Please look in the `Knowledge Base` folder to learn about all the concepts used to build this architecture, designed specifically for a beginner to intermediate HTML/CSS developer.
