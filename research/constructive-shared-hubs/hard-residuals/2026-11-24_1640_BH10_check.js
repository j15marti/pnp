"use strict";
function run() {
 const out={seed:27011,counts:{},ledger:{closureScans:0,unions:0,matchingScans:0,sccScans:0,cycleScans:0,liftScans:0,sourceChecks:0,referenceWords:0},scales:[],hostile:[]};
 let seed=out.seed;const rand=n=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)%n);
 const L=out.ledger; const assert=(b,msg)=>{if(!b)throw Error(msg);};
 const factor=(e,mask=3)=>({e:e.map(v=>[v,0]),mask});
 function check(n,fs,x,guards=[]){for(const [a,b,p] of guards)if((x[a]^x[b])!==p)return false;for(const f of fs){L.sourceChecks++;const v=f.e.map(([i,s])=>x[i]^s);if(v.every(t=>t===v[0])&&(f.mask&(1<<v[0])))return false;}return true;}
 function solve(n,fs,guards=[],cap=2000000){
  const r=n,par=Array.from({length:n+1},(_,i)=>i),q=par.map(()=>0);
  function find(a){if(par[a]===a)return [a,0];const [p,b]=find(par[a]);q[a]^=b;par[a]=p;return [p,q[a]];}
  function join(a,b,p){const [u,s]=find(a),[v,t]=find(b);if(u===v)return (s^t)===p;par[u]=v;q[u]=s^t^p;L.unions++;return true;}
  for(const [a,b,p] of guards)if(!join(a,b,p))return {status:"UNSAT",reason:"guard"};
  let src=fs.map(f=>({e:f.mask===3?f.e:f.mask===1?[...f.e,[r,0]]:f.mask===2?[...f.e,[r,1]]:[],skip:f.mask===0})).filter(f=>!f.skip);
  let live;for(;;){live=[];let changed=false;for(const f of src){L.closureScans++;const seen=new Map();let taut=false;for(const [v,s] of f.e){const [a,b]=find(v),t=s^b;if(seen.has(a)&&seen.get(a)!==t){taut=true;break;}seen.set(a,t);}if(taut)continue;const e=[...seen];if(e.length<2)return {status:"UNSAT",reason:"closure"};if(e.length===2){if(!join(e[0][0],e[1][0],1^e[0][1]^e[1][1]))return {status:"UNSAT",reason:"closure"};changed=true;break;}live.push(e);}if(!changed)break;}
  const match=Array(n+1).fill(-1);
  function aug(i,seen){for(const [v] of live[i]){L.matchingScans++;if(seen.has(v))continue;seen.add(v);if(match[v]<0||aug(match[v],seen)){match[v]=i;return true;}}return false;}
  for(let i=0;i<live.length;i++)if(!aug(i,new Set()))return {status:"UNKNOWN",reason:"Hall"};
  const G=Array.from({length:n+1},()=>[]),rev=G.map(()=>[]);
  for(let v=0;v<=n;v++)if(match[v]>=0){const f=live[match[v]],s=f.find(e=>e[0]===v)[1];for(const [w,t] of f)if(w!==v){const a={u:v,v:w,p:1^s^t};G[v].push(a);rev[w].push(a);}}
  const seen=new Set(),order=[];function dfs(v){seen.add(v);for(const a of G[v]){L.sccScans++;if(!seen.has(a.v))dfs(a.v);}order.push(v);}
  for(let v=0;v<=n;v++)if(!seen.has(v))dfs(v);
  const comp=Array(n+1).fill(-1),parts=[];function back(v,i){comp[v]=i;parts[i].push(v);for(const a of rev[v]){L.sccScans++;if(comp[a.u]<0)back(a.u,i);}}
  for(const v of order.reverse())if(comp[v]<0){parts.push([]);back(v,parts.length-1);}
  const sink=parts.map(()=>true);for(let v=0;v<=n;v++)for(const a of G[v])if(comp[v]!==comp[a.v])sink[comp[v]]=false;
  const val=Array(n+1).fill(-1),queue=[];let scans=0;
  function put(v,b){assert(val[v]<0||val[v]===b,"lift clash");if(val[v]<0){val[v]=b;queue.push(v);}}
  for(let i=0;i<parts.length;i++)if(sink[i]){
   if(parts[i].length===1&&G[parts[i][0]].length===0){put(parts[i][0],0);continue;}
   // TEST BACKEND ONLY: simple-cycle enumeration, capped, not RST algorithm.
   const vs=parts[i].slice().sort((a,b)=>a-b);let found=null,limit=false;
   for(const start of vs){const visited=new Set([start]),path=[];function search(v,p){for(const a of G[v]){L.cycleScans++;if(++scans>cap){limit=true;return;}if(comp[a.v]!==i||a.v<start)continue;if(a.v===start){if((p^a.p)===0){found=[...path,a];return;}}else if(!visited.has(a.v)){visited.add(a.v);path.push(a);search(a.v,p^a.p);path.pop();visited.delete(a.v);if(found||limit)return;}}}search(start,0);if(found||limit)break;}
   if(limit)return {status:"UNKNOWN",reason:"cycle cap",scans};
   if(!found)return {status:"UNSAT",reason:"odd sink",scans};
   let b=0;for(const a of found){put(a.u,b);b^=a.p;}assert(b===0,"cycle parity");
  }
  for(let j=0;j<queue.length;j++){const v=queue[j];for(const a of rev[v]){L.liftScans++;if(val[a.u]<0)put(a.u,val[v]^a.p);}}
  const [rr,rs]=find(r),root=val[rr]^rs;
  const x=Array.from({length:n},(_,v)=>{const [a,b]=find(v);assert(val[a]>=0,"unlifted");return val[a]^b^root;});
  assert(check(n,fs,[...x,0],guards),"invalid source lift");return {status:"SAT",reason:"functional",scans};
 }
 function record(kind,n,fs,expected,guards=[],cap=2000000){const s=solve(n,fs,guards,cap),c=out.counts[kind]??={SAT:0,UNSAT:0,UNKNOWN:0};c[s.status]++;if(expected!==null&&s.status!=="UNKNOWN")assert(s.status===expected,kind+" wrong label");return s;}
 function brute(n,fs,guards=[]){let ct=0;for(let m=0;m<2**n;m++){L.referenceWords++;const x=Array.from({length:n+1},(_,i)=>i===n?0:(m>>i)&1);if(check(n,fs,x,guards))ct++;}return ct;}
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function neighbors(n,edges,kind,rootExpected){let fs=edges.map(e=>factor(e));let a=record(kind,n,fs,rootExpected);let row={kind,n,m:edges.length,root:a,neighborSAT:0,neighborUnknown:0};for(let i=0;i<edges.length;i++)for(const mask of [1,2]){const g=fs.map((f,j)=>j===i?{...f,mask}:f);let s=record(kind,n,g,"SAT");if(s.status==="SAT")row.neighborSAT++;else row.neighborUnknown++;if(n===7)assert(brute(n,g)===5,"Fano neighbor count");}out.scales.push(row);}
 assert(brute(7,fano.map(e=>factor(e)))===0,"Fano root");
 neighbors(7,fano,"Fano","UNSAT");
 function equality(a,b,next,edges){const p=next++,v=next++,w=next++,x=next++,y=next++;edges.push([a,v,w],[a,x,y],[b,v,x],[b,w,y],[p,v,y],[p,w,x]);return next;}
 let ed=[],next=1,ends=[];for(let c=0;c<2;c++){let a=0;for(let j=0;j<4;j++){let b=next++;next=equality(a,b,next,ed);a=b;}ends.push(a);}ed.push([0,...ends]);assert(next===49&&ed.length===49,"DO02 size");
 neighbors(next,ed,"DO02_49","UNSAT");
 let stretched=[],nn=next;for(const e of ed){let occ=[];for(const a of e){let b=nn++;occ.push(b);nn=equality(a,b,nn,stretched);}stretched.push(occ);}assert(nn===931&&stretched.length===931,"stretch size");
 let sr=record("DO02_931_sample",nn,stretched.map(e=>factor(e)),"UNSAT",[],4000000);let sample=[];for(const i of [0,6,123,930])for(const mask of [1,2])sample.push(record("DO02_931_sample",nn,stretched.map((e,j)=>factor(e,i===j?mask:3)),"SAT",[],4000000));out.scales.push({kind:"DO02_931_sample",n:nn,m:stretched.length,root:sr,neighbors:sample});
 // High bits of LCG for nondegenerate random signs.
 const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n;};
 for(let t=0;t<250;t++){const n=3+rnd(6),m=1+rnd(n+3),fs=[];for(let j=0;j<m;j++){let vs=[];while(vs.length<3){let v=rnd(n);if(!vs.includes(v))vs.push(v);}fs.push({e:vs.map(v=>[v,rnd(2)]),mask:1+rnd(3)});}let guards=[];if(t%4===0)guards.push([rnd(n),n,rnd(2)]);if(t%7===0)guards.push([rnd(n),rnd(n),rnd(2)]);record("random_signed_guarded",n,fs,brute(n,fs,guards)?"SAT":"UNSAT",guards);}
 for(const k of [8,32,128]){const fs=Array.from({length:k},(_,i)=>factor([i,(i+1)%k,k+i]));out.scales.push({kind:"loose_cycle",n:2*k,m:k,result:record("loose_cycle",2*k,fs,"SAT")});}
 const dense=[];for(let a=0;a<3;a++)for(let b=a+1;b<3;b++)for(let c=3;c<6;c++)dense.push(factor([a,b,c]));assert(brute(6,dense)>0,"dense SAT");out.hostile.push({kind:"dense_SAT",result:record("Hall_hostile",6,dense,"SAT")});out.hostile.push({kind:"dense_UNSAT",result:record("Hall_hostile",7,[...fano.map(e=>factor(e)),factor([0,1,3])],"UNSAT")});
 out.hostile.push({kind:"forced_cap",result:record("forced_cap",7,fano.map(e=>factor(e)),"UNSAT",[],0)});
 return out;
}
console.log(JSON.stringify(run(),null,2));
