#!/usr/bin/env node
'use strict';
// TMR-2/059: authenticated shared XOR-of-AND DAG -> GF(2) rank -> exact accepting-input count.
const REV='TMR2_XOR_BILINEAR_E2E059_v3',SEED=20261115;
function nat(s){if(!/^(0|[1-9][0-9]*)$/.test(s))throw Error('number');const v=Number(s);if(!Number.isSafeInteger(v))throw Error('precision');return v;}
function parse(src){
 if(typeof src!=='string'||/[^\x09\x0a\x0d\x20-\x7e]/.test(src))throw Error('ASCII');
 const lines=src.trim().split(/\r?\n/).map(s=>s.trim());const h=lines[0]?.split(/\s+/);
 if(!h||h.length!==7||h[0]!=='p'||h[1]!=='nxor')throw Error('header');
 const [n,a,b,g,root]=h.slice(2).map(nat);
 if(n<2||a<1||b<1||n!==a+b||g<1||root<1||root>g||lines.length!==g+1||n>2*g)throw Error('guard');
 const gates=Array(g+1).fill(null);let leaves=0;const used=new Uint8Array(n+1);
 for(const line of lines.slice(1)){
  const z=line.split(/\s+/);if(z.length!==5||z[0]!=='g'||!['E','X'].includes(z[2]))throw Error('record');
  const id=nat(z[1]),u=nat(z[3]),v=nat(z[4]);if(id<1||id>g||gates[id])throw Error('gate id');
  if(z[2]==='E'){if(u<1||u>a||v<=a||v>n)throw Error('shore');leaves++;used[u]=used[v]=1;}
  else if(u<1||u>g||v<1||v>g)throw Error('reference');
  gates[id]={id,op:z[2],u,v};
 }
 if(leaves<1||n>2*leaves||used.slice(1).some(x=>!x))throw Error('unused input');
 // Iterative three-color DFS authenticates even deeply nested, arbitrarily ordered DAGs.
 const color=new Uint8Array(g+1),post=[],stack=[{i:root,next:0}];
 while(stack.length){const f=stack[stack.length-1],t=gates[f.i];if(!t)throw Error('missing');
  if(color[f.i]===0)color[f.i]=1;
  if(t.op==='X'&&f.next<2){const j=f.next++===0?t.u:t.v;
   if(color[j]===1)throw Error('cycle');if(color[j]===0)stack.push({i:j,next:0});
  }else{color[f.i]=2;post.push(f.i);stack.pop();}
 }
 if(post.length!==g)throw Error('dead gate');
 return {n,a,b,g,root,gates,post,bytes:Buffer.byteLength(src)};
}
function fmt(n,a,b,gates,root){return ['p nxor',n,a,b,gates.length,root].join(' ')+'\n'+gates.map(t=>['g',t.id,t.op,t.u,t.v].join(' ')).join('\n')+'\n';}
function coefficient(P){
 const w=new Uint8Array(P.g+1),A=Array.from({length:P.a},()=>new Uint8Array(P.b));w[P.root]=1;
 for(let j=P.post.length-1;j>=0;j--){const t=P.gates[P.post[j]],h=w[t.id];if(!h)continue;
  if(t.op==='E')A[t.u-1][t.v-P.a-1]^=1;
  else {w[t.u]^=1;w[t.v]^=1;}
 }
 return {A,w};
}
function rank2(A){let a=A.map(row=>new Uint8Array(row)),r=0,b=a[0].length;
 for(let j=0;j<b&&r<a.length;j++){
  let i=r;while(i<a.length&&!a[i][j])i++;if(i===a.length)continue;
  [a[i],a[r]]=[a[r],a[i]];
  for(let k=r+1;k<a.length;k++)if(a[k][j])for(let l=j;l<b;l++)a[k][l]^=a[r][l];r++;
 }
 return r;
}
function count(P){const {A,w}=coefficient(P),r=rank2(A);const yes=r===0?0n:(1n<<BigInt(P.n-1))-(1n<<BigInt(P.n-r-1));return {yes,no:(1n<<BigInt(P.n))-yes,rank:r,A,w};}
function evaluate(P,assignment){let vals=new Uint8Array(P.g+1);for(let i of P.post){let t=P.gates[i];vals[i]=t.op==='E'?Number(((assignment>>BigInt(t.u-1))&1n)&&((assignment>>BigInt(t.v-1))&1n)):(vals[t.u]^vals[t.v]);}return vals[P.root];}
function cnf(P){const p=P.n+P.g+1,q=p+1,r=q+1;const cs=[];
 for(let mask=1;mask<8;mask++)cs.push([p,q,r].map((v,j)=>(mask&(1<<j))?-v:v));
 for(let i of P.post){const t=P.gates[i],z=P.n+i;
  if(t.op==='E'){cs.push([-z,t.u,p],[-z,t.v,p],[z,-t.u,-t.v]);}
  else {const a=P.n+t.u,b=P.n+t.v;if(t.u===t.v)cs.push([-z,p,q]);
   else cs.push([-z,a,b],[-z,-a,-b],[z,-a,b],[z,a,-b]);}
 }
 cs.push([P.n+P.root,p,q]);
 if(cs.some(c=>new Set(c.map(Math.abs)).size!==3))throw Error('nonproper CNF');return {vars:r,clauses:cs};
}
function sat(cnf,bits){return cnf.clauses.every(c=>c.some(l=>((bits>>BigInt(Math.abs(l)-1))&1n)===BigInt(l>0)));}
let checks=0,exhaustive=0,cnfChecks=0,malformed=0;function ok(x,msg){checks++;if(!x)throw Error('FAILED '+msg);}
function test(src,full){const P=parse(src),v=count(P);ok(v.yes+v.no===(1n<<BigInt(P.n)),'normalization');
 const C=cnf(P);ok(C.vars===P.n+P.g+3&&C.clauses.length<=4*P.g+8,'encoding size');
 if(P.n<=12){let found=0n;for(let a=0n;a<(1n<<BigInt(P.n));a++){found+=BigInt(evaluate(P,a));}ok(found===v.yes,'brute count');exhaustive++;}
 if(full){let found=0n;for(let a=0n;a<(1n<<BigInt(C.vars));a++)found+=BigInt(sat(C,a));ok(found===v.yes,'complete full CNF count');cnfChecks++;}
 return v;
}
function randomCase(a,b,seed,extra){let s=seed>>>0;function rng(){s=(Math.imul(s,1664525)+1013904223)>>>0;return s;}
 let gates=[];const n=a+b;for(let i=1;i<=n;i++){const u=i<=a?i:1,v=i<=a?a+1:i;gates.push({id:gates.length+1,op:'E',u,v});}
 // Each later gate is XOR of any old gates, possibly with repeated children and high fan-out.
 for(let j=0;j<extra;j++){let u=1+(rng()%gates.length),v=1+(rng()%gates.length);gates.push({id:gates.length+1,op:'X',u,v});}
 // Reachability and full original-variable use: chain all leaves, then use extra gates as needed.
 let root=1;for(let i=2;i<=n;i++){gates.push({id:gates.length+1,op:'X',u:root,v:i});root=gates.length;}
 for(let i=n+1;i<=n+extra;i++){gates.push({id:gates.length+1,op:'X',u:root,v:i});root=gates.length;}
 for(let i=gates.length-1;i>0;i--){const j=rng()%(i+1);[gates[i],gates[j]]=[gates[j],gates[i]];}
 return fmt(n,a,b,gates,root);
}
// Lowest nontrivial collision of old neighborhood-union signature: (x1,x2,y) with edges (x1,y),(x2,y).
const small=fmt(3,2,1,[{id:1,op:'E',u:1,v:3},{id:2,op:'E',u:2,v:3},{id:3,op:'X',u:1,v:2}],3);
const witness=test(small,true);ok(witness.rank===1&&witness.yes===2n,'path witness');
let v2=parse(small);ok(evaluate(v2,5n)===1&&evaluate(v2,7n)===0,'same neighborhood union different continuation');
// Duplicated child = parity cancellation, not two independently counted wires.
const cancellation=fmt(2,1,1,[{id:1,op:'E',u:1,v:2},{id:2,op:'X',u:1,v:1}],2);
const z=test(cancellation,true);ok(z.rank===0&&z.yes===0n,'cancelled output zero');
for(let n=2;n<=9;n++)for(let trial=0;trial<9;trial++){
 const a=Math.max(1,Math.floor(n/2)),b=n-a,src=randomCase(a,b,SEED+n*131+trial,trial%5);
 test(src, n<=4&&trial===0);
}
// Dense and shared larger source with genuine fan-out, fully costed symbolic rank, no brute force.
const large=test(randomCase(35,37,SEED,140),false);
// A repeated shared sub-DAG with exponentially large naive unfolding but a single live output edge.
function cancellationChain(m){const gates=[];for(let i=1;i<=m;i++)gates.push({id:i,op:'E',u:i,v:m+i});let h=1;
 for(let i=2;i<=m;i++){const t=gates.length+1;gates.push({id:t,op:'X',u:h,v:i});gates.push({id:t+1,op:'X',u:h,v:t});h=t+1;}
 return fmt(2*m,m,m,gates.slice().reverse(),h);
}
const chain=test(cancellationChain(80),false);
ok(chain.rank===1&&chain.yes===(1n<<158n),'exponential unrolling cancellation');
// Negative parser controls.
for(let src of [small.replace('p nxor','p other'),small.replace('g 3 X 1 2','g 3 X 3 2'),small.replace('g 2 E 2 3','g 2 E 2 2'),small+'g 4 E 1 3\n',small.replace('p nxor 3 2 1','p nxor 9000000 2 1'),small.replace('g 2 E 2 3','g 1 E 2 3')]){
 let bad=false;try{parse(src)}catch{bad=true;}ok(bad,'malformed source rejected');malformed++;
}
// For source language, linear-size CNF preserves exact original-input accepting multiplicity.
const summary={revision:REV,seed:SEED,checks,failures:0,brute_original_cases:exhaustive,full_CNF_enumerations:cnfChecks,malformed_rejections:malformed,small_path:{a:2,b:1,rank:witness.rank,yes:String(witness.yes),same_union_counterexample:'x=(1,0) versus x=(1,1) at y=1'},chain:{pairs:80,original_inputs:160,gates:238,rank:chain.rank,yes:String(chain.yes),naive_unfolding_nodes:'4*2^79-3'},large:{original_inputs:72,rank:large.rank,yes:String(large.yes)}};
process.stdout.write(JSON.stringify(summary,null,2)+'\n');
