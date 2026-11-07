"use strict";
/* LSPV-4/466 independent finite semantics for dual-arena virtual input index.
   ABSTRACT deterministic AVL sets, not an execution on native FLMV.
   Original-source strict 3-CNF even/odd K4 controls included.
   The proved accounting is for a defined indexed dictionary model;
   complete same-machine interpreter and arbitrary-source contraction are OPEN. */
const assert=(x,m)=>{if(!x)throw Error(m||"assertion"); tests++};
let tests=0;
class Node { constructor(k){this.k=k;this.l=null;this.r=null;this.h=1;} }
class AVL {
 constructor(){this.root=null;this.n=0}
 height(x){return x?x.h:0}
 update(x){x.h=1+Math.max(this.height(x.l),this.height(x.r));return x}
 left(x){let y=x.r;x.r=y.l;y.l=x;this.update(x);return this.update(y)}
 right(x){let y=x.l;x.l=y.r;y.r=x;this.update(x);return this.update(y)}
 balance(x){this.update(x);let b=this.height(x.l)-this.height(x.r);
   if(b>1){if(this.height(x.l.l)<this.height(x.l.r))x.l=this.left(x.l);return this.right(x)}
   if(b< -1){if(this.height(x.r.r)<this.height(x.r.l))x.r=this.right(x.r);return this.left(x)}
   return x}
 has(k){let x=this.root;while(x){if(k===x.k)return true;x=k<x.k?x.l:x.r}return false}
 _ins(x,k){if(!x)return new Node(k);if(k<x.k)x.l=this._ins(x.l,k);else if(k>x.k)x.r=this._ins(x.r,k);return this.balance(x)}
 _del(x,k){if(!x)return null;
   if(k<x.k)x.l=this._del(x.l,k);else if(k>x.k)x.r=this._del(x.r,k);
   else {if(!x.l)return x.r;if(!x.r)return x.l;let y=x.r;while(y.l)y=y.l;x.k=y.k;x.r=this._del(x.r,y.k)}
   return this.balance(x)}
 set(k,b){let old=this.has(k);if(old===!!b)return false;
   this.root=b?this._ins(this.root,k):this._del(this.root,k);this.n+=b?1:-1;return true}
 max(){let x=this.root;if(!x)return -1;while(x.r)x=x.r;return x.k}
 *iter(x=this.root){if(!x)return;yield* this.iter(x.l);yield x.k;yield* this.iter(x.r)}
 clearPaid(){let a=[];for(const k of this.iter())a.push(k); // explicit unique clearing schedule
   for(const k of a)assert(this.set(k,false),"delete clear failed");
   assert(this.n===0 && this.root===null,"not cleared");return a.length}
 check(){let count=0,last=-1;for(const k of this.iter()){assert(k>last,"out of order");last=k;count++}
   assert(count===this.n,"size mismatch");
   const walk=x=>{if(!x)return 0;let a=walk(x.l),b=walk(x.r);assert(Math.abs(a-b)<=1,"AVL imbalance");assert(x.h===Math.max(a,b)+1,"height");return x.h};
   walk(this.root)}
}
class Port {
 constructor(bits){this.bits=bits;this.B=bits.length;this.index=new AVL();this.base=new AVL();this.j=0;this.delta=0;this.inserts=0;this.clears=0;this.jumps=0;this.maxJ=0;this.lookups=0}
 indexMove(d){this.j=Math.max(0,this.j+d);this.maxJ=Math.max(this.j,this.maxJ)}
 indexWrite(v){let old=this.index.has(this.j);this.index.set(this.j,!!v);if(v&&!old)this.inserts++}
 jump(){let erased=this.base.clearPaid();this.clears+=erased;
   let tmp=this.base;this.base=this.index;this.index=tmp;this.delta=0;this.jumps++;
   assert(this.clears<=this.inserts,"unamortized base clearing");
   // Actual indexed-TM implementation must reposition new INDEX-area WORK head
   // to guest INDEX-head j using O(log(j+2)) index bits, counting high-water O(j).
 }
 position(){this.lookups++;
   let c=this.B+Math.abs(this.delta)+2, high=this.base.max();
   let bits=Math.floor(Math.log2(c))+1;
   if(high>=bits)return {far:true};
   let a=0n;for(const k of this.base.iter())a+=(1n<<BigInt(k));
   let p=a+BigInt(this.delta);
   return {far:false,p};
 }
 inputMove(d){if(d>0){this.delta++;return}
   let p=this.position();if(p.far || p.p>0n)this.delta--}
 read(){let p=this.position();if(p.far)return "_";
   return p.p>=0n&&p.p<BigInt(this.B)?this.bits[Number(p.p)]:"_"}
}
function k4(charges){
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],c=[];
 for(let v=0;v<4;v++){let ids=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
  for(let mask=0;mask<8;mask++){let a=[mask&1,(mask>>1)&1,(mask>>2)&1];
   if((a[0]^a[1]^a[2])===charges[v])continue;
   c.push(ids.map((id,i)=>a[i]?-id:id));}}
 return c;
}
function models(c){let n=0;for(let m=0;m<64;m++)if(c.every(row=>row.some(v=>v>0?((m>>(v-1))&1):!((m>>(-v-1))&1))))n++;return n}
function encode(c){return c.map(row=>row.map(l=>(l<0?"1":"0")+Math.abs(l).toString(2).padStart(3,"0")).join("")).join("")}
function validate(bits){if(bits.length!==192)return false;for(let z=0;z<16;z++){let seen=new Set();
   for(let p=0;p<3;p++){let id=parseInt(bits.slice(z*12+p*4+1,z*12+p*4+4),2);
     if(id<1||id>6||seen.has(id))return false;seen.add(id);}}return true}
let sat=k4([0,0,0,0]),unsat=k4([1,0,0,0]),src=encode(unsat);
assert(sat.length===16&&unsat.length===16,"K4 clause count");
assert(models(sat)===8&&models(unsat)===0,"K4 parity SAT/UNSAT");
assert(validate(src)&&validate(encode(sat)),"original-source decode");
assert(!validate(src.slice(1)),"truncated source accepted");
assert(!validate(src.slice(0,1)+"000"+src.slice(4)),"zero variable accepted");
let bits="1011001101"+src+"001101010";
let trials=0,actions=0,totalClears=0,totalInserts=0,totalJumps=0,maxIndex=0,farReads=0;
let seed=46620261107>>>0;
function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
function checkPort(p,ref){let value=p.read(),expected=ref.pos>=0n&&ref.pos<BigInt(bits.length)?bits[Number(ref.pos)]:"_";
 assert(value===expected,"virtual port mismatch");if(expected==="_")farReads++;
 assert(p.index.n===ref.I.size,"INDEX count discrepancy");
 assert(p.base.n===ref.base.size,"BASE count discrepancy");
 assert(p.maxJ>=p.j,"head high-water");}
for(let trial=0;trial<140;trial++){
 let p=new Port(bits),ref={I:new Set(),base:new Set(),j:0,pos:0n};
 const inv=()=>checkPort(p,ref);
 for(let step=0;step<220;step++){
  let kind=rnd()%9,old=ref.j;
  if(kind===0||kind===1){let d=kind===0?1:-1;p.indexMove(d);ref.j=Math.max(0,ref.j+d)}
  else if(kind===2||kind===3){let b=kind===2?1:0;p.indexWrite(b);
    if(b)ref.I.add(ref.j);else ref.I.delete(ref.j)}
  else if(kind===4){p.jump();ref.base=new Set(ref.I);ref.I.clear();
    let a=0n;for(let k of ref.base)a+=1n<<BigInt(k);ref.pos=a;}
  else if(kind===5||kind===6){let d=kind===5?1:-1;p.inputMove(d);ref.pos=d>0?ref.pos+1n:(ref.pos>0n?ref.pos-1n:0n)}
  else if(kind===7){let j=(rnd()%8===0)?(32+rnd()%220):rnd()%32;
    // Test a far sequential INDEX-head walk; the guest must pay these j moves.
    while(ref.j<j){p.indexMove(1);ref.j++}
    while(ref.j>j){p.indexMove(-1);ref.j--}}
  else {p.read()}
  actions++;inv();
  if(step%37===0){p.index.check();p.base.check()}
 }
 totalClears+=p.clears;totalInserts+=p.inserts;totalJumps+=p.jumps;maxIndex=Math.max(maxIndex,p.maxJ);trials++;
}
// Far INDEX head remains at same coordinate across many erasing jumps.
// One bit is rewritten, its old BASE requires at most one charged clear.
let q=new Port(bits);let r={I:new Set(),base:new Set(),j:0,pos:0n};
for(let i=0;i<512;i++){q.indexMove(1);r.j++;}assert(q.j===512,"distant INDEX head");
for(let i=0;i<800;i++){q.indexWrite(1);r.I.add(r.j);q.jump();r.base=new Set(r.I);r.I.clear();r.pos=1n<<512n;
 checkPort(q,r);q.inputMove(-1);r.pos--;checkPort(q,r);}
assert(q.clears===799&&q.inserts===800,"far INDEX amortization");
assert(q.base.max()===512&&q.index.n===0,"frozen far bit");
totalClears+=q.clears;totalInserts+=q.inserts;totalJumps+=q.jumps;maxIndex=Math.max(maxIndex,512);
const result={run:"LSPV4/466",date:"2026-11-07 PST",status:"PROVED/RESTRICTED abstract indexed dictionary lemma; COMPUTATIONAL finite V8 semantics; OPEN native complete interpreter",tests,trials,actions,totalClears,totalInserts,totalJumps,maxIndex,farReads,corruptSourceRejects:2,k4SatModels:8,k4UnsatModels:0,seedFinal:seed,allPass:true};
return result;