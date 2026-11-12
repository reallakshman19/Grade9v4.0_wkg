async page => {
  const root='http://127.0.0.1:8785';
  const results=[]; const errors=[];
  const check=(name,value)=>{results.push({name,pass:!!value});if(!value)throw new Error(name)};
  page.on('pageerror',e=>errors.push(String(e)));
  for(const width of [1280,390]){
    await page.setViewportSize({width,height:900});
    await page.goto(root+'/rendered/core2.html');
    await page.evaluate(()=>localStorage.clear());await page.reload();
    const a=page.locator('#SYN-WPE-DIRECTION-CONTROL-01');
    const sol=a.locator('details[data-g9-payload-ref$="-solution"]');
    const tag=width+':native:';
    check(tag+'nine records',await page.locator('article[data-g9-role="CORE2"]').count()===9);
    check(tag+'source type clearly synthetic',(await a.innerText()).includes('SYNTHETIC CONTROL ONLY'));
    check(tag+'no visible answer before commitment',!(await a.innerText()).includes('C — Zero work by the vertical force.'));
    await sol.locator('summary').click();
    check(tag+'premature solution opening refused',!(await sol.evaluate(el=>el.open)));
    await a.locator('[data-g9-commit]').click();
    check(tag+'empty commitment refused',await a.getAttribute('data-attempted')===null);
    await a.getByText('Need a hint? · guided support',{exact:true}).click();
    const next=a.locator('[data-g9-next-rung]');await next.click();
    check(tag+'one support rung',await a.locator('[data-g9-rung]').count()===1);
    const reveal=a.locator('details[data-g9-support-reveal]').first();await reveal.locator('summary').click();
    check(tag+'support body revealed',(await a.innerText()).includes('Keep your response about the work of the stated force.'));
    await next.click();
    check(tag+'two support rungs',await a.locator('[data-g9-rung]').count()===2);
    check(tag+'support ladder ends',await next.isDisabled());
    check(tag+'assistance retained',await a.getAttribute('data-g9-assisted')==='1');
    check(tag+'help does not reveal answer',!(await a.innerText()).includes('C — Zero work by the vertical force.'));
    await a.locator('input[type=radio][value="1"]').check();
    await a.locator('[data-g9-commit]').focus();await page.keyboard.press('Enter');
    check(tag+'keyboard commits chosen response',await a.getAttribute('data-attempted')==='1');
    check(tag+'commit unlocks solution',await sol.getAttribute('data-locked')===null);
    await sol.locator('summary').click();
    check(tag+'source answer now visible',(await a.innerText()).includes('C — Zero work by the vertical force.'));
    check(tag+'native did not grade wrong choice',!(await a.innerText()).includes('Attempt recorded — incorrect.'));
    await page.reload();
    check(tag+'reload retains attempted state',await a.getAttribute('data-attempted')==='1');
    check(tag+'reload retains response B',await a.locator('input[value="1"]').isChecked());
    check(tag+'reload retains assisted state',await a.getAttribute('data-g9-assisted')==='1');
    await page.evaluate(()=>localStorage.clear());await page.reload();
    await a.locator('input[value="2"]').focus();await page.keyboard.press('Space');
    await a.locator('[data-g9-commit]').focus();await page.keyboard.press('Enter');
    check(tag+'keyboard radio choice C retained',await a.locator('input[value="2"]').isChecked());
    const first=page.locator('#TB-WPE-ILL-01');
    await first.locator('[data-g9-attempt]').fill('-24 J');await first.locator('[data-g9-commit]').click();
    check(tag+'textbook typed commitment',await first.getAttribute('data-attempted')==='1');
    const bookMCQ=page.locator('#TB-WPE-ILL-06');await bookMCQ.locator('input[value="1"]').check();await bookMCQ.locator('[data-g9-commit]').click();
    check(tag+'textbook MCQ commitment',await bookMCQ.getAttribute('data-attempted')==='1');
    check(tag+'no page horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));
    await a.screenshot({path:'D:/CodeD/g9v3.5/chatgpt/output/WPE_Core2_Native_Integration_R1_20261030/review/native-'+width+'.png'});
    // Correct the received browser oracle: exact strings, a wrong-answer control,
    // actual URL navigation, and keyboard interaction. Original files stay intact.
    for(const [choice,expected] of [['B','Attempt recorded — incorrect.'],['C','Attempt recorded — correct.']]){
      await page.goto(root+'/received-engineering/outputs/SYNTHETIC_CORE2_GOLDEN.html');
      await page.locator('input[value="'+choice+'"]').focus();await page.keyboard.press('Space');
      await page.getByRole('button',{name:'Commit attempt',exact:true}).focus();await page.keyboard.press('Enter');
      const text=await page.locator('#result').innerText();
      check(width+':received-viewer:exact '+choice,text===expected);
      if(choice==='B'){
        check(width+':received-viewer:negative control rejects positive verdict',text!=='Attempt recorded — correct.');
        check(width+':received-viewer:old substring oracle demonstrated unsafe',text.includes('correct'));
      }
    }
  }
  await page.goto(root+'/index.html');
  check('Owner matrix has fourteen cells',await page.locator('#matrix [data-cell]').count()===14);
  await page.goto(root+'/review.html');
  check('Owner catalogue has twenty-three records',await page.locator('.record').count()===23);
  await page.locator('#category').selectOption('examination');
  check('examination filter shows fourteen leads',await page.locator('.record:visible').count()===14);
  await page.locator('#search').fill('EX-M105');
  check('search isolates the exact lead',await page.locator('.record:visible').count()===1);
  await page.locator('#search').fill('');await page.locator('#category').selectOption('textbook');
  check('textbook filter shows eight',await page.locator('.record:visible').count()===8);
  await page.locator('#category').selectOption('synthetic');
  check('synthetic filter shows one',await page.locator('.record:visible').count()===1);
  await page.goto(root+'/review.html?category=examination&operation=RETRIEVE&band=D3');
  check('empty matrix cell remains an honest gap',await page.locator('.record:visible').count()===0);
  check('no runtime page exceptions',errors.length===0);
  return {scope:'AUTHOR_BROWSER_CHECKS; native nine-record reader and received synthetic standalone viewer; no independent QA',
    browser:'Chrome via Playwright CLI',results,passed:results.filter(x=>x.pass).length,total:results.length,page_errors:errors,
    limitations:['Native UI is commitment/reveal/self-check, not automatic grading.','Local storage is not independently saved P1 research evidence.','Static source inspection can recover answer bytes.','Inherited presentation and portal-link findings remain open.']};
}
