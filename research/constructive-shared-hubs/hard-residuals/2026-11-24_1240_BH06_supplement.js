"use strict";
function supplemental(){
 const L={assertions:0,featureCandidates:0,featureTests:0,featureXors:0,referenceWords:0,motifCandidates:0,motifTableWords:0,motifRechecks:0,closureScans:0,closureDeductions:0,residualWords:0,sourceChecks:0,verifiedLifts:0,projectionJobs:0};
 const ck=(v,msg)=>{L.assertions++;if(!v)throw Error(msg)};
 const bit=i=>1n<<BigInt(i),parity=w=>{let p=0;while(w){w&=w-1n;p^=1}return p};
 function basis(words,mons){let B=new Map(),R=[];for(let w of words){L.featureCandidates++;let q=0n;for(let j=0;j<mons.length;j++){L.featureTests++;if((w&mons[j])===mons[j])q|=bit(j)}while(q){let p=q&-q;if(!B.has(p)){B.set(p,q);R.push(w);break}q^=B.get(p);L.featureXors++}}return R}
 let scaling=[];
 for(let h of [4,8,12,16]){
  let n=2*h,g=Array.from({length:h},(_,i)=>{let a=0n;for(let j=0;j<h;j++)if(j!==i)a|=bit(h+j);return a});
  let mons=[0n];for(let i=0;i<n;i++){mons.push(bit(i));for(let j=i+1;j<n;j++)mons.push(bit(i)|bit(j))}
  let R=[0n];
  for(let i=n-1;i>=0;i--){let out=[];for(let w of R){out.push(w);if(i>=h||parity(g[i]&w))out.push(w|bit(i))}R=basis(out,mons)}
  let legal=w=>g.every((a,i)=>!(w&bit(i))||parity(a&w)===1);
  ck(R.every(legal),"representatives");ck(R.length===mons.length-h,"quadratic dimension");
  ck(!R.some(w=>(w&1n)&&parity(g[0]&w)===0),"negative joint query");
  let yes=R.find(w=>(w&1n)&&parity(g[0]&w)===1);ck(yes!==undefined&&legal(yes),"positive query lift");
  if(h===4){let count=0;for(let i=0;i<2**n;i++){L.referenceWords++;if(legal(BigInt(i)))count++}ck(count===3**h,"count reference")}
  scaling.push({n,independentDenseParityRank:h,actualBaseModels:(3n**BigInt(h)).toString(),representatives:R.length,capacity:mons.length,witness:yes.toString()});
 }
 const fan=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]], gadget=fan.slice(1);
 const checkEdge=(e,x)=>{L.sourceChecks++;return e.b===null?!(x[e.v[0]]===x[e.v[1]]&&x[e.v[1]]===x[e.v[2]]):e.v.some(v=>x[v]===e.b)};
 const arr=(w,n)=>Array.from({length:n},(_,i)=>(w>>i)&1);
 const local=(H,drop=-1)=>{let R=[];for(let w=0;w<128;w++){L.referenceWords++;let x=arr(w,7);if(H.every((e,i)=>i===drop||!(x[e[0]]===x[e[1]]&&x[e[1]]===x[e[2]])))R.push(x)}return R};
 let models=local(gadget);ck(models.length===10&&models.every(x=>x[0]===x[1]&&x[1]===x[2]),"Fano-minus-line equality");
 for(let j=0;j<6;j++)ck(local(gadget,j).some(x=>x[0]!==x[1]),"minimal two-port equality");
 function connectedWithout(H,i){let a=H[i][0],seen=new Set([a]);for(;;){let size=seen.size;for(let j=0;j<H.length;j++)if(j!==i&&H[j].some(v=>seen.has(v)))for(let v of H[j])seen.add(v);if(size===seen.size)break}return H[i].every(v=>seen.has(v))}
 ck(gadget.every((e,i)=>connectedWithout(gadget,i)),"gadget no first peel");
 function stretch(n,H){
  let E=[],ports=Array.from({length:H.length},()=>[]);
  for(let j=0;j<H.length;j++)for(let v of H[j]){
   let p=[v];for(let i=1;i<7;i++)p.push(n++);ports[j].push(p[1]);
   for(let e of gadget)E.push({v:e.map(i=>p[i]),b:null});
  }
  for(let p of ports)E.push({v:p,b:null});
  return {n,E};
 }
 function discover(n,E){
  let adj=Array.from({length:n},()=>[]);E.forEach((e,i)=>e.v.forEach(v=>adj[v].push(i)));
  let result=[],keys=new Set();
  for(let v=0;v<n;v++){
   if(adj[v].length!==3)continue;L.motifCandidates++;
   let V=[...new Set(adj[v].flatMap(i=>E[i].v))].sort((a,b)=>a-b);if(V.length!==7)continue;
   let s=new Set(V),ids=[...new Set(V.flatMap(u=>adj[u]))].filter(i=>E[i].v.every(u=>s.has(u))).sort((a,b)=>a-b);
   if(ids.length!==6||ids.some(i=>E[i].b!==null))continue;
   let key=ids.join(",");if(keys.has(key))continue;
   let boundary=V.filter(u=>adj[u].some(i=>!ids.includes(i)));
   // A Fano-minus-line motif has three degree-two local vertices. Retain all three as boundary.
   let low=V.filter(u=>ids.filter(i=>E[i].v.includes(u)).length===2);
   if(low.length!==3||boundary.some(u=>!low.includes(u)))continue;
   let interior=V.filter(u=>!low.includes(u));
   if(interior.some(u=>adj[u].length!==3))continue;
   let pos=new Map(V.map((u,i)=>[u,i])),H=ids.map(i=>E[i].v.map(u=>pos.get(u))),R=[];
   for(let w=0;w<128;w++){L.motifTableWords++;let x=arr(w,7);if(H.every(e=>!(x[e[0]]===x[e[1]]&&x[e[1]]===x[e[2]])))R.push(x)}
   let q=low.map(u=>pos.get(u));
   if(!R.length||!R.every(x=>q.every(i=>x[i]===x[q[0]])))continue;
   let lifts=[R.find(x=>x[q[0]]===0),R.find(x=>x[q[0]]===1)];
   if(!lifts[0]||!lifts[1])continue;
   keys.add(key);result.push({V,ids,low,interior,lifts});
  }
  return result;
 }
 function solve(n,E,motifs){
  let active=E.map(()=>true),parent=Array.from({length:n+1},(_,i)=>i),p=Array(n+1).fill(0),size=Array(n+1).fill(1),archive=[];
  function find(x){if(parent[x]===x)return [x,0];let [r,b]=find(parent[x]);p[x]^=b;parent[x]=r;return [r,p[x]]}
  function join(a,b,d){let [r,x]=find(a),[s,y]=find(b);if(r===s)return (x^y)===d?0:-1;if(size[r]<size[s]){[r,s]=[s,r];[x,y]=[y,x]}parent[s]=r;p[s]=d^x^y;size[r]+=size[s];L.closureDeductions++;return 1}
  function closure(){
   for(;;){let changed=false;for(let i=0;i<E.length;i++)if(active[i]){
    L.closureScans++;let e=E[i],vals=e.v.map(find),m=new Map(),taut=false;
    if(e.b===null){
     for(let [r,b] of vals){if(m.has(r)&&m.get(r)!==b){taut=true;break}m.set(r,b)}
     if(taut)continue;if(m.size===1)return false;
     if(m.size===2){let [[r,x],[s,y]]=[...m];let t=join(r,s,1^x^y);if(t<0)return false;if(t){changed=true;break}}
    }else{
     let [r0,b0]=find(n);
     for(let [r,b] of vals){let need=e.b^b;if(r===r0){if(need===b0){taut=true;break}continue}if(m.has(r)&&m.get(r)!==need){taut=true;break}m.set(r,need)}
     if(taut)continue;if(m.size===0)return false;
     if(m.size===1){let [[r,b]]=[...m];let t=join(r,n,b);if(t<0)return false;if(t){changed=true;break}}
    }
   }if(!changed)return true}
  }
  if(!closure())return {label:"UNSAT",projected:0,free:0};
  for(let M of motifs){
   L.motifRechecks++;
   if(M.ids.some(i=>!active[i]||E[i].b!==null))continue;
   // Verify the exact cached source geometry and private interior in the current residual.
   if(M.interior.some(v=>{let [r]=find(v);return r!==v||size[r]!==1||E.some((e,i)=>active[i]&&!M.ids.includes(i)&&e.v.includes(v))}))continue;
   for(let i of M.ids)active[i]=false;
   archive.push(M);L.projectionJobs++;
   for(let v of M.low.slice(1))if(join(M.low[0],v,0)<0)return {label:"UNSAT",projected:archive.length,free:0};
   if(!closure())return {label:"UNSAT",projected:archive.length,free:0};
  }
  if(!closure())return {label:"UNSAT",projected:archive.length,free:0};
  let [r0,b0]=find(n),remain=E.filter((_,i)=>active[i]),roots=[...new Set(remain.flatMap(e=>e.v.map(v=>find(v)[0])))].filter(r=>r!==r0);
  ck(roots.length<=16,"small residual experimental cap");
  for(let w=0;w<2**roots.length;w++){
   L.residualWords++;let values=new Map(roots.map((r,i)=>[r,(w>>i)&1]));values.set(r0,b0);
   let x=Array.from({length:n},(_,v)=>{let [r,b]=find(v);return (values.get(r)??0)^b});
   if(!remain.every(e=>checkEdge(e,x)))continue;
   for(let M of archive.slice().reverse()){
    let a=x[M.low[0]];ck(M.low.every(v=>x[v]===a),"boundary equality");
    let row=M.lifts[a];M.V.forEach((v,i)=>{if(M.interior.includes(v))x[v]=row[i]});
   }
   ck(E.every(e=>checkEdge(e,x)),"original physical source lift");L.verifiedLifts++;
   return {label:"SAT",projected:archive.length,free:roots.length};
  }
  return {label:"UNSAT",projected:archive.length,free:roots.length};
 }
 let K5=[];for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)for(let c=b+1;c<5;c++)K5.push([a,b,c]);
 let stretched=[];
 for(let [name,n,H] of [["Fano",7,fan],["K5_triples",5,K5]]){
  let G=stretch(n,H),motifs=discover(G.n,G.E);ck(motifs.length===3*H.length,"manifest-free motif acquisition");
  let root=solve(G.n,G.E,motifs);ck(root.label==="UNSAT"&&root.projected===motifs.length,"stretched root");
  let maxFree=0,minProjected=Infinity,sat=0;
  for(let i=0;i<G.E.length;i++)for(let b=0;b<2;b++){
   let E=G.E.map((e,j)=>j===i?{v:e.v,b}:e);
   let a=solve(G.n,E,motifs);ck(a.label==="SAT","single owner neighbor");
   sat++;maxFree=Math.max(maxFree,a.free);minProjected=Math.min(minProjected,a.projected);
  }
  stretched.push({name,vertices:G.n,clauses:G.E.length,discoveredMotifs:motifs.length,root,neighborsSAT:sat,minProjected,maxFree,exceptionLowerBound:motifs.length-1});
 }
 return {scaling,stretched,local:{gadgetModels:models.length,minimalEquality:true,noFirstPivot:true},ledger:L};
}
console.log(JSON.stringify(supplemental(),null,2));
