function checker(){
const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let checks=0,batches=0,words=0;const ck=(v)=>{checks++;if(!v)throw Error("assertion "+checks)};
const bit=(x,i)=>Number((x>>BigInt(i))&1n);
const obs=(x,e)=>((bit(x,e[0])^bit(x,e[1]))+2*(bit(x,e[0])^bit(x,e[2])));
const models=(E,f)=>Array.from({length:128},(_,i)=>BigInt(i)).filter(x=>E.every((e,j)=>obs(x,e)!==f[j]));
ck(models(lines,Array(7).fill(0)).length===0);let nb=[];for(let i=0;i<7;i++)for(let f=1;f<=3;f++){let a=Array(7).fill(0);a[i]=f;let z=models(lines,a);ck(z.length===10);nb.push(z.length)}
const base=lines.slice(1);let eq=models(base,Array(6).fill(0));ck(eq.length===10);ck(eq.every(x=>obs(x,lines[0])===0));ck(eq.some(x=>bit(x,0)===0)&&eq.some(x=>bit(x,0)===1));
function chain(q){let E=[],cur=0,n=1,path=[0];for(let k=0;k<4*q-2;k++){let v=[cur,...Array.from({length:6},()=>n++)];E.push(...base.map(e=>e.map(i=>v[i])));cur=v[1];path.push(cur)}let a=Array.from({length:2*q},(_,i)=>path[2*i]);return {E,n,pairs:Array.from({length:q},(_,i)=>[a[2*i],a[2*i+1]])}}
function allTernary(q){return Array.from({length:3**q},(_,i)=>Array.from({length:q},(_,j)=>Math.floor(i/3**j)%3-1))}
function chart(n,pairs,g){let rep=Array.from({length:n},(_,i)=>i),offset=0n;for(let j=0;j<g.length;j++)if(g[j]>=0){let [a,b]=pairs[j];rep[b]=a;if(g[j])offset^=1n<<BigInt(b)}return {rep,offset}}
function image(E,x){let y=0n;for(let j=0;j<E.length;j++)y|=BigInt(obs(x,E[j]))<<BigInt(2*j);return y}
function key(E,n,C){let basis=new Map();const reduce=(v)=>{for(let k of [...basis.keys()].sort((a,b)=>b-a))if((v>>BigInt(k))&1n)v^=basis.get(k);return v};for(let j=0;j<n;j++)if(C.rep[j]===j){let x=0n;for(let k=0;k<n;k++)if(C.rep[k]===j)x|=1n<<BigInt(k);let v=reduce(image(E,x));if(v){let k=v.toString(2).length-1;for(let [l,w] of basis)if((w>>BigInt(k))&1n)basis.set(l,w^v);basis.set(k,v)}}return [...basis.entries()].sort((a,b)=>a[0]-b[0]).map(x=>x[1].toString(16)).join(",")+"|"+reduce(image(E,C.offset)).toString(16)}
function testBatch(E,J,C){const coords=[...new Set(J.flatMap(j=>E[j].map(i=>C.rep[i])))];let actual=new Set(),accepted=new Set();for(let b=0;b<2**coords.length;b++){let x=C.offset;for(let j=0;j<coords.length;j++)if((b>>j)&1)for(const i of new Set(J.flatMap(k=>E[k])))if(C.rep[i]===coords[j])x^=1n<<BigInt(i);let v=J.map(j=>obs(x,E[j]));actual.add(v.join(","));if(v.every(z=>z!==0))accepted.add(v.join(","));words++}ck(actual.size===4**J.length);ck(accepted.size===3**J.length);batches++}
let result=[];for(let q of [1,2,3]){let {E,n,pairs}=chain(q);let keys=new Set(),full=new Set(),sat=0,unsat=0;let J=E.map((e,i)=>[i]);for(let i=0;i<E.length;i++)for(let j=i+1;j<E.length;j++)J.push([i,j]);for(let g of allTernary(q)){let C=chart(n,pairs,g);let k=key(E,n,C);ck(!keys.has(k));keys.add(k);if(g.every(x=>x>=0))full.add(k);if(g.includes(1))unsat++;else sat++;for(let j of J)testBatch(E,j,C)}ck(keys.size===3**q&&full.size===2**q);ck(sat===2**q&&unsat===3**q-2**q);result.push({q,variables:n,owners:E.length,partial_charts:keys.size,full_keys:full.size,sat,unsat,batches_per_chart:J.length})}
return {fano_models:0,fano_sign_neighbors:nb,deleted_line_models:eq.length,chains:result,checks,batches,enumerated_local_words:words,note:"Chain labels certified by exhaustive seven-variable equality gadget projection and gluing, not full source enumeration; no high-girth UNSAT construction or portfolio run."}
}
console.log(JSON.stringify(checker(),null,2));
