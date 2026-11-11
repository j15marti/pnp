"use strict";
const APP=(function(){

"use strict";
// LSPV-2/547: separate source-bound reference grammar, NOT the historical /341 checker.
const C=[[1,2,3],[1,2,-3],[1,-2,3],[1,-2,-3],[-1,2,3],[-1,2,-3],[-1,-2,3],[-1,-2,-3]];
const src="p cnf 3 8\n"+C.map(c=>c.join(" ")+" 0").join("\n")+"\n";
const digest="a2f85326956ed24023d756dc4b0c205657cec886e8cf405083437b2b820cb719";
const id=i=>"s"+i, copy=o=>JSON.parse(JSON.stringify(o)), eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const sort=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const sat=(c,b)=>c.some(l=>(l>0?b[l-1]===1:b[-l-1]===0));
const sup=c=>[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);
const table=(s,pred)=>{let t=0;for(let i=0;i<(1<<s.length);i++){let b=[0,0,0];for(let j=0;j<s.length;j++)b[s[j]-1]=(i>>j)&1;if(pred(b))t|=1<<i;}return t;};
const clause=c=>({kind:"clause",clause:c,support:sup(c),table:table(sup(c),b=>sat(c,b)),depth:0});
const val=(v,b)=>{let i=0;for(let k=0;k<v.support.length;k++)i|=b[v.support[k]-1]<<k;return (v.table>>i)&1;};
const steps=[
 {id:"d0",rule:"RES",parents:["s0","s1"],pivot:3,clause:[1,2]},
 {id:"d1",rule:"RES",parents:["s2","s3"],pivot:3,clause:[1,-2]},
 {id:"d2",rule:"AND3",parents:["d0","d1"],support:[1,2],table:10,row:{mask:1,rhs:1}},
 {id:"d3",rule:"RES",parents:["s4","s5"],pivot:3,clause:[-1,2]},
 {id:"d4",rule:"RES",parents:["s6","s7"],pivot:3,clause:[-1,-2]},
 {id:"d5",rule:"AND3",parents:["d3","d4"],support:[1,2],table:5,row:{mask:1,rhs:0}},
 {id:"d6",rule:"XOR",parents:["d2","d5"],row:{mask:0,rhs:1}}
];
const pkt={format:"REFERENCE_EXT547_NOT_NATIVE_RMIX341",source:src,source_sha256:digest,sources:C.map((_,i)=>id(i)),proof:steps};
function replay(p,mode="EXTENSIONAL"){
 if(p.source!==src||p.source_sha256!==digest||!eq(p.sources,C.map((_,i)=>id(i))))throw Error("external source binding");
 if(typeof require==="function"){const h=require("crypto").createHash("sha256").update(p.source,"utf8").digest("hex");if(h!==digest)throw Error("SHA-256 source mismatch");}
 let states=new Map(),deps=new Map(),paid=new Set(),counts={RES:0,AND3:0,XOR:0},span=0;
 for(let i=0;i<C.length;i++){states.set(id(i),clause(C[i]));deps.set(id(i),[]);}
 for(let [i,n] of p.proof.entries()){
  if(!n||typeof n.id!=="string"||states.has(n.id)||paid.has(n.id))throw Error("paid ID freshness");
  if(!["RES","AND3","XOR"].includes(n.rule))return {status:"MAY_UNAUTHENTICATED",index:i,opcode:n.rule,min_abstract_cost:0};
  if(!Array.isArray(n.parents)||n.parents.length!==2||n.parents[0]===n.parents[1])throw Error("binary parents");
  let a=states.get(n.parents[0]),b=states.get(n.parents[1]);if(!a||!b)throw Error("bad parent reference");
  if(mode==="TAGGED"&&n.rule==="AND3"&&(a.origin==="RES"||b.origin==="RES"))return {status:"MAY_PARENT_GRAMMAR",index:i,min_abstract_cost:0};
  let v;
  if(n.rule==="RES"){
   if(a.kind!=="clause"||b.kind!=="clause"||!Number.isInteger(n.pivot)||n.pivot<1||n.pivot>3)throw Error("RES type/pivot");
   let x=n.pivot,pa=a.clause.includes(x),na=a.clause.includes(-x),pb=b.clause.includes(x),nb=b.clause.includes(-x);
   if(!((pa&&nb)||(na&&pb)))throw Error("RES not complementary");
   let r=sort([...new Set(a.clause.concat(b.clause).filter(l=>Math.abs(l)!==x))]);
   if(r.some(l=>r.includes(-l))||!eq(r,sort(n.clause)))throw Error("bad resolvent");
   v=clause(r);
  }else if(n.rule==="AND3"){
   if(!["clause","factor"].includes(a.kind)||!["clause","factor"].includes(b.kind))throw Error("AND3 type");
   let s=[...new Set(a.support.concat(b.support))].sort((x,y)=>x-y);
   if(s.length>3||!eq(s,n.support))throw Error("AND3 support");
   let t=table(s,bb=>Boolean(val(a,bb)&&val(b,bb)));
   if(t!==n.table)throw Error("AND3 truth-table");
   v={kind:"factor",support:s,table:t};
   if(n.row){
    if(!Number.isInteger(n.row.mask)||n.row.mask<0||n.row.mask>=8||![0,1].includes(n.row.rhs))throw Error("bad affine row");
    let m=n.row.mask,allowed=s.reduce((t,x)=>t|(1<<(x-1)),0);
    if(m&~allowed)throw Error("affine row outside support");
    let rt=table(s,bb=>{let x=0;for(let k=1;k<=3;k++)if(m&(1<<(k-1)))x^=bb[k-1];return x===n.row.rhs;});
    if(rt!==t)throw Error("false affine alias");
    v.row=n.row;
   }
  }else{
   if(!a.row||!b.row||!n.row)throw Error("XOR without rows");
   let m=a.row.mask^b.row.mask,r=a.row.rhs^b.row.rhs;
   if(n.row.mask!==m||n.row.rhs!==r)throw Error("wrong XOR row");
   v={kind:"affine",row:n.row,support:[1,2,3].filter(k=>(m>>(k-1))&1)};
  }
  v.depth=1+Math.max(a.depth,b.depth);v.origin=n.rule;states.set(n.id,v);deps.set(n.id,n.parents);paid.add(n.id);counts[n.rule]++;span=Math.max(span,v.depth);
 }
 if(!p.proof.length)throw Error("no proof");
 let last=states.get(p.proof.at(-1).id);
 if(!last||last.kind!=="affine"||last.row.mask!==0||last.row.rhs!==1)throw Error("no false row");
 let visited=new Set();function walk(i){if(visited.has(i))return;visited.add(i);for(let j of deps.get(i)||[])walk(j);}walk(p.proof.at(-1).id);
 if(C.some((_,i)=>!visited.has(id(i))))throw Error("not all sources used");
 return {status:"ACCEPT_REFERENCE_ONLY",logical_paid_nodes:paid.size,counts,span,source_sha256:digest,source_bytes:src.length,packet_bytes:JSON.stringify(p).length,all_sources_reachable:true};
}
function result(p,mode){try{return replay(p,mode)}catch(e){return {status:"REJECT_REFERENCE_ONLY",error:e.message}}}
function run(){
 let test=[],put=(name,p,exp,mode="EXTENSIONAL")=>{let o=result(p,mode);if(o.status!==exp)throw Error(name+":"+JSON.stringify(o));test.push({name,status:o.status,diagnostic:o.error||o.opcode||null,raw_json:JSON.stringify(p)});return o;};
 let base=put("strict-full-cube-minimal-mixed",pkt,"ACCEPT_REFERENCE_ONLY");
 if(!eq(base.counts,{RES:4,AND3:2,XOR:1})||base.logical_paid_nodes!==7||base.span!==3)throw Error("wrong accounting");
 let deletion=[];
 for(let x=0;x<8;x++){let b=[x&1,(x>>1)&1,(x>>2)&1],falseSources=C.map((c,i)=>sat(c,b)?null:i).filter(i=>i!==null);if(falseSources.length!==1)throw Error("UNSAT/source essential falsifier");deletion.push({source_id:id(falseSources[0]),satisfying_assignment_after_deletion:b.join("")});}
 put("tagged-RES-parent-grammar-is-unresolved",pkt,"MAY_PARENT_GRAMMAR","TAGGED");
 const mutate=[
 ["wrong-RES-pivot",p=>p.proof[0].pivot=2],
 ["wrong-RES-conclusion",p=>p.proof[0].clause=[1,-2]],
 ["wrong-AND3-table",p=>p.proof[2].table^=1],
 ["wrong-GF2-alias",p=>p.proof[2].row.rhs^=1],
 ["wrong-GF2-sink",p=>p.proof[6].row.rhs=0],
 ["external-source-forgery",p=>p.source=p.source.replace("1 2 3 0","-1 2 3 0")],
 ["source-hash-forgery",p=>p.source_sha256="0".repeat(64)],
 ["duplicate-paid-identity",p=>p.proof[1].id="d0"],
 ["unknown-parent",p=>p.proof[0].parents[0]="other"],
 ["missing-source-claim",p=>p.sources.pop()]
 ];
 for(let [name,change]of mutate){let p=copy(pkt);change(p);put(name,p,"REJECT_REFERENCE_ONLY");}
 for(let op of ["LOCAL-CONVERT","DEF","ASSUME","DISCHARGE","JOIN","WEAKEN","DELETE","SPLIT_AND"]){let p=copy(pkt);p.proof[0].rule=op;put("unauthenticated-"+op,p,"MAY_UNAUTHENTICATED");}
 const bad=copy(pkt);bad.proof[0].clause=[1,-2];
 let coarse={status:"MAY_UNCHECKED_SEMANTICS",min_abstract_cost:0,steps:bad.proof.length};
 if(result(bad).status!=="REJECT_REFERENCE_ONLY")throw Error("CEGAR path not falsified");
 return {status:"COMPUTATIONAL reference only; PROVED/RESTRICTED logical seven-node optimum",historical_checker:"not an authoritative RES dispatcher",source:src,source_sha256:digest,source_bytes:src.length,base,unique_source_deletion_witnesses:deletion,tests:test,tests_passed:test.length,cegar:{coarse,concrete:result(bad),refinement:"enforce exact source-bound RES pivot and resolvent",known_paths_preserved:true},remaining:"P2-D1/P2-C3/P2-B1/B2/B3 OPEN; native full grammar not recovered; peak space/time not measured"};
}
return {run,replay,pkt};

})();
const LEDGER=APP.run();
console.log(JSON.stringify(LEDGER,null,2));
