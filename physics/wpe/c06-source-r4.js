/* R4 source-candidate return is separate from the merged Question Bank router.
 * The original source remains RELATED_BRIDGE; this checks exact ID, stem digest,
 * immutable selected bank, and candidate signature before giving a return link.
 * It does NOT claim the teaching has been academically admitted.
 */
(() => {
"use strict";
const mapping={"EX-M18":"C6S","EX-M39":"C6A","EX-N31":"C6H","EX-M36":"C6T","EX-N11":"C6W"};
const box=document.getElementById("candidate-source");
const title=document.getElementById("candidate-source-title");
const message=document.getElementById("candidate-source-message");
const link=document.getElementById("candidate-source-return");
async function bind(){
  const id=new URLSearchParams(location.search).get("source");
  link.hidden=true;
  if(!id){box.hidden=true;return;}
  box.hidden=false;title.textContent="Source identity check";
  message.textContent="Checking the exact original source against the unchanged 74-question bank…";
  if(!/^(?:EX-M18|EX-M39|EX-N31|EX-M36|EX-N11)$/.test(id)){
    message.textContent="This source has no qualified candidate in the C06 construction family. No return is inferred.";
    return;
  }
  const signature=mapping[id],selected=location.hash.slice(1).toUpperCase();
  if(signature!==selected){message.textContent="The selected construction does not belong to "+id+". Choose its matching source lesson first.";return;}
  try{
    const [mapRes,bankRes]=await Promise.all([
      fetch("learning-coverage-r1.json",{cache:"no-store"}),
      fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json",{cache:"no-store"})
    ]);
    if(!mapRes.ok||!bankRes.ok)throw Error("Source data unavailable");
    const [map,bank]=await Promise.all([mapRes.json(),bankRes.json()]);
    if(map.schema!=="wpe-learner-coverage-r1/v1"||map.questions?.length!==74||bank.questions?.length!==74)throw Error("Source inventory changed");
    const original=bank.questions.find(x=>x.source_id===id);
    const route=map.questions.find(x=>x.source_id===id);
    if(!original||!route||!route.stem_sha256||
        original.stem_sha256!==route.stem_sha256||
        route.primary_lesson!=="C06"||route.fit!=="RELATED_BRIDGE"||route.academic_status!=="PRACTICE_ONLY_NOT_ADMITTED")
      throw Error("Source is not in its unchanged candidate state");
    title.textContent="Verified source "+id+" · candidate teaching only";
    message.textContent="This question remains RELATED practice, not academically admitted full coverage. The examples here are NEW; no original coaching answer is endorsed or automatically displayed.";
    link.href="../../preview/question-status.html?question="+encodeURIComponent(id);
    link.textContent="Return to the exact original "+id+" without opening its answer";
    link.hidden=false;
  }catch(_){message.textContent="Source/lesson identity cannot be verified; no source return link has been invented.";link.hidden=true;}
}
window.addEventListener("hashchange",bind);
bind();
})();
