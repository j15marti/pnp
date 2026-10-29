// LSPV-3 PORT-SWAP-TREE166: independent small-control reproducer.
// Node.js: node 2026-10-29_1324_PORT_SWAP_TREE166_independent.js
"use strict";
const G=[[-5,-12,15],[-5,-6,-15],[-4,-9,-11],[-4,-8,-11],[-3,6,-15],
[-3,12,15],[-2,-6,12],[-2,5,-12],[-1,3,-14],[-1,13,14],
[1,-7,10],[1,7,13],[2,-9,11],[2,-8,9],[3,7,-13],
[4,8,-10],[4,9,-10],[5,8,-14],[6,-7,11],[10,-13,14]];
const U=G.map((cl,i)=>cl.map(l=>(Math.abs(l)===4&&(i===3||i===16))?-l:l));
const S=[G,U];
const value=(l,mask)=>((mask>>(Math.abs(l)-1))&1)===Number(l>0);
function models(src){
 let count=0;for(let mask=0;mask<(1<<15);mask++)if(src.every(c=>c.some(l=>value(l,mask))))count++;
 return count;
}
function slot(src,c){
 const sign=c<2?-1:1;
 const positions=[];for(let j=0;j<src.length;j++)if(src[j].includes(4*sign))positions.push(j);
 if(positions.length!==2)throw Error("invalid source");return positions[c%2];
}
function build(k,modes,edges){
 const blocks=modes.map((mode,i)=>S[mode].map(c=>c.map(l=>Math.sign(l)*(15*i+Math.abs(l)))));
 const adj=Array.from({length:k},()=>[]),used=Array.from({length:k},()=>new Set());
 for(const [a,b,c] of edges){
  if(used[a].has(c)||used[b].has(c))throw Error("reused source slot");
  used[a].add(c);used[b].add(c);adj[a].push([b,c]);adj[b].push([a,c]);
  const sign=c<2?-1:1;
  for(const [x,y] of [[a,b],[b,a]]){
   const j=slot(S[modes[x]],c);
   const from=sign*(15*x+4),to=sign*(15*y+4);
   const q=blocks[x][j].indexOf(from);if(q<0)throw Error("missing port");
   blocks[x][j][q]=to;
  }
 }
 const F=blocks.flat(),counts=new Map();
 for(const clause of F){
  if(clause.length!==3||new Set(clause.map(Math.abs)).size!==3)throw Error("not proper");
  for(const l of clause)counts.set(l,(counts.get(l)||0)+1);
 }
 for(let v=1;v<=15*k;v++)if(counts.get(v)!==2||counts.get(-v)!==2)throw Error("not strict22");
 return {k,modes,adj,edges,F};
}
function localTable(x,v){
 const source=S[x.modes[v]],peers=x.adj[v].slice().sort((a,b)=>a[0]-b[0]);
 const changed=new Map(peers.map(([u,c])=>[slot(source,c),u]));
 const retained=[];
 for(let mask=0;mask<(1<<15);mask++){
  if(source.every((cl,j)=>changed.has(j)||cl.some(l=>value(l,mask))))retained.push(mask);
 }
 const rows=[];
 for(let s=0;s<1<<(peers.length+1);s++){
  const bit=r=>(s>>r)&1;let witness=null;
  for(const mask of retained){
   if(((mask>>3)&1)!==bit(0))continue;
   let yes=true;
   for(let j=0;j<peers.length;j++){
    const [u,c]=peers[j],cl=source[slot(source,c)];
    if(!cl.some(l=>(Math.abs(l)===4?bit(j+1):((mask>>(Math.abs(l)-1))&1))===Number(l>0))){
     yes=false;break;
    }
   }
   if(yes){witness=mask;break;}
  }
  rows.push({s,valid:witness!==null,witness});
 }
 return {peers,rows};
}
function solve(x){
 const n=x.k,parent=Array(n).fill(-2),order=[0];parent[0]=-1;
 for(const v of order)for(const [u] of x.adj[v])if(parent[u]===-2){parent[u]=v;order.push(u);}
 if(order.length!==n)throw Error("disconnected");
 const local=Array.from({length:n},(_,v)=>localTable(x,v)),memo=Array(n);
 for(let q=order.length-1;q>=0;q--){
  const v=order[q],pv=parent[v],rels=local[v],entries=new Map();
  for(const row of rels.rows){
   if(!row.valid)continue;
   const own=row.s&1;
   let good=true,parentBit=null;
   rels.peers.forEach(([u],j)=>{
    const other=(row.s>>(j+1))&1;
    if(u===pv)parentBit=other;
    else if(!memo[u].has(other+","+own))good=false;
   });
   if(good)entries.set(pv<0?"root":own+","+parentBit,row.witness);
  }
  memo[v]=entries;
 }
 return {sat:memo[0].has("root"),table_sizes:local.map(r=>r.rows.length)};
}
function run(){
 const source=[models(G),models(U)];
 if(source[0]!==272||source[1]!==0)throw Error("bad finite source");
 const tests=[
 ["G",1,[0],[],true],["U",1,[1],[],false],
 ["allG3",3,[0,0,0],[[0,1,0],[0,2,2]],true],
 ["starU3",3,[0,1,1],[[0,1,0],[0,2,2]],false],
 ["allG4",4,[0,0,0,0],[[0,1,0],[0,2,2],[0,3,1]],true],
 ["starU4",4,[0,1,1,0],[[0,1,0],[0,2,2],[0,3,1]],false]
 ];
 const results=[];
 for(const [name,k,modes,edges,expected] of tests){
  const F=build(k,modes,edges),ans=solve(F);
  if(ans.sat!==expected)throw Error("incorrect "+name);
  results.push({name,k,sat:ans.sat,clauses:F.F.length,table_sizes:ans.table_sizes});
 }
 return {source_models:source,tests:results};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
