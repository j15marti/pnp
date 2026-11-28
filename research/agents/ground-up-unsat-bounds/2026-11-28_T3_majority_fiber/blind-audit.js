const fs=require('node:fs');
const pins={"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"result":["research/agents/ground-up-unsat-bounds/2026-11-28_T3_majority_fiber/results.json","853ec31b6683c302886a156357fb00be501908b6"],"peer":["research/proof-spine-2026-11-26/four-partition-nae/2026-11-27_2248_T2_degree_locality/AND-SEAM-5-3-NO.cert.json",null]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const audit=function audit(data){
const {sha,canon,key,solve,check}=new Function(data.native+";return {sha,canon,key,solve,check};")(),A=(t,m)=>{if(!t)throw Error(m)},enc=x=>JSON.stringify(x)+"\n";
function choose(b,k){return Array.from({length:2**b},(_,w)=>Array.from({length:b},(_,i)=>i).filter(i=>w>>i&1)).filter(a=>a.length===k)}
function lift(B,d){let b=2*d+1,Q=choose(b,d+1),C=[];for(let c of B.C){let rows=[[]];for(let l of c){let x=(Math.abs(l)-1)*b;rows=rows.flatMap(r=>Q.map(q=>[...r,...q.map(i=>Math.sign(l)*(x+i+1))]))}C.push(...rows)}return {n:B.n*b,C}}
function bytes(n,C){return "p cnf "+n+" "+C.length+"\n"+C.map(c=>c.join(" ")+" 0").join("\n")+"\n"}
function blind(C,n){
 let S=new Set(),first=new Map(),lits=0,queries=0,queryLits=0;
 for(let c of C){S.add(key(canon(c)));for(let l of c){lits++;if(!first.has(Math.abs(l)))first.set(Math.abs(l),{c,l})}}
 A(first.size===n&&S.size===C.length,"unused/duplicate");let adj=Array.from({length:n+1},()=>new Set());
 for(let i=1;i<=n;i++){let {c,l}=first.get(i),used=new Set(c.map(Math.abs));for(let j=1;j<=n;j++){if(used.has(j))continue;queries++;queryLits+=c.length;if(S.has(key(canon(c.map(x=>x===l?Math.sign(l)*j:x))))){adj[i].add(j);adj[j].add(i)}}}
 let blocks=[],owner=new Map();for(let i=1;i<=n;i++){if(owner.has(i))continue;let q=[i],k=blocks.length+1;owner.set(i,k);for(let j=0;j<q.length;j++)for(let z of adj[q[j]])if(!owner.has(z)){q.push(z);owner.set(z,k)}blocks.push(q.sort((a,b)=>a-b))}
 let b=blocks[0].length;A(b>=3&&b%2===1&&blocks.every(q=>q.length===b),"not equal odd blocks");let d=(b-1)/2,Q=choose(b,d+1),rows=new Map(),verificationLits=0;
 for(let c of C){let m=new Map();for(let l of c){verificationLits++;let v=owner.get(Math.abs(l))*Math.sign(l);A(!m.has(-v),"mixed sign");if(!m.has(v))m.set(v,[]);m.get(v).push(Math.abs(l))}
 let row=canon([...m.keys()]);A([...m.values()].every(a=>a.length===d+1&&new Set(a).size===a.length),"quota");
 let sig=row.map(v=>m.get(v).sort((a,b)=>a-b).join(",")).join(";"),k=key(row);if(!rows.has(k))rows.set(k,{row,sigs:new Set()});A(!rows.get(k).sigs.has(sig),"repeat");rows.get(k).sigs.add(sig)}
 for(let f of rows.values())A(BigInt(f.sigs.size)===BigInt(Q.length)**BigInt(f.row.length),"missing product");
 return {blocks,phase:[...rows.values()].map(f=>f.row),lits,queries,queryLits,verificationLits,edges:adj.reduce((a,s)=>a+s.size,0)/2,d}
}
let out=[];
for(let f of JSON.parse(data.result).family){let L=lift(f.base,f.d),Y=lift(f.yesBase,f.d),raw=bytes(L.n,L.C),yr=bytes(Y.n,Y.C);A(sha(raw)===f.source.sha&&raw.length*8===f.source.N&&sha(yr)===f.yes.sha&&yr.length*8===f.yes.N,"input hash "+f.m+","+f.d);let B=blind(L.C,L.n),YB=blind(Y.C,Y.n),r=solve(B.phase);A(r.status==="UNSAT","quotient");let ck=check(B.phase,r.tree);let yw=0;for(let c of Y.C){let sat=false;for(let l of c){yw++;if(f.yes.witness[Math.abs(l)]===+(l>0))sat=true}A(sat,"witness")}
 let relabel=null;if(f.m===3&&f.d<=2){let perm=Array.from({length:L.n},(_,i)=>i+1),seed=271128;for(let i=perm.length-1;i>0;i--){seed=(Math.imul(seed,1664525)+1013904223)>>>0;let j=seed%(i+1);[perm[i],perm[j]]=[perm[j],perm[i]]}let C=L.C.map(c=>canon(c.map(l=>Math.sign(l)*perm[Math.abs(l)-1]))),R=blind(C,L.n),P=solve(R.phase),rb=bytes(L.n,C);A(P.status==="UNSAT","relabel");A(enc(B.blocks.map(q=>q.map(v=>perm[v-1]).sort((a,b)=>a-b).join(",")).sort())===enc(R.blocks.map(q=>q.join(",")).sort()),"adapter");relabel={sha:sha(rb),N:rb.length*8,perm,blind:R,proof:P,check:check(R.phase,P.tree)}}
 out.push({m:f.m,d:f.d,n:L.n,clauses:L.C.length,no:f.source,yes:f.yes,blind:B,proof:r,check:ck,yesBlind:YB,yesWitnessVisits:yw,relabel})
}
let p=JSON.parse(data.peer),h=sha(data.peer);A(h==="1509f7012e33a574f7e14d4b8de6be5da2c8161e6f2590cf99333dfbe17fcee7","peer hash");A(sha(p.dimacs)===p.instance_id.split(":").at(-1)&&p.dimacs.length*8===p.original_N_bits,"peer input");let C=p.dimacs.trim().split("\n").slice(1).map(s=>s.trim().split(/\s+/).map(Number).slice(0,-1)),tests=0,litTests=0;for(let e of p.proof.edges){let v=[...p.proof.blocks[e.i],...p.proof.blocks[e.j]];for(let w=0;w<64;w++){let actual=C.slice(e.clauses[0]-1,e.clauses[1]).every(c=>c.some(l=>{litTests++;return ((w>>v.indexOf(Math.abs(l)))&1)===+(l>0)}));A(actual===(((w&7)===7)!==((w>>3)===7)),"peer seam");tests++}}A(p.proof.edges.length%2===1&&p.proof.edges.every((e,i)=>e.j===p.proof.edges[(i+1)%p.proof.edges.length].i&&!e.equal),"peer cycle");
return {out,peer:{instance:p.instance,instance_id:p.instance_id,N:p.original_N_bits,certificateId:"CERT-v1:sha256:"+h,tests,litTests}}
};
console.log(JSON.stringify(audit(data),null,2));
