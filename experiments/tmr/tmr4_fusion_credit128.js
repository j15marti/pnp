"use strict";
function audit() {
  "use strict";
  const F=(a,b=1n)=>{
    a=BigInt(a);b=BigInt(b);
    if(b===0n)throw Error("zero rational denominator");
    if(b<0n){a=-a;b=-b;}
    const gcd=(x,y)=>{x=x<0n?-x:x;while(y){const t=x%y;x=y;y=t;}return x||1n;};
    const d=gcd(a,b);return {n:a/d,d:b/d};
  };
  const zero=()=>F(0),one=()=>F(1);
  const add=(a,b)=>F(a.n*b.d+b.n*a.d,a.d*b.d);
  const neg=a=>F(-a.n,a.d),sub=(a,b)=>add(a,neg(b));
  const mul=(a,b)=>F(a.n*b.n,a.d*b.d);
  const div=(a,b)=>{if(!b.n)throw Error("divide by 0");return F(a.n*b.d,a.d*b.n);};
  const cmp=(a,b)=>a.n*b.d<b.n*a.d?-1:a.n*b.d>b.n*a.d?1:0;
  const txt=a=>a.d===1n?String(a.n):`${a.n}/${a.d}`;
  let assertions=0,errors=[],lpChecks=0,tariffChecks=0,zeroChecks=0;
  function check(b,message){assertions++;if(!b){errors.push(message);throw Error(message);}}
  function pop(x){let r=0;while(x){x&=x-1;r++;}return r;}
  function simplexMax(A,c){
    // Exact rational, Bland rule. max c*x : A*x<=1, x>=0.
    const m=A.length,n=c.length,L=n+m;const T=[];
    T.push([...Array.from({length:L},(_,j)=>j<n?F(-c[j]):zero()),zero()]);
    for(let i=0;i<m;i++)T.push([...Array.from({length:L},(_,j)=>j<n?F(A[i][j]):F(j-n===i?1:0)),one()]);
    let basis=Array.from({length:m},(_,i)=>n+i),pivots=0;
    while(true){
      let entering=-1;
      for(let j=0;j<L;j++)if(T[0][j].n<0n){entering=j;break;}
      if(entering<0)break;
      let leaving=-1,ratio=null;
      for(let i=1;i<=m;i++)if(T[i][entering].n>0n){
        const r=div(T[i][L],T[i][entering]);
        if(leaving<0||cmp(r,ratio)<0||(cmp(r,ratio)===0&&basis[i-1]<basis[leaving-1])){leaving=i;ratio=r;}
      }
      if(leaving<0)throw Error("unbounded fractional cover");
      const p=T[leaving][entering];
      T[leaving]=T[leaving].map(x=>div(x,p));
      for(let i=0;i<=m;i++)if(i!==leaving){
        const factor=T[i][entering];if(factor.n===0n)continue;
        T[i]=T[i].map((x,j)=>sub(x,mul(factor,T[leaving][j])));
      }
      basis[leaving-1]=entering;
      check(++pivots<=500,"simplex pivot limit");
    }
    const x=Array.from({length:n},zero);
    for(let i=0;i<m;i++)if(basis[i]<n)x[basis[i]]=T[i+1][L];
    const y=Array.from({length:m},(_,i)=>T[0][n+i]);
    const objective=T[0][L];
    for(let j=0;j<n;j++)check(x[j].n>=0n,"negative dual packing coordinate");
    for(let i=0;i<m;i++){
      check(y[i].n>=0n,"negative primal covering variable");
      let charged=zero();
      for(let j=0;j<n;j++)if(A[i][j])charged=add(charged,x[j]);
      check(cmp(charged,one())<=0,"dual batch capacity violated");
    }
    for(let j=0;j<n;j++){
      let covered=zero();
      for(let i=0;i<m;i++)if(A[i][j])covered=add(covered,y[i]);
      check(cmp(covered,F(c[j]))>=0,"primal scale coverage violated");
    }
    let px=zero(),dy=zero();
    for(let j=0;j<n;j++)px=add(px,mul(F(c[j]),x[j]));
    for(let i=0;i<m;i++)dy=add(dy,y[i]);
    check(cmp(px,objective)===0&&cmp(dy,objective)===0,"LP primal/dual mismatch");
    lpChecks++;
    return {value:objective,packing:x,cover:y,pivots};
  }
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const specs=[
    {name:"tiny",G:1,q:1,E:[[0]]},
    {name:"fanoG3",G:3,q:7,E:fano},
    {name:"fanoG1",G:1,q:7,E:fano},
    {name:"triangle",G:2,q:3,E:[[0,1],[1,2],[0,2]]},
    {name:"fullBatch",G:3,q:7,E:[[0,1,2,3,4,5,6]]},
    {name:"singletons",G:2,q:4,E:[[0],[1],[2],[3]]}
  ];
  const cases=[],matrixRows=[],tinyAllRows=[],exactCertificates=[];
  for(const spec of specs){
    const {G,q}=spec,full=(1<<q)-1,allG=(1<<G)-1,masks=spec.E.map(S=>S.reduce((a,j)=>a|(1<<j),0));
    const intMemo=new Map([[0,0]]),choice=new Map();
    function tau(U){
      if(intMemo.has(U))return intMemo.get(U);
      let best=Infinity,idx=-1;
      for(let i=0;i<masks.length;i++)if(masks[i]&U){
        const val=1+tau(U&~masks[i]);
        if(val<best){best=val;idx=i;}
      }
      check(Number.isFinite(best),"uncovered scale");
      intMemo.set(U,best);choice.set(U,idx);return best;
    }
    const lp=Array.from({length:full+1},(_,U)=>{
      const cols=Array.from({length:q},(_,j)=>j).filter(j=>U&(1<<j));
      if(!cols.length)return {value:zero(),packing:[],cover:masks.map(()=>zero()),pivots:0};
      const A=masks.map(S=>cols.map(j=>(S>>j)&1));
      return simplexMax(A,cols.map(()=>1));
    });
    for(let U=0;U<=full;U++){
      tau(U);
      check(cmp(lp[U].value,F(tau(U)))<=0,`${spec.name} fractional exceeds integer`);
    }
    const state=(P,U,h,v)=>({P,U,h,v}),key=s=>`${s.P}/${s.U}/${s.h}/${s.v}`;
    const abstractKey=s=>`${s.P}/${s.U}/${s.h}`;
    function edges(s){
      const out=[{rule:"VIEW",w:0,t:state(s.P,s.U,s.h,1-s.v)},
                 {rule:"NOP",w:0,t:state(s.P,s.U,s.h,s.v)}];
      if(!s.h)return out;
      for(let g=0;g<G;g++)if(!(s.P&(1<<g)))
        out.push({rule:"CHECK",w:1,t:state(s.P|(1<<g),s.U,1,s.v)});
      if(s.P===allG&&s.U)for(let i=0;i<masks.length;i++)if(s.U&masks[i])
        out.push({rule:"BATCH",w:1,batch:i,t:state(s.P,s.U&~masks[i],1,s.v)});
      const unpaid=allG^s.P;
      if(s.U===full&&unpaid&&!(unpaid&(unpaid-1)))for(let i=0;i<masks.length;i++)
        out.push({rule:"FUSE",w:1,batch:i,t:state(allG,s.U&~masks[i],1,s.v)});
      if(s.P===allG&&s.U===0)out.push({rule:"HALT",w:1,t:state(allG,0,0,s.v)});
      return out;
    }
    function coord(s,kind){
      const u=G-pop(s.P);
      const credit=(u>0&&s.U===full&&s.h===1)?1:0;
      const pGamma=u-credit;
      return {gamma:pGamma,sep:kind==="fractional"?lp[s.U].value:F(tau(s.U)),machine:s.h};
    }
    const phi=(s,kind)=>{const p=coord(s,kind);return add(F(p.gamma+p.machine),p.sep);};
    let states=[];
    for(let P=0;P<=allG;P++)for(let U=0;U<=full;U++)for(let v=0;v<=1;v++)
      states.push(state(P,U,1,v));
    states.push(state(allG,0,0,0),state(allG,0,0,1));
    const nodes=new Map(states.map(s=>[key(s),s]));
    const index=new Map(),low=new Map(),stack=[],onStack=new Set(),comp=new Map(),scc=[];
    let stepNo=0;
    function tarjan(s){
      const k=key(s);index.set(k,stepNo);low.set(k,stepNo);stepNo++;stack.push(k);onStack.add(k);
      for(const e of edges(s).filter(e=>e.w===0)){
        const next=key(e.t);
        if(!index.has(next)){tarjan(e.t);low.set(k,Math.min(low.get(k),low.get(next)));}
        else if(onStack.has(next))low.set(k,Math.min(low.get(k),index.get(next)));
      }
      if(low.get(k)===index.get(k)){
        const id=scc.length,members=[];let n;
        do{n=stack.pop();onStack.delete(n);comp.set(n,id);members.push(n);}while(n!==k);
        scc.push(members);
      }
    }
    for(const s of states)if(!index.has(key(s)))tarjan(s);
    check(scc.length===states.length/2,`${spec.name} zero SCC count`);
    for(const members of scc){
      check(members.length===2,"zero SCC must be reversible two-view");
      const a=nodes.get(members[0]),b=nodes.get(members[1]);
      check(abstractKey(a)===abstractKey(b),"zero SCC conflates paid history");
      for(const kind of ["integer","fractional"])
        check(cmp(phi(a,kind),phi(b,kind))===0,"zero SCC changes potential");
    }
    const rows={VIEW:{count:0,maxIntegerDelta:"0",maxFractionalDelta:"0"},
                NOP:{count:0,maxIntegerDelta:"0",maxFractionalDelta:"0"},
                CHECK:{count:0,maxIntegerDelta:"0",maxFractionalDelta:"0"},
                BATCH:{count:0,maxIntegerDelta:"0",maxFractionalDelta:"0"},
                FUSE:{count:0,maxIntegerDelta:"0",maxFractionalDelta:"0"},
                HALT:{count:0,maxIntegerDelta:"0",maxFractionalDelta:"0"}};
    const maxI={},maxF={},costs={0:0,1:0};
    for(const s of states){
      for(const e of edges(s)){
        const f=coord(s,"fractional"),ft=coord(e.t,"fractional");
        const i=coord(s,"integer"),it=coord(e.t,"integer");
        const dG=f.gamma-ft.gamma,dM=f.machine-ft.machine,dSepF=sub(f.sep,ft.sep);
        const dSepI=sub(i.sep,it.sep),dF=add(F(dG+dM),dSepF),dI=add(F(dG+dM),dSepI);
        check(dG>=0&&dG<=1&&dM>=0&&dM<=1,"nonmonotone corrected gate/terminal");
        check(cmp(dSepF,zero())>=0&&cmp(dSepI,zero())>=0,"cover must be monotone");
        check(cmp(dF,F(e.w))<=0&&cmp(dI,F(e.w))<=0,`${spec.name} ${e.rule} paid tariff violated`);
        check(nodes.has(key(e.t)),"successor not in concrete system");
        check(comp.has(key(e.t))&&comp.has(key(s)),"SCC simulation undefined");
        if(e.w===0){
          check(comp.get(key(s))===comp.get(key(e.t)),"free step exits SCC");
          check(cmp(dF,zero())===0&&cmp(dI,zero())===0,"zero cost potential changed");
          zeroChecks++;
        }
        tariffChecks++;costs[e.w]++;
        rows[e.rule].count++;
        if(!maxI[e.rule]||cmp(dI,maxI[e.rule])>0)maxI[e.rule]=dI;
        if(!maxF[e.rule]||cmp(dF,maxF[e.rule])>0)maxF[e.rule]=dF;
        if(spec.name==="tiny")tinyAllRows.push({
          from:abstractKey(s),view:s.v,rule:e.rule,
          to:abstractKey(e.t),cost:e.w,
          delta_7:["0","0",txt(dSepF),"0",String(dG),"0",String(dM)],
          integer_sep_delta:txt(dSepI)});
      }
    }
    for(const rule of Object.keys(rows)){
      rows[rule].maxIntegerDelta=txt(maxI[rule]||zero());
      rows[rule].maxFractionalDelta=txt(maxF[rule]||zero());
    }
    // Independent shortest-path replay of the entire system, not derived from potentials.
    const initial=state(0,full,1,0);
    const distances=new Map([[key(initial),0]]),queue=[initial];
    for(let pos=0;pos<queue.length;pos++){
      const s=queue[pos],d=distances.get(key(s));
      for(const e of edges(s)){
        const k=key(e.t),nd=d+e.w;
        if(!distances.has(k)||nd<distances.get(k)){distances.set(k,nd);queue.push(e.t);}
      }
    }
    const shortest=Math.min(distances.get(key(state(allG,0,0,0)))??Infinity,
                            distances.get(key(state(allG,0,0,1)))??Infinity);
    const intCost=G+tau(full),fracCost=add(F(G),lp[full].value);
    check(shortest===intCost,`${spec.name} shortest path is not G+tau`);
    check(cmp(phi(initial,"integer"),F(shortest))===0,"exact nonlinear integer potential");
    check(cmp(phi(initial,"fractional"),fracCost)===0,"fractional potential incorrect");
    const initPhiInt=txt(phi(initial,"integer")),initPhiFrac=txt(phi(initial,"fractional"));
    // A path witness uses G-1 distinct checks, FUSE of last identity and
    // the remaining batches from a minimum cover, then a separate HALT.
    const path=[];let current=initial;
    for(let g=0;g<G-1;g++){
      const next=state(current.P|(1<<g),current.U,1,current.v);
      check(edges(current).some(e=>e.rule==="CHECK"&&key(e.t)===key(next)),"trace CHECK not legal");
      path.push({rule:"CHECK",P:current.P,U:current.U,nextP:next.P,nextU:next.U,cost:1});current=next;
    }
    let coverList=[],remaining=full;
    while(remaining){let idx=choice.get(remaining);check(idx>=0,"cover witness absent");coverList.push(idx);remaining&=~masks[idx];}
    check(coverList.length===tau(full),"integer cover witness incorrect");
    for(let b=0;b<coverList.length;b++){
      const r=b===0?"FUSE":"BATCH",batch=coverList[b];
      const found=edges(current).find(e=>e.rule===r&&e.batch===batch);
      check(!!found,`${spec.name} witness ${r} is not legal`);
      path.push({rule:r,batch,from:abstractKey(current),to:abstractKey(found.t),cost:1});
      current=found.t;
    }
    const halt=edges(current).find(e=>e.rule==="HALT");
    check(!!halt,"witness lacks distinct HALT");
    path.push({rule:"HALT",from:abstractKey(current),to:abstractKey(halt.t),cost:1});
    check(path.reduce((a,x)=>a+x.cost,0)===shortest,"witness paid length mismatch");
    check(cmp(phi(halt.t,"integer"),zero())===0,"completed goal not zero");
    const linearPrevious=spec.name==="fanoG3"?"4":
      spec.name==="fanoG1"?"10/3":
      spec.name==="triangle"?"3":
      spec.name==="fullBatch"?"4":
      spec.name==="singletons"?"5":"2";
    cases.push({spec:spec.name,G,q,batches:spec.E.length,zero_sccs:scc.length,
      concrete_states:states.length,reachable_states:distances.size,
      paid_rows:costs[1],zero_rows:costs[0],
      fractional_cover:txt(lp[full].value),integer_cover:tau(full),
      old_static_linear_tariff:linearPrevious,
      new_fractional_product_tariff:initPhiFrac,
      new_integer_product_tariff:initPhiInt,exact_shortest_path:shortest,
      witness:path});
    matrixRows.push({spec:spec.name,full_pending_mask:full,
      check_and_fuse_rule_counts:rows,closure:"authentic VIEW/NOP SCC only",
      cover_primal:lp[full].cover.map(txt),
      cover_dual:lp[full].packing.map(txt)});
    exactCertificates.push({case:spec.name,
      fractional_primal_cover:lp[full].cover.map(txt),
      fractional_dual_packing:lp[full].packing.map(txt),
      integral_cover_batches:coverList,
      lambda7:["0","0","1","0","1","0","1"],
      objective_fractional:initPhiFrac,objective_integer:initPhiInt});
  }
  check(cases[1].new_integer_product_tariff==="6","Fano integer calibration");
  check(cases[1].new_fractional_product_tariff==="16/3","Fano rational calibration");
  const hostile=[
    {name:"old static unmodified components",case:"tiny",rule:"FUSE",cost:1,
      weights:{Gamma:"1",SEP:"1"},weighted_discharge:"2",result:"FAIL; actual legal edge"},
    {name:"extra two-check fusion",case:"G=2,J={0},E={{0}}",rule:"FUSE_TWO",cost:1,
      before:"P=empty,U=J,h=1, potential=3",
      after:"P=D,U=empty,h=1,potential=1",
      weighted_discharge:"2",result:"FAIL if this model-changing operation is added"},
    {name:"zero-cost full activation",case:"G=3,Fano",rule:"FREE_ALL",cost:0,
      before:"P=empty,U=J,h=1, integer potential=6",
      after:"P=empty,U=empty,h=1, integer potential=4",
      weighted_discharge:"2",result:"FAIL if compact or affine operation is actually free"},
    {name:"full-batch paid shortcut",case:"fullBatch",cost:1,
      result:"PASS, recalibrated authentic batch, exact minimum=4"}
  ];
  const raw={id:"TMR4_FUSCREDIT128",date:"2026-11-15 07:38 PST",
    status:"PROVED/RESTRICTED symbolic theorem; finite exact-rational and SCC audits COMPUTATIONAL",
    model:"TMR-3/046 preauthenticated paid gate/batch calculus, not a SAT Turing machine",
    assertions,lp_subset_primal_dual_checks:lpChecks,all_legal_tariff_checks:tariffChecks,
    zero_price_checks:zeroChecks,failures:errors.length,cases,
    hostile_counterexamples:hostile};
  const matrix={id:"TMR4_FUSCREDIT128_SEVEN_VECTOR_MATRIX",order:["CNF","XOR","SEP","FUS","GAMMA","INTERFACE","MACHINE"],
    source_and_state:"immutable authenticated F, globally canonical D, P subset D, pending U subset J, h, reversible v",
    concrete_authority:"CHECK, BATCH, FUSE only when last unpaid and U=J, HALT distinct, VIEW/NOP cost0",
    abstract_relation:"(F,D,P,U,h,v) related to (P,U,h); free VIEW/NOP become empty path in true zero SCC; paid rules become one quotient edge at identical price",
    component_fractional:"p=(0,0,tau_fractional(U),0,G-|P|-1_{G>|P| and U=J and h=1},0,h)",
    component_integer:"p=(0,0,tau_integer(U),0,G-|P|-1_{G>|P| and U=J and h=1},0,h)",
    lambda7:["0","0","1","0","1","0","1"],
    signed_delta_7:{
      VIEW_NOP:"(0,0,0,0,0,0,0), cost0",
      CHECK:"(0,0,0,0,1 except last CHECK at U=J gives 0,0,0), cost1",
      BATCH:"(0,0,tau(U)-tau(U\\S),0,0,0,0), cost1, delta<=1",
      FUSE:"(0,0,tau(J)-tau(J\\S),0,0,0,0), cost1, delta<=1",
      HALT:"(0,0,0,0,0,0,1), cost1"
    },all_step_certificate:"every concrete step has 0-cost empty abstract path if free, otherwise one edge of cost exactly one; every completed goal has potential 0",
    finite_cases:matrixRows,tiny_all_authentic_rows:tinyAllRows,exact_rational_certificates:exactCertificates,
    hostile};
  return {raw,matrix};
}
if (typeof module !== "undefined" && require.main === module) {
  const o=audit();
  process.stdout.write(JSON.stringify(process.argv.includes("--matrix")?o.matrix:o.raw,null,2)+"\n");
}
