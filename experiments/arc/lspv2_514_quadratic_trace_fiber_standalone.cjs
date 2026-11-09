// LSPV-2/514. Third independent hosted JavaScript verifier, generated from exact tested function source.
// Run: node lspv2_514_quadratic_trace_fiber_standalone.cjs
function verify514(){
  let assertions=0;
  const a=(cond,msg)=>{assertions++;if(!cond)throw Error(msg)};
  const ed4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  function core(odd){
    let cl=[];
    for(let v=0;v<4;v++){
      let ids=ed4.map((e,j)=>e.includes(v)?j+1:0).filter(z=>z>0);
      for(let t=0;t<8;t++){
        let b=[t>>2&1,t>>1&1,t&1];
        if((b[0]^b[1]^b[2])!==(odd&&v===0?1:0))cl.push(ids.map((id,j)=>[id,b[j]]));
      }
    }
    return cl;
  }
  function packet(edges,d,odd){
    let m=edges.length,cl=core(odd),y=[];
    for(let j=0;j<m;j++){let [u,v]=edges[j],vbit=(1-d[u])*(1-d[v]);y.push(vbit);cl.push([[7+3*j,vbit],[8+3*j,0],[9+3*j,0]]);}
    const width=Math.floor(Math.log2(6+3*m))+1;let s="10100101"+"1".repeat(m)+"0",positions=[];
    for(let k=0;k<cl.length;k++){
      a(cl[k].length===3&&new Set(cl[k].map(x=>x[0])).size===3,"proper clause");
      for(let j=0;j<3;j++){
        s+=cl[k][j][0].toString(2).padStart(width,"0");
        if(k>=16&&j===0)positions.push(s.length);
        s+=String(cl[k][j][1]);
      }
    }
    s+="01";return {s,positions,y};
  }
  const cases=[
    ["empty4",4,[],16,203],
    ["single3",3,[[0,1]],6,267],
    ["path4",4,[[0,1],[1,2],[2,3]],8,299],
    ["cycle4",4,[[0,1],[1,2],[2,3],[0,3]],7,375],
    ["triangle3",3,[[0,1],[1,2],[0,2]],4,299],
    ["K4",4,ed4,5,413],
    ["disjoint5",5,[[0,1],[2,3]],18,283],
    ["ladder8",8,[[0,1],[1,2],[2,3],[4,5],[5,6],[6,7],[0,4],[1,5],[2,6],[3,7]],41,567]
  ];
  let summary=[];
  for(let [name,n,edges,count,length] of cases){
    let anchor=packet(edges,Array(n).fill(1),true);
    a(anchor.s.length===length,`${name} length actual=${anchor.s.length} expected=${length}`);
    let coverCount=0,images=new Set();
    for(let mask=0;mask<2**n;mask++){
      let bits=Array.from({length:n},(_,i)=>mask>>i&1),child=packet(edges,bits,true);
      let cover=edges.every(([u,v])=>bits[u]===1||bits[v]===1);
      a((child.s===anchor.s)===cover,`${name} descriptor=${mask} fiber`);
      a(child.y.every(z=>z===0)===cover,`${name} descriptor=${mask} quadratic polynomial`);
      a(child.positions.join(",")===anchor.positions.join(","),`${name} stable coordinates`);
      if(cover)coverCount++;
      images.add(child.s);
    }
    a(coverCount===count,`${name} #VertexCover`);
    a(packet(edges,Array(n).fill(1),false).s!==anchor.s,`${name} even charge control`);
    summary.push({name,n,edges:edges.length,descriptors:2**n,compatible:coverCount,unique_virtual_sources:images.size,packet_bits:anchor.s.length});
  }
  a(summary.reduce((s,v)=>s+v.descriptors,0)===368,"total descriptors");
  a(summary.reduce((s,v)=>s+v.compatible,0)===105,"total compatible");
  return {status:"PASS",assertions,summary,limitations:"Host JS verifier only; no native FLMV or R_mix341 execution. All tails are semantically irrelevant to odd-charge K4 UNSAT core."};
}
if (typeof console !== 'undefined') console.log(JSON.stringify(verify514(),null,2));
