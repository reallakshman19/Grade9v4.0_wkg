/* WPE skill selector: roving tab stop, arrow-key navigation, and deep links.
 * Tabs change presentation only; existing lesson URLs and attempt state are untouched.
 */
(() => {
  "use strict";
  const tablist=document.querySelector(".skill-tabs[role='tablist']");
  if(!tablist)return;
  const tabs=Array.from(tablist.querySelectorAll("[role='tab']"));
  if(tabs.length!==4)return;
  const panels=tabs.map(tab=>document.getElementById(tab.getAttribute("aria-controls")));
  if(panels.some(panel=>!panel))return;

  function activate(index,focus=false){
    tabs.forEach((tab,i)=>{
      const active=i===index;
      tab.setAttribute("aria-selected",String(active));
      tab.tabIndex=active?0:-1;
      panels[i].hidden=!active;
    });
    if(focus)tabs[index].focus();
  }
  function tabForHash(){
    const id=decodeURIComponent(window.location.hash.slice(1));
    const index=panels.findIndex(panel=>panel.id===id);
    if(index!==-1)return index;
    return tabs.findIndex(tab=>tab.id===id);
  }
  tabs.forEach((tab,index)=>{
    tab.addEventListener("click",()=>activate(index));
    tab.addEventListener("keydown",event=>{
      let next;
      if(event.key==="ArrowRight")next=(index+1)%tabs.length;
      else if(event.key==="ArrowLeft")next=(index+tabs.length-1)%tabs.length;
      else if(event.key==="Home")next=0;
      else if(event.key==="End")next=tabs.length-1;
      else return;
      event.preventDefault();
      activate(next,true);
    });
  });
  activate(Math.max(0,tabForHash()));
  window.addEventListener("hashchange",()=>{
    const index=tabForHash();
    if(index!==-1)activate(index);
  });
})();
