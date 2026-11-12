/* Agent A: NSEJS Core2 candidate reader. No Core1A/Core1B authorship or academic admissions. */
(function () {
  "use strict";
  const TOPICS = [
    ["optics","OPTICS","Optics"],
    ["electrostatics","ELECTROSTATICS","Electrostatics"],
    ["circuits","CURRENT_ELECTRICITY","Circuits"],
    ["magnetism","MAGNETISM_AND_EMI","Magnetism & EMI"],
    ["mechanics","MECHANICS","Mechanics"],
    ["fluids","FLUIDS_AND_SOUND","Fluids & Sound"]
  ];
  const status = document.getElementById("status");
  const target = document.getElementById("questions");
  const nav = document.getElementById("topicNav");
  const query = new URLSearchParams(location.search);
  const selectedTopic = TOPICS.some(t => t[0] === query.get("topic")) ? query.get("topic") : "optics";
  const text = (tag, content, className) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    node.textContent = content;
    return node;
  };
  const append = (parent, ...children) => { children.forEach(child => parent.appendChild(child)); return parent; };
  const uidOf = q => "g9:PHYSICS:" + q.source_id;
  const revisionPayload = q => JSON.stringify({
    uid:uidOf(q),source_id:q.source_id,original_id:q.id,
    stem:q.stem,options:q.options,answer:q.answer,question_type:q.question_type,
    figures:q.source_figures || [],figure_note:q.figure_note || "",
    reasoning:q.steps || [],boundary:q.check || ""
  });
  async function revision(q) {
    if (!crypto || !crypto.subtle) throw new Error("SHA-256 revision service unavailable; attempt commitment disabled");
    const bytes = new TextEncoder().encode(revisionPayload(q));
    const hash = await crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(hash), b => b.toString(16).padStart(2,"0")).join("");
  }
  function textOption(opt, i) {
    const match = String(opt).match(/^[A-H]\s*[:.)]\s*/);
    return {id:match ? match[0].trim().charAt(0) : String.fromCharCode(65+i),label:String(opt)};
  }
  function attemptKey(q,rev) {
    return ["g9","nsejs","core2","candidate-attempt","v1",encodeURIComponent(uidOf(q)),rev].join(":");
  }
  function getAttempt(key) {
    try {
      const data=JSON.parse(localStorage.getItem(key) || "null");
      return data && data.content_revision === key.split(":").pop() && data.question_uid ? data : null;
    } catch (_) { return null; }
  }
  function saveAttempt(key,data) {
    try {
      localStorage.setItem(key,JSON.stringify(data));
      const reread=JSON.parse(localStorage.getItem(key) || "null");
      return !!reread && reread.question_uid === data.question_uid && reread.content_revision === data.content_revision;
    } catch (_) { return false; }
  }
  function renderMath(el) {
    if (window.MathJax && typeof window.MathJax.typesetPromise === "function") {
      window.MathJax.typesetPromise([el]).catch(function () { /* text remains visible */ });
    }
  }
  async function createCard(q,index) {
    const box=text("article","", "card"); box.id = "question-"+encodeURIComponent(q.source_id);
    append(box,text("h2","Candidate "+(index+1)+" · "+q.source_id));
    append(box,text("div","Original displayed ID: "+q.id+" · QRT nomination: "+q.op+" / "+q.band+" · NOT_ADMITTED","meta"));
    append(box,text("span","{Unvalidated} · source/key/figures not authenticated","status"));
    const stem=text("p",String(q.stem||"").replace(/\[FIG[^\]]*\]/g,"[Figure required — not available]"),"stem");
    append(box,stem);
    const requiredFigure=Array.isArray(q.source_figures) && q.source_figures.length>0;
    if (requiredFigure) {
      append(box,text("p","Required source figure not supplied in this public candidate page: "+q.source_figures.join(", ")+". Question remains source-fidelity HOLD; commitment disabled.","figure-warning"));
    }
    const group=text("div","","options");
    const chosen=[];
    const controls=[];
    const isMulti=q.question_type === "multiple_correct_mcq";
    (q.options||[]).forEach((o,i)=>{
      const parsed=textOption(o,i);
      const label=document.createElement("label");
      const field=document.createElement("input");
      field.type=isMulti?"checkbox":"radio";
      field.name=uidOf(q);field.value=parsed.id;
      field.disabled=requiredFigure;
      controls.push(field);
      append(label,field,text("span",parsed.label));
      append(group,label);
    });
    append(box,group);
    const action=text("div","","actions");
    const commit=text("button","Save first attempt");commit.type="button";commit.disabled=requiredFigure;
    const reveal=text("button","Show explanation");reveal.type="button";reveal.disabled=true;
    const feedback=text("span","","meta");feedback.setAttribute("role","status");
    append(action,commit,reveal,feedback);append(box,action);
    const answerBox=text("div","","answer");answerBox.hidden=true;
    append(box,answerBox);
    let rev;
    try { rev=await revision(q); } catch(e) { commit.disabled=true;feedback.textContent=e.message;return box; }
    box.dataset.questionUid=uidOf(q);
    box.dataset.contentRevision=rev;
    const key=attemptKey(q,rev);
    let committed=getAttempt(key);
    function setCommitted(saved,labels) {
      controls.forEach(f=>{f.disabled=true;if(labels && labels.includes(f.value)) f.checked=true;});
      commit.disabled=true;reveal.disabled=false;
      feedback.className=saved?"ok":"error";
      feedback.textContent=saved?"First attempt saved locally; not certified.":"Attempt committed in this tab but NOT SAVED. Not an unassisted evidence record.";
    }
    if(committed && committed.question_uid===uidOf(q)) setCommitted(true,committed.selected_option_ids||[]);
    commit.addEventListener("click",function(){
      if(committed) return;
      const selection=controls.filter(f=>f.checked).map(f=>f.value);
      if(selection.length===0){feedback.textContent="Select an answer before committing.";return;}
      const attempt={question_uid:uidOf(q),original_id:q.id,source_id:q.source_id,content_revision:rev,
        selected_option_ids:selection,assistance_events:[],first_answer_at:new Date().toISOString(),
        evidence_class:"UNVERIFIED_BROWSER_RECORD",mode:"LOCAL_INDEPENDENT_PRACTICE"};
      const saved=saveAttempt(key,attempt);
      committed=attempt;setCommitted(saved,selection);
    });
    reveal.addEventListener("click",function(){
      if(!committed)return;
      answerBox.textContent=String(q.answer||"")+"\n\n"+(q.steps||[]).join("\n")+"\n\n"+String(q.check||"");
      answerBox.hidden=false;
      reveal.disabled=true;
      reveal.textContent="Explanation revealed";
      renderMath(answerBox);
    });
    return box;
  }
  async function load() {
    const topic=TOPICS.find(t=>t[0]===selectedTopic);
    TOPICS.forEach(t=>{
      const a=document.createElement("a");
      a.href="question-bank.html?topic="+encodeURIComponent(t[0]);
      a.textContent=t[2];
      a.style.cssText="display:inline-block;padding:10px;border:1px solid #8caeba;border-radius:7px;background:"+(t[0]===selectedTopic?"#d5eff0":"white");
      if(t[0]===selectedTopic)a.setAttribute("aria-current","page");
      nav.append(a);
    });
    const response=await fetch("../../preview/question-status.html",{cache:"no-store"});
    if(!response.ok)throw new Error("Candidate data unavailable (HTTP "+response.status+")");
    const html=await response.text();
    const doc=new DOMParser().parseFromString(html,"text/html");
    const data=doc.querySelector('script#wpe-data[type="application/json"]');
    if(!data)throw new Error("Legacy public candidate source has no wpe-data payload");
    const all=JSON.parse(data.textContent).questions;
    if(!Array.isArray(all))throw new Error("Invalid candidate question payload");
    const physics=all.filter(q=>TOPICS.slice(0,5).some(t=>t[1]===q.topic));
    const identities=physics.map(uidOf);
    if(physics.length!==50 || new Set(identities).size!==50)throw new Error("Physics census/identity mismatch; fail closed");
    const questions=physics.filter(q=>q.topic===topic[1]);
    status.textContent=topic[2]+": "+questions.length+" candidate records · source and QRT admission HOLD.";
    if(questions.length===0){target.append(text("p","No source-backed candidate question bank is available for this topic. Do not infer coverage."));return;}
    const requestedUid=query.get("uid");
    const shown=requestedUid ? questions.filter(q=>uidOf(q)===requestedUid) : questions;
    if(!shown.length){target.append(text("p","Requested question UID not found in this topic.","error"));return;}
    for(let i=0;i<shown.length;i++){const card=await createCard(shown[i],i);target.append(card);renderMath(card);}
  }
  load().catch(function(e){status.textContent="Core2 bank unavailable: "+e.message;status.className="error";});
})();