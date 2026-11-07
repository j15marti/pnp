// Canonical persistent binary positional keys, with independently coded BigInt reference.
// Research prototype only. Native FLMV machine compilation is NOT proved.
'use strict';
class Bits {
 constructor(){this.nodes=[null,{h:0}],this.memo=new Map(),this.ones=[1];this.lookup=0;}
 node(h,a,b){if(!a&&!b)return 0;const key=h+':'+a+':'+b;this.lookup++;let id=this.memo.get(key);if(id!==undefined)return id;id=this.nodes.length;this.nodes.push({h,a,b});this.memo.set(key,id);return id;}
 one(h){while(this.ones.length<=h){let k=this.ones.length;this.ones.push(this.node(k,this.ones[k-1],this.ones[k-1]));}return this.ones[h];}
 kids(id){return id?[this.nodes[id].a,this.nodes[id].b]:[0,0];}
 put(id,h,pos,val){if(!h)return val?1:0;let [l,r]=this.kids(id),half=2**(h-1);if(pos<half)l=this.put(l,h-1,pos,val);else r=this.put(r,h-1,pos-half,val);return this.node(h,l,r);}
 assign(id,h,lo,hi,val,off=0){const len=2**h;if(hi<=off||lo>=off+len)return id;if(lo<=off&&off+len<=hi)return val?this.one(h):0;let [l,r]=this.kids(id),half=len/2;return this.node(h,this.assign(l,h-1,lo,hi,val,off),this.assign(r,h-1,lo,hi,val,off+half));}
 first(id,h,want,off=0){if(want&&id===0)return Infinity;if(!want&&id===this.one(h))return Infinity;if(!h)return off;let [l,r]=this.kids(id),v=this.first(l,h-1,want,off);return Number.isFinite(v)?v:this.first(r,h-1,want,off+2**(h-1));}
 value(id,h){if(!id)return 0n;if(!h)return 1n;let [l,r]=this.kids(id);return this.value(l,h-1)+(this.value(r,h-1)<<BigInt(2**(h-1)));}
}
class Sim {
 constructor(){this.b=new Bits();this.h=1;this.index=0;this.workhead=0;this.indexhead=0;this.mem=new Map();this.growth=0;this.rekeys=0;}
 expand(){const b=this.b,h=this.h,wrap=id=>id?b.node(h+1,id,0):0,newmap=new Map();for(const [id,v] of this.mem){newmap.set(wrap(id),v);this.rekeys++;}this.mem=newmap;this.index=wrap(this.index);this.workhead=wrap(this.workhead);this.h++;this.growth++;}
 ensure(i){while(i>=2**this.h)this.expand();}
 next(id){let p=this.b.first(id,this.h,0);if(!Number.isFinite(p)){this.expand();id=this.workhead;p=this.b.first(id,this.h,0);}id=this.b.assign(id,this.h,0,p,0);return this.b.put(id,this.h,p,1);}
 prev(id){if(!id)return 0;const p=this.b.first(id,this.h,1);id=this.b.assign(id,this.h,0,p,1);return this.b.put(id,this.h,p,0);}
 act(op){if(op==='IR'){this.indexhead++;this.ensure(this.indexhead);}else if(op==='IL')this.indexhead=Math.max(0,this.indexhead-1);else if(op==='I1'||op==='I0')this.index=this.b.put(this.index,this.h,this.indexhead,op==='I1'?1:0);else if(op==='J'){this.workhead=this.index;this.index=0;}else if(op==='WR')this.workhead=this.next(this.workhead);else if(op==='WL')this.workhead=this.prev(this.workhead);else if(op==='W1')this.mem.set(this.workhead,1);else if(op==='W0')this.mem.delete(this.workhead);else if(op!=='R')throw Error('unknown action');}
 read(){return this.mem.get(this.workhead)||0;}
}
class IndependentBigInt {
 constructor(){this.ih=0;this.i=0n;this.w=0n;this.mem=new Map();}
 act(op){if(op==='IR')this.ih++;else if(op==='IL')this.ih=Math.max(0,this.ih-1);else if(op==='I1')this.i|=1n<<BigInt(this.ih);else if(op==='I0')this.i&=~(1n<<BigInt(this.ih));else if(op==='J'){this.w=this.i;this.i=0n;}else if(op==='WR')this.w++;else if(op==='WL'){if(this.w>0n)this.w--;}else if(op==='W1')this.mem.set(this.w.toString(),1);else if(op==='W0')this.mem.delete(this.w.toString());else if(op!=='R')throw Error('unknown ref action');}
 read(){return this.mem.get(this.w.toString())||0;}
}
let seed=0x46812345;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
function main(){let checks=0,actions=0,aliases=0,growth=0,rekeys=0,maxIndex=0,maxNodes=0,nonblank=0;let failures=[];
 function run(ops){const s=new Sim(),o=new IndependentBigInt(),seen=new Map();for(const op of ops){s.act(op);o.act(op);actions++;const vi=s.b.value(s.index,s.h),vw=s.b.value(s.workhead,s.h);if(vi!==o.i||vw!==o.w||s.read()!==o.read()||s.indexhead!==o.ih||s.mem.size!==o.mem.size)throw Error('Mismatch at action '+actions+' '+op);checks+=5;
 const key=vw.toString(),old=seen.get(key);if(old){let id=old.id;for(let h=old.h;h<s.h;h++)id=id?s.b.node(h+1,id,0):0;if(id!==s.workhead)throw Error('NONCANONICAL alias '+key);aliases++;}seen.set(key,{id:s.workhead,h:s.h});checks++;maxIndex=Math.max(maxIndex,o.ih);maxNodes=Math.max(maxNodes,s.b.nodes.length);}growth+=s.growth;rekeys+=s.rekeys;nonblank+=s.mem.size;}
 run(['I1','J','W1','I0','IR','I1','J','WL','R','WR','WL','R']);
 const far=[];for(let j=0;j<257;j++)far.push('IR');far.push('I1','J','W1');for(let j=0;j<100;j++)far.push('I1','J','R');run(far);
 const codes=['IR','IL','I1','I0','J','WR','WL','W1','W0','R'];for(let i=0;i<100;i++){const ops=[];for(let j=0;j<220;j++)ops.push(codes[rand()%codes.length]);run(ops);}
 return {status:'PASS',seed:'0x46812345',traces:102,actions,checks,canonical_alias_checks:aliases,maximum_guest_INDEX_head:maxIndex,maximum_persistent_nodes_per_trace:maxNodes,capacity_doublings:growth,dictionary_rekeys:rekeys,cumulative_nonblank_work_cells:nonblank,environment:'Node.js host',native_FLVM_executed:false};}
const result=main();console.log(JSON.stringify(result));if(typeof module!=='undefined')module.exports=result;
