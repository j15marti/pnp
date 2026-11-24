/* Run: node 2026-11-24_0820_BD02_check.js */
function experiment(){
const C={cases:0,sat:0,unsat:0,guardCases:0,guardAssignments:0,referenceAssignments:0,pointwiseChecks:0,closureScans:0,closureDeductions:0,closureRejects:0,localAcquisitions:0,localAssignments:0,cacheHits:0,cacheMisses:0,quarticsBefore:0,quarticsAfter:0};
let seed=20261124;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>12)%n};
const bit=i=>1n<<BigInt(i), mask=vs=>vs.reduce((a,i)=>a|bit(i),0n);
const par=(x)=>{let p=0;while(x){x&=x-1n;p^=1}return p};
const chi=(x,s)=>1-2*par(x&s);
const size=x=>{let n=0;while(x){x&=x-1n;n++}return n};
const index=(vs,x)=>vs.reduce((a,v,i)=>a+Number((x>>BigInt(v))&1n)*2**i,0);
const fac=(vs,f)=>({vs,f});
const table=(vs,fn)=>fac(vs,Array.from({length:2**vs.length},(_,x)=>fn(x)));
const evalF=(F,x)=>F.reduce((s,a)=>s+a.f[index(a.vs,x)],0);
function submask(vs,k){return mask(vs.filter((_,i)=>(k>>i)&1))}
function add(M,s,w){M.set(s,(M.get(s)||0)+w);if(!M.get(s))M.delete(s)}
function fourier(F){let M=new Map();for(const a of F){let L=a.f.length;for(let k=0;k<L;k++){let s=submask(a.vs,k);let w=0;for(let x=0;x<L;x++)w+=a.f[x]*(1-2*par(BigInt(x&k)));w*=16/L;if(size(s)%2&&w)throw Error("asymmetric");add(M,s,w)}}return M}
function linear(){let b=new Map(),generators=[];function reduce(s){let coeff=0n;while(s){let p=s.toString(2).length-1;let a=b.get(p);if(!a)break;s^=a.s;coeff^=a.c}return {s,coeff}}return {reduce,generators,add(s){let r=reduce(s);if(!r.s)return false;let j=generators.length;generators.push(s);b.set(r.s.toString(2).length-1,{s:r.s,c:r.coeff^bit(j)});return true}}}
function eqsystem(){let b=new Map();function reduce(s,v){while(s){let p=s.toString(2).length-1;let a=b.get(p);if(!a)break;s^=a.s;v^=a.v}return {s,v}}return {add(s,v){let r=reduce(s,v);if(!r.s)return r.v?-1:0;b.set(r.s.toString(2).length-1,r);return 1}}}
function closure(F,pins=[]){let E=eqsystem();for(const [s,v] of pins)if(E.add(s,v)<0)return false;let changed=true;while(changed){changed=false; outer:for(const a of F){let rows=[];for(let x=0;x<a.f.length;x++){C.closureScans++;if(a.f[x]!==0)continue;let test=eqsystem();for(const [s,v] of pins)test.add(s,v);let good=true;for(let i=0;i<a.vs.length;i++)if(test.add(bit(a.vs[i]),(x>>i)&1)<0){good=false;break}if(good)rows.push(x)}if(!rows.length){C.closureRejects++;return false}for(let k=1;k<a.f.length;k++){let z=par(BigInt(rows[0]&k));if(rows.every(x=>par(BigInt(x&k))===z)){let s=submask(a.vs,k);let r=E.add(s,z);if(r<0){C.closureRejects++;return false}if(r>0){pins=[...pins,[s,z]];C.closureDeductions++;changed=true;break outer}}}}}return true}
function edgeSet(scopes){let E=new Set();for(const vs of scopes)for(let i=0;i<vs.length;i++)for(let j=i+1;j<vs.length;j++)E.add(bit(vs[i])|bit(vs[j]));return E}
function plan(M,E){let Q=[...M].filter(([s])=>size(s)===4).map(([s,w])=>({s,w,eligible:[...E].filter(e=>(e&s)===e&&E.has(s^e))}));if(Q.some(q=>!q.eligible.length))return null;for(const [s] of M)if(size(s)===2&&!E.has(s))return null;let H=linear();if(Q.length){let common=Q[0].eligible.find(e=>Q.every(q=>q.eligible.includes(e)));if(common)H.add(common)}
for(const q of Q){if(!q.eligible.some(e=>!H.reduce(e).s))for(const e of q.eligible)H.add(e)}
for(const q of Q){q.e=q.eligible.find(e=>!H.reduce(e).s);if(q.e===undefined)throw Error("uncovered");q.c=H.reduce(q.e).coeff}return {Q,H}}
function solve(F,n,E,pins=[],cache=new Map()){
let rootClosure=closure(F,pins);let M=fourier(F),P=plan(M,E);if(!P)return null;let {Q,H}=P;C.quarticsAfter+=Q.length;C.quarticsBefore+=F.reduce((a,f)=>a+[...fourier([f])].filter(([s])=>size(s)===4).length,0);
let best=Infinity,witness=null;for(let g=0;g<2**H.generators.length;g++){C.guardCases++;let gp=[...pins,...H.generators.map((s,i)=>[s,(g>>i)&1])];let eq=eqsystem();if(gp.some(([s,v])=>eq.add(s,v)<0))continue;let guardClosure=closure(F,gp);let A=new Map(M);for(const q of Q){A.delete(q.s);add(A,q.s^q.e,q.w*chi(BigInt(g),q.c))}
let key=JSON.stringify([n,[...A].sort((a,b)=>a[0]<b[0]?-1:1).map(([s,w])=>[String(s),w]),gp.map(([s,v])=>[String(s),v]),[...E].map(String).sort()]);let val=Infinity,xbest=null;
if(cache.has(key)){C.cacheHits++;[val,xbest]=cache.get(key)}else{C.cacheMisses++;for(let j=0;j<2**n;j++){C.guardAssignments++;let x=BigInt(j);if(!gp.every(([s,v])=>par(x&s)===v))continue;let v=[...A].reduce((a,[s,w])=>a+w*chi(x,s),0);C.pointwiseChecks++;if(v!==16*evalF(F,x))throw Error("pointwise mismatch");if(v<val){val=v;xbest=x}}cache.set(key,[val,xbest])}
if(val===0&&!guardClosure)throw Error("guard closure false reject");if(val<best){best=val;witness=xbest}}
if(best===0&&!rootClosure)throw Error("root closure false reject");if(witness!==null&&(evalF(F,witness)*16!==best||!pins.every(([s,v])=>par(witness&s)===v)))throw Error("lift");return {best:best/16,witness,rank:H.generators.length,q:Q.length}}
function verify(F,n,E,pins=[]){let r=solve(F,n,E,pins);if(!r)throw Error("host declined");let v=Infinity;for(let j=0;j<2**n;j++){C.referenceAssignments++;let x=BigInt(j);if(pins.every(([s,b])=>par(x&s)===b))v=Math.min(v,evalF(F,x))}if(v!==r.best)throw Error("min discrepancy");C.cases++;if(v===0)C.sat++;else C.unsat++;return r}
const k4=[0,1,2,3];const host=edgeSet([k4]);
for(let t=0;t<140;t++){let vs=t%2?k4:[0,1,2,3,4,5];let scopes=t%2?[k4]:[k4,[0,1,4,5]];let E=edgeSet(scopes);let F=[];for(let j=0;j<1+rand(7);j++){let sc=scopes[rand(scopes.length)];let ar=2+rand(3), a=sc.slice(0,ar),L=2**ar;let f=Array(L);for(let x=0;x<L/2;x++)f[x]=f[L-1-x]=rand(4)===0?1:0;F.push(fac(a,f))}
verify(F,vs.length,E);verify(F,vs.length,E,[[mask([0,1]),rand(2)]])}
function star(sign){let F=Array.from({length:4},(_,i)=>table([i,4],x=>(((x&1)^((x>>1)&1)^((sign>>i)&1)))));let f=[],l=[];for(let y=0;y<16;y++){C.localAcquisitions++;let best=Infinity,bestx=0;for(let b=0;b<2;b++){C.localAssignments++;let x=BigInt(y+16*b),v=evalF(F,x);if(v<best){best=v;bestx=b}}f.push(best);l.push(bestx)}return {F,f,l,sign}}
const a=star(0),b=star(1);let am=fourier([fac(k4,a.f)]),bm=fourier([fac(k4,b.f)]);if(am.get(15n)!==-bm.get(15n)||!am.get(15n))throw Error("no cancellation");
let scale=[];for(let t of [2,4,8,16,32,64,128,256,512,1024]){let F=[],leaves=[];for(let i=0;i<t;i++){let s=star(i%2);leaves.push(s);F.push(fac(k4,s.f))}let r=solve(F,4,host);let total=0;for(let s of leaves)total+=evalF(s.F,BigInt(Number(r.witness)+16*s.l[Number(r.witness)]));if(total!==r.best)throw Error("star lift");scale.push({leaves:t,variables:t+4,quarticsBefore:t,after:r.q,guardRank:r.rank,min:r.best,verifiedLift:true})}
// Hostile noncancelling and genuine guarded shared-pair scaling.
let satScale=[];for(let t of [2,8,32,128,512,1024]){let F=[],leaves=[];for(let i=0;i<t;i++){let s=star(0);leaves.push(s);F.push(fac(k4,s.f))}let r=solve(F,4,host);let total=0;for(let s of leaves)total+=evalF(s.F,BigInt(Number(r.witness)+16*s.l[Number(r.witness)]));if(total!==0||r.best!==0||r.rank!==1)throw Error("SAT star lift");satScale.push({leaves:t,rank:r.rank,quartics:r.q,minimum:r.best})}
let rankScale=[];for(let t of [1,2,4,8,16,32,64,128]){let F=[],scopes=[];for(let i=0;i<t;i++){let vs=[0,1,2+2*i,3+2*i];scopes.push(vs);F.push(table(vs,x=>par(BigInt(x))?1:0))}let M=fourier(F),P=plan(M,edgeSet(scopes));if(!P||P.H.generators.length!==1)throw Error("common guard");rankScale.push({quartics:t,rank:P.H.generators.length,guardCases:2,scopeOnly:true})}
// Full Fano and seven full-clause deletion neighbors (independent reference, not planar terminal).
let edges=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let fano=[];for(let omit=-1;omit<7;omit++){let F=edges.filter((_,i)=>i!==omit).map(vs=>table(vs,x=>x===0||x===7?1:0));let count=0;for(let j=0;j<128;j++)if(evalF(F,BigInt(j))===0)count++;fano.push(count)}if(fano[0]!==0||fano.slice(1).some(x=>x!==10))throw Error("Fano");
let owner=[];for(let i=0;i<7;i++)for(let pol=0;pol<2;pol++){let F=edges.map((vs,j)=>table(vs,x=>j===i?(x===(pol?7:0)?1:0):(x===0||x===7?1:0)));let count=0;for(let j=0;j<128;j++)if(evalF(F,BigInt(j))===0)count++;owner.push(count)}if(owner.some(x=>x!==5))throw Error("owners");
let hostile=verify([fac(k4,a.f),fac(k4,a.f)],4,host);let repeatCache=new Map();solve([fac(k4,a.f)],4,host,[],repeatCache);solve([fac(k4,a.f)],4,host,[],repeatCache);
return {seed:20261124,counters:C,starQuartic16:[am.get(15n),bm.get(15n)],scale,satScale,rankScale,hostile:{rank:hostile.rank,quartics:hostile.q,min:hostile.best},fano,owner,limitations:"Local minimization exhaustively enumerates assignments, not blossom. Host graphs are constructed planar K4 edge bouquets or K4; no embedding test. Closure applied to zero-cost rows, guarded deductions not exported outside query. No full strict compiler, general tree engine, arbitrary owner budgets, or complete cooperative closure."}
}
console.log(JSON.stringify(experiment(),null,2));
