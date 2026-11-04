/* LSPV-2/387 independent checker: reconstructs sources, gates and strict pivots. */
"use strict";
const fs=require("fs");
function verify(data){
 let assertions=0;
 function ok(v,m){assertions++;if(!v)throw Error(m);}
 function canon(c){return [...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
 function eq(a,b){return JSON.stringify(a)===JSON.stringify(b);}
 function checkClause(c){
   ok(Array.isArray(c),"clause array");
   ok(eq(c,canon(c)),"canonical clause");
   const seen=new Set();for(const x of c){ok(Number.isInteger(x)&&x!==0,"bad literal");ok(!seen.has(Math.abs(x)),"duplicate variable");seen.add(Math.abs(x));}
 }
 function val(l,assignment){let b=assignment[Math.abs(l)]===1;return l>0?b:!b;}
 function paritySources(n,b){
   const out=[];for(let mask=0;mask<2**n;mask++){
     let parity=0;for(let j=0;j<n;j++)parity^=(mask>>j)&1;
     if(parity!==b)out.push(Array.from({length:n},(_,j)=>(mask>>j)&1?-(j+1):j+1));
   }
   return out;
 }
 function checkRes(record,proof,i){
   ok(Array.isArray(record.parents)&&record.parents.length===2,"parents");
   const [a,b]=record.parents, p=record.pivot;
   ok(Number.isInteger(a)&&a>=0&&a<i&&Number.isInteger(b)&&b>=0&&b<i,"older parents");
   ok(Number.isInteger(p)&&p!==0,"pivot");
   const A=proof[a].c,B=proof[b].c;
   ok(A.includes(p)&&B.includes(-p),"pivot signs");
   const s=new Set([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
   ok(![...s].some(x=>s.has(-x)),"tautology");
   ok(eq(canon([...s]),record.c),"strict resolvent equality");
 }
 ok(data.version===387,"wrong version");
 ok(Array.isArray(data.rows)&&data.rows.length===6,"six cases");
 let resolutionSteps=0,gates=0;
 for(const r of data.rows){
   ok([2,3,4].includes(r.d)&&[0,1].includes(r.b),"row parameters");
   ok(eq(r.clauses,paritySources(r.d,r.b)),"parity source mismatch");
   ok(r.gates.length===3*(r.d-1),"incorrect gate count");
   let fresh=r.d+1;
   const assigned=[];
   for(const g of r.gates){
     ok(g.z===fresh++,"fresh gate");
     ok(Number.isInteger(g.a)&&Number.isInteger(g.b)&&g.a!==0&&g.b!==0,"gate input format");
     ok(Math.abs(g.a)<g.z&&Math.abs(g.b)<g.z&&Math.abs(g.a)!==Math.abs(g.b),"acyclic distinct inputs");
     gates++;
   }
   const defs=[];
   for(const {z,a,b} of r.gates)defs.push([-z,a],[-z,b],[z,-a,-b]);
   ok(eq(r.defs,defs),"definition differs");
   const init=[...r.clauses,...defs];
   ok(r.proof.length>=init.length,"short record set");
   for(let i=0;i<r.proof.length;i++){
     const node=r.proof[i];checkClause(node.c);
     if(i<init.length){ok(node.source===i&&eq(node.c,canon(init[i])),"bad original/def leaf");}
     else{checkRes(node,r.proof,i);resolutionSteps++;}
   }
   const target=r.b===1?r.output:-r.output;
   ok(r.derivedUnit===target,"wrong signed target");
   ok(r.proof.some(z=>eq(z.c,[target])),"unit not derived");
   for(let mask=0;mask<2**r.d;mask++){
     const env={};for(let i=1;i<=r.d;i++)env[i]=(mask>>(i-1))&1;
     for(const {z,a,b} of r.gates)env[z]=Number(val(a,env)&&val(b,env));
     const parity=Array.from({length:r.d},(_,i)=>env[i+1]).reduce((a,b)=>a^b,0);
     ok(Number(val(r.output,env))===parity,"xor gate function");
     for(const c of r.defs)ok(c.some(l=>val(l,env)),"broken gate definition");
     if(parity===r.b)ok(val(target,env),"source-implied parity unit");
   }
 }
 const t=data.triangle;
 ok(t&&t.paid===5&&Array.isArray(t.source)&&t.source.length===6,"triangle structure");
 const source=[
   [1,2],[-1,-2],[2,3],[-2,-3],[1,3],[-1,-3]
 ];
 ok(eq(t.source,source),"triangle signed source");
 ok(t.proof.length===11,"triangle live DAG length");
 let paid=0;const seen=new Map();
 for(const node of t.proof){
   ok(Number.isInteger(node.id)&&!seen.has(node.id),"unique proof ID");
   checkClause(node.c);
   if(node.parents){
     paid++;
     const [i,j]=node.parents;
     ok(seen.has(i)&&seen.has(j),"missing topological parent");
     const A=seen.get(i).c,B=seen.get(j).c,p=node.pivot;
     ok(A.includes(p)&&B.includes(-p),"triangle pivot");
     const s=new Set([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
     ok(![...s].some(x=>s.has(-x))&&eq(canon([...s]),node.c),"triangle wrong RES");
   }else ok(node.source===node.id&&eq(node.c,canon(source[node.source])),"triangle source mismatch");
   seen.set(node.id,node);
 }
 ok(paid===5&&t.proof.at(-1).c.length===0,"triangle proof cost");
 function models(cs){
   let out=[];for(let m=0;m<8;m++){
     const env={1:m&1,2:(m>>1)&1,3:(m>>2)&1};
     if(cs.every(c=>c.some(l=>val(l,env))))out.push(m);
   }return out;
 }
 ok(models(source).length===0,"triangle unsat");
 for(let i=0;i<6;i++)ok(models(source.filter((_,j)=>i!==j)).length>0,"indispensable source");
 const even=[[1,2],[-1,-2],[2,3],[-2,-3],[-1,3],[1,-3]];
 ok(eq(models(even),t.evenModels)&&models(even).length===2,"even controls");
 ok(Array.isArray(data.identities)&&data.identities.length===8,"rewrite table");
 for(const x of data.identities){
   const {a,y}=x, b=x.x;
   ok([a,b,y].every(v=>v===0||v===1),"truth input");
   ok(x.swap===((a^b)^y)&&x.swap===((a^y)^b),"swap");
   ok(x.cancel===((a^b)^b)&&x.cancel===a,"cancellation");
 }
 const bad=JSON.parse(JSON.stringify(data));
 bad.triangle.proof.at(-1).clause=[1];
 let negative=0;
 for(const item of [
   (()=>{const v=JSON.parse(JSON.stringify(data));v.rows[0].gates[0].b=v.rows[0].gates[0].a;return v;})(),
   (()=>{const v=JSON.parse(JSON.stringify(data));v.rows[1].proof.at(-1).c=[2];return v;})(),
   (()=>{const v=JSON.parse(JSON.stringify(data));v.triangle.proof.at(-1).c=[1];return v;})(),
   (()=>{const v=JSON.parse(JSON.stringify(data));v.triangle.source[0][0]*=-1;return v;})(),
   (()=>{const v=JSON.parse(JSON.stringify(data));v.rows[3].b=9;return v;})()
 ]){
   try{verifyNoMutation(item);throw Error("bad fixture accepted");}catch(e){if(String(e).includes("bad fixture accepted"))throw e;negative++;}
 }
 function verifyNoMutation(d){
   if(d.version!==387||d.rows.length!==6)throw Error("header");
   for(const r of d.rows){
     if(![0,1].includes(r.b))throw Error("charge");
     if(!eq(r.clauses,paritySources(r.d,r.b)))throw Error("source");
     let z=r.d+1;
     for(const g of r.gates)if(g.z!==z++||Math.abs(g.a)===Math.abs(g.b))throw Error("gate");
     const defs=r.gates.flatMap(({z,a,b})=>[[-z,a],[-z,b],[z,-a,-b]]);
     if(!eq(defs,r.defs))throw Error("def");
     for(let i=0;i<r.proof.length;i++){
       const v=r.proof[i];
       if(i<r.clauses.length+r.defs.length){if(!eq(v.c,canon([...r.clauses,...r.defs][i])))throw Error("leaf");}
       else{const [a,b]=v.parents,p=v.pivot;if(!r.proof[a].c.includes(p)||!r.proof[b].c.includes(-p))throw Error("pivot");
         const s=new Set([...r.proof[a].c.filter(x=>x!==p),...r.proof[b].c.filter(x=>x!==-p)]);
         if(!eq(v.c,canon([...s])))throw Error("resolution");}
     }
   }
   if(!eq(d.triangle.source,source)||!eq(d.triangle.proof.at(-1).c,[]))throw Error("triangle");
 }
 ok(negative===5,"mutant rejection");
 return {status:"INDEPENDENT_CHECK_PASS",assertions,strictResolutionNodes:resolutionSteps+paid,
  chargedAND2:gates,trianglePaid:paid,sourceDeletionWitnesses:6,mutantsRejected:negative};
}
const data=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
console.log(JSON.stringify(verify(data),null,2));
