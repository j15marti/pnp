/* LSPV-1 368. Deterministic signed-CNF transfer controls. Node 18+; no dependencies. */
"use strict";
function assert(p,msg){if(!p)throw Error(msg);}
function php(h){
  assert(Number.isInteger(h)&&h>=1&&h<=100,"h");
  const n=h*(h+1), c=[];
  for(let p=1;p<=h+1;p++)c.push(Array.from({length:h},(_,j)=>(p-1)*h+j+1));
  for(let p=1;p<=h+1;p++)for(let q=p+1;q<=h+1;q++)for(let j=1;j<=h;j++)
    c.push([-((p-1)*h+j),-((q-1)*h+j)]);
  return {n,c};
}
function dimacs(f){return "p cnf "+f.n+" "+f.c.length+"\n"+f.c.map(c=>c.join(" ")+" 0\n").join("");}
function parse(s){
  if(typeof s!=="string"||!/^[\x20-\x7E\n]*$/.test(s))return null;
  const lines=s.trimEnd().split("\n"),m=/^p cnf ([1-9][0-9]*) ([0-9]+)$/.exec(lines[0]||"");
  if(!m)return null;
  const n=Number(m[1]),k=Number(m[2]);
  if(!Number.isSafeInteger(n)||!Number.isSafeInteger(k)||k!==lines.length-1)return null;
  const c=[];
  for(let i=1;i<lines.length;i++){
    const z=lines[i].trim().split(/\s+/);
    if(z[z.length-1]!=="0"||z.slice(0,-1).some(t=>!/^(-?[1-9][0-9]*)$/.test(t)))return null;
    const cl=z.slice(0,-1).map(Number);
    if(cl.some(x=>!Number.isSafeInteger(x)||!x||Math.abs(x)>n))return null;
    c.push(cl);
  }
  return {n,c};
}
function satisfies(c,mask){return c.every(cl=>cl.some(x=> ((mask>>(Math.abs(x)-1))&1) === (x>0?1:0)));}
function witness(f){assert(f.n<=16,"finite brute-force only");for(let mask=0;mask<2**f.n;mask++)if(satisfies(f.c,mask))return mask;return null;}
function allRepairs(f){
  const deletion=[], flips=[];
  for(let j=0;j<f.c.length;j++){
    const a=f.c.slice(0,j).concat(f.c.slice(j+1)), w=witness({n:f.n,c:a});
    assert(w!==null,"all source deletions should be SAT");deletion.push(w);
    for(let t=0;t<f.c[j].length;t++){
      const b=f.c.map((cl,k)=>k===j?cl.map((x,i)=>i===t?-x:x):cl),v=witness({n:f.n,c:b});
      assert(v!==null,"all single-sign flips should be SAT");flips.push([j,t,v]);
    }
  }
  return {deletion,flips};
}
function k4(charges){
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], c=[];
  for(let v=0;v<4;v++){
    const ids=edges.map((e,j)=>e.includes(v)?j+1:0).filter(Boolean);
    for(let mask=0;mask<8;mask++){
      const parity=((mask&1)+((mask>>1)&1)+((mask>>2)&1))%2;
      if(parity!==charges[v])c.push(ids.map((x,i)=>((mask>>i)&1)?-x:x));
    }
  }
  return {n:6,c};
}
function models(f){let k=0;for(let mask=0;mask<2**f.n;mask++)if(satisfies(f.c,mask))k++;return k;}
function unitProofOk(src,proof){
  const F=parse(src);if(!F)return false;
  if(proof.a<0||proof.b<0||proof.a>=F.c.length||proof.b>=F.c.length||proof.a===proof.b)return false;
  const A=F.c[proof.a],B=F.c[proof.b],x=proof.pivot;
  if(!Number.isInteger(x)||x<=0||!A.includes(x)||!B.includes(-x))return false;
  const r=[...A.filter(z=>z!==x),...B.filter(z=>z!==-x)];
  if(r.some(z=>r.includes(-z))||JSON.stringify(r)!==JSON.stringify(proof.conclusion))return false;
  return r.length===0;
}
function main(){
  let assertions=0;const check=(p,m)=>{assert(p,m);assertions++;};
  const tests=[];
  for(const h of [1,2,3]){
    const f=php(h),src=dimacs(f),P=parse(src),rep=allRepairs(f);
    check(P!==null,"PHP parses");check(witness(f)===null,"PHP UNSAT");
    check(f.c.length===(h+1)+h*h*(h+1)/2,"PHP clause count");
    check(rep.deletion.length===f.c.length,"deletion count");
    check(rep.flips.length===f.c.reduce((sum,c)=>sum+c.length,0),"flips count");
    tests.push({h,n:f.n,m:f.c.length,bitLength:src.length*8,source:src,...rep});
  }
  const odd=k4([1,0,0,0]),even=k4([0,0,0,0]);
  check(models(odd)===0,"odd K4");check(models(even)===8,"even K4");
  const malformed=["p cnf 1 2\n1 0\n","p cnf 1 1\n2 0\n","p cnf 1 1\n1\n","p cnf 0 0\n","p cnf x 1\n1 0\n"];
  for(let s of malformed)check(parse(s)===null,"malformed rejected");
  const sentinels=[];
  for(let t=1;t<=20;t++){
    const s="p cnf 1 "+t+"\n"+"1 0\n".repeat(t), f=parse(s);
    check(f&&witness(f)===1,"SAT sentinel");
    sentinels.push({t,bitLength:s.length*8,source:s});
  }
  for(let i=1;i<sentinels.length;i++)check(sentinels[i].bitLength-sentinels[i-1].bitLength<=40,"bounded length gaps");
  const units="p cnf 1 2\n1 0\n-1 0\n", proof={a:0,b:1,pivot:1,conclusion:[]};
  check(unitProofOk(units,proof),"valid resolution");
  for(let bad of [{...proof,pivot:2},{...proof,a:1},{...proof,conclusion:[1]}])
    check(!unitProofOk(units,bad),"bad proof rejected");
  const costEnvelopes=tests.map(t=>({
    h:t.h,Nbits:t.bitLength,chargedPHPUpper:(BigInt(t.bitLength)**3n).toString(),
    possibleSentinelDelay:(BigInt(t.bitLength)**8n).toString()
  }));
  return {
    runId:"HARD-PHP-QUERY-EXPONENT-FIREWALL368",timestamp:"2026-11-03 10:55 PST",
    status:"COMPUTATIONAL finite labels only; asymptotic published Haken theorem external",
    assertionGroups:assertions,php:tests,k4:{odd:dimacs(odd),even:dimacs(even),oddModels:models(odd),evenModels:models(even)},
    sentinels,malformed,unit:{source:units,proof},costEnvelopes,
    disclaimer:"N^3 and N^8 are symbolic upper/delay envelopes, not benchmarked native steps."
  };
}
if(typeof require!=="undefined" && require.main===module)console.log(JSON.stringify(main(),null,2));
if(typeof module!=="undefined")module.exports={main};