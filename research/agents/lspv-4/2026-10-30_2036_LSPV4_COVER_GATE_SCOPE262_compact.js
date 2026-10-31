/* ARC-COVER-GATE-SCOPE262 compact independent JS experiment.
 * node thisfile.js (no dependencies). Complete original Python producer
 * and 660KB original-clause-indexed raw data are in the local reproducibility ZIP.
 * This compact check is separately implemented, exact and deterministic.
 */
"use strict";
const W1=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
const S15=[[-1,-3,14],[2,8,-9],[-10,13,14],[3,-7,-13],[-4,9,-11],[-5,-8,-14],[4,-8,11],[1,7,-13],[1,-7,10],[-5,-6,15],[-2,6,-12],[4,9,-10],[-2,5,-12],[3,6,-15],[-6,7,11],[2,-9,-11],[-4,8,10],[-3,12,15],[5,12,-15],[-1,13,-14]];
function assert(cond,msg){if(!cond)throw Error(msg||"assertion failed")}
function forbidden(n, predicate){
  let out=[];for(let m=0;m<(1<<n);m++)if(predicate(m)){
    out.push(Array.from({length:n},(_,i)=> (m&(1<<i))?-(i+1):i+1));
  }return out;
}
function litval(l,a){return !!a[Math.abs(l)] === (l>0)}
function clauseval(c,a){return c.some(l=>litval(l,a))}
function makeF(H,n){
  const y=n+1,F=[];
  for(let j=0;j<H.length;j++){
    const [a,b,c]=H[j],z=n+2+j;
    F.push([y,a,z],[-z,b,c]);
  }return {F,y};
}
function pairModes(F){
  let checked=0, conflicting=0;
  for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){
    const names=[...new Set([...F[i],...F[j]].map(Math.abs))];
    const s0=Object.fromEntries(F[i].map(l=>[Math.abs(l),l>0]));
    const s1=Object.fromEntries(F[j].map(l=>[Math.abs(l),l>0]));
    const shared=names.filter(k=>k in s0 && k in s1);
    const same=shared.some(k=>s0[k]===s1[k]);
    const opp=shared.some(k=>s0[k]!==s1[k]);
    const predicted=[!opp,!same,!same,!opp];
    for(let mode=0;mode<4;mode++){
      let seen=false;
      for(let mask=0;mask<(1<<names.length);mask++){
        const a={};
        names.forEach((k,v)=>{a[k]=!!(mask&(1<<v))});
        const t0=F[i].every(l=>litval(l,a));
        const u0=F[i].every(l=>!litval(l,a));
        const t1=F[j].every(l=>litval(l,a));
        const u1=F[j].every(l=>!litval(l,a));
        if(([t0&&t1,t0&&u1,u0&&t1,u0&&u1])[mode]){seen=true;break}
      }
      assert(seen===predicted[mode],"SS/SU/US/UU pair mismatch");
      checked++;
    }
    if(same&&opp)conflicting++;
  }
  return {pair_modes_exhaustively_verified:checked,mixed_sign_pairs:conflicting};
}
function runCase(name,H){
  const n=Math.max(...H.flat().map(Math.abs)), {F,y}=makeF(H,n);
  let models=0,verified=0;
  const modes=pairModes(F);
  for(let mask=0;mask<(1<<n);mask++){
    const x={};for(let i=1;i<=n;i++)x[i]=!!(mask&(1<<(i-1)));
    const sat=H.every(c=>clauseval(c,x));
    if(sat)models++;
    // For each source clause independently, assert y=0 extension iff source
    // clause is SAT; with y=1, z=0 works. This checks both labels on same source.
    for(let j=0;j<H.length;j++){
      const z=n+2+j,local=F.slice(2*j,2*j+2);
      const branch0=[false,true].some(bit=>local.every(c=>clauseval(c,{...x,[y]:false,[z]:bit})));
      assert(branch0===clauseval(H[j],x),"bad y=0 projection");
      assert(local.every(c=>clauseval(c,{...x,[y]:true,[z]:false})),"y=1 always SAT");
      verified+=2;
    }
  }
  for(const c of F){
    const S=Object.fromEntries(c.map(l=>[Math.abs(l),l>0]));
    const U=Object.fromEntries(c.map(l=>[Math.abs(l),l<0]));
    for(const l of c)assert(S[Math.abs(l)]!==U[Math.abs(l)],"S/U inversion");
  }
  return {name,n_source:n,m_source:H.length,n_transformed:n+H.length+1,m_transformed:F.length,source_models:models,semantic_single_cube_cover_F_entails_y:(models===0),local_projection_assertions:verified,...modes};
}
const xor=forbidden(3,m=>((m.toString(2).split("1").length-1)%2===1));
const cases={
  W1_STRICT22_UNSAT:W1,S15_STRICT22_SAT:S15,
  XOR3_SAT:xor,XOR3_UNSAT:forbidden(3,()=>true),
  HIT7_SAT:forbidden(3,m=>m!==7),
  ENDPOINTS_FAIL_BUT_SAT:[[1,2,3],[-1,-2,-3]],
  HORN_SAT:[[-1,-2,3],[-1,-3,2],[-2,-3,1]]
};
const rows=Object.entries(cases).map(([name,H])=>runCase(name,H));
assert(rows[0].source_models===0 && rows[1].source_models===861);
assert(rows[2].source_models===4 && rows[3].source_models===0);
const out={status:"PASS",run:"ARC-COVER-GATE-SCOPE262",source_model_checks:rows.reduce((a,r)=>a+(1<<r.n_source),0),local_projection_assertions:rows.reduce((a,r)=>a+r.local_projection_assertions,0),pair_modes:rows.reduce((a,r)=>a+r.pair_modes_exhaustively_verified,0),rows};
if(typeof process!=="undefined"&&process.stdout)process.stdout.write(JSON.stringify(out,null,2)+"\n");
return out;
