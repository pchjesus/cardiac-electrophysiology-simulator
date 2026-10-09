/*
 * v1.10 Patch 4 — independent non-modal help; no simulation state or timer.
 */
(function(){
    'use strict';
    const trigger=document.getElementById('wiggersHelpButton');
    const popup=document.getElementById('wiggersHelp');
    const closeButton=document.getElementById('wiggersHelpClose');
    if(!trigger || !popup || !closeButton)return;
    function close(restoreFocus=false){
        if(popup.hidden)return;
        popup.hidden=true;
        trigger.setAttribute('aria-expanded','false');
        if(restoreFocus)trigger.focus();
    }
    function open(){
        popup.hidden=false;
        trigger.setAttribute('aria-expanded','true');
        closeButton.focus();
    }
    trigger.addEventListener('click',()=>{
        if(popup.hidden)open();
        else close(true);
    });
    closeButton.addEventListener('click',()=>close(true));
    document.addEventListener('pointerdown',event=>{
        if(!popup.hidden && !popup.contains(event.target) &&
           !trigger.contains(event.target))close();
    });
    document.addEventListener('keydown',event=>{
        if(event.key==='Escape' && !popup.hidden){
            event.preventDefault();
            close(true);
        }
    });
})();
