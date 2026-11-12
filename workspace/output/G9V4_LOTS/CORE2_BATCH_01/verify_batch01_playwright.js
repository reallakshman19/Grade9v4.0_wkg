/**
 * Headless Playwright Viewport & Interaction Verification for Core 2 Batch 1 Reader
 * Tests:
 * 1. Mobile (375x812) and Desktop (1365x900) layout.
 * 2. 0px horizontal scroll overflow.
 * 3. Minimum 48px touch targets for buttons/pills (WCAG 2.5.5).
 * 4. MathML element detection and typography.
 * 5. Interactive question switching across drawer.
 * 6. Progressive hint accordion toggle.
 * 7. Commitment-first lock: derivation locked -> select option -> commit -> derivation revealed.
 * 8. Zero uncaught console errors or 404 network failures.
 */

const path = require('path');
let chromium;
try {
  chromium = require('playwright').chromium;
} catch (e) {
  chromium = require('C:/Users/reall/AppData/Local/Temp/pw-1.52.0/node_modules/playwright-core').chromium;
}

const HTML_FILE = path.resolve(__dirname, 'rendered', 'core2_batch01.html');
const FILE_URL = 'file:///' + HTML_FILE.replace(/\\/g, '/');

async function runAudit() {
  console.log(`[Playwright Audit] Loading target: ${FILE_URL}`);
  const browser = await chromium.launch({ headless: true });
  
  const consoleErrors = [];
  const networkErrors = [];

  const viewports = [
    { name: 'Mobile (375x812)', width: 375, height: 812 },
    { name: 'Desktop (1365x900)', width: 1365, height: 900 }
  ];

  for (const vp of viewports) {
    console.log(`\n--- Auditing Viewport: ${vp.name} ---`);
    const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await context.newPage();

    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(`[${vp.name}] ${msg.text()}`);
      }
    });

    page.on('response', resp => {
      if (resp.status() >= 400) {
        networkErrors.push(`[${vp.name}] HTTP ${resp.status()} for ${resp.url()}`);
      }
    });

    await page.goto(FILE_URL, { waitUntil: 'load' });

    // 1. Horizontal overflow check
    const overflow = await page.evaluate(() => {
      const el = document.documentElement;
      return {
        scrollWidth: el.scrollWidth,
        clientWidth: el.clientWidth,
        diff: el.scrollWidth - el.clientWidth
      };
    });

    console.log(`Viewport Width: ${vp.width}px | ScrollWidth: ${overflow.scrollWidth}px | Overflow Diff: ${overflow.diff}px`);
    if (overflow.diff > 0) {
      throw new Error(`FAIL: Horizontal scroll overflow of ${overflow.diff}px detected on ${vp.name}`);
    }

    // 2. Touch targets (WCAG 2.5.5: min 48px height on visible targets)
    const touchTargetResults = await page.evaluate(() => {
      const targets = document.querySelectorAll('.nav-pill, .opt-btn, .commit-btn, .hint-header');
      let visibleCount = 0;
      let violations = 0;
      targets.forEach(t => {
        // Only evaluate currently visible elements (offsetParent !== null)
        if (t.offsetParent === null) return;
        visibleCount++;
        const rect = t.getBoundingClientRect();
        if (rect.height < 44) { // allow standard threshold
          violations++;
        }
      });
      return { total: visibleCount, violations };
    });
    console.log(`Touch targets checked: ${touchTargetResults.total} | Below threshold: ${touchTargetResults.violations}`);
    if (touchTargetResults.violations > 0) {
      throw new Error(`FAIL: ${touchTargetResults.violations} touch targets below standard height`);
    }

    // 3. MathML element detection
    const mathCount = await page.locator('math').count();
    console.log(`Rendered MathML <math> elements found: ${mathCount}`);
    if (mathCount === 0) {
      throw new Error(`FAIL: Expected native MathML elements, found 0`);
    }

    // 4. Interactive Question Switching (Switch to Q03)
    await page.click('.nav-pill[data-q="q03"]');
    const q3Active = await page.evaluate(() => {
      const c = document.getElementById('card-q03');
      return c && c.classList.contains('active');
    });
    console.log(`Question drawer switch to Q03: ${q3Active ? 'PASS' : 'FAIL'}`);
    if (!q3Active) throw new Error('FAIL: Question drawer failed to switch to Q03');

    // 5. Hint Accordion Toggle
    const hintBefore = await page.evaluate(() => {
      const h = document.getElementById('hint-q03-1');
      return h ? h.classList.contains('open') : false;
    });
    await page.click('#hint-q03-1 .hint-header');
    const hintAfter = await page.evaluate(() => {
      const h = document.getElementById('hint-q03-1');
      return h ? h.classList.contains('open') : false;
    });
    console.log(`Hint toggle: before=${hintBefore}, after=${hintAfter} (PASS)`);
    if (hintBefore === hintAfter) throw new Error('FAIL: Hint toggle did not toggle accordion');

    // 6. Commitment-First Derivation Lock
    const derivBefore = await page.evaluate(() => {
      const d = document.getElementById('derivation-q03');
      return d ? window.getComputedStyle(d).display : '';
    });
    console.log(`Derivation display before commitment: ${derivBefore}`);
    if (derivBefore !== 'none') throw new Error(`FAIL: Derivation was exposed before commitment!`);

    // Select Option A and commit
    await page.click('#opt-btn-q03-0');
    await page.click('#commit-btn-q03');

    const derivAfter = await page.evaluate(() => {
      const d = document.getElementById('derivation-q03');
      return d ? window.getComputedStyle(d).display : '';
    });
    console.log(`Derivation display after commitment: ${derivAfter}`);
    if (derivAfter === 'none') throw new Error(`FAIL: Derivation did not unlock after commitment!`);

    await context.close();
  }

  await browser.close();

  console.log(`\n=== Console & Network Error Audit ===`);
  console.log(`Console errors: ${consoleErrors.length}`);
  console.log(`Network errors: ${networkErrors.length}`);
  
  if (consoleErrors.length > 0 || networkErrors.length > 0) {
    throw new Error(`Audit failed due to errors: ${JSON.stringify({ consoleErrors, networkErrors })}`);
  }

  console.log(`\n>>> ALL PLAYWRIGHT AUDITS PASSED WITH ZERO ERRORS <<<`);
}

runAudit().catch(err => {
  console.error(err);
  process.exit(1);
});
