// TMR5/002, exact binary strict-3CNF suffix-deferral finite regression.
// OS: Node.js >= 18. No dependencies. This is a finite semantic emulator,
// not a physical Turing-machine simulator or a polynomial SAT algorithm.
"use strict";
function audit() {
  const counts={valid_inputs:0, virtual_completions:0, opposite_final_pair:0, malformed_rejected:0, exact_comparisons:0, failures:0, suffix_lengths:[], seed:20261113};
  function check(ok,why){counts.exact_comparisons++;if(!ok){counts.failures++;throw new Error(why);}}
  function width(N){return Math.max(1,Math.ceil(Math.log2(N)));}
  function encode(N,clauses){const w=width(N);return "1".repeat(N)+"0"+"1".repeat(clauses.length)+"0"+clauses.flat().map(([s,i])=>s+Number(i).toString(2).padStart(w,"0")).join("");}
  function parse(s){
    if(typeof s!=="string" || !/^[01]+$/.test(s))return null;
    let k=0;while(k<s.length&&s[k]==="1")k++;
    const N=k;if(k>=s.length||N<3)return null;k++;
    let M=0;while(k<s.length&&s[k]==="1"){M++;k++;}
    if(k>=s.length||M<1)return null;k++;
    const w=width(N),length=k+3*M*(w+1);if(length!==s.length)return null;
    const clauses=[];
    for(let j=0;j<M;j++){let c=[],used=new Set();
      for(let t=0;t<3;t++){const sign=Number(s[k++]);const idx=parseInt(s.slice(k,k+w),2);k+=w;if(idx>=N||used.has(idx))return null;used.add(idx);c.push([sign,idx]);}
      clauses.push(c);
    }
    return {N,M,headerEnd:N+M+2,clauses};
  }
  function satisfiable(s) {
    const p=parse(s);if(!p)return false;
    if(p.N>14)throw Error("Bounded experiment only, not universal SAT solver");
    for(let a=0;a<(1<<p.N);a++){
      let ok=true;
      for(const cl of p.clauses){
        let hit=false;for(const [sg,i] of cl)if((((a>>i)&1)^sg)===1){hit=true;break;}
        if(!hit){ok=false;break;}
      }
      if(ok)return true;
    }return false;
  }
  function spec(s,m){
    const p=parse(s);check(p!==null,"expected valid source");
    const L=s.length;check(m>=1&&m<L-p.headerEnd,"suffix must exclude header");
    const prefix=s.slice(0,L-m), suffix=s.slice(L-m);
    const tbl=[];
    for(let z=0;z<(1<<m);z++){
      const t=z.toString(2).padStart(m,"0");const val=satisfiable(prefix+t);
      tbl.push(val);counts.virtual_completions++;
    }
    let idx=parseInt(suffix.slice(0,-1)||"0",2);
    let finalBit=Number(suffix.slice(-1));
    const pair=[tbl[2*idx],tbl[2*idx+1]];
    check(pair[finalBit]===satisfiable(s),"deferred final-bit selection mismatch");
    check(tbl[parseInt(suffix,2)]===satisfiable(s),"full suffix lookup mismatch");
    counts.valid_inputs++;counts.suffix_lengths.push(m);
  }
  let state=20261113>>>0;
  function next(){state=(Math.imul(state,1664525)+1013904223)>>>0;return state;}
  for(let N=3;N<=5;N++)for(let M=1;M<=3;M++)for(let rep=0;rep<5;rep++){
    const clauses=[];
    for(let j=0;j<M;j++){let ids=Array.from({length:N},(_,i)=>i);
      for(let h=ids.length-1;h>0;h--){let k=next()%(h+1);[ids[k],ids[h]]=[ids[h],ids[k]];}
      clauses.push(ids.slice(0,3).map(i=>[(next()>>>7)&1,i]));
    }
    const s=encode(N,clauses),p=parse(s);
    check(p!==null,"generic generator invalid");
    const m=Math.min(Math.floor(Math.log2(s.length)),Math.max(1,s.length-p.headerEnd-1));
    spec(s,m);
  }
  function force(bit,x,u,v){
    const cl=[];for(let su=0;su<=1;su++)for(let sv=0;sv<=1;sv++)cl.push([[1-bit,x],[su,u],[sv,v]]);return cl;
  }
  for(let n=1;n<=2;n++)for(let a=0;a<1<<n;a++)for(let b=0;b<1<<n;b++){
    const clauses=[];
    for(let side=0;side<2;side++)for(let i=0;i<n;i++){
      const bit=((side===0?a:b)>>i)&1,base=(side===0?n:3*n)+2*i;
      clauses.push(...force(bit,i,base,base+1));
    }
    const s=encode(5*n,clauses),p=parse(s);check(p!==null,"E encoding invalid");
    check(satisfiable(s)===(a===b),"E source label mismatch");
    if(n===1||a===b)spec(s,Math.min(7,Math.floor(Math.log2(s.length))));
  }
  let cnf=[];
  for(const [x,bit,u,v] of [[0,1,6,7],[1,0,8,9],[4,1,10,11],[5,0,12,13]])cnf.push(...force(bit,x,u,v));
  const sat=encode(14,[...cnf,[[1,0],[0,1],[0,4]]]),unsat=encode(14,[...cnf,[[1,0],[0,1],[0,5]]]);
  check(sat.slice(0,-1)===unsat.slice(0,-1),"not same prefix");
  check(satisfiable(sat)===true&&satisfiable(unsat)===false,"opposite pair semantics");
  counts.opposite_final_pair=1;
  spec(sat,1);spec(unsat,1);
  const malformed=["","1","0","1110","11101110",sat.slice(0,-1),sat+"1",sat.replace(/^1/,"0"),"2"];
  for(const s of malformed){check(parse(s)===null,"malformed parsed");counts.malformed_rejected++;}
  counts.suffix_range=[Math.min(...counts.suffix_lengths),Math.max(...counts.suffix_lengths)];
  delete counts.suffix_lengths;
  return counts;
}
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
module.exports={audit};
