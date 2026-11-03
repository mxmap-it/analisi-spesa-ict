---
title: "Amministrazione trasparente: è indicizzabile? (beta)"
date: 2026-11-04
description: "Monitor di tutte le amministrazioni italiane: la sezione «Amministrazione trasparente» è raggiungibile da motori di ricerca e bot, come chiede l'art. 9 c. 1 d.lgs. 33/2013? Esito per ente come open data, tassonomia dei blocchi, piattaforme, log grezzi, serie storica e stato delle segnalazioni. Versione beta."
weight: 19
---

<style>
.tr-bar{display:flex;align-items:center;gap:.5rem;margin:.2rem 0;font-size:.9rem}
.tr-bar .lab{flex:0 0 17rem;max-width:45%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tr-bar .trk{flex:1;background:#e8ecef;border-radius:3px;height:1.05rem;overflow:hidden;white-space:nowrap}
.tr-bar .fill{height:100%;display:inline-block}
.tr-bar .val{flex:0 0 7rem;text-align:right;font-variant-numeric:tabular-nums}
.e-acc{background:#2e7d32}.e-rob{background:#b3261e}.e-noi{background:#e65100}.e-waf{background:#6a1b9a}
.e-irr{background:#9e9e9e}.e-tls{background:#795548}.e-url{background:#bdbdbd}.e-sni{background:#cfd8dc}.e-err{background:#000}.e-gen{background:#1f5fa8}
.tr-leg span{display:inline-block;margin-right:.9rem;font-size:.82rem}.tr-leg i{display:inline-block;width:.75rem;height:.75rem;margin-right:.25rem;vertical-align:middle}
#tr-filtri{display:flex;flex-wrap:wrap;gap:.5rem;margin:.5rem 0}
#tr-filtri input,#tr-filtri select{font-size:.9rem;padding:.25rem;max-width:100%}
#tr-tab{font-size:.82rem;width:100%;border-collapse:collapse}#tr-tab td,#tr-tab th{border-bottom:1px solid #e0e0e0;padding:.25rem;vertical-align:top}
#tr-tab tr.cl{cursor:pointer}#tr-tab tr.cl:hover{background:#f5f7f9}
#tr-tab .st span{display:inline-block;width:.7rem;height:.7rem;margin-right:1px;border-radius:2px}
.tr-num{font-size:1.6rem;font-weight:600}.tr-kpi{display:flex;flex-wrap:wrap;gap:1.5rem;margin:.5rem 0 1rem}
.tr-beta{background:#fff3cd;border:1px solid #e0c36a;padding:.5rem .75rem;border-radius:4px;font-size:.9rem}
.tr-scheda{background:#f8f9fa;font-size:.8rem}.tr-scheda table{width:100%;border-collapse:collapse}.tr-scheda td,.tr-scheda th{border-bottom:1px solid #e3e3e3;padding:.2rem;vertical-align:top}
.tr-scheda pre{white-space:pre-wrap;word-break:break-all;max-height:12rem;overflow:auto;font-size:.75rem;margin:0}
@media (max-width:600px){.tr-bar .lab{flex-basis:8rem}#tr-tab .nasc{display:none}}
</style>

<p class="tr-beta"><strong>Beta.</strong> Metodo <span id="tr-ver">1.1.0-beta</span>. Gli esiti sono misure automatiche ripetibili;
i blocchi diventano «confermati» solo dopo due verifiche distanti almeno un'ora. Limiti noti nel §6. Segnalazioni di errori:
<a href="https://github.com/mxmap-it/analisi-spesa-ict/issues/61">#61</a>.</p>

Byproduct dell'analisi della spesa ICT, deciso da Fabio Pietrosanti il 3/11/2026; diventerà un progetto con nome e
repository propri. **Tutti i numeri di questa pagina sono letti dall'open data del giro più recente.**

## 1. La regola

L'art. 9 c. 1 del d.lgs. 33/2013 vieta alle amministrazioni di disporre «filtri e altre soluzioni tecniche atte ad
impedire ai motori di ricerca web di indicizzare» la sezione «Amministrazione trasparente». Per ogni ente misuriamo:

- **robots.txt**: se vieta la sezione a tutti, a Googlebot, a Bingbot (violazione), e a quali altri client (crawler AI, curl, wget, python: solo informativo);
- **noindex** nella pagina o nell'intestazione X-Robots-Tag;
- **WAF e anti-bot**: risposte reali a cinque identità oneste (il nostro bot dichiarato, python-requests e curl con le impostazioni di default, un browser con l'indirizzo del progetto, un browser reale), da due punti di osservazione (server in datacenter e computer con IP residenziale). Ne ricaviamo il meccanismo: blocco per User-Agent, per IP/datacenter, challenge JavaScript, CAPTCHA;
- **raggiungibilità, certificato TLS e URL**;
- **piattaforma** del portale, solo se dichiarata o certa;
- su un campione, **ricercabilità**: cerchiamo nella sezione un CIG reale 2024-2025 dell'ente, e confrontiamo l'URL comunicato ad ANAC con il percorso dalla home.

Non risolviamo CAPTCHA, non ruotiamo IP né usiamo proxy, non falsifichiamo l'impronta del browser e **non impersoniamo mai Google, Bing o i crawler AI**: le loro regole si leggono solo nel robots.txt.

## 2. Il giro più recente

<div id="tr-kpi" class="tr-kpi">Caricamento…</div>
<div class="tr-leg" id="tr-leg"></div>

### Per esito
<div id="tr-esiti"></div>

### Tassonomia dei blocchi
Meccanismi riconosciuti (un ente può averne più d'uno):
<div id="tr-mecc"></div>

Conferma dei blocchi:
<div id="tr-conf"></div>

robots.txt: identità a cui è vietata la sezione:
<div id="tr-rob"></div>

Protezioni riconosciute dalle firme:
<div id="tr-vend"></div>

Datacenter e IP residenziale a confronto:
<div id="tr-orig"></div>

### Ricercabilità (campione)
<div id="tr-ric"></div>

### Per tipo di ente (violazioni sul totale)
<div id="tr-cat"></div>

### Per regione
<div id="tr-reg"></div>

### Per piattaforma
<div id="tr-pia"></div>

### Nel tempo
<div id="tr-giri"></div>
<p id="tr-camb" style="font-size:.85rem"></p>

## 3. Cerca un ente

Clicca una riga per la scheda diagnostica: tentativi per identità e origine, IP e ASN dell'osservatore, DNS, TLS,
intestazioni, firme riconosciute e link ai log grezzi.

<div id="tr-filtri">
<input id="f-q" type="search" placeholder="denominazione o codice fiscale" aria-label="cerca">
<select id="f-esito" aria-label="esito"><option value="">tutti gli esiti</option></select>
<select id="f-mecc" aria-label="meccanismo"><option value="">tutti i meccanismi</option></select>
<select id="f-cat" aria-label="tipo"><option value="">tutti i tipi</option></select>
<select id="f-reg" aria-label="regione"><option value="">tutte le regioni</option></select>
<select id="f-pia" aria-label="piattaforma"><option value="">tutte le piattaforme</option></select>
</div>
<p id="tr-conta" style="font-size:.85rem"></p>
<div style="overflow-x:auto"><table id="tr-tab"><thead><tr><th>ente</th><th>esito</th><th class="nasc">meccanismo e conferma</th><th class="nasc">piattaforma</th><th>storia</th><th>PEC</th></tr></thead><tbody></tbody></table></div>
<p><button id="tr-piu" type="button" style="display:none">mostra altri</button></p>

## 4. Open data

- Ultimo giro: [`enti.csv.gz`](/dati/trasparenza/ultimo/enti.csv.gz), [`enti.json.gz`](/dati/trasparenza/ultimo/enti.json.gz),
  [`tentativi.csv.gz`](/dati/trasparenza/ultimo/tentativi.csv.gz) (un tentativo per riga), `tentativi.jsonl.gz` (completo, con intestazioni),
  `caratteri.jsonl.gz` (due vie e ricerca), [`riepilogo.json`](/dati/trasparenza/ultimo/riepilogo.json),
  [`cambiamenti.csv`](/dati/trasparenza/ultimo/cambiamenti.csv), tabelle `per-*.csv`, schede `schede/<cf>.json`.
- Ogni giro resta in `/dati/trasparenza/giri/AAAA-MM-GG/` e non si sovrascrive; elenco in [`indice.json`](/dati/trasparenza/indice.json);
  serie storica in [`storico.json`](/dati/trasparenza/storico.json); segnalazioni in [`invii.json`](/dati/trasparenza/invii.json).
- Log grezzi dei tentativi falliti (dump HTTP o HAR del browser) in `/dati/trasparenza/prove/<sha256>.*.gz`: il nome è l'impronta del contenuto.
- Schema: [`enti.schema.json`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/trasparenza/schema/enti.schema.json). Licenza dei dati: CC BY 4.0.
  Codice: [`tools/trasparenza/`](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/tools/trasparenza) (EUPL-1.2), con il
  [catalogo delle problematiche](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/trasparenza/README.md#catalogo-delle-problematiche).

## 5. Segnalazioni

Per ogni ente in violazione il software prepara una PEC all'ente (al Responsabile per la trasparenza) e una ad ANAC
(art. 45 d.lgs. 33/2013) con le evidenze allegate. **Gli invii li decide e li fa Fabio Pietrosanti**: nessuna PEC parte dal
software. Ogni invio, ricevuta e risposta va in un registro pubblico; il giro successivo misura se il problema è risolto.

## 6. Metodo e limiti

Fonti degli URL: registro ANAC delle comunicazioni art. 1 c. 32 L. 190/2012 (l'URL del file XML dei contratti, ultimo anno
disponibile 2023), IndicePA e il link nella home. Metodo completo:
[`METODO.md`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/trasparenza/METODO.md).

- **Verificato e riferito.** Gli esiti sono misurati da noi alla data del giro. L'URL comunicato ad ANAC e l'esito
  dell'accesso di ANAC sono *riferiti* da ANAC.
- L'URL ANAC può essere vecchio; la scoperta dalla home non vede menu generati via JavaScript («sezione non individuata»).
- La verifica estesa (cinque identità, due giri, browser reale) si fa sugli enti con esito dubbio; la caratterizzazione
  (due vie e ricerca per CIG) su un campione stratificato. Il desktop residenziale copre un sottoinsieme.
- «Nessun client accettato» senza firma riconosciuta può essere un sito guasto e non un blocco.
- Il controllo manuale dei falsi positivi è descritto nel registro qui sotto.

## Registro delle revisioni

| versione | data | cambiamento |
|---|---|---|
| 1.0 | 2026-11-03 | prima stesura: metodo 1.0.0, pilota |
| 1.1 beta | 2026-11-04 | metodo 1.1.0-beta: tassonomia per identità, due origini, conferma in due giri, log grezzi, ricercabilità, schede, cambiamenti |

<script>
(function(){
const B='/dati/trasparenza/',U=B+'ultimo/';
const COL={'accessibile':'e-acc','bloccato da robots.txt':'e-rob','noindex':'e-noi','bloccato da WAF/anti-bot':'e-waf','irraggiungibile':'e-irr','tls invalido':'e-tls','url non valido':'e-url','sezione non individuata':'e-sni','errore dello strumento':'e-err'};
const VIOL=new Set(['bloccato da robots.txt','noindex','bloccato da WAF/anti-bot']);
const nf=n=>Number(n||0).toLocaleString('it-IT');const pc=(a,b)=>b?(100*a/b).toLocaleString('it-IT',{maximumFractionDigits:1})+' %':'–';
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const $=id=>document.getElementById(id);
function barre(el,righe,max){el.innerHTML=righe.length?righe.map(([lab,parti,val])=>`<div class="tr-bar"><span class="lab" title="${esc(lab)}">${esc(lab)}</span><span class="trk">${parti.map(p=>`<span class="fill ${COL[p[0]]||'e-gen'}" style="width:${100*p[1]/max}%" title="${esc(p[0])}: ${nf(p[1])}"></span>`).join('')}</span><span class="val">${val}</span></div>`).join(''):'<p style="font-size:.85rem">nessun dato in questo giro</p>'}
function semplice(el,obj,tot){const e=Object.entries(obj||{});const mx=Math.max(1,...e.map(x=>x[1]));barre(el,e.map(([k,v])=>[k,[['',v]],tot?`${nf(v)} (${pc(v,tot)})`:nf(v)]),mx)}
function perGruppo(el,agg,limite){const r=Object.entries(agg||{}).map(([k,v])=>{const t=Object.values(v).reduce((a,b)=>a+b,0);const vi=Object.entries(v).filter(([e])=>VIOL.has(e)).reduce((a,[,n])=>a+n,0);return [k,v,t,vi]}).sort((a,b)=>b[2]-a[2]).slice(0,limite);
 barre(el,r.map(([k,v,t,vi])=>[k,Object.keys(COL).filter(e=>v[e]).map(e=>[e,v[e]/t*100]),`${pc(vi,t)} di ${nf(t)}`]),100)}
const j=u=>fetch(u).then(r=>r.ok?r.json():null).catch(()=>null);
Promise.all([j(U+'riepilogo.json'),j(U+'dashboard.json'),j(B+'storico.json'),j(B+'invii.json'),j(B+'indice.json')]).then(([R,D,S,I,G])=>{
 if(!R||!D){$('tr-kpi').textContent='Dati non ancora pubblicati: il primo giro è in corso.';return}
 S=S||{};I=I||{invii:{}};G=G||{giri:[]};const tot=R.enti;$('tr-ver').textContent=R.metodo||'';
 $('tr-kpi').innerHTML=`<div><div class="tr-num">${nf(tot)}</div>enti verificati (giro ${esc(R.giro)})</div><div><div class="tr-num">${nf(R.violazioni_art9)}</div>in violazione dell'art. 9 (${pc(R.violazioni_art9,tot)})</div><div><div class="tr-num">${nf((R.conferma_blocco||{})['confermato'])}</div>blocchi WAF/anti-bot confermati</div><div><div class="tr-num">${nf(R.esiti['accessibile'])}</div>accessibili (${pc(R.esiti['accessibile'],tot)})</div>`;
 $('tr-leg').innerHTML=Object.keys(COL).map(e=>`<span><i class="${COL[e]}"></i>${e}</span>`).join('');
 const mx=Math.max(...Object.values(R.esiti));
 barre($('tr-esiti'),Object.keys(COL).filter(e=>R.esiti[e]).map(e=>[e,[[e,R.esiti[e]]],`${nf(R.esiti[e])} (${pc(R.esiti[e],tot)})`]),mx);
 semplice($('tr-mecc'),R.meccanismi_blocco);semplice($('tr-conf'),R.conferma_blocco);semplice($('tr-rob'),R.robots_identita_negate,tot);
 semplice($('tr-vend'),R.vendor_blocco);semplice($('tr-orig'),R.lettura_origini);semplice($('tr-ric'),R.ricercabilita);
 perGruppo($('tr-cat'),R.per_categoria,25);perGruppo($('tr-reg'),R.per_regione,25);perGruppo($('tr-pia'),R.per_piattaforma,20);
 barre($('tr-giri'),G.giri.map(g=>[g.giro,Object.keys(COL).filter(e=>g.esiti[e]).map(e=>[e,g.esiti[e]/g.enti*100]),`${pc(g.violazioni_art9,g.enti)} viol.`]),100);
 const cb=R.cambiamenti||{};$('tr-camb').innerHTML=cb.totale?`Rispetto al giro precedente: ${nf(cb.totale)} cambiamenti (<a href="${U}cambiamenti.csv">elenco</a>).`:'Primo giro: nessun confronto ancora disponibile.';
 const C=D.campi,ix=Object.fromEntries(C.map((c,i)=>[c,i])),E=D.enti;
 const opz=(id,k,split)=>{const s=$(id);const v=new Set();E.forEach(e=>{const x=e[ix[k]]||'(n.d.)';(split?x.split(';'):[x]).forEach(y=>y&&v.add(y))});[...v].sort().forEach(x=>{const o=document.createElement('option');o.value=o.textContent=x;s.appendChild(o)})};
 opz('f-esito','esito');opz('f-mecc','meccanismi_blocco',true);opz('f-cat','categoria');opz('f-reg','regione');opz('f-pia','piattaforma');
 let vis=100;const tb=document.querySelector('#tr-tab tbody');
 const pecStato=cf=>{const s=(I.invii||{})[cf];return s?Object.entries(s).map(([d,v])=>`${d}: ${esc(v.ultimo_evento)} ${esc(v[v.ultimo_evento]||'')}`).join('<br>'):''};
 const v=(e,k)=>e[ix[k]]||'';
 function disegna(){const q=$('f-q').value.trim().toLowerCase();const f=k=>$(k).value;
  const ok=E.filter(e=>(!q||v(e,'denominazione').toLowerCase().includes(q)||v(e,'cf').toLowerCase()===q)&&(!f('f-esito')||v(e,'esito')===f('f-esito'))&&(!f('f-mecc')||v(e,'meccanismi_blocco').split(';').includes(f('f-mecc')))&&(!f('f-cat')||(v(e,'categoria')||'(n.d.)')===f('f-cat'))&&(!f('f-reg')||(v(e,'regione')||'(n.d.)')===f('f-reg'))&&(!f('f-pia')||(v(e,'piattaforma')||'(n.d.)')===f('f-pia')));
  $('tr-conta').textContent=`${nf(ok.length)} enti`;
  tb.innerHTML=ok.slice(0,vis).map(e=>{const st=(S[v(e,'cf')]||[]).map(([g,es])=>`<span class="${COL[es]||''}" title="${esc(g)}: ${esc(es)}"></span>`).join('');
   const at=v(e,'at_url')?`<br><a href="${esc(v(e,'at_url'))}" rel="nofollow noopener">sezione</a>`:'';
   const mc=[v(e,'meccanismi_blocco').replaceAll(';','; '),v(e,'conferma_blocco')].filter(Boolean).join(' — ');
   return `<tr class="cl" data-cf="${esc(v(e,'cf'))}"><td>${esc(v(e,'denominazione'))}<br><small>${esc(v(e,'cf'))} · ${esc(v(e,'categoria'))} · ${esc(v(e,'regione'))}</small>${at}${v(e,'pvl_sistemi')?`<br><small>e-procurement (PVL): ${esc(v(e,'pvl_sistemi').replaceAll(';',', '))} · ${esc(v(e,'pvl_link_n'))} link</small>`:''}</td><td><span class="${COL[v(e,'esito')]||''}" style="display:inline-block;width:.7rem;height:.7rem"></span> ${esc(v(e,'esito'))}<br><small>${esc(v(e,'dettaglio_esito')).slice(0,140)}</small></td><td class="nasc">${esc(mc)}</td><td class="nasc">${esc(v(e,'piattaforma'))}</td><td class="st">${st}</td><td><small>${pecStato(v(e,'cf'))}</small></td></tr>`}).join('');
  $('tr-piu').style.display=ok.length>vis?'':'none'}
 tb.addEventListener('click',ev=>{const tr=ev.target.closest('tr.cl');if(!tr||ev.target.tagName==='A')return;const nx=tr.nextElementSibling;if(nx&&nx.classList.contains('tr-scheda')){nx.remove();return}
  const cf=tr.dataset.cf;const td=document.createElement('tr');td.className='tr-scheda';td.innerHTML='<td colspan="6">Caricamento…</td>';tr.after(td);
  j(U+'schede/'+encodeURIComponent(cf)+'.json').then(s=>{if(!s){td.firstChild.textContent='Nessuna verifica estesa per questo ente (esito della sola prima prova).';return}
   const t=(s.tentativi||[]).map(x=>`<tr><td>${esc(x.origine)}<br><small>${esc(x.ip)} ${esc(x.asn)} ${esc(x.asn_nome)}</small></td><td>${esc(x.identita)}<br><small>${esc(x.client)}</small></td><td>${esc(x.ts)}<br><small>giro ${esc(x.giro_conferma)}</small></td><td>${esc(x.status??'')} ${esc(x.errore||'')}<br><small>${esc((x.redirect||[]).join(' → '))}</small></td><td>${esc((x.vendor_blocco||[]).join(', '))}${x.challenge_js?' · challenge JS':''}${x.captcha?' · CAPTCHA':''}<br><small>${esc((x.cdn||[]).join(', '))}</small></td><td>${x.grezzo_url&&x.grezzo_url.startsWith('/')?`<a href="${esc(x.grezzo_url)}">log grezzo</a>`:esc(x.grezzo_sha256?('sha256 '+x.grezzo_sha256.slice(0,12)+'…'):'')}</td></tr>`).join('');
   const d=(s.tentativi||[])[0]||{};const k=s.caratterizzazione;
   td.firstChild.innerHTML=`<p><strong>${esc(s.esito)}</strong>${s.esito_sonda&&s.esito_sonda!==s.esito?` (prima prova: ${esc(s.esito_sonda)})`:''} · ${esc(s.meccanismi||'')} · ${esc(s.conferma||'')}<br>identità bloccate: ${esc(s.identita_bloccate||'nessuna')} · robots.txt vieta a: ${esc(s.robots_negati||'nessuno')} ${s.robots_sha256?`(<small>sha256 ${esc(s.robots_sha256.slice(0,12))}…</small>)`:''}</p>
   ${d.dns?`<p>DNS ${esc(d.dns.host)}: A ${esc((d.dns.a||[]).join(', '))} · AAAA ${esc((d.dns.aaaa||[]).join(', '))} · alias ${esc((d.dns.alias||[]).join(', '))}<br>TLS: ${esc(d.tls&&(d.tls.versione||''))} ${esc(d.tls&&(d.tls.emittente||''))} scade ${esc(d.tls&&(d.tls.scadenza||''))} ${esc(d.tls&&(d.tls.errore||''))}</p>`:''}
   <table><thead><tr><th>origine</th><th>identità</th><th>quando</th><th>risposta</th><th>firme / CDN</th><th>prova</th></tr></thead><tbody>${t}</tbody></table>
   ${k?`<p>Via ANAC: ${esc(k.via_anac||'–')} · via home: ${esc(k.via_home||'–')} · coincidono: ${k.coincidono?'sì':'no'}<br>Ricerca del CIG ${esc(k.cig_test||'')}: <strong>${esc(k.ricercabilita||'')}</strong></p>`:''}`})});
 ['f-q','f-esito','f-mecc','f-cat','f-reg','f-pia'].forEach(id=>$(id).addEventListener('input',()=>{vis=100;disegna()}));
 $('tr-piu').addEventListener('click',()=>{vis+=200;disegna()});
 disegna();
});
})();
</script>
