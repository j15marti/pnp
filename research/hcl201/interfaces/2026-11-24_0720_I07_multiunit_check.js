const run=()=>{
let state=0x6c20707;function rnd(n){state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n}
const sum=a=>a.reduce((s,x)=>s+x,0),key=a=>a.join(","),unique=a=>[...new Map(a.map(x=>[key(x),x])).values()];
function recognize(A){if(!A.length)return false;let k=sum(A[0]),S=new Set(A.map(key));if(A.some(a=>sum(a)!==k))return false;for(let a of A)for(let b of A)for(let i=0;i<a.length;i++)if(a[i]>b[i]){let found=false;for(let j=0;j<a.length;j++)if(a[j]<b[j]){let c=a.slice();c[i]--;c[j]++;if(S.has(key(c)))found=true}if(!found)return false}return true}
let stats={random:0,SAT:0,UNSAT:0,pins:0,pinSAT:0,pinUNSAT:0,referenceTuples:0,augmentations:0,certificates:0,prepassRejects:0,deleted:0,multiunitBlocks:0,invalidExchangeControls:0};
function solve(A,K){let rows=A.map(unique),h=K.length;
for(;;){if(rows.some(a=>!a.length)){stats.prepassRejects++;return false}let m=rows.map(a=>K.map((_,i)=>Math.min(...a.map(x=>x[i])))),s=K.map((_,i)=>sum(m.map(x=>x[i])));if(s.some((x,i)=>x>K[i])){stats.prepassRejects++;return false}let changed=false;for(let b=0;b<rows.length;b++){let j=rows[b].findIndex(a=>a.some((v,i)=>v-m[b][i]>K[i]-s[i]));if(j>=0){rows[b].splice(j,1);stats.deleted++;changed=true;break}}if(!changed)break}
if(rows.some(a=>!recognize(a)))return null;
let minima=rows.map(a=>K.map((_,i)=>Math.min(...a.map(x=>x[i])))),cap=K.map((v,i)=>v-sum(minima.map(a=>a[i])));let R=rows.map((a,b)=>a.map(x=>x.map((v,i)=>v-minima[b][i])));let E=[];for(let b=0;b<R.length;b++)for(let i=0;i<h;i++){let m=Math.max(...R[b].map(x=>x[i]));if(m>=R[b].length)throw Error("range bound");for(let j=0;j<m;j++)E.push([b,i,j])}let rank=sum(R.map(a=>sum(a[0]))),I=new Set();
function counts(S){let a=R.map(()=>K.map(()=>0));for(let e of S){let[b,i]=E[e];a[b][i]++}return a}
function ind(S,m){let a=counts(S);return m===1?R.every((r,b)=>r.some(x=>x.every((v,i)=>v>=a[b][i]))):cap.every((v,i)=>sum(a.map(x=>x[i]))<=v)}
function change(e,f){let S=new Set(I);if(f!==undefined)S.delete(f);S.add(e);return S}
while(I.size<rank){let out=E.map((_,e)=>e).filter(e=>!I.has(e)),ins=[...I],prev=new Map(),q=[];for(let e of out)if(ind(change(e),1)){prev.set(e,-1);q.push(e)}let end=-1;
for(let p=0;p<q.length;p++){let e=q[p];if(!I.has(e)&&ind(change(e),2)){end=e;break}let next=I.has(e)?out.filter(f=>ind(change(f,e),1)):ins.filter(f=>ind(change(e,f),2));for(let f of next)if(!prev.has(f)){prev.set(f,e);q.push(f)}}
if(end<0){let S=cap.map((v,i)=>q.filter(e=>E[e][1]===i).length>=v);let demand=sum(R.map(a=>Math.min(...a.map(x=>sum(x.filter((_,i)=>S[i]))))));let capacity=sum(cap.filter((_,i)=>S[i]));if(demand<=capacity)throw Error("invalid Hall certificate");stats.certificates++;return false}
for(let e=end;e>=0;e=prev.get(e)){if(I.has(e))I.delete(e);else I.add(e)}if(!ind(I,1)||!ind(I,2))throw Error("invalid augmentation");stats.augmentations++}
let w=counts(I).map((a,b)=>a.map((v,i)=>v+minima[b][i]));if(!A.every((r,b)=>r.some(x=>key(x)===key(w[b])))||K.some((v,i)=>sum(w.map(a=>a[i]))>v))throw Error("invalid lift");return true}
function reference(rows,K){let ok=false;function go(b,v){if(b===rows.length){stats.referenceTuples++;if(v.every((x,i)=>x<=K[i]))ok=true;return}for(let a of rows[b])go(b+1,v.map((x,i)=>x+a[i]))}go(0,K.map(()=>0));return ok}
function check(rows,K,pin){let x=solve(rows,K),y=reference(rows,K);if(x!==y)throw Error("mismatch");if(pin){stats.pins++;stats[y?"pinSAT":"pinUNSAT"]++}else{stats.random++;stats[y?"SAT":"UNSAT"]++}}
for(let t=0;t<150;t++){let h=3+rnd(3),B=2+rnd(3),rows=[];for(let b=0;b<B;b++){let q=3+rnd(3),cols=Array.from({length:q},()=>[rnd(h),rnd(3)]),r=[]; // rank-two partition matroid on physical elements; owner aggregation
for(let i=0;i<q;i++)for(let j=i+1;j<q;j++)if(cols[i][1]!==cols[j][1]){let a=Array(h).fill(0);a[cols[i][0]]++;a[cols[j][0]]++;r.push(a)}if(!r.length){let a=Array(h).fill(0);a[cols[0][0]]=1;r.push(a)}r=unique(r);if(!recognize(r))throw Error("generator not exchange");if(r.some(a=>a.some(v=>v>1)))stats.multiunitBlocks++;rows.push(r)}let K=Array.from({length:h},()=>rnd(B+2));check(rows,K,false);for(let b=0;b<B;b++)for(let a of rows[b]){let p=rows.slice();p[b]=[a];check(p,K,true)}}
for(const A of [[[2,0],[0,2]],[[1,1,0,0],[0,0,1,1]],[[1,0],[1,1]]]){if(recognize(A))throw Error("false acceptance");stats.invalidExchangeControls++}
return {seed:"0x6c20707",...stats}};
console.log(JSON.stringify(run(),null,2));
