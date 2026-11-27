function experiment(S,mode){
 const ids=[...new Set(S.fs.flatMap(f=>f.vs))].sort((a,b)=>a-b),n=ids.length,ix=new Map(ids.map((x,i)=>[x,i])),C=1n<<BigInt(n),mask=C-1n,bits=ids.map((_,i)=>1n<<BigInt(i));
 let ops=0,pairs=0,scans=0,peak=0,trace=[],rank=0,probes=0,branches=0,units=0,branchOps=0,pairDirChecks=0,pairDirTests=0,pairDirections=0;
 const tick=()=>{if(++ops>10000000)throw Error("row cap")};
 const pivot=x=>{let y=x&mask;return y===0n?0n:y&-y};
 function canon(rows){let basis=new Map();for(let r of rows){for(const [p,v] of basis){tick();if(r&p)r^=v}const p=pivot(r);if(!p){if(r&C)return null;continue}for(const [q,v] of basis){tick();if(v&p)basis.set(q,v^r)}basis.set(p,r)}return [...basis].sort((a,b)=>a[0]<b[0]?-1:1).map(x=>x[1])}
 function localEq(words,f){if(!words.length)return null;let rr=[];for(let a=1;a<2**f.vs.length;a++){let v=w=>{let x=a&w,p=0;while(x){p^=1;x&=x-1}return p};let t=v(words[0]);if(words.every(w=>v(w)===t)){let q=t?C:0n;f.vs.forEach((x,i)=>{if(a>>i&1)q|=bits[ix.get(x)]});rr.push(q)}}return canon(rr)}
 function holds(eq,w,f){let a=0n;f.vs.forEach((x,i)=>{if(w>>i&1)a|=bits[ix.get(x)]});return eq.every(r=>{let q=r&a,s=0;while(q){s^=1;q&=q-1n}return s===Number(!!(r&C))})}
 let hull=[],bad=[];
 for(const f of S.fs){const e=localEq(f.ok,f);if(e===null)return {status:"UNSAT local"};hull.push(...e);let w=Array.from({length:2**f.vs.length},(_,i)=>i).filter(w=>holds(e,w,f)&&!f.ok.includes(w));if(w.length){const q=localEq(w,f);if(!q||Array.from({length:2**f.vs.length},(_,i)=>i).filter(i=>holds(q,i,f)).length!==w.length)throw Error("bad event not affine");bad.push(q)}}
 const ge=canon(hull);if(!ge)return {status:"UNSAT parity"};rank=ge.length;
 const reduc=r=>{for(const g of ge){tick();if(r&pivot(g))r^=g}return r};
 function unique(F){let m=new Map();for(const e of F)m.set(e.join(","),e);return [...m.values()]}
 let F=unique(bad.map(e=>canon(e.map(reduc))).filter(x=>x!==null));let initial=F.length;let free=bits.filter(b=>!ge.some(r=>pivot(r)===b));
 function project(e,b){let p=e.find(r=>r&b);if(!p)return e;return canon(e.filter(r=>r!==p).map(r=>r&b?r^p:r))}
 function step(F,b){let A=F.filter(e=>e.some(r=>r&b)),O=F.filter(e=>!e.some(r=>r&b));let out=[];for(let i=0;i<A.length;i++)for(let j=i+1;j<A.length;j++){pairs++;let a=canon([...A[i],...A[j].map(r=>r&b?r^C:r)]);if(a!==null){let p=project(a,b);if(p!==null)out.push(p)}}return {A,out,newF:unique([...O,...out])}}
 function cond(F,r){let p=pivot(r);return unique(F.map(e=>canon(e.map(a=>a&p?a^r:a))).filter(e=>e!==null))}
 function tree(F){if(++branches>100000)throw Error("branch cap");let unit=[];for(;;){if(F.some(e=>!e.length))return {unit,conflict:true};if(!F.length)throw Error("SAT witness");let e=F.find(e=>e.length===1);if(!e)break;let r=e[0]^C;unit.push(r.toString(16));units++;F=cond(F,r)}let count=new Map();for(const e of F)for(const r of e){let k=r&mask;count.set(k,(count.get(k)||0)+1)}let r=[...count].sort((a,b)=>b[1]-a[1]||(a[0]<b[0]?-1:1))[0][0];return{unit,split:r.toString(16),children:[tree(cond(F,r)),tree(cond(F,r^C))]}}
 let result={};try{if(mode!=="branch-only")for(;;){peak=Math.max(peak,F.length);if(F.some(e=>e.length===0)||!F.length)break;
 const supports=F.map(e=>e.reduce((a,b)=>a|(b&mask),0n));
 let freq=free.map(b=>{let count=0;for(const s of supports){scans++;if(s&b)count++}return[b,count]}).sort((a,b)=>a[1]-b[1]|| (a[0]<b[0]?-1:1));
 if(scans>20000000)throw Error("scan cap");
 let selected=null;for(const [b,k] of freq){if(k>3)break;probes++;let x=step(F,b);if(x.newF.length<=F.length){selected=[b,k,x];break}}
 if(!selected){let best=null;for(let i=0;i<free.length;i++)for(let j=i+1;j<free.length;j++){let a=free[i],b=free[j],k=0;pairDirTests++;for(const E of F){if(++pairDirChecks>10000000)throw Error('pair direction cap');if(E.some(r=>Boolean(r&a)!==Boolean(r&b)))k++;if(k>3)break}if(k<=3&&(!best||k<best[2]))best=[a,b,k]}if(!best){result.min=freq[0]?.[1];break}let [a,b,k]=best;F=unique(F.map(e=>canon(e.map(r=>r&b?r^a:r))));let x=step(F,a);if(x.newF.length>F.length)throw Error('nonexpansive');selected=[a,k,x,b];pairDirections++}
 let [b,k,x,d]=selected;trace.push([bits.indexOf(b),k,x.out.length,x.newF.length,...(d===undefined?[]:[bits.indexOf(d)])]);F=x.newF;free=free.filter(x=>x!==b);
 }
 if(F.some(e=>!e.length)){result.status="UNSAT";result.tree={conflict:true}}else if(mode==="eliminate-only")result.status="UNKNOWN";else{let before=ops;result.tree=tree(F);branchOps=ops-before;result.status="UNSAT"}
 }catch(e){result.status=String(e)}
 return {...result,n,rank,initial,remaining:F.length,free:free.length,steps:trace.length,pairs,ops,scans,probes,peak,branches,units,branchOps,pairDirChecks,pairDirTests,pairDirections,trace}
}
module.exports={experiment};
