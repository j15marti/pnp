// LSPV-2 HITTING-BACKDOOR-FLIP-DAG276 compact independently executable finite witness.
// Usage: node backdoor_flip276_compact.js
// This is a compact spot-check, not the complete 14-case Python producer in the ZIP.
"use strict";
function canonical(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a)}
function test(c,a){return c.some(l=>a[Math.abs(l)]===(l>0?1:0))}
function allModels(F,n){
 let out=[];for(let mask=0;mask<2**n;mask++){let a={};
 for(let i=1;i<=n;i++)a[i]=((mask>>(i-1))&1);
 if(F.every(c=>test(c,a)))out.push(a)}
 return out
}
function force(x,p,q){let z=[];for(let u of [p,-p])for(let v of [q,-q])z.push(canonical([x,u,v]));return z}
function prove(F,T,b){
 let R=new Set(F.flat().map(x=>Math.abs(x)).filter(x=>!T.includes(x)));
 if(!F.every(c=>c.filter(l=>R.has(Math.abs(l))).length<=2))throw Error("not backdoor");
 let nodes=F.map((c,j)=>({source:j,clause:c})),active=[];
 for(let j=0;j<F.length;j++){
  if(F[j].some(l=>T.includes(Math.abs(l))&&test([l],b)))continue;
  let r=canonical(F[j].filter(l=>R.has(Math.abs(l))));
  active.push([j,r])
 }
 let rv=[...R].sort((a,b)=>a-b);
 for(let mask=0;mask<(1<<rv.length);mask++){
  let a={...b};rv.forEach((v,i)=>a[v]=(mask>>i)&1);
  if(F.every(c=>test(c,a)))return {sat:true,witness:a,nodes:[],root:null}
 }
 for(let x of rv){
  let pos=active.filter(([i,c])=>c.includes(x)),neg=active.filter(([i,c])=>c.includes(-x));
  let keep=active.filter(([i,c])=>!c.includes(x)&&!c.includes(-x));
  for(let [i,a] of pos)for(let [j,b] of neg){
   let r=canonical([...a.filter(l=>l!==x),...b.filter(l=>l!==-x)]);
   if(r.some(l=>r.includes(-l)))continue;
   let full=canonical([...nodes[i].clause.filter(l=>l!==x),...nodes[j].clause.filter(l=>l!==-x)]);
   if(full.some(l=>full.includes(-l)))throw Error("tautological lifted clause");
   let k=nodes.length;nodes.push({parents:[i,j],pivot:x,clause:full});keep.push([k,r]);
  }
  let uniq=new Map();for(let [i,r] of keep){let key=r.join(",");
   if(!uniq.has(key)||nodes[i].clause.length<nodes[uniq.get(key)][0].clause.length)uniq.set(key,[i,r])}
  active=[...uniq.values()]
 }
 let roots=active.filter(([i,r])=>r.length===0);
 if(!roots.length)throw Error("missing DP empty residue");
 let root=roots[0][0],nogood=nodes[root].clause;
 if(nogood.some(l=>!T.includes(Math.abs(l))||test([l],b)))throw Error("bad nogood");
 return {sat:false,nogood,root,nodes};
}
function verify(F,r){
 if(r.sat)return F.every(c=>test(c,r.witness));
 for(let k=0;k<r.nodes.length;k++){
  let x=r.nodes[k],got=canonical(x.clause);
  if(got.join(",")!==x.clause.join(","))return false;
  if("source" in x){if(got.join(",")!==F[x.source].join(","))return false}
  else {let [p,q]=x.parents, v=x.pivot;
   if(p>=k||q>=k||!r.nodes[p].clause.includes(v)||!r.nodes[q].clause.includes(-v))return false;
   let y=canonical([...r.nodes[p].clause.filter(l=>l!==v),...r.nodes[q].clause.filter(l=>l!==-v)]);
   if(y.join(",")!==got.join(","))return false;
  }
 }
 return r.nodes[r.root].clause.join(",")===r.nogood.join(",")
}
function repro(){
 let pos=force(1,2,3),both=[...pos,...force(-1,4,5)],rows=[];
 for(let [name,F,n] of [["yes",pos,3],["no",both,5]]){
  let answers=[];
  for(let x of [0,1]){
   let r=prove(F,[1],{1:x});if(!verify(F,r))throw Error("proof rejected");
   answers.push({x,sat:r.sat,nogood:r.nogood||null,proof_nodes:r.nodes.length});
   if(r.sat)break
  }
  let truth=allModels(F,n).length>0;
  if(truth!==answers.some(a=>a.sat))throw Error("incorrect polarity");
  rows.push({name,truth,answers})
 }
 return rows
}
if(typeof process!=="undefined"&&process.stdout)console.log(JSON.stringify(repro(),null,2));