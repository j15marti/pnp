function run(){
const stats={gauss:0,countQueries:0,termInspections:0,closureScans:0,pins:0,pairedQueries:0,matchRankTests:0,augmentations:0,coreRounds:0,checks:0,sourceWords:0,lifts:0}, cases=[];
const check=(b,msg)=>{stats.checks++;if(!b)throw Error(msg)};
const bit=j=>1<<j;
function parity(v){let p=0;while(v){p^=1;v&=v-1}return p}
function sys(n,eq){stats.gauss++;let rows=new Map();
 for(let [a,b] of eq){for(let j=0;j<n;j++)if((a&bit(j))&&rows.has(j)){let [r,s]=rows.get(j);a^=r;b^=s}
 if(!a){if(b)return null;continue}
 let j=0;while(!(a&bit(j)))j++;
 for(let [k,[r,s]] of rows)if(r&bit(j))rows.set(k,[r^a,s^b]);
 rows.set(j,[a,b]);}
 let anchor=0;for(let [j,[a,b]] of rows)if(b)anchor|=bit(j);
 let ker=[];for(let j=0;j<n;j++)if(!rows.has(j)){let w=bit(j);for(let [k,[r]] of rows)if(r&bit(j))w|=bit(k);ker.push(w)}
 return {rank:rows.size,rows:[...rows.values()].map(x=>x[0]),anchor,ker};
}
const span=(n,rows)=>sys(n,rows.map(a=>[a,0]));
const rank=(n,rows)=>span(n,rows).rank;
const term=(eq,c=1)=>({eq,c});
const good=bad=>[term([],1),...bad.map(t=>term(t.eq,-t.c))];
const holds=(eq,x)=>eq.every(([a,b])=>parity(a&x)===b);
const val=(f,x)=>f.reduce((s,t)=>s+(holds(t.eq,x)?t.c:0),0);
function count(n,f,H){stats.countQueries++;let sum=0n;for(let t of f){stats.termInspections++;let q=sys(n,H.concat(t.eq));if(q)sum+=BigInt(t.c)*(1n<<BigInt(n-q.rank))}return sum}
function witness(n,f,H){if(count(n,f,H)<=0n)return null;let Q=H.slice(),x=0;for(let j=0;j<n;j++){let e=[bit(j),0];if(count(n,f,Q.concat([e]))>0n)Q.push(e);else {Q.push([bit(j),1]);x|=bit(j)}}return x}
function hull(n,f,H){let a=witness(n,f,H);if(a===null)return null;let D=[];while(true){let found=false;for(let u of span(n,D).ker){let b=parity(u&a),w=witness(n,f,H.concat([[u,b^1]]));if(w!==null){D.push(w^a);found=true;break}}if(!found)return span(n,D).ker.map(u=>[u,parity(u&a)])}}
function close(n,B,H){H=H.slice();while(true){let S=sys(n,H);if(!S)return null;let changed=false;for(let bad of B){stats.closureScans++;let h=hull(n,good(bad),H);if(h===null)return null;for(let e of h){let q=sys(n,H.concat([e]));check(q!==null,"closure conflict");if(q.rank>S.rank){H.push(e);stats.pins++;changed=true;break}}if(changed)break}if(!changed)return H}}
function uniform(n,bad,H,P){
 const left=H.concat(P.map(a=>[a,0])); // left unused; actual P equality below
 const guard=H.concat(H.map(([a,b])=>[a<<n,b]),P.map(a=>[a|(a<<n),0]));
 const pair=[];for(let s of bad)for(let t of bad)pair.push(term(s.eq.concat(t.eq.map(([a,b])=>[a<<n,b])),s.c*t.c));
 const query=Q=>{stats.pairedQueries++;return count(2*n,pair,guard.concat(Q.map(([a,b])=>[a|(a<<n),b])))};
 let D=[];while(true){let found=false;for(let u of span(n,D).ker){if(query([[u,1]])===0n)continue;let Q=[[u,1]],w=0;for(let j=0;j<n;j++){let e=[bit(j),0];if(query(Q.concat([e]))>0n)Q.push(e);else{Q.push([bit(j),1]);w|=bit(j)}}check(w!==0,"zero direction");D.push(w);found=true;break}if(!found)return span(n,D).ker}
}
function match(n,U,owners,Q){
 const ground=owners.flatMap(i=>U[i].map(a=>({i,a})));let I=new Set(),base=rank(n,Q);
 const rr=(ids)=>{stats.matchRankTests++;return rank(n,Q.concat(ids.map(j=>ground[j].a)))};
 while(true){let chosen=[...I],used=new Set(chosen.map(j=>ground[j].i)),prev=new Map(),queue=[];
 for(let j=0;j<ground.length;j++)if(!I.has(j)&&!used.has(ground[j].i)){prev.set(j,-1);queue.push(j)}
 let sink=-1;
 for(let k=0;k<queue.length;k++){let j=queue[k];if(!I.has(j)){
 if(rr(chosen.concat(j))===base+chosen.length+1){sink=j;break}
 for(let l of chosen)if(!prev.has(l)&&rr(chosen.filter(t=>t!==l).concat(j))===base+chosen.length){prev.set(l,j);queue.push(l)}
 }else{for(let l=0;l<ground.length;l++)if(!I.has(l)&&!prev.has(l)&&(!used.has(ground[l].i)||ground[l].i===ground[j].i)){prev.set(l,j);queue.push(l)}}}
 if(sink<0){let C=owners.filter(i=>!used.has(i)||chosen.some(j=>ground[j].i===i&&prev.has(j)));return {C,selected:chosen.map(j=>ground[j])}}
 for(let j=sink;j!==-1;j=prev.get(j)){if(I.has(j))I.delete(j);else I.add(j)}stats.augmentations++;
 }}
function core(n,U,V,owners,Q){let C=[];while(true){stats.coreRounds++;let R=owners.filter(i=>!C.includes(i)),q=Q.concat(C.flatMap(i=>V[i]));let m=match(n,U,R,q);if(!m.C.length)return {C,selected:m.selected};C=C.concat(m.C)}}
const key=(P,x)=>P.map(u=>parity(u&x)).join("");
function audit(name,n,B,H0,P){
 let H=close(n,B,H0),src=new Map(),refWords=[];
 for(let x=0;x<bit(n);x++){stats.sourceWords++;if(holds(H0,x)&&B.every(b=>val(b,x)===0)){src.set(key(P,x),x);refWords.push(x)}}
 if(H===null){check(src.size===0,"false closure UNSAT");cases.push({name,n,sourceFibers:0,core:null,legacy:null});return}
 for(let x of refWords)check(holds(H,x),"lost source model");
 let owners=B.map((_,i)=>i).filter(i=>count(n,B[i],H)>0n),Q=H.map(e=>e[0]).concat(P);
 let U=B.map(b=>uniform(n,b,H,P)),U0=B.map(b=>uniform(n,b,H,[])),V=B.map(b=>span(n,b.flatMap(t=>t.eq.map(e=>e[0]))).rows);
 // Independent brute audit of all uniform row spaces.
 for(let i of owners){let a=new Map(),D=[];for(let x=0;x<bit(n);x++)if(holds(H,x)&&val(B[i],x)===1){let k=key(P,x);if(a.has(k))D.push(x^a.get(k));else a.set(k,x)}
 let K=span(n,D).ker;check(rank(n,U[i])===rank(n,K)&&rank(n,U[i].concat(K))===rank(n,K),"uniform space mismatch")}
 let z=core(n,U,V,owners,Q),old=core(n,U0,V,owners,Q);
 check(z.C.every(i=>old.C.includes(i)),"core not monotone");
 // Independently audit least feasible set by all retained subsets (small controls only).
 if(owners.length<=9){for(let mask=0;mask<bit(owners.length);mask++){let S=owners.filter((_,j)=>mask&bit(j)),R=owners.filter(i=>!S.includes(i)),q=Q.concat(S.flatMap(i=>V[i])),base=rank(n,q),ok=true;
 for(let t=1;t<bit(R.length)&&ok;t++){let J=R.filter((_,j)=>t&bit(j));if(rank(n,q.concat(J.flatMap(i=>U[i])))-base<J.length)ok=false}
 if(ok)check(z.C.every(i=>S.includes(i)),"minimality")}}
 let H2=close(n,z.C.map(i=>B[i]),H),dst=new Set();
 for(let x=0;x<bit(n);x++)if(H2&&holds(H2,x)&&z.C.every(i=>val(B[i],x)===0)){let k=key(P,x);dst.add(k);let guard=H2.concat(P.map(a=>[a,parity(a&x)]));let fix=guard.concat(z.C.flatMap(i=>V[i].map(a=>[a,parity(a&x)])));
 for(let {i,a} of z.selected){let c0=count(n,B[i],H.concat(P.map(p=>[p,parity(p&x)]),[[a,0]])),c1=count(n,B[i],H.concat(P.map(p=>[p,parity(p&x)]),[[a,1]]));check(c0===0n||c1===0n,"ambiguous side");fix.push([a,c0>0n?1:0])}
 let w=sys(n,fix);check(w!==null,"inconsistent lift");check(key(P,w.anchor)===k&&holds(H0,w.anchor)&&B.every(b=>val(b,w.anchor)===0),"bad lift");stats.lifts++}
 check(dst.size===src.size&&[...dst].every(k=>src.has(k)),"projection mismatch");
 cases.push({name,n,sourceFibers:src.size,sourceModels:refWords.length,core:z.C.length,legacy:old.C.length,removed:owners.length-z.C.length});
}
const nonlinear=(a,b,x)=>[term([[bit(x),0]]),term([[bit(x),0],[bit(a),1],[bit(b),1]],-1),term([[bit(x),1],[bit(a),1],[bit(b),1]])];
const neq=(a,b,x)=>good(nonlinear(a,b,x));
audit("nonlinear graph",3,[nonlinear(0,1,2)],[],[1,2]);
audit("opposing graphs",3,[nonlinear(0,1,2),neq(0,1,2)],[],[1,2]);
audit("guarded graph",3,[nonlinear(0,1,2)],[[1^2,0]],[1,2]);
for(let k=1;k<=6;k++)audit("shared nonlinear tails "+k,k+2,Array.from({length:k},(_,i)=>nonlinear(0,1,i+2)),[],[1,2]);
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const F=fano.map(([a,b,c])=>[term([[bit(a),0],[bit(b),0],[bit(c),0]]),term([[bit(a),1],[bit(b),1],[bit(c),1]])]);
audit("Fano root",7,F,[],[]);for(let i=0;i<7;i++)for(let j=0;j<2;j++)audit("Fano neighbor "+i+"/"+j,7,F.map((b,k)=>k===i?[b[j]]:b),[],[]);
audit("Fano plus nonlinear",10,F.concat([nonlinear(7,8,9)]),[],[bit(7),bit(8)]);
audit("Fano neighbor plus nonlinear",10,F.map((b,k)=>k===0?[b[0]]:b).concat([nonlinear(7,8,9)]),[],[bit(7),bit(8)]);
let seed=2081125;const rnd=m=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%m};
for(let t=0;t<30;t++){let n=4+(t%2),P=[1,2],B=[];for(let j=0;j<2+(t%3);j++){let x=2+rnd(n-2);if(rnd(3)===0)B.push(nonlinear(0,1,x));else{let bad=[];for(let w=0;w<bit(n);w++)if(rnd(5)===0)bad.push(term(Array.from({length:n},(_,i)=>[bit(i),(w>>i)&1])));B.push(bad)}}audit("seeded "+t,n,B,t%5===0?[[3,t%2]]:[],P)}
return {seed:2081125,stats,cases,sat:cases.filter(c=>c.sourceFibers>0).length,unsat:cases.filter(c=>c.sourceFibers===0).length};
}
console.log(JSON.stringify(run(),null,2));
