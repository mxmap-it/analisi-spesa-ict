---
title: "Amministrazione trasparente: è indicizzabile?"
date: 2026-11-03
description: "Monitor mensile di tutte le amministrazioni italiane: la sezione «Amministrazione trasparente» è raggiungibile da motori di ricerca e bot, come chiede l'art. 9 c. 1 d.lgs. 33/2013? Esito per ente come open data, con serie storica, piattaforme e stato delle segnalazioni."
weight: 19
---

<style>
.tr-bar{display:flex;align-items:center;gap:.5rem;margin:.2rem 0;font-size:.9rem}
.tr-bar .lab{flex:0 0 16rem;max-width:45%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tr-bar .trk{flex:1;background:#e8ecef;border-radius:3px;height:1.05rem;overflow:hidden;white-space:nowrap}
.tr-bar .fill{height:100%;display:inline-block}
.tr-bar .val{flex:0 0 6.5rem;text-align:right;font-variant-numeric:tabular-nums}
.e-acc{background:#2e7d32}.e-rob{background:#b3261e}.e-noi{background:#e65100}.e-waf{background:#6a1b9a}
.e-irr{background:#9e9e9e}.e-tls{background:#795548}.e-url{background:#bdbdbd}.e-sni{background:#cfd8dc}.e-err{background:#000}
.tr-leg span{display:inline-block;margin-right:.9rem;font-size:.82rem}.tr-leg i{display:inline-block;width:.75rem;height:.75rem;margin-right:.25rem;vertical-align:middle}
#tr-filtri{display:flex;flex-wrap:wrap;gap:.5rem;margin:.5rem 0}
#tr-filtri input,#tr-filtri select{font-size:.9rem;padding:.25rem;max-width:100%}
#tr-tab{font-size:.82rem;width:100%;border-collapse:collapse}#tr-tab td,#tr-tab th{border-bottom:1px solid #e0e0e0;padding:.25rem;vertical-align:top}
#tr-tab .st span{display:inline-block;width:.7rem;height:.7rem;margin-right:1px;border-radius:2px}
.tr-num{font-size:1.6rem;font-weight:600}.tr-kpi{display:flex;flex-wrap:wrap;gap:1.5rem;margin:.5rem 0 1rem}
@media (max-width:600px){.tr-bar .lab{flex-basis:8rem}#tr-tab .nasc{display:none}}
</style>

**Versione del metodo 1.0.0.** Byproduct dell'analisi della spesa ICT, deciso da Fabio Pietrosanti il 3/11/2026
([#61](https://github.com/mxmap-it/analisi-spesa-ict/issues/61)); diventerà un progetto autonomo. Tutti i numeri di
questa pagina sono letti dall'open data del giro più recente: nessuna cifra è copiata a mano.

## 1. La regola

L'art. 9 c. 1 del d.lgs. 33/2013 vieta alle amministrazioni di disporre «filtri e altre soluzioni tecniche atte ad
impedire ai motori di ricerca web di indicizzare» la sezione «Amministrazione trasparente». Misuriamo, ente per ente:

- se il **robots.txt** vieta la sezione (o il file XML dei contratti) a tutti i bot, a Googlebot o a Bingbot;
- se la pagina dichiara **noindex** (meta robots o intestazione X-Robots-Tag);
- se un **WAF o un sistema anti-bot** respinge i client automatici (Cloudflare, Imperva, Akamai, Azure, F5…);
- se la sezione è **irraggiungibile**, ha un **certificato non valido** o un **URL non valido**;
- quale **piattaforma** la pubblica, solo quando è dichiarata o certa (altrimenti «ignota»).

Da dove vengono gli URL: il **registro ANAC delle comunicazioni art. 1 c. 32 L. 190/2012** (l'URL del file XML dei
contratti che ogni ente comunica ad ANAC), **IndicePA** (sito istituzionale) e, se serve, il link nella home.
Metodo completo, firme e limiti: [`METODO.md`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/trasparenza/METODO.md).
Software: [`tools/trasparenza/`](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/tools/trasparenza) (EUPL-1.2).

Non risolviamo CAPTCHA, non ruotiamo IP, non usiamo lo User-Agent di Google: ci presentiamo come bot dichiarato e come
browser con l'indirizzo di questa pagina, una richiesta ogni 5 secondi per sito.

## 2. Il giro più recente

<div id="tr-kpi" class="tr-kpi">Caricamento…</div>
<div class="tr-leg" id="tr-leg"></div>

### Per esito
<div id="tr-esiti"></div>

### Per tipo di ente (violazioni art. 9 sul totale)
<div id="tr-cat"></div>

### Per regione
<div id="tr-reg"></div>

### Per piattaforma
<div id="tr-pia"></div>

### Nel tempo
<div id="tr-giri"></div>

## 3. Cerca un ente

<div id="tr-filtri">
<input id="f-q" type="search" placeholder="denominazione o codice fiscale" aria-label="cerca">
<select id="f-esito" aria-label="esito"><option value="">tutti gli esiti</option></select>
<select id="f-cat" aria-label="tipo"><option value="">tutti i tipi</option></select>
<select id="f-reg" aria-label="regione"><option value="">tutte le regioni</option></select>
<select id="f-pia" aria-label="piattaforma"><option value="">tutte le piattaforme</option></select>
</div>
<p id="tr-conta" style="font-size:.85rem"></p>
<div style="overflow-x:auto"><table id="tr-tab"><thead><tr><th>ente</th><th>esito</th><th class="nasc">dettaglio</th><th class="nasc">piattaforma</th><th>storia</th><th>PEC</th></tr></thead><tbody></tbody></table></div>
<p><button id="tr-piu" type="button" style="display:none">mostra altri</button></p>

## 4. Open data

- Ultimo giro: [`enti.csv.gz`](/dati/trasparenza/ultimo/enti.csv.gz), [`enti.json.gz`](/dati/trasparenza/ultimo/enti.json.gz),
  [`riepilogo.json`](/dati/trasparenza/ultimo/riepilogo.json), tabelle `per-esito.csv`, `per-categoria.csv`,
  `per-regione.csv`, `per-piattaforma.csv` nella stessa cartella.
- Ogni giro resta pubblicato in `/dati/trasparenza/giri/AAAA-MM-GG/` e non si sovrascrive; elenco in
  [`indice.json`](/dati/trasparenza/indice.json); serie storica per ente in [`storico.json`](/dati/trasparenza/storico.json);
  stato delle segnalazioni in [`invii.json`](/dati/trasparenza/invii.json).
- Schema: [`enti.schema.json`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/trasparenza/schema/enti.schema.json).
  Licenza dei dati: CC BY 4.0.
- Le evidenze (robots.txt e risposte dei casi non accessibili) sono archiviate con sha256, citato nei dati.

## 5. Segnalazioni

Per ogni ente in violazione prepariamo una PEC all'ente (al Responsabile per la trasparenza) e una ad ANAC
(art. 45 d.lgs. 33/2013), con le evidenze allegate. Gli invii li decide e li fa Fabio Pietrosanti; ogni invio, ricevuta e
risposta finisce in un registro pubblico, e il giro successivo misura se il problema è stato risolto.

**Verificato e riferito.** Gli esiti sono misurati da noi alla data del giro. L'URL comunicato ad ANAC e l'esito
dell'accesso di ANAC sono *riferiti* da ANAC. Un esito «bloccato» con codice 403 a entrambi i client, senza firma di
WAF riconosciuta, può essere un sito guasto: è segnato come da confermare.

## Registro delle revisioni

| versione | data | cambiamento |
|---|---|---|
| 1.0 | 2026-11-03 | prima pubblicazione: metodo 1.0.0, pilota e censimento completo |

<script>
(function(){
const B='/dati/trasparenza/';
const COL={'accessibile':'e-acc','bloccato da robots.txt':'e-rob','noindex':'e-noi','bloccato da WAF/anti-bot':'e-waf','irraggiungibile':'e-irr','tls invalido':'e-tls','url non valido':'e-url','sezione non individuata':'e-sni','errore dello strumento':'e-err'};
const VIOL=new Set(['bloccato da robots.txt','noindex','bloccato da WAF/anti-bot']);
const nf=n=>n.toLocaleString('it-IT');const pc=(a,b)=>b?(100*a/b).toLocaleString('it-IT',{maximumFractionDigits:1})+' %':'–';
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function barre(el,righe,max){el.innerHTML=righe.map(([lab,parti,val])=>{const tot=parti.reduce((a,p)=>a+p[1],0);
 return `<div class="tr-bar"><span class="lab" title="${esc(lab)}">${esc(lab)}</span><span class="trk">${parti.map(p=>`<span class="fill ${COL[p[0]]||''}" style="width:${100*p[1]/max}%" title="${esc(p[0])}: ${nf(p[1])}"></span>`).join('')}</span><span class="val">${val}</span></div>`}).join('')}
function perGruppo(el,agg,limite){const r=Object.entries(agg).map(([k,v])=>{const t=Object.values(v).reduce((a,b)=>a+b,0);const vi=Object.entries(v).filter(([e])=>VIOL.has(e)).reduce((a,[,n])=>a+n,0);return [k,v,t,vi]}).sort((a,b)=>b[2]-a[2]).slice(0,limite);
 barre(el,r.map(([k,v,t,vi])=>[k,Object.keys(COL).filter(e=>v[e]).map(e=>[e,v[e]/t*100]),`${pc(vi,t)} di ${nf(t)}`]),100)}
Promise.all([fetch(B+'ultimo/riepilogo.json').then(r=>r.json()),fetch(B+'ultimo/dashboard.json').then(r=>r.json()),
 fetch(B+'storico.json').then(r=>r.ok?r.json():{}).catch(()=>({})),fetch(B+'invii.json').then(r=>r.ok?r.json():{invii:{}}).catch(()=>({invii:{}})),
 fetch(B+'indice.json').then(r=>r.ok?r.json():{giri:[]}).catch(()=>({giri:[]}))]).then(([R,D,S,I,G])=>{
 const tot=R.enti;
 document.getElementById('tr-kpi').innerHTML=`<div><div class="tr-num">${nf(tot)}</div>enti verificati (giro ${esc(R.giro)})</div><div><div class="tr-num">${nf(R.violazioni_art9)}</div>in violazione dell'art. 9 (${pc(R.violazioni_art9,tot)})</div><div><div class="tr-num">${nf(R.esiti['accessibile']||0)}</div>accessibili (${pc(R.esiti['accessibile']||0,tot)})</div>`;
 document.getElementById('tr-leg').innerHTML=Object.keys(COL).map(e=>`<span><i class="${COL[e]}"></i>${e}</span>`).join('');
 const mx=Math.max(...Object.values(R.esiti));
 barre(document.getElementById('tr-esiti'),Object.keys(COL).filter(e=>R.esiti[e]).map(e=>[e,[[e,R.esiti[e]]],`${nf(R.esiti[e])} (${pc(R.esiti[e],tot)})`]),mx);
 perGruppo(document.getElementById('tr-cat'),R.per_categoria,25);
 perGruppo(document.getElementById('tr-reg'),R.per_regione,25);
 perGruppo(document.getElementById('tr-pia'),R.per_piattaforma,20);
 barre(document.getElementById('tr-giri'),G.giri.map(g=>[g.giro,Object.keys(COL).filter(e=>g.esiti[e]).map(e=>[e,g.esiti[e]/g.enti*100]),`${pc(g.violazioni_art9,g.enti)} viol.`]),100);
 const C=D.campi,ix=Object.fromEntries(C.map((c,i)=>[c,i])),E=D.enti;
 const opz=(id,k)=>{const s=document.getElementById(id);[...new Set(E.map(e=>e[ix[k]]||'(n.d.)'))].sort().forEach(v=>{const o=document.createElement('option');o.value=o.textContent=v;s.appendChild(o)})};
 opz('f-esito','esito');opz('f-cat','categoria');opz('f-reg','regione');opz('f-pia','piattaforma');
 let vis=100;const tb=document.querySelector('#tr-tab tbody');
 function pecStato(cf){const s=(I.invii||{})[cf];if(!s)return '';return Object.entries(s).map(([d,v])=>`${d}: ${esc(v.ultimo_evento)} ${esc(v[v.ultimo_evento]||'')}`).join('<br>')}
 function disegna(){const q=document.getElementById('f-q').value.trim().toLowerCase();const f=k=>document.getElementById(k).value;
  const ok=E.filter(e=>(!q||e[ix.denominazione].toLowerCase().includes(q)||e[ix.cf].toLowerCase()===q)&&(!f('f-esito')||e[ix.esito]===f('f-esito'))&&(!f('f-cat')||(e[ix.categoria]||'(n.d.)')===f('f-cat'))&&(!f('f-reg')||(e[ix.regione]||'(n.d.)')===f('f-reg'))&&(!f('f-pia')||(e[ix.piattaforma]||'(n.d.)')===f('f-pia')));
  document.getElementById('tr-conta').textContent=`${nf(ok.length)} enti`;
  tb.innerHTML=ok.slice(0,vis).map(e=>{const st=(S[e[ix.cf]]||[]).map(([g,es])=>`<span class="${COL[es]||''}" title="${esc(g)}: ${esc(es)}"></span>`).join('');
   const at=e[ix.at_url]?`<br><a href="${esc(e[ix.at_url])}" rel="nofollow noopener">sezione</a>`:'';
   return `<tr><td>${esc(e[ix.denominazione])}<br><small>${esc(e[ix.cf])} · ${esc(e[ix.categoria])} · ${esc(e[ix.regione])}</small>${at}</td><td><span class="${COL[e[ix.esito]]||''}" style="display:inline-block;width:.7rem;height:.7rem"></span> ${esc(e[ix.esito])}</td><td class="nasc">${esc(e[ix.dettaglio_esito]).slice(0,180)}</td><td class="nasc">${esc(e[ix.piattaforma])}</td><td class="st">${st}</td><td><small>${pecStato(e[ix.cf])}</small></td></tr>`}).join('');
  document.getElementById('tr-piu').style.display=ok.length>vis?'':'none'}
 ['f-q','f-esito','f-cat','f-reg','f-pia'].forEach(id=>document.getElementById(id).addEventListener('input',()=>{vis=100;disegna()}));
 document.getElementById('tr-piu').addEventListener('click',()=>{vis+=200;disegna()});
 disegna();
}).catch(e=>{document.getElementById('tr-kpi').textContent='Dati non ancora pubblicati: il primo giro completo è in corso.'});
})();
</script>
