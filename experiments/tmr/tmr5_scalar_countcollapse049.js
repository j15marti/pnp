"use strict";
const result = (function reproduce() {
  "use strict";
  let checks=0, uniqueTests=0, circuitPairs=0, totalFormulas=0, fullAssignments=0;
  const ensure=(p,msg)=>{checks++;if(!p)throw Error(msg)};
  const val=(lit,a)=>lit>0?!!a[lit]:!a[-lit];
  const sat=(cs,a)=>cs.every(c=>c.some(l=>val(l,a)));
  const evalLit=(lit,a)=>val(lit,a);
  function makeComparator(n,K){
    const limit=1<<n;
    let clauses=[],gates=[],V=n,output=null;
    if(K===0){clauses.push([1],[-1])}
    else if(K!==limit){
      let j=0;while(((K>>j)&1)===0)j++;
      output=-(j+1);
      for(let i=j+1;i<n;i++){
        const a=-(i+1), b=output, z=++V;
        const op=((K>>i)&1)===1?"OR":"AND";
        if(op==="AND")clauses.push([-z,a],[-z,b],[z,-a,-b]);
        else clauses.push([z,-a],[z,-b],[-z,a,b]);
        gates.push({type:op,out:z,a,b});
        output=z;
      }
      clauses.push([output]);
    }
    const mentioned=new Set(clauses.flat().map(Math.abs));
    for(let i=1;i<=n;i++){
      if(!mentioned.has(i)){
        const z=++V;
        clauses.push([-z,i],[z,-i]);
        gates.push({type:"COPY",out:z,a:i});
      }
    }
    const pinA=++V,pinB=++V,pinC=++V;
    let strict=clauses.map(c=>c.length===1?[...c,pinA,pinB]:c.length===2?[...c,pinA]:c.slice());
    for(let m=1;m<8;m++){
      strict.push([pinA,pinB,pinC].map((v,j)=>((m>>j)&1)?-v:v));
    }
    function extension(x){
      const values=Array(V+1).fill(false);
      for(let i=1;i<=n;i++)values[i]=!!((x>>(i-1))&1);
      for(const g of gates){
        if(g.type==="COPY")values[g.out]=evalLit(g.a,values);
        else if(g.type==="AND")values[g.out]=evalLit(g.a,values)&&evalLit(g.b,values);
        else values[g.out]=evalLit(g.a,values)||evalLit(g.b,values);
      }
      return values;
    }
    return {n,K,V,strict,gates,extension};
  }
  for(let n=1;n<=7;n++){
    for(let K=0;K<=(1<<n);K++){
      const F=makeComparator(n,K);totalFormulas++;
      ensure(F.V<=2*n+3,"V budget n="+n+" K="+K);
      ensure(F.strict.length<=3*n+7,"clause budget n="+n+" K="+K);
      ensure(F.strict.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"strict proper clauses");
      ensure(new Set(F.strict.map(c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(","))).size===F.strict.length,"nodup");
      const occurring=new Set(F.strict.flat().map(Math.abs));
      ensure(occurring.size===F.V,"all occur");
      let cnt=0;
      for(let x=0;x<(1<<n);x++){
        const a=F.extension(x), accepted=sat(F.strict,a);
        ensure(accepted===(x<K),"comparator semantic n="+n+" K="+K+" x="+x);
        if(accepted){
          cnt++;
          for(let v=n+1;v<=F.V;v++){
            a[v]=!a[v];ensure(!sat(F.strict,a),"unique extension");a[v]=!a[v];uniqueTests++;
          }
        }
      }
      ensure(cnt===K,"exact count");
      if(n<=3){
        let exhaustive=0;
        for(let mask=0;mask<(1<<F.V);mask++){
          let a=Array(F.V+1).fill(false);for(let i=1;i<=F.V;i++)a[i]=!!((mask>>(i-1))&1);
          if(sat(F.strict,a))exhaustive++;
          fullAssignments++;
        }
        ensure(exhaustive===K,"full count brute");
      }
    }
  }
  const family=[];
  for(let k=2;k<=4;k++){
    const n=k+2,r=1<<k,half=r/2,limit=(1<<r);
    let count=0, seen=new Set(),sharedK=half,different=false, prior="";
    for(let S=0;S<limit&&count<(k===4?96:100000);S++){
      let pop=0;for(let j=0;j<r;j++)pop+=(S>>j)&1;
      if(pop!==half)continue;
      const signature=[];
      let sourceCount=0,shortcutCount=0;
      for(let x=0;x<(1<<n);x++){
        let f=(((x>>k)===(1<<(n-k))-1)&&(((S>>(x&((1<<k)-1)))&1)!==0));
        let h=true;for(let i=k-1;i<n;i++)h&&=!!((x>>i)&1);
        if(f)sourceCount++;if(h)shortcutCount++;
        signature.push(f?"1":"0");
      }
      ensure(sourceCount===half&&shortcutCount===half,"same count");
      const sig=signature.join("");
      ensure(!seen.has(sig),"distinct pointwise functions");
      if(prior&&prior!==sig)different=true;prior=sig;seen.add(sig);count++;
      circuitPairs++;
    }
    ensure(different,"nontrivial family");
    family.push({k,n,r,half,distinctFunctionsChecked:count,commonExactCount:half,shortcut:"AND(x_k,...,x_n)",CNF_original_variables:n,original_cheap_clauses:n-k+1});
  }
  return {revision:"tmr5_scalar_countcollapse049_v1",seed:"none",runtime:"hosted V8 ECMAScript",tests:{assertions:checks,genericComparatorCNFs:totalFormulas,fullyEnumeratedAuxiliaryAssignments:fullAssignments,uniqueAuxiliaryBitFlips:uniqueTests,familyDistinctFunctionsChecked:circuitPairs},bounds:{generic_strict_3CNF_variables:"V<=2n+3",generic_strict_3CNF_clauses:"m<=3n+7",count_range:"0<=K<=2^n",family_shortcut_count:"r/2 for every S of size r/2"},family,failures:0};
})();
console.log(JSON.stringify(result,null,2));
