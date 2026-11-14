'use strict';
function runAudit() {
  const counts={assertions:0,formulas:0,truthTables:0,bitComparisons:0,syntacticBranchOn:0,syntacticBranchOff:0,microMachineCases:0,microMachineBitChecks:0,thresholdChecks:0,negativeControls:0};
  function check(x,where){counts.assertions++; if(!x)throw Error(where);}
  function properClauses(v){let ans=[];for(let a=0;a<v;a++)for(let b=a+1;b<v;b++)for(let c=b+1;c<v;c++)for(let mask=0;mask<8;mask++)ans.push([[a,mask&1],[b,(mask>>1)&1],[c,(mask>>2)&1]]);return ans;}
  function checksum(clauses){let x=clauses.length&1;for(const c of clauses)for(const [_i,neg] of c)x^=neg;return x;}
  function direct(v,clauses,t,k){
    const ok=clauses.every(c=>c.some(([j,neg])=>((((k>>j)&1)^neg)===1)));
    let allZ=true;for(let j=0;j<t;j++)allZ=allZ&&(((k>>(v+j))&1)===1);
    const twist=checksum(clauses)&&((((k&1)===1)||(((k>>v)&1)===1)));
    return Number(Boolean(ok&&allZ)!==Boolean(twist));
  }
  function compiler(v,clauses,t){
    const n=v+t,gates=[],NOT=new Map(),ZERO=-1,ONE=-2;
    function gate(op,a,b){const q=n+gates.length;gates.push({op,a,b});return q;}
    function neg(a){return gate('NOT',a,null);}
    function xor(a,b){return gate('AND',gate('OR',a,b),neg(gate('AND',a,b)));}
    function lit(i,sign){if(!sign)return i;if(!NOT.has(i))NOT.set(i,neg(i));return NOT.get(i);}
    let f=ONE;
    for(const c of clauses){let a=lit(c[0][0],c[0][1]);for(let j=1;j<c.length;j++)a=gate('OR',a,lit(c[j][0],c[j][1]));f=gate('AND',f,a);}
    let full=f;for(let j=0;j<t;j++)full=gate('AND',full,v+j);
    let twist=checksum(clauses)?gate('OR',0,v):ZERO;
    const root=xor(full,twist);
    return {n,root,gates,ZERO,ONE};
  }
  function evaluate(c,k){let bits=Array.from({length:c.n},(_,j)=>(k>>j)&1);function val(id){return id===c.ZERO?0:id===c.ONE?1:bits[id];}
    for(const g of c.gates)bits.push(g.op==='NOT'?1-val(g.a):g.op==='OR'?val(g.a)|val(g.b):val(g.a)&val(g.b));return val(c.root);
  }
  const universe=properClauses(3),formulae=[];
  for(let m=1;m<=3;m++){
    function enumerate(a){if(a.length===m){formulae.push({v:3,cs:a.slice()});return;}
      for(const c of universe)enumerate(a.concat([c]));}
    enumerate([]);
  }
  formulae.push({v:3,cs:universe.slice()});
  for(let k=0;k<8;k++)formulae.push({v:3,cs:universe.filter((_,i)=>i!==k)});
  formulae.push({v:3,cs:universe.filter((_,i)=>((i.toString(2).split('1').length-1)&1)===0)});
  formulae.push({v:3,cs:[[[0,1],[1,1],[2,0]],[[0,0],[1,1],[2,0]]]});
  formulae.push({v:3,cs:[[[0,0],[1,1],[1,1]],[[0,1],[1,0],[1,0]]]});
  formulae.push({v:6,cs:[[[0,0],[1,1],[2,0]],[[3,1],[4,0],[5,1]]]});
  for(const {v,cs} of formulae){
    let branch=checksum(cs);if(branch)counts.syntacticBranchOn++;else counts.syntacticBranchOff++;
    for(const t of [1,2]){
      const c=compiler(v,cs,t),N=2**c.n;
      check(c.gates.length <= v+3*cs.length+t+9,'explicit gate cap');
      const table=[];
      for(let k=0;k<N;k++){
        const a=direct(v,cs,t,k),b=evaluate(c,k);table.push(a);counts.bitComparisons++;check(a===b,'source-bound generated truth-table bit '+JSON.stringify({v,t,k,cs}));
      }
      check(table.length===N,'full target table length');
      counts.truthTables++;
    }
    counts.formulas++;
  }
  function toyMachineCircuit(n,seed){
    const gates=[],Z=-1,O=-2;function gate(op,a,b){let id=n+gates.length;gates.push({op,a,b});return id;}
    const xor=(a,b)=>gate('AND',gate('OR',a,b),gate('NOT',gate('AND',a,b),null));
    let p=seed?O:Z;let heads=Array.from({length:n+1},(_,i)=>i===0?O:Z);
    for(let t=0;t<n;t++){
      let symbol=Z;for(let j=0;j<n;j++)symbol=gate('OR',symbol,gate('AND',heads[j],j));
      p=xor(p,symbol);heads=[Z,...heads.slice(0,n)];
    }
    return {n,root:p,gates,Z,O};
  }
  function evalToy(c,k){let bs=Array.from({length:c.n},(_,j)=>(k>>j)&1);const v=id=>id===c.Z?0:id===c.O?1:bs[id];
    for(const g of c.gates)bs.push(g.op==='NOT'?1-v(g.a):g.op==='OR'?v(g.a)|v(g.b):v(g.a)&v(g.b));return v(c.root);
  }
  for(let n=1;n<=8;n++)for(let seed=0;seed<=1;seed++){
    let c=toyMachineCircuit(n,seed);
    for(let k=0;k<2**n;k++){
      let bit=seed;for(let j=0;j<n;j++)bit^=(k>>j)&1;
      check(bit===evalToy(c,k),'all-step finite-control parity/head simulation');counts.microMachineBitChecks++;
    }
    check(c.gates.length<=8*n*n+10*n,'toy explicit spatial size cap');
    counts.microMachineCases++;
  }
  for(const {v,cs} of [formulae[0],formulae[10],formulae[formulae.length-1]]){
    let found=null;
    for(let t=1;t<=300;t++){
      let c=compiler(v,cs,t),g=BigInt(c.gates.length),n=BigInt(c.n);
      const yes=(2n**n >= g**10n);
      if(yes&&found===null)found=t;
      if(found!==null&&t<=found+6)check(yes,'threshold monotonic after crossing (checked local)');
      counts.thresholdChecks++;check(c.gates.length <= 3*cs.length+v+t+9,'linear hardwired compiler size');
    }
    check(found!==null,'finite crossover exists');
  }
  for(let n=1;n<=4;n++){
    let c=toyMachineCircuit(n,0);
    let vals=new Set();for(let k=0;k<2**n;k++)vals.add(evalToy(c,k));
    check(vals.size===2,'nonconstant truth-table cost cannot be zero');counts.negativeControls++;
  }
  return {status:'COMPUTATIONAL',engine:'ECMAScript V8 finite gate-DAG test, not physical TM compiler',randomness:'none',sourceVariables:[3,6],maskVariables:[1,2],counts,failures:0,scope:'proper 3-CNF formula syntax, duplicated-literal 2-SAT, disjoint-product, Horn, unsat, unique witness, parity clauses; syntax-controlled nonlinear indexed output; finite spatial one-head parity transducer; numeric threshold only at large n'};
}
const result=runAudit();
if(typeof process!=='undefined'&&process.stdout)process.stdout.write(JSON.stringify(result,null,2)+'\n');
