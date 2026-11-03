"use strict";
/* LSPV-2 PORT-INPUT-RES356. Independent proof-stream verifier is separate. */
function canon(xs){return [...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function flip(x,b){return x<0?!b:b;}
function makeCircuit(k,gates,offset){
  const out=[];
  function wire(l){const v=Math.abs(l);const id=v<=k?v+0:offset+(v-k);return l<0?-id:id;}
  for(let i=0;i<gates.length;i++){
    let g=gates[i],u=wire(g.a),v=wire(g.b),z=offset+i+1;
    if(!["A","X"].includes(g.op)||Math.abs(g.a)===Math.abs(g.b)||!g.a||!g.b||Math.abs(g.a)>k+i||Math.abs(g.b)>k+i)throw Error("malformed gate");
    let ids=[Math.abs(u),Math.abs(v),z],s=[];
    for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let q=0;q<2;q++){
       const expected=g.op==="A"?(flip(u,x)&&flip(v,y)?1:0):(Number(flip(u,x))^Number(flip(v,y)));
       if(q!==expected)s.push(canon([x?-ids[0]:ids[0],y?-ids[1]:ids[1],q?-z:z]));
    }
    out.push(...s);
  }
  return {clauses:out,output:offset+gates.length};
}
function sourceOf(t){
  let {k,A,B}=t;if(!Number.isInteger(k)||k<2||!Array.isArray(A)||!Array.isArray(B)||!A.length||!B.length)throw Error("malformed circuit");
  let aa=makeCircuit(k,A,k),bb=makeCircuit(k,B,k+A.length);
  return {clauses:[...aa.clauses,...bb.clauses,[aa.output],[-bb.output]],n:k+A.length+B.length,s:A.length+B.length};
}
function resolve(P,Q,v){
 const p=P.find(x=>Math.abs(x)===v),q=Q.find(x=>Math.abs(x)===v);
 if(!p||!q||p!==-q)throw Error("bad pivot "+v);
 const R=canon([...P.filter(x=>Math.abs(x)!==v),...Q.filter(x=>Math.abs(x)!==v)]);
 if(R.some(x=>R.includes(-x)))throw Error("tautological resolvent");
 return R;
}
function produce(test){
 const {clauses,n,s}=sourceOf(test),k=test.k,lines=clauses.map(c=>({c,p:null})),nSource=lines.length;
 let analysisNodes=0,mergeNodes=0,leaves=0,satWitness=null,propagations=0;
 function add(p,q,v){let c=resolve(lines[p].c,lines[q].c,v);let id=lines.length;lines.push({c,p:[p,q],v});return id;}
 function leaf(alpha){
  leaves++;
  let val=Array(n+1).fill(-1),why=Array(n+1).fill(-1),when=Array(n+1).fill(-1),timer=0;
  for(let j=1;j<=k;j++){val[j]=alpha[j];when[j]=timer++;}
  let bad=-1,progress=true;
  while(progress&&bad<0){
   progress=false;
   for(let id=0;id<clauses.length;id++){
     let c=clauses[id],un=0,lit=0,satisfied=false;
     for(const l of c){
       let b=val[Math.abs(l)];
       if(b===-1){un++;lit=l;}
       else if((l>0&&b===1)||(l<0&&b===0)){satisfied=true;break;}
     }
     if(satisfied)continue;
     if(un===0){bad=id;break;}
     if(un===1){
       const j=Math.abs(lit),b=lit>0?1:0;
       if(val[j]!==-1&&val[j]!==b){bad=id;break;}
       if(val[j]===-1){val[j]=b;why[j]=id;when[j]=timer++;propagations++;progress=true;}
     }
   }
  }
  if(bad<0){satWitness=val.slice(1);return null;}
  let id=bad;
  for(let iter=0;iter<=s+2;iter++){
    let candidates=lines[id].c.map(l=>Math.abs(l)).filter(j=>why[j]>=0);
    if(!candidates.length)break;
    let v=candidates.reduce((x,y)=>when[x]>when[y]?x:y);
    id=add(id,why[v],v);analysisNodes++;
  }
  if(lines[id].c.some(l=>Math.abs(l)>k))throw Error("nondecision survived");
  if(lines[id].c.some(l=>l>0?alpha[l]!==0:alpha[-l]!==1))throw Error("leaf clause not falsified");
  return id;
 }
 function tree(depth,alpha){
    if(depth>k)return leaf(alpha);
    alpha[depth]=0;const a=tree(depth+1,alpha);if(a===null)return null;
    alpha[depth]=1;const b=tree(depth+1,alpha);if(b===null)return null;
    const ca=lines[a].c,cb=lines[b].c,hasA=ca.includes(depth),hasB=cb.includes(-depth);
    if(!hasA)return a;
    if(!hasB)return b;
    mergeNodes++;return add(a,b,depth);
 }
 const root=tree(1,Array(k+1).fill(0));if(root!==null && lines[root].c.length)throw Error("nonempty root");
 return {test,source:clauses,lines:root===null?[]:lines.slice(nSource),root:root===null?null:root,metrics:{sourceClauses:nSource,variables:n,gateOutputs:s,derived:lines.length-nSource,analysisNodes,mergeNodes,leaves,propagations,bound:(s+1)*2**k-1},satWitness};
}
const cases=[
 {name:"distributivity3",k:3,A:[{op:"X",a:2,b:3},{op:"A",a:1,b:4}],B:[{op:"A",a:1,b:2},{op:"A",a:1,b:3},{op:"X",a:4,b:5}]},
 {name:"signed_distributivity3",k:3,A:[{op:"X",a:2,b:3},{op:"A",a:-1,b:4}],B:[{op:"A",a:-1,b:2},{op:"A",a:-1,b:3},{op:"X",a:4,b:5}]},
 {name:"xor_absorption2",k:2,A:[{op:"X",a:1,b:2},{op:"A",a:1,b:3}],B:[{op:"A",a:1,b:-2}]},
 {name:"distributivity4",k:4,A:[{op:"X",a:3,b:4},{op:"X",a:2,b:5},{op:"A",a:1,b:6}],B:[{op:"A",a:1,b:2},{op:"A",a:1,b:3},{op:"A",a:1,b:4},{op:"X",a:5,b:6},{op:"X",a:7,b:8}]},
 {name:"xor_tree4",k:4,A:[{op:"X",a:1,b:2},{op:"X",a:5,b:3},{op:"X",a:6,b:4}],B:[{op:"X",a:3,b:4},{op:"X",a:2,b:5},{op:"X",a:1,b:6}]},
 {name:"SAT_neighbor",k:3,A:[{op:"X",a:2,b:3},{op:"A",a:1,b:4}],B:[{op:"A",a:1,b:2},{op:"A",a:1,b:3},{op:"A",a:4,b:5}]}
];
function evaluate(c,alpha){let vals=[null,...alpha];for(const g of c){const a=flip(g.a,vals[Math.abs(g.a)]),b=flip(g.b,vals[Math.abs(g.b)]);vals.push(g.op==="A"?Number(a&&b):(Number(a)^Number(b)));}return vals[vals.length-1];}
const data=[];
for(const t of cases){const truth=[];for(let i=0;i<2**t.k;i++){let as=Array.from({length:t.k},(_,j)=>(i>>j)&1);truth.push({as,A:evaluate(t.A,as),B:evaluate(t.B,as)});}let p=produce(t);let equivalent=truth.every(x=>x.A===x.B);if(equivalent!==(p.root!==null))throw Error("label mismatch "+t.name);if(p.metrics.derived>p.metrics.bound)throw Error("cost bound");data.push({...p,equivalent,truth});}
for(let bad of [{k:0,A:[],B:[]},{k:3,A:[{op:"A",a:1,b:1}],B:[{op:"A",a:1,b:2}]},{k:2,A:[{op:"Z",a:1,b:2}],B:[{op:"A",a:1,b:2}]},{k:2,A:[{op:"A",a:1,b:5}],B:[{op:"A",a:1,b:2}]}]){let rejected=false;try{produce(bad)}catch{rejected=true}if(!rejected)throw Error("malformed accepted");}
return {claim:"PORT-INPUT-RES356",date:"2026-11-03",cases:data,malformedRejected:4};

const data=new Function("\"use strict\";\n/* LSPV-2 PORT-INPUT-RES356. Independent proof-stream verifier is separate. */\nfunction canon(xs){return [...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}\nfunction flip(x,b){return x<0?!b:b;}\nfunction makeCircuit(k,gates,offset){\n  const out=[];\n  function wire(l){const v=Math.abs(l);const id=v<=k?v+0:offset+(v-k);return l<0?-id:id;}\n  for(let i=0;i<gates.length;i++){\n    let g=gates[i],u=wire(g.a),v=wire(g.b),z=offset+i+1;\n    if(![\"A\",\"X\"].includes(g.op)||Math.abs(g.a)===Math.abs(g.b)||!g.a||!g.b||Math.abs(g.a)>k+i||Math.abs(g.b)>k+i)throw Error(\"malformed gate\");\n    let ids=[Math.abs(u),Math.abs(v),z],s=[];\n    for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let q=0;q<2;q++){\n       const expected=g.op===\"A\"?(flip(u,x)&&flip(v,y)?1:0):(Number(flip(u,x))^Number(flip(v,y)));\n       if(q!==expected)s.push(canon([x?-ids[0]:ids[0],y?-ids[1]:ids[1],q?-z:z]));\n    }\n    out.push(...s);\n  }\n  return {clauses:out,output:offset+gates.length};\n}\nfunction sourceOf(t){\n  let {k,A,B}=t;if(!Number.isInteger(k)||k<2||!Array.isArray(A)||!Array.isArray(B)||!A.length||!B.length)throw Error(\"malformed circuit\");\n  let aa=makeCircuit(k,A,k),bb=makeCircuit(k,B,k+A.length);\n  return {clauses:[...aa.clauses,...bb.clauses,[aa.output],[-bb.output]],n:k+A.length+B.length,s:A.length+B.length};\n}\nfunction resolve(P,Q,v){\n const p=P.find(x=>Math.abs(x)===v),q=Q.find(x=>Math.abs(x)===v);\n if(!p||!q||p!==-q)throw Error(\"bad pivot \"+v);\n const R=canon([...P.filter(x=>Math.abs(x)!==v),...Q.filter(x=>Math.abs(x)!==v)]);\n if(R.some(x=>R.includes(-x)))throw Error(\"tautological resolvent\");\n return R;\n}\nfunction produce(test){\n const {clauses,n,s}=sourceOf(test),k=test.k,lines=clauses.map(c=>({c,p:null})),nSource=lines.length;\n let analysisNodes=0,mergeNodes=0,leaves=0,satWitness=null,propagations=0;\n function add(p,q,v){let c=resolve(lines[p].c,lines[q].c,v);let id=lines.length;lines.push({c,p:[p,q],v});return id;}\n function leaf(alpha){\n  leaves++;\n  let val=Array(n+1).fill(-1),why=Array(n+1).fill(-1),when=Array(n+1).fill(-1),timer=0;\n  for(let j=1;j<=k;j++){val[j]=alpha[j];when[j]=timer++;}\n  let bad=-1,progress=true;\n  while(progress&&bad<0){\n   progress=false;\n   for(let id=0;id<clauses.length;id++){\n     let c=clauses[id],un=0,lit=0,satisfied=false;\n     for(const l of c){\n       let b=val[Math.abs(l)];\n       if(b===-1){un++;lit=l;}\n       else if((l>0&&b===1)||(l<0&&b===0)){satisfied=true;break;}\n     }\n     if(satisfied)continue;\n     if(un===0){bad=id;break;}\n     if(un===1){\n       const j=Math.abs(lit),b=lit>0?1:0;\n       if(val[j]!==-1&&val[j]!==b){bad=id;break;}\n       if(val[j]===-1){val[j]=b;why[j]=id;when[j]=timer++;propagations++;progress=true;}\n     }\n   }\n  }\n  if(bad<0){satWitness=val.slice(1);return null;}\n  let id=bad;\n  for(let iter=0;iter<=s+2;iter++){\n    let candidates=lines[id].c.map(l=>Math.abs(l)).filter(j=>why[j]>=0);\n    if(!candidates.length)break;\n    let v=candidates.reduce((x,y)=>when[x]>when[y]?x:y);\n    id=add(id,why[v],v);analysisNodes++;\n  }\n  if(lines[id].c.some(l=>Math.abs(l)>k))throw Error(\"nondecision survived\");\n  if(lines[id].c.some(l=>l>0?alpha[l]!==0:alpha[-l]!==1))throw Error(\"leaf clause not falsified\");\n  return id;\n }\n function tree(depth,alpha){\n    if(depth>k)return leaf(alpha);\n    alpha[depth]=0;const a=tree(depth+1,alpha);if(a===null)return null;\n    alpha[depth]=1;const b=tree(depth+1,alpha);if(b===null)return null;\n    const ca=lines[a].c,cb=lines[b].c,hasA=ca.includes(depth),hasB=cb.includes(-depth);\n    if(!hasA)return a;\n    if(!hasB)return b;\n    mergeNodes++;return add(a,b,depth);\n }\n const root=tree(1,Array(k+1).fill(0));if(root!==null && lines[root].c.length)throw Error(\"nonempty root\");\n return {test,source:clauses,lines:root===null?[]:lines.slice(nSource),root:root===null?null:root,metrics:{sourceClauses:nSource,variables:n,gateOutputs:s,derived:lines.length-nSource,analysisNodes,mergeNodes,leaves,propagations,bound:(s+1)*2**k-1},satWitness};\n}\nconst cases=[\n {name:\"distributivity3\",k:3,A:[{op:\"X\",a:2,b:3},{op:\"A\",a:1,b:4}],B:[{op:\"A\",a:1,b:2},{op:\"A\",a:1,b:3},{op:\"X\",a:4,b:5}]},\n {name:\"signed_distributivity3\",k:3,A:[{op:\"X\",a:2,b:3},{op:\"A\",a:-1,b:4}],B:[{op:\"A\",a:-1,b:2},{op:\"A\",a:-1,b:3},{op:\"X\",a:4,b:5}]},\n {name:\"xor_absorption2\",k:2,A:[{op:\"X\",a:1,b:2},{op:\"A\",a:1,b:3}],B:[{op:\"A\",a:1,b:-2}]},\n {name:\"distributivity4\",k:4,A:[{op:\"X\",a:3,b:4},{op:\"X\",a:2,b:5},{op:\"A\",a:1,b:6}],B:[{op:\"A\",a:1,b:2},{op:\"A\",a:1,b:3},{op:\"A\",a:1,b:4},{op:\"X\",a:5,b:6},{op:\"X\",a:7,b:8}]},\n {name:\"xor_tree4\",k:4,A:[{op:\"X\",a:1,b:2},{op:\"X\",a:5,b:3},{op:\"X\",a:6,b:4}],B:[{op:\"X\",a:3,b:4},{op:\"X\",a:2,b:5},{op:\"X\",a:1,b:6}]},\n {name:\"SAT_neighbor\",k:3,A:[{op:\"X\",a:2,b:3},{op:\"A\",a:1,b:4}],B:[{op:\"A\",a:1,b:2},{op:\"A\",a:1,b:3},{op:\"A\",a:4,b:5}]}\n];\nfunction evaluate(c,alpha){let vals=[null,...alpha];for(const g of c){const a=flip(g.a,vals[Math.abs(g.a)]),b=flip(g.b,vals[Math.abs(g.b)]);vals.push(g.op===\"A\"?Number(a&&b):(Number(a)^Number(b)));}return vals[vals.length-1];}\nconst data=[];\nfor(const t of cases){const truth=[];for(let i=0;i<2**t.k;i++){let as=Array.from({length:t.k},(_,j)=>(i>>j)&1);truth.push({as,A:evaluate(t.A,as),B:evaluate(t.B,as)});}let p=produce(t);let equivalent=truth.every(x=>x.A===x.B);if(equivalent!==(p.root!==null))throw Error(\"label mismatch \"+t.name);if(p.metrics.derived>p.metrics.bound)throw Error(\"cost bound\");data.push({...p,equivalent,truth});}\nfor(let bad of [{k:0,A:[],B:[]},{k:3,A:[{op:\"A\",a:1,b:1}],B:[{op:\"A\",a:1,b:2}]},{k:2,A:[{op:\"Z\",a:1,b:2}],B:[{op:\"A\",a:1,b:2}]},{k:2,A:[{op:\"A\",a:1,b:5}],B:[{op:\"A\",a:1,b:2}]}]){let rejected=false;try{produce(bad)}catch{rejected=true}if(!rejected)throw Error(\"malformed accepted\");}\nreturn {claim:\"PORT-INPUT-RES356\",date:\"2026-11-03\",cases:data,malformedRejected:4};\n")();
if(typeof console!=='undefined')console.log(JSON.stringify(data,null,2));
