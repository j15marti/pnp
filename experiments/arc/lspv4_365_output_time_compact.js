(function compactVerifier(){
  const assert=(c,m)=>{if(!c)throw Error(m)};
  let checks=0,records=[];
  const check=c=>{checks++;assert(c,"assertion "+checks)};
  function php(h){let v=h*(h+1),cs=[];for(let i=0;i<h+1;i++){let c=[];for(let j=0;j<h;j++)c.push(i*h+j+1);cs.push(c)}for(let j=0;j<h;j++)for(let i=0;i<h+1;i++)for(let k=i+1;k<h+1;k++)cs.push([-(i*h+j+1),-(k*h+j+1)]);return {v,cs};}
  function bphp(ell){let n=2**ell,cs=[];for(let i=0;i<n+1;i++)for(let j=i+1;j<n+1;j++)for(let z=0;z<n;z++){let c=[];for(let t=0;t<ell;t++){let s=(z>>t)&1;c.push(s?-(i*ell+t+1):(i*ell+t+1));c.push(s?-(j*ell+t+1):(j*ell+t+1))}cs.push(c)}return {v:(n+1)*ell,cs};}
  function sat(f,deleted=-1,flipC=-1,flipL=-1){if(f.v>15)throw Error("exhaustive cap");for(let a=0;a<2**f.v;a++){let ok=true;for(let i=0;i<f.cs.length;i++){if(i===deleted)continue;let c=f.cs[i];if(!c.some((literal,j)=>{let l=(i===flipC&&j===flipL)?-literal:literal;return ((a>>(Math.abs(l)-1))&1)===(l>0?1:0)})){ok=false;break}}if(ok)return a}return -1;}
  for(let h=1;h<=3;h++){let f=php(h);check(sat(f)===-1);let sd=0,sf=0;for(let i=0;i<f.cs.length;i++){check(sat(f,i)!==-1);sd++;for(let j=0;j<f.cs[i].length;j++){check(sat(f,-1,i,j)!==-1);sf++}}records.push({family:"PHP",h,clauses:f.cs.length,source_deletion_sat:sd,source_occurrence_flip_sat:sf})}
  for(let ell=1;ell<=2;ell++){let f=bphp(ell);check(sat(f)===-1);let sd=0,sf=0;for(let i=0;i<f.cs.length;i++){check(sat(f,i)!==-1);sd++;for(let j=0;j<f.cs[i].length;j++){check(sat(f,-1,i,j)!==-1);sf++}}records.push({family:"BPHP",ell,clauses:f.cs.length,source_deletion_sat:sd,source_occurrence_flip_sat:sf})}
  return {id:"LSPV4_HAKEN_BRAUN_OUTPUT_TIME_TRANSPORT365_COMPACT",status:"PASS",assertions:checks,records,scope:"Finite same-source SAT neighbors and UNSAT controls. No asymptotic theorem inferred; long-run independent check in local archive."};
})();
