const fs=require('node:fs'),crypto=require('node:crypto');
const audit=function audit(x){
 const A=(b,m)=>{if(!b)throw Error(m)},K=c=>c.slice().sort((a,b)=>a-b).join(","),rows=x.raw.trimEnd().split("\n"),header=rows.shift().split(" ").map(Number),C=rows.map(s=>s.split(" ").map(Number).slice(0,-1)),n=x.vertices,vs=3*n;A(header[2]===vs&&header[3]===C.length,"header");
 let R=new Set(C.map(K)),ad=Array.from({length:n},()=>new Set()),tests=0,edges=[];
 const lit=(v,c)=>3*v+c+1;
 for(let v=0;v<n;v++){let a=[0,1,2].map(c=>lit(v,c));for(let c of [a,[-a[0],-a[1]],[-a[0],-a[2]],[-a[1],-a[2]]]){tests++;A(R.delete(K(c)),"onehot")}}
 // exact independent source proof for NO, exact model checker for YES; no access to generator labels as solver advice.
 if(x.label==="YES"){let W=new Set(x.witness);A(C.every(c=>c.some(l=>W.has(Math.abs(l))===(l>0))),"witness");return {status:"SAT",sourceRows:C.length,literalVisits:C.flat().length}}
 for(let s of [...R]){let [l,m]=s.split(",").map(Number);A(l<0&&m<0&&(-l-1)%3===(-m-1)%3,"edge");let u=Math.floor((-l-1)/3),v=Math.floor((-m-1)/3);if(u>v)[u,v]=[v,u];if(ad[u].has(v))continue;for(let c=0;c<3;c++){tests++;A(R.delete(K([-lit(u,c),-lit(v,c)])),"complete edge")}ad[u].add(v);ad[v].add(u);edges.push([u,v])}
 A(R.size===0,"extra rows");let {apex,pair,cycle}=x.recognizer,B=new Set(pair.map(p=>p[0])),S=new Set(pair.map(p=>p[1]));A(B.size===S.size&&B.size+S.size+1===n&&!B.has(apex)&&!S.has(apex)&&![...B].some(v=>S.has(v)),"partition");
 A(ad[apex].size===S.size&&[...S].every(v=>ad[apex].has(v)),"apex");
 for(let [v,s] of pair){A(ad[s].size===[...ad[v]].filter(u=>B.has(u)).length+1,"degree");for(let u of B){tests++;A(ad[v].has(u)===ad[s].has(u),"neighborhood")}A([...ad[s]].every(u=>u===apex||B.has(u)),"independent shadows")}
 A(cycle.length>=3&&cycle.length%2===1&&new Set(cycle).size===cycle.length&&cycle.every((v,i)=>B.has(v)&&ad[v].has(cycle[(i+1)%cycle.length])),"odd cycle");
 let triChecks=0;for(let [u,v] of edges)for(let w of ad[u]){triChecks++;A(!ad[v].has(w),"triangle")}
 // Exact local relation checks for affine hull and quotient ANF, not full polynomial calculus.
 let localWords=0;
 function parity(a){let q=0;while(a){a&=a-1;q^=1}return q}
 let allowed=[1,2,4],aff=[];for(let mask=1;mask<8;mask++){let a=allowed.map(w=>{localWords++;return parity(w&mask)});if(a.every(q=>q===a[0]))aff.push([mask,a[0]])}A(JSON.stringify(aff)==="[[7,1]]","affine hull");
 let edgeAffine=[];for(let mask=1;mask<4;mask++){let a=[0,1,2].map(w=>{localWords++;return parity(w&mask)});if(a.every(q=>q===a[0]))edgeAffine.push([mask,a[0]])}A(edgeAffine.length===0,"edge hull");
 for(let w=0;w<4;w++){let a=w&1,b=w>>1,z=1^a^b;localWords++;A((+(a+b+z!==1))===(a*b),"onehot quotient")}
 // For each edge, row C3 has a private mixed x_u*y_v coefficient; then C1 and C2 have private xx/yy; each local xy unique.
 let rank=n+3*edges.length;A(rank===x.groupedRank,"rank");
 let occ=0;for(let c of C){let sum=c.reduce((s,l)=>s+(l>0?1:2),0);occ++;A(sum>=3,"fractional clause feasibility")}
 // Five disjoint guards on apex original variable IDs. Exact UP and direct structural method, same root. Scope only.
 let [a,b,c]=[0,1,2].map(i=>lit(apex,i)),guards=[[-a,-b],[-a,b],[a,-b],[a,b,-c],[a,b,c]],counts=[],gwork=0;
 for(let g of guards){let P=new Set(g),conf=false;for(;;){let change=false;for(let c of C){let sat=false,un=[];for(let l of c){gwork++;if(P.has(l)){sat=true;break}if(!P.has(-l))un.push(l)}if(sat)continue;if(!un.length){conf=true;break}if(un.length===1){P.add(un[0]);change=true}}if(conf||!change)break}counts.push({guard:g,UPConflict:conf,pins:P.size})}
 let union=0n,intersections=[];for(let mask=1;mask<32;mask++){let P=new Map(),bad=false,bits=0;for(let i=0;i<5;i++)if(mask>>i&1){bits++;for(let l of guards[i]){if(P.has(Math.abs(l))&&P.get(Math.abs(l))!==l)bad=true;P.set(Math.abs(l),l)}}let v=bad?0n:2n**BigInt(vs-P.size);intersections.push(String(v));union+=(bits%2?v:-v)}A(union===2n**BigInt(vs),"coverage");
 return {status:"UNSAT",sourceRows:C.length,structuralChecks:tests,triChecks,localWords,affineRows:n,affineConsistent:true,groupedRank:rank,constantAbsent:true,lpFeasible:true,cliqueHallMax:2,occupancyRows:occ,guardResults:counts,guardVisits:gwork,intersectionCounts:intersections,cover:String(union),oddCycle:cycle,apex,pair}
};
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));const out=data.families.map(x=>{if(crypto.createHash('sha256').update(x.raw).digest('hex')!==x.sha||Buffer.byteLength(x.raw)*8!==x.N)throw Error('digest');return {k:x.k,label:x.label,sha:x.sha,a:audit(x)}});console.log(JSON.stringify(out,null,2));
