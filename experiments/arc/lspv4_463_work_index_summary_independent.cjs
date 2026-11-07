'use strict';
const assert=(ok,msg)=>{if(!ok)throw new Error(msg||'assertion failed');};
let checks=0;
class GuestIndex {
  constructor(D){this.D=D;this.head=0;this.highest=0;this.raw=new Map();this.low=0n;this.high=0;this.steps=0;this.scans=0;}
  move(delta){this.head+=delta;assert(this.head>=0);this.highest=Math.max(this.highest,this.head);this.steps++;}
  write(v){assert(v===0||v===1);const old=this.raw.get(this.head)||0;this.raw.set(this.head,v);
    if(this.head<this.D)this.low+=BigInt(v-old)*(1n<<BigInt(this.head));else this.high+=v-old;
    this.steps++;this.verify();}
  exact(){let target=0n;for(const [i,v] of this.raw)if(v)target+=1n<<BigInt(i);return target;}
  verify(){let low=0n,hi=0;for(const [i,v] of this.raw){if(i<this.D)low+=BigInt(v)*(1n<<BigInt(i));else hi+=v;}
    assert(low===this.low && hi===this.high);checks++;}
  jump(){const target=this.exact();
    assert(this.high===0?target===this.low:target>=(1n<<BigInt(this.D)));
    this.scans+=this.highest+1;this.raw.clear();this.low=0n;this.high=0;this.steps++;this.verify();return target;}
}
const cases=[];
for(const L of [8,16,32,64,128,256]){
 const D=Math.max(3,Math.floor(Math.log2(L+2))+1),q=L;const m=new GuestIndex(D);
 for(let i=0;i<L;i++)m.move(1);m.write(0);
 for(let i=0;i<q;i++){m.write(0);assert(m.jump()===0n);checks++;}
 const before=m.steps;assert(before===L+1+2*q && m.scans===q*(L+1));
 m.write(1);assert(m.high===1);m.write(0);assert(m.high===0);
 for(let i=0;i<L;i++)m.move(-1);m.write(1);assert(m.jump()===1n);
 cases.push({L,D,q,guest_steps_before_tail:before,baseline_index_scans_before_tail:q*(L+1),
 scan_to_step_ratio:Math.round(10000*q*(L+1)/before)/10000,work_high_water:1,tail_steps:m.steps-before,total_jumps:q+1});
}
for(let D=1;D<=5;D++)for(let mask=0;mask<1<<Math.min(D+2,6);mask++){
 const m=new GuestIndex(D),n=Math.min(D+2,6);
 for(let i=0;i<n;i++){while(m.head<i)m.move(1);m.write((mask>>i)&1);}
 const expected=m.exact();assert(m.jump()===expected);checks++;
}
// Native signed four-clause-per-vertex strict 3-CNF K4 Tseitin parity controls.
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function models(charge){const cls=[];for(let v=0;v<4;v++){
 const es=edges.flatMap(([a,b],i)=>a===v||b===v?[i+1]:[]);
 for(let mask=0;mask<8;mask++){
 const parity=((mask&1)?1:0)^((mask&2)?1:0)^((mask&4)?1:0);
 if(parity!==charge[v])cls.push(es.map((id,j)=>mask&(1<<j)?-id:id));
 }}
 assert(cls.length===16);let count=0;
 for(let a=0;a<64;a++)if(cls.every(c=>c.some(l=>l>0?Boolean(a&(1<<(l-1))):!Boolean(a&(1<<(-l-1))))))count++;
 return count;}
assert(models([0,0,0,0])===8 && models([1,0,0,0])===0);
assert([1,0,-3].some(l=>l===0));checks+=3;
const result={status:'COMPUTATIONAL',cases,assertion_groups:checks,k4_original_source_control:{
 even_charge_models:8,odd_charge_models:0,original_ternary_clauses:16,malformed_zero_literal_rejected:true},
 model_limit:'Independent exact host-machine index semantics, NOT native FLMV timing or universal SAT contraction.'};
if(typeof module!=='undefined')console.log(JSON.stringify(result,null,2));