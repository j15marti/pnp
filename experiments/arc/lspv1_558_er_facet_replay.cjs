// LSPV-1/558: executable DECLARED facet-owner + Resolution completion, not /341.
"use strict";
const must=(p,m)=>{if(!p)throw Error(m)};
const key=a=>JSON.stringify([...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y));
const canon=a=>{must(Array.isArray(a)&&a.every(x=>Number.isInteger(x)&&x!==0),"literal");let z=new Set(a);must(![...z].some(x=>z.has(-x)),"tautological result");return JSON.parse(key(a))};
const source=[];
for(let c of [3,-3])for(let a of [1,-1])for(let b of [2,-2])source.push([a,b,c]);
const original=JSON.stringify(source);
const facets=(z,a,b)=>[[-z,a,b],[z,-a],[z,-b]].map(canon);
const res=(a,b,p)=>{
 let x=new Set(a),y=new Set(b);
 must((x.has(p)&&y.has(-p))||(x.has(-p)&&y.has(p)),"pivot");
 return canon([...a,...b].filter(l=>Math.abs(l)!==p));
};
function construct(){
 const map=new Map(source.map((c,i)=>[key(c),"s"+i])),ids=new Map(source.map((c,i)=>["s"+i,canon(c)]));
 const get=c=>{let v=map.get(key(c));must(v,"source reference");return v};
 const proof=[{id:"d0",rule:"DEF",z:4,a:1,b:2}];
 facets(4,1,2).forEach((c,i)=>ids.set("d0:f"+i,c));
 const add=(x,y,p)=>{
  let id="d"+proof.length,cl=res(ids.get(x),ids.get(y),p);
  proof.push({id,rule:"RES",from:[x,y],pivot:p,clause:cl});ids.set(id,cl);return id;
 };
 const units=[];
 for(let c of [3,-3]){
  let A=get([1,2,c]),B=get([1,-2,c]),C=get([-1,2,c]),D=get([-1,-2,c]);
  let E=add(A,"d0:f1",1),G=add(E,"d0:f2",2);
  let H=add(B,D,1),I=add(C,D,2);
  let J=add("d0:f0",I,1),K=add(J,H,2);
  units.push(add(G,K,4));
 }
 add(units[0],units[1],3);
 return {source:JSON.parse(original),proof};
}
function check(cert){
 must(JSON.stringify(cert.source)===original,"source externally bound");
 let db=new Map(source.map((c,i)=>["s"+i,canon(c)])),used=new Set(db.keys()),live=new Set([1,2,3]);
 let defs=0,rules=0,facetsMade=0;
 for(let n of cert.proof){
  must(/^d\d+$/.test(n.id)&&!used.has(n.id),"paid identity");
  if(n.rule==="DEF"){
   must(Number.isInteger(n.z)&&n.z>3&&!live.has(n.z),"fresh output");
   must(Number.isInteger(n.a)&&Number.isInteger(n.b)&&live.has(Math.abs(n.a))&&live.has(Math.abs(n.b)),"gate inputs");
   must(Math.abs(n.a)!==Math.abs(n.b),"test-subgrammar distinct inputs");
   let fs=facets(n.z,n.a,n.b);
   for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++){
    let v={[Math.abs(n.a)]:x,[Math.abs(n.b)]:y,[n.z]:z};
    let lit=t=>t>0?v[t]:1-v[-t];
    must(fs.every(c=>c.some(lit))===(z===(lit(n.a)|lit(n.b))),"facets are exactly equivalent");
   }
   fs.forEach((c,i)=>{let id=n.id+":f"+i;must(!used.has(id),"facet collision");db.set(id,c);used.add(id);facetsMade++});
   live.add(n.z);defs++;
  }else if(n.rule==="RES"){
   must(Array.isArray(n.from)&&n.from.length===2&&n.from.every(p=>db.has(p)),"parents");
   let out=res(db.get(n.from[0]),db.get(n.from[1]),n.pivot);
   must(key(out)===key(n.clause),"exact resolvent");
   db.set(n.id,out);rules++;
  }else throw Error("unknown rule");
  used.add(n.id);
 }
 must(cert.proof.length>0&&key(db.get(cert.proof.at(-1).id))==="[]","empty root");
 return {defs,resolutions:rules,facets:facetsMade,paid:defs+rules};
}
const good=construct(),ok=check(good),bad=[];
function corrupt(name,f){let z=JSON.parse(JSON.stringify(good));f(z);let reject=false;try{check(z)}catch(e){reject=true}must(reject,"mutation passes "+name);bad.push(name)}
corrupt("source_changed",q=>q.source[0][0]=-1);
corrupt("missing_facet_owner",q=>q.proof[1].from[1]="d9:f1");
corrupt("wrong_RES_pivot",q=>q.proof[1].pivot=3);
corrupt("forged_RES_output",q=>q.proof[1].clause=[3]);
corrupt("reused_paid_id",q=>q.proof[2].id=q.proof[1].id);
corrupt("cyclic_DEF",q=>q.proof[0].a=4);
corrupt("unknown_rule",q=>q.proof[1].rule="SPLIT");
corrupt("drop_RES_node",q=>q.proof.splice(2,1));
let sat=0;for(let a=0;a<8;a++){let v={1:a&1,2:(a>>1)&1,3:(a>>2)&1};if(source.every(c=>c.some(l=>l>0?v[l]:!v[-l])))sat++}
must(sat===0,"F8 must be UNSAT");
console.log(JSON.stringify({role:"LSPV-1",result:558,scope:"DECLARED R_fac owner-facet + RES completion, NOT authenticated historical R_mix341 byte parser",originalClauses:8,originalVariables:3,source,paid:ok,proof:good.proof,satModels:sat,hostileRejected:bad},null,2));
