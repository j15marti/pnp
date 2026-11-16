#!/usr/bin/env node
'use strict';
// Independent TMR-5/057 end-to-end authenticated shared OR/XOR/AND DAG audit.
const REV='TMR5_OR_BILINEAR_E2E057_v1',SEED=20261115;
let checks=0,brute=0,cnfTests=0,malformed=0;
function ok(b,tag){checks++;if(!b)throw Error('ASSERT '+tag);}
function nat(s){if(!/^(0|[1-9][0-9]*)$/.test(s))throw Error('decimal');const k=Number(s);if(!Number.isSafeInteger(k))throw Error('large integer');return k;}
function fmt(n,a,b,gs,root){return ['p norxor',n,a,b,gs.length,root].join(' ')+'\n'+gs.map(t=>['g',t.id,t.op,t.u,t.v].join(' ')).join('\n')+'\n';}
function parse(src){
 if(typeof src!=='string'||/[^\x09\x0a\x0d\x20-\x7e]/.test(src))throw Error('ASCII');
 const lines=src.trim().split(/\r?\n/).map(x=>x.trim()),h=lines[0]?.split(/\s+/);
 if(!h||h.length!==7||h[0]!=='p'||h[1]!=='norxor')throw Error('header');
 const [n,a,b,g,root]=h.slice(2).map(nat);
 if(n<2||a<1||b<1||n!==a+b||g<1||g>src.length||root<1||root>g||lines.length!==g+1||n>2*g)throw Error('arity');
 const gs=Array(g+1).fill(null),used=new Uint8Array(n+1);let E=0;
 for(const line of lines.slice(1)){
  const z=line.split(/\s+/);if(z.length!==5||z[0]!=='g'||!['E','X','O'].includes(z[2]))throw Error('record');
  const id=nat(z[1]),u=nat(z[3]),v=nat(z[4]);if(id<1||id>g||gs[id])throw Error('gateID');
  if(z[2]==='E'){
   if(u<1||u>a||v<=a||v>n)throw Error('edge');used[u]=used[v]=1;E++;
  }else if(u<1||u>g||v<1||v>g)throw Error('reference');
  gs[id]={id,op:z[2],u,v};
 }
 if(n>2*E||used.slice(1).some(x=>!x))throw Error('unused original');
 const color=new Uint8Array(g+1),post=[],st=[{id:root,next:0}];
 while(st.length){const f=st[st.length-1],t=gs[f.id];if(!t)throw Error('missing');
  if(!color[f.id])color[f.id]=1;
  if(t.op!=='E'&&f.next<2){const child=f.next++===0?t.u:t.v;
   if(t.op==='X'&&gs[child]?.op==='O')throw Error('OR within XOR');
   if(color[child]===1)throw Error('cycle');if(color[child]===0)st.push({id:child,next:0});
  }else {color[f.id]=2;post.push(f.id);st.pop();}
 }
 if(post.length!==g)throw Error('dead gate');
 const layers=[],seen=new Set(),queue=[root];
 while(queue.length){const id=queue.pop(),t=gs[id];if(t.op==='O'){
   if(seen.has(id))continue;seen.add(id);queue.push(t.u,t.v);
  }else if(!seen.has(id)){seen.add(id);layers.push(id);}
 }
 if(!layers.length)throw Error('no layers');
 return {n,a,b,g,root,gs,post,layers,N:Buffer.byteLength(src)};
}
function coefficient(P,root){const w=new Uint8Array(P.g+1);w[root]=1;
 const A=Array.from({length:P.a},()=>0n);
 for(let k=P.post.length-1;k>=0;k--){const t=P.gs[P.post[k]];if(!w[t.id])continue;
  if(t.op==='E')A[t.u-1]^=1n<<BigInt(t.v-P.a-1);
  else if(t.op==='X'){w[t.u]^=1;w[t.v]^=1;}
  else throw Error('OR contamination');
 }return A;
}
function rank2(matrix,b){const A=matrix.slice();let r=0;
 for(let col=0;col<b&&r<A.length;col++){
  let pivot=r;while(pivot<A.length&&(((A[pivot]>>BigInt(col))&1n)===0n))pivot++;
  if(pivot===A.length)continue;[A[r],A[pivot]]=[A[pivot],A[r]];
  for(let i=r+1;i<A.length;i++)if((A[i]>>BigInt(col))&1n)A[i]^=A[r];r++;
 }return r;
}
function exact(P){const matrices=P.layers.map(root=>coefficient(P,root)),q=matrices.length;
 let acc=Array(P.a).fill(0n),previousGray=0n,weighted=0n;const hist=[];
 // Streaming Gray-code rank sum, with NO storage proportional to 2^q.
 for(let z=0n,limit=1n<<BigInt(q);z<limit;z++){
  const gray=z^(z>>1n),delta=gray^previousGray;
  if(delta!==0n){let idx=0;while((delta>>BigInt(idx))!==1n)idx++;
   for(let i=0;i<P.a;i++)acc[i]^=matrices[idx][i];}
  const r=rank2(acc,P.b);weighted+=1n<<BigInt(P.n-r);hist[r]=(hist[r]||0)+1;
  previousGray=gray;
 }
 const divisor=1n<<BigInt(q);if(weighted%divisor!==0n)throw Error('nonintegral inversion');
 const zero=weighted/divisor,yes=(1n<<BigInt(P.n))-zero;
 return {yes,zero,q,ranks:hist,matrices,weighted};
}
function evalGates(P,bits){const v=new Uint8Array(P.g+1);
 for(let id of P.post){const t=P.gs[id];v[id]=t.op==='E'?Number(((bits>>BigInt(t.u-1))&1n)&&((bits>>BigInt(t.v-1))&1n)):(t.op==='X'?v[t.u]^v[t.v]:v[t.u]|v[t.v]);}
 return v[P.root];
}
function cnf(P){const p=P.n+P.g+1,q=p+1,r=q+1,cs=[];
 for(let mask=1;mask<8;mask++)cs.push([p,q,r].map((v,j)=>(mask&(1<<j))?-v:v));
 for(let id of P.post){const t=P.gs[id],z=P.n+id;
  if(t.op==='E')cs.push([-z,t.u,p],[-z,t.v,p],[z,-t.u,-t.v]);
  else {const a=P.n+t.u,b=P.n+t.v;
   if(t.u===t.v){if(t.op==='X')cs.push([-z,p,q]);
    else cs.push([-z,a,p],[z,-a,p]);
   }else if(t.op==='X')cs.push([-z,a,b],[-z,-a,-b],[z,-a,b],[z,a,-b]);
   else cs.push([z,-a,p],[z,-b,p],[-z,a,b]);
  }
 }
 cs.push([P.n+P.root,p,q]);
 if(cs.some(c=>new Set(c.map(Math.abs)).size!==3))throw Error('nonproper CNF');
 return {vars:r,clauses:cs};
}
function test(src,fullCNF=false){const P=parse(src),e=exact(P),C=cnf(P);
 ok(C.vars===P.n+P.g+3&&C.clauses.length<=4*P.g+8,'CNF size');
 ok(e.yes>=0n&&e.zero>=0n&&e.yes+e.zero===(1n<<BigInt(P.n)),'count range');
 if(P.n<=10){let got=0n;for(let z=0n;z<(1n<<BigInt(P.n));z++)got+=BigInt(evalGates(P,z));
  ok(got===e.yes,'brute original');brute++;
 }
 if(fullCNF){const orig=1<<P.n,aux=1<<(P.g+3);let counted=0n;
  // Prove UNIQUE auxiliary extension for every original input by exhaustive assignments.
  for(let x=0;x<orig;x++){let local=0,expected=evalGates(P,BigInt(x));
   for(let y=0;y<aux;y++){
    const z=(BigInt(y)<<BigInt(P.n))|BigInt(x);
    if(C.clauses.every(cl=>cl.some(l=>((z>>BigInt(Math.abs(l)-1))&1n)===BigInt(l>0))))local++;
   }
   ok(local===expected,'parsimonious output');counted+=BigInt(local);
  }ok(counted===e.yes,'CNF total');cnfTests++;
 }return {P,e,C};
}
function build(a,b,variant){const n=a+b,gs=[];function add(op,u,v){const id=gs.length+1;gs.push({id,op,u,v});return id;}
 const edges=[];for(let i=1;i<=n;i++)edges.push(add('E',i<=a?i:1,i<=a?a+1:i));
 let h=edges[0];for(let j=1;j<edges.length;j++)h=add('X',h,edges[j]);
 const y=variant%3===0?edges[0]:variant%3===1?edges[edges.length-1]:h;
 const dup=variant%2===0?add('X',y,y):add('X',h,edges[0]);
 const layer2=add('X',dup,y);const o=add('O',h,layer2);
 return fmt(n,a,b,gs,o);
}
const small=fmt(3,2,1,[{id:1,op:'E',u:1,v:3},{id:2,op:'E',u:2,v:3},{id:3,op:'O',u:1,v:2}],3);
const a=test(small,true);ok(a.e.yes===3n&&a.e.q===2,'OR shared y 3 of 8');
const duplicated=fmt(2,1,1,[{id:1,op:'E',u:1,v:2},{id:2,op:'X',u:1,v:1},{id:3,op:'X',u:1,v:2},{id:4,op:'O',u:1,v:3}],4);
const b=test(duplicated,true);ok(b.e.yes===1n&&b.e.q===2,'duplicate semantic layer');
const rankCollision=fmt(3,2,1,[{id:1,op:'E',u:1,v:3},{id:2,op:'E',u:2,v:3},{id:3,op:'X',u:2,v:2},{id:4,op:'X',u:1,v:3},{id:5,op:'O',u:1,v:4}],5);
const collision=test(rankCollision,false);ok(collision.e.q===2&&collision.e.yes===2n,'individual rank vector same, count differs');
const same=fmt(2,1,1,[{id:1,op:'E',u:1,v:2},{id:2,op:'O',u:1,v:1}],2);
const c=test(same,true);ok(c.e.q===1&&c.e.yes===1n,'idempotent gate DAG');
for(let aa=1;aa<=3;aa++)for(let bb=1;bb<=3;bb++)for(let t=0;t<7;t++)test(build(aa,bb,t),false);
// True fan-out, random record permutation and exponentially expanded OR with duplicated children.
const gs=[];function add(op,u,v){const id=gs.length+1;gs.push({id,op,u,v});return id;}
let leaf=add('E',1,2),root=leaf;for(let j=0;j<90;j++)root=add('O',root,root);
const deep=test(fmt(2,1,1,gs.slice().reverse(),root),false);
ok(deep.e.q===1&&deep.e.yes===1n,'90-level sharing not unfolded');
for(const bad of [small.replace('p norxor','p nxor'),small.replace('g 3 O 1 2','g 3 O 3 2'),small.replace('g 2 E 2 3','g 2 E 2 2'),small.replace('p norxor 3 2 1','p norxor 999999999 2 1'),small.replace('g 2 E 2 3','g 1 E 2 3'),small+'g 4 E 1 3\n',small+'\u00e9',fmt(2,1,1,[{id:1,op:'E',u:1,v:2},{id:2,op:'O',u:1,v:1},{id:3,op:'X',u:2,v:1}],3)]){
 let rejected=false;try{parse(bad);}catch{rejected=true;}ok(rejected,'invalid rejected');malformed++;
}
const raw={revision:REV,seed:SEED,checks,brute_original_executions:brute,full_CNF_unique_extension_executions:cnfTests,malformed_rejections:malformed,failures:0,minimal_OR:{source:small,yes:String(a.e.yes),q:a.e.q,rank_histogram:a.e.ranks},duplicate_layer:{yes:String(b.e.yes),rank_histogram:b.e.ranks},rank_collision:{source:rankCollision,yes:String(collision.e.yes),rank_histogram:collision.e.ranks},idempotent_OR:{q:c.e.q,yes:String(c.e.yes)},deep_shared_OR:{depth:90,gates:gs.length,q:deep.e.q,yes:String(deep.e.yes)}};
console.log(JSON.stringify(raw,null,2));
