"use strict";
// TMR-2/060: Authenticated two-stage shared DAG, GF(2) bilinear-span compression, exact integer Walsh count.
// Run: node experiments/tmr/tmr2_post_bilinear_span060.js
// The V8 harness limits the Walsh table to 2^16 entries; the mathematical algorithm is parameterized by d.
function parseSource(source) {
  if(typeof source!=="string"||!/^[\x20-\x7e\n]*$/.test(source))throw Error("Non-ASCII source");
  let lines=source.trimEnd().split("\n");
  if(!lines.length || lines.some(x=>x.length===0||x.trim()!==x))throw Error("Noncanonical lines");
  let hdr=/^p npost ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)$/.exec(lines.shift());
  if(!hdr)throw Error("Header");
  let [n,a,b,g,root]=hdr.slice(1).map(Number);
  if([n,a,b,g,root].some(x=>!Number.isSafeInteger(x)))throw Error("Unsafe index");
  if(a<1||b<1||n!==a+b||g<2||n>2*g||root<0||root>=g||lines.length!==g)throw Error("Dimensions");
  let gates=Array(g).fill(null), usedX=new Set(),usedY=new Set();
  for(const line of lines){
    let t=line.split(" "), type=t[0],id=Number(t[1]);
    if(!["E","X","O","A","P","N"].includes(type)||!Number.isSafeInteger(id)||id<0||id>=g||gates[id])throw Error("Gate ID");
    const expected=(type==="N"?3:4);
    if(t.length!==expected ||t.slice(2).some(x=>!/^[0-9]+$/.test(x)))throw Error("Arity");
    let c=t.slice(2).map(Number);
    if(c.some(x=>!Number.isSafeInteger(x)))throw Error("Indices");
    if(type==="E"){
      if(c[0]>=a||c[1]>=b)throw Error("Edge shore");
      usedX.add(c[0]);usedY.add(c[1]);
    }else if(c.some(j=>j<0||j>=g))throw Error("Child range");
    gates[id]={id,type,c};
  }
  if(usedX.size!==a||usedY.size!==b||["E","X"].includes(gates[root].type))throw Error("Uncovered inputs or early root");
  for(const gate of gates){
    if(gate.type==="X" && gate.c.some(j=>!["E","X"].includes(gates[j].type)))throw Error("Bad early dependence");
  }
  let state=Array(g).fill(0), topo=[];
  function visit(id){
    if(state[id]===1)throw Error("Cycle");
    if(state[id]===2)return;
    state[id]=1;let gate=gates[id];
    if(gate.type!=="E")for(const j of gate.c)visit(j);
    state[id]=2;topo.push(id);
  }
  visit(root);
  if(topo.length!==g)throw Error("Unreachable gate");
  let interfaceIDs=[...new Set(gates.filter(x=>!["E","X"].includes(x.type)).flatMap(x=>x.c.filter(j=>["E","X"].includes(gates[j].type))))].sort((x,y)=>x-y);
  return {source,n,a,b,g,root,gates,topo,interfaceIDs};
}

function highestBit(x) {return x.toString(2).length-1;}

function spanCompress(vectors) {
  let basis=[],pivots=[],masks=[];
  for(const v of vectors){
    let rem=v,old=0n;
    for(const p of pivots){
      if((rem>>BigInt(p.p))&1n){rem^=p.vec;old^=p.combo;}
    }
    if(rem===0n){masks.push(old);continue;}
    const pos=basis.length,bit=1n<<BigInt(pos);
    basis.push(v);
    pivots.push({p:highestBit(rem),vec:rem,combo:old^bit});
    pivots.sort((a,b)=>b.p-a.p);
    masks.push(bit);
  }
  for(let i=0;i<vectors.length;i++){
    let rebuild=0n;
    for(let j=0;j<basis.length;j++)if((masks[i]>>BigInt(j))&1n)rebuild^=basis[j];
    if(rebuild!==vectors[i])throw Error("Basis reconstruction");
  }
  return {basis,masks,d:basis.length};
}

function rankGF2(mask,a,b){
  let rows=[],low=(1n<<BigInt(b))-1n;
  for(let i=0;i<a;i++)rows.push((mask>>BigInt(i*b))&low);
  let r=0;
  for(let j=b-1;j>=0 && r<a;j--){
    const bit=1n<<BigInt(j);
    let pivot=r;
    while(pivot<a&&(rows[pivot]&bit)===0n)pivot++;
    if(pivot===a)continue;
    [rows[r],rows[pivot]]=[rows[pivot],rows[r]];
    for(let i=r+1;i<a;i++)if((rows[i]&bit)!==0n)rows[i]^=rows[r];
    r++;
  }
  return r;
}

function parity(bits){
  let p=0;while(bits){p^=1;bits&=bits-1n;}return p;
}

function circuitCount(source){
  const p=parseSource(source);
  let mats=Array(p.g).fill(null);
  for(const i of p.topo){
    let z=p.gates[i], t=z.type;
    if(t==="E")mats[i]=1n<<BigInt(z.c[0]*p.b+z.c[1]);
    else if(t==="X")mats[i]=mats[z.c[0]]^mats[z.c[1]];
  }
  const vectors=p.interfaceIDs.map(i=>mats[i]);
  const sp=spanCompress(vectors),d=sp.d, size=2**d;
  if(!Number.isSafeInteger(size)||size>65536)throw Error("Harness limit: dimension > 16");
  const layer=new Map(p.interfaceIDs.map((id,j)=>[id,sp.masks[j]]));
  const truth=new Array(size);
  for(let i=0;i<size;i++){
    const w=BigInt(i),v=Array(p.g).fill(0);
    for(const id of p.topo){
      let z=p.gates[id], t=z.type;
      if(t==="E"||t==="X"){
        if(layer.has(id))v[id]=parity(w&layer.get(id));
      }else if(t==="N")v[id]=1-v[z.c[0]];
      else if(t==="O")v[id]=v[z.c[0]]|v[z.c[1]];
      else if(t==="A")v[id]=v[z.c[0]]&v[z.c[1]];
      else if(t==="P")v[id]=v[z.c[0]]^v[z.c[1]];
    }
    truth[i]=BigInt(v[p.root]);
  }
  let had=truth.slice();
  for(let block=1;block<size;block*=2){
    for(let base=0;base<size;base+=block*2){
      for(let j=0;j<block;j++){
        const x=had[base+j],y=had[base+block+j];
        had[base+j]=x+y;had[base+block+j]=x-y;
      }
    }
  }
  let numerator=0n,rankProfile=[];
  for(let s=0;s<size;s++){
    let mm=0n;
    for(let j=0;j<d;j++)if((s>>j)&1)mm^=sp.basis[j];
    let r=rankGF2(mm,p.a,p.b);
    rankProfile.push(r);
    numerator+=had[s]*(1n<<BigInt(p.n-r));
  }
  let denominator=1n<<BigInt(d);
  if(numerator%denominator!==0n)throw Error("Nonintegral Walsh count");
  let total=numerator/denominator;
  if(total<0n||total>(1n<<BigInt(p.n)))throw Error("Count range");
  return {n:p.n,g:p.g,q:vectors.length,d,accept:total.toString(),rankProfile};
}

function bruteCount(source){
  let p=parseSource(source),sum=0n;
  if(p.n>16)throw Error("Brute limit");
  for(let mask=0;mask<2**p.n;mask++){
    let v=Array(p.g).fill(0);
    for(const id of p.topo){
      let g=p.gates[id],t=g.type;
      if(t==="E")v[id]=((mask>>g.c[0])&1)&((mask>>(p.a+g.c[1]))&1);
      else if(t==="X"||t==="P")v[id]=v[g.c[0]]^v[g.c[1]];
      else if(t==="O")v[id]=v[g.c[0]]|v[g.c[1]];
      else if(t==="A")v[id]=v[g.c[0]]&v[g.c[1]];
      else if(t==="N")v[id]=1-v[g.c[0]];
    }
    sum+=BigInt(v[p.root]);
  }
  return sum.toString();
}

function makeSource(a,b,gates,root){
  return `p npost ${a+b} ${a} ${b} ${gates.length} ${root}\n`+
  gates.map((t,id)=>t[0]+" "+id+" "+t.slice(1).join(" ")).join("\n")+"\n";
}

function orAllParities(d){
  let gates=[],leaves=[];
  for(let i=0;i<d;i++)gates.push(["E",i,i]);
  for(let mask=1;mask<2**d;mask++){
    const bits=[];for(let i=0;i<d;i++)if((mask>>i)&1)bits.push(i);
    let cur=bits[0];
    for(let j=1;j<bits.length;j++){cur=gates.length;gates.push(["X",j===1?bits[0]:cur-1,bits[j]]);}
    leaves.push(cur);
  }
  while(leaves.length>1){
    const next=[];for(let i=0;i<leaves.length;i+=2){
      if(i+1<leaves.length){let id=gates.length;gates.push(["O",leaves[i],leaves[i+1]]);next.push(id);}
      else next.push(leaves[i]);
    }leaves=next;
  }
  return makeSource(d,d,gates,leaves[0]);
}

function testAll(){
  let results=[],checks=0,invalids=0;
  function check(name,source,expect,qExpected,dExpected,brute=true){
    const r=circuitCount(source);checks++;
    if(expect!==null&&r.accept!==String(expect))throw Error("Expected count "+name+" "+r.accept+" vs "+expect);
    if(qExpected!==null&&r.q!==qExpected)throw Error("q "+name+" "+r.q+" != "+qExpected);
    if(dExpected!==null&&r.d!==dExpected)throw Error("d "+name+" "+r.d+" != "+dExpected);
    if(brute){let b=bruteCount(source);checks++;if(b!==r.accept)throw Error("Brute mismatch "+name);}
    results.push({name,...r,brute});
  }
  let sx=makeSource(1,1,[["E",0,0],["P",0,0]],1);
  check("zero X(E,E)",sx,0,1,1);
  check("NOT edge",makeSource(1,1,[["E",0,0],["N",0]],1),3,1,1);
  check("repeat OR",makeSource(1,1,[["E",0,0],["O",0,0]],1),1,1,1);
  check("two-edge conjunction",makeSource(2,2,[["E",0,0],["E",1,1],["A",0,1]],2),1,2,2);
  check("post Boolean blend",makeSource(3,3,[["E",0,0],["E",1,1],["E",2,2],["X",0,1],["X",1,2],["N",3],["O",5,4],["A",6,0],["P",7,2]],8),null,4,3);
  for(let d=2;d<=6;d++){
    let src=orAllParities(d),q=2**d-1;
    check("all nonzero parity layers d="+d,src,(4n**BigInt(d)-3n**BigInt(d)).toString(),q,d,true);
  }
  for(let d=2;d<=5;d++){
    let gates=[];for(let i=0;i<d;i++)gates.push(["E",i,i]);
    let cur=d;gates.push(["O",0,1]);for(let i=2;i<d;i++){cur=gates.length;gates.push(["O",cur-1,i]);}
    const last=gates.length;gates.push(["N",cur]);
    check("DISJ_"+d,makeSource(d,d,gates,last),(3n**BigInt(d)).toString(),d,d);
  }
  const bad=[
    sx.replace("p npost 2 1 1 2 1","p npost 3 1 1 2 1"),
    sx.replace("P 1 0 0","P 1 1 0"),
    sx.replace("E 0 0 0","E 0 1 0"),
    sx.replace("P 1 0 0","X 1 0 0"),
    sx.replace("P 1 0 0","P 0 0 0"),
    sx.replace("P 1 0 0","O 1 9 0"),
    sx+"extra\n",
    sx.replace("P 1 0 0","P 1 0 0\x01")
  ];
  for(const badsource of bad){let ok=false;try{circuitCount(badsource);}catch(e){ok=true;}if(!ok)throw Error("Bad source accepted");invalids++;}
  return {revision:"TMR2_POST_BILINEAR_SPAN060_v1",seed:20261115,runtime:"V8 Code Mode",method:"exact integer Walsh-Fourier, GF2 span and matrix rank, independent original-input exhaustive evaluator",assertions:checks+invalids,failures:0,malformedRejections:invalids,cases:results};
}
console.log(JSON.stringify(testAll(),null,2));
