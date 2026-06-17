const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

async function generatePdf() {
    // 1. Load data
    const dataPath = path.join(__dirname, 'sample_data.json');
    const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

    // 2. Read HTML template
    const templatePath = path.join(__dirname, 'index.html');
    let htmlContent = fs.readFileSync(templatePath, 'utf8');

    // 3. Replace simple placeholders
    htmlContent = htmlContent.replace('{{page_number_left}}', data.page_number_left);
    htmlContent = htmlContent.replace('{{page_number_right}}', data.page_number_right);
    htmlContent = htmlContent.replace(/{{word}}/g, data.word);
    htmlContent = htmlContent.replace('{{definition}}', data.definition);

    // Replace target words in text
    const targetWordHTML = `<span class="target-word">${data.word.toLowerCase()}</span>`;
    const exampleHtml = data.example.replace(new RegExp(data.word, 'gi'), targetWordHTML);
    htmlContent = htmlContent.replace('{{example_html}}', exampleHtml);

    const evolutionHtml = data.evolution_story.replace(new RegExp(data.word, 'gi'), targetWordHTML);
    htmlContent = htmlContent.replace('{{evolution_story_html}}', evolutionHtml);

    htmlContent = htmlContent.replace('{{trivia}}', data.trivia);
    htmlContent = htmlContent.replace('{{image_path}}', data.image_path);

    // 4. Generate Bubbles HTML
    let bubblesHtml = '';
    data.bubbles.forEach((bubble, index) => {
        bubblesHtml += `<div class="bubble bubble-${index + 1}">${bubble}</div>\n`;
    });
    htmlContent = htmlContent.replace('{{bubbles_html}}', bubblesHtml);

    // 5. Generate Word In Action HTML
    let wordInActionHtml = '';
    data.word_in_action.forEach(item => {
        const itemText = item.text.replace(new RegExp(data.word, 'gi'), targetWordHTML);
        wordInActionHtml += `
        <div class="action-item">
            <p class="action-source">${item.source}</p>
            <p class="action-text">"${itemText}"</p>
        </div>
        `;
    });
    htmlContent = htmlContent.replace('{{word_in_action_html}}', wordInActionHtml);

    // 6. Save populated HTML to a temporary file
    const tempHtmlPath = path.join(__dirname, 'temp_render.html');
    fs.writeFileSync(tempHtmlPath, htmlContent, 'utf8');

    // 7. Use Playwright to generate PDF
    console.log('Launching browser to generate PDF...');
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    await page.goto(`file://${tempHtmlPath}`, { waitUntil: 'networkidle' });
    
    const outputPath = path.join(__dirname, 'output_manuscript.pdf');
    await page.pdf({
        path: outputPath,
        width: '8.5in',
        height: '11in',
        printBackground: true,
        margin: { top: '0', right: '0', bottom: '0', left: '0' }
    });

    await browser.close();

    // 8. Clean up
    if (fs.existsSync(tempHtmlPath)) {
        fs.unlinkSync(tempHtmlPath);
    }

    console.log(`✅ Success! PDF generated at: ${outputPath}`);
}

generatePdf().catch(console.error);
