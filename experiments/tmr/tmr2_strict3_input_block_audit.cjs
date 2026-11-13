/* TMR-2 strict-3CNF equality/block-sensitivity regression. Node.js >=18, no packages. */
function audit(){
  const check=(cond,msg)=>{if(!cond)throw Error(msg);};
  function make(a,b){
    const n=a.length,N=5*n,M=8*n,w=Math.max(1,Math.ceil(Math.log2(N)));
    const clauses=[],blocks=[],head="1".repeat(N)+"0"+"1".repeat(M)+"0";
    for(const [side,bits,off] of [["prefix",a,n],["suffix",b,3*n]]){
      for(let i=0;i<n;i++){
        const start=clauses.length,sign=bits[i]?0:1,p=off+2*i,q=p+1;
        for(const [ps,qs] of [[0,0],[0,1],[1,0],[1,1]])clauses.push([[sign,i],[ps,p],[qs,q]]);
        blocks.push({side,i,start});
      }
    }
    const binary=head+clauses.map(c=>c.map(([sg,id])=>sg+id.toString(2).padStart(w,"0")).join("")).join("");
    const positions={};
    for(const {side,i,start} of blocks)positions[`${side}_${i}`]=Array.from({length:4},(_,d)=>head.length+(start+d)*3*(1+w));
    check(binary.length===13*n+2+24*n*(1+w),"encoded length");
    return {binary,clauses,positions,N,M,w};
  }
  const evalCNF=(cls,mask)=>cls.every(c=>c.some(([sg,id])=>(((mask>>id)&1)^sg)===1));
  function sat(cls,vars){for(let mask=0;mask<2**vars;mask++)if(evalCNF(cls,mask))return true;return false;}
  const stats=[];let checkedGadgets=0;
  for(let n=1;n<=5;n++){
    let pairs=0,brute=0,flips=0,satPairs=0,sourceLen=null;
    for(let x=0;x<2**n;x++){
      const a=Array.from({length:n},(_,i)=>(x>>i)&1);
      for(let y=0;y<2**n;y++){
        const b=Array.from({length:n},(_,i)=>(y>>i)&1);
        const f=make(a,b);if(sourceLen===null)sourceLen=f.binary.length;
        check(f.binary.length===sourceLen,"pair length");
        check(f.clauses.every(c=>c.length===3 && new Set(c.map(p=>p[1])).size===3),"proper clause");
        for(const [side,bits,off,base] of [["prefix",a,n,0],["suffix",b,3*n,4*n]]){
          for(let i=0;i<n;i++){
            const pos=f.positions[`${side}_${i}`],cl=f.clauses.slice(base+4*i,base+4*i+4);
            check(pos.length===4 && new Set(pos).size===4,"sign positions");
            check(pos.every(j=>f.binary[j]===(bits[i]?"0":"1")),"encoded sign");
            for(let xb=0;xb<2;xb++)for(let pb=0;pb<2;pb++)for(let qb=0;qb<2;qb++){
              const mask=(xb<<i)|(pb<<(off+2*i))|(qb<<(off+2*i+1));
              check(evalCNF(cl,mask)===(xb===bits[i]),"gadget truth table");
              checkedGadgets++;
            }
          }
        }
        if(n<=2){check(sat(f.clauses,5*n)===(x===y),"brute force formula label");brute++;}
        if(x===y)satPairs++;pairs++;
      }
      const baseline=make(a,a);
      for(const side of ["prefix","suffix"])for(let i=0;i<n;i++){
        const alt=a.slice();alt[i]^=1;
        const changed=side==="prefix"?make(alt,a):make(a,alt);
        const d=[];for(let j=0;j<baseline.binary.length;j++)if(baseline.binary[j]!==changed.binary[j])d.push(j);
        const required=baseline.positions[`${side}_${i}`];
        check(JSON.stringify(d)===JSON.stringify(required),"opposite label 4-bit sensitive block");
        if(n<=2)check(!sat(changed.clauses,5*n),"opposite label brute");
        flips++;
      }
    }
    stats.push({n,variables:5*n,clauses:8*n,input_bits:sourceLen,pairs_checked:pairs,brute_formula_cases:brute,sat_equal_pairs:satPairs,opposite_label_block_flips:flips});
  }
  return {test:"TMR2_STRICT3_INPUT_BLOCK_001",status:"COMPUTATIONAL finite verification only",method:"deterministic complete pair enumeration n=1..5; independent local gadget truth tables; brute force full CNFs n<=2; same-length four-sign-bit deltas; no randomness",stats,totals:{pairs:stats.reduce((s,x)=>s+x.pairs_checked,0),brute:stats.reduce((s,x)=>s+x.brute_formula_cases,0),flips:stats.reduce((s,x)=>s+x.opposite_label_block_flips,0),local_gadget_truth_checks:checkedGadgets},scope:"promise equality family; no unrestricted SAT lower-bound claim"};
}
const fs=require('node:fs');
const result=audit();
const output=process.argv[2] || 'TMR2_STRICT3_INPUT_BLOCK_001.json';
fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result.totals));
