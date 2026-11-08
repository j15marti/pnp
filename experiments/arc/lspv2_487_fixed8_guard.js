"use strict";
/* LSPV-2/487. Fixed-eight-clause proper-3 normalization and guarded port.
   Reproducible finite JS reference, not a native indexed-FLMV execution.
   node experiments/arc/lspv2_487_fixed8_guard.js */
const assert=require("assert");
let checks=0; function ok(x,msg){assert.ok(x,msg);checks++}
function litValue(l,a){return l>0?!!a[Math.abs(l)]:!a[Math.abs(l)]}
function evalClause(c,a){return c.some(l=>litValue(l,a))}
function evalCNF(f,a){return f.every(c=>evalClause(c,a))}
function simp(c){let p=new Map();for(const l of c){const v=Math.abs(l),s=Math.sign(l);if(p.has(v)&&p.get(v)!==s)return null;p.set(v,s)}return Array.from(p,([v,s])=>v*s)}
function normOne(c,j,r){
  const x=simp(c),p=[0,1,2].map(k=>4*(3*j+1+k)+1),fill=p.slice();
  if(x===null)return fill;
  const y=x.map(l=>Math.sign(l)*4*Math.abs(l));
  if(y.length===0)return p.map((v,k)=>((r>>k)&1)?-v:v);
  if(y.length===1&&r<4)return [y[0],((r>>1)&1)?-p[0]:p[0],(r&1)?-p[1]:p[1]];
  if(y.length===2&&r<2)return [y[0],y[1],r?-p[0]:p[0]];
  if(y.length===3&&r===0)return y;
  return fill;
}
function normalized(F){return F.flatMap((c,j)=>Array.from({length:8},(_,r)=>normOne(c,j,r)))}
function guardPair(c,r){const a=4*(r+1)+2,z=3;return [[c[0],c[1],a],[-a,c[2],z]]}
function guarded(F){return normalized(F).flatMap((c,r)=>guardPair(c,r))}
function proper(c){return c.length===3&&c.every(l=>l!==0)&&new Set(c.map(Math.abs)).size===3}
function boolAssignments(ids,fn){const a={};for(let v=0;v<2**ids.length;v++){ids.forEach((x,k)=>a[x]=Boolean(v&(1<<k)));fn(a)}}
function B(n,m){return Math.ceil(Math.log2(128*(n+m+3)))}
function bin(v,b){return v.toString(2).padStart(b,"0")}
function encodeSource(n,F){
  const b=B(n,F.length);
  return "1".repeat(b)+"0"+bin(n,b)+bin(F.length,b)+F.map(c=>[0,1,2].map(k=>{
    if(k>=c.length)return "00"+bin(0,b);
    const l=c[k];return "1"+(l<0?"1":"0")+bin(Math.abs(l),b)
  }).join("")).join("");
}
function validatedSource(src){
  if(/[^01]/.test(src))throw Error("alphabet");
  const b=src.indexOf("0");if(b<=0||b>Math.ceil(Math.log2(src.length))+10)throw Error("width");
  if(src.length<3*b+1)throw Error("short header");
  const n=parseInt(src.slice(b+1,2*b+1),2),m=parseInt(src.slice(2*b+1,3*b+1),2);
  if(b!==B(n,m)||n>3*m+3||src.length!==3*b+1+3*m*(b+2))throw Error("headers/length");
  for(let j=0;j<m;j++)readClause(src,b,n,m,j);
  return {n,m,b,src};
}
function readClause(src,b,n,m,j){
  const c=[];let missing=false;
  for(let k=0;k<3;k++){
    const off=3*b+1+(3*j+k)*(b+2),pr=src[off],sg=src[off+1],id=parseInt(src.slice(off+2,off+b+2),2);
    if(pr==="0"){if(sg!=="0"||id!==0)throw Error("bad absent slot");missing=true;continue}
    if(pr!=="1"||missing||id===0||id>n)throw Error("bad literal");
    c.push(sg==="1"?-id:id);
  }
  return c;
}
function outHeader(n,m){return Math.max(4*n,4*(3*m+1)+1,4*(8*m+1)+2,3)}
function virtualLength(n,m){return 2*B(n,m)+16*m*3*(B(n,m)+2)}
function virtualBit(v,index){
  const {n,m,b,src}=v,out=virtualLength(n,m);if(index<0||index>=out)throw Error("bad bit index");
  if(index<2*b){const num=index<b?outHeader(n,m):16*m;return bin(num,b)[index%b]}
  const recBits=3*(b+2),rr=index-2*b,rec=Math.floor(rr/recBits);
  const sub=rr%recBits,pos=Math.floor(sub/(b+2)),within=sub%(b+2);
  const j=Math.floor(rec/16),r=Math.floor((rec%16)/2),half=rec%2;
  const c=normOne(readClause(src,b,n,m,j),j,r);
  const lit=guardPair(c,8*j+r)[half][pos];
  return within===0?"1":within===1?(lit<0?"1":"0"):bin(Math.abs(lit),b)[within-2];
}
function encodeGuard(n,F){
  const b=B(n,F.length),g=guarded(F);
  return bin(outHeader(n,F.length),b)+bin(g.length,b)+g.flatMap(c=>c.map(l=>"1"+(l<0?"1":"0")+bin(Math.abs(l),b))).join("");
}
let local=0,whole=0,probes=0,negatives=0;
const cases=[[],[1],[-1],[1,1],[1,-1],[1,2],[-2,2,3],[-1,-2,3],[1,-2,3],[1,2,3],[1,-1,2],[-3,-3]];
for(const c of cases){for(const j of [0,2]){
  const ids=[...new Set(c.map(Math.abs))].filter(x=>x>0);
  boolAssignments(ids,a=>{
    const p=[0,1,2].map(k=>4*(3*j+1+k)+1),q=Array.from({length:8},(_,r)=>normOne(c,j,r));
    ok(q.every(proper),"not proper");let exists=false;
    boolAssignments(p,ap=>{
      const b={...ap};ids.forEach(v=>b[4*v]=a[v]);
      if(evalCNF(q,b))exists=true
    });
    ok(exists===evalClause(c,a),"local equivalence");local++;
  })
}}
let seed=487;function random(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
const fset=[[],[[1]],[[1,-1]],[[1,2],[-1]],[[1,2,3],[-1,-2,-3]],[[]]];
for(let q=0;q<64;q++){const n=1+random()%3,m=random()%3,F=[];
  for(let j=0;j<m;j++){const c=[];for(let k=0;k<(random()%4);k++){const v=1+random()%n;c.push((random()%2)?v:-v)}F.push(c)}fset.push(F)}
for(const F of fset){
  const n=Math.max(1,...F.flat().map(Math.abs)),m=F.length;
  const ns=normalized(F),g=guarded(F),src=encodeSource(n,F),v=validatedSource(src),out=encodeGuard(n,F);
  ok(ns.length===8*m&&g.length===16*m,"count");
  ok(ns.every(proper)&&g.every(proper),"proper");
  ok(out.length===virtualLength(n,m),"output length");
  const ids=Array.from({length:n},(_,i)=>i+1);
  if(m<=2&&n<=3){
    boolAssignments(ids,a=>{
      let ex=false;const aids=Array.from({length:3*m},(_,i)=>4*(i+1)+1);
      boolAssignments(aids,ap=>{const b={...ap};ids.forEach(k=>b[4*k]=a[k]);if(evalCNF(ns,b))ex=true});
      ok(ex===evalCNF(F,a),"global normalization");whole++;
    })
  }
  for(let i=0;i<out.length;i++){ok(virtualBit(v,i)===out[i],"virtual bit");probes++}
  const bads=[src+"0",src.slice(0,-1),src.slice(0,3*v.b+1)+"x"+src.slice(3*v.b+2)];
  if(m){const s=src.split("");s[3*v.b+1]="0";s[3*v.b+2]="1";bads.push(s.join(""))}
  for(const bad of bads){let rejected=false;try{validatedSource(bad)}catch(e){rejected=true}ok(rejected,"malformed allowed");negatives++}
}
const edge=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let tSat=0,tUnsat=0;
for(let charge=0;charge<16;charge++){
  let F=[];for(let v=0;v<4;v++){
    const incident=edge.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
    for(let mask=0;mask<8;mask++){
      const parity=(mask&1)^((mask>>1)&1)^((mask>>2)&1);
      if(parity!==((charge>>v)&1))F.push(incident.map((id,k)=>((mask>>k)&1)?-id:id))
    }
  }
  ok(F.length===16&&F.every(proper),"K4 source");
  let sat=false;for(let ass=0;ass<64;ass++){const a={};for(let k=1;k<=6;k++)a[k]=!!(ass&(1<<(k-1)));if(evalCNF(F,a))sat=true}
  ok(sat===((charge.toString(2).split("1").length-1)%2===0),"K4 parity");
  sat?tSat++:tUnsat++;
  const g=guarded(F);ok(g.length===256&&g.every(proper),"K4 guard")
}
ok(tSat===8&&tUnsat===8,"K4 counts");
const result={run:"LSPV-2/487",status:"COMPUTATIONAL",seed:487,checks,local_cases:local,global_assignments:whole,bit_probes:probes,malformed_rejections:negatives,K4:{SAT:tSat,UNSAT:tUnsat},claim:"fixed8 projection and virtual bit checks; not native FLMV"};
if(require.main===module)console.log(JSON.stringify(result,null,2));
module.exports={normOne,normalized,guarded,encodeSource,validatedSource,virtualBit,encodeGuard,result};
