"use strict";
// TMR-5/059 independently executed exact raw-probe Fourier/GF2 verifier.
function parity(x){let k=0;while(x){x&=x-1n;k^=1}return k}

function source(a,b,g,root=g.length-1){return "p nraw "+(a+b)+" "+a+" "+b+" "+g.length+" "+root+"\n"+g.map((r,i)=>[r[0],i,...r.slice(1)].join(" ")).join("\n")+"\n"}

function parse(src){
 if(typeof src!=="string"||!/^[ -~\n]+$/.test(src)||!src.endsWith("\n"))throw Error("ASCII");
 const lines=src.trimEnd().split("\n"),head=lines.shift().split(" ");
 if(head.length!==7||head[0]!=="p"||head[1]!=="nraw"||head.slice(2).some(s=>!/^(0|[1-9]\d*)$/.test(s)||s.length>8))throw Error("header");
 const [n,a,b,g,root]=head.slice(2).map(Number);
 if(a<1||b<1||n!==a+b||g<2||n>2*g||root>=g||lines.length!==g)throw Error("dimension");
 let gates=Array(g).fill(null),ux=new Set(),uy=new Set(),probes=new Set();
 for(const line of lines){
  if(line.trim()!==line||line.includes("  "))throw Error("line");
  const t=line.split(" "),kind=t[0];if(!"EXROAPN".includes(kind)||t.slice(1).some(s=>!/^(0|[1-9]\d*)$/.test(s)||s.length>8))throw Error("gate");
  const args=t.slice(1).map(Number),id=args.shift();if(id>=g||gates[id]||args.length!==("RN".includes(kind)?1:2))throw Error("arity/id");
  if(kind==="E"){if(args[0]>=a||args[1]>=b)throw Error("edge");ux.add(args[0]);uy.add(args[1]);}
  else if(kind==="R"){if(args[0]>=n)throw Error("raw");probes.add(args[0]);}
  else if(args.some(x=>x>=g))throw Error("child");
  gates[id]={kind,args};
 }
 if(ux.size!==a||uy.size!==b||"EX".includes(gates[root].kind))throw Error("coverage/root");
 for(const v of gates)if(v.kind==="X"&&v.args.some(j=>!"EX".includes(gates[j].kind)))throw Error("early type");
 const seen=Array(g).fill(0),topo=[];
 function visit(i){if(seen[i]===1)throw Error("cycle");if(seen[i]===2)return;seen[i]=1;const v=gates[i];if(!"ER".includes(v.kind))for(const j of v.args)visit(j);seen[i]=2;topo.push(i)}
 visit(root);if(topo.length!==g)throw Error("unreachable");
 const interfaceIDs=[...new Set(gates.filter(t=>!"EX".includes(t.kind)&&t.kind!=="R").flatMap(t=>t.args).filter(i=>"EX".includes(gates[i].kind)))].sort((x,y)=>x-y);
 return {n,a,b,g,root,gates,topo,interfaceIDs,probes:[...probes].sort((x,y)=>x-y)};
}

function span(vectors){
 const bases=[],pivots=[],coords=[];
 for(const v of vectors){
  let rem=v,m=0n;
  for(const [bit,red,combo] of pivots.slice().sort((x,y)=>y[0]-x[0]))if((rem>>BigInt(bit))&1n){rem^=red;m^=combo}
  if(rem){const bit=bases.length;bases.push(v);pivots.push([rem.toString(2).length-1,rem,m^(1n<<BigInt(bit))]);m=1n<<BigInt(bit)}
  coords.push(m)
 }
 for(let i=0;i<vectors.length;i++){let sum=0n;for(let j=0;j<bases.length;j++)if((coords[i]>>BigInt(j))&1n)sum^=bases[j];if(sum!==vectors[i])throw Error("span witness")}
 return {bases,coords};
}

function solve(rows,rhs,cols){
 let a=rows.map((v,i)=>[v,Number((rhs>>BigInt(i))&1n)]),piv=[],r=0;
 for(let col=0;col<cols&&r<a.length;col++){
  let j=r;while(j<a.length&&!((a[j][0]>>BigInt(col))&1n))j++;if(j===a.length)continue;
  [a[r],a[j]]=[a[j],a[r]];
  for(let z=0;z<a.length;z++)if(z!==r&&((a[z][0]>>BigInt(col))&1n)){a[z][0]^=a[r][0];a[z][1]^=a[r][1]}
  piv.push(col);r++;
 }
 if(a.some(([v,bit])=>v===0n&&bit===1))return null;
 let ans=0n;for(let i=0;i<piv.length;i++)if(a[i][1])ans|=1n<<BigInt(piv[i]);
 if(rows.some((row,i)=>parity(row&ans)!==Number((rhs>>BigInt(i))&1n)))throw Error("solve");
 return {ans,rank:r};
}

function gamma(mat,p,pattern){
 const pinned=new Map(p.probes.map((index,i)=>[index,(pattern>>i)&1]));
 const ux=Array.from({length:p.a},(_,i)=>i).filter(i=>!pinned.has(i));
 const uy=Array.from({length:p.b},(_,j)=>j).filter(j=>!pinned.has(p.a+j));
 let rows=[],alpha=0n,beta=0n,c=0;
 for(let t=0;t<ux.length;t++){
  const i=ux[t];let row=0n,q=0;
  for(let h=0;h<uy.length;h++)if((mat>>BigInt(i*p.b+uy[h]))&1n)row|=1n<<BigInt(h);
  for(let j=0;j<p.b;j++)if(pinned.has(p.a+j)&&((mat>>BigInt(i*p.b+j))&1n))q^=pinned.get(p.a+j);
  rows.push(row);if(q)alpha|=1n<<BigInt(t);
 }
 for(let h=0;h<uy.length;h++){let q=0;for(let i=0;i<p.a;i++)if(pinned.has(i)&&((mat>>BigInt(i*p.b+uy[h]))&1n))q^=pinned.get(i);if(q)beta|=1n<<BigInt(h)}
 for(let i=0;i<p.a;i++)if(pinned.has(i))for(let j=0;j<p.b;j++)if(pinned.has(p.a+j)&&((mat>>BigInt(i*p.b+j))&1n))c^=pinned.get(i)&pinned.get(p.a+j);
 const s=solve(rows,alpha,uy.length);if(!s)return 0n;
 const trans=uy.map((_,j)=>rows.reduce((acc,row,i)=>acc|=(((row>>BigInt(j))&1n)<<BigInt(i)),0n));
 const t=solve(trans,beta,ux.length);if(!t)return 0n;
 const z=1n<<BigInt(ux.length+uy.length-s.rank);
 return (c^parity(alpha&t.ans))?-z:z;
}

function count(src){
 const p=parse(src),mats=Array(p.g).fill(null);
 for(const id of p.topo){const t=p.gates[id];if(t.kind==="E")mats[id]=1n<<BigInt(t.args[0]*p.b+t.args[1]);else if(t.kind==="X")mats[id]=mats[t.args[0]]^mats[t.args[1]]}
 const {bases,coords}=span(p.interfaceIDs.map(i=>mats[i])),d=bases.length,k=p.probes.length;
 if(d>12)throw Error("finite tester dimension guard");
 const leaves=new Map(p.interfaceIDs.map((id,i)=>[id,coords[i]]));let numerator=0n,size=1<<d;
 for(let pat=0;pat<(1<<k);pat++){
  let table=[];
  for(let w=0;w<size;w++){
   const v=Array(p.g).fill(0),raw=new Map(p.probes.map((i,j)=>[i,(pat>>j)&1]));
   for(const id of p.topo){
    const t=p.gates[id],a=t.args;
    if("EX".includes(t.kind)){if(leaves.has(id))v[id]=parity(BigInt(w)&leaves.get(id));}
    else if(t.kind==="R")v[id]=raw.get(a[0]);
    else if(t.kind==="N")v[id]=1-v[a[0]];
    else if(t.kind==="O")v[id]=v[a[0]]|v[a[1]];
    else if(t.kind==="A")v[id]=v[a[0]]&v[a[1]];
    else v[id]=v[a[0]]^v[a[1]];
   }table.push(v[p.root]);
  }
  for(let block=1;block<size;block*=2)for(let i=0;i<size;i+=2*block)for(let j=0;j<block;j++){let x=table[i+j],y=table[i+j+block];table[i+j]=x+y;table[i+j+block]=x-y}
  for(let z=0;z<size;z++)if(table[z]){let mat=0n;for(let j=0;j<d;j++)if((z>>j)&1)mat^=bases[j];numerator+=BigInt(table[z])*gamma(mat,p,pat)}
 }
 if(numerator%(1n<<BigInt(d)))throw Error("denominator");
 const answer=numerator/(1n<<BigInt(d));if(answer<0n||answer>(1n<<BigInt(p.n)))throw Error("range");
 return {answer:answer.toString(),d,k,q:p.interfaceIDs.length,n:p.n,g:p.g};
}

function brute(src){
 const p=parse(src);if(p.n>12)throw Error("brute guard");
 let sum=0;
 for(let bits=0;bits<(1<<p.n);bits++){
  const val=Array(p.g).fill(0);
  for(const id of p.topo){const t=p.gates[id],a=t.args;
   if(t.kind==="E")val[id]=((bits>>a[0])&1)&((bits>>(p.a+a[1]))&1);
   else if(t.kind==="R")val[id]=(bits>>a[0])&1;
   else if(t.kind==="N")val[id]=1-val[a[0]];
   else if(t.kind==="O")val[id]=val[a[0]]|val[a[1]];
   else if(t.kind==="A")val[id]=val[a[0]]&val[a[1]];
   else val[id]=val[a[0]]^val[a[1]];
  }sum+=val[p.root]
 }return sum;
}

function tests(){
 let checks=0,examples=[];
 const controls=[
  ["raw-read-break",source(1,1,[["E",0,0],["R",0],["O",0,1]]),2],
  ["mixed-affine",source(1,1,[["E",0,0],["R",0],["P",0,1],["R",1],["P",2,3]]),3],
  ["unique",source(1,1,[["E",0,0],["R",0],["A",0,1],["R",1],["A",2,3]]),1],
  ["DISJ2",source(2,2,[["E",0,0],["E",1,1],["O",0,1],["N",2]]),9],
  ["cancel",source(1,1,[["E",0,0],["X",0,0],["R",0],["P",1,2]]),2]
 ];
 for(const [name,s,expected] of controls){const r=count(s),b=brute(s);if(Number(r.answer)!==expected||b!==expected)throw Error("control "+name);checks+=2;examples.push({name,answer:r.answer,d:r.d,k:r.k})}
 let seed=20261115>>>0;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
 for(let z=0;z<180;z++){
  const a=1+rnd(3),b=1+rnd(3),g=[],early=[];
  for(let i=0;i<a;i++){early.push(g.length);g.push(["E",i,i%b])}
  for(let j=0;j<b;j++){early.push(g.length);g.push(["E",j%a,j])}
  const extras=1+rnd(4);
  for(let i=0;i<extras;i++){let u=early[rnd(early.length)],v=early[rnd(early.length)];early.push(g.length);g.push(["X",u,v])}
  let top=early[0];for(const leaf of early.slice(1)){g.push(["X",top,leaf]);top=g.length-1}
  g.push(["N",top]);let root=g.length-1;
  const pins=Array.from({length:a+b},(_,i)=>i);
  for(let i=pins.length-1;i>0;i--){const j=rnd(i+1);[pins[i],pins[j]]=[pins[j],pins[i]]}
  const k=rnd(a+b+1);
  for(const pin of pins.slice(0,k)){g.push(["R",pin]);let p=g.length-1;g.push([["O","A","P"][rnd(3)],root,p]);root=g.length-1}
  let s=source(a,b,g,root),x=count(s),y=brute(s);
  if(Number(x.answer)!==y)throw Error("full source mismatch");
  checks++;
 }
 const p={a:2,b:2,probes:[]};let gaussian=0;
 for(let mat=0;mat<16;mat++)for(let pins=0;pins<16;pins++){
  const selected=[0,1,2,3].filter(i=>(pins>>i)&1);p.probes=selected;
  for(let pattern=0;pattern<(1<<selected.length);pattern++){
   const fixed=new Map(selected.map((s,j)=>[s,(pattern>>j)&1]));let val=0;
   for(let v=0;v<16;v++){if(selected.some((s)=>(v>>s&1)!==fixed.get(s)))continue;let bit=0;for(let i=0;i<2;i++)for(let j=0;j<2;j++)bit^=((mat>>(2*i+j))&1)&((v>>i)&1)&((v>>(j+2))&1);val+=bit?-1:1}
   if(BigInt(val)!==gamma(BigInt(mat),p,pattern))throw Error("Gauss sum mismatch");gaussian++;
  }
 }
 const malformed=[controls[0][1].replace("p nraw","p npost"),controls[0][1].replace("E 0 0 0","E 0 2 0"),controls[0][1].replace("O 2 0 1","X 2 0 1"),controls[0][1].replace("O 2 0 1","O 2 2 1"),controls[0][1]+"garbage\n"];
 for(const s of malformed){let rejected=false;try{count(s)}catch(e){rejected=true}if(!rejected)throw Error("invalid accepted");checks++}
 return {revision:"TMR5_RAWPROBE_AFFINE_JS059_V1",seed:20261115,source_cases:controls.length+180,checks,quadratic_character_checks:gaussian,malformed:malformed.length,failures:0,controls:examples};
}

console.log(JSON.stringify(tests(),null,2));
