"use strict";
// TMR-1/016 independent one-source-head, charged binary-work-counter audit.
// Each primitive touches only the current head cell, and each head movement
// or tape write is one counted locally implementable transition.
function check(x,msg){if(!x)throw Error(msg);}
class Ledger{
 constructor(){this.t=0;this.input=0;this.work=0;this.write=0;}
 step(kind){this.t++;this[kind]++;}
}
class Tape{
 constructor(log){this.log=log;this.a=[];this.h=0;this.max=0;}
 read(){this.max=Math.max(this.max,this.h+1);return this.a[this.h]===undefined?"B":this.a[this.h];}
 move(dir){check(this.h+dir>=0,"negative work head");this.h+=dir;this.max=Math.max(this.max,this.h+1);this.log.step("work");}
 write(b){this.max=Math.max(this.max,this.h+1);this.a[this.h]=b;this.log.step("write");}
 inc(){
  check(this.h===0,"increment head not reset");
  for(;;){let v=this.read();this.write(v===1?0:1);
   if(v!==1)break;this.move(1);
  }
  while(this.h>0)this.move(-1);
 }
 equal(y){
  check(this.h===0&&y.h===0,"compare heads not reset");
  let ok=true;
  for(;;){const a=this.read(),b=y.read();this.log.step("work");
   if(a==="B"&&b==="B")break;
   if(a!==b)ok=false;
   this.move(1);y.move(1);
  }
  while(this.h>0)this.move(-1);
  while(y.h>0)y.move(-1);
  return ok;
 }
 clear(){
  check(this.h===0,"clear head not reset");
  while(this.read()!=="B"){this.write(0);this.move(1);}
  this.log.step("work");
  while(this.h>0)this.move(-1);
 }
 value(){return this.a.reduce((s,b,i)=>s+(b===1?2**i:0),0);}
}
class Physical{
 constructor(bits){this.bits=bits;this.p=0;this.log=new Ledger();this.par=0;this.part=0;this.mod=0;this.mask=0;this.qreg=new Tape(this.log);this.leaves=0;this.counters=[];this.gateLabel=null;}
 symbol(){return this.p===0?"L":this.p===this.bits.length+1?"R":+this.bits[this.p-1];}
 right(parse){
  check(this.symbol()!=="R","input right overflow");
  const v=this.symbol();
  if(parse&&v!=="L"){this.par^=v;this.part=((this.part<<1)|v)&7;this.mod=(this.mod+1)%3;
    if(this.mod===0)this.mask|=1<<this.part;}
  this.p++;this.log.step("input");
 }
 left(){check(this.p>0,"input left overflow");this.p--;this.log.step("input");}
 sweep(parse){check(this.p===0,"sweep begins off left endmarker");while(this.symbol()!=="R"){
    if(parse)this.qreg.inc();this.right(parse);
   }while(this.symbol()!=="L")this.left();}
 classify(){return this.mod!==0?"MALFORMED":this.mask===255?"UNSAT":"SAT";}
 enter(){this.sweep(true);check(this.qreg.value()===this.bits.length+1,"length tally");this.gateLabel=this.classify();this.log.step("work");}
 detour(d){this.counters=Array.from({length:d},()=>new Tape(this.log));
  const nested=(level)=>{if(level===d){this.sweep(false);this.leaves++;return;}
    for(;;){nested(level+1);this.counters[level].inc();
      if(this.counters[level].equal(this.qreg)){this.counters[level].clear();break;}
    }};
  nested(0);
  check(this.p===0&&this.counters.every(t=>t.value()===0),"detour restoration");
 }
}
function ref(bits){if(bits.length%3)return "MALFORMED";const seen=new Set();
 for(let i=0;i<bits.length;i+=3)seen.add(parseInt(bits.slice(i,i+3),2));
 return seen.size===8?"UNSAT":"SAT";
}
function evaluate(bits,d,stats){
 const a=new Physical(bits);a.enter();
 const baseline=a.log.t,label=ref(bits),odd=+bits.split("").reduce((v,c)=>v^(+c),0);
 check(a.par===odd&&a.gateLabel===label,"parser/parity mismatch");
 check(a.p===0&&a.qreg.value()===bits.length+1,"input baseline");
 if(odd)a.detour(d);
 const gap=a.log.t-baseline,q=bits.length+1;
 check(a.gateLabel===label&&a.p===0,"changed output/source head");
 check(a.qreg.value()===q,"counter source q corrupted");
 check(!odd||a.leaves===q**d,"incorrect nested scan count");
 check(odd||gap===0,"detour on even input");
 check(!odd||gap>=2*q**(d+1),"missing physically charged sweeps");
 check(a.log.t===a.log.input+a.log.work+a.log.write,"unaccounted transitions");
 const used=[a.qreg,...a.counters].reduce((s,t)=>s+t.max,0);
 const w=Math.ceil(Math.log2(q+2));
 check(used<=(d+1)*(w+3),"more than logarithmic visited work cells");
 stats.cases++;stats[label.toLowerCase()]++;stats.transitions+=a.log.t;
 stats.inputTransitions+=a.log.input;stats.workTransitions+=a.log.work;
 stats.writeTransitions+=a.log.write;stats.peakWork=Math.max(stats.peakWork,used);
 if(odd){stats.odd++;stats.minRatio=Math.min(stats.minRatio,a.log.t/baseline);
  stats.maxRatio=Math.max(stats.maxRatio,a.log.t/baseline);
  stats.totalExtra+=gap;stats.leafScans+=a.leaves;}
 return {bits,d,odd,label,q,baseline,steps:a.log.t,extra:gap,leaves:a.leaves,visited:used,ratio:a.log.t/baseline};
}
function run(){
 const out={status:"COMPUTATIONAL",model:"one read-only input head plus d+1 locally moving binary work tapes",tests:{},examples:[],failures:0};
 for(let d=0;d<=3;d++){
  const s={cases:0,sat:0,unsat:0,malformed:0,odd:0,transitions:0,inputTransitions:0,workTransitions:0,writeTransitions:0,peakWork:0,minRatio:Infinity,maxRatio:0,totalExtra:0,leafScans:0};
  const maxLen=[8,7,5,4][d],cases=[];
  for(let L=0;L<=maxLen;L++)for(let v=0;v<2**L;v++)cases.push(L===0?"":v.toString(2).padStart(L,"0"));
  cases.push("001".repeat(1)+"000".repeat(7));
  cases.push(Array.from({length:8},(_,i)=>i.toString(2).padStart(3,"0")).join("")+"001");
  cases.push("000".repeat(8));
  cases.push("000".repeat(8)+"1");
  for(const bits of cases){let r=evaluate(bits,d,s);
    if(bits.length>=24&&bits.length%3===0&&r.odd)out.examples.push(r);
  }
  if(s.odd===0)s.minRatio=null;
  out.tests[d]={...s,fixtureCount:cases.length};
 }
 out.totalCases=Object.values(out.tests).reduce((v,s)=>v+s.cases,0);
 out.totalTransitions=Object.values(out.tests).reduce((v,s)=>v+s.transitions,0);
 return out;
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));