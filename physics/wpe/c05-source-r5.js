/* R5 candidate return. No original Question Bank/gateway edit.
 * Compare source ID, exact 74-bank stem, C05 owner, unchanged academic status.
 */
(()=>{
"use strict";
const mapping={"EX-M11":"G5U","EX-M61":"G5E","EX-M69":"G5P","EX-M85":"G5V","AN-2":"G5W","AN-6":"G5C","JEE-2026-04-06-S2-Q29":"G5X"};
const box=document.getElementById("candidate-source");
const title=document.getElementById("candidate-source-title");
const message=document.getElementById("candidate-source-message");
const link=document.getElementById("candidate-source-return");
async function bind(){
 const source=new URLSearchParams(location.search).get("source");
 link.hidden=true;
 if(!source){box.hidden=true;return;}
 box.hidden=false;title.textContent="Checking original Question Bank evidence";
 message.textContent="Comparing source ID, lesson signature, source stem hash and original related-only status…";
 if(!Object.hasOwn(mapping,source)){
  message.textContent="Unknown or unqualified graph source. No original-question return link is inferred.";
  return;
 }
 const expected=mapping[source],chosen=location.hash.slice(1).toUpperCase();
 if(expected!==chosen){message.textContent="The selected operation does not belong to "+source+"; choose its matching graph lesson.";return;}
 try{
  const [c,b]=await Promise.all([
   fetch("learning-coverage-r1.json",{cache:"no-store"}),
   fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json",{cache:"no-store"})
  ]);
  if(!c.ok||!b.ok)throw Error("bank not available");
  const [coverage,bank]=await Promise.all([c.json(),b.json()]);
  if(coverage.schema!=="wpe-learner-coverage-r1/v1"||coverage.questions?.length!==74||bank.questions?.length!==74)throw Error("source inventory changed");
  const row=coverage.questions.find(x=>x.source_id===source);
  const original=bank.questions.find(x=>x.source_id===source);
  if(!row||!original||row.stem_sha256!==original.stem_sha256||
     row.primary_lesson!=="C05"||row.fit!=="RELATED_BRIDGE"||
     row.academic_status!=="PRACTICE_ONLY_NOT_ADMITTED"||
     original.review_state!=="NOT_ADMITTED")throw Error("candidate source state changed");
  title.textContent="Verified original source "+source+" · candidate learning only";
  message.textContent="This source remains RELATED_BRIDGE and NOT academically admitted. The lesson solves DIFFERENT invented examples and does not authenticate the original graph or coaching key.";
  link.href="../../preview/question-status.html?question="+encodeURIComponent(source);
  link.textContent="Return to the exact original "+source+" without opening the answer";
  link.hidden=false;
 }catch(_){
  message.textContent="The source cannot be verified against the unchanged bank. No return link is invented.";
  link.hidden=true;
 }
}
window.addEventListener("hashchange",bind);
bind();
})();
