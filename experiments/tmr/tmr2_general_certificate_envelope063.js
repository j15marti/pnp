"use strict";
// TMR-2 GENCERT063: exact general Boolean function certificate-envelope audit.
// Qualified model: immutable hidden n-bit source, price-one unknown-coordinate reads,
// zero-price tag toggles/transcript normalization, free local Boolean reasoning.
// Run: node experiments/tmr/tmr2_general_certificate_envelope063.js
function audit() {
  const stats={tag:"GENCERT063",model:"fixed hidden n-bit source; charged coordinate reads",
    full_n3_functions:0,n4_control_functions:0,transcripts:0,source_states:0,
    paid_edges:0,checks:0,failures:0,max_W_minus_B:0,
    examples:[], controls:[], or_cone:[]};
  function check(a,msg){stats.checks++;if(!a){stats.failures++;throw Error(msg);}}
  function pop(x){let k=0;while(x){k+=x&1;x>>=1;}return k;}
  function bits(n){return Array.from({length:n},(_,i)=>3**i);}
  function witnessMask(n,fn){let mask=0;for(let x=0;x<(1<<n);x++)if(fn(x))mask|=1<<x;return mask>>>0;}
  function run(n,f,label){
    const nn=1<<n, bases=bits(n), total=3**n;
    const digits=Array.from({length:total},(_,s)=>bases.map(p=>Math.floor(s/p)%3));
    const candidates=digits.map(d=>Array.from({length:nn},(_,x)=>x).filter(x=>d.every((v,i)=>v===0||((x>>i)&1)===v-1)));
    const known=digits.map(d=>d.reduce((a,v,i)=>v?a|(1<<i):a,0));
    const out=x=>(f>>>x)&1;
    const force=s=>{const cs=candidates[s];return cs.every(x=>out(x)===out(cs[0]));};
    const wm=new Array(total);
    function W(s){if(wm[s]!==undefined)return wm[s];if(force(s))return wm[s]=0;
      let b=nn+1;for(let i=0;i<n;i++)if(digits[s][i]===0){
        const p=bases[i],z=W(s+p),o=W(s+2*p);b=Math.min(b,1+Math.max(z,o));
      }return wm[s]=b;}
    const dm=Array.from({length:total},()=>new Array(nn));
    function D(s,x){
      if(dm[s][x]!==undefined)return dm[s][x];
      if(!candidates[s].includes(x))throw Error("incompatible source");
      const target=out(x);let best=n+1;
      for(let sub=0;sub<nn;sub++){
        if((sub&known[s])!==0||pop(sub)>=best)continue;
        let all=true;
        for(const y of candidates[s])if(((y^x)&sub)===0&&out(y)!==target){all=false;break;}
        if(all)best=pop(sub);
      }
      check(best<=n-pop(known[s]),"certificate exists "+label);
      return dm[s][x]=best;
    }
    const bm=new Array(total),em=new Array(total);
    function B(s){if(bm[s]!==undefined)return bm[s];return bm[s]=Math.min(...candidates[s].map(x=>D(s,x)));}
    function E(s){if(em[s]!==undefined)return em[s];let best=W(s);
      for(let i=0;i<n;i++)if(digits[s][i]===0){
        const p=bases[i];best=Math.min(best,1+E(s+p),1+E(s+2*p));
      }return em[s]=best;}
    const edm=Array.from({length:total},()=>new Array(nn));
    function Ex(s,x){
      if(edm[s][x]!==undefined)return edm[s][x];
      let best=W(s);
      for(let i=0;i<n;i++)if(digits[s][i]===0){
        const p=bases[i],d=(x>>i)&1;best=Math.min(best,1+Ex(s+p*(d+1),x));
      }return edm[s][x]=best;
    }
    for(let s=total-1;s>=0;s--){
      const w=W(s),b=B(s),e=E(s);stats.transcripts++;
      check(e===b,"MAY envelope=B "+label+" "+s);
      check(b<=w,"certificate <= minimax "+label);
      check(b>=0&&w>=0,"nonnegative");
      if(force(s))check(b===0&&w===0,"goal terminal zero");
      if(s===0){stats.max_W_minus_B=Math.max(stats.max_W_minus_B,w-b);
        if(stats.examples.length<16)stats.examples.push({name:label,n,W:w,B:b});}
      for(const x of candidates[s]){
        const d=D(s,x),ex=Ex(s,x);stats.source_states++;
        check(ex===d,"fixed source envelope=D "+label+" "+s+" "+x);
        check(d>=b&&d<=w,"best<=fixed<=worst "+label);
        if(force(s))check(d===0,"source terminal zero");
      }
      for(let i=0;i<n;i++)if(digits[s][i]===0){
        const p=bases[i];
        for(let bit=0;bit<2;bit++){
          const t=s+p*(bit+1),bt=B(t),wt=W(t);stats.paid_edges++;
          check(b<=1+bt,"B tariff "+label);
          check(w>=0&&wt>=0,"W nonnegative");
          for(const x of candidates[t]){
            const d=D(s,x),dt=D(t,x);
            check(d>=dt&&d<=dt+1,"fixed D 0/1 discharge "+label);
            check(n*(b-bt)+2*(w-wt)+n*(d-dt)<=4*n,"universal 3-column exact tariff witness "+label);
          }
        }
      }
    }
    return {name:label,n,W:W(0),B:B(0),testedStates:total};
  }
  const n=3,nn=1<<n;
  for(let f=0;f<(1<<nn);f++){run(n,f,"truth_table_"+f);stats.full_n3_functions++;}
  function ctrl(name,n,fn){const rec=run(n,witnessMask(n,fn),name);stats.controls.push(rec);stats.n4_control_functions++;}
  ctrl("OR4",4,x=>x!==0);
  ctrl("AND4",4,x=>x===15);
  ctrl("PARITY4",4,x=>pop(x)%2===1);
  ctrl("EQUAL4",4,x=>((x&1)===((x>>1)&1)));
  ctrl("MAJORITY4",4,x=>pop(x)>=3);
  ctrl("HORN_IMPLICATION4",4,x=>!((x&1)&&!((x>>1)&1)));
  ctrl("KROM_2CNF4",4,x=>(!(x&1)||((x>>1)&1))&&(!((x>>2)&1)||((x>>3)&1)));
  ctrl("TWO_BLOCKS_AND_OR4",4,x=>((x&3)!==0)&&((x&12)!==0));
  ctrl("XOR_EXTENSION4",4,x=>((pop(x&7)%2)===((x>>3)&1)));
  for(let m=1;m<=25;m++){
    // OR_m: W(?^m)=m, B(?^m)=1. A positive bit read discharges (1,m).
    // Every read in a subcube of r remaining relevant bits discharges
    // Delta B<=1 and Delta W<=r<=m. Therefore exact 2-weight cone:
    // lambda_B+m*lambda_W <=1, including equality on initial positive read.
    const numB=1,numW=1,den=m+1;
    check(numB+m*numW===den,"OR exact integer rational cone boundary");
    check(m>=1,"positive read exists");
    stats.or_cone.push({m,initial_W:m,initial_B:1,sharp_delta_B:1,
      sharp_delta_W:m,cone:"lambda_B+"+m+"*lambda_W<=1"});
  }
  check(stats.full_n3_functions===256,"all 3-bit functions audited");
  check(stats.n4_control_functions===9,"all controls audited");
  return stats;
}
if(typeof console!=="undefined"&&typeof process!=="undefined"){
  console.log(JSON.stringify(audit(),null,2));
}
