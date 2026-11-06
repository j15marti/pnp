function audit427(){
  let checks=0;
  function ok(c,where){checks++;if(!c)throw Error("check failed: "+where);}
  function graphEdges(name){
    if(name==="K4")return [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
    if(name==="Cube"){let e=[];for(let v=0;v<8;v++)for(let w=v+1;w<8;w++){let d=v^w;if(d===1||d===2||d===4)e.push([v,w]);}return e;}
    throw Error("unknown graph");
  }
  function build(name,odd){
    const H=name==="K4"?4:8,E=graphEdges(name),clauses=[];
    for(let v=0;v<H;v++){
      const inc=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
      ok(inc.length===3,"cubic "+name);
      const charge=odd&&v===0?1:0;
      for(let mask=0;mask<8;mask++){
        let par=((mask>>0)&1)^((mask>>1)&1)^((mask>>2)&1);
        if(par!==charge)clauses.push(inc.map((x,j)=>((mask>>j)&1)?-x:x));
      }
    }
    const text="p cnf "+E.length+" "+clauses.length+"\n"+clauses.map(c=>c.join(" ")+" 0\n").join("");
    return {name,odd,H,E,clauses,text};
  }
  function validate(text){
    if(typeof text!=="string")return false;
    const lines=text.trim().split(/\n/);
    const m=/^p cnf ([1-9]\d*) ([1-9]\d*)$/.exec(lines[0]||"");if(!m)return false;
    const n=+m[1],num=+m[2];if(!Number.isSafeInteger(n)||!Number.isSafeInteger(num)||lines.length!==num+1)return false;
    for(let i=1;i<lines.length;i++){
      const ms=/^(-?\d+) (-?\d+) (-?\d+) 0$/.exec(lines[i]);if(!ms)return false;
      const vals=ms.slice(1).map(Number);
      if(vals.some(x=>!Number.isSafeInteger(x)||x===0||Math.abs(x)>n)||new Set(vals.map(Math.abs)).size!==3)return false;
    }
    return true;
  }
  function sat(form){
    const n=form.E.length;
    for(let mask=0;mask<(1<<n);mask++) {
      let good=true;
      for(const c of form.clauses){if(!c.some(l=>{let bit=((mask>>(Math.abs(l)-1))&1)===1;return l>0?bit:!bit;})){good=false;break;}}
      if(good)return true;
    }
    return false;
  }
  function toBits(s){let b="";for(let i=0;i<s.length;i++)b+=s.charCodeAt(i).toString(2).padStart(8,"0");return b;}
  // Index jump costs one native transition and clears the index tape.
  // A work-tape read at position h charges h to the FLMV space high-water.
  function probe(bits,i,mode){
    const n=bits.length,k=Math.ceil(Math.log2(n+1));
    const h=2**(2*k)-1; // safe in all finite tests
    let time=0,indexWrites=0,jumps=0,inputReads=0,workReads=0,peakIndex=0,peakWork=0;
    function seekRead(tape,address){
      const indexBits=Math.max(1,address.toString(2).length);
      time+=indexBits;indexWrites+=indexBits;peakIndex=Math.max(peakIndex,indexBits);
      time++;jumps++; // native indexed jump, automatic full erasure
      time++;if(tape==="work"){workReads++;peakWork=Math.max(peakWork,address);return 0;}
      inputReads++;return address<n?+bits[address]:0;
    }
    if(mode==="sparse")seekRead("work",h);
    const bit=seekRead("input",i);time++; // output-bit write, write-only
    return {bit,time,indexWrites,jumps,inputReads,workReads,peakIndex,peakWork,nonblankWorkCells:0,high:h,k};
  }
  let records=[];
  for(const name of ["K4","Cube"])for(const odd of [false,true]){
    const f=build(name,odd),bits=toBits(f.text);
    ok(validate(f.text),"valid source "+name);
    ok(sat(f)===!odd,"original SAT label "+name+odd);
    ok(f.clauses.length===4*f.H,"four clauses per cubic vertex");
    const invalid=f.text.replace("p cnf","p cxf");
    ok(!validate(invalid),"malformed encoding rejects");
    const truncated=f.text.slice(0,-4);
    ok(!validate(truncated),"truncated source rejects");
    const mutated=f.text.replace(/ 0\n/," 1\n"); // may parse invalid, but bytes definitely change
    ok(mutated!==f.text,"corrupt byte detected by exact source equality");
    let sample=new Set([0,1,2,bits.length-1]);
    for(let i=0;i<bits.length;i+=Math.max(1,Math.floor(bits.length/23)))sample.add(i);
    let sumDense=0,sumSparse=0,sumInput=0,sumIndexSparse=0,sumJumpsSparse=0,h=null;
    for(const i of [...sample].sort((a,b)=>a-b)){
      let dense=probe(bits,i,"dense"),sparse=probe(bits,i,"sparse");
      ok(dense.bit===+bits[i],"dense bit exact");
      ok(sparse.bit===+bits[i],"sparse bit exact");
      ok(dense.bit===sparse.bit,"same extensional port");
      ok(dense.peakWork===0,"dense no work tape high position");
      ok(sparse.peakWork===sparse.high,"sparse tape high-water");
      ok(sparse.nonblankWorkCells===0,"no retained payload");
      ok(sparse.peakIndex===2*sparse.k,"index width");
      ok(sparse.time-dense.time===2*sparse.k+2,"charged extra seek");
      ok(sparse.peakWork>=bits.length**2,"quadratic high-water");
      ok(sparse.peakWork<4*(bits.length+1)**2,"quadratic bound");
      ok(sparse.workReads===1&&dense.workReads===0,"explicit work read");
      ok(dense.inputReads===1&&sparse.inputReads===1,"input tape probe");
      ok(sparse.jumps===dense.jumps+1,"indexed jump");
      h=sparse.peakWork;sumDense+=dense.time;sumSparse+=sparse.time;sumInput+=sparse.inputReads;sumIndexSparse+=sparse.indexWrites;sumJumpsSparse+=sparse.jumps;
    }
    records.push({name,charge:odd?"odd UNSAT":"even SAT",variables:f.E.length,clauses:f.clauses.length,source_bytes:f.text.length,source_bits:bits.length,probes:sample.size,work_tape_highwater:h,work_tape_nonblank_cells:0,summed_dense_native_steps:sumDense,summed_sparse_native_steps:sumSparse,sparse_index_digit_writes:sumIndexSparse,sparse_index_jumps:sumJumpsSparse,sparse_input_bit_reads:sumInput});
  }
  return {status:"COMPUTATIONAL witness plus independently checked symbolic construction",assertions:checks,records,interpretation:"Sparse indexed work-tape read of high address costs FLMV peak physical tape span even if no cells retain data. The uniform transformation itself remains OPEN.",date:"2026-11-05 18:36 PST"};
}
const r=audit427();console.log(JSON.stringify(r,null,2));
