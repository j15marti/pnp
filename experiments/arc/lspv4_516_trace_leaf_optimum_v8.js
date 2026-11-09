// LSPV-4/516 independently executable V8/Node verifier.
// No native FLMV emulator, no historical R_mix341 checker.
function verify() {
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  let checks=0,malformedRejected=0;
  function mk(k,d) {
    let core=[], n=6, clauses=[],gs=[];
    for(let v=0;v<4;v++){
      let es=[];edges.forEach((e,i)=>{if(e.includes(v))es.push(i+1)});
      for(let a=0;a<8;a++){
        let b=[0,1,2].map(j=>(a>>j)&1);
        if((b[0]^b[1]^b[2])!==Number(v===0))
          core.push(es.map((e,j)=>b[j]?-e:e));
      }
    }
    for(let j=0;j<k;j++){
      let g=++n,a=++n,b=++n;gs.push(g);
      let t=((d>>j)&1)?g:-g;
      clauses.push([t,a,b],[t,a,-b],[t,-a,b],[t,-a,-b]);
    }
    let g=gs[0];
    for(let j=1;j<k;j++){
      let x=gs[j],z=++n,u=++n,v=++n;
      clauses.push([-g,z,u],[-g,z,-u],[-x,z,v],[-x,z,-v],[g,x,-z]);
      g=z;
    }
    for(const [a,b,c] of core){
      let h=++n;clauses.push([g,a,h],[-h,b,c]);
    }
    if(n!==19+6*k||clauses.length!==27+9*k||
       clauses.some(c=>new Set(c.map(Math.abs)).size!==3))throw Error('strict-3 source');
    let w=Math.floor(Math.log2(n))+1;
    let bits='10110110'+'1'.repeat(n)+'0';
    for(const c of clauses)for(const x of c)
      bits+=Math.abs(x).toString(2).padStart(w,'0')+(x<0?'1':'0');
    bits+='01';
    return {bits,n,clauses};
  }
  function tagPositions(k) {
    let base=mk(k,0).bits, pos=[];
    for(let j=0;j<k;j++){
      let b=mk(k,2**j).bits, changed=[];
      for(let i=0;i<base.length;i++)if(base[i]!==b[i])changed.push(i);
      if(changed.length!==4)throw Error('non-four tag');
      pos.push(...changed);
    }
    if(new Set(pos).size!==4*k)throw Error('dependent tags');
    return pos;
  }
  function authentic(k,pkt) {
    let expected=mk(k,0).bits, tags=new Set(tagPositions(k));
    if(pkt.length!==expected.length)return false;
    for(let i=0;i<expected.length;i++)
      if(!tags.has(i)&&pkt[i]!==expected[i])return false;
    return true;
  }
  // A positive sign in any of the four pin facets permits that pin g=1.
  // Brute-force every possible 4-bit tag pattern and g,a,b assignment.
  for(let pattern=0;pattern<16;pattern++){
    for(let g=0;g<2;g++){
      let feasible=false;
      for(let a=0;a<2;a++)for(let b=0;b<2;b++){
        let facets=[a||b,a||!b,!a||b,!a||!b];
        if([0,1,2,3].every(j=>(((pattern>>j)&1)?g:!g)||facets[j]))
          feasible=true;
      }
      if(feasible!==(g?pattern!==0:pattern!==15))
        throw Error('pin satisfiability identity');
      checks++;
    }
  }
  const rows=[];
  for(let k=1;k<=10;k++){
    let q=2**k, src=mk(k,0).bits, tags=tagPositions(k);
    let short=new Set(), full=new Set(),shortReads=0,fullReads=0;
    let suffixTest=src.slice(0,-1), headerTest='0'+src.slice(1);
    let fixedIndex=8+(19+6*k)+1;
    let flipped=src.slice(0,fixedIndex)+(src[fixedIndex]==='0'?'1':'0')+src.slice(fixedIndex+1);
    for(const hostile of [suffixTest,headerTest,flipped,src+'0']){
      if(authentic(k,hostile))throw Error('malformed source accepted');
      malformedRejected++;
    }
    for(let d=0;d<q;d++){
      let actual=mk(k,d).bits,obs=[],all=[];
      if(!authentic(k,actual))throw Error('valid source rejected');
      checks++;
      for(let j=0;j<k;j++)
        for(let t=0;t<4;t++)
          all.push([j,t,(d>>j)&1]);
      outer: for(let j=0;j<k;j++)
        for(let t=0;t<4;t++){
          let bit=(d>>j)&1;
          obs.push([j,t,bit]);
          if(bit)break outer;
        }
      let label=d===0?'UNSAT':'SAT';
      short.add(JSON.stringify([obs,label]));
      full.add(JSON.stringify([all,label]));
      shortReads+=obs.length;fullReads+=all.length;
    }
    if(short.size!==k+1 || full.size!==q || shortReads!==5*q-5
      || fullReads!==4*k*q)throw Error('trace count');
    checks+=4;
    rows.push({k,q,source_len:src.length,short_classes:short.size,
      full_scan_classes:full.size,short_tag_reads:shortReads,
      full_tag_reads:fullReads});
  }
  return {status:'PASS',verifier:'V8 / Node.js independent strict-3 source and trace classes',checks,
    gadget_exhaustive_patterns:16,malformedRejected,rows,
    qualifier:'Tag reads EXCLUDE common source-authentication reads. No native FLMV simulation.'};
}
if(typeof module!=='undefined'&&require.main===module)
  console.log(JSON.stringify(verify(),null,2));
