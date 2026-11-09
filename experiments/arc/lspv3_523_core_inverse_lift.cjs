/* LSPV-3/523 source-core port of LSPV-1/524 packet.
   Execute from repository root: node experiments/arc/lspv3_523_core_inverse_lift.cjs
   Uses the exact /524 generator as its dependency. This is proposed ER2,
   NOT the unverified historical R_mix341 accepted-byte language. */
"use strict";
function canon(a){
  let b=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
  if(b.some(x=>b.includes(-x)))throw Error("tautology");
  return b;
}
function same(a,b){return JSON.stringify(canon(a))===JSON.stringify(canon(b));}
function lift(P){
  const old=P.proof, newlines=[], oldToNew={}, owners=[], src=[], amo={}, signs=[1,1,1], charge=0;
  const add=(type,c,more={})=>{let id=newlines.length;newlines.push({id,kind:type,clause:canon(c),...more});return id;};
  function original(c,label){let id=add("SOURCE",c,{label});src.push(id);return id;}
  const lookup=new Map();
  for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++){
    if((a+b+c)%3!==charge){
      const clause=[-(a+1),-(b+4),-(c+7)];
      lookup.set(canon(clause).join(","),original(clause,"D:"+a+b+c));
    }
  }
  const ax=original([1,2,3],"ALO:X"),ay=original([4,5,6],"ALO:Y"),az=original([7,8,9],"ALO:Z");
  if(src.length!==21)throw Error("21-source count");
  function res(u,v,p,expected){
    let A=newlines[u].clause,B=newlines[v].clause;
    if(!A.includes(p)){[u,v]=[v,u];[A,B]=[B,A];}
    if(!A.includes(p)||!B.includes(-p))throw Error("oriented RES");
    let cl=canon([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
    if(expected&&!same(cl,expected))throw Error("resolvent mismatch");
    return add("RES",cl,{left:u,right:v,pivot:p});
  }
  for(const [a,b] of [[1,2],[1,3],[2,3]]){
    let ys=[];
    for(let j=0;j<3;j++){
      let r=az;
      for(let k=0;k<3;k++){
        let t=([a-1,b-1]).find(v=>(v+j+k)%3!==charge);
        const key=canon([-(t+1),-(j+4),-(k+7)]).join(",");
        if(!lookup.has(key))throw Error("foreign source clause");
        r=res(r,lookup.get(key),k+7);
      }
      if(!same(newlines[r].clause,[-a,-b,-(j+4)]))throw Error("bad intermediate AMO");
      ys.push(r);
    }
    let r=ay;for(let j=0;j<3;j++)r=res(r,ys[j],j+4);
    if(!same(newlines[r].clause,[-a,-b]))throw Error("bad final AMO");
    amo[a+","+b]=r;
  }
  const mappedLiteral=l=>{
    if(Math.abs(l)===4)throw Error("padding bit 4 leaked to port");
    let sign=Math.sign(l),abs=Math.abs(l);
    return sign*(abs>=5?abs+5:abs);
  };
  oldToNew[0]=ax;
  oldToNew[7]=amo["1,2"];
  oldToNew[8]=amo["1,3"];
  oldToNew[9]=amo["2,3"];
  for(const node of old.lines.slice(10)){
    if(node.kind==="FACET"){
      oldToNew[node.id]=add("FACET",node.clause.map(mappedLiteral),{owner:node.owner,tag:node.tag});
    }else if(node.kind==="RES"){
      let u=oldToNew[node.left],v=oldToNew[node.right];
      if(u===undefined||v===undefined)throw Error("unmapped parent");
      oldToNew[node.id]=res(u,v,mappedLiteral(node.pivot),node.clause.map(mappedLiteral));
    }else throw Error("unexpected post-AMO line kind "+node.kind);
  }
  for(const g of old.definitions){
    owners.push({...g,id:mappedLiteral(g.id),a:mappedLiteral(g.a),b:mappedLiteral(g.b),
      facets:g.facets.map(f=>oldToNew[f])});
  }
  const targets=old.targets.map(t=>({id:oldToNew[t.id],clause:newlines[oldToNew[t.id]].clause}));
  const nres=newlines.filter(l=>l.kind==="RES").length;
  if(newlines.length!==165||nres!==87||owners.length!==19||targets.length!==7)throw Error("count mismatch");
  if(!same(targets[0].clause,[11,12,13])||!same(targets[4].clause,[-24])||
     !same(targets[5].clause,[26])||!same(targets[6].clause,[28]))throw Error("goals mismatch");
  const ext={source:src.map(id=>newlines[id].clause),lines:newlines,owners,targets,
     counts:{originals:21,RES:nres,DEF:owners.length,facets:57,paid:nres+owners.length,
       literal_occurrences:newlines.reduce((a,l)=>a+l.clause.length,0)}};
  return ext;
}
function replay(q){
  const n=q.lines,owners=q.owners;
  const cols=new Map(),depth=[];
  for(let i=0;i<n.length;i++){
    let v=n[i];if(v.id!==i)throw Error("line ID");
    if(!same(v.clause,canon(v.clause)))throw Error("noncanonical line");
    if(v.kind==="SOURCE"){if(i>=21)throw Error("source not original");depth[i]=0;}
    else if(v.kind==="FACET"){
      let g=owners[v.owner],pos=g.facets.indexOf(v.id),cl=[[-g.id,g.a],[-g.id,g.b],[g.id,-g.a,-g.b]][pos];
      if(pos<0||!same(v.clause,cl))throw Error("unowned facet");
      depth[i]=1;
    }else if(v.kind==="RES"){
      if(v.left>=i||v.right>=i)throw Error("forward resolution");
      const A=n[v.left].clause,B=n[v.right].clause,p=v.pivot;
      if(!A.includes(p)||!B.includes(-p))throw Error("pivot");
      if(!same(v.clause,canon([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)])))throw Error("res");
      depth[i]=1+Math.max(depth[v.left],depth[v.right]);
    }else throw Error("kind");
  }
  const original=new Set();
  for(let i=0;i<3;i++)for(let j=0;j<3;j++)for(let k=0;k<3;k++)
    if((i+j+k)%3!==0)original.add(canon([-(i+1),-(j+4),-(k+7)]).join(","));
  [[1,2,3],[4,5,6],[7,8,9]].forEach(c=>original.add(canon(c).join(",")));
  if(original.size!==21||new Set(q.source.map(c=>canon(c).join(","))).size!==21||
    q.source.some(c=>!original.has(canon(c).join(","))))throw Error("source not Tcore");
  for(const g of owners){
    if(g.id<10||g.id>28||Math.abs(g.a)===Math.abs(g.b)||
       Math.abs(g.a)>=g.id||Math.abs(g.b)>=g.id)throw Error("invalid DEF");
  }
  let accepts=0;
  for(let mask=0;mask<512;mask++){
    let v={};for(let i=1;i<=9;i++)v[i]=!!(mask&(1<<(i-1)));
    let lit=x=>x>0?v[x]:!v[-x],holds=c=>c.some(lit);
    for(const g of owners)v[g.id]=lit(g.a)&&lit(g.b);
    if(q.source.every(holds)){
      accepts++;if(!q.targets.every(t=>holds(t.clause)))throw Error("false goal");
    }
  }
  if(accepts!==9)throw Error("source model count");
  return {status:"PASS",original_source_valuations:512,satisfying_original_source:accepts,
     corrupted_source_rejection:"checked by exact Tcore source matching",records:n.length,
     logical_work:q.counts.paid,resolution_only_depth:Math.max(...depth)};
}
if(typeof module!=="undefined"&&require.main===module){
  const fs=require("fs"),vm=require("vm"),dep="experiments/arc/lspv1_524_strict3_inverse_cancellation.js";
  const P=vm.runInNewContext(fs.readFileSync(dep,"utf8")+";\nmain()");
  const q=lift(P);const r=replay(q);
  console.log(JSON.stringify({summary:r,certificate:q},null,2));
}