'use strict';
/* LSPV-4/591, standalone Node or hosted JS. No packages or external corpus required. */
function parity(n){let p=0;while(n){p^=n&1;n>>=1;}return p;}
function graphK4(){return {name:"K4",v:4,e:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]};}
function graphK33(){let e=[];for(let a=0;a<3;a++)for(let b=3;b<6;b++)e.push([a,b]);return {name:"K33",v:6,e};}
function graphCube(){let e=[];for(let i=0;i<8;i++)for(const b of [1,2,4])if((i&b)===0)e.push([i,i^b]);return {name:"CUBE",v:8,e};}
function graphPrism(){return {name:"PRISM6",v:6,e:[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]]};}
function graphK4x2(){const g=graphK4();return {name:"K4+K4",v:8,e:[...g.e,...g.e.map(([a,b])=>[a+4,b+4])]};}
function signedTseitin(g,charge){
 const incident=Array.from({length:g.v},()=>[]);
 g.e.forEach(([a,b],i)=>{incident[a].push(i+1);incident[b].push(i+1);});
 const F=[];
 for(let v=0;v<g.v;v++){
  if(incident[v].length!==3)throw Error("not cubic");
  for(let k=0;k<8;k++)if(parity(k)!==charge[v]){
    const c=incident[v].map((x,j)=>((k>>j)&1)?-x:x);
    F.push(c);
  }
 }
 return F;
}
function recognizableAffine(F){
 if(!Array.isArray(F)||F.length===0)return null;
 const groups=new Map();
 for(const c of F){
  if(!Array.isArray(c)||c.length!==3||c.some(x=>!Number.isSafeInteger(x)||x===0))return null;
  const vars=c.map(Math.abs).sort((a,b)=>a-b);
  if(new Set(vars).size!==3)return null;
  const key=vars.join(",");
  if(!groups.has(key))groups.set(key,{vars,clauses:[]});
  groups.get(key).clauses.push(c);
 }
 const blocks=[...groups.values()];
 const occ=new Map();
 for(let i=0;i<blocks.length;i++){
  const block=blocks[i], patterns=new Set();
  if(block.clauses.length!==4)return null;
  for(const c of block.clauses){
   let mask=0;for(let j=0;j<3;j++){const lit=c.find(x=>Math.abs(x)===block.vars[j]);if(lit<0)mask|=1<<j;}
   patterns.add(mask);
  }
  if(patterns.size!==4)return null;
  const ps=[...patterns].map(parity);
  if(ps.some(p=>p!==ps[0]))return null;
  block.charge=1-ps[0];
  for(const x of block.vars){if(!occ.has(x))occ.set(x,[]);occ.get(x).push(i);}
 }
 if([...occ.values()].some(a=>a.length!==2||a[0]===a[1]))return null;
 const adj=Array.from({length:blocks.length},()=>[]);
 for(const vv of occ.values()){const [u,v]=vv;adj[u].push(v);adj[v].push(u);}
 const seen=new Set();let oddComponents=0,components=0;
 for(let i=0;i<blocks.length;i++)if(!seen.has(i)){
  components++;const work=[i];seen.add(i);let x=0;
  for(let at=0;at<work.length;at++){const u=work[at];x^=blocks[u].charge;for(const v of adj[u])if(!seen.has(v)){seen.add(v);work.push(v);}}
  if(x!==0)oddComponents++;
 }
 return {sat:oddComponents===0,components,oddComponents,blocks:blocks.length,variables:occ.size};
}
function exhaustive(F){
 const ids=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);
 if(ids.length>18)throw Error("exhaustive bound exceeded");
 let count=0;const pos=new Map(ids.map((v,i)=>[v,i]));
 for(let z=0;z<2**ids.length;z++){
  let ok=true;
  for(const c of F)if(!c.some(lit=>Boolean((z>>pos.get(Math.abs(lit)))&1)===(lit>0))){ok=false;break;}
  if(ok)count++;
 }
 return {sat:count>0,count,variableCount:ids.length};
}
function totalDecider(F){
 const aff=recognizableAffine(F);
 if(aff!==null)return {sat:aff.sat,route:"AFFINE",aff};
 return {...exhaustive(F),route:"EXHAUSTIVE"};
}
function assert(b,msg){if(!b)throw Error(msg);}
function audit(){
 let assertions=0,rows=[],routeCounts={AFFINE:0,EXHAUSTIVE:0};
 const eq=(x,y,n)=>{assert(x===y,n);assertions++;};
 for(const g of [graphK4(),graphK33(),graphPrism(),graphCube(),graphK4x2()]){
  for(const charged of ["even","odd","two-odd"]){
   const ch=Array(g.v).fill(0);if(charged==="odd")ch[0]=1;if(charged==="two-odd"){ch[0]=1;ch[1]=1;}
   const F=signedTseitin(g,ch);const oracle=exhaustive(F);const A=totalDecider(F);
   eq(A.route,"AFFINE","missing affine fast path");eq(A.sat,oracle.sat,"SAT error");eq(A.sat,charged!=="odd","charge parity");
   const expected=oracle.sat?2**(g.e.length-g.v+A.aff.components):0;eq(oracle.count,expected,"model count");
   const reverse=F.map(c=>[...c].reverse());const B=totalDecider(reverse);eq(B.route,"AFFINE","literal order");eq(B.sat,oracle.sat,"literal order label");
   routeCounts.AFFINE+=2;
   rows.push({graph:g.name,vertices:g.v,edges:g.e.length,clauses:F.length,charge:charged,recognizer:A.route,components:A.aff.components,oddComponents:A.aff.oddComponents,oracleModels:oracle.count});
  }
 }
 const base=signedTseitin(graphK4(),[1,0,0,0]);
 const controls=[
  {name:"extra-unit",F:[...base,[1]]},
  {name:"source-deletion",F:base.slice(1)},
  {name:"wrong-sign-source",F:base.map((c,i)=>i===0?[-c[0],...c.slice(1)]:c)},
  {name:"unrelated-2CNF-SAT",F:[[1,2],[-1,2]]},
  {name:"unit-contradiction",F:[[1],[-1]]},
  {name:"non-parity-four",F:[[1,2,3],[1,2,-3],[-1,2,3],[-1,2,-3]]},
  {name:"duplicate-source",F:[...base,base[0]]},
  {name:"non-parity-tautology",F:[[1,-1,2]]}
 ];
 for(const {name,F} of controls){
  const A=totalDecider(F),O=exhaustive(F);
  eq(A.route,"EXHAUSTIVE","false affine recognition "+name);eq(A.sat,O.sat,"fallback error "+name);
  routeCounts.EXHAUSTIVE++;rows.push({control:name,route:A.route,oracleModels:O.count});
 }
 return {report:"LSPV-4/591",date:"2026-11-13 11:39 PST",status:"COMPUTATIONAL (finite recognizer), symbolic restricted transfer theorem separate",algorithm:"parity-pattern recognizer plus exhaustive fallback",assumptions:"finite canonical signed integer clause arrays; at most 18 IDs for bounded oracle in tests",checks:assertions,sourceSets:15,fastRecognized:routeCounts.AFFINE,slowFallbacks:routeCounts.EXHAUSTIVE,rows,limitations:"No asymptotic Resolution lower bound is inferred from these finite tests. The lower bound uses Ben-Sasson/Wigderson's DAG Resolution theorem on explicit expander families. This is not historical mixed R_mix341."};
}
if (typeof require!=="undefined" && require.main===module) console.log(JSON.stringify(audit(),null,2));
