#!/usr/bin/env node
'use strict';
// TMR-2/058: Shared-edge-AND DAG source -> exact source count; Tseitin strict proper 3CNF.
// Syntactic restricted class only; no unrestricted SAT lower bound.
const REV='TMR2_SHARED_EDGE_AND_DAG_E2E058_v1',SEED=20261115;
function readNat(s){if(!/^(0|[1-9][0-9]*)$/.test(s))throw Error('nat');let x=Number(s);if(!Number.isSafeInteger(x))throw Error('precision');return x;}
function parse(src){
 if(typeof src!=='string'||/[^\x09\x0a\x0d\x20-\x7e]/.test(src))throw Error('ASCII');
 const ls=src.trim().split(/\r?\n/).map(x=>x.trim()).filter(Boolean),h=ls[0]?.split(/\s+/);
 if(!h||h.length!==7||h[0]!=='p'||h[1]!=='nad')throw Error('header');
 const [n,a,b,g,root]=h.slice(2).map(readNat);
 if(n<2||a<1||b<1||n!==a+b||g<1||root<1||root>g||g>ls.length-1||ls.length!==g+1||n>2*g)throw Error('bounded header');
 let gates=Array(g+1).fill(null),e=0,seen=Array(n+1).fill(false);
 for(let i=1;i<ls.length;i++){
  let w=ls[i].split(/\s+/);if(w.length!==5||w[0]!=='g'||!['E','A'].includes(w[2]))throw Error('gate syntax');
  let id=readNat(w[1]),x=readNat(w[3]),y=readNat(w[4]);
  if(id<1||id>g||gates[id])throw Error('duplicate or range');
  if(w[2]==='E'){
   if(x<1||x>a||y<=a||y>n)throw Error('edge cross');
   seen[x]=seen[y]=true;e++;
  } else if(x<1||x>g||y<1||y>g){throw Error('gate reference')}
  gates[id]={id,kind:w[2],x,y};
 }
 if(e===0||n>2*e||seen.slice(1).some(z=>!z))throw Error('unused or impossible input');
 let color=new Uint8Array(g+1),order=[],stack=[[root,0]];
 while(stack.length){const [i,post]=stack.pop();if(post){color[i]=2;order.push(i);continue}
  if(color[i]===2)continue;if(color[i]===1)throw Error('cycle');color[i]=1;
  let v=gates[i];if(!v)throw Error('missing gate');stack.push([i,1]);
  if(v.kind==='A')for(const j of [v.x,v.y]){if(color[j]===1)throw Error('cycle');if(color[j]===0)stack.push([j,0]);}
 }
 if(order.length!==g)throw Error('dead gates or bad refs');
 const E=new Map();for(let i of order){const z=gates[i];if(z.kind==='E')E.set(`${z.x},${z.y}`, [z.x-1,z.y-a-1]);}
 return {n,a,b,g,root,gates,order,E:[...E.values()],sourceBytes:Buffer.byteLength(src,'ascii')};
}
function fmt(n,a,b,gates,root){const rows=[`p nad ${n} ${a} ${b} ${gates.length} ${root}`];for(let z of gates)rows.push(`g ${z.id} ${z.kind} ${z.x} ${z.y}`);return rows.join('\n')+'\n';}
function twins(P){const M=Array.from({length:P.a},()=>Array(P.b).fill(0));for(const [u,v] of P.E)M[u][v]=1;
 let A=new Map(),B=new Map();for(let u=0;u<P.a;u++){let key=M[u].join('');if(!A.has(key))A.set(key,[]);A.get(key).push(u)}
 for(let v=0;v<P.b;v++){let key=M.map(row=>row[v]).join('');if(!B.has(key))B.set(key,[]);B.get(key).push(v)}
 let L=[...A.values()],R=[...B.values()],Q=L.map(l=>R.map(r=>M[l[0]][r[0]]));
 return {L,R,Q,M};}
function cycle(T){const k=T.L.length;if(k<3||T.R.length!==k)return null;
 const AL=T.Q.map(row=>row.flatMap((v,i)=>v?[i]:[])),BR=T.R.map((_,j)=>T.Q.flatMap((row,i)=>row[j]?[i]:[]));
 if(AL.some(x=>x.length!==2)||BR.some(x=>x.length!==2))return null;
 let l=[],r=[],seenL=new Set(),seenR=new Set(),cur=0,prev=-1;
 for(let t=0;t<k;t++){if(seenL.has(cur))return null;seenL.add(cur);l.push(cur);const j=AL[cur].find(x=>x!==prev);if(j===undefined||seenR.has(j))return null;r.push(j);seenR.add(j);let next=BR[j].find(x=>x!==cur);if(next===undefined)return null;prev=j;cur=next;}
 return cur===0&&seenL.size===k&&seenR.size===k?{l,r}:null;
}
function transfer(T,C){let P=[[1n,0n],[0n,1n]],ops=0;
 for(let j=0;j<C.l.length;j++){const a=T.L[C.l[j]].length,b=T.R[C.r[j]].length,w=(1n<<BigInt(a))-1n,z=(1n<<BigInt(b));
 const M=[[z,1n],[w,w]],N=[[0n,0n],[0n,0n]];
 for(let x=0;x<2;x++)for(let y=0;y<2;y++){N[x][y]=P[x][0]*M[0][y]+P[x][1]*M[1][y];ops+=2;}P=N;}
 return {count:P[0][0]+P[1][1],ops,k:C.l.length};}
function evaluate(P,bits){let val=Array(P.g+1).fill(false);
 for(let i of P.order){let z=P.gates[i];val[i]=z.kind==='E'?!(bits[z.x-1]&&bits[z.y-1]):val[z.x]&&val[z.y];}
 return val[P.root];}
function exhaustive(P){let count=0n;for(let s=0n;s<(1n<<BigInt(P.n));s++){let bits=Array.from({length:P.n},(_,i)=>(s>>BigInt(i)&1n)===1n);if(evaluate(P,bits))count++;}return count;}
function solve(src){const P=parse(src),T=twins(P),C=cycle(T);if(C)return {route:'shared-dag-twin-cycle',...transfer(T,C),P,T,C};return {route:'fallback-exhaustive',count:exhaustive(P),P,T};}
function toCNF(P){let n=P.n,base=n+P.g,pp=base+1,qq=base+2,rr=base+3,clauses=[];
 for(let mask=1;mask<8;mask++)clauses.push([pp,qq,rr].map((v,i)=>(mask&(1<<i))?-v:v));
 for(let i of P.order){const z=P.gates[i],out=n+i;if(z.kind==='E'){
  clauses.push([-out,-z.x,-z.y],[out,z.x,pp],[out,z.y,pp]);
 }else {let x=n+z.x,y=n+z.y;
  if(x===y)clauses.push([-out,x,pp],[out,-x,pp]);
  else clauses.push([-out,x,pp],[-out,y,pp],[out,-x,-y]);
 }}
 clauses.push([n+P.root,pp,qq]);
 for(let c of clauses)if(c.length!==3||new Set(c.map(Math.abs)).size!==3)throw Error('improper strict3 clause');
 return {n:base+3,clauses};}
function evalCNF(C,bits){return C.clauses.every(c=>c.some(z=>z>0?bits[z-1]:!bits[-z-1]));}
function extend(P,bits){let val=Array(P.g+1).fill(false);for(let i of P.order){let z=P.gates[i];val[i]=z.kind==='E'?!(bits[z.x-1]&&bits[z.y-1]):val[z.x]&&val[z.y];}
 return [...bits,...val.slice(1),false,false,false];}
function bruteCNF(C){let count=0n;for(let s=0;s<2**C.n;s++){let bits=Array.from({length:C.n},(_,i)=>Math.floor(s/2**i)%2===1);if(evalCNF(C,bits))count++;}return count;}
function sharedBuild(k,g,rand){let A=[],B=[],nA=0,nB=0;
 for(let i=0;i<k;i++){A.push(Array.from({length:g},()=>++nA));B.push(Array.from({length:g},()=>++nB))}
 let E=[];for(let i=0;i<k;i++)for(let u of A[i])for(let j of [i,(i+k-1)%k])for(let v of B[j])E.push([u,nA+v]);
 // Randomly permute all original vertex names within each shore, preserving source semantics.
 if(rand){let X=Array.from({length:nA},(_,i)=>i+1),Y=Array.from({length:nB},(_,i)=>i+1);
  for(let i=nA-1;i>0;i--){let j=rand()%(i+1);[X[i],X[j]]=[X[j],X[i]]}
  for(let i=nB-1;i>0;i--){let j=rand()%(i+1);[Y[i],Y[j]]=[Y[j],Y[i]]}
  E=E.map(([u,v])=>[X[u-1],nA+Y[v-nA-1]]);
 }
 let gates=[];for(let i=0;i<E.length;i++)gates.push({id:i+1,kind:'E',x:E[i][0],y:E[i][1]});
 let acc=1;for(let i=2;i<=E.length;i++){let x=gates.length+1;gates.push({id:x,kind:'A',x:acc,y:i});let y=gates.length+1;gates.push({id:y,kind:'A',x:acc,y:x});acc=y;}
 // Scramble gate record order, not identifiers or semantics.
 if(rand)for(let i=gates.length-1;i>0;i--){let j=rand()%(i+1);[gates[i],gates[j]]=[gates[j],gates[i]]}
 return fmt(nA+nB,nA,nB,gates,acc);
}
function audit(){let seed=SEED>>>0,checks=0,recogn=0,brutes=0,cnfChecks=0,controls=0,examples=[];
 function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 function ok(b,msg){checks++;if(!b)throw Error('AUDIT '+msg)}
 for(let k=3;k<=8;k++)for(let g of [1,2,3]){let src=sharedBuild(k,g,rand),sol=solve(src),P=sol.P;ok(sol.route==='shared-dag-twin-cycle','route');ok(P.g===3*P.E.length-2,'shared gates');ok(sol.count>0n,'nonempty');recogn++;
  if(P.n<=16){ok(sol.count===exhaustive(P),'brute circuit');brutes++;}
  if(P.n<=8){let C=toCNF(P);ok(C.clauses.length<=3*P.g+8,'linear Tseitin');for(let s=0;s<2**P.n;s++){
    let bits=Array.from({length:P.n},(_,i)=>(s>>i&1)===1),ext=extend(P,bits);
    ok(evalCNF(C,ext)===evaluate(P,bits),'unique extension/equivalence');
    for(let j=P.n;j<P.n+P.g;j++){let e=ext.slice();e[j]=!e[j];ok(!evalCNF(C,e),'flipped gate');}
   }cnfChecks++;
  }
  if([3,5,8].includes(k)&&[1,3].includes(g))examples.push({k,g,originalVariables:P.n,uniqueEdges:P.E.length,sharedGates:P.g,sourceBits:8*P.sourceBytes,formulaUnrollNodes:(3n*(1n<<BigInt(P.E.length-1))-2n).toString(),count:sol.count.toString(),matrixMultiplications:sol.ops});
 }
 for(let [name,n,a,b,edges,ans] of [
 ['DISJ',8,4,4,[[1,5],[2,6],[3,7],[4,8]],81n],
 ['STAR',5,1,4,[[1,2],[1,3],[1,4],[1,5]],17n],
 ['K22',4,2,2,[[1,3],[1,4],[2,3],[2,4]],7n]]){
  let gates=edges.map(([u,v],i)=>({id:i+1,kind:'E',x:u,y:v})),acc=1;
  for(let i=2;i<=edges.length;i++){let id=gates.length+1;gates.push({id,kind:'A',x:acc,y:i});acc=id;}
  let sol=solve(fmt(n,a,b,gates,acc));ok(sol.route==='fallback-exhaustive'&&sol.count===ans,name);controls++;
 }
 // A single edge verifies true exhaustive strict-3CNF semantics including pin multiplicity.
 let one=fmt(2,1,1,[{id:1,kind:'E',x:1,y:2}],1),p=parse(one),c=toCNF(p);
 ok(bruteCNF(c)===3n,'full CNF 1edge');cnfChecks++;
 let two=fmt(4,2,2,[{id:1,kind:'E',x:1,y:3},{id:2,kind:'E',x:2,y:4},{id:3,kind:'A',x:1,y:2}],3);
 ok(bruteCNF(toCNF(parse(two)))===9n,'full CNF 2edge');cnfChecks++;
 for(let bad of [one.replace('p nad 2 1 1','p nad 999999999999 1 999999999998'),one.replace('g 1 E 1 2','g 1 E 1 1'),one.replace('g 1 E 1 2','g 1 A 1 1'),one.replace('g 1 E 1 2','g 1 E 1 2\ng 1 E 1 2'),one.replace('g 1 E 1 2','g 1 E 3 2')]){
 let rejected=false;try{solve(bad)}catch(_){rejected=true}ok(rejected,'malformed');controls++;}
 return {revision:REV,seed:SEED,checks,failures:0,recognizedSharedTwinCycles:recogn,bruteCircuitComparisons:brutes,strictCNFControlGroups:cnfChecks,hostileAndMalformed:controls,examples};}
if(require.main===module){console.log(JSON.stringify(audit(),null,2));}
module.exports={parse,solve,toCNF,evaluate,extend,sharedBuild,audit};
