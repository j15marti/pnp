// LSPV-4/530: exact finite paid-value slot search on the K4 /341-/529
// SOURCE/AND3/XOR occurrence DAG. Separate test model, NOT full R_mix341.
// Run: node experiments/arc/lspv4_530_inplace_recompute.mjs
function check(b,m){if(!b)throw Error(m||"assertion failed")}
function graph(k){
  check(Number.isInteger(k)&&k>=0,"k");
  const P=[];
  for(let v=0;v<4;v++){
    let s=4*v,d=3*v;
    P.push([-s-1,-s-2],[d,-s-3],[d+1,-s-4]);
  }
  P.push([2,5],[12,8],[13,11]);
  for(let i=0;i<k;i++)P.push([14+2*i,12],[15+2*i,12]);
  check(P.length===15+2*k,"node count");
  P.forEach((p,i)=>p.forEach(q=>check(q<0||q<i,"future parent")));
  return P;
}
function sourceCounts(charges){
  const E=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)E.push([a,b]);
  const clauses=[];
  for(let v=0;v<4;v++){
    const e=E.map(([a,b],i)=>(a===v||b===v)?i:-1).filter(i=>i>=0);
    for(let t=0;t<8;t++){
      if((((t>>0)&1)^((t>>1)&1)^((t>>2)&1))===charges[v])continue;
      clauses.push(e.map((id,j)=>(t>>j&1)?-(id+1):id+1));
    }
  }
  const source="p cnf 6 16\n"+clauses.map(c=>c.join(" ")+" 0\n").join("");
  let sat=0;
  for(let a=0;a<64;a++)if(clauses.every(c=>c.some(x=>((a>>(Math.abs(x)-1))&1)===(x>0?1:0))))sat++;
  return {sat,clauses:clauses.length,bytes:source.length};
}
function search(P,cap){
  // State = physically retained paid values. Recomputations, arbitrary
  // eviction and overwriting a paid operand are explicitly allowed.
  // Every evaluation costs 1 physical step, even when the ID already
  // occurred in the fixed logical proof.
  let n=P.length,bit=i=>1n<<BigInt(i),seen=new Map([[0n,0]]),Q=[0n];
  for(let pos=0;pos<Q.length;pos++){
    let S=Q[pos],steps=seen.get(S);
    if((S&bit(n-1))!==0n)return {min_evaluations:steps,states:seen.size};
    let live=[];
    for(let j=0;j<n;j++)if((S&bit(j))!==0n)live.push(j);
    for(let i=0;i<n;i++){
      if((S&bit(i))!==0n || P[i].some(p=>p>=0 && (S&bit(p))===0n))continue;
      const retained=[0n];
      if(cap>=2)for(let p of live)retained.push(bit(p));
      if(cap>=3)for(let x=0;x<live.length;x++)for(let y=x+1;y<live.length;y++)retained.push(bit(live[x])|bit(live[y]));
      for(let r of retained){
        let T=r|bit(i);
        if(!seen.has(T)){seen.set(T,steps+1);Q.push(T);}
      }
    }
  }
  return {min_evaluations:null,states:seen.size};
}
function greedy(P){
  // Explicit no-recomputation order; outputs overwrite last-use parents.
  const order=[0,1,2,3,4,5,12,6,7,8,13,9,10,11,14];
  for(let i=15;i<P.length;i++)order.push(i);
  const cons=P.map(()=>[]);
  P.forEach((pp,i)=>pp.forEach(q=>{if(q>=0)cons[q].push(i)}));
  const done=new Set(),live=new Set();
  let peak=0;
  for(let i of order){
    check(!done.has(i),"duplicate evaluation");
    check(P[i].every(q=>q<0||live.has(q)),"evicted premise");
    let dying=P[i].filter(q=>q>=0&&cons[q].every(j=>j===i||done.has(j)));
    peak=Math.max(peak,live.size+(dying.length?0:1));
    dying.forEach(q=>live.delete(q));
    live.add(i);done.add(i);
    for(let q of [...live])if(q!==P.length-1&&cons[q].every(j=>done.has(j)))live.delete(q);
  }
  check(done.size===P.length,"missing inference");
  return peak;
}
function run(){
  let odd=sourceCounts([1,0,0,0]),even=sourceCounts([0,0,0,0]);
  check(odd.sat===0&&even.sat===8&&odd.clauses===16&&odd.bytes===163,"source controls");
  const rows=[];
  for(let k of [0,1,2,3,4,8,16]){
    let P=graph(k),c1=search(P,1),c2=search(P,2),c3=search(P,3),upper=greedy(P);
    check(c1.min_evaluations===null,"one-slot false positive");
    check(c2.min_evaluations===(k===0?15:null),"two-slot false positive");
    check(c3.min_evaluations===P.length,"recomputation physical work");
    check(upper===(k===0?2:3),"in-place schedule");
    rows.push({k,paid_nodes:P.length,references:2*P.length,span:6+2*k,
      inplace_no_recompute_peak:upper,cap1:c1,cap2:c2,cap3:c3});
  }
  return {run:"LSPV-4/530",status:"PROVED/RESTRICTED fixed semantic-slot model + COMPUTATIONAL BFS",
    original_source:"K4 signed odd Tseitin, 6 variables, 16 clauses, 163 ASCII DIMACS bytes",
    source_sha256:"861b38239ec08050a7b38b3da04fd79c17d43624a8f755be5a1417d8f01745c8",
    odd_models:0,even_models:8,rows,
    scope:"No complete historical R_mix341 checker; not physical RAM or universal SAT lower bound."};
}
if(typeof process!=="undefined"&&process.versions?.node)console.log(JSON.stringify(run(),null,2));
