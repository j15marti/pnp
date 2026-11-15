const tmr2Leaf041 = function tmr2Leaf041() {
  "use strict";
  let assertions=0, seed=417003;
  const ok=(x,m)=>{assertions++;if(!x)throw Error("ASSERTION: "+m)};
  const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
  const permute=xs=>{const x=xs.slice();for(let i=x.length-1;i>0;i--){const j=Math.floor(rand()*(i+1));[x[i],x[j]]=[x[j],x[i]]}return x};
  const Q=k=>{let e=[],z=3*k;for(let i=0;i<k;i++)e.push([[i,0],[k+i,0],[2*k+i,0]]);
    for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)e.push([[i,0],[j,0],[z++,0]]);return {e,n:z}};
  const encode=edges=>edges.flatMap(e=>[0,1].map(bit=>e.map(([v,neg])=>(neg^bit)?-(v+1):(v+1))));
  function decode(clauses) {
    let groups=new Map();
    for(const c of clauses){
      if(!Array.isArray(c)||c.length!==3||c.some(x=>!Number.isSafeInteger(x)||x===0))return null;
      const t=c.map(x=>[Math.abs(x)-1,x<0?1:0]).sort((a,b)=>a[0]-b[0]);
      if(t[0][0]===t[1][0]||t[1][0]===t[2][0])return null;
      const key=t.map(a=>a[0]).join(","),sign=t.map(a=>a[1]).join("");
      if(!groups.has(key))groups.set(key,new Set());
      groups.get(key).add(sign);
    }
    const edges=[];
    for(const [key,s] of groups){
      if(s.size!==2)return null;
      const a=[...s];if(a[1]!==a[0].split("").map(b=>1-Number(b)).join(""))return null;
      const vars=key.split(",").map(Number);
      edges.push(vars.map((v,i)=>[v,+a[0][i]]));
    }
    return edges;
  }
  const verify=(clauses,a)=>clauses.every(c=>c.some(l=>((a[Math.abs(l)-1]??0)^(l<0?1:0))===1));
  function peel(edges){
    let live=edges.map((edge,id)=>({edge,id})),history=[];
    while(live.length){
      const degree=new Map();
      for(const {edge} of live)for(const [v] of edge)degree.set(v,(degree.get(v)||0)+1);
      let i=-1,pivot=-1;
      outer:for(let j=0;j<live.length;j++)for(const [v] of live[j].edge)if(degree.get(v)===1){i=j;pivot=v;break outer}
      if(i<0)return null;
      history.push({edge:live[i].edge,id:live[i].id,pivot});live.splice(i,1);
    }
    let n=0;for(const edge of edges)for(const [v] of edge)n=Math.max(n,v+1);
    const a=Array(n).fill(null);
    for(let j=history.length-1;j>=0;j--){
      const {edge,pivot}=history[j],other=[];
      for(const [v,sign] of edge)if(v!==pivot){if(a[v]===null)a[v]=0;other.push(a[v]^sign)}
      const wanted=(other[0]===other[1])?1-other[0]:0;
      const pivotSign=edge.find(x=>x[0]===pivot)[1];
      ok(a[pivot]===null,"reverse pivot private");
      a[pivot]=wanted^pivotSign;
      ok(edge.some(([v,s])=>(a[v]^s)===0)&&edge.some(([v,s])=>(a[v]^s)===1),"reverse NAE");
    }
    return {assignment:a.map(v=>v??0),history};
  }
  function transform(clauses,n){
    const ren=permute(Array.from({length:n},(_,i)=>i));
    const invert=Array.from({length:n},()=>rand()<.5?1:0);
    let next=clauses.map(c=>permute(c.map(l=>{
      const v=Math.abs(l)-1,sign=(l<0?1:0)^invert[v];
      return sign?-(ren[v]+1):ren[v]+1;
    })));
    const len=next.length;for(let i=0;i<len;i++)if(rand()<.3)next.push(next[i].slice());
    return permute(next);
  }
  let qTrials=0,maxK=0,records=0;
  for(let k=2;k<=11;k++){
    const {e,n}=Q(k),base=encode(e);maxK=k;
    for(let trial=0;trial<19;trial++){
      const cnf=transform(base,n),d=decode(cnf);
      ok(d!==null&&d.length===e.length,"NAE pair authentication");
      const p=peel(d);ok(p!==null,"Q leaf-completable");
      ok(verify(cnf,p.assignment),"signed/permuted SAT witness");
      ok(p.history.length===d.length,"all source obligations peeled");
      records+=p.history.length;qTrials++;
    }
  }
  let exhaustive=0,leafSuccess=0,nonleaf=0;
  const quadruples=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]];
  for(let i=0;i<625;i++){
    let v=i,edges=[];
    for(const t of quadruples){
      const d=v%5;v=Math.floor(v/5);
      if(d)edges.push(t.map((x,j)=>[x,((d-1)>>j)&1]));
    }
    const cnf=encode(edges),d=decode(cnf);
    ok(d!==null&&d.length===edges.length,"4-variable exact NAE parsing");
    const p=peel(d);
    if(p){leafSuccess++;ok(verify(cnf,p.assignment),"4-variable signed witness")}else nonleaf++;
    exhaustive++;
  }
  let sampled=0;
  for(let t=0;t<1200;t++){
    let e=[];
    for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)for(let h=j+1;h<6;h++)
      if(rand()<.33)e.push([[i,rand()<.5?1:0],[j,rand()<.5?1:0],[h,rand()<.5?1:0]]);
    const c=encode(e),p=peel(decode(c));
    if(p)ok(verify(c,p.assignment),"6-variable sampled signed witness");
    sampled++;
  }
  let bad=encode(Q(3).e);
  ok(decode(bad.slice(1))===null,"unpaired clause rejected");
  ok(decode(bad.concat([[1,2,-3]]))===null,"competing sign class rejected");
  ok(decode([[1,1,2]])===null,"nonproper triple rejected");
  const K5=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)for(let h=j+1;h<5;h++)K5.push([[i,0],[j,0],[h,0]]);
  ok(peel(K5)===null,"no private-variable pivot in complete 3-hypergraph");
  let sat=false;for(let x=0;x<32;x++)if(verify(encode(K5),Array.from({length:5},(_,i)=>(x>>i)&1)))sat=true;
  ok(!sat,"complete five-vertex 3-hypergraph unsatisfiable");
  function rankMod(matrix,p){
    const a=matrix.map(r=>r.slice());let rr=0;
    const power=(base,exponent)=>{let z=1;while(exponent){if(exponent%2)z=z*base%p;base=base*base%p;exponent=Math.floor(exponent/2)}return z};
    for(let j=0;j<a[0].length;j++){
      let q=rr;while(q<a.length&&a[q][j]===0)q++;if(q===a.length)continue;
      [a[q],a[rr]]=[a[rr],a[q]];let inv=power(a[rr][j],p-2);
      for(let h=j;h<a[0].length;h++)a[rr][h]=a[rr][h]*inv%p;
      for(let i=rr+1;i<a.length;i++)if(a[i][j]){
        const coeff=a[i][j];
        for(let h=j;h<a[0].length;h++)a[i][h]=(a[i][h]-coeff*a[rr][h]%p+p)%p;
      }
      rr++;
    }
    return rr;
  }
  const ranks=[];
  for(let k=2;k<=5;k++){
    const dim=1<<k,mat=[];
    for(let x=0;x<dim;x++){
      const t=x.toString(2).replace(/0/g,"").length,row=[];
      for(let y=0;y<dim;y++){
        let good=true;
        for(let i=0;i<k;i++)if(!((x>>i)&1)&&!((y>>i)&1))good=false;
        row.push(good?2**(t*(k-t)):0);
      }
      mat.push(row);
    }
    const r=rankMod(mat,1000003);ok(r===dim,"modular full rank");ranks.push({k,rank:r});
  }
  const col=["CNF","XOR","SEP","FUS","GAMMA","INT","MACHINE"],lambda=[0,0,0,1,1,0,1];
  const rows=[
    {rule:"ZERO_NOP",cost:0,delta:[0,0,0,0,0,0,0]},
    {rule:"ZERO_PHASE_SWITCH",cost:0,delta:[0,0,0,0,0,0,0]},
    {rule:"PEEL_EDGE",cost:1,delta:[0,0,0,2,-1,0,0]},
    {rule:"RESTORE_PIVOT",cost:1,delta:[0,0,0,0,1,0,0]},
    {rule:"HALT_VERIFIED",cost:1,delta:[0,0,0,0,0,0,1]}
  ];
  for(const r of rows){r.discharge=r.delta.reduce((s,d,i)=>s+d*lambda[i],0);ok(r.discharge<=r.cost,"tariff "+r.rule)}
  const m=Q(11).e.length;ok(2*m+1===133,"exact abstract cost 133");
  return {status:"PASS",assertions,failures:0,seed_initial:417003,seed_final:seed,mode:"V8 function execution; symbolic all-k statements separately proved",tests:{signed_globally_flipped_permuted_duplicate_Q:qTrials,max_k:maxK,source_leaf_records:records,exhaustive_fourvar_signed_NAE_hypergraphs:exhaustive,peelable_fourvar:leafSuccess,unpeeled_fourvar:nonleaf,sampled_sixvar_signed_NAE:sampled,malformed_authentication_rejections:3,K5_NAE_unsat_nonpeelable:true,modular_aggregated_ranks:ranks},tariff:{columns:col,lambda,rows,example_k:11,example_m:m,initial_phi:2*m+1,exact_typed_protocol_cost:2*m+1}};
};
console.log(JSON.stringify(tmr2Leaf041(), null, 2));
