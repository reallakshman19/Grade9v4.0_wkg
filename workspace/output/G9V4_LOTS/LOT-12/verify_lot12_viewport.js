const { chromium } = require('C:/Users/reall/AppData/Local/Temp/pw-1.52.0/node_modules/playwright-core');
const path = require('path');

const DASHBOARD_URL = 'file:///' + path.resolve(__dirname, 'review/index.html').replace(/\\/g, '/');

async function run() {
    console.log("Starting LOT-12 Viewport Verification...");
    console.log("Target URL:", DASHBOARD_URL);

    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    let allPassed = true;

    try {
        // Mobile 375x667
        await page.setViewportSize({ width: 375, height: 667 });
        await page.goto(DASHBOARD_URL, { waitUntil: 'load' });
        await page.waitForTimeout(500);

        let bodyScrollWidth = await page.evaluate(() => document.body.scrollWidth);
        let docScrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
        let windowWidth = await page.evaluate(() => window.innerWidth);

        console.log(`[Mobile 375x667] Window: ${windowWidth}, DocScrollWidth: ${docScrollWidth}, BodyScrollWidth: ${bodyScrollWidth}`);
        if (docScrollWidth > windowWidth || bodyScrollWidth > windowWidth) {
            console.error(`FAILED: Horizontal overflow detected on mobile: body=${bodyScrollWidth}, doc=${docScrollWidth}, window=${windowWidth}`);
            allPassed = false;
        } else {
            console.log("PASSED: Mobile viewport cleanly rendered without horizontal page overflow.");
        }

        // Desktop 1365x900
        await page.setViewportSize({ width: 1365, height: 900 });
        await page.goto(DASHBOARD_URL, { waitUntil: 'load' });
        await page.waitForTimeout(500);

        bodyScrollWidth = await page.evaluate(() => document.body.scrollWidth);
        docScrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
        windowWidth = await page.evaluate(() => window.innerWidth);

        console.log(`[Desktop 1365x900] Window: ${windowWidth}, DocScrollWidth: ${docScrollWidth}, BodyScrollWidth: ${bodyScrollWidth}`);
        if (docScrollWidth > windowWidth || bodyScrollWidth > windowWidth) {
            console.error(`FAILED: Horizontal overflow detected on desktop: body=${bodyScrollWidth}, doc=${docScrollWidth}, window=${windowWidth}`);
            allPassed = false;
        } else {
            console.log("PASSED: Desktop viewport cleanly rendered without horizontal page overflow.");
        }
    } finally {
        await browser.close();
    }

    if (allPassed) {
        console.log("ALL LOT-12 VIEWPORT CHECKS PASSED.");
        process.exit(0);
    } else {
        console.error("LOT-12 VIEWPORT VERIFICATION FAILED.");
        process.exit(1);
    }
}

run();
