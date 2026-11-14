"use strict";
// TMR-1/016: one physical input head, d+1 locally moving binary work tapes.
// Every work-head movement and tape bit read/write costs one counted microstep.
// High-level fixed-d program control is not a compiled TM transition table.
function ck(ok,msg){if(!ok)throw Error(msg);}

class Tape {
  constructor(ticks){this.bits=[];this.h=0;this.ticks=ticks;this.max=0;}
  seek(j){ck(j>=0,"negative work address");while(this.h!==j){this.h+=this.h<j?1:-1;this.ticks.n++;this.max=Math.max(this.max,this.h+1);}}
  read(j){this.seek(j);this.ticks.n++;this.max=Math.max(this.max,j+1);return this.bits[j]||0;}
  put(j,v){this.seek(j);this.ticks.n++;this.bits[j]=v;this.max=Math.max(this.max,j+1);}
  inc(){let j=0;while(this.read(j)===1){this.put(j,0);j++;}this.put(j,1);this.seek(0);}
  copy(src){const n=Math.max(this.bits.length,src.bits.length);for(let j=0;j<n;j++)this.put(j,j<src.bits.length?src.read(j):0);this.seek(0);src.seek(0);}
  zero(){let z=true;for(let j=0;j<this.bits.length;j++)if(this.read(j)!==0)z=false;this.seek(0);return z;}
  dec(){ck(!this.zero(),"counter underflow");let j=0;while(this.read(j)===0){this.put(j,1);j++;}this.put(j,0);this.seek(0);}
}

function semantic(bits){
 if(bits.length%3)return "MALFORMED";
 for(let a=0;a<8;a++){let good=true;for(let i=0;i<bits.length;i+=3){if(parseInt(bits.slice(i,i+3),2)===a){good=false;break;}}if(good)return "SAT";}return "UNSAT";
}

function simulate(bits,d,gated){
 ck(Number.isInteger(d)&&d>=0&&d<=8,"invalid d");const L=bits.length,q=L+1,steps={n:0},qt=new Tape(steps),cnt=Array.from({length:d},()=>new Tape(steps));let p=0,parity=0,mask=0,part=0,mod=0;
 while(p<q){
   if(p>=1&&p<=L){const v=Number(bits[p-1]);parity^=v;part=((part<<1)|v)&7;mod=(mod+1)%3;if(mod===0)mask|=1<<part;}
   p++;steps.n++;qt.inc();
 }
 while(p>0){p--;steps.n++;}
 const prepass=steps.n,lab=mod?"MALFORMED":mask===255?"UNSAT":"SAT",expect=semantic(bits);
 ck(lab===expect,"incorrect SAT label");ck(parity===[...bits].reduce((s,x)=>s^Number(x),0),"parity error");ck(p===0,"prepass head reset");
 let tours=0;
 function lap(){while(p<q){p++;steps.n++;}while(p>0){p--;steps.n++;}tours++;}
 function loops(level){
   if(level===0){lap();return;}
   const t=cnt[level-1];t.copy(qt);
   while(!t.zero()){loops(level-1);t.dec();}
 }
 if(gated&&parity===1)loops(d);
 steps.n++; // terminal gate, no hidden source transition
 const baseline=prepass+1,extra=steps.n-baseline;
 const expectedTours=gated&&parity===1?q**d:0;
 ck(tours===expectedTours,"wrong lap count");ck(extra>=2*q*expectedTours,"missing real head moves");
 ck(p===0&&qt.h===0&&cnt.every(c=>c.h===0),"unrestored physical heads");
 const actualSpace=qt.max+cnt.reduce((s,c)=>s+c.max,0);
 const w=Math.floor(Math.log2(q))+1;
 ck(actualSpace<=(d+1)*(w+1),"work space bound");
 return {label:lab,q,d,parity,gated,steps:steps.n,prepass,extra,tours,space:actualSpace,abstract:baseline};
}

function run(){
 const out={method:"direct hosted-V8 instrumented local-head binary tape controller, no foreign source",status:"COMPUTATIONAL",counts:{cases:0,sat:0,unsat:0,malformed:0,steps:0,odd_detours:0,roundtrips:0,max_space:0,failures:0},per_d:{}};
 for(let d=0;d<=3;d++){
  const s={cases:0,steps:0,sat:0,unsat:0,malformed:0,odd_detours:0,roundtrips:0,max_space:0,min_odd_ratio:Infinity,max_odd_ratio:0};
  const fixtures=[];const maxL=d===3?4:7;
  for(let L=0;L<=maxL;L++)for(let n=0;n<2**L;n++)fixtures.push(L===0?"":n.toString(2).padStart(L,"0"));
  if(d<=1)fixtures.push("000".repeat(8),Array.from({length:8},(_,k)=>k.toString(2).padStart(3,"0")).join(""),"111".repeat(7)+"010");
  for(const bits of fixtures)for(const gated of [false,true]){
    const r=simulate(bits,d,gated);s.cases++;s.steps+=r.steps;s[r.label.toLowerCase()]++;s.roundtrips+=r.tours;s.max_space=Math.max(s.max_space,r.space);
    if(gated&&r.parity){s.odd_detours++;const ratio=r.steps/r.abstract;s.min_odd_ratio=Math.min(s.min_odd_ratio,ratio);s.max_odd_ratio=Math.max(s.max_odd_ratio,ratio);}
  }
  out.per_d[d]={...s,fixture_count:fixtures.length};
  for(const k of ["cases","steps","sat","unsat","malformed","odd_detours","roundtrips"])out.counts[k]+=s[k];
  out.counts.max_space=Math.max(out.counts.max_space,s.max_space);
 }
 return out;
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
