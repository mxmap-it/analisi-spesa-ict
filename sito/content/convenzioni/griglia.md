---
title: "Griglia delle convenzioni ICT"
date: 2026-11-05
description: "Cruscotto a griglia: per ogni iniziativa ICT, quali documenti e dati sono archiviati, reperiti altrove, mancanti o richiesti."
---

<!-- Generata da tools/convenzioni/pagine.py (griglia_pagina.py): i dati vengono da /dati/convenzioni-griglia.json, prodotto da tools/convenzioni/base_dati.py. -->

Una riga per iniziativa, una colonna per documento o dato atteso. Clic (o Invio) su una cella per i dettagli.
Torna all'[indice delle convenzioni](/convenzioni/) · [accesso civico](/convenzioni/accesso-civico/).

<div id="g-riepilogo" aria-live="polite"></div>

<fieldset class="g-filtri">
<legend>Filtri</legend>
<label>Soggetto <select id="f-tipo"><option value="">tutti</option><option value="consip">Consip</option><option value="psn">PSN</option><option value="aggregatore-regionale">Aggregatore regionale</option><option value="consorzio-unione">Consorzio o unione</option><option value="altro">Altro</option></select></label>
<label>Stato <select id="f-stato"><option value="">tutti</option><option value="attiva">attiva</option><option value="storica">storica</option></select></label>
<label>Categoria <select id="f-cat"><option value="">tutte</option></select></label>
<label>Valore minimo (M€) <input id="f-val" type="number" min="0" step="10" value="0" style="width:6em"></label>
</fieldset>

<ul class="g-legenda" aria-label="Legenda">
<li><span class="c s-ufficiale">✔</span> archiviato da fonte ufficiale</li>
<li><span class="c s-non-ufficiale">◐</span> reperito da fonte non ufficiale</li>
<li><span class="c s-pubblicato">○</span> pubblicato, non archiviato</li>
<li><span class="c s-carenza">✖</span> non pubblicato (carenza)</li>
<li><span class="c s-da-verificare">?</span> da verificare</li>
<li><span class="c s-richiesto">✉</span> richiesto con accesso civico</li>
</ul>

<div class="g-scroll"><table id="g-tab" class="g-tab"><thead></thead><tbody></tbody></table></div>
<div id="g-dettaglio" class="g-dettaglio" role="region" aria-label="Dettaglio della cella" tabindex="-1"></div>

<style>
.g-filtri{display:flex;flex-wrap:wrap;gap:.6em 1.2em;border:1px solid #ccc;padding:.5em .8em;margin:1em 0}
.g-filtri legend{font-size:1em;width:auto;padding:0 .3em}
.g-legenda{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:.4em 1.2em;font-size:.9em}
.g-scroll{overflow-x:auto;max-width:100%}
.g-tab{border-collapse:collapse;font-size:.8em}
.g-tab th,.g-tab td{border:1px solid #ddd;padding:2px 4px;text-align:center}
.g-tab th.r,.g-tab td.r{text-align:left;position:sticky;left:0;background:#fff;min-width:14em;max-width:22em}
.g-tab thead th{writing-mode:vertical-rl;transform:rotate(180deg);height:9em;white-space:nowrap;font-weight:600}
.g-tab thead th.r{writing-mode:horizontal-tb;transform:none;height:auto}
.c{display:inline-block;min-width:1.6em;border-radius:3px;font-weight:700;cursor:pointer}
.s-ufficiale{background:#1b7a3a;color:#fff}.s-non-ufficiale{background:#7fb3d5;color:#000}.s-pubblicato{background:#f4d35e;color:#000}
.s-carenza{background:#b00020;color:#fff}.s-da-verificare{background:#e0e0e0;color:#000}.s-richiesto{background:#5e35b1;color:#fff}
.g-dettaglio{border-left:6px solid #06c;background:#f2f6fc;padding:.6em 1em;margin:1em 0;display:none}
.g-riep{border-collapse:collapse;font-size:.85em;margin:.4em 0 1em}.g-riep td,.g-riep th{border:1px solid #ddd;padding:2px 6px}
.g-kpi{display:flex;flex-wrap:wrap;gap:1em}.g-kpi div{border:1px solid #ccc;padding:.4em .8em}.g-kpi b{display:block;font-size:1.4em}
</style>

<script>
(function(){
var SIMB={"ufficiale":"✔","non-ufficiale":"◐","pubblicato":"○","carenza":"✖","da-verificare":"?","richiesto":"✉"};
var TESTO={"ufficiale":"archiviato da fonte ufficiale","non-ufficiale":"reperito da fonte non ufficiale","pubblicato":"pubblicato, non archiviato","carenza":"non pubblicato (carenza)","da-verificare":"da verificare","richiesto":"richiesto con accesso civico"};
var TIPI={"consip":"Consip","psn":"PSN","aggregatore-regionale":"Aggregatore regionale","consorzio-unione":"Consorzio o unione","altro":"Altro"};
var GH="https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/accesso-civico/bozze/";
var D=null;
function e(t){return String(t==null?"":t).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function meur(v){return (v/1e6).toLocaleString("it-IT",{maximumFractionDigits:1})}
function filtrate(){
  var t=document.getElementById("f-tipo").value,s=document.getElementById("f-stato").value,c=document.getElementById("f-cat").value,m=+document.getElementById("f-val").value*1e6;
  return D.righe.filter(function(r){return (!t||r.tipo===t)&&(!s||r.stato===s)&&(!c||r.categoria===c)&&r.valore>=m})}
function riepilogo(rr){
  var tipi=D.tipi,h='<div class="g-kpi">';
  var val=0,cop=0,car=0;rr.forEach(function(r){val+=r.valore;cop+=r.valore*r.copertura;car+=r.carenze.length});
  h+='<div><b>'+rr.length+'</b>iniziative</div><div><b>'+meur(val)+' M€</b>valore ICT 2024-25</div><div><b>'+meur(cop)+' M€</b>valore coperto (pesato)</div><div><b>'+meur(val-cop)+' M€</b>valore scoperto</div><div><b>'+car+'</b>carenze</div><div><b>'+D.istanze.preparate+' / '+D.istanze.inviate+'</b>istanze preparate / inviate</div></div>';
  h+='<table class="g-riep"><caption>Copertura per tipo di documento (celle archiviate da fonte ufficiale)</caption><tr><th>Documento</th><th>Archiviati</th><th>Altrove</th><th>Carenza</th><th>%</th></tr>';
  tipi.forEach(function(t){var n=0,a=0,k=0,x=0;rr.forEach(function(r){var c=r.celle[t.id];if(!c)return;n++;if(c.s==="ufficiale")a++;if(c.s==="non-ufficiale")x++;if(c.s==="carenza")k++});
    if(n)h+='<tr><td>'+e(t.descrizione)+'</td><td>'+a+'</td><td>'+x+'</td><td>'+k+'</td><td>'+Math.round(100*a/n)+' %</td></tr>'});
  h+='</table><table class="g-riep"><caption>Per tipo di soggetto</caption><tr><th>Soggetto</th><th>Iniziative</th><th>Copertura media</th><th>Carenze</th></tr>';
  Object.keys(TIPI).forEach(function(k){var x=rr.filter(function(r){return r.tipo===k});if(!x.length)return;var c=0,n=0;x.forEach(function(r){c+=r.copertura;n+=r.carenze.length});
    h+='<tr><td>'+TIPI[k]+'</td><td>'+x.length+'</td><td>'+Math.round(100*c/x.length)+' %</td><td>'+n+'</td></tr>'});
  document.getElementById("g-riepilogo").innerHTML=h+'</table>'}
function disegna(){
  var rr=filtrate(),th='<tr><th class="r" scope="col">Iniziativa (M€ 2024-25)</th>';
  D.tipi.forEach(function(t){th+='<th scope="col" title="'+e(t.descrizione)+'">'+e(t.descrizione)+'</th>'});
  document.querySelector("#g-tab thead").innerHTML=th+'</tr>';
  var b="";rr.forEach(function(r,i){b+='<tr><th class="r" scope="row"><a href="/convenzioni/'+r.id.toLowerCase()+'/">'+e(r.nome)+'</a> <small>('+TIPI[r.tipo]+', '+meur(r.valore)+')</small></th>';
    D.tipi.forEach(function(t){var c=r.celle[t.id];b+=c?'<td><span class="c s-'+c.s+'" role="button" tabindex="0" data-r="'+i+'" data-t="'+t.id+'" aria-label="'+e(t.descrizione+": "+TESTO[c.s])+'">'+SIMB[c.s]+'</span></td>':'<td>–</td>'});b+='</tr>'});
  document.querySelector("#g-tab tbody").innerHTML=b;riepilogo(rr);window._rr=rr}
function dettaglio(el){
  var r=window._rr[+el.dataset.r],t=el.dataset.t,c=r.celle[t],d=document.getElementById("g-dettaglio"),desc=D.tipi.filter(function(x){return x.id===t})[0].descrizione;
  var h='<strong>'+e(r.nome)+'</strong> — '+e(desc)+': <strong>'+SIMB[c.s]+' '+TESTO[c.s]+'</strong>';
  if(c.doc)h+='<br>Documento: '+(c.url?'<a href="'+e(c.url)+'">'+e(c.doc)+'</a>':e(c.doc))+(c.n>1?' (e altri '+(c.n-1)+')':'');
  if(c.sha)h+='<br>sha256: <code>'+e(c.sha)+'</code>';
  if(c.fonte)h+='<br>Fonte: '+e(c.fonte)+(c.s==="non-ufficiale"?' (fonte non ufficiale: la carenza resta)':'');
  if(c.nota)h+='<br>Nota: '+e(c.nota);
  if(c.carenza)h+='<br>Carenza: '+e(c.carenza);
  if(c.istanza)h+='<br>Istanza di accesso civico: <a href="'+GH+e(c.istanza)+'.md">'+e(c.istanza)+'</a> ('+e(c.istanza_stato)+')';
  h+='<br><a href="/convenzioni/'+r.id.toLowerCase()+'/">Scheda dell\'iniziativa</a>';
  d.innerHTML=h;d.style.display="block";d.focus()}
fetch("/dati/convenzioni-griglia.json").then(function(x){return x.json()}).then(function(j){D=j;
  var cats={};j.righe.forEach(function(r){cats[r.categoria]=1});var s=document.getElementById("f-cat");
  Object.keys(cats).sort().forEach(function(k){var o=document.createElement("option");o.value=k;o.textContent=k;s.appendChild(o)});
  ["f-tipo","f-stato","f-cat","f-val"].forEach(function(id){document.getElementById(id).addEventListener("change",disegna)});
  document.getElementById("g-tab").addEventListener("click",function(ev){if(ev.target.dataset&&ev.target.dataset.t)dettaglio(ev.target)});
  document.getElementById("g-tab").addEventListener("keydown",function(ev){if((ev.key==="Enter"||ev.key===" ")&&ev.target.dataset&&ev.target.dataset.t){ev.preventDefault();dettaglio(ev.target)}});
  disegna()}).catch(function(){document.getElementById("g-riepilogo").textContent="Dati non disponibili: /dati/convenzioni-griglia.json"});
})();
</script>
