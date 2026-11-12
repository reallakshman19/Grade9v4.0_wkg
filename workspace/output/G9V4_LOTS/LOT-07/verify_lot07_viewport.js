const { chromium } = require('C:/Users/reall/AppData/Local/Temp/pw-1.52.0/node_modules/playwright-core');
const path = require('path');

const DASHBOARD_URL = 'file:///' + path.resolve(__dirname, 'review/index.html').replace(/\\/g, '/');

async function checkViewport(page, width, height, label) {
    await page.setViewportSize({ width, height });
    await page.goto(DASHBOARD_URL, { waitUntil: 'load' });
    await page.waitForTimeout(500);

    const metrics = await page.evaluate(() => {
        return {
            windowWidth: window.innerWidth,
            docScrollWidth: document.documentElement.scrollWidth,
            bodyScrollWidth: document.body.scrollWidth,
            containerScrollWidth: document.querySelector('.container') ? document.querySelector('.container').scrollWidth : null,
            tableWrapperScrollWidth: document.querySelector('.table-wrapper') ? document.querySelector('.table-wrapper').scrollWidth : null,
            tableWrapperClientWidth: document.querySelector('.table-wrapper') ? document.querySelector('.table-wrapper').clientWidth : null
        };
    });

    console.log(`[${label} ${width}x${height}] Window: ${metrics.windowWidth}, DocScrollWidth: ${metrics.docScrollWidth}, BodyScrollWidth: ${metrics.bodyScrollWidth}`);

    // Body scroll width must not exceed window width by more than 1px
    if (metrics.bodyScrollWidth > metrics.windowWidth + 1) {
        console.error(`FAILED: Horizontal overflow detected on ${label}! bodyScrollWidth (${metrics.bodyScrollWidth}) > windowWidth (${metrics.windowWidth})`);
        return false;
    }

    // Verify presence of table and badges
    const badgeCount = await page.locator('.badge-admission').count();
    if (badgeCount !== 5) {
        console.error(`FAILED: Expected 5 admission badges, found ${badgeCount}`);
        return false;
    }

    console.log(`PASSED: ${label} viewport cleanly rendered without horizontal page overflow.`);
    return true;
}

async function run() {
    console.log("Starting LOT-07 Viewport Verification...");
    console.log("Target URL:", DASHBOARD_URL);

    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    let allPassed = true;
    try {
        const passMobile = await checkViewport(page, 375, 667, 'Mobile');
        const passDesktop = await checkViewport(page, 1365, 900, 'Desktop');
        allPassed = passMobile && passDesktop;
    } catch (err) {
        console.error("Test threw exception:", err);
        allPassed = false;
    } finally {
        await browser.close();
    }

    if (!allPassed) {
        console.error("LOT-07 Viewport Verification FAILED.");
        process.exit(1);
    } else {
        console.log("ALL LOT-07 VIEWPORT CHECKS PASSED.");
    }
}

run();
