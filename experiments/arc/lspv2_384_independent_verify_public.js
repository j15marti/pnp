// LSPV-2/384 independent verifier. Does not import producer or prior /383 templates.
'use strict';
const fs=require('fs'),d=JSON.parse(fs.readFileSync(process.argv[2]||'lspv2_384_global_k4_raw.json','utf8'));let n=0;
const ok=(x,s)=>{n++;if(!x)throw Error(s||String(n));};
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function cn(a){ok(Array.isArray(a));const b=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?1:-1));for(const x of b)ok(Number.isInteger(x)&&x!==0&&!b.includes(-x));return b;}
function src(es,ch){let o=[];for(let a=0;a<8;a++)if(((a&1)^((a>>1)&1)^((a>>2)&1))!==ch)o.push(cn(es.map((e,j)=>a>>j&1?-e:e).concat([-7])));return o;}
function check(D){ok(eq(D.graph_edges,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]));ok(eq(D.charges,[1,0,0,0]));ok(D.guard===7&&D.rows.length===4);
const sources=new Map(),views=new Map();
for(let v=0;v<4;v++){const r=D.rows[v],es=D.graph_edges.map((e,i)=>e.includes(v)?i+1:null).filter(Boolean);
ok(r.vertex===v&&r.charge===D.charges[v]&&eq(es,r.edges));ok(r.gates.length===6);
for(const c of src(es,D.charges[v]))sources.set(JSON.stringify(c),v);
for(let j=0;j<6;j++){const g=r.gates[j];ok(g.out===8+6*v+j&&g.inputs.length===2);
const [a,b]=g.inputs;ok(Math.abs(a)<g.out&&Math.abs(b)<g.out);
[[-g.out,a],[-g.out,b],[g.out,-a,-b]].forEach((c,i)=>views.set(JSON.stringify([v,j,i]),cn(c)));}}
sources.set('[7]','guard');
let paid=0,nviews=0;const used=new Set(),ss=new Set();
for(let i=0;i<D.proof.length;i++){const q=D.proof[i],c=cn(q.c);ok(eq(c,q.c));
if(q.kind==='source'){ok(sources.get(JSON.stringify(c))===q.vertex);ss.add(JSON.stringify(c));}
else if(q.kind==='view'){ok(eq(c,views.get(JSON.stringify([q.vertex,q.gate,q.view]))));nviews++;used.add(q.vertex*6+q.gate);}
else if(q.kind==='res'){const [a,b]=q.parents||[];ok(Number.isInteger(a)&&Number.isInteger(b)&&a>=0&&b>=0&&a<i&&b<i);
const A=D.proof[a].c,B=D.proof[b].c,p=q.pivot;ok((A.includes(p)&&B.includes(-p))||(A.includes(-p)&&B.includes(p)));
ok(eq(c,cn(A.filter(x=>Math.abs(x)!==p).concat(B.filter(x=>Math.abs(x)!==p)))));paid++;}
else throw Error('unrecognized proof rule');}
ok(ss.size===17&&nviews===72&&used.size===24);
for(let v=0;v<4;v++)ok(eq(D.proof[D.rows[v].goal].c,cn([-7,(v===0?-1:1)*(13+6*v)])));
ok(eq(D.proof[D.target_unit].c,[-7]));ok(D.last_id===D.proof.length-1&&eq(D.proof[D.last_id].c,[]));
ok(D.paid_resolution===paid&&paid===104&&D.paid_AND2===24&&D.total_paid===128);
ok(D.proof.length===193&&D.source_clauses===17);
ok(D.encoded_proof_bytes===Buffer.byteLength(JSON.stringify(D)+'\n'));
// Source-level truth controls, plus gate-rail semantics on every one of the 64 original edge assignments.
for(let a=0;a<64;a++)for(let v=0;v<4;v++){const row=D.rows[v],bits=row.edges.map(k=>(a>>(k-1))&1),p=bits[0]^bits[1]^bits[2];
const val={};row.edges.forEach((e,j)=>val[e]=bits[j]);
for(const g of row.gates){const l=x=>x>0?val[x]:1-val[-x];val[g.out]=l(g.inputs[0])&l(g.inputs[1]);}
ok(val[13+6*v]===1-p);for(const c of src(row.edges,D.charges[v]))ok(c.includes(-7));}
for(let v=0;v<4;v++)for(const c of src(D.rows[v].edges,0))ok(c.some(x=>x<0&&x>=-6));
return {lines:D.proof.length,paid:paid+24,bytes:D.encoded_proof_bytes};}
const stats=check(d),original=n;
function corrupt(f){const x=structuredClone(d);f(x);let rejected=false;try{check(x);}catch(e){rejected=true;}ok(rejected,'mutation accepted');}
const ri=d.proof.findIndex(z=>z.kind==='res');
corrupt(x=>x.proof[ri].pivot=99);corrupt(x=>x.proof[ri].parents[0]=999);
corrupt(x=>x.proof[ri].c.push(99));corrupt(x=>x.proof[0].c[0]*=-1);
corrupt(x=>x.rows[0].gates[0].inputs[0]*=-1);corrupt(x=>x.total_paid++);
console.log(JSON.stringify({...stats,checks:original,total_checks:n,corruptions_rejected:6,status:'PASS'}));