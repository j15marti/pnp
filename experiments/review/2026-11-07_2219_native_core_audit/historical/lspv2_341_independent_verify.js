/* LSPV-2 341 independent verifier. Usage: node thisfile.js results.json */
const fs=require('fs'); const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const verify=(function(data){
"use strict";
let checks=0;
function assert(b,msg){checks++;if(!b)throw Error("Verifier: "+msg);}
function validateCNF(raw){
 if(typeof raw!=="string")throw Error("not string");
 const t=raw.trim().split(/\s+/),nPos=t.indexOf("p");if(nPos!==0||t[1]!=="cnf")throw Error("missing header");
 const nv=Number(t[2]), nc=Number(t[3]);if(!Number.isInteger(nv)||nv<0||!Number.isInteger(nc)||nc<0)throw Error("bad counts");
 let clauses=[],row=[];for(let i=4;i<t.length;i++){
  if(!/^-?\d+$/.test(t[i]))throw Error("nonnumeric literal");let x=Number(t[i]);
  if(!Number.isSafeInteger(x))throw Error("unsafe integer");
  if(x===0){clauses.push(row);row=[];}else {if(Math.abs(x)>nv)throw Error("out of range");row.push(x);}
 }
 if(row.length)throw Error("unterminated clause");
 if(clauses.length!==nc)throw Error("wrong clause count");
 return {nv,nc,clauses};
}
const malformed=["p cnf 2 1\n1 -2","p cnf 2 1\n3 0","p cnf 2 1\na 0","p cnf 2 2\n1 0","cnf 2 1\n1 0","p cnf -2 0","p cnf 2 1\n1.4 0"];
for(let x of malformed){let failed=false;try{validateCNF(x)}catch(e){failed=true;}assert(failed,"malformed input was accepted");}
assert(validateCNF("p cnf 2 2\n1 1 0\n0").nc===2,"valid duplicate-literal/empty-clause control");
function clauseSat(c,bits){for(let lit of c){let p=Math.abs(lit)-1,b=Number(bits[p]);if((lit>0&&b===1)||(lit<0&&b===0))return true;}return false;}
function graphStructure(g){
 assert(g.n>=4&&g.edges.length*2===3*g.n,"cubic dimensions");
 const degree=Array(g.n).fill(0),pairs=new Set();
 for(const [u,v] of g.edges){
  assert(Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&v>=0&&u<g.n&&v<g.n&&u!==v,"edge");
  const k=Math.min(u,v)+":"+Math.max(u,v);assert(!pairs.has(k),"edge duplicated");pairs.add(k);degree[u]++;degree[v]++;
 }
 assert(degree.every(x=>x===3),"degree");
 function connected(withoutV,withoutEdge=-1){
  const source=Array.from({length:g.n},(_,i)=>i).find(i=>i!==withoutV);
  if(source===undefined)return false;
  let seen=new Set([source]),todo=[source];
  for(let j=0;j<todo.length;j++){let u=todo[j];
   for(let e=0;e<g.edges.length;e++){if(e===withoutEdge)continue;
    let [a,b]=g.edges[e],v=a===u?b:b===u?a:-1;if(v>=0&&v!==withoutV&&!seen.has(v)){seen.add(v);todo.push(v);}
   }
  }
  return seen.size===g.n-(withoutV===-1?0:1);
 }
 assert(connected(-1),"graph connected");
 const bridgeless=g.edges.every((_,i)=>connected(-1,i));
 const vertexBiconnected=Array.from({length:g.n},(_,v)=>connected(v)).every(Boolean);
 if(bridgeless)assert(vertexBiconnected,"bridgeless cubic no cut vertex");
 return {bridgeless,vertexBiconnected};
}
function evalTable(tab,support,bits){
 let p=0;for(let i=0;i<support.length;i++)p|=Number(bits[support[i]])<<i;
 return (tab>>p)&1;
}
function independentCheck(f){
 const g=f.graph,E=g.edges.length,V=g.n,gs=graphStructure(g);
 assert(f.charges.length===V,"charges size");assert(f.charges.reduce((x,y)=>x^y,0)===1,"odd parity charge");
 const incid=Array.from({length:V},()=>[]);
 g.edges.forEach(([u,v],e)=>{incid[u].push(e);incid[v].push(e);});
 const src=new Map(),byVertex=Array.from({length:V},()=>new Set());
 assert(f.clauses.length===4*V,"clause count");
 for(const c of f.clauses){
  const v=c.vertex;assert(Number.isInteger(v)&&v>=0&&v<V,"vertex");assert(!src.has(c.id),"unique source id");
  assert(c.literals.length===3,"local width");
  const edgeIds=c.literals.map(x=>Math.abs(x)-1).sort((a,b)=>a-b);
  assert(edgeIds.join(",")===incid[v].slice().sort((a,b)=>a-b).join(","),"signed incidence mismatch");
  const loc=c.literals.map(x=>x<0?1:0);
  let parity=loc.reduce((x,y)=>x^y,0);assert(parity!==f.charges[v],"source forbidden pattern parity");
  const key=incid[v].map(e=>c.literals.find(x=>Math.abs(x)===e+1)<0?1:0).join("");
  assert(!byVertex[v].has(key),"duplicate local forbidden pattern");byVertex[v].add(key);
  const sup=incid[v].slice(),tab=Array.from({length:8},(_,a)=>{
    let bits=Array(E).fill(0);sup.forEach((edge,i)=>bits[edge]=(a>>i)&1);return clauseSat(c.literals,bits)?1:0;
  }).reduce((x,y,i)=>x|(y<<i),0);
  src.set(c.id,{kind:"factor",support:sup,table:tab});
 }
 assert(byVertex.every(s=>s.size===4),"missing original local pattern");
 const byId=new Map(src),used=new Set();
 assert(f.proof.length===4*V-1,"proof candidate length");
 for(const p of f.proof){
  assert(!byId.has(p.id),"fresh inference ID");assert(p.parents?.length===2,"binary rule parent count");
  const [a,b]=p.parents.map(id=>byId.get(id));assert(a&&b,"missing antecedent");assert(p.parents[0]!==p.parents[1],"duplicate parents");
  if(p.rule==="AND3"){
   assert(a.kind==="factor"&&b.kind==="factor"&&p.kind==="factor","AND3 types");
   const sup=[...new Set([...a.support,...b.support])];
   assert(sup.length<=3&&p.support?.length===sup.length&&new Set(p.support).size===sup.length,"AND3 support size");
   assert(sup.every(x=>p.support.includes(x)),"AND3 support names");
   let table=0;
   for(let m=0;m<(1<<sup.length);m++){
    let bits=Array(E).fill(0);for(let j=0;j<p.support.length;j++)bits[p.support[j]]=(m>>j)&1;
    if(evalTable(a.table,a.support,bits)&&evalTable(b.table,b.support,bits))table|=1<<m;
   }
   assert(table===p.table,"incorrect AND3 conjunction");
   if(p.row){
    const mask=BigInt(p.row.mask),rhs=p.row.rhs;
    assert((rhs===0||rhs===1),"parity RHS");
    assert([...Array(E).keys()].every(e=>((mask>>BigInt(e))&1n)===0n||p.support.includes(e)),"unscoped parity variable");
    for(let m=0;m<(1<<p.support.length);m++){
      let bits=Array(E).fill(0);for(let j=0;j<p.support.length;j++)bits[p.support[j]]=(m>>j)&1;
      let lhs=0;for(let e=0;e<E;e++)if((mask>>BigInt(e))&1n)lhs^=bits[e];
      assert(((p.table>>m)&1)===(lhs===rhs?1:0),"invalid affine alias");
    }
   }
  }else if(p.rule==="XOR"){
   assert(a.row&&b.row&&p.row&&p.kind==="affine","XOR types");
   const mask=BigInt(a.row.mask)^BigInt(b.row.mask),rhs=a.row.rhs^b.row.rhs;
   assert(BigInt(p.row.mask)===mask&&p.row.rhs===rhs,"bad GF2 elimination");
  }else throw Error("unknown rule");
  byId.set(p.id,p);
 }
 const last=f.proof.at(-1);assert(last.kind==="affine"&&BigInt(last.row.mask)===0n&&last.row.rhs===1,"invalid sink");
 function ancestor(id){if(used.has(id))return;used.add(id);const p=byId.get(id);if(p.parents)for(const parent of p.parents)ancestor(parent);}
 ancestor(last.id);
 assert(f.clauses.every(c=>used.has(c.id)),"not all sources in proof");
 assert(f.deleted.length===f.clauses.length,"witness list");
 let essential=0;
 for(let i=0;i<f.deleted.length;i++){
  const d=f.deleted[i],c=f.clauses[i];assert(d.sourceId===c.id,"deletion indexing");
  if(d.assignment!==null){
   essential++;assert(d.assignment.length===E&&/^[01]+$/.test(d.assignment),"bad deletion witness bits");
   assert(!clauseSat(c.literals,d.assignment),"deletion witness does not falsify deleted clause");
   for(let j=0;j<f.clauses.length;j++)if(i!==j)assert(clauseSat(f.clauses[j].literals,d.assignment),"deletion witness invalid");
  }
 }
 assert(essential===f.properties.essential,"essential count");
 if(gs.bridgeless)assert(essential===f.clauses.length,"bridgeless minimality failed");
 if(!gs.bridgeless&&f.graph.name==="BRIDGE_K4x2")assert(essential<f.clauses.length,"bridge falsifier absent");
 assert(f.evenWitness.length===E&&/^[01]+$/.test(f.evenWitness),"even witness");
 let even=Array.from({length:V},()=>0);
 for(let v=0;v<V;v++){let bits=incid[v].map(e=>Number(f.evenWitness[e]));assert((bits[0]^bits[1]^bits[2])===even[v],"even parity fail");}
 if(E<=15){ // independent exhaustive truth-table count, not producer elimination
  let oddCount=0,evenCount=0;
  for(let x=0;x<(1<<E);x++){
   const bits=Array.from({length:E},(_,i)=>(x>>i)&1);
   if(f.clauses.every(c=>clauseSat(c.literals,bits)))oddCount++;
   let ok=true;for(let v=0;v<V;v++){let val=0;for(let e of incid[v])val^=bits[e];if(val!==0){ok=false;break;}}if(ok)evenCount++;
  }
  assert(oddCount===0,"UNSAT brute-force failure");
  assert(evenCount===(1<<(E-V+1)),"even count by rank");
 }
 return {name:g.name,proofNodes:f.proof.length,essential,allEssential:essential===f.clauses.length,
     bridgeless:gs.bridgeless,certifiedMinimum:gs.bridgeless?f.clauses.length-1:null};
}
let cases=data.fixtures.map(independentCheck);
function negative(test,name){let rejected=false;try{independentCheck(test);}catch(e){rejected=true;}assert(rejected,"corrupted "+name+" accepted");}
for(const kind of ["sink","conjunction","parent","witness","badsource"]){
 const c=JSON.parse(JSON.stringify(data.fixtures[0]));
 if(kind==="sink")c.proof.at(-1).row.rhs^=1;
 if(kind==="conjunction")c.proof[0].table^=1;
 if(kind==="parent")c.proof[0].parents[0]="fake-source";
 if(kind==="witness")c.deleted[0].assignment=c.deleted[0].assignment.replace(/^./,b=>b==="0"?"1":"0");
 if(kind==="badsource")c.clauses[0].literals[0]=999;
 negative(c,kind);
}
assert(cases.length===data.summary.length,"summary count");
return {verifier:"independent literal/truth-table/GF2/provenance checker",checks,cases,malformed:malformed.length,corruptions:5,
scope:"unbounded DAG optimality for bridgeless cases is certified by 4h essentiality witnesses plus binary-arity lemma, not optimizer BFS"};
});
console.log(JSON.stringify(verify(data),null,2));
