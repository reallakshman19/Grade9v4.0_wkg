const http = require('http');
const { spawn } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const TARGET_URL = "file:///D:/CodeD/grade9v4/workspace/output/G9V4_LOTS/LOT-00/inventory.html";
const PORT = 9222;
const USER_DATA = path.join(os.tmpdir(), 'chrome-test-profile-' + Date.now());

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function waitForChrome(port, maxTries = 20) {
  for (let i = 0; i < maxTries; i++) {
    try {
      const data = await fetchJson(`http://127.0.0.1:${port}/json/list`);
      if (Array.isArray(data) && data.length > 0) return data;
    } catch (e) {
      // wait
    }
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error("Timeout waiting for Chrome CDP");
}

async function run() {
  console.log("Starting Chrome in headless mode with clean profile...");
  const chrome = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${USER_DATA}`,
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    TARGET_URL
  ]);

  try {
    const listData = await waitForChrome(PORT);
    const page = listData.find(p => p.type === 'page');
    if (!page) throw new Error("No page target found");

    console.log(`Connected to page target: ${page.id}`);
    const ws = new WebSocket(page.webSocketDebuggerUrl);

    let id = 1;
    const callbacks = new Map();
    const pageErrors = [];

    ws.onmessage = msg => {
      const data = JSON.parse(msg.data);
      if (data.method === 'Runtime.consoleAPICalled') {
        if (data.params.type === 'error') {
          pageErrors.push(data.params.args.map(a => a.value || a.description).join(' '));
        }
      } else if (data.method === 'Runtime.exceptionThrown') {
        pageErrors.push(data.params.exceptionDetails.text);
      } else if (data.id && callbacks.has(data.id)) {
        const { resolve, reject } = callbacks.get(data.id);
        callbacks.delete(data.id);
        if (data.error) reject(data.error);
        else resolve(data.result);
      }
    };

    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const msgId = id++;
      callbacks.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });

    await new Promise(r => ws.onopen = r);

    await send('Runtime.enable');
    await send('Page.enable');

    // 1. Test 375px viewport (Mobile)
    console.log("Setting viewport to 375x667 (Mobile)...");
    await send('Emulation.setDeviceMetricsOverride', {
      width: 375,
      height: 667,
      deviceScaleFactor: 2,
      mobile: true
    });

    let evalRes = await send('Runtime.evaluate', {
      expression: `({
        docScrollWidth: document.documentElement.scrollWidth,
        bodyScrollWidth: document.body.scrollWidth,
        tableContainerScrollWidth: document.querySelector('.table-container').scrollWidth,
        tableContainerClientWidth: document.querySelector('.table-container').clientWidth,
        visibleRowCount: document.querySelectorAll('#inventoryTable tbody tr:not([style*="display: none"])').length
      })`,
      returnByValue: true
    });

    const m = evalRes.result.value;
    console.log(`Mobile (375px) metrics:`, m);
    if (m.docScrollWidth > 375) {
      throw new Error(`Mobile document overflows! docScrollWidth = ${m.docScrollWidth} > 375`);
    }
    if (m.bodyScrollWidth > 375) {
      throw new Error(`Mobile body overflows! bodyScrollWidth = ${m.bodyScrollWidth} > 375`);
    }
    console.log("PASS: Mobile (375px) has zero document horizontal overflow!");
    console.log(`PASS: Table container scrollable: scrollWidth=${m.tableContainerScrollWidth} > clientWidth=${m.tableContainerClientWidth}`);

    // 2. Test input event search filtering
    console.log("Testing search input with 'input' event...");
    await send('Runtime.evaluate', {
      expression: `(() => {
        const input = document.getElementById('searchInput');
        input.value = 'EX-M4';
        input.dispatchEvent(new Event('input', { bubbles: true }));
      })()`
    });

    evalRes = await send('Runtime.evaluate', {
      expression: `document.querySelectorAll('#inventoryTable tbody tr:not([style*="display: none"])').length`,
      returnByValue: true
    });
    console.log(`Filtered row count for 'EX-M4': ${evalRes.result.value}`);
    if (evalRes.result.value !== 1) {
      throw new Error(`Expected 1 row for 'EX-M4', got ${evalRes.result.value}`);
    }
    console.log("PASS: 'input' event correctly triggers search filter!");

    // Reset search
    await send('Runtime.evaluate', {
      expression: `(() => {
        const input = document.getElementById('searchInput');
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
      })()`
    });

    // 3. Test 1365px viewport (Desktop)
    console.log("Setting viewport to 1365x900 (Desktop)...");
    await send('Emulation.setDeviceMetricsOverride', {
      width: 1365,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });

    evalRes = await send('Runtime.evaluate', {
      expression: `({
        docScrollWidth: document.documentElement.scrollWidth,
        bodyScrollWidth: document.body.scrollWidth,
        visibleRowCount: document.querySelectorAll('#inventoryTable tbody tr:not([style*="display: none"])').length
      })`,
      returnByValue: true
    });
    const d = evalRes.result.value;
    console.log(`Desktop (1365px) metrics:`, d);
    if (d.docScrollWidth > 1365) {
      throw new Error(`Desktop document overflows! docScrollWidth = ${d.docScrollWidth} > 1365`);
    }
    console.log("PASS: Desktop (1365px) has zero document horizontal overflow!");

    // 4. Check console errors
    console.log(`Page errors caught: ${pageErrors.length}`);
    if (pageErrors.length > 0) {
      throw new Error(`Console errors found: ${pageErrors.join(', ')}`);
    }
    console.log("PASS: Zero console errors / JS exceptions!");

    ws.close();
    console.log("\nALL DASHBOARD BROWSER VIEWPORT CHECKS PASSED!");
  } finally {
    chrome.kill();
    try { fs.rmSync(USER_DATA, { recursive: true, force: true }); } catch (e) {}
  }
}

run().catch(err => {
  console.error("FAIL:", err);
  process.exit(1);
});
