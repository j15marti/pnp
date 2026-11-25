function runGD20(){
const C={queries:0,yes:0,no:0,closureScans:0,closureRows:0,gaussian:0,transitions:0,merges:0,maxKeys:0,maxWidth:0,refWords:0,witnesses:0,assertions:0};
const check=(v,msg)=>{C.assertions++;if(!v)throw Error(msg)};
const bit=i=>1n<<BigInt(i);
function dot(a,b){let x=a&b,s=0;while(x){s^=1;x&=x-1n}return s}
function basis(rows){C.gaussian++;let a=[];for(let x of rows){for(const y of a)if((x^y)<x)x^=y;if(x){a.push(x);a.sort((p,q)=>p>q?-1:p<q?1:0)}}return a}
function red(x,a){for(const y of a)if((x^y)<x)x^=y;return x}
function meet(a,b){let t=[],out=[];for(let [x,h] of [...a.map(x=>[x,x]),...b.map(x=>[x,0n])]){for(const [v,z] of t)if((x^v)<x){x^=v;h^=z}if(!x){if(h)out.push(h)}else{t.push([x,h]);t.sort((p,q)=>p[0]>q[0]?-1:1)}}return basis(out)}
const aug=(r,b)=>(r<<1n)|BigInt(b);
const eqs=(rows)=>basis(rows);
function sol(rows){const a=eqs(rows);if(a.includes(1n))return null;let x=0n;for(const y of [...a].reverse()){let r=y>>1n;if(dot(r,x)!==Number(y&1n))x^=1n<<BigInt(r.toString(2).length-1)}return x}
const ineq=(g)=>g.map(([r,b])=>[aug(r,1^b)]);
function posBranches(e){return [...ineq(e.g),[aug(e.d^e.s,e.b)]]}
function close(E){let h=[];for(;;){let change=false;for(const e of E){if(e.t!=="p")continue;C.closureScans++;let bs=posBranches(e).map(a=>eqs([...h,...a])).filter(a=>!a.includes(1n));if(!bs.length)return null;let common=bs.reduce(meet);let next=basis([...h,...common]);if(next.length>h.length){C.closureRows+=next.length-h.length;h=next;change=true;break}}if(!change)return h}}
function reduceEq(r,b,h){let v=red(aug(r,b),h); // only coefficient pivot, no inconsistent RHS in h
return [v>>1n,Number(v&1n)]}
function solve(E, ext, neg){
 C.queries++;let h=close(E);if(h===null){C.no++;return {ok:false,width:0,keys:0}}
 let F=E.map(e=>{let g=e.g.map(([r,b])=>reduceEq(r,b,h));if(e.t==="p"){let [r,b]=reduceEq(e.d^e.s,e.b,h);return {...e,g,d:r,s:0n,b}}let [s,b]=reduceEq(e.s,e.b,h);return {...e,g,s,b}});
 let U=F.map(e=>basis([...e.g.map(x=>x[0]),e.t==="p"?e.d:e.s]));
 let m=E.length,P=[[]],S=Array(m+1),D=[[]],G=Array(m+1);S[m]=[];G[m]=[];
 for(let i=0;i<m;i++){P.push(basis([...P[i],...U[i]]));D.push(basis([...D[i],...(F[i].t==="n"?[F[i].d]:[])]))}
 for(let i=m-1;i>=0;i--){S[i]=basis([...S[i+1],...U[i]]);G[i]=basis([...G[i+1],...(F[i].t==="n"?[F[i].d]:[])])}
 let W=P.map((a,i)=>meet(a,S[i])),width=Math.max(...W.map((a,i)=>a.length+meet(D[i],G[i]).length+(neg?1:0)));C.maxWidth=Math.max(C.maxWidth,width);
 let tab=new Map([["0,0,0",{k:0,z:0n,p:0,prev:null}]]),max=1;
 const pins=(w,k)=>w.map((r,i)=>aug(r,(k>>i)&1));
 for(let i=0;i<m;i++){
  const e=F[i],out=new Map();
  if(W[i+1].length>20)throw Error("test width cap");
  for(const a of tab.values())for(let k=0;k<2**W[i+1].length;k++){
   const pre=[...pins(W[i],a.k),...pins(W[i+1],k)];
   const opts=e.t==="p"?posBranches(e).map(q=>({q,y:0,p:0})):[{q:[],y:0,p:0},...[0,1].map(p=>({q:[...e.g.map(([r,b])=>aug(r,b)),aug(e.s,p^e.b)],y:1,p}))];
   for(const o of opts){C.transitions++;let z=a.z^(o.y?e.d:0n),p=a.p^o.p;if(red(z,G[i+1]))continue;let x=sol([...pre,...o.q]);if(x===null)continue;
    const key=[k,z.toString(),p].join(",");if(out.has(key)){C.merges++;continue}out.set(key,{k,z,p,prev:a,x,y:o.y,i});
   }
  }
  tab=out;max=Math.max(max,tab.size);C.maxKeys=Math.max(C.maxKeys,tab.size);if(!tab.size)break;
 }
 let a=tab.get("0,0,"+(neg?1:0));if(!a||a.i!==m-1&&m){C.no++;return {ok:false,width,keys:max}}
 let rows=[...h],ys=Array(m).fill(0);while(a.prev){for(const r of U[a.i])rows.push(aug(r,dot(r,a.x)));ys[a.i]=a.y;a=a.prev}
 let x=sol(rows);check(x!==null,"lift");let z=0n,p=0;
 for(let i=0;i<m;i++){const e=E[i],active=e.g.every(([r,b])=>dot(r,x)===b),s=dot(e.s,x)^e.b;if(e.t==="p")check(!active||dot(e.d,x)===s,"positive witness");else if(ys[i]){check(active,"negative activation");z^=e.d;p^=s}}
 check(z===0n&&p===(neg?1:0),"dual witness");C.witnesses++;C.yes++;return {ok:true,width,keys:max}
}
function ev(net,x){return sol(net.filter(e=>e.g.every(([r,b])=>dot(r,x)===b)).map(e=>aug(e.d,dot(e.s,x)^e.b)))!==null}
function ref(A,B,d){let ok=false;for(let x=0;x<2**d;x++){C.refWords++;if(ev(A,BigInt(x))&&(!B||!ev(B,BigInt(x))))ok=true}return ok}
function query(A,B,d,interleave=true){const a=A.map(e=>({...e,t:"p",d:e.d<<BigInt(d)}));const b=(B||[]).map(e=>({...e,t:"n"}));const E=[];if(interleave){for(let i=0;i<Math.max(a.length,b.length);i++){if(a[i])E.push(a[i]);if(b[i])E.push(b[i])}}else E.push(...a,...b);return solve(E,d,!!B)}
function test(A,B,d){let r=query(A,B,d);check(r.ok===ref(A,B,d),"reference decision");return r}
const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function fano(flip=-1){return triples.flatMap((t,i)=>{let s=t.map((_,j)=>flip===3*i+j?1:0),g=[[bit(t[0])^bit(t[1]),s[0]^s[1]],[bit(t[0])^bit(t[2]),s[0]^s[2]]];return [0,1].map(b=>({g,d:bit(i),s:0n,b}))})}
let F=fano(),fanoData={root:test(F,null,7),neighbors:[],directions:[]};
for(let i=0;i<21;i++){let H=fano(i);fanoData.neighbors.push(test(H,null,7).ok);fanoData.directions.push([test(F,H,7).ok,test(H,F,7).ok,test(H,H,7).ok])}
let seed=201208;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)}
function random(){return Array.from({length:5},()=>({g:Array.from({length:rnd(4)},()=>[BigInt(rnd(16)),rnd(2)]),d:BigInt(rnd(8)),s:BigInt(rnd(16)),b:rnd(2)}))}
let randomData={queries:0,yes:0};for(let i=0;i<50;i++){let A=random(),B=random();for(let H of [null,B,A]){let r=test(A,H,4);randomData.queries++;randomData.yes+=+r.ok}}
function path(k,flip){let a=[];for(let i=0;i<k;i++)for(let j=0;j<2;j++)a.push({g:[[bit(2*i+j),1]],d:bit(i)^bit(i+1),s:0n,b:0});a.push({g:[],d:bit(0)^bit(k),s:0n,b:flip?0:1});return a}
let scaling=[];for(let k of [2,4,8,16,32,64]){let A=path(k,false),B=path(k,true);let same=query(A,A,2*k),forward=query(A,B,2*k),back=query(B,A,2*k);check(!same.ok&&!forward.ok&&back.ok,"path");if(k<=4)check(back.ok===ref(B,A,2*k),"path ref");scaling.push({k,same,forward,back})}
let dense=[{g:Array.from({length:48},(_,i)=>[bit(i),1]),d:1n,s:0n,b:0},{g:Array.from({length:48},(_,i)=>[bit(i),1]),d:1n,s:0n,b:1}];
// Directly comparing repeats all 48 rows across events; instead use one zero private row with guard of rank 48, hence no internal cut.
let D=[{g:dense[0].g,d:0n,s:0n,b:1}],T=[{g:[],d:0n,s:0n,b:0}];
let denseResult=query(T,D,48);check(denseResult.ok,"dense local guard");
return {C,fanoData,randomData,scaling,denseResult,seed:201208};
}
console.log(JSON.stringify(runGD20(),null,2));
