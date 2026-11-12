const path = require('path');
const { chromium } = require('C:/Users/reall/AppData/Local/Temp/pw-1.52.0/node_modules/playwright-core');

const FILE_PATH = path.resolve('workspace/output/G9V4_LOTS/LOT-01/review/source-gate.html');
const URL = 'file:///' + FILE_PATH.replace(/\\/g, '/');

(async () => {
  console.log(`Testing source-gate.html with Playwright Chromium: ${URL}`);
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));

  await page.goto(URL, { waitUntil: 'load' });

  // 1. Mobile Viewport 375px
  console.log("\n--- Testing 375px Viewport (Mobile) ---");
  await page.setViewportSize({ width: 375, height: 667 });
  await page.waitForTimeout(200);

  const mobileMetrics = await page.evaluate(() => ({
    docClientWidth: document.documentElement.clientWidth,
    docScrollWidth: document.documentElement.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
    tableContainerScrollWidth: document.querySelector('.table-container').scrollWidth,
    tableContainerClientWidth: document.querySelector('.table-container').clientWidth
  }));
  console.log("Mobile Metrics (375px):", mobileMetrics);

  const mobilePass = mobileMetrics.docScrollWidth <= 375 && mobileMetrics.bodyScrollWidth <= 375;
  console.log(`Document horizontal overflow at 375px: ${mobilePass ? "NONE (PASS)" : "OVERFLOW (FAIL)"}`);
  if (!mobilePass) {
    throw new Error(`Mobile document overflows! docScrollWidth=${mobileMetrics.docScrollWidth} > 375`);
  }

  // 2. Desktop Viewport 1365px
  console.log("\n--- Testing 1365px Viewport (Desktop) ---");
  await page.setViewportSize({ width: 1365, height: 900 });
  await page.waitForTimeout(200);

  const desktopMetrics = await page.evaluate(() => ({
    docClientWidth: document.documentElement.clientWidth,
    docScrollWidth: document.documentElement.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth
  }));
  console.log("Desktop Metrics (1365px):", desktopMetrics);

  const desktopPass = desktopMetrics.docScrollWidth <= 1365;
  console.log(`Document horizontal overflow at 1365px: ${desktopPass ? "NONE (PASS)" : "OVERFLOW (FAIL)"}`);
  if (!desktopPass) {
    throw new Error(`Desktop document overflows! docScrollWidth=${desktopMetrics.docScrollWidth} > 1365`);
  }

  // 3. Page Errors
  console.log(`\nPage errors caught: ${errors.length}`);
  if (errors.length > 0) throw new Error(`Caught page errors: ${errors.join(', ')}`);
  console.log("PASS: Zero console errors or unhandled exceptions.");

  await browser.close();
  console.log("\n>>> ALL PLAYWRIGHT CHROMIUM SOURCE-GATE CHECKS PASSED SUCCESSFULLY! <<<\n");
})().catch(err => {
  console.error("FAIL:", err);
  process.exit(1);
});
