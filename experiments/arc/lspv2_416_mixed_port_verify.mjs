#!/usr/bin/env node
// LSPV-2/416 independently validates mixed grammar node semantics and oriented pivots.
// Usage: node experiments/arc/lspv2_416_mixed_port_verify.mjs
import fs from "node:fs";
const data=JSON.parse(fs.readFileSync("results/raw/arc/2026-11-05_0512_LSPV2_MIXED_DEF_PORT416.json","utf8"));
const D=data.complete_certificate;
let checks=0;
function ok(x,msg){checks++;if(!x)throw Error(msg)}
const norm=c=>[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const clause=(c,e)=>c.some(x=>e[Math.abs(x)]===Number(x>0));
const truth=(r,e)=>r.truth.reduce((v,b,k)=>v||Boolean(b&&r.support.every((s,j)=>e[s]===((k>>j)&1))),false);
function evalr(r,e){if(r.kind==="clause")return clause(r.clause,e);if(r.kind==="factor")return truth(r,e);return r.mask.reduce((v,k)=>v^e[k],0)===r.rhs;}
const sourceLines=data.raw_dimacs.split("\n").filter(l=>l&&!l.startsWith("c"));
ok(sourceLines[0]==="p cnf 2 4","header");
const src=sourceLines.slice(1).map(l=>{const t=l.trim().split(/\s+/).map(Number);ok(t.at(-1)===0,"unterminated");return t.slice(0,-1)});
ok(eq(src.map(norm),D.source.clauses),"source ids/order");
const E=Array.from({length:16},(_,k)=>Object.fromEntries([1,2,3,4].map(v=>[v,(k>>(v-1))&1])));
const views=new Map(src.map((c,i)=>["S"+i,{kind:"clause",clause:norm(c)}]));
const kref=(r)=>"src" in r?"S"+r.src:"N"+r.node+":"+r.view+("facet" in r?":"+r.facet:"");
function get(r,i){if("node" in r)ok(r.node<i,"forward ref");const key=kref(r);ok(views.has(key),"unavailable "+key);return views.get(key)}
function put(i,view,type,facet){const key="N"+i+":"+(type??view.kind)+(facet===undefined?"":":"+facet);ok(!views.has(key),"duplicate");views.set(key,view)}
function facets(r){const [a,b]=r.inputs, z=r.var, t=r.truth;let f=[];for(let av=0;av<2;av++)for(let bv=0;bv<2;bv++){let o=1-t[av|(bv<<1)];f.push(norm([av===0?a:-a,bv===0?b:-b,o===0?z:-z]));}return f;}
const consistent=E.filter(e=>D.nodes.filter(n=>n.rule==="DEF").every(n=>e[n.var]===n.truth[e[n.inputs[0]]|(e[n.inputs[1]]<<1)]));
ok(consistent.length===4,"unique extension");
function support(r){return r.kind==="clause"?[...new Set(r.clause.map(Math.abs))]:r.kind==="factor"?r.support:r.mask}
for(const n of D.nodes){const i=n.id;ok(i===D.nodes.indexOf(n),"bad index");
if(n.rule==="DEF"){for(const [j,c] of facets(n).entries()){const o={kind:"clause",clause:c};put(i,o,"clause",j);for(const e of consistent)ok(evalr(o,e),"invalid DEF facet")}}
else if(n.rule==="RES"){const a=get(n.left,i),b=get(n.right,i);ok(a.kind==="clause"&&b.kind==="clause","RES types");const p=n.pivot;let v=[];
if(a.clause.includes(p)&&b.clause.includes(-p))v.push(norm([...a.clause.filter(t=>t!==p),...b.clause.filter(t=>t!==-p)]));
if(a.clause.includes(-p)&&b.clause.includes(p))v.push(norm([...a.clause.filter(t=>t!==-p),...b.clause.filter(t=>t!==p)]));
ok(v.some(c=>eq(c,n.clause)),"not oriented RES");
const o={kind:"clause",clause:n.clause};for(const e of E)ok(!(evalr(a,e)&&evalr(b,e))||evalr(o,e),"RES unsound");put(i,o)}
else if(n.rule==="AND3"){const a=get(n.left,i),b=get(n.right,i),f={kind:"factor",...n.factor},z={kind:"affine",...n.affine};
const s=[...new Set([...support(a),...support(b)])].sort((x,y)=>x-y);
ok(eq(s,f.support)&&s.length<=3&&s.every(k=>k<=2),"AND3 source support");
for(const e of E){ok(evalr(f,e)===(evalr(a,e)&&evalr(b,e)),"AND3 wrong conjunction");ok(evalr(f,e)===evalr(z,e),"invalid affine annotation");}
put(i,f);put(i,z)}
else if(n.rule==="LOCAL"){const a=get(n.parent,i),b={kind:"clause",clause:n.out.clause};
ok(n.out.kind==="clause","LOCAL type");for(const e of E)ok(!evalr(a,e)||evalr(b,e),"LOCAL unsound");put(i,b)}
else if(n.rule==="GF2"){const a=get(n.left,i),b=get(n.right,i),z={kind:"affine",...n.affine};
ok(a.kind==="affine"&&b.kind==="affine","GF2 parents");
const m=a.mask.filter(v=>!b.mask.includes(v)).concat(b.mask.filter(v=>!a.mask.includes(v))).sort((x,y)=>x-y);
ok(eq(m,z.mask)&&z.rhs===(a.rhs^b.rhs),"GF2 wrong");
for(const e of E)ok(!(evalr(a,e)&&evalr(b,e))||evalr(z,e),"GF2 unsound");put(i,z)}
else throw Error("unknown rule")}
const end=get(D.final,D.nodes.length);ok(end.kind==="affine"&&eq(end.mask,[])&&end.rhs===1,"no contradiction");
const reached=new Set;
function walk(ref){if(!("node" in ref))return;let i=ref.node;if(reached.has(i))return;reached.add(i);for(const key of ["left","right","parent"])if(D.nodes[i][key])walk(D.nodes[i][key]);}
walk(D.final);ok(reached.size===D.nodes.length,"dead paid gate");
for(let k=0;k<4;k++){const e={1:k&1,2:(k>>1)&1};ok(!src.every(c=>clause(c,e)),"false UNSAT");}
ok(src.slice(0,2).every(c=>clause(c,{1:1,2:0})),"SAT control");
console.log(JSON.stringify({status:"PASS",assertions:checks,paid_nodes:reached.size,source_bytes:Buffer.byteLength(data.raw_dimacs)}));
