// ARC209 source-lossless firewall: deterministic finite hostile controls.
// Environment: node >=18; run "node ARC209_source_lossless_repro.js".
// No SAT solver, external modules, randomness, or GitHub data required.
"use strict";
function assert(c,m){if(!c)throw new Error(m);}
function make(m,bits,unsat){
  assert(bits.length===m,"length");
  const vars=5*m+(unsat?3:0), clauses=2*m+(unsat?8:0);
  let rows=["p cnf "+vars+" "+clauses];
  for(let i=0;i<m;i++){
    const x=5*i+1,y=x+1,z=x+2,u=x+3,v=x+4;
    const s=bits[i]?-x:x;
    rows.push(s+" "+y+" "+z+" 0");
    rows.push((-s)+" "+u+" "+v+" 0");
  }
  if(unsat){
    const a=5*m+1,b=a+1,c=a+2;
    for(let h=0;h<8;h++){
      const lits=[a,b,c].map((v,j)=>(h&(1<<j))?-v:v);
      rows.push(lits.join(" ")+" 0");
    }
  }
  return rows.join("\n")+"\n";
}
function parse(src){
  const rows=src.trimEnd().split("\n");
  const h=rows.shift().split(" ");
  assert(h.length===4&&h[0]==="p"&&h[1]==="cnf","header");
  const n=+h[2],k=+h[3];
  assert(rows.length===k,"clauses header");
  const cnf=rows.map(r=>{
    const a=r.split(" ").map(Number);
    assert(a.length===4&&a[3]===0&&new Set(a.slice(0,3).map(Math.abs)).size===3,"proper 3cnf");
    for(const v of a.slice(0,3))assert(v!==0&&Math.abs(v)<=n,"literal index");
    return a.slice(0,3);
  });
  return {n,k,cnf};
}
function satUnder(clauses,assignment){
  return clauses.every(row=>row.some(lit=>lit>0?!!assignment[Math.abs(lit)]:!assignment[Math.abs(lit)]));
}
function bytesBitCount(x){return 8*x.length;} // canonical ASCII DIMACS
function brute(p){
  const n=p.n; assert(n<=13,"brute capped");
  for(let mask=0;mask<2**n;mask++){
    const a=Array(n+1).fill(false);
    for(let i=1;i<=n;i++)a[i]=Boolean(mask & (1<<(i-1)));
    if(satUnder(p.cnf,a))return true;
  }
  return false;
}
function run(){
  const summary=[],checks={formulas:0,clauseChecks:0,satWitnesses:0,unsatCoreAssignments:0,bruteTruthChecks:0,uniqueInputs:0};
  for(let m=1;m<=10;m++){
    const known=[new Set(),new Set()],lens=[new Set(),new Set()];
    for(let b=0;b<2**m;b++){
      const bits=Array.from({length:m},(_,i)=>(b>>>i)&1);
      for(let flag=0;flag<=1;flag++){
        const raw=make(m,bits,!!flag),p=parse(raw);
        checks.formulas++;checks.clauseChecks+=p.k;
        assert(p.n===5*m+(flag?3:0)&&p.k===2*m+(flag?8:0),"counts");
        const a=Array(p.n+1).fill(false);
        for(let i=0;i<m;i++)a[5*i+2]=a[5*i+4]=true;
        if(flag){
          const u=5*m+1;
          for(let h=0;h<8;h++){
            for(let j=0;j<3;j++)a[u+j]=Boolean(h&(1<<j));
            assert(!satUnder(p.cnf.slice(-8),a),"8-clause UNSAT core");
            checks.unsatCoreAssignments++;
          }
        }else{
          assert(satUnder(p.cnf,a),"SAT witness");
          checks.satWitnesses++;
        }
        if(m<=2){
          assert(brute(p)===!flag,"full brute truth");checks.bruteTruthChecks++;
        }
        assert(!known[flag].has(raw),"unique formula");
        known[flag].add(raw);checks.uniqueInputs++;
        lens[flag].add(bytesBitCount(raw));
      }
    }
    assert(lens[0].size===1&&lens[1].size===1,"constant bit length across all sign strings");
    summary.push({m,numberPerSide:2**m,satBits:[...lens[0]][0],unsatBits:[...lens[1]][0],sameSizeWithinEachSide:true});
  }
  const pairedToy=new Map();
  for(let b=0;b<128;b++){
    const child=b&15,sidecar=(b>>4)&3;
    const key=child+":"+sidecar;
    pairedToy.set(key,(pairedToy.get(key)||0)+1);
  }
  assert(pairedToy.size===64,"6-bit output count");
  assert([...pairedToy.values()].every(v=>v===2),"7-to-6-bit collisions");
  const big=[];
  for(const m of [64,256,1024,4096]){
    const n=bytesBitCount(make(m,Array(m).fill(0),false));
    big.push({m,Nbits:n,mbitsOverN06:m/n**0.6,mbitsOverN07:m/n**0.7});
  }
  return {status:"COMPUTATIONAL",seed:null,exhaustive:"all 2^m bit strings for m=1..10; brute complete 3CNF SAT for m<=2",summary,checks,toyCollision:{m:7,childBits:4,sidecarBits:2,distinctParents:128,distinctPairs:pairedToy.size,collidingPairs:64},big,scope:"Counts only reversible reconstructions. Does NOT bound lossy answer-preserving SAT compressors or collision-resistant computational bindings."};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
