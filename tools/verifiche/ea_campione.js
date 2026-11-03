// Campione EA Microsoft (#55): unisce campione + dati ANAC + letture degli atti, calcola le stime.
// Uso: node tools/verifiche/ea_campione.js   (da un clone pulito; nessun accesso di rete)
const fs = require("fs"), path = require("path");
const D = path.join(__dirname, "../../report/convenzioni/ea-campione");
function parse(s){const rows=[];let r=[],f="",q=false;for(let i=0;i<s.length;i++){const c=s[i];if(q){if(c=='"'){if(s[i+1]=='"'){f+='"';i++}else q=false}else f+=c}else if(c=='"')q=true;else if(c==","){r.push(f);f=""}else if(c=="\n"){r.push(f);rows.push(r);r=[];f=""}else if(c!="\r")f+=c}if(f||r.length){r.push(f);rows.push(r)}return rows}
const esc=v=>{v=v==null?"":String(v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};
const camp=parse(fs.readFileSync(path.join(D,"campione.csv"),"utf8")).slice(1).filter(r=>r.length>5);
const anac=Object.fromEntries(parse(fs.readFileSync(path.join(D,"anac.csv"),"utf8")).slice(1).map(r=>[r[0],r]));
const L=JSON.parse(fs.readFileSync(path.join(D,"letture.json"),"utf8"));
const H=["strato","cig","ente","importo_anac","importo_aggiudicazione_anac","canale_anac","importo_atto","url_atto","sha256","carrello","euro_cloud","euro_onprem","euro_non_attribuibile","stima_cloud_listino","stima_onprem_listino","prodotti","canale","stato_ricerca","note","oggetto"];
const rows=camp.map(r=>{const a=anac[r[1]]||[],l=L[r[1]]||{};return {strato:r[0],cig:r[1],ente:r[5].replace(/\s+/g," "),importo_anac:r[2],importo_aggiudicazione_anac:a[3]||"",canale_anac:a[2]||"",importo_atto:l.importo_atto||"",url_atto:l.url_atto||"",sha256:l.sha256||"",carrello:l.carrello||(l.stato_ricerca?"non trovato":""),euro_cloud:l.euro_cloud||"",euro_onprem:l.euro_onprem||"",euro_non_attribuibile:l.euro_non_attribuibile||"",stima_cloud_listino:l.stima_cloud_listino||"",stima_onprem_listino:l.stima_onprem_listino||"",prodotti:l.prodotti||"",canale:l.canale||"",stato_ricerca:l.stato_ricerca||"non ancora cercato",note:l.note||"",oggetto:(r[7]||"").split(" | ")[0].slice(0,150)}});
fs.writeFileSync(path.join(D,"risultati.csv"),[H.join(",")].concat(rows.map(o=>H.map(h=>esc(o[h])).join(","))).join("\n")+"\n");
// stime
const n=x=>parseFloat(x)||0, out=[];
const strati=["C1","C2","C3","E-saas","E-onprem"];
for(const s of strati){const R=rows.filter(o=>o.strato===s);const cerc=R.filter(o=>o.stato_ricerca!=="non ancora cercato").length;
 const C=R.filter(o=>o.carrello.startsWith("si"));const cl=C.reduce((a,o)=>a+n(o.euro_cloud),0),op=C.reduce((a,o)=>a+n(o.euro_onprem),0);
 // bootstrap della quota pesata in euro sui contratti con carrello
 let ci="";if(C.length>=2){const q=[];let seed=55;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648};
  for(let b=0;b<5000;b++){let a=0,t=0;for(let i=0;i<C.length;i++){const o=C[Math.floor(rnd()*C.length)];a+=n(o.euro_cloud);t+=n(o.euro_cloud)+n(o.euro_onprem)}q.push(a/t)}q.sort((x,y)=>x-y);ci=`[${(100*q[125]).toFixed(1)}-${(100*q[4874]).toFixed(1)} %]`}
 out.push(`${s}: ${R.length} contratti, ${cerc} cercati, ${C.length} con carrello in euro; cloud ${cl.toFixed(2)} EUR, on-premise ${op.toFixed(2)} EUR, quota cloud ${cl+op?(100*cl/(cl+op)).toFixed(1)+" %":"n.d."} ${ci}`)}
fs.writeFileSync(path.join(D,"stime.txt"),out.join("\n")+"\n");console.log(out.join("\n"));
