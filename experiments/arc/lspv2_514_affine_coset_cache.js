const result = /* LSPV-2/514, independent JavaScript reference verifier. Node: node lspv2_514_affine_cache.js
   Restricted 3-CNF family only. This is NOT a native FLMV emulator or universal SAT decider. */
(function () {
  "use strict";
  const edges=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
  let asserts=0;
  function check(c,m){asserts++;if(!c)throw Error(m||"assert");}
  function clauses(d){
    const out=[], charges=[1^(d&1),0,0,0];
    for(let v=0;v<4;v++){
      const inc=edges.map((e,i)=>e.includes(v)?i+1:0).filter(x=>x);
      for(let b=0;b<8;b++){
        const bits=[(b>>2)&1,(b>>1)&1,b&1];
        if((bits[0]^bits[1]^bits[2])!==charges[v])
          out.push(inc.map((x,j)=>bits[j]?-x:x));
      }
    }
    for(let j=0;j<7;j++){
      const x=7+3*j;out.push([(d>>(j+1))&1?-x:x,x+1,x+2]);
    }
    return out;
  }
  function pack(C){
    let s="10100101"+C.length.toString(2).padStart(8,"0");
    for(const row of C)for(const l of row)
      s+=Math.abs(l).toString(2).padStart(5,"0")+(l<0?"1":"0");
    return s+"01";
  }
  function parse(s){
    if(!/^[01]+$/.test(s)||s.length<18||s.slice(0,8)!=="10100101")return null;
    const n=parseInt(s.slice(8,16),2);
    if(!n||s.length!==18+18*n||s.slice(-2)!=="01")return null;
    const C=[];
    for(let j=0;j<n;j++){
      const row=[];
      for(let h=0;h<3;h++){
        const i=16+j*18+h*6,v=parseInt(s.slice(i,i+5),2);
        if(!v)return null;
        row.push(s[i+5]==="1"?-v:v);
      }
      if(new Set(row.map(Math.abs)).size!==3)return null;
      C.push(row);
    }
    return C;
  }
  const parent=pack(clauses(0)), template1=pack(clauses(1)), k=8;
  check(parent.length===432,"packet length");
  const masks=Array(parent.length).fill(0);
  for(let j=0;j<8;j++){
    const alt=pack(clauses(1<<j));
    for(let i=0;i<parent.length;i++)if(alt[i]!==parent[i])masks[i]|=1<<j;
  }
  for(let d=0;d<256;d++){
    const p=pack(clauses(d));
    for(let i=0;i<p.length;i++)check((p[i]!==parent[i])===((popcount(masks[i]&d)&1)!==0),"affine bit");
  }
  function popcount(x){let c=0;while(x){c++;x&=x-1}return c}
  for(let d=0;d<2;d++){
    let models=0;
    const core=clauses(d).slice(0,16);
    for(let a=0;a<64;a++){
      if(core.every(row=>row.some(l=>(((a>>(Math.abs(l)-1))&1)===+(l>0)))))
        models++;
    }
    check(models===(d?8:0),"exact K4 parity");
  }
  const tailPositions=Array.from({length:7},(_,j)=>16+(16+j)*18+5);
  function guest(s,r){
    if(s.length!==432||!/^[01]+$/.test(s))return {label:"MALFORMED",read:[]};
    const skip=new Set(tailPositions.slice(r-1)),allTail=new Set(tailPositions);
    let a0=true,a1=true;const read=[];
    for(let i=0;i<s.length;i++){
      if(skip.has(i))continue;
      read.push(i);
      if(allTail.has(i))continue;
      if(s[i]!==parent[i])a0=false;
      if(s[i]!==template1[i])a1=false;
    }
    if(a0||a1)return {label:a0?"UNSAT":"SAT",read};
    return {label:parse(s)?"OUTSIDE_FAMILY":"MALFORMED",read:[]};
  }
  function basis(xs){
    const piv={};
    for(let x of xs){while(x){const bit=Math.floor(Math.log2(x));
      if(piv[bit]===undefined){piv[bit]=x;break}x^=piv[bit];
    }}
    return Object.keys(piv).map(Number).sort((a,b)=>b-a).map(b=>piv[b]);
  }
  const rows=[];
  for(let r=1;r<=8;r++){
    const anchors=[], counts=[],classIds=[];
    let membership=0, referenceRuns=0, policyGuestRuns=0, readProbes=0;
    for(let d=0;d<256;d++){
      const pkt=pack(clauses(d));
      const ground=guest(pkt,r);referenceRuns++;readProbes+=ground.read.length;
      check(ground.label===(d&1?"SAT":"UNSAT"),"both-label");
      let found=-1;
      for(let j=0;j<anchors.length;j++){
        const a=anchors[j];membership++;
        if(a.basis.every(row=>(popcount((d^a.d)&row)&1)===0)){
          found=j;check(a.label===ground.label,"cached label");
          check(a.read.length===ground.read.length,"read length");
          for(let t=0;t<a.read.length;t++){
            const pos=a.read[t];
            check(pos===ground.read[t] && pkt[pos]===a.pkt[pos],"trace value");
          }
          break;
        }
      }
      if(found<0){
        const actual=guest(pkt,r);policyGuestRuns++;
        const b=basis(actual.read.map(i=>masks[i]));
        check(b.length===r,"affine rank");
        anchors.push({d,basis:b,label:actual.label,read:actual.read,pkt});
        found=anchors.length-1;
      }
      classIds.push(found);counts[found]=(counts[found]||0)+1;
    }
    check(anchors.length===(1<<r),"trace count");
    check(counts.every(x=>x===(1<<(8-r))),"equal coset size");
    check(referenceRuns===256 && policyGuestRuns===anchors.length,"policy separation");
    rows.push({rank:r,classes:anchors.length,reuses:256-anchors.length,
      membership_tests:membership,reference_ground_truth_runs:referenceRuns,
      policy_fresh_guest_runs:policyGuestRuns,
      read_probes_no_cache:readProbes,
      retained_basis_anchor_label_bits:anchors.length*(r*8+8+1)});
  }
  const corrupt=[
    "00000000"+parent.slice(8),
    parent.slice(0,-2)+"10",
    parent.slice(0,8)+"00000000"+parent.slice(16),
    parent.slice(0,16)+"00000"+parent.slice(21),
    parent.slice(0,-1),parent+"0"
  ];
  for(const pkt of corrupt)check(guest(pkt,4).label==="MALFORMED","corrupted original source");
  return {assertions:asserts,k,encoded_bits:432,malformed_rejected:corrupt.length,
    rows,status:"FINITE CONTROL ONLY. Independently written V8 version, not native FLMV."};
})();
if (typeof module !== 'undefined' && typeof console !== 'undefined') console.log(JSON.stringify(result,null,2));
