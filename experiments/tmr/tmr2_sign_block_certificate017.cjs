"use strict";
// TMR-2/017: executable strict-3CNF clause-sign block certificates
// Run with: node experiments/tmr/tmr2_sign_block_certificate017.cjs
// This is the exact hosted-V8 experiment function executed for publication.
const experiment = function experiment(){
  function gamma(v){if(!Number.isInteger(v)||v<1)throw Error("gamma domain");const s=v.toString(2);return "0".repeat(s.length-1)+s;}
  function make(n){
    const N=2*n+3,clauses=[],types=[],pivot=[];
    for(const [a,b] of [[1,1],[1,-1],[-1,1],[-1,-1]]){clauses.push([1,a*(2*n),b*(2*n+1)]);types.push(["first",0]);pivot.push(1);}
    for(let i=1;i<n;i++){for(const s of [1,-1]){clauses.push([-i,i+1,s*(n+i)]);types.push(["edge",i]);pivot.push(2);}}
    for(const [a,b] of [[1,1],[1,-1],[-1,1],[-1,-1]]){clauses.push([-n,a*(2*n+2),b*(2*n+3)]);types.push(["last",0]);pivot.push(1);}
    if(clauses.length!==2*n+6||clauses.some(c=>new Set(c.map(Math.abs)).size!==3))throw Error("not proper 3CNF");
    return {N,clauses,types,pivot};
  }
  function encode(N,clauses){
    const w=N.toString(2).length;return gamma(N)+gamma(clauses.length)+clauses.map(c=>c.map(l=>Math.abs(l).toString(2).padStart(w,"0")+(l<0?"1":"0")).join("")).join("");
  }
  function decode(bits){
    let i=0;
    function readGamma(){let z=0;while(i<bits.length&&bits[i]==="0"){z++;i++;}if(i+z+1>bits.length)throw Error("bad gamma");const val=parseInt(bits.slice(i,i+z+1),2);i+=z+1;return val;}
    const N=readGamma(),m=readGamma(),w=N.toString(2).length;
    if(bits.length-i!==3*m*(w+1))throw Error("record length");
    const cs=[];
    for(let j=0;j<m;j++){const clause=[];for(let k=0;k<3;k++){const idx=parseInt(bits.slice(i,i+w),2);i+=w;const sign=bits[i++];if(!(idx>=1&&idx<=N))throw Error("index");clause.push(sign==="1"?-idx:idx);}if(new Set(clause.map(Math.abs)).size!==3)throw Error("not proper");cs.push(clause);}
    return {N,cs};
  }
  function holds(clauses,a){return clauses.every(c=>c.some(v=>v>0?!!a[Math.abs(v)]:!a[Math.abs(v)]));}
  function dpll(clauses){
    function reduce(cs,varid,val){const good=val?varid:-varid, bad=-good, out=[];for(const c of cs){if(c.includes(good))continue;const v=c.filter(t=>t!==bad);if(!v.length)return null;out.push(v);}return out;}
    function rec(cs){
      while(true){if(!cs.length)return true;const unit=cs.find(c=>c.length===1);if(!unit)break;cs=reduce(cs,Math.abs(unit[0]),unit[0]>0);if(cs===null)return false;}
      const counts=new Map();for(const c of cs)for(const v of c)counts.set(Math.abs(v),(counts.get(Math.abs(v))||0)+1);
      let vv=null,max=0;for(const [v,count]of counts)if(count>max){vv=v;max=count;}
      for(const val of [true,false]){const t=reduce(cs,vv,val);if(t!==null&&rec(t))return true;}return false;
    }
    return rec(clauses);
  }
  const rows=[];let clauseBlockCases=0,workChecks=0,dpllRuns=0,singletonControls=0,flippedBits=0,parseChecks=0;
  for(let n=1;n<=14;n++){
    const {N,clauses:base,types,pivot}=make(n),m=base.length;
    for(const r of [1,2,3]){
      const original=Array.from({length:r},()=>base.map(c=>c.slice())).flat(),x=encode(N,original);
      if(JSON.stringify(decode(x).cs)!==JSON.stringify(original))throw Error("decode original");parseChecks++;
      if(n<=7){if(dpll(original))throw Error("unsat instance sat");dpllRuns++;}
      for(let j=0;j<m;j++){
        const [kind,idx]=types[j],assignment=Array(N+1).fill(false);
        for(let k=1;k<=n;k++)assignment[k]=kind==="last"||(kind==="edge"&&k<=idx);
        const aux=kind==="first"?[2*n,2*n+1]:kind==="last"?[2*n+2,2*n+3]:[n+idx];
        const alteredClause=base[j].slice();alteredClause[pivot[j]]=-alteredClause[pivot[j]];
        let witness=null;
        for(let a=0;a<1<<aux.length;a++){
          for(let t=0;t<aux.length;t++)assignment[aux[t]]=!!(a&(1<<t));
          if(holds([alteredClause],assignment)&&base.every((c,k)=>k===j||holds([c],assignment))){witness=assignment.slice();break;}
        }
        if(!witness)throw Error(`missing witness n=${n},j=${j}`);
        const yclauses=original.map((c,k)=>k%m===j?alteredClause.slice():c.slice()),y=encode(N,yclauses);
        if(y.length!==x.length||[...x].filter((b,k)=>b!==y[k]).length!==r||!holds(yclauses,witness))throw Error("failed r-bit witness");
        clauseBlockCases++;flippedBits+=r;workChecks+=3;
        if(n<=7){if(!dpll(yclauses))throw Error("DPLL failed SAT witness");dpllRuns++;}
        if(r>=2){
          const one=original.map(c=>c.slice());one[j][pivot[j]]=-one[j][pivot[j]];
          if(!Array.from({length:r},(_,copy)=>copy).some(copy=>base.every((c,k)=>JSON.stringify(one[copy*m+k])===JSON.stringify(c))))throw Error("no untouched copy");
          const z=encode(N,one);if([ ...x].filter((b,k)=>b!==z[k]).length!==1)throw Error("singleton bit change");
          if(n<=7){if(dpll(one))throw Error("singleton should be UNSAT");dpllRuns++;}
          singletonControls++;workChecks+=2;
        }
      }
      const expected=gamma(N).length+gamma(r*m).length+3*r*m*(N.toString(2).length+1);
      if(x.length!==expected)throw Error("length accounting");
      if(n<=3||n>=13)rows.push({n,r,N,m,L:x.length,certificateLowerBound:m,signSensitive:r===1?m:0,disjointBlockSensitivityLowerBound:m});
    }
  }
  return {status:"PASS",scope:"strict proper 3CNF fixed-width signed-variable encoding",nMin:1,nMax:14,replications:[1,2,3],clauseBlockCases,workChecks,parseChecks,dpllRuns,singletonControls,flippedBits,failedAssertions:0,rows};
};
const result = experiment();
console.log(JSON.stringify(result, null, 2));
