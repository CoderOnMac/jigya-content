# Amazon KDP Print Requirements

Publishing a physical book on Amazon KDP (Kindle Direct Publishing) requires strict adherence to their print specifications. Our system handles these automatically.

## Trim Size
The "Trim Size" is the final physical dimension of your printed book. We have set this system to `8.5 x 11 inches`, which is standard for workbooks and large visual books.
This is enforced via CSS `@page { size: 8.5in 11in; }` and Playwright's `page.pdf({ width: '8.5in', height: '11in' })` arguments.

## Bleed vs No-Bleed
- **Bleed** means an image goes all the way to the absolute edge of the paper, meaning the printing press actually prints past the cut line, and then physically slices it off.
- **No-Bleed** means everything must sit safely inside a white margin.

In our system, the left page has a white margin (`padding: 30px;` in `.left-page`). This makes it safely a "No-Bleed" interior. If you wanted the image to touch the edge of the paper, you would remove that padding and instruct KDP to print *with Bleed*.

## Resolution (DPI)
KDP requires 300 DPI (Dots Per Inch) for print-quality images.
Since HTML doesn't strictly adhere to DPI in the traditional Photoshop sense, you must ensure that your source image (`image_path` in JSON) is physically large enough.
An 8.5 x 11 inch page at 300 DPI equals **2550 x 3300 pixels**. As long as the images you put in the JSON are roughly that size or larger, KDP will accept them without warnings!
