// LSPV-1/514: self-checking independent JavaScript source-and-sparse-XOR control.
// Source/AND3/XOR fragment only; NOT an execution of historical R_mix341 checker.
function sparseTree514() {
  function family(name,h) {
    let E=[];
    if(name==="K4"){h=4;for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)E.push([a,b]);}
    else if(name==="K33"){h=6;for(let a=0;a<3;a++)for(let b=3;b<6;b++)E.push([a,b]);}
    else if(name==="cube"){h=8;for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)if(((a^b).toString(2).match(/1/g)||[]).length===1)E.push([a,b]);}
    else if(name==="prism"){let r=h/2;const S=new Map();for(let i=0;i<r;i++)for(let [a,b] of [[i,(i+1)%r],[i+r,(i+1)%r+r],[i,i+r]]){let x=Math.min(a,b),y=Math.max(a,b);S.set(x+","+y,[x,y]);}E=[...S.values()];}
    else throw Error("family");
    E.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
    if(E.length!==3*h/2||Array.from({length:h},(_,v)=>E.filter(e=>e.includes(v)).length).some(d=>d!==3)) throw Error("not cubic");
    return {h,E};
  }
  function gen(h,E,odd){
    const C=[];
    for(let v=0;v<h;v++){const xs=E.map((e,j)=>e.includes(v)?j+1:0).filter(Boolean);
      for(let k=0;k<8;k++){const p=((k&1)+((k>>1)&1)+((k>>2)&1))%2;
        if(p!==(v===0&&odd?1:0))C.push(xs.map((id,j)=>(k>>j)&1?-id:id));
      }
    }
    return C;
  }
  function sourceCheck(h,E,C,odd){
    for(let v=0;v<h;v++){const G=C.slice(4*v,4*v+4),xs=E.map((e,j)=>e.includes(v)?j+1:0).filter(Boolean);
      if(G.length!==4||G.some(c=>c.length!==3||c.some(l=>!xs.includes(Math.abs(l)))))throw Error("source group");
      for(let a=0;a<8;a++){
        const assign=new Set(xs.filter((_,j)=>Boolean(a&(1<<j))));
        const sat=G.every(c=>c.some(l=>l>0?assign.has(l):!assign.has(-l)));
        if(sat!==(((a&1)+((a>>1)&1)+((a>>2)&1))%2===(v===0&&odd?1:0)))throw Error("wrong parity");
      }
    }
  }
  function merge(A,B){
    let i=0,j=0,out=[],comparisons=0;
    while(i<A.length&&j<B.length){comparisons++;
      if(A[i]===B[j]){i++;j++}else if(A[i]<B[j])out.push(A[i++]);else out.push(B[j++]);
    }
    out.push(...A.slice(i),...B.slice(j));
    return {out,comparisons};
  }
  const cases=[];let corruptRejected=0;
  for(let [name,h0] of [["K4",4],["K33",6],["cube",8],["prism",16],["prism",64],["prism",256],["prism",1024]]) {
    const {h,E}=family(name,h0),clauses=gen(h,E,true);
    if(clauses.length!==4*h)throw Error("source size");
    sourceCheck(h,E,clauses,true);
    let work=0,cmp=0,xors=0,maxwidth=0,live=0,peakAlloc=0;
    function sub(lo,hi){
      if(hi-lo===1){const m=E.map((e,j)=>e.includes(lo)?j+1:0).filter(Boolean);live+=m.length;return {mask:m,rhs:lo===0?1:0};}
      const mid=(lo+hi)>>1,L=sub(lo,mid),R=sub(mid,hi),z=merge(L.mask,R.mask);
      const independent=new Set(L.mask);
      for(const id of R.mask){if(independent.has(id))independent.delete(id);else independent.add(id);}
      if(z.out.length!==independent.size||z.out.some(v=>!independent.has(v)))throw Error("independent row mismatch");
      work+=L.mask.length+R.mask.length;cmp+=z.comparisons;xors++;maxwidth=Math.max(maxwidth,z.out.length);
      peakAlloc=Math.max(peakAlloc,live+z.out.length);live+=z.out.length-L.mask.length-R.mask.length;
      return {mask:z.out,rhs:L.rhs^R.rhs};
    }
    const root=sub(0,h);
    if(root.rhs!==1||root.mask.length||live||xors!==h-1)throw Error("no UNSAT");
    if(work>3*h*Math.ceil(Math.log2(h))||peakAlloc>4.5*h)throw Error("cost invariant");
    cases.push({family:name,h,edges:E.length,original_clauses:clauses.length,paid_nodes:4*h-1,source_truth_assignments_checked:8*h,xor_operand_entries:work,merge_id_comparisons:cmp,max_xor_row_width:maxwidth,simultaneous_allocate_before_free_row_entries:peakAlloc});
    const malformed=[C=>C[0][0]*=-1,C=>C.pop()];
    for(const f of malformed){const bad=clauses.map(row=>row.slice());f(bad);
      try{sourceCheck(h,E,bad,true);}catch(e){corruptRejected++;continue;}throw Error("corrupt accepted");
    }
    try{sourceCheck(h,E,gen(h,E,false),true);}catch(e){corruptRejected++;continue;}throw Error("even parity accepted");
  }
  return {status:"PASS",scope:"separate source/AND3/XOR balanced tree, not native full R_mix341",cases,negative_source_controls_rejected:corruptRejected};
}
if (typeof module !== "undefined") module.exports = sparseTree514;
console.log(JSON.stringify(sparseTree514(),null,2));
