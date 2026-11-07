// LSPV-1/465 self-contained verifier: ordinary Resolution only, no assumed split rule.
'use strict';
let checks=0;const ok=(c,m)=>{checks++;if(!c)throw Error(m||'assertion');};
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const norm=a=>{let s=new Set(a);for(let x of s)if(s.has(-x))return null;return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)};
const res=(a,b,p)=>{let A=new Set(a),B=new Set(b);if(A.has(p)&&B.has(-p)){A.delete(p);B.delete(-p);}else if(A.has(-p)&&B.has(p)){A.delete(-p);B.delete(p)}else throw Error('pivot');return norm([...A,...B]);};
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function ts(ch){let F=[];for(let v=0;v<4;v++){let e=edges.map((z,i)=>z.includes(v)?i+1:0).filter(Boolean);for(let t=0;t<8;t++){let z=e.map((_,j)=>(t>>(2-j))&1);if((z[0]+z[1]+z[2])%2!==ch[v])F.push(norm(e.map((x,j)=>z[j]?-x:x)));}}return F;}
const F=ts([1,0,0,0]),even=ts([0,0,0,0]);ok(F.length===16);
const holds=(c,a)=>c.some(x=>a[Math.abs(x)]===Number(x>0));
let evenModels=0;for(let k=0;k<64;k++){let a={};for(let i=1;i<=6;i++)a[i]=(k>>(i-1))&1;ok(!F.every(c=>holds(c,a)),'odd SAT');if(even.every(c=>holds(c,a)))evenModels++;}ok(evenModels===8);
const G=[[-7,1,8],[-7,1,-8],[-7,2,9],[-7,2,-9],[7,-1,-2]];
const leaves=[[{1:0},0],[{1:1,2:0},0],[{1:1,2:1},1]];
for(let [a,y] of leaves)for(let k=0;k<64;k++){let x={...a,7:y,8:0,9:0};for(let i=1;i<=6;i++)if(x[i]===undefined)x[i]=(k>>(i-1))&1;for(let c of G)ok(holds(c,x),'bad Skolem leaf');}
for(let i=0;i<4;i++)for(let y=0;y<2;y++)for(let p=0;p<4;p++){let a={1:i&1,2:(i>>1)&1,7:y,8:p&1,9:(p>>1)&1};ok(G.every(c=>holds(c,a))===(y===(a[1]&a[2])),'not AND');}
const restrict=(c,a)=>{for(let x of c)if(a[Math.abs(x)]!==undefined&&a[Math.abs(x)]===Number(x>0))return null;return norm(c.filter(x=>a[Math.abs(x)]===undefined));};
const nodes={};let sn=0;F.forEach((c,i)=>nodes['s'+(i+1)]={rule:'SOURCE',source:i+1,c});
function step(a,b,p){let c=res(nodes[a].c,nodes[b].c,p);if(!c)return null;let id='r'+(++sn);nodes[id]={rule:'RES',a,b,p,c};return id;}
function dp(alpha){let now=new Map();F.forEach((c,i)=>{let r=restrict(c,alpha);if(r!==null&&!now.has(JSON.stringify(r)))now.set(JSON.stringify(r),'s'+(i+1));});if(now.has('[]'))return now.get('[]');for(let p=1;p<=6;p++){if(alpha[p]!==undefined)continue;let pos=[],neg=[],next=new Map();for(let [k,id] of now){let c=JSON.parse(k);if(c.includes(p))pos.push([c,id]);else if(c.includes(-p))neg.push([c,id]);else next.set(k,id);}for(let [A,a] of pos)for(let [B,b] of neg){let C=res(A,B,p);if(C===null)continue;let key=JSON.stringify(C);if(next.has(key))continue;let id=step(a,b,p);ok(eq(restrict(nodes[id].c,alpha),C),'lift mismatch');next.set(key,id);if(key==='[]')return id;}now=next;}throw Error('no refutation');}
const plain=dp({});ok(eq(nodes[plain].c,[]));let leafIDs=leaves.map(([a])=>dp(a));
function join(a,b,p){if(!nodes[a].c.includes(p))return a;if(!nodes[b].c.includes(-p))return b;return step(a,b,p);}
const branch=join(leafIDs[1],leafIDs[2],2),root=join(leafIDs[0],branch,1);ok(eq(nodes[root].c,[]));
function verify(goal,ns){let seen=new Set(),pending=new Set(),depth={};function visit(id){if(pending.has(id))throw Error('cycle');if(seen.has(id))return;let n=ns[id];if(!n)throw Error('missing');pending.add(id);if(n.rule==='SOURCE'){if(!(n.source>=1&&n.source<=16)||!eq(n.c,F[n.source-1]))throw Error('source');depth[id]=0;}else if(n.rule==='RES'){visit(n.a);visit(n.b);if(!eq(n.c,res(ns[n.a].c,ns[n.b].c,n.p)))throw Error('bad RES');depth[id]=1+Math.max(depth[n.a],depth[n.b]);}else throw Error('unlicensed rule');pending.delete(id);seen.add(id);}visit(goal);if(!eq(ns[goal].c,[]))throw Error('goal');return {paid:[...seen].filter(id=>ns[id].rule==='RES').length,source:[...seen].filter(id=>ns[id].rule==='SOURCE').length,span:depth[goal]};}
const a=verify(plain,nodes),b=verify(root,nodes);ok(a.paid===31&&b.paid===31&&b.span===6&&b.source===16);ok(b.paid<=3*(a.paid+1)-1);
let errors=[];function bad(label,change){let x=structuredClone(nodes);change(x);try{verify(root,x);}catch(e){errors.push(label);return;}throw Error('bad certificate accepted: '+label);}
bad('source',x=>{x.s1.source=99});bad('pivot',x=>{x[root].p=99});bad('missing',x=>{x[root].a='ABSENT'});bad('cycle',x=>{x[root].a=root});bad('goal',x=>{x[root].c=[1]});ok(errors.length===5);
console.log(JSON.stringify({status:'PASS',checks,odd_models:0,even_models:evenModels,original_clauses:16,auxiliary_strict3_clauses:G.length,section_leaves:leaves.length,plain:a,reconstructed:b,corruptions:errors},null,2));
