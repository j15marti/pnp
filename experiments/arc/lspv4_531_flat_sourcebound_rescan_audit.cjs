// LSPV-4/531: read-only source-bound typed proof-DAG resource audit.
// This is a separate canonical SOURCE/AND3/XOR format, NOT the missing historical
// R_mix341 accepted-byte grammar. The JS test stores inputs in host memory.
"use strict";
function assert(x,msg){if(!x)throw Error(msg)}
function graph(name,k=0){
 if(name==="K4"){let e=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)e.push([i,j]);return {name,V:4,edges:e}}
 let E=[];for(let i=0;i<k;i++)E.push([i,(i+1)%k],[i+k,(i+1)%k+k],[i,i+k]);
 return {name,V:2*k,edges:E};
}
function clauseTable(C,S){
 let out=0;for(let a=0;a<(1<<S.length);a++)if(C.some(l=>((a>>S.indexOf(Math.abs(l)-1))&1)===(l>0?1:0)))out|=1<<a;
 return out
}
function source(G,odd){
 const E=G.edges.length,incident=Array.from({length:G.V},()=>[]),clauses=[];
 G.edges.forEach(([u,v],i)=>{incident[u].push(i);incident[v].push(i)});
 for(let v=0;v<G.V;v++)for(let z=0;z<8;z++){
  const p=(z&1)^((z>>1)&1)^((z>>2)&1);
  if(p===(odd&&v===0?1:0))continue;
  clauses.push(incident[v].map((e,j)=>(z>>j)&1?-(e+1):e+1))
 }
 return {E,incident,clauses,text:"p cnf "+E+" "+clauses.length+"\n"+clauses.map(c=>c.join(" ")+" 0\n").join("")};
}
function generate(G,k){
 const F=source(G,true),E=F.E,m=F.clauses.length,all=[],lines=[],depth=Array(m).fill(0),heads=[];
 for(let j=0;j<m;j++){
  const sup=F.clauses[j].map(l=>Math.abs(l)-1).sort((a,b)=>a-b);
  all.push({sup,table:clauseTable(F.clauses[j],sup),row:null})
 }
 function add(kind,p,q,sup,table,mask,rhs){
  const id=all.length;
  assert(p!==q&&p<id&&q<id,"DAG");
  depth.push(1+Math.max(depth[p],depth[q]));
  lines.push([kind,id,p,q,sup?sup.join(","):"-",table===null?"-":table,mask===null?"-":mask,rhs===null?"-":rhs].join(" "));
  all.push({sup,table,row:mask===null?null:{mask,rhs}});
  return id
 }
 function evalNode(n,union,assignment){
  let i=0;for(let j=0;j<n.sup.length;j++)i|=((assignment>>union.indexOf(n.sup[j]))&1)<<j;
  return n.table>>i&1
 }
 const maskFor=S=>Array.from({length:E},(_,i)=>S.includes(i)?"1":"0").join("");
 for(let v=0;v<G.V;v++){
  let s=v*4,cur=s,sup=F.incident[v].slice().sort((a,b)=>a-b);
  for(let i=1;i<4;i++){
   let table=0;
   for(let a=0;a<8;a++)if(evalNode(all[cur],sup,a)&&evalNode(all[s+i],sup,a))table|=1<<a;
   cur=add("A",cur,s+i,sup,table,i===3?maskFor(sup):null,i===3?(v===0?1:0):null);
  }
  heads.push(cur);
 }
 function xor(p,q){
  const A=all[p].row,B=all[q].row;
  assert(A&&B,"nonaffine parent");
  let mask="";for(let j=0;j<E;j++)mask+=(Number(A.mask[j])^Number(B.mask[j]));
  return add("X",p,q,null,null,mask,A.rhs^B.rhs)
 }
 const a=xor(heads[0],heads[1]);let z=a;
 for(let i=2;i<heads.length;i++)z=xor(z,heads[i]);
 for(let i=0;i<k;i++){let u=xor(z,a);z=xor(u,a)}
 assert(all[z].row.mask==="0".repeat(E)&&all[z].row.rhs===1,"goal");
 return {G,F,k,proof:lines.join("\n")+"\n",span:Math.max(...depth)};
}
function parseSource(s){
 const t=s.trim().split(/\s+/);
 assert(t[0]==="p"&&t[1]==="cnf","DIMACS header");
 const E=+t[2],m=+t[3],clauses=[];let row=[];
 assert(Number.isSafeInteger(E)&&E>0&&Number.isSafeInteger(m)&&m>0,"source dimensions");
 for(let j=4;j<t.length;j++){
  assert(/^(?:0|-?[1-9][0-9]*)$/.test(t[j]),"source literal grammar");
  const v=Number(t[j]);assert(Number.isSafeInteger(v)&&Math.abs(v)<=E,"source literal bounds");
  if(v===0){assert(row.length===3&&new Set(row.map(Math.abs)).size===3,"strict3");clauses.push(row);row=[]}
  else {assert(row.length<3,"width");row.push(v)}
 }
 assert(!row.length&&clauses.length===m,"source count");
 return {E,m,clauses}
}
function readLine(s,index){
 let start=0,count=0;
 for(let j=0;j<s.length;j++)if(s[j]==="\n"){
  if(count===index)return s.slice(start,j);
  count++;start=j+1
 }
 throw Error("record absent")
}
function readRec(s,index,E,m){
 const f=readLine(s,index).split(" ");
 assert(f.length===8,"field count");
 const [rule,rawId,rawP,rawQ,rawSup,rawTable,mask,rawRhs]=f;
 assert(rule==="A"||rule==="X","rule");
 assert([rawId,rawP,rawQ].every(x=>/^(?:0|[1-9]\d*)$/.test(x)),"decimal ids");
 const id=+rawId,p=+rawP,q=+rawQ;
 assert(Number.isSafeInteger(id)&&id===m+index&&Number.isSafeInteger(p)&&Number.isSafeInteger(q)&&p!==q&&p>=0&&q>=0&&p<id&&q<id,"topological ids");
 let sup=null,table=null;
 if(rule==="A"){
  assert(/^\d+(,\d+){0,2}$/.test(rawSup),"factor support");
  sup=rawSup.split(",").map(Number);
  assert(sup.every((x,i)=>x<E&&(i===0||x>sup[i-1])),"support sorted/in bounds");
  table=+rawTable;assert(Number.isInteger(table)&&table>=0&&table<256,"table byte");
  assert((mask==="-"&&rawRhs==="-")||(/^[01]+$/.test(mask)&&mask.length===E&&/^[01]$/.test(rawRhs)),"A alias");
 } else {
  assert(rawSup==="-"&&rawTable==="-"&&/^[01]+$/.test(mask)&&mask.length===E&&/^[01]$/.test(rawRhs),"XOR fields")
 }
 return {rule,id,p,q,sup,table,mask,rhs:rawRhs==="-"?null:+rawRhs}
}
function verify(F,P){
 const {E,m,clauses}=parseSource(F),count=P.trimEnd().split("\n").length;
 assert(count>0&&P.endsWith("\n"),"empty/missing newline");
 let parent_reads=0,bit_checks=0;
 function get(id){
  parent_reads++;
  if(id>=m)return readRec(P,id-m,E,m);
  const sup=clauses[id].map(l=>Math.abs(l)-1).sort((a,b)=>a-b);
  return {rule:"S",id,sup,table:clauseTable(clauses[id],sup),mask:"-",rhs:null}
 }
 for(let i=0;i<count;i++){
  const d=readRec(P,i,E,m),a=get(d.p),b=get(d.q);
  if(d.rule==="A"){
   assert(a.sup&&b.sup,"AND3 factors");
   const u=[...new Set([...a.sup,...b.sup])].sort((x,y)=>x-y);
   assert(u.length<=3&&u.join(",")===d.sup.join(","),"AND3 union");
   let table=0;
   function evalAt(n,x){let j=0;for(let r=0;r<n.sup.length;r++)j|=((x>>u.indexOf(n.sup[r]))&1)<<r;return n.table>>j&1}
   for(let x=0;x<(1<<u.length);x++)if(evalAt(a,x)&&evalAt(b,x))table|=1<<x;
   assert(d.table===table,"AND3 truth table");
   if(d.mask!=="-"){
    for(let x=0;x<E;x++){assert(d.mask[x]===(u.includes(x)?"1":"0"),"alias support");bit_checks++}
    for(let x=0;x<(1<<u.length);x++){
     let val=0;for(let j=0;j<u.length;j++)val^=(x>>j)&1;
     assert(((d.table>>x)&1)===(val===d.rhs?1:0),"alias equivalence");
    }
   }
  }else{
   assert(a.mask!=="-"&&b.mask!=="-","GF2 parents");
   for(let j=0;j<E;j++){assert(Number(d.mask[j])===(Number(a.mask[j])^Number(b.mask[j])),"GF2 row");bit_checks++}
   assert(d.rhs===(a.rhs^b.rhs),"GF2 rhs")
  }
 }
 const last=readRec(P,count-1,E,m);
 assert(last.mask==="0".repeat(E)&&last.rhs===1,"sink");
 return {paid:count,source_bytes:F.length,proof_bytes:P.length,source_clauses:m,parent_reads,bit_checks};
}
function run(){
 const data=[],rejects=[];
 function negative(label,F,P){let rejected=false;try{verify(F,P)}catch(e){rejected=true}assert(rejected,"hostile packet accepted: "+label);rejects.push(label)}
 for(const G of [graph("K4"),graph("PRISM6",6),graph("PRISM16",16)])
 for(const k of G.V===4?[0,1,2,4,8,16]:[0,1]){
  const x=generate(G,k),a=verify(x.F.text,x.proof);
  assert(a.paid===4*G.V-1+2*k,"count");
  data.push({graph:G.name,k,variables:x.F.E,source_clauses:a.source_clauses,paid:a.paid,refs:a.parent_reads,span:x.span,source_bytes:a.source_bytes,proof_bytes:a.proof_bytes,bit_checks:a.bit_checks});
  const lines=x.proof.trimEnd().split("\n");
  const change=(idx,fn)=>lines.map((l,j)=>j===idx?fn(l):l).join("\n")+"\n";
  negative("wrong-rule "+G.name+" k"+k,x.F.text,change(0,l=>l.replace(/^A /,"X ")));
  negative("wrong-goal-mask "+G.name+" k"+k,x.F.text,change(lines.length-1,l=>{const t=l.split(" ");t[6]="1"+t[6].slice(1);return t.join(" ")}));
  negative("forward-ref "+G.name+" k"+k,x.F.text,change(0,l=>{const t=l.split(" ");t[2]=t[1];return t.join(" ")}));
  negative("duplicate-parent "+G.name+" k"+k,x.F.text,change(0,l=>{const t=l.split(" ");t[3]=t[2];return t.join(" ")}));
  negative("even-charge-source "+G.name+" k"+k,source(G,false).text,x.proof);
  if(k===0)negative("omitted-sink "+G.name,x.F.text,lines.slice(0,-1).join("\n")+"\n");
 }
 return {name:"LSPV-4/531",status:"PROVED/RESTRICTED theoretical bound; COMPUTATIONAL independently generated finite controls",scope:"separate canonical source-bound line encoding, not historical R_mix341 parser",execution:"V8 JavaScript, not native indexed-machine hardware",cases:data,hostile_rejections:rejects.length,verified:true};
}
if(typeof process!=="undefined"&&process.versions?.node)console.log(JSON.stringify(run(),null,2));
