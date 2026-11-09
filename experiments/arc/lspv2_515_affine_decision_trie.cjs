"use strict";
// Independent Javascript/V8 implementation of LSPV-2/515 restricted test.
function bitcount(v){let n=0;for(;v;v&=v-1)n++;return n}
function build(){
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],charge=[1,0,0,0],cl=[];
 for(let vertex=0;vertex<4;vertex++){
  const ids=edges.map((e,i)=>e.includes(vertex)?i+1:null).filter(x=>x!==null);
  for(let a=0;a<2;a++)for(let b=0;b<2;b++){
    const z=(1^charge[vertex]^a^b);
    cl.push(ids.map((id,j)=>[a,b,z][j]?-id:id));
  }
 }
 for(let j=0;j<7;j++){const v=7+3*j;cl.push([v,v+1,v+2])}
 const bits=[..."10100101",..."00010111"],core=[],tags=[];
 for(let ci=0;ci<cl.length;ci++)for(let li=0;li<3;li++){
  let v=Math.abs(cl[ci][li]);
  bits.push(...v.toString(2).padStart(5,"0"));
  let pos=bits.length;
  bits.push(cl[ci][li]<0?"1":"0");
  if(ci<4&&li===2)core.push(pos);
  if(ci>=16&&li===0)tags.push(pos);
 }
 bits.push("0","1");
 const parent=bits.join(""),masks=new Array(parent.length).fill(0);
 core.forEach(p=>masks[p]=1);
 tags.forEach((p,j)=>masks[p]=1<<(j+1));
 if(parent.length!==432||cl.length!==23||core.length!==4||tags.length!==7)throw Error("source construction");
 return {parent,masks,core,tags,clauses:cl};
}
const F=build();
function valueAt(pos,d){return (+F.parent[pos])^(bitcount(F.masks[pos]&d)&1)}
function child(d){return [...F.parent].map((_,i)=>String(valueAt(i,d))).join("")}
function decode(packet){
 if(packet.length!==432||packet.slice(0,8)!=="10100101"||parseInt(packet.slice(8,16),2)!==23||packet.slice(-2)!=="01")return null;
 let out=[],off=16;
 for(let i=0;i<23;i++){let c=[];
  for(let j=0;j<3;j++){const v=parseInt(packet.slice(off,off+5),2),sgn=packet[off+5];off+=6;if(!v||v>31)return null;c.push(sgn==="1"?-v:v)}
  if(new Set(c.map(Math.abs)).size!==3)return null;
  out.push(c);
 }
 return off===430?out:null;
}
function authentic(packet){
 const clauses=decode(packet); if(!clauses)return false;
 const offset=(+packet[F.core[0]])^(+F.parent[F.core[0]]);
 for(let p of F.core){if(((+packet[p])^(+F.parent[p]))!==offset)return false}
 const change=new Set([...F.core,...F.tags]);
 for(let p=0;p<packet.length;p++)if(!change.has(p)&&packet[p]!==F.parent[p])return false;
 return true;
}
function truth(d){
 const clauses=decode(child(d));
 if(!clauses)throw Error("invalid child");
 for(let bits=0;bits<64;bits++){
  if(clauses.slice(0,16).every(c=>c.some(l=>Boolean(bits&(1<<(Math.abs(l)-1)))===(l>0))))return "SAT";
 }
 return "UNSAT";
}
function insert(base,row){
 let b={...base},x=row;
 while(x){let p=31-Math.clz32(x);if(b[p]===undefined){b[p]=x;return [b,true]}x^=b[p]}
 return [base,false];
}
class Guest{
 constructor(rank,adaptive){this.rank=rank;this.adaptive=adaptive;this.calls=0;this.reads=0}
 run(d){this.calls++;let used=new Set(),state=0,ev=[];
  for(let j=0;j<this.rank;j++){
   const rest=[0,1,2,3,4,5,6,7].filter(x=>!used.has(x));
   const idx=j===0?0:this.adaptive&&(state&1)?rest[rest.length-1]:rest[0];
   used.add(idx);
   const pos=idx===0?F.core[0]:F.tags[idx-1],val=valueAt(pos,d);
   ev.push([pos,val]);state=((state<<1)|val)&255;
  }
  this.reads+=ev.length;const label=(d&1)?"SAT":"UNSAT";
  return [label,ev];
 }
}
class LinearCache{
 constructor(guest){this.guest=guest;this.anchors=[];this.tests=0}
 query(d){
  for(const [label,events] of this.anchors){
   let valid=true;for(const [pos,v] of events){this.tests++;if(valueAt(pos,d)!==v){valid=false;break}}
   if(valid)return label;
  }
  const [label,ev]=this.guest.run(d);this.anchors.push([label,ev]);return label;
 }
}
class DecisionTrie{
 constructor(guest){this.guest=guest;this.root={kind:"unknown"};this.tests=0;this.rankChecks=0;this.nodes=0;this.maxDepth=0}
 query(d){
  let node=this.root,base={},depth=0;
  while(node.kind==="test"){
   const pos=node.pos;
   this.tests++;let [next,ind]=insert(base,F.masks[pos]);
   if(!ind)throw Error("dependent test");base=next;depth++;
   node=node.children[valueAt(pos,d)];
  }
  this.maxDepth=Math.max(this.maxDepth,depth);
  if(node.kind==="known")return node.label;
  const [label,events]=this.guest.run(d);
  for(const [pos,val] of events){
   this.rankChecks++;
   let [next,ind]=insert(base,F.masks[pos]);if(!ind)continue;
   if(depth>=this.guest.rank)throw Error("rank cap");
   const sub={kind:"unknown"};
   node.kind="test";node.pos=pos;
   node.children=[{kind:"unknown"},{kind:"unknown"}];
   node.children[val]=sub;
   delete node.label;
   this.nodes++;node=sub;base=next;depth++;
  }
  node.kind="known";node.label=label;
  this.maxDepth=Math.max(this.maxDepth,depth);
  return label;
 }
}
function main(){
 let assertions=0,positive=0,negative=0,malformed=0,result=[];
 for(let d=0;d<256;d++){
  const p=child(d),lab=truth(d);
  if(!authentic(p)||lab!==((d&1)?"SAT":"UNSAT"))throw Error("source/label mismatch "+d);
  assertions+=2;if(lab==="SAT")positive++;else negative++;
 }
 for(const p of [0,8,431,F.core[1],16,F.tags[0]-1]){
  let v=[...F.parent];v[p]=v[p]==="0"?"1":"0";
  if(authentic(v.join("")))throw Error("malformed accepted at "+p);
  assertions++;malformed++;
 }
 for(const adaptive of [false,true])for(let rank=1;rank<=8;rank++)
  for(const order of ["ascending","descending"]){
   const a=new Guest(rank,adaptive),b=new Guest(rank,adaptive);
   const linear=new LinearCache(a),trie=new DecisionTrie(b);
   for(let j=0;j<256;j++){
    const d=order==="ascending"?j:255-j;
    const t1=linear.query(d),t2=trie.query(d);
    if(t1!==t2||t1!==((d&1)?"SAT":"UNSAT"))throw Error("bad cache classification");
    assertions++;
   }
   if(a.calls!==(1<<rank)||b.calls!==(1<<rank)||trie.nodes!==(1<<rank)-1||trie.maxDepth!==rank||trie.tests>256*rank)throw Error("bad count");
   assertions+=5;
   result.push({adaptive,rank,order,guest_calls:a.calls,scan_tests:linear.tests,trie_tests:trie.tests,trie_nodes:trie.nodes,rank_checks:trie.rankChecks});
  }
 return {status:"PASS",assertions,sat:positive,unsat:negative,malformed_rejected:malformed,source_bits:F.parent.length,source_SHA256_from_independent_python:"f22c2223cb73262db1ee75a4741bfe9f3643933aaa7154021ea107dc4b892387",results:result};
}
console.log(JSON.stringify(main(),null,2));
