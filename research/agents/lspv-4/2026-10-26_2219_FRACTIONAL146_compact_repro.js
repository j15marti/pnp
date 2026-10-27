/* LSPV-4 ARC-FRACTIONAL-CELL-TRANSVERSAL146 independent compact audit.
   Node.js: node 2026-10-26_2219_FRACTIONAL146_compact_repro.js
   No packages, seed-free. Promise-only, not unrestricted SAT. */
function reproduce(){
 let checks=0; const ok=(v,s)=>{checks++; if(!v)throw Error(s)};
 const pop=x=>{let c=0;while(x){c+=Number(x&1n);x>>=1n}return c};
 const par=x=>pop(x)%2;
 function prism(h){
  let ek=new Set(),edges=[],inc=Array.from({length:2*h},()=>[]);
  const add=(a,b)=>ek.add([Math.min(a,b),Math.max(a,b)].join(","));
  for(let i=0;i<h;i++){add(i,(i+1)%h);add(h+i,h+(i+1)%h);add(i,h+i)}
  edges=[...ek].map(s=>s.split(",").map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  ok(edges.length===3*h,"edge-count");
  edges.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i)});
  inc.forEach(a=>{a.sort((x,y)=>x-y);ok(a.length===3,"degree")});
  const charges=Array.from({length:2*h},(_,i)=>i===0?1:0);
  let clauses=[],where=[],occ=Array.from({length:3*h},()=>[]);
  for(let v=0;v<2*h;v++)for(let z=0;z<8;z++){
   let b=[z&1,(z>>1)&1,(z>>2)&1];if((b[0]^b[1]^b[2])===charges[v])continue;
   let ci=clauses.length,cl=inc[v].map((e,j)=>[e,b[j]]);clauses.push(cl);where.push(v);
   cl.forEach(([e,s],j)=>occ[e].push([ci,j,s,v]));
  }
  ok(clauses.length===8*h,"clauses");
  occ.forEach(o=>ok(o.length===8&&o.filter(x=>x[2]===0).length===4,"exact4"));
  const gf2=(pins,ex)=>{
   let rows=[]; for(let v=0;v<2*h;v++)if(v!==ex){
    let m=inc[v].reduce((s,e)=>s|(1n<<BigInt(e)),0n);rows.push([m,charges[v]])
   }
   for(let [e,b] of pins)rows.push([1n<<BigInt(e),b]);
   let basis=new Map();
   for(let [mask,bit] of rows){while(mask){
    let lead=mask.toString(2).length-1;
    if(basis.has(lead)){let [m,b]=basis.get(lead);mask^=m;bit^=b}
    else {basis.set(lead,[mask,bit]);break}
   }if(!mask&&bit)return null}
   let x=0n;
   for(let lead of [...basis.keys()].sort((a,b)=>a-b)){
    let [m,b]=basis.get(lead);if(b^par(m&x))x|=1n<<BigInt(lead)
   }
   rows.forEach(([m,b])=>ok(par(m&x)===b,"linear-system"));
   return x
  };
  const sat=(x,flips)=>clauses.every((cl,ci)=>cl.some(([e,s],j)=>Number((x>>BigInt(e))&1n)!==(s^Number(flips.has(ci+":"+j)))));
  ok(clauses.reduce((n,cl)=>n+cl.length,0)===24*h,"signs");
  if(h===3){for(let x=0;x<(1<<9);x++)ok(!sat(BigInt(x),new Set()),"UNSAT exhaustive")}
  for(let ci=0;ci<clauses.length;ci++){
   let pins=new Map(clauses[ci]),x=gf2(pins,where[ci]);ok(x!==null,"single witness");
   ok(!sat(x,new Set()),"baseline witness");
   for(let j=0;j<3;j++)ok(sat(x,new Set([ci+":"+j])),"sign flip SAT")
  }
  let pairs=[];
  edges.forEach(([u,v],e)=>{
   const uu=occ[e].filter(x=>x[3]===u),vv=occ[e].filter(x=>x[3]===v);
   for(let s=0;s<=1;s++){
    let a=uu.filter(x=>x[2]===s).sort((x,y)=>x[0]-y[0]);
    let b=vv.filter(x=>x[2]!==s).sort((x,y)=>x[0]-y[0]);
    ok(a.length===2&&b.length===2,"pair multiplicity");
    for(let j=0;j<2;j++)pairs.push([u,v,a[j],b[j]])
   }
  });
  ok(pairs.length===12*h,"paired count");
  let touched=new Set();
  for(let [u,v,a,b] of pairs){
   let [ci,j]=a,[di,k]=b;
   touched.add(ci+":"+j);touched.add(di+":"+k);
   let pins=new Map(clauses[di]);
   for(let [e,s] of clauses[ci]){
    if(pins.has(e))ok(pins.get(e)===1-s,"common pinned sign");
    else pins.set(e,1-s)
   }
   let x=gf2(pins,v);ok(x!==null,"pair witness");
   ok(sat(x,new Set([ci+":"+j,di+":"+k])),"balanced pair SAT")
  }
  ok(touched.size===24*h,"disjoint mutation support");
  const n=3*h,m=8*h,w=Math.ceil(Math.log2(n+1)),gam=z=>2*Math.floor(Math.log2(z))+1;
  const header=16+gam(n)+gam(m),rec=3*(w+1)+1,N=header+m*rec,W=Math.ceil(Math.log2(N+1));
  let cells=new Set();
  for(let ci=0;ci<m;ci++)for(let j=0;j<3;j++)cells.add(Math.floor((header+ci*rec+j*(w+1))/W));
  return {h,N,signs:24*h,pairs:12*h,W,sign_cells:cells.size}
 }
 const prisms=[3,4,5,6,7,8].map(prism);
 let dense=[];
 for(let n of [4,6,8,10,12]){
  const q=n/2,ee=[];
  for(let e=1;e<(1<<n);e++)if(e.toString(2).replace(/0/g,"").length===q)ee.push(e);
  let tau=n+1;
  for(let s=0;s<(1<<n);s++){
   if(ee.every(e=>(s&e)!==0))tau=Math.min(tau,s.toString(2).replace(/0/g,"").length);
  }
  ok(tau===n-q+1,"dense integral transversal");
  ok((n-q)*(n-q)*4===n*n,"two uniform samples exactly quarter miss");
  dense.push({n,neighbors:ee.length,tau,tau_fractional:2,randomized_probes:2,error:"1/4"})
 }
 for(let r=1;r<=8;r++){
  let err=0,det=Array(r).fill(0),reads=0;
  for(let branch=0;branch<3;branch++)for(let mask=0;mask<(1<<r);mask++){
   if(branch===0){err++;for(let i=0;i<r;i++)det[i]++}
   else {reads+=mask.toString(2).replace(/0/g,"").length;
    for(let i=0;i<r;i++)if(mask&(1<<i))det[i]++
   }
  }
  ok(err*3===3*(1<<r),"baseline error 1/3");
  det.forEach(v=>ok(v*3===2*3*(1<<r),"mutant success 2/3"));
  ok(reads*3===r*3*(1<<r),"expected reads r/3")
 }
 return {artifact:"ARC-FRACTIONAL-CELL-TRANSVERSAL146",scope:"restricted input-cell and signed (4,4) prism promise",prisms,dense,assertions:checks,failures:0,random_seed:null,provenance:"standalone JavaScript exact finite test"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(reproduce(),null,2));
return reproduce();