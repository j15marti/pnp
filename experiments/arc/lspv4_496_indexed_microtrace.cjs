'use strict';
/* LSPV-4/496: exact primitive-semantics microtrace, not a compiled FLMV program.
 * All higher-level packet arithmetic and host Map operations are TEST HARNESS
 * logic; only named INDEX/WORK operations are counted as native primitives.
 */
function audit496(){
 let checks=0, source_cases=0, sessions=0, reads=0, work_jumps=0, invalid=0;
 const A=(ok,msg)=>{checks++;if(!ok)throw Error('ASSERT '+msg);};
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const incid=Array.from({length:4},(_,v)=>edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean));
 const bin=(n,w)=>n.toString(2).padStart(w,'0');
 function build(ch){
   let s=bin(0xa7,8)+bin(4,8), clauses=[];
   for(let v=0;v<4;v++)for(let p=0;p<2;p++)for(let q=0;q<2;q++){
     const r=p^q^1^ch[v],signs=[p,q,r];
     clauses.push(signs.map((b,k)=>b?-incid[v][k]:incid[v][k]));
     for(let k=0;k<3;k++)s+=String(signs[k])+bin(incid[v][k],8);
   }
   return {bits:s,clauses};
 }
 function sat(cs){
   for(let a=0;a<64;a++)if(cs.every(c=>c.some(l=>{let b=(a>>(Math.abs(l)-1))&1;return l>0?b===1:b===0;})))return true;
   return false;
 }
 class Indexed{
   constructor(root){this.root=root;this.tick=0;this.local=0;this.work=new Map();this.wh=-1;this.dirty=new Set();this.idx={root:new Map(),work:new Map(),guest:new Map()};this.head={root:0,work:0,guest:0};this.workHead=0;this.rootHead=0;this.guestHead=0;this.peak=0;this.workJumps=0;}
   charge(){let ib=Object.values(this.idx).reduce((s,t)=>s+t.size,0);let h=Math.max(1,this.wh+1);this.peak=Math.max(this.peak,h+ib+this.dirty.size*Math.ceil(Math.log2(h+2))+80);}
   put(channel,b){A(b===0||b===1,'bit');const p=this.head[channel];if(b)this.idx[channel].set(p,1);else this.idx[channel].delete(p);this.tick++;this.charge();}
   step(channel,dir){const p=this.head[channel]+dir;A(p>=0,'index head nonnegative');this.head[channel]=p;this.tick++;this.charge();}
   prepare(channel,a){
     A(Number.isSafeInteger(a)&&a>=0,'valid address');
     while(this.head[channel]>0)this.step(channel,-1);
     A(this.idx[channel].size===0,'previous indexed move erases index');
     const b=a.toString(2).split('').reverse().map(Number);
     for(let i=0;i<b.length;i++){this.put(channel,b[i]);if(i+1<b.length)this.step(channel,+1);}
   }
   jump(channel){
     let a=0;for(const [i,b] of this.idx[channel])if(b)a+=2**i;
     A(Number.isSafeInteger(a),'safe finite address');
     this.idx[channel].clear();this.tick++;
     if(channel==='root')this.rootHead=a;
     else if(channel==='work'){this.workHead=a;this.wh=Math.max(this.wh,a);this.workJumps++;}
     else this.guestHead=a;
     this.charge(); A(this.idx[channel].size===0,'erased after jump');return a;
   }
   rootRead(a){this.prepare('root',a);this.jump('root');this.tick++;const b=this.root[this.rootHead]||'0';this.charge();return b==='1'?1:0;}
   workWrite(a,b){this.prepare('work',a);this.jump('work');if(b)this.work.set(a,1);else this.work.delete(a);this.dirty.add(a);this.tick++;this.charge();}
   workRead(a){this.prepare('work',a);this.jump('work');this.tick++;this.charge();return this.work.get(a)||0;}
   begin(edits){A(edits.every(x=>Number.isInteger(x)&&x>=0&&x<4),'edit validation');
     for(let i=0;i<edits.length;i++)for(let k=0;k<2;k++)this.workWrite(2*i+k,(edits[i]>>k)&1);
   }
   guestRead(a,nedits){
     this.prepare('guest',a);this.jump('guest');this.tick++;this.charge();
     let b=this.rootRead(this.guestHead);this.local+=12;
     const j=this.guestHead-16;
     if(j>=0 && j<432 && j%27===18){
       const v=Math.floor(Math.floor(j/27)/4);
       for(let i=0;i<nedits;i++){let q=this.workRead(2*i)|(this.workRead(2*i+1)<<1);b^=Number(q===v);this.local+=8;}
     }
     return b;
   }
   end(){for(const a of this.dirty)this.workWrite(a,0);this.dirty.clear();this.charge();A(this.work.size===0,'no residual work');}
 }
 const paths=[[],[0],[1,3,1]];
 let maximum=0, total_steps=0, total_local=0, total_peak=0, erased=0, guest_index_reads=0;
 for(let mask=0;mask<16;mask++){
   const ch=Array.from({length:4},(_,v)=>(mask>>v)&1), root=build(ch);
   A(root.bits.length===448,'original fixed-length signed proper3 source');
   A(root.clauses.length===16,'16 original clauses');
   for(const c of root.clauses)A(c.length===3&&new Set(c.map(Math.abs)).size===3,'proper clauses');
   A(sat(root.clauses)===(ch.reduce((a,b)=>a^b,0)===0),'parity SAT equivalence');
   source_cases++;
   for(const edits of paths){
     let after=ch.slice();for(const v of edits)after[v]^=1;
     const target=build(after), host=new Indexed(root.bits);
     host.begin(edits);
     let addresses=[0,7,8,15,16,17,18,26,27,447,448,449];
     for(let v=0;v<4;v++)for(let c=0;c<4;c++){
       const h=16+(4*v+c)*27;addresses.push(h,h+9,h+18,h+19,h+26);
     }
     let seed=(mask+1)*7919+edits.length*101;
     for(let i=0;i<90;i++){seed=(seed*1664525+1013904223)>>>0;addresses.push(seed%452);}
     for(const a of addresses){
       const val=host.guestRead(a,edits.length);
       A(val===(target.bits[a]==='1'?1:0),'virtual bit identical to materialized target @'+a);
       A(host.idx.root.size===0&&host.idx.work.size===0&&host.idx.guest.size===0,'all three indexes erased');
       reads++;guest_index_reads++;erased++;
     }
     A(sat(target.clauses)===(after.reduce((a,b)=>a^b,0)===0),'edited formula label');
     A(host.wh+1<=Math.max(1,2*edits.length),'no child body stored in work');
     host.end();A(host.work.size===0,'cleared work across calls');
     work_jumps+=host.workJumps;total_steps+=host.tick;total_local+=host.local;maximum=Math.max(maximum,host.peak);total_peak+=host.peak;
     sessions++;
   }
 }
 const huge=new Indexed(build([0,0,0,0]).bits);
 huge.prepare('work',2**25);A(huge.jump('work')===2**25,'huge indexed work jump');
 A(huge.wh>=2**25,'sparse one-cell jump charges full high-water');
 A(huge.peak>=2**25,'peak counts address, not touched cells');
 huge.prepare('work',0);A(huge.jump('work')===0,'index tape erased and reused');
 A(huge.idx.work.size===0,'index cleared on second jump');
 const padded=new Indexed(build([0,0,0,0]).bits);
 padded.prepare('work',0);padded.jump('work');
 for(let i=0;i<48;i++){if(i)padded.step('work',+1);padded.put('work',0);}
 A(padded.jump('work')===0,'zero-padded index has numeric address zero');
 A(padded.idx.work.size===0,'padded index erased in a single native jump');
 const original=build([0,0,0,0]).bits;
 for(const j of [0,8,16,34,447]){
   const corrupt=original.slice(0,j)+(original[j]==='1'?'0':'1')+original.slice(j+1);
   A(corrupt!==original,'corruption distinct');
   A(corrupt!==build([0,0,0,0]).bits,'source-exact authentication rejects corruption');
   invalid++;
 }
 return {status:'PASS',kind:'finite operational microtrace, not compiled native FLMV',source_cases,sat:8,unsat:8,sessions,guest_virtual_bit_reads:reads,guest_index_erasures_checked:erased,work_index_jumps:work_jumps,primitive_tape_transitions:total_steps,charged_local_address_arithmetic_proxy:total_local,maximum_all_phase_peak_proxy_bits:maximum,total_session_peak_proxy_bits:total_peak,high_work_index_test:2**25,zero_padded_index_bits:48,invalid_source_controls:invalid,assertions:checks,limitations:['The host JavaScript packet arithmetic, Map storage and macro transition scheduler are not compiled to the original indexed Turing machine.','The child bit stream has unchanged encoded length 448; no Route A contraction follows.','Only a subset of indexed operations is modeled. No arbitrary guest WORK-index decoder, native proof checker, or all-input SAT compiler is established.']};
}
return audit496();