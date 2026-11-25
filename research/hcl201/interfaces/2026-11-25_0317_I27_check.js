function run(rt,da){
const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};let checks=0;
function test(n,reg,cuts){
 // exact local singleton rank closure via affine equations on original coordinates
 let basis=new Map();function add(m,b){while(m){let p=31-Math.clz32(m);if(!basis.has(p)){basis.set(p,[m,b]);return 1}let [s,t]=basis.get(p);m^=s;b^=t}return b?-1:0}
 function reduce(m,b=0){for(let p of [...basis.keys()].sort((a,b)=>b-a))if(m>>p&1){let [s,t]=basis.get(p);m^=s;b^=t}return [m,b]}
 function form(o){let [a,b,c]=o.t, v=o.bad[0];return [[(1<<a)^(1<<b),(v^(v>>1))&1],[(1<<a)^(1<<c),(v^(v>>2))&1]].map(([s,t])=>reduce(s,t))}
 let contradiction=false, passes=0, inferred=0;
 function close(){let change;do{change=false;passes++;for(let o of reg){let [[a,b],[c,d]]=form(o);if((!a&&b)||(!c&&d)||(a===c&&b!==d))continue;if(!a&&!c){contradiction=true;return}if(!a||!c||a===c){let s=a||c,t=a?b:d;let u=add(s,t^1);if(u<0){contradiction=true;return}if(u){change=true;inferred++;break}}}}while(change)}
 close();for(let [m,b] of cuts){if(contradiction)break;let u=add(parseInt(m,16),b);if(u<0){contradiction=true;break}close()}if(!contradiction)close();
 let original=0, guarded=0,min=Infinity, hist={}, word=null, reference=[];
 for(let x=0;x<1<<n;x++){let e=0;for(let o of reg){let v=o.t.reduce((a,t,i)=>a|((x>>t&1)<<i),0);e+=o.bad.includes(v)}if(!e){original++;if(cuts.every(([m,b])=>parity(x&parseInt(m,16))===b))guarded++;else throw Error("invalid peer cut on actual model")}if(!contradiction&&[...basis.values()].every(([m,b])=>parity(x&m)===b)){reference.push([x,e]);if(e<min){min=e;word=x}}}
 if(contradiction){if(original)throw Error("bad closure");return {original,guarded,contradiction,passes,inferred}}
 let coeff=new Map();function inc(m,w){coeff.set(m,(coeff.get(m)||0)+w)}
 // 4 times violation indicator
 for(let o of reg){let [[a,b],[c,d]]=form(o);inc(0,1);inc(a,b?-1:1);inc(c,d?-1:1);inc(a^c,b^d?-1:1)}
 let constant=coeff.get(0)||0,terms=[...coeff].filter(([m,w])=>m&&w);
 let cols=terms.map(([m])=>m), weights=terms.map(([,w])=>Math.abs(w)*2), pref=terms.map(([,w])=>+(w>0)), offset=constant-terms.reduce((a,[,w])=>a+Math.abs(w),0);
 // reference consumer: exact parity syndrome DP, cap on explicit syndrome states.
 let piv=new Map(),deps=[];for(let j=0;j<cols.length;j++){let m=cols[j],v=1n<<BigInt(j);while(m){let p=31-Math.clz32(m);if(!piv.has(p)){piv.set(p,[m,v]);break}let [a,b]=piv.get(p);m^=a;v^=b}if(!m)deps.push(v)}
 for(let [x,e] of reference){let energy=constant+terms.reduce((s,[m,w])=>s+(parity(m&x)?-w:w),0);if(energy!==4*e)throw Error("energy mismatch");checks++}
 let h=deps.length, dpmin=null,peak=0,trans=0,graphEdges=terms.every(([m])=>m.toString(2).replace(/0/g,"").length===2),active=new Set(cols.flatMap(m=>Array.from({length:n},(_,i)=>i).filter(i=>m>>i&1))),eulerFails=graphEdges&&active.size>=3&&terms.length>3*active.size-6;
 if(h<=18){let s=0, hc=cols.map((_,j)=>deps.reduce((v,d,i)=>v|Number((d>>BigInt(j))&1n)<<i,0));hc.forEach((v,j)=>{if(pref[j])s^=v});let d=new Map([[0,0]]);for(let j=0;j<hc.length;j++){let z=new Map(d);for(let [k,v] of d){let l=k^hc[j],w=v+weights[j];if(w<(z.get(l)??Infinity))z.set(l,w);trans++}d=z;peak=Math.max(peak,d.size)}dpmin=offset+d.get(s);if(dpmin!==4*min)throw Error("syndrome mismatch");checks++}
 return {original,guarded,contradiction,passes,inferred,guardRank:basis.size,terms:terms.length,rank:piv.size,h,offset,min,word,dpmin,peak,trans,graphEdges,eulerFails,active:active.size}
}
let out=[];for(let i=0;i<rt.controls.length;i++){let {n,registry:r}=rt.controls[i], d=da.rt[i];let neighbor=r.map((o,j)=>j?o:{...o,bad:o.bad.map(x=>x^1)});out.push({n,root:test(n,r,[]),rootCombined:test(n,r,d.alternating.accepted),neighbor:test(n,neighbor,[]),neighborCombined:test(n,neighbor,d.neighborAlternating.accepted)})}
return {checks,out}
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2))}
