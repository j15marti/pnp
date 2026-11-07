/* LSPV-2/468 independently implemented segment-tree/BigInt control.
 * This checks mathematical port semantics, NOT native FLMV.
 */
"use strict";
function run(){
  let seed=4682026, checks=0, far=0, jumps=0, inserted=0, retired=0, steps=0, maxIndex=0;
  function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
  function ok(x,m){if(!x)throw Error(m||"failed");checks++;}
  class Arena{
    constructor(){this.p=1;this.bits=[0];this.tree=[0,0];this.live=new Set();}
    grow(j){
      if(j<this.p)return;
      let cap=this.p;while(j>=cap)cap*=2;
      this.bits.length=cap;for(let a=this.p;a<cap;a++)this.bits[a]=0;
      this.p=cap;this.tree=Array(2*cap).fill(0);
      for(let a=0;a<cap;a++)this.tree[cap+a]=this.bits[a]||0;
      for(let a=cap-1;a>0;a--)this.tree[a]=this.tree[2*a]+this.tree[2*a+1];
    }
    write(j,b){
      this.grow(j);if(this.bits[j]===b)return;
      this.bits[j]=b;
      if(b){this.live.add(j);inserted++;}else this.live.delete(j);
      let p=this.p+j;this.tree[p]=b;
      while(p>1){p>>=1;this.tree[p]=this.tree[2*p]+this.tree[2*p+1];}
    }
    top(){
      if(!this.tree[1])return -1;
      let p=1;while(p<this.p){p=(this.tree[p*2+1]>0)?p*2+1:p*2;}
      return p-this.p;
    }
    clear(){const n=this.live.size;for(const j of Array.from(this.live))this.write(j,0);retired+=n;}
    small(c){let v=0n;for(let j=0;j<=c && j<this.p;j++)if(this.bits[j])v|=(1n<<BigInt(j));return v;}
    verify(){ok(this.live.size===this.tree[1],"tree total");let count=0;for(let j=0;j<this.p;j++){if(this.bits[j]){count++;ok(this.live.has(j),"list membership");}}ok(count===this.live.size);}
  }
  function testcase(bits){
    let live=new Arena(),frozen=new Arena(),index=0,delta=0n,refHead=0n,refBits=new Set();
    function pos(){
      const lim=BigInt(bits.length)+(delta<0n?-delta:delta)+2n;
      const cutoff=lim.toString(2).length;
      const highest=frozen.top();
      if(highest>=cutoff)return null;
      return frozen.small(cutoff)+delta;
    }
    function read(){
      const a=pos();
      const got=(a===null||a<0n||a>=BigInt(bits.length))?0:bits[Number(a)];
      const ref=(refHead<0n||refHead>=BigInt(bits.length))?0:bits[Number(refHead)];
      if(refHead>=BigInt(bits.length))far++;
      ok(got===ref,"input bit");
      ok(refBits.size===live.live.size,"live bits");
      for(const j of refBits)ok(live.live.has(j),"live set");
      steps++;
    }
    for(let i=0;i<350;i++){
      const choice=rand()%100;
      if(choice<22){
        const d=(rand()%3===0)?-1:1;
        index=Math.max(0,index+d);maxIndex=Math.max(maxIndex,index);
      }else if(choice<45){
        const b=rand()%2;
        live.write(index,b);
        if(b)refBits.add(index);else refBits.delete(index);
      }else if(choice<69){
        refHead=0n;for(const j of refBits)refHead+=1n<<BigInt(j);
        refBits.clear();
        frozen.clear();
        const tmp=live;live=frozen;frozen=tmp;delta=0n;
        jumps++;
      }else if(choice<82){
        const d=(rand()%2)?1:-1;
        if(d===1){delta++;refHead++;}
        else{if(pos()!==0n)delta--;if(refHead>0n)refHead--;}
      }else read();
      steps++;
      if(i%31===0){read();live.verify();frozen.verify();}
    }
    read();live.verify();frozen.verify();
  }
  for(let i=0;i<120;i++){
    const n=1+rand()%40,bits=Array.from({length:n},()=>rand()%2);
    testcase(bits);
  }
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  let even=0,odd=0;
  for(let charge=0;charge<16;charge++){
    let clauses=[];
    for(let v=0;v<4;v++){
      const es=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
      for(let a=0;a<8;a++)if(((a.toString(2).split("1").length-1)&1)!==((charge>>v)&1))
        clauses.push(es.map((j,k)=>((a>>k)&1)?-(j+1):j+1));
    }
    let models=0;
    for(let assignment=0;assignment<64;assignment++)
      if(clauses.every(cl=>cl.some(l=>((assignment>>(Math.abs(l)-1))&1)===(l>0?1:0))))models++;
    ok(clauses.length===16,"strict 3 clauses");
    ok(models===((charge.toString(2).split("1").length-1)%2===0?8:0),"parity label");
    if(models)even++;else odd++;
  }
  ok(even===8&&odd===8);
  ok(retired<=inserted);
  return {seed:4682026,tests:120,assertions:checks,guest_actions:steps,jumps,insertions:inserted,retirements:retired,max_index_coordinate:maxIndex,far_read_checks:far,labels:{SAT:even,UNSAT:odd},status:"COMPUTATIONAL; not native FLMV"};
}
if(typeof module!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");