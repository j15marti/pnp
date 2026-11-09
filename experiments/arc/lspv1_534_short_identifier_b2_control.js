'use strict';
// LSPV-1/534: independent, finite, source-exact verification of ID-length branching.
// Not a 3-SAT subexponential machine; no R_mix341 or Pang bound is executed here.
function enc(F) {
  return 'cnf\n'+F.map(c=>'c'+(c.length?' '+c.map(x=>(x>0?'+':'-')+Math.abs(x).toString(2)).join(' '):'')+'\n').join('');
}
function parse(s) {
  if(typeof s!=='string'||!s.startsWith('cnf\n')) throw Error('header');
  const body=s.slice(4); if(!body)return [];
  if(!body.endsWith('\n'))throw Error('termination');
  return body.slice(0,-1).split('\n').map(line=>{
    const t=line.split(' ');if(t.shift()!=='c'||t.some(x=>!x))throw Error('clause');
    return t.map(tok=>{
      if(!/^[+-]1[01]*$/.test(tok))throw Error('literal');
      const v=parseInt(tok.slice(1),2);
      if(!Number.isSafeInteger(v)||v<=0)throw Error('unsafe integer');
      return tok[0]==='+'?v:-v;
    });
  });
}
function sat(F) {
  const vars=[...new Set(F.flat().map(Math.abs))];
  if(vars.length>18)throw Error('test bound');
  for(let bits=0;bits<2**vars.length;bits++){
    const a=new Map(vars.map((v,i)=>[v,Boolean(bits & (2**i))]));
    if(F.every(c=>c.some(l=>a.get(Math.abs(l))===(l>0))))return true;
  }
  return false;
}
function simplify(F,a) {
  return F.filter(c=>!c.some(l=>a.has(Math.abs(l))&&a.get(Math.abs(l))===(l>0)))
    .map(c=>[...new Set(c.filter(l=>!a.has(Math.abs(l))))])
    .filter(c=>!c.some(l=>c.includes(-l)));
}
function three(F) {
  const vars=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);
  const map=new Map(vars.map((x,i)=>[x,i+1]));
  let n=vars.length, out=[];
  for(const row of F){
    const c=row.map(l=>(l>0?1:-1)*map.get(Math.abs(l)));
    if(c.length<=3){out.push(c);continue;}
    const k=c.length-3,aux=Array.from({length:k},()=>++n);
    out.push([c[0],c[1],aux[0]]);
    for(let j=1;j<k;j++)out.push([-aux[j-1],c[j+1],aux[j]]);
    out.push([-aux[k-1],c[c.length-2],c[c.length-1]]);
  }
  return {F:out,n};
}
let seed=534;
function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k;}
function check(F){
  const s=enc(F), parsed=parse(s),N=s.length,ln=Math.log2(Math.max(N,4));
  if(JSON.stringify(parsed)!==JSON.stringify(F))throw Error('source');
  const L=Math.max(1,Math.floor(Math.log2(Math.max(2,N/(ln*ln)))));
  const vars=[...new Set(F.flat().map(Math.abs))];
  const short=vars.filter(v=>Math.floor(Math.log2(v))+1<L);
  const q=F.flat().filter(x=>Math.floor(Math.log2(Math.abs(x)))+1>=L).length;
  if(short.length>2**L || q*L>N)throw Error('capacity');
  const truth=sat(F);let found=false,branches=0,maxn=0;
  if(short.length>12)throw Error('finite test capacity');
  for(let bits=0;bits<2**short.length;bits++){
    const a=new Map(short.map((v,j)=>[v,Boolean(bits & (2**j))]));
    const residual=simplify(F,a);
    if(residual.flat().length>q)throw Error('long occurrences');
    const converted=three(residual);
    if(converted.n>2*q||converted.F.some(c=>c.length>3))throw Error('3CNF bound');
    found=found||sat(converted.F);maxn=Math.max(maxn,converted.n);branches++;
  }
  if(truth!==found)throw Error('satisfiability mismatch');
  return {N,L,q,short:short.length,branches,truth,maxn,clauses:F.length};
}
function main(){
  const cases=[
    [],[[]],[[1],[-1]],[[1,2],[-1,2]],[[2,4,8],[-2,-4,-8]],
    [[1,2,4,8,16],[1,-2,4,8,16],[-1,-2,-4,-8,-16]],
    [[1025,2049],[-1025],[-2049]],[[1,2,1048577],[-1,-2,-1048577]],
    [[1,2],[2,-1]],[[-3,3],[7]],[[257,513,1025,2049]],
    [[65537,131073],[-65537,262145],[131073,-262145]]
  ];
  const pool=[1,2,3,4,5,8,16,32,257,1025,1048577,33554437];
  for(let t=0;t<80;t++){
    const selected=[...new Set(Array.from({length:1+rnd(6)},()=>pool[rnd(pool.length)]))];
    const F=[];
    const m=1+rnd(9);
    for(let i=0;i<m;i++){
      const row=[];
      for(let j=0;j<1+rnd(5);j++) {
        const v=selected[rnd(selected.length)];
        if(!row.includes(v)&&!row.includes(-v))row.push(rnd(2)?v:-v);
      }
      F.push(row);
    }
    cases.push(F);
  }
  const results=cases.map(check);
  const invalid=['','CNF\n','cnf\nc +01\n','cnf\nc +0\n','cnf\nc --1\n','cnf\nc +2\n','cnf\nc +1','cnf\n+1\n','cnf\nc +1  -1\n','cnf\nc -\n'];
  let rejected=0;
  for(const bad of invalid){try{parse(bad)}catch(e){rejected++;}}
  if(rejected!==invalid.length)throw Error('invalid accepted');
  return {run:'LSPV1-534-IDCUT-JS-v1',scope:'finite source-equivalence only',configurations:results.length,
    SAT:results.filter(x=>x.truth).length,UNSAT:results.filter(x=>!x.truth).length,
    branches:results.reduce((x,y)=>x+y.branches,0),malformed_rejected:rejected,
    maxN:Math.max(...results.map(x=>x.N)),maxCut:Math.max(...results.map(x=>x.L)),
    max3CNFvars:Math.max(...results.map(x=>x.maxn)),bad_source_executed:true,
    external_subexp_algorithm_executed:false,historical_Rmix341_checker_executed:false,
    all_checks:'PASS'};
}
if(typeof module!=='undefined' && require.main===module)console.log(JSON.stringify(main(),null,2));
