"use strict";
function run(){
 const L={rank:0,xor:0,exchanges:0,augmentations:0,closureSweeps:0,pins:0,referenceWords:0,subsetChecks:0,lifts:0,assertions:0,peakGround:0};
 const ck=(v)=>{L.assertions++;if(!v)throw Error("assertion "+L.assertions)};
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 function basis(rows){L.rank++;let b=[];for(let a of rows){for(let v of b)if((a^v)<a){a^=v;L.xor++}if(a){b.push(a);b.sort((a,b)=>b-a)}}return b}
 const reduce=(a,b)=>{for(let v of b)if((a^v)<a){a^=v;L.xor++}return a};
 function gauss(eq,n){let b=new Map();for(let [a,c] of eq){while(a){let k=31-Math.clz32(a);if(!b.has(k)){b.set(k,[a,c]);break}let [v,d]=b.get(k);a^=v;c^=d;L.xor++}if(!a&&c)return null}return b}
 function solve(eq,n){let b=gauss(eq,n);if(!b)return null;let x=0;for(let k of [...b.keys()].sort((a,b)=>a-b)){let [a,c]=b.get(k);if(parity(a&x)!==c)x^=1<<k}return x}
 const holds=(e,x)=>e.every(([a,c])=>parity(a&x)===c);
 const legal=(E,x)=>E.every(e=>!holds(e,x));
 function closure(E,H,n){H=H.slice();E=E.slice();while(true){L.closureSweeps++;if(!gauss(H,n))return {H,E,bad:true};let h=basis(H.map(e=>e[0])),changed=false,keep=[];for(let e of E){if(!gauss(H.concat(e),n)){changed=true;continue}let R=basis(e.map(([a])=>reduce(a,h)));if(!R.length)return {H,E,bad:true};if(R.length===1){let row=e.find(([a])=>reduce(a,h));H.push([row[0],1^row[1]]);L.pins++;changed=true;break}keep.push(e)}if(changed){if(keep.length===E.length)throw Error("closure loop");if(keep.length===0||keep.length<E.length){ // retain all if a pin was added; otherwise drop inconsistent events
 E=E.filter(e=>gauss(H.concat(e),n)!==null);
 }continue}return {H,E,bad:false}}}
 function match(E,base){let g=[];for(let i=0;i<E.length;i++)for(let row of E[i]){let a=reduce(row[0],base);if(a)g.push({i,a,row})}L.peakGround=Math.max(L.peakGround,g.length);let I=[];
 while(true){let inI=new Set(I),owner=new Set(I.map(j=>g[j].i)),out=g.map((_,j)=>j).filter(j=>!inI.has(j)),q=[],pred=new Map();for(let j of out)if(!owner.has(g[j].i)){q.push(j);pred.set(j,-1)}let sink=-1,span=basis(I.map(j=>g[j].a));
 for(let t=0;t<q.length;t++){let j=q[t];if(!inI.has(j)){if(reduce(g[j].a,span)){sink=j;break}for(let v of I)if(!pred.has(v)){L.exchanges++;if(basis(I.filter(k=>k!==v).map(k=>g[k].a).concat(g[j].a)).length===I.length){pred.set(v,j);q.push(v)}}}else{for(let v of out)if(!pred.has(v)&&(!owner.has(g[v].i)||g[v].i===g[j].i)){L.exchanges++;pred.set(v,j);q.push(v)}}}
 if(sink<0){let J=E.map((_,i)=>i).filter(i=>!owner.has(i)||I.some(j=>g[j].i===i&&pred.has(j)));return {selected:I.map(j=>g[j]),J}}
 let next=new Set(I);for(let v=sink;v!==-1;v=pred.get(v)){if(next.has(v))next.delete(v);else next.add(v)}I=[...next];L.augmentations++;ck(new Set(I.map(j=>g[j].i)).size===I.length);ck(basis(I.map(j=>g[j].a)).length===I.length)
 }}
 function core(E,H,W){let base=basis(H.map(e=>e[0]).concat(W));let {selected,J}=match(E,base),D=E.length-selected.length;let rows=J.flatMap(i=>E[i].map(e=>e[0]));let b=basis(base.concat(rows));let K=E.map((_,i)=>i).filter(i=>!J.includes(i));let M=match(K.map(i=>E[i]),b).selected;ck(M.length===K.length);ck(J.length-(b.length-base.length)===D);return {J,K,D,r:b.length-base.length,flip:M.map(({row:[a,c]})=>[a,1^c]),rows}}
 let stats={cube:{sat:0,unsat:0,empty:0},fano:{sat:0,unsat:0,empty:0},random:{sat:0,unsat:0,empty:0},padded:[],critical:[]};
 function check(n,E,H,W,kind){let s=stats[kind],ref=[],C=closure(E,H,n);for(let x=0;x<2**n;x++){L.referenceWords++;if(holds(H,x)&&legal(E,x))ref.push(x)}s[ref.length?"sat":"unsat"]++;
 if(C.bad){ck(!ref.length);return {bad:true,models:ref.length}}
 for(let x=0;x<2**n;x++){L.referenceWords++;ck((holds(H,x)&&legal(E,x))===(holds(C.H,x)&&legal(C.E,x)))}
 let a=core(C.E,C.H,W);if(!a.J.length)s.empty++;
 let base=basis(C.H.map(e=>e[0]).concat(W)),best=-1,mins=null,m=C.E.length;
 if(m<=12){for(let mask=0;mask<2**m;mask++){let j=[];for(let i=0;i<m;i++)if(mask&(1<<i))j.push(i);let d=j.length-basis(j.flatMap(i=>C.E[i].map(([v])=>reduce(v,base)))).length;L.subsetChecks++;if(d>best){best=d;mins=mask}else if(d===best)mins&=mask}ck(best===a.D);ck(a.J.reduce((z,i)=>z|(1<<i),0)===mins)}
 let residual=a.J.map(i=>C.E[i]);let c2=closure(residual,C.H,n);let key=x=>W.map(v=>parity(v&x)).join("");let original=new Set(ref.map(key)),projected=new Set(),seen=new Set();
 for(let x=0;x<2**n;x++){L.referenceWords++;if(!holds(C.H,x)||!legal(residual,x))continue;ck(!c2.bad&&holds(c2.H,x)&&legal(c2.E,x));projected.add(key(x));let obs=W.concat(a.rows),k=obs.map(v=>parity(v&x)).join("");if(seen.has(k))continue;seen.add(k);let y=solve(C.H.concat(obs.map(v=>[v,parity(v&x)]),a.flip),n);ck(y!==null&&holds(H,y)&&legal(E,y)&&obs.every(v=>parity(v&y)===parity(v&x)));L.lifts++}
 ck(projected.size===original.size&&[...projected].every(k=>original.has(k)));return {D:a.D,core:a.J.length,rank:a.r,models:ref.length,deleted:a.K.length}}
 const point=(x,n)=>Array.from({length:n},(_,i)=>[1<<i,(x>>i)&1]);
 for(let mask=0;mask<256;mask++)check(3,Array.from({length:8},(_,x)=>x).filter(x=>mask&(1<<x)).map(x=>point(x,3)),[],[],"cube");
 let triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const nae=t=>[[ (1<<t[0])^(1<<t[1]),0],[(1<<t[0])^(1<<t[2]),0]];
 let root=triples.map(nae);stats.critical.push(check(7,root,[],[],"fano"));for(let i=0;i<7;i++)for(let c=0;c<2;c++){let E=root.slice();E[i]=triples[i].map(v=>[1<<v,c]);stats.critical.push(check(7,E,[],[],"fano"))}
 let seed=173511;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
 for(let t=0;t<120;t++){let n=5+rnd(3),m=1+rnd(9),E=Array.from({length:m},()=>Array.from({length:1+rnd(3)},()=>[1+rnd((1<<n)-1),rnd(2)])),H=Array.from({length:rnd(3)},()=>[1+rnd((1<<n)-1),rnd(2)]),W=Array.from({length:rnd(3)},()=>1+rnd((1<<n)-1));check(n,E,H,W,"random")}
 // Fano core plus independent cyclic rank-two owners sharing one core observation.
 for(let k of [2,4,8,16]){let n=7+k,E=root.concat(Array.from({length:k},(_,i)=>[[ (1<<(7+i))^1,0],[(1<<(7+(i+1)%k))^1,0]]));let C=closure(E,[],n),a=core(C.E,C.H,[]);ck(a.D===1&&a.J.length===7&&a.K.length===k);stats.padded.push({k,core:a.J.length,deleted:a.K.length,deficiency:a.D});let F=E.slice();F[0]=triples[0].map(v=>[1<<v,0]);let B=closure(F,[],n),b=core(B.E,B.H,[]);ck(!b.J.length);let y=solve(B.H.concat(b.flip),n);ck(y!==null&&legal(F,y));L.lifts++;stats.padded.at(-1).neighborCore=b.J.length}
 return {seed:173511,stats,ledger:L,scope:"finite <=23-bit mask controls; no measured bit time, peak bytes or CM"};
}
console.log(JSON.stringify(run(),null,2));
