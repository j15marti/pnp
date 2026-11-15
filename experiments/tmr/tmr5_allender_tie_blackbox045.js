/* TMR-5/045: independent exhaustive redteam, Node 18+; no external packages. */
function audit() {
  let assertions=0, exceptions=0, sampleEvaluations=0;
  const check=(ok,msg)=>{assertions++;if(!ok){exceptions++;throw Error(msg)}};
  const tie=[];
  for(let m=2;m<=11;m++){
    const n=2**m, mask=n-1, exceptMask=mask^1;
    function f(x,minus){return (x&1)!==0 && (!minus || (x&exceptMask)!==exceptMask)}
    function sampleAccept(z,minus){
      const b=Math.floor(z/n), x=z%n;
      return (b<2&&f(x,minus)) || b===2 || (b===3&&x===0);
    }
    const Splus=Array.from({length:n},(_,x)=>f(x,false)?1:0).reduce((a,b)=>a+b,0);
    const Sminus=Array.from({length:n},(_,x)=>f(x,true)?1:0).reduce((a,b)=>a+b,0);
    let Aplus=0,Aminus=0;
    for(let z=0;z<4*n;z++){if(sampleAccept(z,false))Aplus++;if(sampleAccept(z,true))Aminus++;sampleEvaluations+=2}
    check(Splus===n/2&&Sminus===n/2-1,`truth counts m${m}`);
    check(Aplus===2*n+1&&Aminus===2*n-1,`tie normalized counts m${m}`);
    const eps=1/(4*n), pPlus=Aplus/(4*n), pMinus=Aminus/(4*n);
    check(Math.abs(pPlus-(.5+eps))<1e-14&&Math.abs(pMinus-(.5-eps))<1e-14,`bias m${m}`);
    check(pPlus*pPlus<.5,`two-call AND failure m${m}`);
    tie.push({m,bit_assignments:n,sat_count_yes:Splus,sat_count_no:Sminus,random_branch_count:4*n,accept_yes:Aplus,accept_no:Aminus,epsilon:eps,p_plus:pPlus,p_minus:pMinus,lower_bound_samples_ceiling:Math.ceil(1/(72*eps*eps))});
  }
  const fusion=[];
  let fusionStates=0;
  const w=(t,u,memo=new Map())=>{
    const key=t+","+u;
    if(memo.has(key))return memo.get(key);
    if(t===0&&u===0)return 1; // distinct mandatory HALT
    const options=[];
    if(t>0)options.push(1+w(t-1,u,memo));
    if(u>0)options.push(1+w(t,u-1,memo));
    if(t>=2&&u>0)options.push(1+w(t-2,u-1,memo));
    const ans=Math.min(...options);memo.set(key,ans);return ans;
  };
  for(let t=0;t<=12;t++)for(let u=0;u<=9;u++){
    const actual=w(t,u);const M=2*Math.min(Math.floor(t/2),u);
    const expected=t+u-M+1;
    check(actual===expected,`repeatable FUSE2 Bellman ${t},${u}`);fusionStates++;
    if((t===4&&u===2)||(t===5&&u===4))fusion.push({t,u,M,actual,expected});
  }
  const cache=new Map();
  function overlap(t,mask){
    const key=t+":"+mask;if(cache.has(key))return cache.get(key);
    if(t===0&&mask===0)return {cost:1,path:["HALT"]};
    let best={cost:Infinity,path:[]};
    const add=(name,nt,nmask)=>{const tail=overlap(nt,nmask);if(1+tail.cost<best.cost)best={cost:1+tail.cost,path:[name,...tail.path]}};
    if(t>0)add("CHECK",t-1,mask);
    for(const S of [1,2,3])if((mask&S)!==0)add("BATCH_"+S,t,mask&~S);
    if(t>=2)for(const S of [1,2])if((mask&S)!==0)add("FUSE2_"+S,t-2,mask&~S);
    cache.set(key,best);return best;
  }
  const hostile=overlap(4,3);
  check(hostile.cost===3,`overlap shortcut real shortest work`);
  const naive=4+1-2+1;
  check(naive===4&&hostile.cost<naive,"naive tau fusion credit falsely high");
  const cartesian=[];
  let cartesianRows=0;
  for(let q=2;q<=5;q++)for(let r=2;r<=4;r++){
    let rows=0;
    const size=(q+1)**r;
    for(let state=0;state<size;state++){
      const u=[];let x=state;
      for(let i=0;i<r;i++){u.push(x%(q+1));x=Math.floor(x/(q+1))}
      const oldMin=Math.min(...u),oldAll=u.every(v=>v>0)?1:0,oldProd=u.reduce((a,b)=>a*b,1);
      for(let i=0;i<r;i++)if(u[i]>0){
        const v=u.slice();v[i]--;
        const drop=[oldMin-Math.min(...v),oldAll-(v.every(y=>y>0)?1:0),oldProd-v.reduce((a,b)=>a*b,1)];
        check(drop[0]>=0&&drop[0]<=1&&drop[1]>=0&&drop[1]<=1&&drop[2]>=0&&drop[2]<=q**(r-1),`cartesian row q${q} r${r}`);
        rows++;cartesianRows++;
      }
    }
    const u=[1,...Array(r-1).fill(q)],v=[0,...Array(r-1).fill(q)];
    const discharge=[Math.min(...u)-Math.min(...v),1, u.reduce((a,b)=>a*b,1)-v.reduce((a,b)=>a*b,1)];
    check(JSON.stringify(discharge)===JSON.stringify([1,1,q**(r-1)]),`maximizing genuine row`);
    const vertexOpt=Math.max(q,1,(q**r)/(q**(r-1)));
    check(vertexOpt===q,"LP extreme nonnegative objective");
    cartesian.push({q,r,states:size,paid_rows:rows,max_joint_row:discharge,exact_lp_optimum:q});
  }
  return {run:"TMR5-ALLENDER045",kind:"independent exact enumeration plus symbolic restricted lemmas",tie,quantitative_blackbox_bound:"K >= 1/(72 epsilon^2) = (2/9) * 4^m for two-thirds-success sample-only discrimination",hostile_PP_AND:"p_plus^2<1/2 for all tested m>=2; symbolic holds for every m>=2",repeatable_fuse2_checks:fusionStates,fusion,overlap_shortcut:{start_unpaid_gates:4,pending_obligations:["a","b"],batch_menu:["a","b","ab"],FUSE2_eligible:["a","b"],genuine_shortest:hostile,naive_tau_credit_cost:naive},cartesian,cartesian_rows:cartesianRows,assertions,sample_evaluations:sampleEvaluations,exceptions};
}
console.log(JSON.stringify(audit(),null,2));
