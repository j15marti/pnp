/* LSPV-2/422 Route A expander Tseitin boundary-sieve falsifier, deterministic, no dependencies.
   Run: node experiments/arc/lspv2_422_expander_cut_replay.js
   Finite graphs are controls; no finite result certifies an infinite expander sequence.
*/
"use strict";
function assert(p,msg){if(!p)throw Error(msg)}
function uniqueEdges(n,E){const z=new Set();for(const [u,v] of E){assert(Number.isInteger(u)&&Number.isInteger(v)&&u!==v&&u>=0&&v>=0&&u<n&&v<n,"bad edge");z.add([Math.min(u,v),Math.max(u,v)].join(":"))}return [...z].map(s=>s.split(":").map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1])}
function graph(id){
 let n,E=[];
 if(id==="K4"){n=4;for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)E.push([a,b])}
 if(id==="cube"){n=8;for(let a=0;a<n;a++)for(let d=0;d<3;d++){let b=a^(1<<d);if(a<b)E.push([a,b])}}
 if(id==="Petersen"){n=10;for(let i=0;i<5;i++){E.push([i,(i+1)%5]);E.push([i,5+i]);E.push([5+i,5+(i+2)%5])}}
 if(id==="Heawood"){n=14;let lines=[[0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2]];for(let j=0;j<7;j++)for(const v of lines[j])E.push([v,7+j])}
 assert(n&&E.length,"unknown graph");E=uniqueEdges(n,E);
 let adj=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{adj[u].push([v,i]);adj[v].push([u,i])});
 assert(E.length*2===3*n&&adj.every(a=>a.length===3),"not cubic");
 const connected=(excluded=-1)=>{let seen=new Set([0]),q=[0];for(let k=0;k<q.length;k++)for(const [v,i] of adj[q[k]])if(i!==excluded&&!seen.has(v)){seen.add(v);q.push(v)}return seen.size===n};
 assert(connected()&&E.every((_,i)=>connected(i)),"not connected/bridgeless");
 return {id,n,E,adj}
}
function parity(z){let p=0;while(z){p^=z&1;z>>=1}return p}
function encode(g,odd){let out="p cnf "+g.E.length+" "+(4*g.n)+"\n",clauses=[];for(let v=0;v<g.n;v++){
 const vars=g.adj[v].map(q=>q[1]+1).sort((a,b)=>a-b),charge=(odd&&v===g.n-1)?1:0;
 for(let a=0;a<8;a++)if(parity(a)!==charge){let c=vars.map((x,j)=>(a>>j&1)?-x:x);clauses.push(c);out+=c.join(" ")+" 0\n"}
}assert(clauses.length===4*g.n,"wrong clause count");return {text:out,clauses,bytes:out.length,bits:8*out.length}}
function parseStrict(g,src){let lines=src.trimEnd().split("\n"),h=lines.shift();assert(h==="p cnf "+g.E.length+" "+4*g.n,"header");
 assert(lines.length===4*g.n,"clause count");let c=[];for(const row of lines){assert(/^-?\d+ -?\d+ -?\d+ 0$/.test(row),"malformed clause");let a=row.split(" ").map(Number);assert(a.slice(0,3).every(x=>x!==0&&Math.abs(x)<=g.E.length),"variable range");c.push(a.slice(0,3))}
 return c
}
function evaluate(clauses,model){return clauses.every(c=>c.some(x=>x>0?!!(model&(1n<<BigInt(x-1))):!(model&(1n<<BigInt(-x-1)))))}
function gf2(g,odd){let pivots=new Map(),rank=0,conflict=false;for(let v=0;v<g.n;v++){let row=0n;for(const [,j] of g.adj[v])row^=1n<<BigInt(j);let rhs=odd&&v===g.n-1?1:0;while(row){let i=0;while(((row>>BigInt(i))&1n)===0n)i++;let p=pivots.get(i);if(!p){pivots.set(i,[row,rhs]);rank++;break}row^=p[0];rhs^=p[1]}if(row===0n&&rhs)conflict=true}return {rank,conflict}}
function firstDifference(a,b){for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return i;return Math.min(a.length,b.length)}
function edgeCut(g,mask){let c=0;for(const [u,v] of g.E)c+=Number(((mask>>u)&1)!==((mask>>v)&1));return c}
function popcount(x){let c=0;while(x){x&=x-1;c++}return c}
function cuts(g){
 let mn=Infinity,md=1,bestBalanced=Infinity,verified=0,half=g.n/2;
 for(let mask=1;mask<(1<<g.n)-1;mask++){let count=popcount(mask);if(count>half)continue;let cross=edgeCut(g,mask);assert(cross>0,"disconnected");verified++;if(cross*md<mn*count){mn=cross;md=count}if(count===half&&cross<bestBalanced)bestBalanced=cross}
 assert(mn!==Infinity,"no subsets");
 return {edge_expansion_numerator:mn,edge_expansion_denominator:md,minimum_balanced_cut:bestBalanced,subsets_checked:verified,
  certified_lower_boundary_fraction:mn/md/2,
  minimum_two_block_mask_bits:2**bestBalanced}
}
function brute(g,src,limit=15){if(g.E.length>limit)return null;let sat=0;for(let a=0n;a<(1n<<BigInt(g.E.length));a++)if(evaluate(src.clauses,a))sat++;return sat}
function run(){
 const rows=[],tests={assertions:0,malformed_rejected:0,corrupted_rejected:0,opposite_labels:0};
 const check=(p,msg)=>{assert(p,msg);tests.assertions++};
 for(const name of ["K4","cube","Petersen","Heawood"]){
  let g=graph(name),even=encode(g,false),odd=encode(g,true),ec=parseStrict(g,even.text),oc=parseStrict(g,odd.text),cut=cuts(g);
  check(ec.length===4*g.n&&oc.length===4*g.n,"source counts");
  check(even.bytes===odd.bytes,"same length opposite labels");
  check(firstDifference(even.text,odd.text)>0.7*even.text.length,"long shared prefix");
  let ge=gf2(g,false),go=gf2(g,true);check(!ge.conflict&&go.conflict&&ge.rank===g.n-1&&go.rank===g.n-1,"GF2 both labels");
  tests.opposite_labels+=2;
  if(g.E.length<=15){check(brute(g,even)>0,"even SAT");check(brute(g,odd)===0,"odd UNSAT")}
  for(const altered of [odd.text.replace("p cnf","p cna"),odd.text.slice(0,-3),odd.text.replace(/\b0\n/,"999 0\n")]){
   let reject=false;try{parseStrict(g,altered)}catch(_){reject=true}check(reject,"malformed accepted");tests.malformed_rejected++
  }
  let corrupted=odd.text.replace("p cnf "+g.E.length+" "+(4*g.n),"p cnf "+g.E.length+" "+(4*g.n+1));
  let reject=false;try{parseStrict(g,corrupted)}catch(_){reject=true}check(reject,"corrupt header accepted");tests.corrupted_rejected++;
  rows.push({graph:name,vertices:g.n,edges:g.E.length,source_clauses:4*g.n,odd_DIMACS_bytes:odd.bytes,odd_encoded_bits:odd.bits,
   shared_prefix_bytes:firstDifference(even.text,odd.text),...cut,GF2_rank:go.rank,odd_unsat:true,even_sat:true,
   Rmix341_known_exact_upper_and_lower_nodes:4*g.n-1,
   source_bridgeless:true,
   brute_counts_even:g.E.length<=15?brute(g,even):null});
 }
 return {schema:"LSPV2_422_TSEITIN_BOUNDARY",status:"FINITE COMPUTATIONAL CONTROL + RESTRICTED ALL-SIZE CUT LEMMA",graphs:rows,checks:tests,
 notes:"Asymptotic Ω(H) separator theorem requires an infinite cubic edge-expander sequence and vertex-clause-respecting partitions. The explicit survivor-mask method allocates 2^b bits. This is not a lower bound for arbitrary SAT algorithms or arbitrary shared-DAG branching."};
}
const result=run();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
