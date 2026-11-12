/* One set of learner-facing role controls; every lesson still runs in its original page.
 * Journey pointer is a local resume convenience, not an assessment record.
 */
(()=>{
 "use strict";
 const path=location.pathname.split("/").pop();
 const info={
  "d3d4-self-tutor.html":{re:/^C0[1-8]$/,guide:".guide-panel",challenge:".challenge-panel, .challenge, [data-stage-root]"},
  "extension-learning.html":{re:/^E0[1-5]$/,guide:".guide",challenge:".challenge"},
  "focused-journeys.html":{re:/^F0[1-3]$/,guide:".guide",challenge:".challenge"}
 }[path];
 if(!info)return;
 const pointerKey="g9:wpe:journey:v1";
 const source=new URLSearchParams(location.search).get("question");
 const variant=path==="focused-journeys.html"&&new URLSearchParams(location.search).get("variant")==="transfer"?"transfer":"first";
 const chooseLesson=()=>{const id=location.hash.slice(1).toUpperCase();return info.re.test(id)?id:null;};
 const section=()=>{
   const lesson=chooseLesson();
   if(!lesson)return null;
   if(path==="d3d4-self-tutor.html")return document.getElementById(lesson);
   return document.querySelector("#journey-root .lesson, #lesson-surface .lesson")||document.getElementById(lesson);
 };
 const element=(tag,label,cls)=>{const e=document.createElement(tag);if(label!=null)e.textContent=label;if(cls)e.className=cls;return e;};
 async function verifiedSource(lesson){
   if(!source||!/^[A-Za-z0-9-]{2,64}$/.test(source))return false;
   try{
     const [m,b]=await Promise.all([fetch("learning-coverage-r1.json"),fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json")]);
     if(!m.ok||!b.ok)return false;
     const coverage=await m.json(),bank=await b.json();
     if(coverage.schema!=="wpe-learner-coverage-r1/v1"||coverage.questions?.length!==74||bank.questions?.length!==74)return false;
     const row=coverage.questions.find(r=>r.source_id===source);
     return !!(row&&row.primary_lesson===lesson&&row.fit!=="MISSING_CONSTRUCTION"&&
       bank.questions.some(q=>q.source_id===source&&q.stem_sha256===row.stem_sha256));
   }catch(_){return false;}
 }
 let cycle=0;
 async function update(){
   const seq=++cycle,lesson=chooseLesson();
   if(!lesson)return;
   const valid=await verifiedSource(lesson);
   if(seq!==cycle)return;
   const place=section();if(!place)return;
   let bar=place.querySelector(".lesson-roles");
   if(!bar){bar=element("nav",null,"lesson-roles");bar.setAttribute("aria-label","Learn, challenge and return");place.insertBefore(bar,place.firstChild);}
   bar.replaceChildren();
   const guide=element("button","Learn the idea");guide.type="button";
   const challenge=element("button",variant==="transfer"?"Try another challenge":"Try it yourself");challenge.type="button";
   bar.append(guide,challenge);
   const scrollTo=sel=>{const root=place.querySelector(sel);root?.scrollIntoView({behavior:"smooth",block:"start"});root?.querySelector("button, textarea, input, select")?.focus({preventScroll:true});};
   guide.addEventListener("click",()=>scrollTo(info.guide));
   challenge.addEventListener("click",()=>scrollTo(info.challenge));
   if(valid){
     const a=element("a","Return to my question · "+source,"source-return-inline");
     a.href="../../preview/question-status.html?question="+encodeURIComponent(source);
     bar.append(a);
   }
   const notice=element("span","The teaching and challenge share this lesson. Browser progress is local and not secure or independently graded.","role-status");bar.append(notice);
   const pointer={schema:1,path,lesson,variant,question:valid?source:null};
   try{localStorage.setItem(pointerKey,JSON.stringify(pointer));}catch(_){notice.textContent+=" Local saving is unavailable.";}
 }
 window.addEventListener("hashchange",update);
 window.addEventListener("pageshow",update);
 update();
})();
