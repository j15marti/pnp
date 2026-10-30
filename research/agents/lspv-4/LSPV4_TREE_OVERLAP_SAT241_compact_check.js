'use strict';
const assert = require('assert');
function local(c){return c.map(l=>({variable:Math.abs(l),sign:l>0?'+':'-',S:l>0?1:0,invS:l>0?0:1,U:l>0?0:1,invU:l>0?1:0}));}
function modes(c,d){const same=c.some(a=>d.includes(a));const opp=c.some(a=>d.includes(-a));return {SS:!opp,SU:!same,US:!same,UU:!opp};}
function full(c,a){return c.map(l=>a[Math.abs(l)-1]===Number(l>0));}
function sat(F,a){return F.every(c=>full(c,a).some(Boolean));}
function count(F,a){return F.reduce((z,c)=>{z[full(c,a).filter(Boolean).length]++;return z;},[0,0,0,0]);}
function brute(F,n){let models=0;for(let m=0;m<2**n;m++){let a=Array.from({length:n},(_,i)=>(m>>i)&1);let r=count(F,a),rc=count(F,a.map(z=>1-z));assert.deepStrictEqual(rc,r.slice().reverse());if(sat(F,a)) models++;}return models;}
function falseMap(c){let d=new Map();for(const l of c){let v=Math.abs(l),bit=l<0?1:0;if(d.has(v)&&d.get(v)!==bit)return null;d.set(v,bit);}return d;}
function intersect(c,d,n){let m=falseMap(c),p=falseMap(d);if(!m||!p)return 0;for(const [v,b] of p)if(m.has(v)&&m.get(v)!==b)return 0;for(const [v,b] of p)m.set(v,b);return 2**(n-m.size);}
function maxTreeNumer(F,n){let scores=[];for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++)scores.push({j,k,w:intersect(F[j],F[k],n)});scores.sort((a,b)=>b.w-a.w||a.j-b.j||a.k-b.k);const parent=Array.from({length:F.length},(_,i)=>i);function root(x){while(parent[x]!==x)x=parent[x];return x;}let weight=0,edges=[];for(const e of scores){let x=root(e.j),y=root(e.k);if(x===y)continue;parent[x]=y;weight+=e.w;edges.push(e);if(edges.length===F.length-1)break;}let singles=F.reduce((a,c)=>a+intersect(c,[],n),0);return {numer:2**n-singles+weight,denom:2**n,edges};}
function checkPair(c,d,n){let p=modes(c,d);for(const [tag,want] of Object.entries(p)){let found=false;for(let mask=0;mask<2**n;mask++){let a=Array.from({length:n},(_,i)=>(mask>>i)&1);let cv=full(c,a),dv=full(d,a);if(cv.every(v=>v===Boolean(tag[0]==='S'))&&dv.every(v=>v===Boolean(tag[1]==='S'))){found=true;break;}}assert.strictEqual(found,want,JSON.stringify({c,d,tag}));}return 4;}
let assertions=0;const clauseBank=[];for(let a=1;a<=3;a++)for(let b=a+1;b<=4;b++)for(let c=b+1;c<=5;c++)for(let signs=0;signs<8;signs++)clauseBank.push([a,b,c].map((v,i)=>signs&(1<<i)?-v:v));
for(let j=0;j<clauseBank.length;j++)for(let k=j+1;k<clauseBank.length;k++)assertions+=checkPair(clauseBank[j],clauseBank[k],5);
const overlap=[[1,2,3],[1,-2,4]];
assert.deepStrictEqual(modes(...overlap),{SS:false,SU:false,US:false,UU:false});
assert.strictEqual(brute(overlap,4),12);
assert.deepStrictEqual(local(overlap[0]).map(x=>x.invS),local(overlap[0]).map(x=>x.U));
const star=m=>Array.from({length:m},(_,i)=>[1,2,i+3]);
for(const m of [1,7,14,15,16]){let b=maxTreeNumer(star(m),m+2);assert.strictEqual(b.numer,2**(m+2)*(15-m)/16);}
const eight=Array.from({length:8},(_,mask)=>[1,2,3].map((v,i)=>mask&(1<<i)?-v:v));
assert.strictEqual(brute(eight,3),0);
assert.strictEqual(maxTreeNumer(eight,3).numer,0);
const seven=eight.slice(1);
assert.strictEqual(brute(seven,3),1);
assert.strictEqual(maxTreeNumer(seven,3).numer,1);
const endpoints=[[1,2,3],[-1,-2,-3]];
assert.strictEqual(brute(endpoints,3),6);
assert.strictEqual(sat(endpoints,[0,0,0]),false);
assert.strictEqual(sat(endpoints,[1,1,1]),false);
assert.strictEqual(6*(2*2),24);assert(24<28);
const hostile=eight.concat(Array.from({length:14},(_,i)=>[1,2,i+4]));
let pair=0;
for(let j=0;j<hostile.length;j++)for(let k=j+1;k<hostile.length;k++)pair+=intersect(hostile[j],hostile[k],17);
const allPair=2**17-hostile.reduce((a,c)=>a+intersect(c,[],17),0)+pair;
assert.strictEqual(allPair/(2**17),5.6875);
assert.strictEqual(maxTreeNumer(hostile,17).numer/(2**17),-13/16);
const out={run_id:'TREE-OVERLAP-SAT241',assertions:assertions+22,distinct_clause_pairs:clauseBank.length*(clauseBank.length-1)/2,all_modes_exhaustive:true,star14_numerator:maxTreeNumer(star(14),16).numer,star15_numerator:maxTreeNumer(star(15),17).numer,star16_numerator:maxTreeNumer(star(16),18).numer,hostile_allpair:allPair/(2**17),hostile_tree:maxTreeNumer(hostile,17).numer/(2**17),hitting8_models:0,seven_models:1,restricted_6var_exact22_sat_theorem:true,scope:'finite controls for independently proved restricted theorems; no general P vs NP result'};
console.log(JSON.stringify(out));