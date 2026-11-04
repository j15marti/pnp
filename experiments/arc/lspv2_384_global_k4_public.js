// LSPV-2/384 complete K4 guarded proof composer, strict RES + paid conservative AND2 only.
'use strict';
const fs=require('fs'),crypto=require('crypto');
const local=process.argv[3]||'results/raw/arc/2026-11-04_0037_LSPV2_GUARDED_PARITY_ER383_raw.json';
const output=process.argv[2]||'lspv2_384_global_k4_raw.json';
const bytes=fs.readFileSync(local);
const templates=Object.fromEntries(JSON.parse(bytes).cases.map(x=>[x.charge,x]));
const cn=a=>{const s=[...new Set(a)];if(s.includes(0)||s.some(x=>s.includes(-x)))return null;return s.sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:-1));};
const lines=[],seen=new Map(),key=x=>JSON.stringify(x);let paidRes=0;
function add(kind,c,extra={}){c=cn(c);if(!c)throw Error('invalid clause');const k=key(c);if(seen.has(k))return seen.get(k);const i=lines.length;lines.push({kind,c,...extra});seen.set(k,i);if(kind==='res')paidRes++;return i;}
function res(i,j,p,phase){const A=lines[i].c,B=lines[j].c;if(!(A.includes(p)&&B.includes(-p))&&!(A.includes(-p)&&B.includes(p)))throw Error('pivot');const r=cn([...A.filter(x=>Math.abs(x)!==p),...B.filter(x=>Math.abs(x)!==p)]);return r===null?null:add('res',r,{parents:[i,j],pivot:p,phase});}
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],charges=[1,0,0,0],rows=[],defs=[],goals=[],sources=[];
for(let v=0;v<4;v++){
 const edges=E.map((e,i)=>e.includes(v)?i+1:null).filter(Boolean),tm=templates[charges[v]],m={1:edges[0],2:edges[1],3:edges[2],4:7};
 for(let j=5;j<=10;j++)m[j]=8+6*v+j-5;
 const lit=x=>Math.sign(x)*m[Math.abs(x)],gates=tm.gates.map(g=>({out:m[g.output],inputs:g.inputs.map(lit)})),ids=[];
 tm.clauses.forEach((q,i)=>{const c=q.c.map(lit);let id;
   if(q.kind==='source'){id=add('source',c,{vertex:v});sources.push(id);}
   else if(q.kind==='view'){id=add('view',c,{vertex:v,gate:q.gate,view:q.view});defs.push(id);}
   else if(q.kind==='res'){id=res(ids[q.parents[0]],ids[q.parents[1]],m[q.pivot],'local');if(id===null)throw Error('local tautology');}
   else throw Error('rule');ids[i]=id;
 });
 const goal=ids[tm.goal_id];goals.push(goal);rows.push({vertex:v,charge:charges[v],edges,gates,goal});
}
let active=new Set([...defs,...goals]),steps=[];
for(const p of [...Array.from({length:24},(_,i)=>31-i),1,2,3,4,5,6]){
 const pos=[...active].filter(i=>lines[i].c.includes(p)),neg=[...active].filter(i=>lines[i].c.includes(-p)),added=[];
 for(const i of pos)for(const j of neg){const k=res(i,j,p,'elim');if(k!==null)added.push(k);}
 for(const i of [...pos,...neg])active.delete(i);for(const i of added)active.add(i);
 steps.push({pivot:p,positive:pos.length,negative:neg.length,added:added.length,active:active.size});
}
const target=seen.get(key([-7]));if(target===undefined)throw Error('missing guarded literal');
const unit=add('source',[7],{vertex:'guard'}),end=res(target,unit,7,'finish');
if(end!==lines.length-1||lines[end].c.length)throw Error('not refuted');
const d={id:'LSPV2-384',model:'strict binary Resolution + paid conservative signed AND2 defs (the R_mix341 fragment E_AND2)',scope:'one concrete K4 graph, upper proof only, NOT shortest proof',graph_edges:E,charges,guard:7,rows,sources,local_383_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),elimination_pivots:steps,proof:lines,target_unit:target,last_id:end,paid_AND2:24,paid_resolution:paidRes,total_paid:24+paidRes,source_clauses:17,encoded_proof_bytes:0};
while(true){const s=JSON.stringify(d)+'\n',n=Buffer.byteLength(s);if(n===d.encoded_proof_bytes){fs.writeFileSync(output,s);break;}d.encoded_proof_bytes=n;}
console.log(JSON.stringify({path:output,lines:lines.length,paid:d.total_paid,bytes:d.encoded_proof_bytes}));