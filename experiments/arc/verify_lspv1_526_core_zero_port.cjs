/* Independently authored LSPV-1/526 structural and semantic verifier.
   Validates ORIGINAL local Tcore sources, exact signed DEF owners/facets,
   oriented RES, DAG acyclicity and six 0+Y=Y equality goals.
   Not the historical R_mix341 verifier. */
"use strict";
function verify(x){
 const norm=a=>{if(!Array.isArray(a)||a.some(t=>!Number.isInteger(t)||t===0))throw Error("bad literal");const z=[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);if(z.some(v=>z.includes(-v)))throw Error("tautology");return z};
 const eq=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
 const expected=[];for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++)if((a+b+c)%3!==0)expected.push([-(a+1),-(b+4),-(c+7)]);
 expected.push([1,2,3],[4,5,6],[7,8,9]);
 const L=x.lines,G=x.owners;
 if(expected.length!==21||L.length!==237||G.length!==34||!x.counts||x.counts.paid!==148||x.targets.length!==3||x.base_goals.length!==7)throw Error("top-level shape/cost");
 let checks=0,depth=[],kindCount={SOURCE:0,FACET:0,RES:0},facets=new Set();
 for(let j=0;j<G.length;j++){let g=G[j];if(g.owner!==j||g.id!==j+10||Math.abs(g.a)>=g.id||Math.abs(g.b)>=g.id||Math.abs(g.a)===Math.abs(g.b)||g.facets.length!==3)throw Error("nonconservative/invalid DEF");for(const f of g.facets){if(facets.has(f))throw Error("reused facet");facets.add(f);}checks++;}
 for(let i=0;i<L.length;i++){
  const v=L[i];if(v.id!==i||JSON.stringify(v.clause)!==JSON.stringify(norm(v.clause)))throw Error("noncanonical clause/index");if(!(v.kind in kindCount))throw Error("foreign inference");
  kindCount[v.kind]++;
  if(v.kind==="SOURCE"){if(i>=21||!eq(v.clause,expected[i]))throw Error("foreign original source");depth[i]=0;}
  if(v.kind==="FACET"){const g=G[v.owner];if(!g||!facets.has(i))throw Error("orphan facet");const j=g.facets.indexOf(i),facet=[[-g.id,g.a],[-g.id,g.b],[g.id,-g.a,-g.b]][j],tag=["left","right","back"][j];if(j<0||v.tag!==tag||!eq(v.clause,facet))throw Error("wrong facet owner/value");depth[i]=1;}
  if(v.kind==="RES"){const A=L[v.left],B=L[v.right],p=v.pivot;if(!A||!B||v.left>=i||v.right>=i||!Number.isInteger(p)||p<=0||!A.clause.includes(p)||!B.clause.includes(-p))throw Error("illegal RES/pivot/cycle");if(!eq(v.clause,[...A.clause.filter(z=>z!==p),...B.clause.filter(z=>z!==-p)]))throw Error("non-exact resolvent");depth[i]=1+Math.max(depth[v.left],depth[v.right]);}
  checks++;
 }
 if(facets.size!==102||JSON.stringify(kindCount)!==JSON.stringify({SOURCE:21,FACET:102,RES:114})||x.counts.sources!==21||x.counts.res!==114||x.counts.defs!==34||x.counts.facets!==102||x.counts.records!==237)throw Error("count mismatch");
 for(let k=0;k<3;k++){let t=x.targets[k];if(t.k!==k||t.input!==k+4||t.bit!==-(39+2*k)||!eq(L[t.positive].clause,[-t.bit,t.input])||!eq(L[t.negative].clause,[t.bit,-t.input]))throw Error("wrong equality output");checks+=2;}
 let satisfiers=0;for(let n=0;n<512;n++){
  const w={};for(let j=1;j<=9;j++)w[j]=!!(n&(1<<(j-1)));const lit=v=>v>0?w[v]:!w[-v],holds=c=>c.some(lit);
  for(const g of G)w[g.id]=lit(g.a)&&lit(g.b);
  for(const g of G)for(const j of g.facets){if(!holds(L[j].clause))throw Error("gate facet falsified");checks++;}
  if(expected.every(holds)){satisfiers++;for(const t of x.targets){if(lit(t.bit)!==lit(t.input)||!holds(L[t.positive].clause)||!holds(L[t.negative].clause))throw Error("equality countermodel");checks+=3;}for(const t of x.base_goals){if(!holds(L[t.id].clause))throw Error("old CORE-to-zero goal");checks++;}}
 }
 if(satisfiers!==9)throw Error("wrong charge/core models");
 return {pass:true,original_core_clauses:21,checked_original_assignments:512,source_models:satisfiers,paid_work:148,critical_path:Math.max(...depth),checks,original_source_validation:true,historical_Rmix_checker:false};
}
if(typeof module!=="undefined")module.exports={verify};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){const fs=require("fs");const x=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));console.log(JSON.stringify(verify(x),null,2));}
