// SEPARATOR_LATTICE083: exact three-variable source/interpolant audit.
// The function below is byte-for-byte the body executed in V8 via the GitHub tools context.
function audit() {
  const n=3, m=1<<n, ALL=(1<<m)-1;
  let checks=0, failures=0;
  const must=(ok,msg)=>{checks++;if(!ok){failures++;throw Error(msg)}};
  const popcount=x=>{let c=0;while(x){c+=x&1;x>>>=1;}return c};
  const forbidClause=(assignment)=>Array.from({length:n},(_,j)=>((assignment>>j)&1)?-(j+1):(j+1));
  const truth=(cnf)=>{let mask=0;for(let a=0;a<m;a++){const ok=cnf.every(c=>c.some(l=>l>0?((a>>(l-1))&1)===1:((a>>(-l-1))&1)===0));if(ok)mask|=1<<a}return mask};
  const sourceCNFs=Array.from({length:ALL+1},(_,U)=>Array.from({length:m},(_,a)=>a).filter(a=>!(U&(1<<a))).map(forbidClause));
  for(let U=0;U<=ALL;U++) must(truth(sourceCNFs[U])===U,"CNF representation "+U);
  let disjoint=0, unique=0, bothSat=0, bothSatUnique=0, totalInterpolants=0, explicitSeparators=0;
  let nonuniqueExample=null;
  for(let U=0;U<=ALL;U++)for(let V=0;V<=ALL;V++){
    if(U&V)continue;
    disjoint++;
    const free=ALL^(U|V), theoretical=1<<popcount(free), lo=U, hi=ALL^V;
    let actual=0, actualMin=ALL, actualMax=0;
    for(let I=0;I<=ALL;I++){
      const interp=((U&(~I))===0)&&((V&I)===0);
      if(interp){actual++;actualMin&=I;actualMax|=I;}
      explicitSeparators++;
    }
    must(actual===theoretical,"count U="+U+" V="+V);
    must(actualMin===lo&&actualMax===hi,"extremal U="+U+" V="+V);
    must((theoretical===1)===(free===0),"uniqueness");
    totalInterpolants+=actual;
    if(theoretical===1)unique++;
    if(U!==0&&V!==0){bothSat++;if(theoretical===1)bothSatUnique++;}
    if(!nonuniqueExample && U===1 && V===2) nonuniqueExample={U,V,free,interpolants:actual};
  }
  must(disjoint===3**m,"all disjoint pairs");
  must(unique===2**m,"all unique pairs");
  must(bothSat===3**m-2*(2**m)+1,"both satisfiable");
  must(bothSatUnique===2**m-2,"both SAT unique");
  must(totalInterpolants===4**m,"all interpolants");
  let parity=0,nae=0;
  for(let a=0;a<m;a++){let cnt=popcount(a);if(cnt%2)parity|=1<<a;if(cnt>0&&cnt<n)nae|=1<<a;}
  const controls=[{name:"parity3",U:parity},{name:"NAE3",U:nae}].map(({name,U})=>{
    const V=ALL^U, A=sourceCNFs[U],B=sourceCNFs[V];
    must((U&V)===0&&(U|V)===ALL,"complement controls");
    must(truth(A)===U&&truth(B)===V,"source truth controls");
    return {name,projectionA:U,projectionB:V,clausesA:A.length,clausesB:B.length,all_shared_vars:3,unique:true};
  });
  return {experiment:"SEPARATOR_LATTICE083",scope:"all disjoint pairs of two proper-width-three CNFs on exactly three shared bits (no private variables)",masks:2**m,disjoint_pairs:disjoint,unique_pairs:unique,both_sources_satisfiable_pairs:bothSat,unique_both_sources_satisfiable_pairs:bothSatUnique,total_valid_interpolants:totalInterpolants,individual_candidate_interpolants_checked:explicitSeparators,source_CNF_masks_checked:ALL+1,assertions:checks,failures,nonuniqueExample,controls,asymptotic_claim:"NONE from finite enumeration. General separator-lattice theorem is symbolic.",status:"COMPUTATIONAL"};
}
console.log(JSON.stringify(audit(),null,2));
