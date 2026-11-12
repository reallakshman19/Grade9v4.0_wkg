/* Source-linked Chemistry/Biology NSEJS paper practice. No question text or
 * answer key is imported. 2024 code-51 range and dropped Q20 are from the
 * independently-held local locator registry. All attempts UNVERIFIED.
 */
(() => {
  "use strict";
  const subject=document.body.dataset.paperSubject;
  const subjects=["CHEMISTRY","BIOLOGY"];
  const root=document.getElementById("source-index");
  const control=document.getElementById("paper-practice-form");
  const outcome=document.getElementById("attempt-status");
  const selectYear=document.getElementById("source-year");
  const qNumber=document.getElementById("source-question-number");
  const choices=document.getElementById("practice-choices");
  const commit=document.getElementById("save-first-response");
  const paperLink=document.getElementById("active-paper-link");
  const keyLink=document.getElementById("publisher-key-link");
  let index=null, revision=null, item=null, key=null;
  const allowed=new Set(["A","B","C","D"]);
  const words=(tag,value,cls)=>{
    const n=document.createElement(tag);
    n.textContent=value;
    if(cls)n.className=cls;
    return n;
  };
  const fail=code=>{
    outcome.textContent="HOLD · "+code+". No attempt accepted, verified answer, or academic score.";
    outcome.dataset.status="HOLD";
    commit.disabled=true;
  };
  const trustedUrl=value=>{
    try {
      const u=new URL(value);
      return u.protocol==="https:"&&["iapt.org.in","www.iapt.org.in","mail.iapt.org.in"].includes(u.hostname)&&
             !u.username&&!u.password&&!u.port&&!u.search&&!u.hash;
    } catch {return false;}
  };
  const hash=async value=>{
    if(!crypto?.subtle)throw Error("SHA256_UNAVAILABLE");
    const h=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(value));
    return Array.from(new Uint8Array(h),b=>b.toString(16).padStart(2,"0")).join("");
  };
  function currentMeta() {
    if(!item||item.year!==2024||item.paper_code!==51||
       item.attempt_eligibility!=="UNVERIFIED_LOCAL_NOTES_ONLY_CODE51"||
       item.source_authentication!=="HOLD"||item.academic_admission!=="HOLD"||
       item.question_text_present!==false||item.official_answer_values_present!==false||
       JSON.stringify(item.supported_question_range)!=="[1,60]"||
       JSON.stringify(item.multi_answer_range)!=="[49,60]"||
       JSON.stringify(item.dropped_question_numbers)!=="[20]") return null;
    const q=Number(qNumber.value);
    if(!Number.isInteger(q)||q<1||q>60||String(q)!==qNumber.value.trim()||q===20)return null;
    return {q,isMulti:q>=49};
  }
  function storageKey(q) {
    return ["g9","nsejs","iapt-link-note","v1",revision,subject,
      "2024","CODE51","Q"+String(q).padStart(2,"0")].join(":");
  }
  function read(keyValue) {
    try {
      const raw=localStorage.getItem(keyValue);
      if(!raw)return null;
      const data=JSON.parse(raw);
      return (data&&data.key===keyValue&&data.subject===subject&&data.year===2024&&
        data.paper_code===51&&Array.isArray(data.options)&&data.options.length>0&&
        data.options.every(x=>allowed.has(x))&&data.source_revision===revision)?
        data:null;
    }catch {return null;}
  }
  function save(keyValue,record) {
    try {
      const prior=localStorage.getItem(keyValue);
      if(prior!==null)return false; // preserve first-attempt-only contract.
      const bytes=JSON.stringify(record);
      localStorage.setItem(keyValue,bytes);
      return localStorage.getItem(keyValue)===bytes;
    }catch{return false;}
  }
  function setLink(target,url) {
    if(!trustedUrl(url))throw Error("UNTRUSTED_OFFICIAL_LINK");
    target.href=url;
    target.target="_blank";
    target.rel="noopener noreferrer";
  }
  function selected(){
    return Array.from(choices.querySelectorAll("input:checked")).map(n=>n.value);
  }
  function presentSaved(record) {
    commit.disabled=true;
    for(const f of choices.querySelectorAll("input")){
      f.disabled=true;
      f.checked=record.options.includes(f.value);
    }
    outcome.dataset.status="SAVED_UNVERIFIED";
    outcome.textContent="First local response stored for "+subject+
      " · IAPT 2024 Code 51 Q"+record.question+". No actual question was imported; "+
      "no answer comparison, correctness or official mark is claimed.";
    keyLink.hidden=false;
    setLink(keyLink,item.key_url);
  }
  function update() {
    choices.replaceChildren();
    keyLink.hidden=true;
    commit.disabled=true;
    outcome.dataset.status="HOLD";
    const year=Number(selectYear.value);
    item=index?.years.find(x=>x.year===year)||null;
    if(!item||item.attempt_eligibility!=="UNVERIFIED_LOCAL_NOTES_ONLY_CODE51") {
      paperLink.hidden=!item;
      if(item){setLink(paperLink,item.paper_url);}
      outcome.textContent="HOLD · Paper and source links only; code/language and question ranges "+
        "are not authenticated for this year. No local question-attempt identity may be inferred.";
      return;
    }
    paperLink.hidden=false;
    setLink(paperLink,item.paper_url);
    const meta=currentMeta();
    if(!meta){
      outcome.textContent=qNumber.value.trim()==="20"?
        "2024 Code 51 Q20 was DROPPED by the publisher; no answer or score accepted.":
        "Choose an integer paper question number 1–60 (Q20 dropped). "+
        "Questions 49–60 permit multiple options. The paper stays on IAPT; all source claims HOLD.";
      return;
    }
    key=storageKey(meta.q);
    const fieldset=words("fieldset","");
    const legend=words("legend",meta.isMulti?
      "Select all your first-response options (A2 multiple-choice; unverified)":
      "Select one first-response option (A1; unverified)");
    fieldset.append(legend);
    for(const letter of allowed){
      const label=words("label","");
      const input=document.createElement("input");
      input.type=meta.isMulti?"checkbox":"radio";
      input.name="practice-answer";
      input.value=letter;
      label.append(input,words("span",letter));
      fieldset.append(label);
    }
    choices.append(fieldset);
    if(meta.q===20){fail("Q20_DROPPED");return;}
    const previous=read(key);
    if(previous){presentSaved(previous);return;}
    commit.disabled=false;
    outcome.dataset.status="PENDING";
    outcome.textContent="No first attempt saved. Choose option(s) using the original IAPT paper, "+
      "then save locally. Questions, figures and official correct answers are not imported.";
  }
  async function init() {
    if(!subjects.includes(subject)||!root||!control||!outcome||
       !selectYear||!qNumber||!choices||!commit||!paperLink||!keyLink)
      throw Error("UNRECOGNIZED_SUBJECT_OR_MOUNT");
    const response=await fetch("../data/source-linked-practice.v1.json",{cache:"no-store"});
    if(!response.ok)throw Error("PUBLIC_SOURCE_INDEX_MISSING");
    const raw=await response.text();
    const data=JSON.parse(raw);
    if(data.schema!=="grade9-nsejs-source-linked-practice/v1"||
       data.academic_admission!=="HOLD"||data.redistribution_rights!=="HOLD"||
       data.student_claim!=="UNVERIFIED_LOCAL_PAPER_NOTES_NOT_AN_EXAM_SCORE"||
       data.source_authority!=="IAPT_OFFICIAL_PAPER_LINK_ONLY_CONTENT_UNVERIFIED"||
       data.question_count_claimed!==0||data.actual_question_bodies!==0||
       !Array.isArray(data.years)||data.years.length!==5||
       !Array.isArray(data.subjects)||data.subjects.length!==2||
       !data.subjects.includes(subject)||
       new Set(data.years.map(x=>x.year)).size!==5)
      throw Error("SOURCE_PRACTICE_AUTHORITY_GATE_FAILED");
    if(!data.years.every(r=>r.source_origin===data.source_authority&&
       r.source_authentication==="HOLD"&&r.academic_admission==="HOLD"&&
       r.question_text_present===false&&r.official_answer_values_present===false&&
       trustedUrl(r.paper_url)&&trustedUrl(r.archive_url)&&trustedUrl(r.key_url)))
      throw Error("UNTRUSTED_OR_PROMOTED_OFFICIAL_LINK");
    revision=await hash(raw);
    index=data;
    root.replaceChildren();
    selectYear.replaceChildren();
    for(const year of data.years){
      const section=words("article","","paper-source-card");
      section.append(words("h2",year.year+" · "+year.exam_series));
      section.append(words("p","Linked IAPT paper only · source/authenticity HOLD. "+
        (year.year===2024?"Code 51 question labels 1–60; Q20 dropped; Q49–60 multiple-answer.":
          "Question-count, code and language scope not yet authenticated.")));
      const paper=words("a","Open paper at IAPT (external)");
      setLink(paper,year.paper_url);
      section.append(paper);
      root.append(section);
      const opt=document.createElement("option");
      opt.value=String(year.year);
      opt.textContent=String(year.year)+" · "+year.exam_series+
        (year.year===2024?" · manual unverified notes":" · links only");
      selectYear.append(opt);
    }
    selectYear.value="2024";
    selectYear.addEventListener("change",()=>{
      qNumber.value="";update();
    });
    qNumber.addEventListener("input",update);
    commit.addEventListener("click",()=>{
      const meta=currentMeta();
      if(!meta){fail("INVALID_YEAR_QUESTION_OR_DROPPED_ITEM");return;}
      const options=selected().sort();
      if(options.length===0){outcome.textContent="Choose an option before saving.";return;}
      if(!meta.isMulti&&options.length!==1){fail("A1_REQUIRES_ONE_OPTION");return;}
      const record={key:storageKey(meta.q),subject,year:2024,paper_code:51,
        question:meta.q,options,source_revision:revision,
        first_response_at:new Date().toISOString(),
        status:"UNVERIFIED_LOCAL_FIRST_ATTEMPT_NO_QUESTION_CONTENT",
        evidence_class:"BROWSER_UNVERIFIED"};
      if(!save(record.key,record)){
        fail("BROWSER_STORAGE_UNAVAILABLE_OR_FIRST_RESPONSE_EXISTS");
        return;
      }
      presentSaved(record);
    });
    const query=new URLSearchParams(location.search);
    if(query.has("year")&&query.has("question")){
      selectYear.value=query.get("year");
      qNumber.value=query.get("question");
    }
    update();
    control.hidden=false;
  }
  init().catch(error=>fail(error.message||"SOURCE_PRACTICE_START_FAILED"));
})();