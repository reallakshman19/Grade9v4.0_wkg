const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/reall/AppData/Local/Temp/pw-1.52.0/node_modules/playwright-core');

const FILE_PATH = path.resolve('workspace/output/G9V4_LOTS/LOT-00/inventory.html');
const URL = 'file:///' + FILE_PATH.replace(/\\/g, '/');

(async () => {
  console.log(`Testing dashboard with Playwright Chromium: ${URL}`);
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));

  await page.goto(URL, { waitUntil: 'load' });

  // 1. Test 375px viewport (Mobile)
  console.log("\n--- Testing 375px Viewport (Mobile) ---");
  await page.setViewportSize({ width: 375, height: 667 });
  await page.waitForTimeout(200);

  const mobileMetrics = await page.evaluate(() => {
    return {
      docClientWidth: document.documentElement.clientWidth,
      docScrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body.scrollWidth,
      containerScrollWidth: document.querySelector('.container').scrollWidth,
      tableContainerScrollWidth: document.querySelector('.table-container').scrollWidth,
      tableContainerClientWidth: document.querySelector('.table-container').clientWidth,
      rowsCount: document.querySelectorAll('#inventoryTable tbody tr').length
    };
  });
  console.log("Mobile Metrics (375px):", mobileMetrics);

  const mobilePass = mobileMetrics.docScrollWidth <= 375 && mobileMetrics.bodyScrollWidth <= 375;
  console.log(`Document horizontal overflow at 375px: ${mobilePass ? "NONE (PASS)" : "OVERFLOW (FAIL)"}`);
  if (!mobilePass) {
    throw new Error(`Mobile document overflows! docScrollWidth=${mobileMetrics.docScrollWidth} > 375`);
  }

  // 2. Test Input Event (Typing / Pasting in Search)
  console.log("\n--- Testing Search Input Event ---");
  // Test typing a specific unique record ID: 'EX-M39'
  await page.evaluate(() => {
    const input = document.getElementById('searchInput');
    input.value = 'EX-M39';
    input.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await page.waitForTimeout(100);

  let filteredCount = await page.evaluate(() => {
    return document.querySelectorAll('#inventoryTable tbody tr:not([style*="display: none"])').length;
  });
  console.log(`Visible rows after typing 'EX-M39': ${filteredCount}`);
  if (filteredCount !== 1) {
    throw new Error(`Expected 1 row for 'EX-M39', got ${filteredCount}`);
  }
  console.log("PASS: 'input' event successfully triggers instant 1-row filtering for 'EX-M39'!");

  // Test pasting text into search: 'WEP07-03'
  await page.evaluate(() => {
    const input = document.getElementById('searchInput');
    input.value = 'WEP07-03';
    input.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await page.waitForTimeout(100);
  filteredCount = await page.evaluate(() => {
    return document.querySelectorAll('#inventoryTable tbody tr:not([style*="display: none"])').length;
  });
  console.log(`Visible rows after pasting 'WEP07-03': ${filteredCount}`);
  if (filteredCount !== 1) {
    throw new Error(`Expected 1 row for 'WEP07-03', got ${filteredCount}`);
  }
  console.log("PASS: Pasted text triggers 'input' event correctly!");

  // Reset search
  await page.evaluate(() => {
    const input = document.getElementById('searchInput');
    input.value = '';
    input.dispatchEvent(new Event('input', { bubbles: true }));
  });

  // 3. Test 1365px Viewport (Desktop)
  console.log("\n--- Testing 1365px Viewport (Desktop) ---");
  await page.setViewportSize({ width: 1365, height: 900 });
  await page.waitForTimeout(200);

  const desktopMetrics = await page.evaluate(() => {
    return {
      docClientWidth: document.documentElement.clientWidth,
      docScrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body.scrollWidth,
      rowsCount: document.querySelectorAll('#inventoryTable tbody tr:not([style*="display: none"])').length
    };
  });
  console.log("Desktop Metrics (1365px):", desktopMetrics);

  const desktopPass = desktopMetrics.docScrollWidth <= 1365;
  console.log(`Document horizontal overflow at 1365px: ${desktopPass ? "NONE (PASS)" : "OVERFLOW (FAIL)"}`);
  if (!desktopPass) {
    throw new Error(`Desktop document overflows! docScrollWidth=${desktopMetrics.docScrollWidth} > 1365`);
  }

  // 4. Verify Filters
  console.log("\n--- Testing Dropdown Filters ---");
  // Scope filter: IN_SCOPE
  await page.selectOption('#scopeFilter', 'IN_SCOPE');
  const inScopeCount = await page.evaluate(() => document.querySelectorAll('#inventoryTable tbody tr:not([style*="display: none"])').length);
  console.log(`Rows for IN_SCOPE: ${inScopeCount} (Expected 66)`);
  if (inScopeCount !== 66) throw new Error(`Expected 66 rows for IN_SCOPE, got ${inScopeCount}`);

  // Deduplication filter: PRIMARY_ONLY
  await page.selectOption('#dupFilter', 'PRIMARY_ONLY');
  const uniqueInScopeCount = await page.evaluate(() => document.querySelectorAll('#inventoryTable tbody tr:not([style*="display: none"])').length);
  console.log(`Rows for IN_SCOPE + PRIMARY_ONLY: ${uniqueInScopeCount} (Expected 65)`);
  if (uniqueInScopeCount !== 65) throw new Error(`Expected 65 rows for IN_SCOPE + PRIMARY_ONLY, got ${uniqueInScopeCount}`);

  // Verified key filter
  await page.selectOption('#scopeFilter', 'ALL');
  await page.selectOption('#keyFilter', 'VERIFIED');
  const verifiedCount = await page.evaluate(() => document.querySelectorAll('#inventoryTable tbody tr:not([style*="display: none"])').length);
  console.log(`Rows for VERIFIED + PRIMARY_ONLY: ${verifiedCount} (Expected 1)`);
  if (verifiedCount !== 1) throw new Error(`Expected 1 row for VERIFIED + PRIMARY_ONLY, got ${verifiedCount}`);

  // Reset filters
  await page.selectOption('#scopeFilter', 'ALL');
  await page.selectOption('#keyFilter', 'ALL');
  await page.selectOption('#dupFilter', 'ALL');

  console.log(`\nPage errors caught: ${errors.length}`);
  if (errors.length > 0) throw new Error(`Caught page errors: ${errors.join(', ')}`);
  console.log("PASS: Zero console errors or unhandled exceptions.");

  await browser.close();
  console.log("\n>>> ALL PLAYWRIGHT CHROMIUM DASHBOARD CHECKS PASSED SUCCESSFULLY! <<<\n");
})().catch(err => {
  console.error("FAIL:", err);
  process.exit(1);
});
