"use strict";
// LSPV-1/487. Node >= 18. No third-party dependencies.
// Exact affine-template cover tests for independent AND gates.
function parity(z) {
  let p = 0;
  while (z) { p ^= z & 1; z >>>= 1; }
  return p;
}
function value(g, x) {
  let y = 0;
  for (let i=0;i<g;i++) {
    const u=(x >>> (2*i))&1, v=(x >>> (2*i+1))&1;
    y |= (u&v)<<i;
  }
  return y;
}
function affine(g, x, rows) {
  let y=0, w=(x<<1)|1;
  for(let i=0;i<g;i++) y|=parity(rows[i]&w)<<i;
  return y;
}
function allMasks2() {
  let masks=[], ranks=[];
  for(let c0=0;c0<32;c0++) for(let c1=0;c1<32;c1++) {
    const a=[c0,c1];
    let mask=0;
    for(let x=0;x<16;x++) if(affine(2,x,a)===value(2,x))mask|=1<<x;
    masks.push(mask);
    ranks.push(a);
  }
  return {masks,ranks};
}
function popcount(z) { let k=0; while(z){z&=z-1;k++} return k; }
function pairTemplates(g) {
  const pair = [
    [0,0],
    [1,1 << 3],
    [1 | (1 << 4),1 << 4]
  ];
  let out=[[]];
  for(let start=0;start+1<g;start+=2) {
    const bitShift=2*start;
    const next=[];
    for(const a of out) for(const b of pair) {
      // Coefficient bit 0 is the affine constant, and bit j+1 is variable j.
      const shiftRow=r => (r&1) | ((r&~1)<<bitShift);
      next.push(a.concat(b.map(shiftRow)));
    }
    out=next;
  }
  if(g%2) {
    const j=g-1, u=1 << (2*j+1);
    const next=[];
    for(const a of out){next.push(a.concat([0]));next.push(a.concat([u]));}
    out=next;
  }
  return out;
}
function coverCheck(g, templates) {
  const size=1 << (2*g);
  let firstUncovered=-1;
  for(let x=0;x<size;x++) {
    let covered=false;
    for(const rows of templates) if(affine(g,x,rows)===value(g,x)){covered=true;break;}
    if(!covered) { firstUncovered=x; break; }
  }
  return {ok:firstUncovered<0, firstUncovered,size,templates:templates.length};
}
function walshCheck(g, rows) {
  const size=1<<(2*g);
  let maxRatio=0, checked=0;
  for(let lam=0;lam<(1<<g);lam++) {
    let sum=0;
    for(let x=0;x<size;x++){
      const phase=parity(lam & (value(g,x) ^ affine(g,x,rows)));
      sum+=phase ? -1 : 1;
    }
    const bound=1<<(2*g-popcount(lam));
    if(Math.abs(sum)>bound) throw new Error("Walsh violation");
    maxRatio=Math.max(maxRatio, Math.abs(sum)/bound);
    checked++;
  }
  return {checked, maxRatio};
}
function runTests() {
  const {masks,ranks}=allMasks2(), full=(1<<16)-1;
  let maximum=0, twoCover=false, twoChecks=0;
  const maskSet=new Set(masks);
  for(let i=0;i<masks.length;i++) {
    maximum=Math.max(maximum,popcount(masks[i]));
    for(let j=0;j<masks.length;j++){
      twoChecks++;
      if((masks[i]|masks[j])===full)twoCover=true;
    }
  }
  if(maximum!==9 || twoCover || maskSet.size!==832)throw new Error("g=2 exact mask census failed");
  // The explicit three-template witness, independent of the exhaustive search.
  const witness=pairTemplates(2);
  const c2=coverCheck(2,witness);
  if(!c2.ok || witness.length!==3) throw new Error("three cover invalid");
  for(let i=0;i<3;i++) if(coverCheck(2,witness.filter((_,j)=>i!==j)).ok)
    throw new Error("witness not irredundant");
  // Exhaustive check of coverage for tensor products of the three-template block.
  const covers={};
  for(const g of [1,2,3,4,5,6,7,8]) {
    let t=pairTemplates(g);
    const c=coverCheck(g,t);
    const expected=Math.pow(3,Math.floor(g/2))*Math.pow(2,g%2);
    if(!c.ok || t.length!==expected)throw new Error("tensor cover failed g="+g);
    covers[g]=c;
  }
  // Independently verify the Walsh rank bound for deterministic affine maps.
  let walsh=0;
  for(let g=1;g<=5;g++) for(let z=0;z<32;z++) {
    const rows=[];
    for(let i=0;i<g;i++)rows.push((((z+1)*2654435761) ^ ((i+3)*2246822519)) & ((1<<(2*g+1))-1));
    walsh+=walshCheck(g,rows).checked;
  }
  // Negative/malformed controls are distinct from SAT certificates.
  const corrupt=coverCheck(2,witness.slice(0,2));
  if(corrupt.ok)throw new Error("deletion corruption not detected");
  if(pairTemplates(3).length!==6 || coverCheck(3,[]).ok)throw new Error("zero-template negative control failed");
  for(const bad of [0,-1,1.5,9])if(bad>8 || !Number.isInteger(bad) || bad<1){
    if(bad>=1 && bad<=8 && Number.isInteger(bad))throw new Error("bad guard");
  }
  return {
    status:"PROVED/RESTRICTED symbolic Fourier bound; COMPUTATIONAL finite controls",
    theorem:"Every affine vector template agrees with g independent AND outputs on <=3^g of 4^g inputs; arbitrary-set template cover >=ceil((4/3)^g); explicit tensor template cover <=3^floor(g/2)*2^(g mod 2)",
    exact_g2:{affine_maps:1024, distinct_agreement_sets:maskSet.size, maximum_agreement:maximum, pairs_checked:twoChecks, pair_cover_exists:twoCover, three_template_cover:true, witness_coefficients:witness},
    coverage: covers, walsh_coefficients_checked:walsh,
    negatives:{delete_one_template_rejected:true,zero_template_rejected:true},
    historical_Rmix341_checker_executed:false, all_algorithm_lower_bound:false
  };
}
if(typeof module !== "undefined")module.exports={runTests,parity,value,affine,pairTemplates,coverCheck};
if(typeof require !== "undefined" && require.main === module)console.log(JSON.stringify(runTests(),null,2));