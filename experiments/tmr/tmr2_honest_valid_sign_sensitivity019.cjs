// TMR-2/019: honest-encoding valid-neighbor sign sensitivity, reproducible hosted V8.
// One fixed explicit encoding: 1^n 0 1^c 0 followed by c triples of (w-bit id, sign).
// w=ceil(log2(n+1)); ids in 1..n; sign 1 positive, 0 negative.
// Three DIFFERENT IDs required inside each clause. Malformed strings are rejected.
"use strict";
function assert(q,msg){if(!q)throw Error(msg);}
function width(n){return Math.ceil(Math.log2(n+1));}
function enc(n,cs){
  let out='1'.repeat(n)+'0'+'1'.repeat(cs.length)+'0';
  const w=width(n);
  for(const c of cs){assert(c.length===3&&new Set(c.map(a=>a[0])).size===3,'nonproper');
    for(const [id,sgn] of c){assert(id>=1&&id<=n,'id');out+=id.toString(2).padStart(w,'0')+String(sgn);}}
  return out;
}
function dec(s){
  if(typeof s!=='string'||!/^[01]+$/.test(s))return null;
  let p=0;while(p<s.length&&s[p]==='1')p++;
  const n=p;if(n<3||p>=s.length)return null;p++;
  let c=0;while(p<s.length&&s[p]==='1'){c++;p++;}
  if(p>=s.length)return null;p++;
  const w=width(n);if(s.length-p!==3*(w+1)*c)return null;
  const out=[];
  for(let j=0;j<c;j++){const clause=[];
    for(let t=0;t<3;t++){
      const id=parseInt(s.slice(p,p+w),2);p+=w;
      const sign=Number(s[p++]);
      if(id<1||id>n)return null;clause.push([id,sign]);
    }
    if(new Set(clause.map(a=>a[0])).size!==3)return null;
    out.push(clause);
  }
  return {n,clauses:out};
}
function force(v,pol,u,w){
  const out=[];
  for(const a of [0,1])for(const b of [0,1])
    out.push([[v,pol],[u,a],[w,b]]);
  return out;
}
function family(m){
  assert(Number.isInteger(m)&&m>=1,'m');
  let out=[...force(1,1,4,5),...force(2,0,6,7),...force(3,0,8,9)];
  for(let j=0;j<m;j++)out.push([[2,1],[3,1],[1,1]]);
  return out;
}
function brute(cs,n=9){
  for(let mask=0;mask<(1<<n);mask++){
    if(cs.every(c=>c.some(([id,sgn])=>(((mask>>(id-1))&1)===sgn))))return true;
  }
  return false;
}
const Pos=Array(10).fill(0n);
for(let v=1;v<=9;v++)for(let a=0;a<512;a++)
  if((a>>(v-1))&1)Pos[v]|=1n<<BigInt(a);
const All=(1n<<512n)-1n;
function bitset(cs){
  let x=All;
  for(const c of cs){let q=0n;
    for(const [v,sgn] of c)q|=(sgn?Pos[v]:(All^Pos[v]));
    x&=q;
  }
  return x!==0n;
}
function rename(cs,p){return cs.map(c=>c.map(([v,s])=>[p[v],s]));}
function run(){
  const sizes=[1,2,3,4,5,8,12,17,24,32,48];
  const counts={base_cases:0,valid_opposite_neighbors:0,solver_agreements:0,
    renamed_cases:0,malformed_controls:0,horn_controls:0,xor_controls:0,
    max_length:0,max_clauses:0,last_pivot_is_final_bit:0,independently_forced_tests:0};
  let lastSamples=[],seed=0xC0FFEE;
  function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
  function solveTest(cs,expected){
    const b=brute(cs),v=bitset(cs);
    assert(b===v,'independent solvers disagree');
    assert(b===expected,'incorrect expected SAT');
    counts.solver_agreements++;
  }
  for(let m of sizes){
    const cs=family(m),s=enc(9,cs),parsed=dec(s),L=s.length;
    assert(parsed&&enc(parsed.n,parsed.clauses)===s,'roundtrip');
    assert(L===203+16*m,'exact length');
    solveTest(parsed.clauses,true);counts.base_cases++;
    counts.max_length=Math.max(counts.max_length,L);
    counts.max_clauses=Math.max(counts.max_clauses,cs.length);
    const positions=new Set();
    for(let j=0;j<m;j++){
      const mutated=cs.map(c=>c.map(a=>a.slice()));mutated[12+j][2][1]=0;
      const alt=enc(9,mutated);let diff=[];
      for(let i=0;i<L;i++)if(s[i]!==alt[i])diff.push(i+1);
      assert(diff.length===1,'not single bit');
      const pos=diff[0];assert(pos===L-15*(m-1-j),'wrong pivot sign cell');
      positions.add(pos);
      assert(dec(alt)!==null,'neighbor malformed');
      solveTest(dec(alt).clauses,false);
      counts.valid_opposite_neighbors++;
      if(j===m-1){assert(pos===L,'last input bit not sensitive');counts.last_pivot_is_final_bit++;}
    }
    assert(positions.size===m,'not independent singletons');
    lastSamples.push({m,L,pivotal_sign_positions:positions.size,last_pivot_position:L,
       sensitivity_fraction:m/L});
    for(let rep=0;rep<3;rep++){
      const order=Array.from({length:10},(_,i)=>i);
      for(let i=9;i>1;i--){const j=1+rnd()%i;[order[i],order[j]]=[order[j],order[i]];}
      const newcs=rename(cs,order);
      assert(dec(enc(9,newcs))!==null,'renaming malformed');
      solveTest(newcs,true);counts.renamed_cases++;
      const j=rnd()%m,newbad=newcs.map(c=>c.map(a=>a.slice()));
      newbad[12+j][2][1]=0;solveTest(newbad,false);counts.renamed_cases++;
    }
    for(let bad of [s+'1',s.slice(0,-1),s.slice(0,10)+'0'+s.slice(11),s.replace(/^1/,'0')]){
      assert(dec(bad)===null,'malformed accepted');counts.malformed_controls++;
    }
  }
  // Independent exhaustive proof of each 4-clause force gadget.
  for(let pol of [0,1])for(let mask=0;mask<8;mask++){
    let cl=force(1,pol,2,3);
    let result=cl.every(c=>c.some(([v,s])=>(((mask>>(v-1))&1)===s)));
    assert(result===(((mask&1)!==0)===(pol===1)),'force gadget failure');
    counts.independently_forced_tests++;
  }
  // Three-variable parity (XOR) encoding. Four clauses forbid the opposite parity assignments.
  for(let want of [0,1]){
    const parityClauses=[];
    for(let mask=0;mask<8;mask++){
      const parity=(((mask&1)!==0)+(((mask>>1)&1)!==0)+(((mask>>2)&1)!==0))%2;
      if(parity!==want)parityClauses.push([1,2,3].map(v=>[v,1-((mask>>(v-1))&1)]));
    }
    assert(parityClauses.length===4,'xor count');
    for(let mask=0;mask<8;mask++){
      const parity=(((mask&1)!==0)+(((mask>>1)&1)!==0)+(((mask>>2)&1)!==0))%2;
      const sat=parityClauses.every(c=>c.some(([v,s])=>(((mask>>(v-1))&1)===s)));
      assert(sat===(parity===want),'xor truth table');
      counts.xor_controls++;
    }
  }
  const horn=[[[1,0],[2,0],[3,1]],[[1,1],[4,0],[5,0]]];
  solveTest(horn,true);counts.horn_controls++;
  return {run_id:"TMR2-019",timestamp_pst:"2026-11-14 05:12 PST",
    encoding:"unary n and clause count; three fixed-width (id,sign) fields per proper clause; n=9, w=4",
    formula:"L=203+16m; m pairwise disjoint SINGLE-bit valid SAT->UNSAT neighbors; last pivotal bit at L",
    counts,samples:lastSamples,assertions_failed:0,
    caveat:"Hosted V8 mathematical/encoding experiments, not a compiled physical TM executor; brute-force and BigInt bitset independently agree."};
}
const RESULT = run();
if (typeof console !== 'undefined' && console.log) console.log(JSON.stringify(RESULT,null,2));
RESULT;