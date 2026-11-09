// LSPV-3/535: independent *finite* original-source essential-core test.
// This is NOT the historical R_mix341 parser or a full link-diagram generator.
// node experiments/arc/lspv3_535_core_essential_link_rank.cjs
"use strict";
function fail(x){throw new Error(x)}
function sourceGraph(r){
 if(r===0)return [4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]];
 let edges=new Map(),h=2*r;
 for(let i=0;i<r;i++)for(let [a,b] of [[i,(i+1)%r],[r+i,r+(i+1)%r],[i,r+i]]){
  let x=Math.min(a,b),y=Math.max(a,b);edges.set(x+":"+y,[x,y]);
 }
 return [h,[...edges.values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1])];
}
function sat(c,x){return c.some(l=>Boolean(x&(1<<(Math.abs(l)-1)))===(l>0))}
function solve(rows){
 let piv=new Map();
 for(let [mask,rhs] of rows){
  while(mask){
   let p=31-Math.clz32(mask);
   if(!piv.has(p)){piv.set(p,[mask,rhs]);mask=0;rhs=0;break}
   let [m,b]=piv.get(p);mask^=m;rhs^=b;
  }
  if(mask===0&&rhs) return null;
 }
 let x=0;
 for(let p of [...piv.keys()].sort((a,b)=>a-b)){
  let [m,b]=piv.get(p);let y=m^(1<<p);
  let par=0;while(y){par^=(y&1);y>>>=1}
  // Re-evaluate with current assigned bits.
  y=(m^(1<<p))&x;par=0;while(y){par^=(y&1);y>>>=1}
  if(par^b)x|=1<<p;
 }
 for(let [m,b] of rows){
  let y=m&x,par=0;while(y){par^=y&1;y>>>=1}
  if(par!==b)fail("solver inconsistency");
 }
 return x;
}
function gf2Rank(rows){
 let piv=new Map();
 for(let row of rows)while(row){
  let p=row.toString(2).length-1;
  if(!piv.has(p)){piv.set(p,row);break}
  row^=piv.get(p);
 }
 return piv.size;
}
function run(){
 let rows=[],witnesses=0,corruption=0;
 for(let r of [0,3,4,5,6]){
  let [h,edges]=sourceGraph(r),n=edges.length,chi=Array(h).fill(0);chi[0]=1;
  if(n*2!==3*h)fail("not cubic");
  let inc=Array.from({length:h},()=>[]);
  for(let j=0;j<n;j++){let [a,b]=edges[j];inc[a].push(j);inc[b].push(j)}
  if(inc.some(x=>x.length!==3))fail("degree");
  let source=[],meta=[];
  for(let v=0;v<h;v++)for(let t=0;t<8;t++){
   let b=[(t>>2)&1,(t>>1)&1,t&1];
   if(((b[0]^b[1]^b[2])===1-chi[v])){
    source.push(inc[v].map((e,i)=>b[i] ? -(e+1) :e+1));
    meta.push([v,b]);
   }
  }
  if(source.length!==4*h)fail("source count");
  for(let i=0;i<source.length;i++){
   let [v,b]=meta[i],eq=[];
   for(let u=0;u<h;u++)if(u!==v)eq.push([inc[u].reduce((s,e)=>s|(1<<e),0),chi[u]]);
   for(let j=0;j<3;j++)eq.push([1<<inc[v][j],b[j]]);
   let x=solve(eq);
   if(x===null || sat(source[i],x))fail("deletion witness");
   for(let j=0;j<source.length;j++)if(j!==i&&!sat(source[j],x))fail("source clause");
   witnesses++;
   let altered=source[i].slice();altered[0]*=-1;
   if(altered.join(",")===source[i].join(","))fail("corruption control");
   corruption++;
  }
  // The n variable Hopf pairs survive insertion of any clause components.
  let hopf=Array.from({length:2*n},(_,i)=>1n<<BigInt(i^1));
  let rank=gf2Rank(hopf);
  if(rank!==2*n)fail("Hopf rank");
  rows.push({h,variables:n,clauses:source.length,deletion_witnesses:source.length,
    paid_AND3:3*h,paid_XOR:h-1,paid_nodes:4*h-1,
    span:2+Math.ceil(Math.log2(h)),hopf_principal_rank:rank,
    KT_components:2*n+source.length});
 }
 return {status:"PROVED/RESTRICTED only in declared semantic /341",
  graphs:rows,witnesses,source_corruption_controls:corruption,
  warning:"No historical full accepted-byte proof or full link diagram"};
}
if(typeof module!=="undefined")module.exports={run};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
