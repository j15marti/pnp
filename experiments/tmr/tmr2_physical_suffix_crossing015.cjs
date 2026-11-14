'use strict';
// TMR-2/015 independently executable physical one-head crossing and SAT controls.
// Node.js: node experiments/tmr/tmr2_physical_suffix_crossing015.cjs
const independentTruth=function(bits) {
  if (bits.length%3!==0) return "MALFORMED";
  for (let a=0;a<8;a++) {
    let ok=true;
    for(let i=0;i<bits.length;i+=3){const mask=4*bits[i]+2*bits[i+1]+bits[i+2];if(mask===a){ok=false;break}}
    if(ok)return "SAT";
  }
  return "UNSAT";
};
const fixedLabel=function(bits) {
  if(bits.length%3!==0)return "MALFORMED";
  let seen=0;
  for(let i=0;i<bits.length;i+=3)seen|=(1<<(4*bits[i]+2*bits[i+1]+bits[i+2]));
  return seen===255?"UNSAT":"SAT";
};
const runPhysical=function(bits) {
  const L=bits.length, crossings=Array.from({length:L+1},()=>[]);
  let pos=0, parity=0,last=null, prepass=0;
  for(let i=0;i<=L;i++){
    const old=pos;
    if(old>=1&&old<=L){last=bits[old-1];parity^=last}
    pos++;prepass++;crossings[old].push(["F",last,parity]);
  }
  if(pos!==L+1)throw Error("forward end marker");
  for(let i=L;i>=0;i--){pos--;prepass++;crossings[pos].push(["B",last,parity]);}
  if(pos!==0)throw Error("left reset");
  if(parity===0){
    for(let i=0;i<=L;i++){const old=pos;pos++;prepass++;crossings[old].push(["EF",last,parity]);}
    for(let i=L;i>=0;i--){pos--;prepass++;crossings[pos].push(["EB",last,parity]);}
  }
  if(pos!==0||prepass!==2*(L+1)*(1+(parity===0?1:0)))throw Error("charged prepass");
  for(let i=0;i<=L;i++){
    const c=crossings[i];
    if(c.length!==(parity===0?4:2)||c[1][0]!=="B"||c[1][2]!==parity)throw Error("crossing count");
    if(i>0&&c[0][1]!==bits[i-1])throw Error("forward captured source bit");
  }
  const label=fixedLabel(bits);
  if(label!==independentTruth(bits))throw Error("SAT label mismatch");
  return {label,parity,crossings,prepass,total:prepass+L+2};
};
const audit=function() {
  const out={mode:"fully charged single-head physical prepass; 3-variable 3-CNF fallback",exhaustive:0,fixture:0,bitflips:0,conditional_code_fibers:0,tail_states:0,transitions:0,SAT:0,UNSAT:0,MALFORMED:0,failed:0,fixture_details:[]};
  for(let K=0;K<=10;K++){
    const n=1<<K;
    for(let x=0;x<n;x++){
      const bits=Array.from({length:K},(_,i)=>(x>>i)&1);
      const r=runPhysical(bits);
      out.exhaustive++;out.transitions+=r.total;out[r.label]++;
      for(let i=0;i<K;i++){
        const code=[r.crossings[i+1][0][1],r.crossings[i+1][1][2]];
        if(code[0]!==bits[i]||code[1]!==r.parity)throw Error("crossing-derived code");
        out.tail_states++;
        const other=bits.slice();other[i]^=1;
        const s=runPhysical(other);
        if(s.parity===r.parity)throw Error("parity nonflip");
        if(r.crossings.some((c,j)=>c.length===s.crossings[j].length))throw Error("crossing lengths not global");
        for(let cut=0;cut<=i;cut++)if(r.crossings[cut][1][2]===s.crossings[cut][1][2])throw Error("future depends on later bit");
        out.bitflips++;
        const s0=bits.slice();s0[i]=0;
        const s1=bits.slice();s1[i]=1;
        const a=runPhysical(s0),b=runPhysical(s1);
        const c0=[a.crossings[i+1][0][1],a.crossings[i+1][1][2]].join("");
        const c1=[b.crossings[i+1][0][1],b.crossings[i+1][1][2]].join("");
        if(c0===c1||c0.length!==2||c1.length!==2)throw Error("conditional prefix-free fail");
        out.conditional_code_fibers++;
      }
    }
  }
  const asbits=m=>[(m>>2)&1,(m>>1)&1,m&1];
  const pats=[Array(24).fill(0),Array.from({length:8},(_,i)=>asbits(i)).flat(),Array.from({length:8},(_,i)=>asbits(7-i)).flat()];
  let z=20261114>>>0;
  for(let j=0;j<256;j++){
    const arr=[];
    for(let b=0;b<24;b++){z=(Math.imul(1664525,z)+1013904223)>>>0;arr.push((z>>>31)&1)}
    pats.push(arr);
  }
  for(let j=0;j<pats.length;j++){
    const r=runPhysical(pats[j]);out.fixture++;out.transitions+=r.total;out[r.label]++;
    if(j<3)out.fixture_details.push({bits:pats[j].join(""),label:r.label,parity:r.parity,prepass:r.prepass,transitions:r.total,per_cut_crossings:r.crossings[0].length});
  }
  out.total=out.exhaustive+out.fixture;
  return out;
};
if(typeof module!=='undefined'&&require.main===module){process.stdout.write(JSON.stringify(audit(),null,2)+'\n')}
