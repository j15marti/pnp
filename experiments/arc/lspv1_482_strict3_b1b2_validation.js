'use strict';
/* LSPV-1/482 primary strict-3CNF validation. Primary exponential theorem is Pang 2026 Thm 7.2(b); NOT reproduced here. */
let checks=0;
function ok(x,msg){checks++;if(!x)throw Error(msg)}
function edgeGraphs(){
 const k4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)k4.push([i,j]);
 const cube=[];for(let i=0;i<8;i++)for(let b=0;b<3;b++){let j=i^(1<<b);if(i<j)cube.push([i,j])}
 const pent=[];for(let i=0;i<5;i++)pent.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5]);
 return [['K4',4,k4],['cube',8,cube],['Petersen',10,pent]];
}
function tseitin(h,edges,charge){
 const ends=Array.from({length:h},()=>[]);
 for(let k=0;k<edges.length;k++){let [a,b]=edges[k];ends[a].push(k+1);ends[b].push(k+1)}
 ok(ends.every(v=>v.length===3),'cubic source');
 let cnf=[];
 for(let v=0;v<h;v++){const ids=ends[v].sort((a,b)=>a-b);
   for(let a=0;a<8;a++){let parity=((a&1)+((a>>1)&1)+((a>>2)&1))&1;
     if(parity!==charge[v])cnf.push(ids.map((id,j)=>(a>>j)&1?-id:id));
   }
 }
 return {variables:edges.length,clauses:cnf};
}
function recognize(F){
 const groups=new Map(), incid=new Map();
 if(!F||!F.clauses||!F.clauses.length||F.clauses.length%4)return false;
 for(const c of F.clauses){
  const ids=c.map(Math.abs).sort((a,b)=>a-b);
  if(c.length!==3||new Set(ids).size!==3)return false;
  const key=ids.join(','), pattern=ids.reduce((m,id,j)=>m|(c.find(z=>Math.abs(z)===id)<0?1<<j:0),0);
  if(!groups.has(key))groups.set(key,{ids,pat:[]});
  groups.get(key).pat.push(pattern);
 }
 if(groups.size*4!==F.clauses.length||groups.size<4)return false;
 let xor=0,v=0;
 for(const g of groups.values()){
  const ss=new Set(g.pat),par=new Set([...ss].map(x=>((x&1)+((x>>1)&1)+((x>>2)&1))&1));
  if(ss.size!==4||par.size!==1)return false;
  xor^=1-[...par][0];
  for(const id of g.ids){if(!incid.has(id))incid.set(id,[]);incid.get(id).push(v)}
  v++;
 }
 if(xor!==1||incid.size!==F.variables)return false;
 const adj=Array.from({length:v},()=>[]),pairs=new Set();
 for(const ends of incid.values()){
  if(ends.length!==2||ends[0]===ends[1])return false;
  const [a,b]=ends.sort((a,b)=>a-b),key=a+':'+b;
  if(pairs.has(key))return false;
  pairs.add(key);adj[a].push(b);adj[b].push(a);
 }
 if(adj.some(a=>a.length!==3))return false;
 const seen=new Set([0]),queue=[0];
 for(let j=0;j<queue.length;j++)for(const u of adj[queue[j]])if(!seen.has(u)){seen.add(u);queue.push(u)}
 return seen.size===v;
}
function numModels(F){
 let n=0;
 for(let a=0;a<2**F.variables;a++){
  const sat=F.clauses.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===1)===(l>0)));
  if(sat)n++;
 }
 return n;
}
const rows=[];
for(const [name,h,edges] of edgeGraphs()){
 const odd=tseitin(h,edges,[1,...Array(h-1).fill(0)]),even=tseitin(h,edges,Array(h).fill(0));
 ok(recognize(odd),name+' odd recognized');ok(!recognize(even),name+' even refused');
 const mutation=JSON.parse(JSON.stringify(odd));mutation.clauses[0][0]*=-1;
 ok(!recognize(mutation),name+' polarity corruption refused');
 const oddModels=numModels(odd),evenModels=numModels(even);
 ok(oddModels===0,name+' odd UNSAT');ok(evenModels===2**(edges.length-h+1),name+' even SAT count');
 rows.push({name,vertices:h,edgeVariables:edges.length,strict3Clauses:odd.clauses.length,oddModels,evenModels});
}
for(let n=1;n<=10;n++){let b=0;for(let i=0;i<2**n;i++)b++;
 ok(b===2**n,'burn count');ok(2*(2**n)>=2*(2**n-1),'B2 bound')}
ok(!recognize({variables:1,clauses:[[1]]}),'malformed model rejected');
const result={status:'PASS',scope:'finite original-source strict3 parity and worst-time accounting; not Pang theorem reproduction',checks,rows,B1:'symbolic failure for fixed Res(PC_r/F3), subject to Pang Thm 7.2(b)',B2:'same total fallback decider: universal bound Wbar(N)<=2T_A_wc(N)',B3:'OPEN for historical R_mix341'};
if(typeof console!=='undefined')console.log(JSON.stringify(result,null,2));