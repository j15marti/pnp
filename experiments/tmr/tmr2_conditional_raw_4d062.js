"use strict";
// TMR-2/062: authenticated conditional-affine raw-read shared DAG.
// Source: p ncond n a b g root, exactly g canonical gate records.
// Host tests cap d<=8; the uniform mathematical method has no fixed d cap.
const REV="TMR2_CONDITIONAL_RAW_4D062_v1";
function parity(v){let t=0;while(v){t^=1;v&=v-1n;}return t;}
function parse(src){
 if(typeof src!=="string"||!/^[\x20-\x7e\n]*$/.test(src)||!src.endsWith("\n")||src.endsWith("\n\n"))throw Error("ASCII/termination");
 const lines=src.slice(0,-1).split("\n");
 if(lines.some(s=>!s||s.trim()!==s||s.includes("  ")))throw Error("canonical lines");
 const h=/^p ncond ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)$/.exec(lines.shift()||"");
 if(!h||h.slice(1).some(s=>!/^(0|[1-9][0-9]*)$/.test(s)))throw Error("header");
 const [n,a,b,g,root]=h.slice(1).map(Number);
 if([n,a,b,g,root].some(t=>!Number.isSafeInteger(t))||a<1||b<1||n!==a+b||g<2||n>2*g||root>=g||lines.length!==g)throw Error("dimensions");
 const early=new Set(["E","X"]),post=new Set(["O","A","P","N"]),allowed=new Set(["E","X","O","A","P","N","R","Z"]);
 const gates=Array(g).fill(null),used=new Set();
 for(const line of lines){
  const tok=line.split(" "),t=tok[0],sid=tok[1];
  if(!allowed.has(t)||!/^(0|[1-9][0-9]*)$/.test(sid||""))throw Error("type/id");
  const id=Number(sid);if(!Number.isSafeInteger(id)||id>=g||gates[id])throw Error("id");
  if(tok.length!==(t==="N"?3:4)||tok.slice(2).some(s=>!/^(0|[1-9][0-9]*)$/.test(s)))throw Error("arity/ref syntax");
  const c=tok.slice(2).map(Number);if(c.some(z=>!Number.isSafeInteger(z)))throw Error("unsafe ref");
  if(t==="E"){if(c[0]>=a||c[1]>=b)throw Error("shore");used.add(c[0]);used.add(a+c[1]);}
  else if(t==="R"){if(c[0]>=n||c[1]>=g)throw Error("raw ref");used.add(c[0]);}
  else if(c.some(z=>z>=g))throw Error("ref range");
  gates[id]={t,c,id};
 }
 if(used.size!==n||gates[root].t!=="Z")throw Error("coverage/root");
 const kind=id=>early.has(gates[id].t)?"early":post.has(gates[id].t)?"post":gates[id].t==="R"?"raw":"mix";
 for(const z of gates){
  const children=z.t==="E"?[]:z.t==="R"?[z.c[1]]:z.c,ks=children.map(kind);
  if(z.t==="X"&&ks.some(k=>k!=="early"))throw Error("early restriction");
  if(post.has(z.t)&&ks.some(k=>k!=="early"&&k!=="post"))throw Error("post nonlinear raw");
  if(z.t==="R"&&ks.some(k=>k!=="early"&&k!=="post"))throw Error("raw nonlinear control");
 }
 const state=Array(g).fill(0),order=[];
 function visit(id){if(state[id]===1)throw Error("cycle");if(state[id]===2)return;
  state[id]=1;const z=gates[id],children=z.t==="E"?[]:z.t==="R"?[z.c[1]]:z.c;
  for(const c of children)visit(c);state[id]=2;order.push(id);}
 visit(root);if(order.length!==g)throw Error("unreachable");
 const interfaces=[...new Set(gates.filter(z=>!early.has(z.t)).flatMap(z=>
  (z.t==="R"?[z.c[1]]:z.c).filter(id=>kind(id)==="early")))].sort((x,y)=>x-y);
 return {n,a,b,g,root,gates,order,interfaces};
}
function compress(vecs){
 const basis=[],pivots=[],masks=[];
 for(const v of vecs){
  let rem=v,comb=0n;for(const p of pivots)if((rem>>BigInt(p.bit))&1n){rem^=p.vec;comb^=p.combo;}
  if(!rem){masks.push(comb);continue;}
  const bit=rem.toString(2).length-1,mark=1n<<BigInt(basis.length);
  basis.push(v);pivots.push({bit,vec:rem,combo:comb^mark});
  pivots.sort((x,y)=>y.bit-x.bit);masks.push(mark);
 }
 for(let i=0;i<vecs.length;i++){let got=0n;
  for(let j=0;j<basis.length;j++)if((masks[i]>>BigInt(j))&1n)got^=basis[j];
  if(got!==vecs[i])throw Error("span reconstruction");
 }
 return {basis,masks,d:basis.length};
}
function solve(rows,width,rhs){
 const m=rows.length,bit=1n<<BigInt(width),mask=bit-1n;
 const A=rows.map((v,i)=>v|(((rhs>>BigInt(i))&1n)<<BigInt(width))),pivots=[];
 let rank=0;
 for(let col=0;col<width&&rank<m;col++){
  let j=rank;while(j<m&&!((A[j]>>BigInt(col))&1n))j++;
  if(j===m)continue;[A[j],A[rank]]=[A[rank],A[j]];
  for(let i=0;i<m;i++)if(i!==rank&&((A[i]>>BigInt(col))&1n))A[i]^=A[rank];
  pivots.push(col);rank++;
 }
 for(let i=rank;i<m;i++)if((A[i]&mask)===0n&&(A[i]&bit))return null;
 let x=0n;for(let i=0;i<rank;i++)if(A[i]&bit)x|=1n<<BigInt(pivots[i]);
 return {x,rank};
}
function character(M,a,b,lin){
 const mx=(1n<<BigInt(a))-1n,my=(1n<<BigInt(b))-1n,u=lin&mx,v=(lin>>BigInt(a))&my;
 const rows=Array.from({length:a},(_,i)=>(M>>BigInt(i*b))&my);
 const tr=Array.from({length:b},(_,j)=>{
  let col=0n;for(let i=0;i<a;i++)if((rows[i]>>BigInt(j))&1n)col|=1n<<BigInt(i);
  return col;
 });
 const sy=solve(rows,b,u),sx=solve(tr,a,v);
 if(!sy||!sx)return 0n;
 if(sy.rank!==sx.rank)throw Error("rank transpose");
 return (parity(sx.x&u)?-1n:1n)*(1n<<BigInt(a+b-sy.rank));
}
function count(src){
 const p=parse(src),mats=Array(p.g).fill(0n);
 for(const id of p.order){const z=p.gates[id];if(z.t==="E")mats[id]=1n<<BigInt(z.c[0]*p.b+z.c[1]);
  if(z.t==="X")mats[id]=mats[z.c[0]]^mats[z.c[1]];}
 const sp=compress(p.interfaces.map(id=>mats[id]));
 if(sp.d>8)throw Error("test-harness d cap");
 const co=new Map(p.interfaces.map((id,i)=>[id,sp.masks[i]])),size=2**sp.d;
 let numerator=0n,nonzero=0;const examples=[];
 for(let w=0;w<size;w++){
  const vals=Array(p.g).fill(null),aff=Array(p.g).fill(null),word=BigInt(w);
  for(const id of p.order){const z=p.gates[id],c=z.c;
   if(z.t==="E"||z.t==="X")vals[id]=parity(word&(co.get(id)||0n));
   if(z.t==="O")vals[id]=vals[c[0]]|vals[c[1]];
   if(z.t==="A")vals[id]=vals[c[0]]&vals[c[1]];
   if(z.t==="P")vals[id]=vals[c[0]]^vals[c[1]];
   if(z.t==="N")vals[id]=vals[c[0]]^1;
   if(z.t==="R")aff[id]={lin:vals[c[1]]?1n<<BigInt(c[0]):0n,c:0};
   if(z.t==="Z"){
    const f=aff[c[0]]||{lin:0n,c:vals[c[0]]},h=aff[c[1]]||{lin:0n,c:vals[c[1]]};
    aff[id]={lin:f.lin^h.lin,c:f.c^h.c};
   }
  }
  const final=aff[p.root];if(!final)throw Error("nonaffine root");
  if(size<=8)examples.push({w,linear:final.lin.toString(),constant:final.c});
  for(let lam=0;lam<size;lam++){
   let M=0n;for(let j=0;j<sp.d;j++)if((lam>>j)&1)M^=sp.basis[j];
   const G=character(M,p.a,p.b,final.lin);if(G)nonzero++;
   numerator+=(final.c^parity(BigInt(lam)&word))?-G:G;
  }
 }
 const den=1n<<BigInt(sp.d+1),num=(1n<<BigInt(p.n+sp.d))-numerator;
 if(num%den)throw Error("integer normalization");
 const answer=num/den;
 if(answer<0n||answer>(1n<<BigInt(p.n)))throw Error("range");
 return {n:p.n,g:p.g,q:p.interfaces.length,d:sp.d,rawBits:new Set(p.gates.filter(z=>z.t==="R").map(z=>z.c[0])).size,characters:size*size,nonzeroCharacters:nonzero,accept:answer.toString(),conditional:examples};
}
function brute(src){
 const p=parse(src);if(p.n>14)throw Error("brute cap");let sum=0n;
 for(let x=0;x<2**p.n;x++){
  const v=Array(p.g).fill(0);
  for(const id of p.order){const z=p.gates[id],c=z.c;
   if(z.t==="E")v[id]=((x>>c[0])&1)&((x>>(p.a+c[1]))&1);
   if(z.t==="X"||z.t==="P"||z.t==="Z")v[id]=v[c[0]]^v[c[1]];
   if(z.t==="O")v[id]=v[c[0]]|v[c[1]];
   if(z.t==="A")v[id]=v[c[0]]&v[c[1]];
   if(z.t==="N")v[id]=1-v[c[0]];
   if(z.t==="R")v[id]=((x>>c[0])&1)&v[c[1]];
  }sum+=BigInt(v[p.root]);
 }return sum.toString();
}
function source(a,b,arr,root=arr.length-1){return "p ncond "+[a+b,a,b,arr.length,root].join(" ")+"\n"+arr.map((z,i)=>[z[0],i,...z.slice(1)].join(" ")).join("\n")+"\n";}
function dense(a,b,omitFirst){
 const gs=[];for(let i=0;i<a;i++)for(let j=0;j<b;j++)gs.push(["E",i,j]);
 let w=0;for(let i=1;i<a*b;i++){gs.push(["X",w,i]);w=gs.length-1;}
 const zero=gs.length;gs.push(["X",w,w]);let cur=zero;
 for(let i=0;i<a+b;i++){gs.push(["R",i,(omitFirst&&i===0)?zero:w]);const r=gs.length-1;
  gs.push(["Z",cur,r]);cur=gs.length-1;}
 return source(a,b,gs,cur);
}
function randomSource(a,b,seed){
 let x=seed>>>0;function rnd(n){x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)%n;}
 const gs=[],leaves=[];for(let i=0;i<a;i++){leaves.push(gs.length);gs.push(["E",i,i%b]);}
 for(let j=0;j<b;j++){leaves.push(gs.length);gs.push(["E",j%a,j]);}
 let c=leaves[0];for(let i=1;i<leaves.length;i++){gs.push([["O","P","A"][rnd(3)],c,leaves[i]]);c=gs.length-1;}
 if(rnd(2)){gs.push(["N",c]);c=gs.length-1;}
 let root=c;for(let i=0;i<a+b;i++){gs.push(["R",i,c]);const r=gs.length-1;
  gs.push(["Z",root,r]);root=gs.length-1;}
 return source(a,b,gs,root);
}
function tests(){
 const cases=[];let checks=0,compared=0,invalid=0;
 function check(name,src,expected=null,exhaustive=true){
  const r=count(src);checks++;
  if(expected!==null&&r.accept!==String(expected))throw Error(name+" expected "+expected+" actual "+r.accept);
  if(exhaustive){const ref=brute(src);checks++;compared++;if(ref!==r.accept)throw Error(name+" brute "+ref+" actual "+r.accept);}
  cases.push({name,...r,exhaustive});
 }
 check("nonseparable cubic",source(2,1,[["E",0,0],["X",0,0],["R",1,0],["Z",2,1]]),"1");
 check("DISJ1 complement",source(1,1,[["E",0,0],["N",0],["X",0,0],["Z",1,2]]),"3");
 check("zero rank raw",source(1,1,[["E",0,0],["X",0,0],["N",1],["R",0,2],["Z",3,1]]),"2");
 for(let a=1;a<=4;a++)for(let b=1;b<=4;b++){
  check("dense cancellation "+a+","+b,dense(a,b,false),"0");
  if(a>=2)check("dense all 64 raw gates "+a+","+b,dense(a,b,true),(1n<<BigInt(a+b-3)).toString());
 }
 for(let seed=1;seed<=72;seed++){const a=1+seed%4,b=1+Math.floor(seed/4)%4;
  check("seeded mixed "+seed,randomSource(a,b,20261116^seed));}
 const d=4,gs=[];for(let i=0;i<d;i++)gs.push(["E",i,i]);
 let cur=0;for(let i=1;i<d;i++){gs.push(["O",cur,i]);cur=gs.length-1;}
 gs.push(["X",0,0]);gs.push(["Z",cur,gs.length-1]);
 check("DISJ4",source(d,d,gs),(4n**4n-3n**4n).toString());
 check("64-bit conditional raw",dense(32,32,true),(1n<<61n).toString(),false);
 const tiny=source(2,1,[["E",0,0],["X",0,0],["R",1,0],["Z",2,1]]);
 const bad=[tiny.replace("p ncond","p naff"),tiny.replace("ncond 3 2 1","ncond 3 2 2"),tiny.replace("R 2 1 0","R 2 3 0"),tiny.replace("Z 3 2 1","Z 3 3 1"),tiny.replace("Z 3 2 1","A 3 2 1"),tiny.replace("R 2 1 0","R 2 1 2"),tiny.replace("R 2 1 0","R 2 1 99"),tiny.replace("X 1 0 0","X 1 2 0"),tiny.replace("E 0 0 0","E 0 0 0\r"),tiny+"\nBAD\n",tiny+"\n",tiny.slice(0,-1),tiny.replace("Z 3 2 1","Z 0 2 1")];
 for(const src of bad){let failed=false;try{count(src);}catch(e){failed=true;}if(!failed)throw Error("accepted malformed");checks++;invalid++;}
 return {revision:REV,seed:20261116,runtime:"V8 Code Mode",checks,exhaustiveComparisons:compared,malformedRejections:invalid,failures:0,large:cases.find(z=>z.name==="64-bit conditional raw"),cases};
}
console.log(JSON.stringify(tests(),null,2));
