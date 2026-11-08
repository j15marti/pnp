"use strict";
/* LSPV-4/489. A stand-alone V8/Node verifier for canonical fixed-record guard
   self-closure, old-format rejection and explicit second-layer saturation.
   Host program only; NOT a native FLMV instruction-level run. */
let checks=0,queries=0,bad=0,second=0;
function ok(x,s){if(!x)throw Error(s);checks++}
function B(n,m){return Math.ceil(Math.log2(128*(n+m+3)))}
function bin(n,b){if(n<0||!Number.isSafeInteger(n)||n>=2**b)throw Error("overflow");return n.toString(2).padStart(b,"0")}
function pack(n,F){let m=F.length,b=B(n,m);if(n>3*m+3)throw Error("n-limit");
 let s="1".repeat(b)+"0"+bin(n,b)+bin(m,b);
 for(const c of F){if(c.length>3)throw Error("width");
  for(let k=0;k<3;k++){const l=c[k]||0;
   if(l&&Math.abs(l)>n)throw Error("id");
   s+=l?"1"+(l<0?"1":"0")+bin(Math.abs(l),b):"00"+bin(0,b)}
 }return s;
}
function parse(s){if(!/^[01]+$/.test(s))throw Error("alphabet");
 const b=s.indexOf("0");if(b<1||b>40||s.length<3*b+1)throw Error("width");
 const n=parseInt(s.slice(b+1,2*b+1),2),m=parseInt(s.slice(2*b+1,3*b+1),2);
 if(b!==B(n,m)||n>3*m+3||s.length!==3*b+1+3*m*(b+2))throw Error("header/length");
 let C=[],p=3*b+1;
 for(let j=0;j<m;j++){let c=[],absent=false;
  for(let k=0;k<3;k++){let pr=s[p++],neg=s[p++],id=parseInt(s.slice(p,p+b),2);p+=b;
   if(pr==="0"){if(neg!=="0"||id)throw Error("absent");absent=true}
   else{if(pr!=="1"||absent||id<1||id>n)throw Error("literal");c.push(neg==="1"?-id:id)}
  }C.push(c)}
 return {n,m,b,C,s};
}
function normalize(c,j,r){let map=new Map(),taut=false;
 for(let l of c){let id=Math.abs(l),sg=Math.sign(l);
  if(map.has(id)&&map.get(id)!==sg)taut=true;map.set(id,sg)}
 const p=[0,1,2].map(k=>4*(3*j+1+k)+1);
 if(taut)return p;
 const x=[...map].map(([v,sg])=>4*v*sg);
 if(!x.length)return p.map((v,k)=>(r>>k)&1?-v:v);
 if(x.length===1&&r<4)return [x[0],(r>>1)&1?-p[0]:p[0],(r&1)?-p[1]:p[1]];
 if(x.length===2&&r<2)return [x[0],x[1],r?-p[0]:p[0]];
 if(x.length===3&&r===0)return x;
 return p;
}
function clause(v,i){let j=Math.floor(i/16),r=Math.floor((i%16)/2),h=i%2;
 let c=normalize(v.C[j],j,r),a=4*(8*j+r+1)+2;
 return h===0?[c[0],c[1],a]:[-a,c[2],3];
}
function spec(v){let m=v.m,mo=16*m,no=m?Math.max(4*v.n,12*m+1,32*m+2,3):3;
 let bo=B(no,mo),len=3*bo+1+3*mo*(bo+2);
 ok(no<=3*mo+3,"output variable bound");
 return {mo,no,bo,len};
}
function material(v){let d=spec(v),C=Array.from({length:d.mo},(_,i)=>clause(v,i));return pack(d.no,C)}
function bit(v,i){let d=spec(v);if(i<0||i>=d.len)return null;queries++;
 let b=d.bo;if(i<b)return "1";if(i===b)return "0";
 if(i<=2*b)return bin(d.no,b)[i-b-1];if(i<=3*b)return bin(d.mo,b)[i-2*b-1];
 let t=i-(3*b+1),rec=Math.floor(t/(3*(b+2))),sub=t%(3*(b+2)),k=Math.floor(sub/(b+2)),z=sub%(b+2),l=clause(v,rec)[k];
 return z===0?"1":z===1?(l<0?"1":"0"):bin(Math.abs(l),b)[z-2];
}
function legacy(v){let b=v.b,m=v.m,no=Math.max(4*v.n,12*m+5,32*m+6,3);
 let s=bin(no,b)+bin(16*m,b);for(let i=0;i<16*m;i++)for(let l of clause(v,i))s+="1"+(l<0?"1":"0")+bin(Math.abs(l),b);return s;
}
function truth(l,a){let z=!!a[Math.abs(l)];return l<0?!z:z}
function sat(c,a){return c.some(l=>truth(l,a))}
function witness(F){let n=Math.max(1,...F.flat().map(Math.abs)),v1=parse(material(parse(pack(n,F))));
 let W={};for(let i=1;i<=v1.n;i++)W[4*i]=false;
 W[12]=true;for(let r=0;r<8*F.length;r++)W[4*(4*(r+1)+2)]=true;
 for(let j=0;j<v1.m;j++)for(let k=0;k<3;k++)W[4*(3*j+1+k)+1]=true;
 for(let r=0;r<8*v1.m;r++){let c=normalize(v1.C[r>>3],r>>3,r%8);
  W[4*(r+1)+2]=!(truth(c[0],W)||truth(c[1],W))}
 W[3]=false;let d=spec(v1);for(let i=0;i<d.mo;i++){ok(sat(clause(v1,i),W),"second layer counterexample");second++}
 return {source_m:v1.m,second_m:d.mo};
}
let seed=489;function rnd(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
let cases=[{n:0,F:[]},{n:3,F:[]},{n:1,F:[[]]},{n:1,F:[[1]]},{n:1,F:[[1,-1]]},{n:3,F:[[1,2,3]]},{n:3,F:[[-1,2,3],[-2,2,1]]},{n:6,F:[[4,-4],[5,6,6]]}];
for(let i=0;i<128;i++){let m=rnd()%3,n=1+rnd()%(3*m+3),F=[];
 for(let j=0;j<m;j++){let c=[],k=rnd()%4;for(let a=0;a<k;a++){let id=1+rnd()%n;c.push(rnd()%2?id:-id)}F.push(c)}
 cases.push({n,F})}
let samples=[];
for(let t of cases){let v=parse(pack(t.n,t.F)),o=material(v),u=parse(o),d=spec(v);
 ok(u.m===d.mo&&u.n===d.no,"closed parser");
 for(let i=0;i<o.length;i++)ok(bit(v,i)===o[i],"bit mismatch");
 ok(bit(v,-1)===null&&bit(v,o.length)===null,"blank");
 let rejected=false;try{parse(legacy(v))}catch(e){rejected=true}ok(rejected,"old format unexpectedly valid");
 if(samples.length<8)samples.push({n:v.n,m:v.m,N:v.s.length,n2:d.no,m2:d.mo,M:o.length,legacy_rejected:rejected});
 for(let x of [o+"0",o.slice(0,-1),"x"+o.slice(1)]){let fail=false;try{parse(x)}catch(e){fail=true}ok(fail,"accepted corruption");bad++}
}
let s0=witness([[]]),s1=witness([[1]]);
globalThis.lspv489={run:"LSPV-4/489",status:"COMPUTATIONAL",sources:cases.length,guard_parses:cases.length,
 bit_queries:queries,malformed_rejections:bad,second_guard_checked_clauses:second,
 second_witnesses:[s0,s1],assertions:checks,samples,
 qualification:"Source-grammar closure ONLY. Iterated one-port SAT signal collapses; no universal Phi(A); host V8 not a native FLMV machine."};
if(typeof console!=="undefined"&&typeof module!=="undefined"&&module?.parent==null)console.log(JSON.stringify(globalThis.lspv489,null,2));
