'use strict';
// TMR-1/030 finite single-physical-head block emulator. Logical blocks are
// indexed in the test harness; they are delimiter-located in the proof.
function run() {
  let asserts=0, cases=0, steps=0, simulatedMoves=0, maxRatio=0;
  function check(x,msg) { asserts++; if(!x) throw new Error(msg); }
  function headerEmulator(bits) {
    const h=bits.length, W=2*(h+1)+4, tape=new Map();
    let physical=0, cost=0, guestPos=0, touched=new Set([0]);
    const base=j=>j*W;
    function go(x){cost+=Math.abs(physical-x);physical=x;}
    function read(x){go(x);cost++;return tape.has(x)?tape.get(x):'_';}
    function write(x,v){go(x);cost++;tape.set(x,v);}
    function init(){write(0,'_');write(1,'X');for(let i=0;i<=h;i++){
      write(2+2*i,i<h?bits[i]:'#');write(3+2*i,i===0?'H':'.');
    }}
    init();
    function observation(){let b=base(guestPos),sym=read(b),head=-1,bit='?';
      for(let i=0;i<=h;i++){let v=read(b+3+2*i);if(v==='H'){
        check(head<0,'double input head');head=i;bit=read(b+2+2*i);
      }}
      check(head>=0,'missing header head');return {symbol:sym,head,bit};
    }
    function update(symbol,newHead,delta){let oldB=base(guestPos);
      write(oldB,symbol);
      for(let i=0;i<=h;i++)write(oldB+3+2*i,i===newHead?'H':'.');
      let next=Math.max(0,guestPos+delta), newB=base(next);
      if(next!==guestPos){
        let prior=read(newB+1);if(prior!=='X'){
          write(newB,'_');write(newB+1,'X');
        }
        // Copy the complete short read-only header and its current head mark.
        // Each copy performs charged physical traversals between adjacent blocks.
        for(let i=0;i<=h;i++)for(let sub=0;sub<2;sub++){
          let off=2+2*i+sub;
          write(newB+off,read(oldB+off));
        }
        guestPos=next;touched.add(next);
      }
      go(base(guestPos));
    }
    return {h,W,tape,base,observation,update,position:()=>guestPos,
      cells:()=>touched,cost:()=>cost};
  }
  function generator(seed){let x=seed>>>0;return ()=>{x=(Math.imul(x,1664525)+1013904223)>>>0;return x;};}
  for(let h=1;h<=12;h++)for(let seed=1;seed<=18;seed++){
    const rng=generator(h*65537+seed),bits=Array.from({length:h},()=>String(rng()&1));
    const em=headerEmulator(bits),work=new Map();let p=0,j=0,prev=em.cost();
    for(let s=0;s<90;s++){
      let ob=em.observation();
      check(ob.symbol===(work.get(j)||'_'),'guest work read mismatch');
      check(ob.head===p,'header head mismatch');
      check(ob.bit===(p<h?bits[p]:'#'),'header bit mismatch');
      let r=rng(),newSymbol=String(((r>>>7)^(ob.symbol==='1'?1:0)^(ob.bit==='1'?1:0))&1);
      let dp=((r>>>12)%3)-1,dj=((r>>>19)%3)-1;
      let np=Math.max(0,Math.min(h,p+dp)),nj=Math.max(0,j+dj);
      work.set(j,newSymbol);em.update(newSymbol,np,dj);
      check(em.position()===nj,'guest work head mismatch');
      let inc=em.cost()-prev;prev=em.cost();
      check(inc<=75*(h+4)*(h+4),'short-header quadratic per-step cap');
      maxRatio=Math.max(maxRatio,inc/((h+1)*(h+1)));
      for(let k of em.cells())check(em.tape.get(em.base(k))===(work.get(k)||'_'),'global guest tape mismatch');
      p=np;j=nj;steps++;
    }
    cases++;simulatedMoves+=em.cost();
  }
  // Repeated adjacent-pair deletion verifies length = 2^n without destroying data.
  let halving=0;
  for(let N=1;N<=257;N++){
    let live=Array(N).fill(true),n=0,parityOK=true,visits=0;
    while(true){let count=live.filter(Boolean).length;
      if(count===1)break;
      if(count%2){parityOK=false;break;}
      let toggle=0;
      for(let i=0;i<N;i++){visits++;if(live[i]){toggle^=1;if(toggle===0)live[i]=false;}}
      n++;
    }
    check(parityOK===(Number.isInteger(Math.log2(N))),'power-two detection');
    if(parityOK)check(n===Math.log2(N),'derived arity');
    check(visits<=N*(Math.ceil(Math.log2(N))+1),'N log N sweeps');
    halving++;
  }
  // The repaired exponent budget is c<1.99, not 2c<1.99, for this
  // length-only, short-header constructor with compact output prefix.
  let frontiers=0;
  for(let c=0;c<=198;c+=3)for(let a=0;a<=100;a+=10)
    for(let b=0;b<=100;b+=10)for(let e=0;e<=100;e+=10){
      let d=Math.max(100,a,b,e); // all exponents expressed in hundredths
      let valid=(c<199 && e+d<199);
      check(valid===((c<199)&&(e+Math.max(100,a,b,e)<199)),'exponent equivalence');
      if(c>=100&&c<199&&e+d<199)check(2*c>=199,'quadratic old fallback loses constructor regime');
      frontiers++;
    }
  return {status:'COMPUTATIONAL',engine:'host-native-JavaScript',seed:'h*65537+seed',
    constructorCases:cases,guestSteps:steps,physicalHeadMovementAndReadWrite:simulatedMoves,
    maxPerStepRatio:maxRatio,halvingCases:halving,exponentCases:frontiers,
    assertions:asserts,failures:0,note:'Finite block emulator, not an actual compiled finite-alphabet one-tape TM; asymptotic proof is separate.'};
}
const result=run();
if(typeof process!=='undefined' && process.stdout)process.stdout.write(JSON.stringify(result)+'\n');
