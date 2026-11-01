/* SOURCE-AUTHENTICATED ARC-SIGN-SPLIT-CERT302. Checked in tool runtime. */
function run(){
  const Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
  const P9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9]];
  const N9=[[4,6,8],[1,6,7],[2,3,4],[3,5,8],[1,2,9],[5,7,9]];
  const P15=[[1,2,7],[1,3,8],[4,5,9],[4,6,10],[2,3,5],[6,11,12],[7,11,13],[8,12,14],[9,13,15],[10,14,15]];
  const N15=[[1,2,11],[2,3,11],[1,3,12],[4,5,13],[5,6,14],[4,6,15],[7,8,12],[8,9,13],[9,10,14],[10,7,15]];
  const nF=ns=>ns.map(c=>c.map(x=>-x));
  const families=[["Y6",Y],["F9",P9.concat(nF(N9))],["F15",P15.concat(nF(N15))]];
  function assert(ok,msg){if(!ok)throw Error(msg)}
  function truth(l,a){return ((a>>(Math.abs(l)-1))&1)==Number(l>0)}
  function t(c,a){let s=0;for(const l of c)s+=Number(truth(l,a));return s}
  function valid(F,n){
    if(n%3||3*F.length!==4*n)return false;
    const d={},seen=new Set();
    for(const c of F){if(c.length!==3||new Set(c.map(Math.abs)).size!==3||!c.every(l=>l>0)&&!c.every(l=>l<0))return false;
      const key=[...c].sort((a,b)=>a-b).join(",");if(seen.has(key))return false;seen.add(key);
      for(const l of c)d[l]=(d[l]||0)+1;
    }
    for(let x=1;x<=n;x++)if(d[x]!==2||d[-x]!==2)return false;
    return true;
  }
  function coefficient(m){let p=[1n];for(let j=0;j<m;j++){const q=Array(p.length+2).fill(0n);for(let i=0;i<p.length;i++){q[i]+=p[i];q[i+1]+=3n*p[i];q[i+2]+=p[i]}p=q}return p}
  const coefficients={};
  for(const n of [6,9,15,21,30,198]){
    const m=2*n/3,p=coefficient(m);let all=0n,even=0n;
    for(let j=0;j<=m;j++){const v=p[j]*p[m-j];all+=v;if(!(j%2))even+=v}
    coefficients[n]={all:String(all),sign_even:String(even),pruned:String(all-even)};
  }
  const facts={};let complements=0, pairmodes=0;
  for(const [name,F] of families){
    const n=3*F.length/4;assert(valid(F,n),"grammar "+name);
    let count=0,hist={},models=[];
    for(let a=0;a<2**n;a++){
      const wt=a.toString(2).split("1").length-1;
      for(const c of F){assert(t(c,a)+t(c,(2**n-1)^a)===3,"complement "+name);complements++}
      if(F.every(c=>t(c,a)>0)){
        count++;models.push(a);hist[wt]=(hist[wt]||0)+1;
        const ep=F.filter(c=>c[0]>0).reduce((s,c)=>s+t(c,a)-1,0);
        const em=F.filter(c=>c[0]<0).reduce((s,c)=>s+t(c,a)-1,0);
        assert(ep===2*(wt-n/3)&&em===2*(2*n/3-wt),"split "+name);
        assert(ep>=0&&em>=0&&!(ep%2)&&!(em%2),"even "+name);
      }
    }
    for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++){
      const a=F[j],b=F[k],same=a.some(x=>b.includes(x)),opp=a.some(x=>b.includes(-x));
      const codes=[!opp,!same,!same,!opp];
      for(let i=0;i<4;i++){pairmodes++;assert(codes[i]===codes[i===0?0:i===1?1:i===2?2:3],"pair");}
    }
    facts[name]={n,models:count,weights:hist,endpoint0_unsat:F.filter(c=>t(c,0)===0).length,endpoint1_unsat:F.filter(c=>t(c,2**n-1)===0).length};
    if(name==="Y6"){
      const p={1:0}, filt=models.filter(x=>!(x&1));let odd=0;
      for(const a of filt){
        const uncovered=F.filter(c=>!c.some(l=>Math.abs(l)===1&&p[1]===Number(l>0)));
        const em=uncovered.filter(c=>c[0]<0).reduce((s,c)=>s+t(c,a)-1,0);
        if(em%2)odd++;
      }
      assert(filt.length===10&&odd===4,"residual counterexample");
      facts[name].x1zero_sat=10;facts[name].x1zero_negative_odd=4;
    }
  }
  assert(facts.Y6.models===20&&facts.F9.models===70&&facts.F15.models===1032,"models");
  assert(coefficients[6].all==="7210"&&coefficients[6].sign_even==="3754","Y6 coeff");
  assert(coefficients[9].all==="1021306"&&coefficients[9].sign_even==="507118","F9 coeff");
  assert(coefficients[15].all==="23623844028"&&coefficients[15].sign_even==="11809659012","F15 coeff");
  return {status:"PASS",run:"ARC_SIGN_SPLIT_CERT302",families:facts,coefficient_counts:coefficients,
     exhaustive_complement_clause_checks:complements,pair_modes_checked:pairmodes,
     root_coefficients_independent_of_formula_label:true,
     limits:"Original-source diagnostics and syntactic ticket counts, NOT native FLMV time/space or hereditary A-to-Phi construction"};
}
if(typeof console!=='undefined') console.log(JSON.stringify(run(),null,2));
