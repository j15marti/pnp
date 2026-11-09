/* LSPV-2/517, deterministic source-access parity audit. Standalone Node >=18. */
const verify = function jsVerify(){
  const MAGIC="10110110";
  const assert=(x,m)=>{if(!x)throw Error(m||"assert");};
  let tests=0, cases=0, sat=0, unsat=0, localChecks=0, malformed=0;
  let ledger=[];
  function graph(n){
    let s=new Set();
    const add=(a,b)=>s.add(Math.min(a,b)+","+Math.max(a,b));
    if(n===4)for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)add(i,j);
    else {const h=n/2;for(let l=0;l<2;l++)for(let i=0;i<h;i++)add(l*h+i,l*h+(i+1)%h);for(let i=0;i<h;i++)add(i,h+i);}
    let edges=[...s].map(x=>x.split(",").map(Number)).sort((x,y)=>x[0]-y[0]||x[1]-y[1]);
    assert(edges.length===3*n/2,"edge count");tests++;
    return edges;
  }
  function construct(n,d,edges){
    let clauses=[], k=n-1, m=edges.length;
    for(let v=0;v<n;v++){
      let vars=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
      assert(vars.length===3,"cubic");tests++;
      const charge=v<k?(d>>v)&1:0;
      for(let base of [1,2,4,7]){
        let bits=base^charge;
        clauses.push(vars.map((z,i)=>(bits>>i)&1?-z:z));
      }
    }
    const w=Math.ceil(Math.log2(m+1));
    let packet=MAGIC+"1".repeat(m)+"0";
    for(let c of clauses)for(let lit of c)packet+=Math.abs(lit).toString(2).padStart(w,"0")+(lit<0?"1":"0");
    packet+="01";
    return {clauses,packet,w};
  }
  function algebraicSolvable(n,edges,d){
    // Independent exact GF(2) Gaussian elimination. Does not use DPLL.
    const m=edges.length, k=n-1, rows=[];
    for(let v=0;v<n;v++){
      let row=0;
      edges.forEach((edge,i)=>{if(edge.includes(v))row^=(1<<i);});
      rows.push([row,v<k?(d>>v)&1:0]);
    }
    let pivot=0;
    for(let bit=0;bit<m;bit++){
      let t=rows.findIndex((r,i)=>i>=pivot && ((r[0]>>bit)&1));
      if(t<0)continue;
      [rows[pivot],rows[t]]=[rows[t],rows[pivot]];
      for(let i=0;i<n;i++)if(i!==pivot && ((rows[i][0]>>bit)&1)){rows[i][0]^=rows[pivot][0];rows[i][1]^=rows[pivot][1];}
      pivot++;
    }
    assert(pivot===n-1,"connected rank");tests++;
    return !rows.some(([mask,b])=>mask===0 && b!==0);
  }
  function checkLocalFacets(clauses,n,d){
    for(let v=0;v<n;v++){
      let c=clauses.slice(4*v,4*v+4), charge=v<n-1?(d>>v)&1:0;
      for(let a=0;a<8;a++){
        const got=c.every(cl=>cl.some((lit,i)=>{const val=(a>>i)&1;return lit>0?Boolean(val):!val;}));
        assert(got===((a.toString(2).replace(/0/g,"").length&1)===charge),"local 3cnf parity");
        localChecks++;
      }
    }
  }
  for(const n of [4,6,8,10]){
    const edges=graph(n),k=n-1,count=2**k;
    let originals=[], seen=new Set(), countSat=0, countUnsat=0;
    for(let d=0;d<count;d++){
      let {clauses,packet,w}=construct(n,d,edges);
      assert(packet.length===8+edges.length+1+12*n*(w+1)+2,"length");tests++;
      const expectedLabel=(d.toString(2).replace(/0/g,"").length%2===0);
      const fromAlgebra=algebraicSolvable(n,edges,d);
      assert(expectedLabel===fromAlgebra,"GF2/label");tests++;
      checkLocalFacets(clauses,n,d);
      if(d===0)originals=packet.split("");
      let changed=new Set();
      for(let i=0;i<packet.length;i++)if(packet[i]!==originals[i])changed.add(i);
      let predicted=new Set();
      const offset=8+edges.length+1;
      for(let v=0;v<k;v++)if((d>>v)&1)for(let j=0;j<4;j++)predicted.add(offset+(4*v+j)*3*(w+1)+w);
      assert(changed.size===predicted.size && [...changed].every(x=>predicted.has(x)),"affine positions");tests++;
      let transcript=[];
      for(let v=0;v<k;v++)transcript.push(packet[offset+4*v*3*(w+1)+w]);
      const signature=transcript.join("");
      assert(!seen.has(signature),"unique transcript");tests++;
      seen.add(signature);
      if(fromAlgebra){sat++;countSat++;}else{unsat++;countUnsat++;}
      cases++;
    }
    assert(seen.size===count,"all classes");tests++;
    ledger.push({vertices:n,edges:edges.length,k,inputs:count,sat:countSat,unsat:countUnsat,packetBits:8+edges.length+1+12*n*(Math.ceil(Math.log2(edges.length+1))+1)+2,traceClasses:seen.size});
    // Hostile controls exercise simple packet framing checks, not a universal CNF parser.
    const s=originals.join("");
    const validPacket=x=>x.length===s.length && x.startsWith(MAGIC) && x.slice(8,8+edges.length+1)==="1".repeat(edges.length)+"0" && x.endsWith("01");
    for(const corrupt of ["0"+s.slice(1),s.slice(0,-1),s.slice(0,-2)+"00",s.slice(0,8)+"0"+s.slice(9)]){
      assert(!validPacket(corrupt),"corrupt packet accepted");malformed++;tests++;
    }
  }
  assert(cases===680 && sat===340 && unsat===340,"totals");tests++;
  return {status:"COMPUTATIONAL",independent_method:"GF(2) Gaussian elimination plus exhaustive local truth-table checks; no SAT DPLL",sources:cases,sat,unsat,localTruthChecks:localChecks,malformedFrameControls:malformed,assertions:tests,ledger,native_FLMV_executed:false};
};
console.log(JSON.stringify(verify(),null,2));
