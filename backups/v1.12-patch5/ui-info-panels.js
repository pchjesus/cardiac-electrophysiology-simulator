/*
 * v1.10 Patch 5 — lightweight nonmodal user guide / categorized patch notes.
 * One delegated click listener + one keydown listener, no timers or
 * interactions with physiological state. Native controls retain activation.
 */
(function(){
 'use strict';
 const buttons=[...document.querySelectorAll('[data-open-info]')];
 const panels=[...document.querySelectorAll('[data-info-panel]')];
 if(!buttons.length||!panels.length)return;
 let current=null, opener=null;
 const getPanel=id=>panels.find(p=>p.id===id);
 function close(restoreFocus=false){
   if(!current)return;
   current.hidden=true;
   if(opener)opener.setAttribute('aria-expanded','false');
   const prev=opener;current=null;opener=null;
   if(restoreFocus&&prev)prev.focus();
 }
 function open(button){
   const next=getPanel(button.dataset.openInfo);
   if(!next)return;
   if(current===next){close(true);return;}
   close(false);
   current=next;opener=button;
   current.hidden=false;
   opener.setAttribute('aria-expanded','true');
   const firstClose=current.querySelector('[data-close-info]');
   if(firstClose)firstClose.focus();
 }
 document.addEventListener('click',event=>{
   const opening=event.target.closest('[data-open-info]');
   if(opening){open(opening);return;}
   const closing=event.target.closest('[data-close-info]');
   if(closing && current && current.contains(closing)){close(true);return;}
   if(current&&!current.contains(event.target))close(false);
 });
 document.addEventListener('keydown',event=>{
   if(event.key==='Escape'&&current){
      event.preventDefault();close(true);
   }
 });
 window.CardiacInfoPanels=Object.freeze({
   get current(){return current?.id||null;}
 });
})();
