function dense(R,k=3,cap=4000000){
 const n=R.free.length,B=R.free.map(x=>BigInt("0x"+x)),C=1n<<BigInt(n),mask=C-1n,oldC=1n<<BigInt(R.original_root_positions.length),low=x=>x&-x,hex=x=>x.toString(16);
 const par=x=>{let b=0;while(x){x&=x-1n;b^=1}return b},bits=B.map((_,i)=>1n<<BigInt(i)),wt=x=>{let n=0;while(x){x&=x-1n;n++}return n};
 const met={rankXors:0,signaturePatterns:0,pairProbes:0,orientationChecks:0,packAttempts:0,peakSignatures:0};
 function echelon(rows){let m=new Map();for(let r of rows){while(r&mask){let p=low(r&mask);if(m.has(p)){r^=m.get(p);met.rankXors++}else{m.set(p,r);break}}if(r===C)return null}return m}
 function ge(rows){let m=echelon(rows);if(m===null)return null;let keys=[...m.keys()].sort((a,b)=>a>b?-1:1);for(let i=0;i<keys.length;i++){let p=keys[i],a=m.get(p);for(let j=i+1;j<keys.length;j++){let q=keys[j],b=m.get(q);if(b&p){m.set(q,b^a);met.rankXors++}}}return keys.reverse().map(p=>m.get(p))}
 function unique(F){let seen=new Set();return F.filter(e=>e!==null&&!seen.has(e.join(","))&&(seen.add(e.join(",")),true))}
 function compress(s){let v=BigInt("0x"+s),r=v&oldC?C:0n;B.forEach((p,i)=>{if(v&p)r|=bits[i]});return r}
 let F=unique(R.events.map(e=>ge(e.map(compress)))),free=bits.slice(),trace=[],initial={d:free.length,m:F.length},stop;
 const touch=(F,h)=>F.map((e,i)=>e.some(r=>par((r&mask)&h))?i:-1).filter(i=>i>=0);
 function solution(rows){let a=echelon(rows);if(a===null)return null;let h=0n;for(let p of [...a.keys()].sort((a,b)=>a>b?-1:1)){let r=a.get(p);if(par((r&mask)&h)!==Number(!!(r&C)))h|=p}return h}
 function packs(F,d,need){let rem=F.map((_,i)=>i),out=[];while(out.length<need){let a=new Map(),sel=[];for(let i of rem){let z=a.size;for(let r of F[i]){r&=mask;while(r){let p=low(r);if(a.has(p)){r^=a.get(p);met.rankXors++}else{a.set(p,r);break}}}if(a.size>z)sel.push(i);if(a.size===d)break}met.packAttempts++;if(a.size<d)break;out.push(sel);let s=new Set(sel);rem=rem.filter(i=>!s.has(i))}return out}
 function find(F,free,k){
  let flat=F.flat().map(x=>x&mask),M=echelon(flat),piv=[...M.keys()].sort((a,b)=>a>b?-1:1),unused=free.filter(b=>!M.has(b));
  if(unused.length){let periods=unused.map(b=>{let h=b;for(let p of piv)if(par(M.get(p)&h))h^=p;if(touch(F,h).length)throw Error("bad kernel");return hex(h)});return {gauge:unused,periods}}
  let pack=packs(F,free.length,k+1);if(pack.length===k+1)return {status:"REFUSAL",kind:"disjoint spanning groups",groups:pack};
  let m=new Map(),dep=[],groups=[],idx=0;
  for(let e of F){let g=[];for(let a of e){g.push(idx);let r=a&mask,t=1n<<BigInt(idx++);while(r){let p=low(r);if(!m.has(p)){m.set(p,[r,t]);break}let [v,w]=m.get(p);r^=v;t^=w;met.rankXors++}if(!r)dep.push(t)}groups.push(g)}
  const col=flat.map(()=>0n);for(let i=0;i<dep.length;i++){let r=dep[i];while(r){let v=low(r),j=v.toString(2).length-1;col[j]|=1n<<BigInt(i);r^=v}}
  let table=new Map(),list=[];
  function lift(w,t){let h=solution(flat.map((r,i)=>r|((w>>BigInt(i))&1n?C:0n)));if(h===null||!h||touch(F,h).length!==t)throw Error("bad lift");return {h,t,method:"syndrome"}}
  for(let i=0;i<groups.length;i++){let G=groups[i];if(G.length>16||list.length+2**G.length>20000)return{status:"UNKNOWN",kind:"pattern cap"};let sig=[0n],pat=[0n];for(let j of G){let sz=sig.length;for(let l=0;l<sz;l++){sig.push(sig[l]^col[j]);pat.push(pat[l]^(1n<<BigInt(j)))}}for(let l=1;l<sig.length;l++){met.signaturePatterns++;let s=sig[l],w=pat[l];if(!s)return lift(w,1);if(table.has(s)){let a=table.get(s);return lift(w^a.w,a.i===i?1:2)}let a={s,w,i};table.set(s,a);list.push(a);met.peakSignatures=Math.max(met.peakSignatures,list.length)}}
  for(let i=0;i<list.length;i++)for(let j=i+1;j<list.length;j++){let a=list[i],b=list[j];if(a.i===b.i)continue;if(++met.pairProbes>cap)return{status:"UNKNOWN",kind:"pair cap"};let c=table.get(a.s^b.s);if(c&&c.i!==a.i&&c.i!==b.i)return lift(a.w^b.w^c.w,3)}
  if(k===3)return{status:"REFUSAL",kind:"complete syndrome",words:list.length,partialPacking:pack};
  const pm=new Map();for(let i=0;i<list.length;i++)for(let j=i+1;j<list.length;j++){let a=list[i],b=list[j];if(a.i===b.i)continue;if(++met.pairProbes>cap||pm.size>=500000)return{status:"UNKNOWN",kind:"four-touch pair cap"};let s=a.s^b.s;if(pm.has(s)){let [u,v]=pm.get(s);if(new Set([a.i,b.i,u.i,v.i]).size!==4)throw Error("overlap after <=3 refusal");return lift(a.w^b.w^u.w^v.w,4)}pm.set(s,[a,b]);met.peakSignatures=Math.max(met.peakSignatures,list.length+pm.size)}
  return{status:"REFUSAL",kind:"complete four-touch syndrome",words:list.length,partialPacking:pack};
 }
 const restrict=(e,b,v)=>ge(e.map(r=>r&b?r^b^(v?C:0n):r));
 const join=(a,b)=>a===null||b===null?null:ge([...a,...b]);
 const count=(e,d)=>e===null?0n:1n<<BigInt(d-e.length);
 function elim(F,h,free){let b=low(h),S=F.map(e=>ge(e.map(r=>Boolean(r&b)!==Boolean(par((r&mask)&h))?r^b:r))),A=S.filter(e=>e.some(r=>r&b)),O=S.filter(e=>!e.some(r=>r&b));for(let i=0;i<A.length;i++)for(let j=i+1;j<A.length;j++){
   let T=ge([...A[i],...A[j].map(r=>r&b?r^C:r)]),Q=null;if(T!==null){let u=T.find(r=>r&b);if(!u)throw Error("projection pivot");Q=ge(T.filter(r=>r!==u).map(r=>r&b?r^u:r))}
   let U=join(restrict(A[i],b,0),restrict(A[j],b,1)),V=join(restrict(A[i],b,1),restrict(A[j],b,0));
   for(let Z of [U,V])if(Z!==null&&(Q===null||Q.some(r=>ge([...Z,r^C])!==null)))throw Error("orientation inclusion");
   let d=free.length-1;if(count(Q,d)!==count(U,d)+count(V,d)-count(join(U,V),d))throw Error("orientation count");met.orientationChecks++;if(Q!==null)O.push(Q)
 }return unique(O)}
 for(;;){
  if(F.some(e=>!e.length)){stop={status:"UNSAT"};break}if(!F.length){stop={status:"SAT residual"};break}
  let unit=F.find(e=>e.length===1);if(unit){let r=unit[0]^C,b=low(r&mask);F=unique(F.map(e=>ge(e.map(a=>a&b?a^r:a))));free=free.filter(x=>x!==b);trace.push({unit:hex(r),d:free.length,m:F.length});continue}
  let z=find(F,free,k);if(z.gauge){let G=z.gauge.reduce((a,b)=>a|b,0n);F=unique(F.map(e=>ge(e.map(r=>r&~G))));free=free.filter(b=>!(b&G));trace.push({gauge:z.gauge.map(hex),periods:z.periods,d:free.length,m:F.length});continue}
  if(!z.h){stop=z;break}
  let h=z.h,old=F.length,ids=touch(F,h);F=elim(F,h,free);free=free.filter(b=>b!==low(h));if(F.length>old+Math.max(0,k*(k-1)/2-k))throw Error("growth");trace.push({h:hex(h),weight:wt(h),t:z.t,events:ids,d:free.length,m:F.length})
 }
 return {initial,final:{d:free.length,m:F.length},stop,trace,metrics:met,free:free.map(hex),events:F.map(e=>e.map(hex)),n};
}
module.exports={dense};
if(require.main===module){const fs=require('fs');const R=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));console.log(JSON.stringify(dense(R,Number(process.argv[3]||3)),null,2))}
