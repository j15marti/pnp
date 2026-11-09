/* LSPV1/525 independent packet checker. node verify_lspv1_525_zero_sum.cjs packet.json */
"use strict";
const fs=require("fs");
function verify(x){
 const P=x.proof,L=P.lines,G=P.defs,normalize=a=>{if(!Array.isArray(a)||a.some(v=>!Number.isInteger(v)||v===0))throw Error("bad literal");const c=[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);if(c.some(v=>c.includes(-v)))throw Error("tautology");return c},equals=(a,b)=>JSON.stringify(normalize(a))===JSON.stringify(normalize(b));
 const sources=[[1,2,3],[-1,-2,4],[-1,-2,-4],[-1,-3,4],[-1,-3,-4],[-2,-3,4],[-2,-3,-4]];
 if(P.paid_defs!==34||P.paid_res!==81||P.paid_work!==115||G.length!==34||L.length!==190||x.targets.length!==3)throw Error("counts");
 let facts=new Map(),last=7,tests=0;
 for(let i=0;i<G.length;i++){let g=G[i];if(g.owner!==i||g.id!==last+1||Math.abs(g.a)>last||Math.abs(g.b)>last||Math.abs(g.a)===Math.abs(g.b))throw Error("gates");last=g.id;[[[-g.id,g.a],"left"],[[-g.id,g.b],"right"],[[g.id,-g.a,-g.b],"back"]].forEach(([c,tag],j)=>facts.set(g.facets[j],{c,tag,owner:i}));tests++;}
 let nsource=0,nfacet=0,nres=0;let depth=L.map(()=>0);
 for(let i=0;i<L.length;i++){let v=L[i];if(v.id!==i||JSON.stringify(v.clause)!==JSON.stringify(normalize(v.clause)))throw Error("record");
  if(v.kind==="SOURCE"){if(i!==nsource||nsource>=7||!equals(v.clause,sources[nsource]))throw Error("source");nsource++;}
  else if(v.kind==="FACET"){let f=facts.get(i);if(!f||v.tag!==f.tag||v.owner!==f.owner||!equals(v.clause,f.c))throw Error("facet");nfacet++;}
  else if(v.kind==="RES"){let a=L[v.left],b=L[v.right],p=v.pivot;if(!a||!b||v.left>=i||v.right>=i||!Number.isInteger(p)||p<=0||!a.clause.includes(p)||!b.clause.includes(-p))throw Error("pivot");if(!equals(v.clause,[...a.clause.filter(z=>z!==p),...b.clause.filter(z=>z!==-p)]))throw Error("resolvent");depth[i]=1+Math.max(depth[v.left],depth[v.right]);nres++;}
  else throw Error("rule");tests++;
 }
 if(nsource!==7||nfacet!==102||nres!==81||last!==41)throw Error("types");
 if(JSON.stringify(x.zero_units.map(i=>L[i].clause))!==JSON.stringify([[-22],[24],[26]]))throw Error("zero refs");
 for(let k=0;k<3;k++){const t=x.targets[k];if(t.k!==k||t.bit>=0||t.input!==5+k||!equals(L[t.positive].clause,[-t.bit,t.input])||!equals(L[t.negative].clause,[t.bit,-t.input]))throw Error("equality goal");tests+=2;}
 let sat=0,other=0;for(let mask=0;mask<128;mask++){let V={};for(let j=1;j<=7;j++)V[j]=!!(mask&(1<<(j-1)));const lit=z=>z>0?V[z]:!V[-z];for(let g of G)V[g.id]=lit(g.a)&&lit(g.b);for(let g of G){for(let c of [[-g.id,g.a],[-g.id,g.b],[g.id,-g.a,-g.b]]){if(!c.some(lit))throw Error("semantic gate");tests++;}}if(sources.every(c=>c.some(lit))){sat++;for(let t of x.targets){if(lit(t.bit)!==lit(t.input)||!L[t.positive].clause.some(lit)||!L[t.negative].clause.some(lit))throw Error("counterexample");tests+=3;}}else other++;}
 if(sat!==48||other!==80)throw Error("source model count");
 return {pass:true,checks:tests,source_models:sat,rejected_source_assignments:other,maximum_resolution_depth:Math.max(...depth)};
}
if(require.main===module){if(process.argv.length!==3)throw Error("Expected JSON file");const x=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));console.log(JSON.stringify(verify(x),null,2));}
module.exports={verify};
