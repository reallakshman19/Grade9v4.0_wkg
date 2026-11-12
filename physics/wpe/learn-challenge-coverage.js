/* Student-first source-question router for the existing Learn → Challenge tile.
 * The 74-question evidence is reconciled against the original bank, 13
 * pre-existing C/E lessons and F01–F08. Routes are practice, not QRT decisions.
 */
(async()=>{
  "use strict";
  const $=s=>document.querySelector(s),panel=$("#question-plan"),
        picker=$("#question-pick"),search=$("#question-search"),status=$("#question-route-status");
  const newEl=(tag,text,cls)=>{const e=document.createElement(tag);if(text!=null)e.textContent=text;if(cls)e.className=cls;return e;};
  const add=(root,tag,text,cls)=>{const e=newEl(tag,text,cls);root.append(e);return e;};
  const valid=s=>typeof s==="string"&&/^[A-Za-z0-9-]{2,64}$/.test(s);
  let bank,map,rows=[],selected=null;
  try{
    const [b,r]=await Promise.all([
      fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json",{cache:"no-store"}),
      fetch("learning-coverage-r1.json",{cache:"no-store"})
    ]);
    if(!b.ok||!r.ok)throw Error("Question Bank evidence unavailable");
    bank=await b.json();map=await r.json();
    if(bank.questions?.length!==74||map.schema!=="wpe-learner-coverage-r1/v1"||map.questions?.length!==74)throw Error("Source inventory changed");
    const original=new Map(bank.questions.map(q=>[q.source_id,q]));
    if(original.size!==74||map.questions.some(row=>!original.has(row.source_id)||row.stem_sha256!==original.get(row.source_id).stem_sha256))throw Error("Question IDs or source stems no longer match");
    rows=map.questions;
  }catch(err){panel.textContent="The exact question-to-lesson route cannot be verified right now. Use the Question Bank directly.";status.textContent="Learning route unavailable.";return;}
  const query=new URLSearchParams(location.search).get("question");
  selected=query && valid(query) && rows.some(x=>x.source_id===query)?query:null;
  const names={F01:"Applied power vs net power",F02:"Round-trip incline energy",F03:"Spring force switching",F04:"Two-body spring energy",F05:"Massive spring",F06:"Wind energy flow",F07:"Pendulum turning or holding",F08:"Shock absorber energy",C01:"Every force counts",C02:"Spring contact",C03:"Constant power",C04:"Distributed mass",C05:"Choose the graph operation",C06:"Vertical-circle contact",C07:"Conveyor momentum flow",C08:"Comparing spring controls",E01:"Potential wells",E02:"Instantaneous power",E03:"Spring to projectile",E04:"Repeated bouncing",E05:"Radial force and potential"};
  function fillChoices(){
    const term=search.value.trim().toLowerCase();
    const filtered=rows.filter(row=>(row.source_id+" "+row.student_goal+" "+(names[row.primary_lesson]||"")).toLowerCase().includes(term));
    picker.replaceChildren();
    const placeholder=add(picker,"option","Choose a Question Bank ID");placeholder.value="";
    if(!filtered.length){add(picker,"option","No matching source questions").value="";picker.disabled=true;selected=null;}
    else{
      picker.disabled=false;
      for(const row of filtered){
        const opt=add(picker,"option",row.source_id+" · "+row.student_goal.slice(0,52));opt.value=row.source_id;
      }
      if(!filtered.some(x=>x.source_id===selected))selected=null;
      picker.value=selected||"";
    }
    status.textContent=filtered.length+" of 74 source questions shown; "+map.counts.focused_new+" focused journeys, "+map.counts.targeted+" close practice matches, "+map.counts.related+" related-only bridges, "+map.counts.missing+" unmapped. Every question has a route; related-only routes are NOT complete teaching for the original question.";
    draw();
  }
  // Verified source inventory supplies the only allowed lesson mapping.
  // A browser URL is not an authority: reject cross-origin, foreign directories,
  // unexpected query keys, bad anchors, and wrong source/lesson combinations.
  const safeLessonURL=(href,source,lesson)=>{
    if(typeof href!=="string"||!valid(source)||typeof lesson!=="string")return null;
    const path=/^C0[1-8]$/.test(lesson)?"d3d4-self-tutor.html":
      /^E0[1-5]$/.test(lesson)?"extension-learning.html":
      /^F0[1-3]$/.test(lesson)?"focused-journeys.html":
      /^F0[4-8]$/.test(lesson)?"gap-journeys.html":null;
    if(!path)return null;
    // The selected row must be the verified source-bound primary route.
    if(!rows.some(row=>row.source_id===source&&row.primary_lesson===lesson&&
                      row.fit!=="MISSING_CONSTRUCTION"&&row.lesson_href===href))return null;
    try{
      const url=new URL(href,location.href),expected=new URL(path,location.href);
      const bridge=new URL("study-bridge.html",location.href);
      if(!["http:","https:"].includes(url.protocol)||url.username||url.password||
         url.origin!==expected.origin)return null;
      const isBridge=url.pathname===bridge.pathname;
      if(url.pathname!==(isBridge?bridge.pathname:expected.pathname))return null;
      if(url.searchParams.getAll("question").length!==1||
         url.searchParams.get("question")!==source)return null;
      const keys=Array.from(url.searchParams.keys());
      if(isBridge){
        if(url.hash||url.searchParams.getAll("lesson").length!==1||
           url.searchParams.get("lesson")!==lesson||
           keys.length!==2||!keys.every(k=>["question","lesson"].includes(k)))return null;
      }else if(url.hash!=="#"+lesson||keys.length!==1||keys[0]!=="question")return null;
      const target=new URL(path,location.href);
      target.searchParams.set("question",source);
      target.hash=lesson;
      return target.href;
    }catch(_){return null;}
  };
  function draw(){
    panel.replaceChildren();
    const row=rows.find(x=>x.source_id===selected);
    if(!row){
      add(panel,"h3","Choose an exact question, or explore a Physics skill below.");
      add(panel,"p","No question-to-lesson match is guessed. Unknown IDs never receive an invented route.");
      return;
    }
    const heading=add(panel,"h3",row.source_id+" · Your learning route");
    const description=add(panel,"p",row.student_goal,"student-goal");
    const summary=add(panel,"p",null,"fit-explanation");
    let fitText={
      FOCUSED_NEW:"Fully relevant focused teaching and a fresh challenge for the identified physical operation. This does not certify the original answer.",
      TARGETED_PRACTICE:"Close practice match: the same reasoning model is useful, but check the assumptions on your original problem.",
      RELATED_BRIDGE:"Related practice only: a helpful idea, but NOT the complete reasoning needed for your original question.",
      MISSING_CONSTRUCTION:"Missing teaching: the required reasoning construction is not yet available. No unrelated lesson is offered as a substitute."
    }[row.fit]||"Study status could not be determined.";
    summary.textContent=fitText;
    add(panel,"p","What the current teaching does NOT establish: "+row.teaching_limit,"teaching-limit");
    if(row.has_source_caution){
      const caution=add(panel,"p",row.source_science_note||"Some source physics, figures or answer-key claims are not independently resolved.","source-caution");
      caution.setAttribute("role","note");
    }
    const actions=add(panel,"nav",null,"question-actions");
    actions.setAttribute("aria-label","Question learning actions");
    const lessonHref=safeLessonURL(row.lesson_href,row.source_id,row.primary_lesson);
    if(lessonHref){
      const label=row.fit==="RELATED_BRIDGE"?"Practise a RELATED idea":row.fit==="FOCUSED_NEW"?"Start the new reasoning journey":"Learn the reasoning → Fresh challenge";
      const link=add(actions,"a",label+" · "+row.primary_lesson+" ("+(names[row.primary_lesson]||"practice")+")","primary-link");
      link.href=lessonHref;
    }else{
      add(actions,"span","No dedicated student lesson available for this operation yet.","no-lesson");
    }
    const original=add(actions,"a","Return to original "+row.source_id+" (attempt first)","source-link");
    original.href="../../preview/question-status.html?question="+encodeURIComponent(row.source_id);
    const support=add(panel,"details",null,"related-support");
    add(support,"summary","What else can I practise?");
    add(support,"p","These are additional existing ideas, not automatic replacements for the original question.");
    const list=add(support,"div",null,"related-links");
    for(const l of row.related_lessons){
      if(l===row.primary_lesson||!names[l])continue;
      const sourceKnown=map.questions.some(x=>x.source_id===row.source_id&&x.related_lessons.includes(l));
      if(!sourceKnown)continue;
      // The older lesson validates its own author-proposed source associations.
      const a=add(list,"a",l+" · "+names[l]);a.href="reasoning-paths.html?question="+encodeURIComponent(row.source_id)+"#WPE-"+l;
    }
    const all=add(support,"a","See the complete 74-question learning coverage");
    all.href="question-coverage.html?question="+encodeURIComponent(row.source_id);
    if(row.fit==="MISSING_CONSTRUCTION"){
      const p=add(support,"p","You can still practise the five foundational WPE mini-lessons below, but they are not a substitute for this missing reasoning construction.");
      const a=add(support,"a","Review the foundational Work → Energy path");a.href="#work-sign";
    }
    if(location.search!==""&&new URLSearchParams(location.search).get("question")===row.source_id)heading.setAttribute("data-exact-source","true");
  }
  search.addEventListener("input",fillChoices);
  picker.addEventListener("change",()=>{
    selected=picker.value;
    const url=new URL(location.href);
    if(selected)url.searchParams.set("question",selected);
    url.hash="question-routes";
    history.replaceState(null,"",url.pathname+url.search+url.hash);
    draw();
  });
  fillChoices();
  const resume=$("#journey-resume"),notice=$("#journey-notice");
  function refreshManager(){
    let entry=null;
    try{entry=JSON.parse(localStorage.getItem("g9:wpe:journey:v1")||"null")}catch(_){}
    const allowed={"d3d4-self-tutor.html":/^C0[1-8]$/,"extension-learning.html":/^E0[1-5]$/,"focused-journeys.html":/^F0[1-3]$/,"gap-journeys.html":/^F0[4-8]$/};
    if(entry&&typeof entry.path==="string"&&allowed[entry.path]?.test(entry.lesson||"")&&(!entry.question||rows.some(x=>x.source_id===entry.question&&x.primary_lesson===entry.lesson))&&(!entry.variant||["first","transfer"].includes(entry.variant))){
      const url=new URL(entry.path,location.href);
      if(entry.question)url.searchParams.set("question",entry.question);
      if(entry.variant==="transfer"&&entry.path==="focused-journeys.html")url.searchParams.set("variant","transfer");
      url.hash=entry.lesson;
      resume.href=url.href;resume.textContent="Resume · "+entry.lesson+(entry.variant==="transfer"?" · another challenge":"")+(entry.question?" · from "+entry.question:"");resume.removeAttribute("aria-disabled");
    }else{resume.href="#skill-explorer";resume.textContent="Explore a skill · no saved journey yet";resume.setAttribute("aria-disabled","true");}
  }
  $("#journey-start").addEventListener("click",()=>{
    try{localStorage.removeItem("g9:wpe:journey:v1")}catch(_){}
    refreshManager();notice.textContent="Choose a new route. Your earlier first attempts remain saved.";location.hash="skill-explorer";
  });
  $("#journey-clear").addEventListener("click",()=>{
    if(!confirm("Clear all WPE lesson practice saved in this browser? Original Question Bank attempts will be kept."))return;
    try{
      const prefixes=["g9:wpe:journey:v1","g9:wpe:learn-challenge:v2:","g9:wpe:d3d4:self-tutor:v1:","g9:wpe:extensions:v1:","g9:wpe:focused:v1:","g9:wpe:gaps:v2:"];
      for(let i=localStorage.length-1;i>=0;i--){const key=localStorage.key(i);if(prefixes.some(p=>key.startsWith(p)))localStorage.removeItem(key);}
    }catch(_){notice.textContent="Local storage is unavailable: saved practice could not be fully cleared.";return;}
    refreshManager();notice.textContent="Saved lesson practice cleared; original Question Bank answers remain untouched.";
  });
  window.addEventListener("pageshow",refreshManager);
  refreshManager();
})();
