'use strict';
// LSPV-1/603 hypothetical evidence-explicit two-premise proof-system countercontrol.
// Execute: node experiments/arc/lspv1_603_evidence_explicit_native_unknown_firewall.cjs
// NOT original historical R_mix341 acceptance.
function run(){
  "use strict";
  let checks=0;
  function ok(c,msg){checks++;if(!c)throw Error(msg)}
  function canon(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
  function satClause(c,a){return c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))}
  function models(F,n){let z=0;for(let a=0;a<2**n;a++)if(F.every(c=>satClause(c,a)))z++;return z}
  function k4(charges){
    const e=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],o=Array.from({length:4},()=>[]);
    e.forEach(([u,v],j)=>{o[u].push(j+1);o[v].push(j+1)});
    let F=[];for(let v=0;v<4;v++)for(let a=0;a<8;a++){let b=[a&1,(a>>1)&1,(a>>2)&1];if((b[0]^b[1]^b[2])!==charges[v])F.push(canon(o[v].map((x,j)=>b[j]?-x:x)))}
    return {n:6,F};
  }
  function cube(){let F=[];for(let a=0;a<8;a++)F.push(canon([1,2,3].map((x,j)=>((a>>j)&1)?-x:x)));return {n:3,F}}
  function php(p,h){let F=[];let x=(i,j)=>i*h+j+1;for(let i=0;i<p;i++)F.push(Array.from({length:h},(_,j)=>x(i,j)));for(let j=0;j<h;j++)for(let i=0;i<p;i++)for(let k=i+1;k<p;k++)F.push(canon([-x(i,j),-x(k,j)]));return {n:p*h,F}}
  function make(F,n){
    const m=F.length,records=F.map((_,i)=>({id:"S"+i,kind:"SOURCE",source:i,parents:[],mask:[i],charge:0}));let layer=records.map(r=>r.id),uid=0;
    while(layer.length>2){let nxt=[];for(let k=0;k<layer.length;k+=2){if(k+1===layer.length){nxt.push(layer[k]);continue}let a=records.find(r=>r.id===layer[k]),b=records.find(r=>r.id===layer[k+1]);let id="P"+uid++;records.push({id,kind:"MERGE",parents:[a.id,b.id],mask:[...new Set([...a.mask,...b.mask])].sort((x,y)=>x-y),charge:1});nxt.push(id)}layer=nxt}
    ok(layer.length===2,"two final roots");
    let pa=records.find(r=>r.id===layer[0]),pb=records.find(r=>r.id===layer[1]);
    let mask=[...new Set([...pa.mask,...pb.mask])].sort((x,y)=>x-y),table=[];
    for(let a=0;a<2**n;a++){let i=mask.find(i=>!satClause(F[i],a));if(i===undefined)throw Error("SAT source cannot have EXH_BOTTOM certificate");table.push(i)}
    records.push({id:"E",kind:"EXH_BOTTOM",parents:[pa.id,pb.id],mask,charge:1,table,claim:"BOTTOM"});
    return {n,source:F,records,summary:{source:m,paid:m-1,rows:2**n}};
  }
  function verify(packet,extern){
    ok(JSON.stringify(packet.source)===JSON.stringify(extern),"external signed source mismatch");
    let {n,source:F,records}=packet,m=F.length;
    ok(Number.isInteger(n)&&n>=1&&n<=20,"finite runner bound");ok(m>=2&&records.length===2*m-1,"source/node cardinality");
    let idx=new Map(),paid=0;
    for(let j=0;j<records.length;j++){
      let r=records[j];ok(typeof r.id==="string"&&!idx.has(r.id),"fresh record ID");
      if(j<m){ok(r.kind==="SOURCE"&&r.source===j&&r.id==="S"+j&&r.charge===0,"authenticated SOURCE");
        ok(Array.isArray(r.parents)&&r.parents.length===0,"SOURCE parent");ok(JSON.stringify(r.mask)===JSON.stringify([j]),"source mask")}
      else{
        ok(r.kind===(j===records.length-1?"EXH_BOTTOM":"MERGE")&&r.charge===1,"rule charge/kind");
        ok(Array.isArray(r.parents)&&r.parents.length===2&&r.parents[0]!==r.parents[1]&&r.parents.every(x=>idx.has(x)),"chronological two parents");
        let a=idx.get(r.parents[0]),b=idx.get(r.parents[1]),U=[...new Set([...a.mask,...b.mask])].sort((x,y)=>x-y);
        ok(JSON.stringify(r.mask)===JSON.stringify(U),"exact source ancestry mask");
        paid++;
        if(r.kind==="EXH_BOTTOM"){
          ok(r.claim==="BOTTOM"&&JSON.stringify(U)===JSON.stringify([...Array(m).keys()]),"complete discharged source obligation");
          ok(Array.isArray(r.table)&&r.table.length===2**n,"complete assignment table");
          for(let t=0;t<2**n;t++){let i=r.table[t];ok(Number.isInteger(i)&&U.includes(i)&&!satClause(F[i],t),"false clause witness at assignment "+t)}
        }else{ok(!("table" in r),"no illicit semantic evidence on MERGE")}
      }
      idx.set(r.id,r);
    }
    ok(packet.summary.source===m&&packet.summary.paid===paid&&packet.summary.rows===2**n,"exact accounting");
    return {paid,source:m,rows:2**n,bytes:JSON.stringify(packet).length};
  }
  const specs=[["cube3",cube()],["odd_K4",k4([1,0,0,0])],["PHP_3_2",php(3,2)],["PHP_4_3",php(4,3)]], cases=[],certs={};
  for(let [name,{n,F}] of specs){
    ok(models(F,n)===0,"UNSAT reference "+name);
    let P=make(F,n),v=verify(P,F),dels=F.map((_,i)=>models(F.filter((_,j)=>i!==j),n));
    ok(dels.every(x=>x>0),"indispensable source control "+name);
    cases.push({name,n,clauses:F.length,models:0,minDeletionModels:Math.min(...dels),maxDeletionModels:Math.max(...dels),paid:v.paid,assignmentWitnesses:v.rows,certificateBytes:v.bytes,logicalSpanAtMost:Math.ceil(Math.log2(F.length)),workFormulaMatches:v.paid===F.length-1});
    certs[name]=P;
  }
  const bad=[];
  function hostile(label,packet,external){let failure="";try{verify(packet,external)}catch(e){failure=String(e.message)}ok(!!failure,"hostile must reject "+label);bad.push({label,rejected:true,reason:failure})}
  const base=certs.odd_K4,clone=x=>JSON.parse(JSON.stringify(x));
  {let x=clone(base);x.records[0].source=1;hostile("forged_SOURCE_id",x,base.source)}
  {let x=clone(base);x.source[0][0]*=-1;hostile("source_external_mismatch",x,base.source)}
  {let x=clone(base);x.records.at(-1).table.pop();hostile("truncated_full_table",x,base.source)}
  {let x=clone(base),t=x.records.at(-1);t.table[0]=x.source.findIndex(c=>satClause(c,0));hostile("falsified_row_certificate",x,base.source)}
  {let x=clone(base);x.records.at(-1).mask.pop();hostile("omitted_ancestry",x,base.source)}
  {let x=clone(base);x.records.at(-1).parents[0]="E";hostile("cyclic_producer_reference",x,base.source)}
  {let x=clone(base);x.records[x.source.length+1].id=x.records[x.source.length].id;hostile("duplicate_paid_identity",x,base.source)}
  {let x=clone(base);x.records.at(-1).charge=0;hostile("zero_paid_terminal",x,base.source)}
  {let x=clone(base);x.summary.paid--;hostile("summary_cost_forgery",x,base.source)}
  {let x=clone(base);x.records.splice(x.source.length,0,{id:"X",kind:"FREE",parents:[],mask:[],charge:0});hostile("unauthorized_free_rule",x,base.source)}
  const sat=k4([0,0,0,0]);ok(models(sat.F,sat.n)===8,"even_K4_is_SAT");
  let satRejected=false;try{make(sat.F,sat.n)}catch(e){satRejected=true}ok(satRejected,"SAT builder must reject");
  {let x=clone(base);x.source=sat.F;x.records=x.records.map(r=>r);hostile("SAT_even_K4_replay",x,sat.F)}
  return {theorem:"hypothetical evidence-explicit two-premise calculus: for every UNSAT CNF with m>=2, optimal paid work is m-1; verifier polynomial in entire certificate bytes",checker:"deterministic pure JavaScript; exact signed source; chronological binary parents; all 2^n assignment rows; zero uncharged SAT-oracle calls",cases,hostile:bad,satControls:{even_K4_models:8,even_K4_builder_rejected:satRejected},checks,certificates:certs,limitations:"NOT an authenticated R_mix341 opcode; witness table can be exponential in input size; finite test n<=12; OS Node subprocess not executed in this run"};
}
console.log(JSON.stringify(run(),null,2));
