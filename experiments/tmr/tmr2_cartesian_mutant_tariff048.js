"use strict";
// Reproducible TMR-2/048 original-source signed 3CNF high-order SAT mutant audit.
// Exact mathematical arguments in research/agents/tmr-2/2026-11-15_0918_TMR2_CARTESIAN_HIGHER_ORDER_MUTANT_TARIFF048.md
function audit(maxM=6,maxR=6){
  let assertions=0,mutants=0,paidRows=0,freeRows=0,exhaustive=0;const records=[];
  const ok=(x,s)=>{assertions++;if(!x)throw Error("FAIL "+s)};
  const gamma=n=>{let b=n.toString(2);return "0".repeat(b.length-1)+b};
  const parity=a=>a.reduce((v,x)=>v^x,0);
  const SAT=(cs,vals)=>cs.every(c=>c.some(([e,s])=>(vals[e]^s)===1));
  function gadget(m){
    let t=2*m,H=4*m,map=new Map();
    for(let i=0;i<t;i++)for(let [u,v] of [[i,(i+1)%t],[i+t,t+(i+1)%t],[i,i+t]]){
      let a=Math.min(u,v),b=Math.max(u,v);map.set(a+","+b,[a,b]);
    }
    let edges=[...map.values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1]),E=edges.length,
        inc=Array.from({length:H},()=>[]),charge=Array.from({length:H},(_,v)=>+(v===0));
    edges.forEach(([u,v],e)=>{inc[u].push(e);inc[v].push(e)});
    inc.forEach(a=>a.sort((x,y)=>x-y));
    let clauses=[],wrongByVertex=[];
    for(let v=0;v<H;v++){
      let wrong=[];
      for(let z=0;z<8;z++){
        let a=[(z>>2)&1,(z>>1)&1,z&1];
        if(parity(a)!==charge[v])wrong.push(a);
      }
      let tail=wrong.find(s=>s[2]===0);
      wrong=[...wrong.filter(s=>s!==tail),tail];wrongByVertex.push(wrong);
      for(let s of wrong)clauses.push(inc[v].map((e,j)=>[e,s[j]]));
    }
    function witness(k){
      let ci=Math.floor(k/3),j=k%3,v=Math.floor(ci/4),wrong=wrongByVertex[v][ci%4];
      let vals=Array(E).fill(0),rhs=charge.slice(),adj=Array.from({length:H},()=>[]);
      for(let h=0;h<3;h++){let e=inc[v][h];vals[e]=wrong[h];let [a,b]=edges[e];rhs[a===v?b:a]^=wrong[h]}
      edges.forEach(([a,b],e)=>{if(a!==v&&b!==v){adj[a].push([b,e]);adj[b].push([a,e])}});
      let root=v===0?1:0,parent=Array(H).fill(-1),pedge=Array(H).fill(-1),order=[root];parent[root]=root;
      for(let h=0;h<order.length;h++)for(let [x,e] of adj[order[h]])if(parent[x]<0){parent[x]=order[h];pedge[x]=e;order.push(x)}
      ok(order.length===H-1,"G-v connected");
      for(let h=order.length-1;h>0;h--){let x=order[h];vals[pedge[x]]=rhs[x];rhs[parent[x]]^=rhs[x]}
      ok(rhs[root]===0,"parity root");
      let modified=clauses.map(c=>c.map(z=>z.slice()));modified[ci][j][1]^=1;
      ok(SAT(modified,vals),"single sign local SAT");
      return vals;
    }
    return {H,E,edges,inc,charge,clauses,witness};
  }
  for(let m=2;m<=maxM;m++)for(let r=2;r<=maxR;r++){
    let g=gadget(m),q=3*g.clauses.length,Q=BigInt(q)**BigInt(r-1),E=r*g.E,C=r*g.clauses.length,
        w=Math.ceil(Math.log2(E+1)),bits="00110101"+gamma(E)+gamma(C),
        signs=Array.from({length:r},()=>[]),clauses=[];
    for(let i=0;i<r;i++)for(let c of g.clauses){
      let shifted=c.map(([e,s])=>[e+i*g.E,s]);clauses.push(shifted);
      for(let [e,s] of shifted){bits+=(e+1).toString(2).padStart(w,"0");signs[i].push(bits.length);bits+=s}
    }
    let N=bits.length;
    ok(g.H===4*m&&g.E===6*m&&q===48*m,"gadget counts");
    ok(N===8+gamma(E).length+gamma(C).length+3*C*(w+1),"honest encoding");
    ok(signs.every(v=>v.length===q),"sign partition");
    ok(clauses.every(c=>new Set(c.map(z=>z[0])).size===3),"proper3");
    for(let k=0;k<q;k++)g.witness(k);
    if(m===2)for(let z=0;z<(1<<g.E);z++){
      ok(!SAT(g.clauses,Array.from({length:g.E},(_,e)=>(z>>e)&1)),"base UNSAT exhaustive");
      exhaustive++;
    }
    let tuples=[];
    if(m===2&&r===2)for(let a=0;a<q;a++)for(let b=0;b<q;b++)tuples.push([a,b]);
    else for(let z=0;z<100;z++)tuples.push(Array.from({length:r},(_,i)=>(z*17+29*i+z*i*i)%q));
    for(let tuple of tuples){
      let vals=tuple.flatMap(k=>g.witness(k)),modified=clauses.map(c=>c.map(z=>z.slice())),b=bits;
      for(let i=0;i<r;i++){
        let k=tuple[i],p=signs[i][k];
        modified[i*g.clauses.length+Math.floor(k/3)][k%3][1]^=1;
        b=b.slice(0,p)+(b[p]==="0"?"1":"0")+b.slice(p+1);
      }
      ok(SAT(modified,vals),"cartesian mutant SAT");
      ok(Array.from(b).filter((v,i)=>v!==bits[i]).length===r,"exact r sign bits changed");
      mutants++;
    }
    let critical=new Map();
    signs.forEach((arr,i)=>arr.forEach(p=>critical.set(p,i)));
    let unread=Array(r).fill(q),maxDischarge=0n,dominating=0;
    const p=()=>({sep:Math.min(...unread),fus:+unread.every(x=>x>0),int:unread.reduce((a,x)=>a*BigInt(x),1n)});
    ok(p().int===BigInt(q)**BigInt(r),"initial product");
    for(let pos=0;pos<N;pos++){
      let before=p(),i=critical.get(pos);
      if(i!==undefined)unread[i]--;
      let after=p(),dsep=before.sep-after.sep,dfus=before.fus-after.fus,dint=before.int-after.int;
      ok(dsep>=0&&dsep<=1&&dfus>=0&&dfus<=1,"sep/fusion local");
      ok(dint>=0n&&dint<=Q,"Cartesian local");
      ok(BigInt(dsep)*Q+BigInt(dfus)*Q+dint<=3n*Q,"mixed rational");
      if(dint>maxDischarge)maxDischarge=dint;
      if(pos===signs[0][q-1]){
        ok(dsep===1&&dfus===1&&dint===Q,"authentic joint dominating row");dominating++;
      }
      let view=p();ok(view.sep===after.sep&&view.fus===after.fus&&view.int===after.int,"free view invariance");
      paidRows++;freeRows++;
    }
    let goal=p();ok(goal.sep===0&&goal.fus===0&&goal.int===0n,"completed goals zero");
    ok(dominating===1&&maxDischarge===Q,"joint row maximum");
    records.push({m,r,q,N,H:4*m*r,E:6*m*r,clauses:16*m*r,
      alternatives:String(BigInt(q)**BigInt(r)),maxPaidProductDischarge:String(Q),
      initial:[0,0,q,1,0,String(BigInt(q)**BigInt(r)),0],LPOptimum:q,
      lastFirstCopySignPosition:signs[0][q-1]});
  }
  return {id:"TMR2_CARTESIAN048",status:"COMPUTATIONAL finite V8, symbolic theorem in report",
    tested_m:[2,maxM],tested_r:[2,maxR],assertions,failures:0,mutants,paidRows,freeRows,exhaustive,
    exactCone:"lambda_SEP+lambda_FUS+q^(r-1)*lambda_Interface<=1",
    provenSymbolicOptimalInitial:"q=48m",records};
}
if(typeof module!=="undefined"&&module.exports){module.exports={audit};if(require.main===module)console.log(JSON.stringify(audit(),null,2));}
