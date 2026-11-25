const data = {"s27":[],"cuts":[{"id":"S27-7-UNSAT","n":7,"models":0,"imported":[],"runs":[{"mode":0,"use":false,"label":"UNSAT","kind":"PD","cuts":[]},{"mode":1,"use":false,"label":"UNSAT","kind":"PD","cuts":[]},{"mode":2,"use":false,"label":"UNSAT","kind":"PD","cuts":[]}]},{"id":"S27-7-SAT","n":7,"models":10,"imported":[],"runs":[{"mode":0,"use":false,"label":"OPEN","cuts":[]},{"mode":1,"use":false,"label":"SAT","witness":7,"kind":"descent","cuts":[]},{"mode":2,"use":false,"label":"SAT","witness":7,"kind":"descent","cuts":[]}]},{"id":"S27-15-UNSAT","n":15,"models":0,"imported":[],"runs":[{"mode":0,"use":false,"label":"OPEN","cuts":[]},{"mode":1,"use":false,"label":"OPEN","cuts":[]},{"mode":2,"use":false,"label":"UNSAT","kind":"closure","cuts":[{"cut":[4,6,0],"reason":"PD"},{"cut":[6,8,0],"reason":"closure"},{"cut":[0,3,0],"reason":"closure"},{"cut":[1,2,0],"reason":"closure"},{"cut":[2,3,0],"reason":"closure"},{"cut":[3,5,1],"reason":"closure"},{"cut":[5,7,1],"reason":"closure"}]}]},{"id":"S27-15-SAT","n":15,"models":4,"imported":[],"runs":[{"mode":0,"use":false,"label":"SAT","witness":0,"kind":"seed","cuts":[]},{"mode":1,"use":false,"label":"SAT","witness":0,"kind":"seed","cuts":[]},{"mode":2,"use":false,"label":"SAT","witness":0,"kind":"seed","cuts":[]}]}]};
const run = function run(data){
const bit=i=>1n<<BigInt(i), parity=x=>{let v=0;while(x){x&=x-1n;v^=1}return v}, pop=x=>{let v=0;while(x){x&=x-1n;v++}return v};
let checks=0,rankCalls=0,scans=0,groups=0,dependencyProbes=0,referenceWords=0,termChecks=0;
function ck(x){checks++;if(!x)throw Error("assert "+checks)}
function add(B,v,b){while(v){let k=v.toString(2).length-1;if(!B.has(k)){B.set(k,[v,b]);return 1}let p=B.get(k);v^=p[0];b^=p[1]}return b?-1:0}
function basis(R){rankCalls++;let B=new Map();for(let [v,b] of R)if(add(B,v,b)<0)return null;return B}
function reduce(B,v){let b=0;for(let k of [...B.keys()].sort((a,b)=>b-a))if(v&bit(k)){v^=B.get(k)[0];b^=B.get(k)[1]}return [v,b]}
function owner({t,bad}){let f=bad[0];return [[bit(t[0])^bit(t[1]),(f^(f>>1))&1],[bit(t[0])^bit(t[2]),(f^(f>>2))&1]]}
function intersection(B,rows){let C=new Map(B);for(let [v,b] of rows)if(add(C,v,b)<0)return 0;return 2**(B.size-C.size)}
function closure(O,R){let B=basis(R);if(!B)return {reject:true};let del=0,forced=0;for(;;){scans++;let change=false;for(let e of O){let p=intersection(B,e);if(p===1)return {reject:true,B,del,forced};if(p===.5){let s=e.map(([v,b])=>{let [r,d]=reduce(B,v);return [r,b^d]}).find(([r])=>r);ck(!!s);ck(add(B,s[0],s[1]^1)===1);forced++;change=true;break}}if(!change){del=O.filter(e=>intersection(B,e)===0).length;return {reject:false,B,del,forced}}}}
function* subsets(n,k,start=0,p=[]){yield p;if(k)for(let i=start;i<n;i++)yield* subsets(n,k-1,i+1,p.concat(i))}
function avoid(B,O,J){let p=0;for(let mask=0;mask<(1<<J.length);mask++){let rows=[],s=0;J.forEach((id,j)=>{if(mask>>j&1){rows.push(...O[id]);s++}});p+=(s%2?-1:1)*intersection(B,rows)}return p}
function term(B,O,i,J){let p=0;for(let mask=0;mask<(1<<J.length);mask++){let rows=[...O[i]],s=0;J.forEach((id,j)=>{if(mask>>j&1){rows.push(...O[id]);s++}});p+=(s%2?-1:1)*intersection(B,rows)}return p}
function valid(x,R,O){return R.every(([v,b])=>parity(v&x)===b)&&O.every(e=>e.some(([v,b])=>parity(v&x)!==b))}
function trial(name,n,reg,R,w,reference,forest){
let O=reg.map(owner),cl=closure(O,R),models=null;if(reference){models=0;for(let x=0n;x<bit(n);x++){referenceWords++;if(valid(x,R,O))models++}}
if(cl.reject){ck(models===null||models===0);return {name,n,m:O.length,w,models,closure:"UNSAT",forced:cl.forced||0}}
let B=cl.B,L=new Map(),G=[...subsets(O.length,w+1)].filter(J=>J.length);
for(let J of G){groups++;let a=J.flatMap(i=>O[i].map(q=>q[0])),v=0n;for(let mask=1;mask<(1<<a.length);mask++){v=0n;a.forEach((q,j)=>{if(mask>>j&1)v^=q});dependencyProbes++;let [r,b]=reduce(B,v);if(!r)ck(add(L,v,b)>=0)}}
let H=[...L.values()].reduce((z,[v])=>z|v,0n);ck(pop(H)<=3*(w+1)*B.size);
let near=new Set(reg.flatMap(({t},i)=>t.some(v=>H&bit(v))?[i]:[]));
for(let j=0;j<w;j++){let vertices=new Set([...near].flatMap(i=>reg[i].t));reg.forEach(({t},i)=>{if(t.some(v=>vertices.has(v)))near.add(i)})}
let cover=false;for(let J of G){let p=intersection(B,J.flatMap(i=>O[i])),q=intersection(L,J.flatMap(i=>O[i]));ck(p===q);if(J.length<=w){let a=avoid(B,O,J),b=avoid(L,O,J);ck(a===b);if(a===0)cover=true}}
let score=0,minUnordered=0,remoteTerms=0;
for(let i=0;i<O.length;i++){let a=Infinity,b=Infinity;for(let J of G){if(J.length>w||J.includes(i))continue;let p=term(B,O,i,J);ck(p===term(L,O,i,J));termChecks++;if(J.every(j=>j<i))a=Math.min(a,p);b=Math.min(b,p);if(forest&&!near.has(i)){ck(p===.25*avoid(B,O,J));if(!cover)ck(p>=2**(-2*w-2));remoteTerms++}}let p=intersection(B,O[i]);a=Math.min(a,p);b=Math.min(b,p);score+=a;minUnordered+=b}
let lower=(O.length-near.size)*2**(-2*w-2);if(forest&&!cover)ck(minUnordered>=lower);if(cover)ck(models===null||models===0);
return {name,n,m:O.length,w,models,closure:cover?"small-cover UNSAT":"fixed point",rank:B.size,localizedRank:L.size,support:pop(H),near:near.size,remoteTerms,score,minUnordered,lower:forest&&!cover?lower:null,forced:cl.forced,impossible:cl.del}
}
let cases=[];
for(let z of data.s27)for(let mode of ["root","sat"]){let O=mode==="root"?z.root:z.satRegistry,n=z.n,id="S27-"+n+"-"+(mode==="root"?"UNSAT":"SAT");let cuts=data.cuts.find(q=>q.id===id).runs.find(q=>q.mode===2&&!q.use).cuts.map(({cut:[u,v,b]})=>[bit(u)^bit(v),b]);let w=n===7?2:1;cases.push(trial(id+" raw",n,O,[],w,true,false));if(cuts.length)cases.push(trial(id+" imported DA22",n,O,cuts,w,true,false));let dense=n===7?bit(n)-1n:bit(10)-1n;cases.push(trial(id+" dense=0",n,O,[[dense,0]],w,true,false));cases.push(trial(id+" pin=0",n,O,[[1n,0]],w,true,false))}
for(let [m,w] of [[24,1],[12,2]]){let O=Array.from({length:m},(_,i)=>({t:[i,(i+1)%m,m+i],bad:[0,7]})),n=2*m,witness=(bit(m)-1n)<<BigInt(m);let a=bit(n)-1n,b=a^1n^bit(1);for(let [name,R] of [["raw",[]],["dense",[[a,parity(a&witness)]]],["dense-cancellation",[[a,parity(a&witness)],[b,parity(b&witness)]]]]){ck(valid(witness,R,O.map(owner)));cases.push(trial("loose-"+m+" "+name,n,O,R,w,false,true))}}
return {checks,rankCalls,scans,groups,dependencyProbes,referenceWords,termChecks,cases};
};
console.log(JSON.stringify(run(data),null,2));
