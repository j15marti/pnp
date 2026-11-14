function runAudit() {
  const check = (ok, where) => { stats.assertions++; if (!ok) throw new Error(where); };
  const stats = {assertions: 0, formulas: 0, truth_tables: 0, evaluated_bits: 0, sat_formulas: 0, unsat_formulas: 0, zero_gate_rejections: 0, maximal_slack: 0};
  const makeClauses = v => {
    const out = [];
    for (let a=0;a<v;a++) for(let b=a+1;b<v;b++) for(let c=b+1;c<v;c++)
      for(let mask=0;mask<8;mask++) out.push([[a,mask&1],[b,(mask>>1)&1],[c,(mask>>2)&1]]);
    return out;
  };
  const directF = (clauses, mask) => clauses.every(clause =>
    clause.some(([variable,negative]) => (((mask>>variable)&1) ^ negative) === 1)
  );
  const compile = (v, clauses, t) => {
    const n=v+t, gates=[], negative={};
    const gate=(op,a,b=null)=>{const index=n+gates.length; gates.push({op,a,b});return index;};
    const literals=clause=>clause.map(([variable,neg])=>{
      if(!neg)return variable;
      if(negative[variable]===undefined)negative[variable]=gate("NOT",variable);
      return negative[variable];
    });
    let root=null;
    for(const clause of clauses){
      const ls=literals(clause);
      const node=gate("OR",gate("OR",ls[0],ls[1]),ls[2]);
      root=root===null?node:gate("AND",root,node);
    }
    for(let j=0;j<t;j++)root=gate("AND",root,v+j);
    return {n,gates,root};
  };
  const evalCircuit=(c,mask)=>{
    const values=Array.from({length:c.n},(_,i)=>(mask>>i)&1);
    for(const g of c.gates) values.push(g.op==="NOT"?(1-values[g.a]):g.op==="OR"?(values[g.a]|values[g.b]):(values[g.a]&values[g.b]));
    return values[c.root];
  };
  const zeroGate=(table,n)=>{
    const N=1<<n;
    for(const constant of [0,1])if(table.every(x=>x===constant))return true;
    for(let k=0;k<n;k++){
      if(table.every((bit,i)=>bit===((i>>k)&1)))return true;
    }
    return false;
  };
  const formulaCases=[];
  for(const v of [3,4,5]){
    const universe=makeClauses(v);
    const maxM=v===3?3:v===4?2:1;
    for(let m=1;m<=maxM;m++){
      const build=(prefix,depth)=>{
        if(depth===m){formulaCases.push({v,clauses:prefix});return;}
        for(const clause of universe)build(prefix.concat([clause]),depth+1);
      };
      build([],0);
    }
    if(v===3){
      for(let omitted=0;omitted<8;omitted++)
        formulaCases.push({v,clauses:universe.filter((_,i)=>i!==omitted)});
      formulaCases.push({v,clauses:universe});
    }
  }
  for(const {v,clauses} of formulaCases){
    stats.formulas++;
    const satCount=Array.from({length:1<<v},(_,x)=>Number(directF(clauses,x))).reduce((a,b)=>a+b,0);
    if(satCount>0)stats.sat_formulas++;else stats.unsat_formulas++;
    for(const t of [2,3]){
      const c=compile(v,clauses,t),n=v+t,N=1<<n;
      const upper=v+3*clauses.length+t-1;
      check(c.gates.length<=upper,"gate upper count");
      stats.maximal_slack=Math.max(stats.maximal_slack,upper-c.gates.length);
      const table=[];
      for(let x=0;x<N;x++){
        const direct=Number(directF(clauses,x&((1<<v)-1)) && ((x>>v)&((1<<t)-1))===((1<<t)-1));
        const compiled=evalCircuit(c,x);
        check(direct===compiled,"independent compilation equality");
        table.push(compiled);stats.evaluated_bits++;
      }
      const weight=table.reduce((a,b)=>a+b,0);
      check(weight===satCount,"Hamming weight equals number of source solutions");
      check((weight===0)===(satCount===0),"both labels");
      const hasZeroGate=zeroGate(table,n);
      check(hasZeroGate===(satCount===0),"MCSP[0] exact classification");
      if(satCount>0){stats.zero_gate_rejections++;check(weight>0&&weight<=N/(1<<t),"positive and sparse");}
      if(satCount===1)check(weight/N===1/N,"unique witness exact Hamming density");
      stats.truth_tables++;
    }
  }
  const crossings=[];
  for(const m of [7,8,64]){
    let first=null;
    for(let t=2;t<=256;t++){
      const v=3,n=v+t,B=BigInt(v+3*m+t-1);
      const clear=(1n<<BigInt(n))>=B**10n;
      if(clear&&first===null)first=t;
      if(first!==null)check(clear,"monotonic crossing after first");
    }
    check(first!==null,"threshold crossing exists");
    const t=first,n=3+t,B=3+3*m+t-1;
    crossings.push({source_variable_count:3,clauses:m,mask_variables:t,truth_table_arity:n,output_length_as_power_of_two:`2^${n}`,gate_upper_bound:B,mu:"1/10",verified_by_integer_inequality:`2^${n} >= ${B}^10`});
  }
  check(stats.unsat_formulas>=1,"explicit UNSAT control");
  return {status:"COMPUTATIONAL", execution:"hosted V8, exact executable JS source, not physical Turing machine", parameters:{source_variables:[3,4,5],full_ordered_clause_sequences:{v3_max_m:3,v4_max_m:2,v5_max_m:1},additional_v3_unique_witness:8,additional_v3_unsat:1,mask_lengths:[2,3],randomness:"none"},stats,crossings,failures:0,scope:"3-distinct-variable clauses; AND/OR/NOT gates, free constants/input wires, shared unary negations; complete truth table directly checked; positive-power crossings are arithmetic only"};
}

const result=runAudit();
if(typeof process!== 'undefined')process.stdout.write(JSON.stringify(result,null,2)+'\n');
