"use strict";
function run050(){
  "use strict";
  let state=0x0502026>>>0, assertions=0, cases=0, assignmentsChecked=0, totalCNFSolutions=0, totalCircuitSolutions=0;
  const samples=[];
  function check(b,msg){assertions++;if(!b)throw Error(msg)}
  function rand(k){state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%k}
  function make(n,g){
    const gates=[];
    for(let j=0;j<g;j++){
      const op=["AND","OR","NOT"][rand(3)];
      const a=1+rand(n+j),b=op==="NOT"?null:1+rand(n+j);
      gates.push({op,a,b});
    }
    return gates;
  }
  function compiled(n,gates){
    const g=gates.length, clauses=[], output=n+g;
    for(let i=0;i<g;i++){
      const z=n+i+1,{op,a,b}=gates[i];
      if(op==="AND")clauses.push([-z,a],[-z,b],[z,-a,-b]);
      else if(op==="OR")clauses.push([z,-a],[z,-b],[-z,a,b]);
      else if(op==="NOT")clauses.push([-z,-a],[z,a]);
      else throw Error("bad operator");
    }
    clauses.push([output]);
    const seen=new Set(clauses.flat().map(Math.abs));
    for(let i=1;i<=n;i++)if(!seen.has(i))clauses.push([i,-i]);
    const unique=new Map();
    for(const c of clauses){
      const d=[...new Set(c)].sort((a,b)=>a-b),key=d.join(",");
      unique.set(key,d);
    }
    return [...unique.values()];
  }
  function evalCircuit(n,gates,x){
    let v=Array(n+gates.length+1).fill(false);
    for(let i=0;i<n;i++)v[i+1]=!!(x&(1<<i));
    gates.forEach(({op,a,b},j)=>{
      const A=v[a],B=b===null?false:v[b];
      v[n+j+1]=op==="AND"?A&&B:op==="OR"?A||B:!A;
    });
    return v[n+gates.length];
  }
  function evalCNF(cnf,bits){
    for(const clause of cnf){
      let sat=false;
      for(const lit of clause){
        const value=!!(bits&(1<<(Math.abs(lit)-1)));
        if(lit>0?value:!value){sat=true;break}
      }
      if(!sat)return false;
    }
    return true;
  }
  function test(n,gates,tag){
    const g=gates.length,cnf=compiled(n,gates),V=n+g,B=Math.floor(Math.log2(2*V))+1;
    check(g>=1&&V<=20,"size");
    check(cnf.length>=2&&cnf.length<=3*g+1+n,"clause bound");
    check(cnf.every(c=>c.length<=3),"width");
    check(new Set(cnf.map(c=>c.join(","))).size===cnf.length,"nodup");
    check(new Set(cnf.flat().map(Math.abs)).size===V,"all occur");
    let satOriginal=0,satCNF=0;
    for(let x=0;x<(1<<n);x++)if(evalCircuit(n,gates,x))satOriginal++;
    for(let z=0;z<(1<<V);z++)if(evalCNF(cnf,z))satCNF++;
    assignmentsChecked+=(1<<V);
    check(satOriginal===satCNF,"parsimonious count "+tag);
    const serializedBits=3+1+V+1+3*B*cnf.length;
    check(serializedBits<=5+V+3*B*(3*g+1+n),"encoding length bound");
    cases++;totalCNFSolutions+=satCNF;totalCircuitSolutions+=satOriginal;
    if(samples.length<6)samples.push({tag,n,g,m:cnf.length,count:satCNF,bits:serializedBits,gates,cnf});
    return {n,g,m:cnf.length,sat:satCNF};
  }
  for(let n=2;n<=4;n++)for(let g=1;g<=5;g++)for(let j=0;j<32;j++)test(n,make(n,g),`n${n}g${g}case${j}`);
  function disj(k){
    const n=2*k,gates=[],terms=[];
    function gate(op,a,b=null){gates.push({op,a,b});return n+gates.length}
    for(let i=0;i<k;i++){const both=gate("AND",i+1,k+i+1);terms.push(gate("NOT",both));}
    let out=terms[0];for(let i=1;i<terms.length;i++)out=gate("AND",out,terms[i]);
    return {n,gates};
  }
  for(let k=1;k<=3;k++){
    const a=disj(k),r=test(a.n,a.gates,"DISJ_"+k);
    check(r.sat===Math.pow(3,k),"DISJ truth table");
  }
  const xor={n:2,gates:[{op:"OR",a:1,b:2},{op:"AND",a:1,b:2},{op:"NOT",a:4,b:null},{op:"AND",a:3,b:5}]};
  const xorR=test(xor.n,xor.gates,"XOR2");
  check(xorR.sat===2,"XOR2 count");
  const budget=[];
  for(const n of [64,1024,65536,1048576]){
    for(const mode of ["linear","n_log04","n_sqrtlog","quadratic"]){
      const L=Math.log2(n),g=Math.floor(mode==="linear"?n:mode==="n_log04"?n*Math.pow(L,.4):mode==="n_sqrtlog"?n*Math.sqrt(L):n*n);
      const V=n+g, m=3*g+1+n, Em=3*m/Math.sqrt(Math.log2(Math.max(m,2)));
      const En=9*V*Math.log2(Math.log2(Math.max(V,4)))/Math.sqrt(Math.log2(Math.max(V,4)));
      budget.push({n,g,mode,log2_runtime_upper_coefficient_one:Math.min(Em,En),ratio_to_n:Math.min(Em,En)/n});
    }
  }
  check(cases===484,"case count");
  return {schema:"tmr1_050_v1",seed:"0x0502026",runtime:"V8",model:"topological fan-in-two AND/OR/NOT circuits, functional Tseitin width <=3 and all-occurring variables",method:"exact exhaustive finite enumeration, no SAT algorithm claim",cases,assignmentsChecked,assertions,totalCircuitSolutions,totalCNFSolutions,failures:0,samples,budget,source_refs:{openai_commit:"4eaee87548250b2682affda7d05d947c05554bae",anthropic_commit:"16a5ce41304fcdaea4e0be7c132e1c361dc26da5"},limitations:["exponential complete enumeration for small circuits only","numerical exponent coefficients set to 1 solely for scale; theorem's real constant is unknown","no empirical verification of the October 2026 counting algorithms","no unconditional circuit lower bound"]};
}
console.log(JSON.stringify(run050(),null,2));
