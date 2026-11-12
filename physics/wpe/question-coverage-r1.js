/* 74-question source-to-reasoning coverage; preserve source and academic-status custody. */
(async()=>{
  "use strict";
  const tbody=document.getElementById("rows"),summary=document.getElementById("counts"),
        status=document.getElementById("table-status"),search=document.getElementById("search"),
        filter=document.getElementById("filter");
  const cell=(row,label,value)=>{
    const item=document.createElement("td");item.dataset.label=label;
    if(typeof value==="string")item.textContent=value;
    else if(value)item.append(value);
    row.append(item);return item;
  };
  const link=(href,caption)=>{const a=document.createElement("a");a.href=href;a.textContent=caption;return a;};
  let bank,coverage;
  try{
    const [b,r]=await Promise.all([
      fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"),
      fetch("learning-coverage-r1.json")
    ]);
    if(!b.ok||!r.ok)throw Error("Source records unavailable");
    bank=await b.json();coverage=await r.json();
    if(bank.questions?.length!==74||coverage.schema!=="wpe-learner-coverage-r1/v1"||coverage.questions?.length!==74)
      throw Error("Question inventory changed");
    const bySource=new Map(bank.questions.map(q=>[q.source_id,q]));
    if(bySource.size!==74||coverage.questions.some(x=>bySource.get(x.source_id)?.stem_sha256!==x.stem_sha256))
      throw Error("Original question identity changed");
  }catch(error){summary.textContent="Question map unavailable: "+error.message;return;}
  const bySource=new Map(bank.questions.map(q=>[q.source_id,q]));
  const categories={FOCUSED_NEW:"focused",TARGETED_PRACTICE:"targeted",RELATED_BRIDGE:"related",MISSING_CONSTRUCTION:"missing"};
  const counts=coverage.counts;
  summary.textContent=coverage.questions.length+" questions · "+counts.focused_new+" new focused journeys · "+counts.targeted+" close-practice matches · "+counts.related+" related-only bridges · "+counts.missing+" missing constructions.";
  const requested=new URLSearchParams(location.search).get("question");
  if(requested&&coverage.questions.some(q=>q.source_id===requested))search.value=requested;
  function draw(){
    const keyword=search.value.trim().toLowerCase(),f=filter.value;
    tbody.replaceChildren();let count=0;
    for(const e of coverage.questions){
      const q=bySource.get(e.source_id),fit=categories[e.fit];
      if(f!=="all"&&f!==fit)continue;
      if(keyword&&!((q.source_id+" "+e.student_goal+" "+e.primary_lesson+" "+e.teaching_limit).toLowerCase().includes(keyword)))continue;
      count++;const row=document.createElement("tr");
      cell(row,"Question",link("../../preview/question-status.html?question="+encodeURIComponent(q.source_id),q.source_id));
      cell(row,"Essential reasoning",e.student_goal);
      const options=document.createElement("div");options.className="topic-links";
      if(e.lesson_href){
        const label=e.fit==="RELATED_BRIDGE"?"Related practice, NOT sufficient":e.fit==="FOCUSED_NEW"?"New six-stage focused challenge":"Learn + fresh challenge";
        options.append(link(e.lesson_href,e.primary_lesson+" · "+label));
      }else options.textContent="No adequate construction; gap identified";
      cell(row,"Learn → Challenge",options);
      const gap=cell(row,"Teaching limit",e.teaching_limit);
      gap.className=e.fit==="MISSING_CONSTRUCTION"?"missing":"skill";
      tbody.append(row);
    }
    status.textContent=count+" of 74 questions shown.";
  }
  search.addEventListener("input",draw);
  filter.addEventListener("change",draw);
  draw();
})();
