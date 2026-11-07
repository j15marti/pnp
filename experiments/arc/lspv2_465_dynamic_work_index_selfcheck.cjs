function selfcheck() {
  function ok(p,msg){if(!p) throw new Error(msg);}
  class Machine {
    constructor(B){this.B=B;this.D=Math.max(1,Math.ceil(Math.log2(B+2)));this.low=0n;this.high=0;this.head=0;this.highwater=0;this.tape=new Map();this.T=0;this.scan=0;this.expansions=0;this.maxD=this.D;this.maxHigh=0;this.jumps=0;}
    move(to){ok(Number.isInteger(to)&&to>=0,"head");this.T+=Math.abs(to-this.head);this.head=to;this.highwater=Math.max(this.highwater,to);}
    readAt(i){return this.tape.get(i)||0;}
    write(b){ok(b===0||b===1,"binary");const i=this.head,old=this.readAt(i);this.T++;if(b)this.tape.set(i,1);else this.tape.delete(i);if(i<this.D){const bit=1n<<BigInt(i);if(old!==b)this.low+=(b?bit:-bit);} else this.high+=b-old;this.maxHigh=Math.max(this.maxHigh,this.high);}
    check(){let bits=0n,high=0;for(const [i,b] of this.tape){ok(b===1,"bad tape");if(i<this.D)bits|=(1n<<BigInt(i));else high++}ok(this.low===bits&&high===this.high,"summary mismatch");ok(this.high>=0,"negative high count");}
    expand(){ok(this.high>0,"spurious expand");let j=-1;for(let i=0;i<=this.highwater;i++){this.scan++;if(this.readAt(i))j=i;}ok(j>=this.D,"lost high");const next=Math.max(2*this.D,j+1);this.D=next;this.low=0n;this.high=0;for(let i=0;i<=this.highwater;i++){this.scan++;if(this.readAt(i)){if(i<this.D)this.low|=(1n<<BigInt(i));else this.high++;}}this.maxD=Math.max(this.maxD,this.D);this.expansions++;this.check();}
    jump(){this.check();let full=0n;for(const [i,b] of this.tape){if(b)full|=(1n<<BigInt(i));}if(this.high>0)this.expand();ok(this.high===0&&full===this.low,"jump decode");const target=this.low;this.T++;this.tape.clear();this.low=0n;this.high=0;this.jumps++;this.check();return target;}
  }
  let asserts=0,instances=0,expansions=0,scans=0,maxCapacity=0,largeZero=0,highBurst=0, maxSteps=0;
  const verify=(c)=>{c.check();asserts++;};
  const finish=(c,target,limit)=>{const value=c.jump();ok(value===BigInt(target),"target");asserts++;ok(value<=BigInt(limit),"illegal high target");asserts++;const bound=Math.max(1,Math.ceil(Math.log2(limit+1)));ok(c.maxD<=2*Math.max(c.D,bound),"capacity");asserts++;instances++;expansions+=c.expansions;scans+=c.scan;maxCapacity=Math.max(maxCapacity,c.maxD);maxSteps=Math.max(maxSteps,c.T);};
  // Large temporary index-tape occupancy need not enlarge the mirrored low budget.
  for(let size of [24,96,512,2048]){
    const c=new Machine(64);
    for(let i=0;i<size;i++){c.move(i);c.write(1);} highBurst+=size;
    for(let i=size-1;i>=0;i--){c.move(i);c.write(0);}
    c.move(0);c.write(1);verify(c);ok(c.expansions===0,"premature expansion");asserts++;
    finish(c,1,64**5);largeZero++;
  }
  // One legal far jump expands the budget only at a real jump; later jumps reuse it.
  for(let pow=7;pow<=35;pow+=2){
    let c=new Machine(64);
    for(let j=0;j<3;j++){const k=Math.min(pow+j,37);c.move(k);c.write(1);verify(c);let val=c.jump();ok(val===2n**BigInt(k),"wide jump");asserts++;}
    ok(c.expansions<=2,"too many expansions in three jumps");asserts++;
    instances++;expansions+=c.expansions;scans+=c.scan;maxCapacity=Math.max(maxCapacity,c.maxD);maxSteps=Math.max(maxSteps,c.T);
  }
  // Adversarial noisy high-zero and transient-high-one runs; actual jumps <= 2^24.
  let seed=0x9e3779b9;
  function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
  for(let z=0;z<180;z++){
    let c=new Machine(32),count=0;const tmp=60+rand(140);
    for(let i=0;i<tmp;i++){c.move(i);c.write(rand(2));count++;}
    for(let i=tmp-1;i>=0;i--){c.move(i);c.write(0);}
    const width=1+rand(24);let want=0n;
    for(let i=0;i<width;i++){c.move(i);let v=rand(2);c.write(v);if(v)want|=1n<<BigInt(i);}
    verify(c);
    finish(c,want,2**24);
  }
  return {status:"PASS",mode:"finite_host_JS_not_native_FLMV",instances,assertions:asserts,guest_index_jumps:180+4+15*3,range_expansions:expansions,total_scanned_index_cells:scans,maximum_low_budget_bits:maxCapacity,large_temporary_ones:highBurst,long_high_zero_controls:largeZero,max_simulated_steps:maxSteps,seed:"0x9e3779b9"};
}
console.log(JSON.stringify(selfcheck(),null,2));
