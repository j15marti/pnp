function sharedAudit(input){
const lines=input.dimacs.trim().split("\n"),hdr=lines.shift().split(/\s+/),n=+hdr[2],C=lines.map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));let events=0;const cap=1e7;function charge(k=1){events+=k;if(events>cap)throw Error("cap")}
function propagate(A){A=A.slice();let trail=[],again=true;while(again){again=false;for(let i=0;i<C.length;i++){let sat=false,open=[];for(let l of C[i]){charge();let v=A[Math.abs(l)-1];if(v===-1)open.push(l);else if(v===(l>0?1:0)){sat=true;break}}if(sat)continue;if(!open.length)return {A,trail,conflict:i+1};if(open.length===1){let l=open[0];A[Math.abs(l)-1]=l>0?1:0;trail.push([l,i+1]);again=true}}}return {A,trail}}
let initial=propagate(Array(n).fill(-1)),start=events,treeNodes=0,maxDepth=0;
function dpll(A,depth=0){treeNodes++;maxDepth=Math.max(depth,maxDepth===undefined?0:maxDepth);let p=propagate(A);if(p.conflict)return {trail:p.trail,conflict:p.conflict};let scores=Array(n).fill(0);let remaining=0;for(let c of C){let sat=false;for(let l of c){charge();if(p.A[Math.abs(l)-1]===(l>0?1:0)){sat=true;break}}if(sat)continue;remaining++;for(let l of c){charge();if(p.A[Math.abs(l)-1]===-1)scores[Math.abs(l)-1]++}}if(!remaining)return {sat:p.A};let i=scores.indexOf(Math.max(...scores)),left=p.A.slice(),right=p.A.slice();left[i]=0;right[i]=1;let L=dpll(left,depth+1);if(L.sat)return L;let R=dpll(right,depth+1);if(R.sat)return R;return {trail:p.trail,branch:i+1,left:L,right:R}}
let tree,status;try{tree=dpll(Array(n).fill(-1));status=tree.sat?"SAT":"UNSAT"}catch(e){status="UNKNOWN"}
let discoveryEvents=events-start,verificationEvents=0;
function verify(T,A){A=A.slice();for(let [l,id] of T.trail){let c=C[id-1];if(!c.includes(l)||A[Math.abs(l)-1]!==-1)throw Error("bad unit");for(let z of c){verificationEvents++;if(z!==l&&A[Math.abs(z)-1]!== (z>0?0:1))throw Error("bad reason")}A[Math.abs(l)-1]=l>0?1:0;}if(T.conflict){for(let z of C[T.conflict-1]){verificationEvents++;if(A[Math.abs(z)-1]!== (z>0?0:1))throw Error("bad conflict")}return;}let i=T.branch-1;if(A[i]!==-1)throw Error("bad branch");let L=A.slice(),R=A.slice();L[i]=0;R[i]=1;verify(T.left,L);verify(T.right,R)}
if(status==="UNSAT")verify(tree,Array(n).fill(-1));
// Independent GF(2) lane: exact-one recognizer on original clause IDs; GE plus degree-D static products.
let G=[],pairs=new Map();C.forEach((c,i)=>{if(c.length===2&&c.every(x=>x<0)){pairs.set(c.map(x=>-x).sort((a,b)=>a-b).join(","),i+1)}});
C.forEach((c,i)=>{if(c.every(x=>x>0)&&new Set(c).size===c.length){let ids=[],ok=true;for(let j=0;j<c.length;j++)for(let k=j+1;k<c.length;k++){let id=pairs.get([c[j],c[k]].sort((a,b)=>a-b).join(","));if(!id)ok=false;else ids.push(id)}if(ok)G.push({clause:i+1,pairs:ids,vars:c})}});
let affine=null,algEvents=0;function ac(k=1){algEvents+=k;if(algEvents+events+verificationEvents>cap)throw Error("cap")}
try{
let rows=G.map(g=>g.vars.reduce((r,v)=>r^(1n<<BigInt(v-1)),1n<<BigInt(n))),piv=[],rank=0;for(let j=0;j<n;j++){let i=rows.findIndex((r,i)=>i>=rank&&((r>>BigInt(j))&1n));if(i<0)continue;[rows[i],rows[rank]]=[rows[rank],rows[i]];for(let k=0;k<rows.length;k++)if(k!==rank&&((rows[k]>>BigInt(j))&1n)){ac();rows[k]^=rows[rank]}piv.push(j);rank++}let free=Array.from({length:n},(_,i)=>i).filter(i=>!piv.includes(i));if(rows.some(r=>r===1n<<BigInt(n))){affine={rank,nullity:free.length,status:"UNSAT-GE"}}else if(G.length){
let d=free.length,lin=Array(n);for(let j=0;j<n;j++){if(free.includes(j))lin[j]=new Set([1n<<BigInt(free.indexOf(j))]);else{let r=rows[piv.indexOf(j)],s=new Set();if((r>>BigInt(n))&1n)s.add(0n);for(let k=0;k<d;k++)if((r>>BigInt(free[k]))&1n)s.add(1n<<BigInt(k));lin[j]=s}}
function toggle(S,x){ac();if(S.has(x))S.delete(x);else S.add(x)}
function mul(A,B){let s=new Set();for(let a of A)for(let b of B)toggle(s,a|b);return s}
const fs=C.map(c=>c.reduce((p,l)=>{let q=new Set(lin[Math.abs(l)-1]);if(l>0)toggle(q,0n);return mul(p,q)},new Set([0n])));
let levels=[],B=new Map(),labels=[],witness=null;const mon=[0n];for(let k=0;k<d;k++)mon.push(1n<<BigInt(k));for(let k=0;k<d;k++)for(let j=k+1;j<d;j++)mon.push((1n<<BigInt(k))|(1n<<BigInt(j)));
const cuts=[1,1+d,mon.length];for(let D=0;D<=2;D++){let lo=D?cuts[D-1]:0;for(let q=lo;q<cuts[D]&&!witness;q++)for(let i=0;i<fs.length&&!witness;i++){let v=mul(fs[i],new Set([mon[q]])),cert=1n<<BigInt(labels.length);labels.push([i+1,mon[q].toString()]);while(v.size){let p=-1n;for(let z of v){ac();if(z>p)p=z}if(!B.has(p)){B.set(p,[v,cert]);if(p===0n)witness=cert;break}let [b,t]=B.get(p);for(let z of b)toggle(v,z);cert^=t}}levels.push({degree:D,columns:labels.length,rank:B.size,events:algEvents});if(witness)break}
let proof=witness===null?null:labels.filter((_,i)=>(witness>>BigInt(i))&1n);if(proof){let v=new Set();for(let [id,u] of proof)for(let z of mul(fs[id-1],new Set([BigInt(u)])))toggle(v,z);if(v.size!==1||!v.has(0n))throw Error("syzygy check")}
affine={rank,nullity:d,free:free.map(i=>i+1),groups:G,levels,proof,status:proof?"UNSAT":"UNKNOWN"};
}else affine={rank,nullity:free.length,status:"NO-EXACT-ONE-GROUPS"};
}catch(e){affine={status:"UNKNOWN",error:String(e),groups:G.length}}
return {id:input.id,N:input.dimacs.length*8,n,m:C.length,initialForced:initial.trail.length,status,treeNodes,maxDepth,discoveryEvents,verificationEvents,algebraEvents:algEvents,tree,affine,events:events+verificationEvents+algEvents}
}
const fs=require('fs');const j=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));console.log(JSON.stringify(j.primary.map(id=>{const v=j.instances.find(x=>x.id===id);return sharedAudit({id,dimacs:v.dimacs})}),null,2));
