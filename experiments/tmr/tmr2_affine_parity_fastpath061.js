"use strict";
// TMR-2/061: authentic p naff source -> discovered XOR-bilinear basis and raw affine parity -> exact signed-character count.
// Run: node experiments/tmr/tmr2_affine_parity_fastpath061.js
// Host-only bound: d<=12. Uniform mathematical algorithm has no hard cap.
function parseSource(src){
 if(typeof src!=="string"||!/^[\x20-\x7e\n]*$/.test(src))throw Error("Non-ASCII");
 const lines=src.trimEnd().split("\n");if(lines.some(l=>!l||l.trim()!==l))throw Error("Noncanonical");
 const hdr=/^p naff ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)$/.exec(lines.shift()||"");
 if(!hdr)throw Error("Header");const [n,a,b,g,root]=hdr.slice(1).map(Number);
 if([n,a,b,g,root].some(t=>!Number.isSafeInteger(t))||a<1||b<1||n!==a+b||g<3||n>2*g||root<0||root>=g||lines.length!==g)throw Error("Dimensions");
 const gates=Array(g).fill(null),used=new Set(),early=new Set(["E","X"]),post=new Set(["O","A","P","N"]),raw=new Set(["R","L","U"]);
 for(const line of lines){
  let parts=line.split(" "),t=parts[0],sid=parts[1],id=Number(sid);
  if(!["E","X","O","A","P","N","R","L","U","Z"].includes(t)||!/^(0|[1-9][0-9]*)$/.test(sid||"")||!Number.isSafeInteger(id)||id>=g||gates[id])throw Error("Gate identity");
  let arity=["N","R","U"].includes(t)?1:2;
  if(parts.length!==arity+2||parts.slice(2).some(v=>!/^(0|[1-9][0-9]*)$/.test(v)))throw Error("Canonical arguments");
  let c=parts.slice(2).map(Number);if(c.some(v=>!Number.isSafeInteger(v)))throw Error("Unsafe reference");
  if(t==="E"){if(c[0]>=a||c[1]>=b)throw Error("Shore");used.add(c[0]);used.add(a+c[1]);}
  else if(t==="R"){if(c[0]>=n)throw Error("Raw range");used.add(c[0]);}
  else if(c.some(v=>v>=g))throw Error("Child range");
  gates[id]={id,t,c};
 }
 if(used.size!==n||gates[root].t!=="Z"||gates.filter(z=>z.t==="Z").length!==1)throw Error("Coverage/root");
 const kind=id=>early.has(gates[id].t)?"early":post.has(gates[id].t)?"post":raw.has(gates[id].t)?"raw":"root";
 for(const z of gates){
  let types=z.c.map(kind);
  if(z.t==="X"&&types.some(t=>t!=="early"))throw Error("Early phase");
  if(post.has(z.t)&&types.some(t=>t!=="post"&&t!=="early"))throw Error("Post phase");
  if(["L","U"].includes(z.t)&&types.some(t=>t!=="raw"))throw Error("Raw phase");
  if(z.t==="Z"&&(types[0]!=="post"||types[1]!=="raw"))throw Error("Final phase");
 }
 const state=Array(g).fill(0),topo=[];
 function visit(id){
  if(state[id]===1)throw Error("Cycle");if(state[id]===2)return;
  state[id]=1;const z=gates[id];if(z.t!=="E"&&z.t!=="R")for(const c of z.c)visit(c);
  state[id]=2;topo.push(id);
 }
 visit(root);if(topo.length!==g)throw Error("Unreachable");
 const interfaceIDs=[...new Set(gates.filter(z=>post.has(z.t)).flatMap(z=>z.c.filter(id=>kind(id)==="early")))].sort((x,y)=>x-y);
 return {src,n,a,b,g,root,gates,topo,interfaceIDs};
}

function parity(x){let t=0;while(x){t^=1;x&=x-1n;}return t;}

function highestBit(x){return x.toString(2).length-1;}

function spanCompress(vectors){
 const basis=[],pivots=[],masks=[];
 for(const v of vectors){
  let rem=v,combo=0n;
  for(const p of pivots)if(((rem>>BigInt(p.index))&1n)!==0n){rem^=p.vec;combo^=p.combo;}
  if(rem===0n){masks.push(combo);continue;}
  let pos=basis.length,bit=1n<<BigInt(pos);basis.push(v);
  pivots.push({index:highestBit(rem),vec:rem,combo:combo^bit});
  pivots.sort((x,y)=>y.index-x.index);masks.push(bit);
 }
 for(let i=0;i<vectors.length;i++){let rebuild=0n;for(let j=0;j<basis.length;j++)if((masks[i]>>BigInt(j))&1n)rebuild^=basis[j];if(rebuild!==vectors[i])throw Error("Basis mismatch");}
 return {basis,masks,d:basis.length};
}

function solveGF2(rows,width,rhs){
 const m=rows.length,bit=1n<<BigInt(width),mask=bit-1n;
 let A=rows.map((r,i)=>r|(((rhs>>BigInt(i))&1n)<<BigInt(width)));
 const pivots=[];let rank=0;
 for(let col=0;col<width&&rank<m;col++){
  let j=rank;while(j<m&&((A[j]>>BigInt(col))&1n)===0n)j++;
  if(j===m)continue;[A[rank],A[j]]=[A[j],A[rank]];
  for(let i=0;i<m;i++)if(i!==rank&&((A[i]>>BigInt(col))&1n)!==0n)A[i]^=A[rank];
  pivots.push(col);rank++;
 }
 for(let i=rank;i<m;i++)if((A[i]&mask)===0n&&(A[i]&bit)!==0n)return null;
 let solution=0n;for(let i=0;i<rank;i++)if((A[i]&bit)!==0n)solution|=1n<<BigInt(pivots[i]);
 return {solution,rank};
}

function gaussCharacter(M,a,b,linear){
 const xmask=(1n<<BigInt(a))-1n,ymask=(1n<<BigInt(b))-1n,u=linear&xmask,v=(linear>>BigInt(a))&ymask;
 const rows=[],trans=[];
 for(let i=0;i<a;i++)rows.push((M>>BigInt(i*b))&ymask);
 for(let j=0;j<b;j++){let col=0n;for(let i=0;i<a;i++)if((rows[i]>>BigInt(j))&1n)col|=1n<<BigInt(i);trans.push(col);}
 const solY=solveGF2(rows,b,u);if(!solY)return 0n;
 const solX=solveGF2(trans,a,v);if(!solX)return 0n;
 if(solY.rank!==solX.rank)throw Error("Transpose rank");
 return (parity(solX.solution&u)?-1n:1n)*(1n<<BigInt(a+b-solY.rank));
}

function circuitCount(source){
 const p=parseSource(source),mats=Array(p.g).fill(null),raw=Array(p.g).fill(null);
 for(const id of p.topo){const z=p.gates[id],c=z.c;
  if(z.t==="E")mats[id]=1n<<BigInt(c[0]*p.b+c[1]);
  if(z.t==="X")mats[id]=mats[c[0]]^mats[c[1]];
  if(z.t==="R")raw[id]={lin:1n<<BigInt(c[0]),constant:0};
  if(z.t==="L")raw[id]={lin:raw[c[0]].lin^raw[c[1]].lin,constant:raw[c[0]].constant^raw[c[1]].constant};
  if(z.t==="U")raw[id]={lin:raw[c[0]].lin,constant:raw[c[0]].constant^1};
 }
 const vectors=p.interfaceIDs.map(id=>mats[id]),sp=spanCompress(vectors),d=sp.d,size=2**d;
 if(!Number.isSafeInteger(size)||size>4096)throw Error("Host Walsh-table capacity");
 const layer=new Map(p.interfaceIDs.map((id,i)=>[id,sp.masks[i]]));
 const truth=[];
 for(let v=0;v<size;v++){
  const vals=Array(p.g).fill(0),w=BigInt(v);
  for(const id of p.topo){
   const z=p.gates[id],c=z.c;
   if(z.t==="E"||z.t==="X"){if(layer.has(id))vals[id]=parity(w&layer.get(id));}
   else if(z.t==="N")vals[id]=1-vals[c[0]];
   else if(z.t==="O")vals[id]=vals[c[0]]|vals[c[1]];
   else if(z.t==="A")vals[id]=vals[c[0]]&vals[c[1]];
   else if(z.t==="P")vals[id]=vals[c[0]]^vals[c[1]];
  }
  truth.push(vals[p.gates[p.root].c[0]]?-1n:1n);
 }
 for(let step=1;step<size;step*=2)for(let base=0;base<size;base+=2*step)for(let j=0;j<step;j++){
  const x=truth[base+j],y=truth[base+j+step];truth[base+j]=x+y;truth[base+j+step]=x-y;
 }
 const aff=raw[p.gates[p.root].c[1]],den=1n<<BigInt(d),total=1n<<BigInt(p.n);
 let signedNumerator=0n,nonzeroCharacters=0;
 for(let s=0;s<size;s++){
  let M=0n;for(let j=0;j<d;j++)if((s>>j)&1)M^=sp.basis[j];
  const G=gaussCharacter(M,p.a,p.b,aff.lin);if(G!==0n)nonzeroCharacters++;signedNumerator+=truth[s]*G;
 }
 if(aff.constant)signedNumerator=-signedNumerator;
 if(signedNumerator%den!==0n)throw Error("Walsh nonintegrality");
 const signed=signedNumerator/den;if((total-signed)%2n!==0n)throw Error("Parity nonintegrality");
 const count=(total-signed)/2n;if(count<0n||count>total)throw Error("Out of range");
 return {n:p.n,g:p.g,q:vectors.length,d,k:[...new Set(p.gates.filter(z=>z.t==="R").map(z=>z.c[0]))].length,characterTerms:size,nonzeroCharacters,accept:count.toString()};
}

function bruteCount(source){
 const p=parseSource(source);if(p.n>14)throw Error("Exhaustive guard");let count=0n;
 for(let bits=0;bits<2**p.n;bits++){
  const v=Array(p.g).fill(0);
  for(const id of p.topo){let z=p.gates[id],c=z.c;
   if(z.t==="E")v[id]=((bits>>c[0])&1)&((bits>>(p.a+c[1]))&1);
   else if(z.t==="R")v[id]=(bits>>c[0])&1;
   else if(z.t==="X"||z.t==="P"||z.t==="L"||z.t==="Z")v[id]=v[c[0]]^v[c[1]];
   else if(z.t==="O")v[id]=v[c[0]]|v[c[1]];
   else if(z.t==="A")v[id]=v[c[0]]&v[c[1]];
   else if(z.t==="N"||z.t==="U")v[id]=1-v[c[0]];
  }
  count+=BigInt(v[p.root]);
 }return count.toString();
}

function makeSource(a,b,tuples,root){
 const n=a+b,g=tuples.length;
 return "p naff "+[n,a,b,g,root].join(" ")+"\n"+tuples.map((t,i)=>t[0]+" "+i+" "+t.slice(1).join(" ")).join("\n")+"\n";
}

function denseCase(a,b,flip){
 const g=[];for(let i=0;i<a;i++)for(let j=0;j<b;j++)g.push(["E",i,j]);
 let current=0;for(let i=1;i<a*b;i++){g.push(["X",current,i]);current=g.length-1;}
 g.push(["O",current,current]);current=g.length-1;
 if(flip){g.push(["N",current]);current=g.length-1;}
 let previous;for(let i=0;i<a+b;i++){g.push(["R",i]);let rid=g.length-1;if(previous===undefined)previous=rid;else{g.push(["L",previous,rid]);previous=g.length-1;}}
 g.push(["Z",current,previous]);return makeSource(a,b,g,g.length-1);
}

function testAll(){
 let assertions=0,comparisons=0,invalid=0,examples=[];
 function check(name,source,expected=null,brute=true){
  const x=circuitCount(source);assertions++;
  if(expected!==null&&x.accept!==String(expected))throw Error("Expected "+name+" "+x.accept+" != "+expected);
  if(brute){const y=bruteCount(source);comparisons++;assertions++;if(x.accept!==y)throw Error("Mismatch "+name+" "+x.accept+" != "+y);}
  examples.push({name,...x,exhaustive:brute});
 }
 for(let a=1;a<=5;a++)for(let b=1;b<=5;b++)for(let flip=0;flip<=1;flip++){
  const expected=BigInt(flip?1:3)*(1n<<BigInt(a+b-2));
  check(`dense rank-one ${a}x${b} flip=${flip}`,denseCase(a,b,flip),expected.toString());
 }
 const small=makeSource(1,1,[["E",0,0],["X",0,0],["N",1],["R",0],["L",3,3],["U",4],["Z",2,5]],6);
 check("zero coefficient, two constants cancel",small,"0");
 check("NOT edge XOR raw x",makeSource(1,1,[["E",0,0],["N",0],["R",0],["Z",1,2]],3));
 check("independent layer OR, four-bit affine XOR",makeSource(2,2,[["E",0,0],["E",1,1],["O",0,1],["R",0],["R",1],["L",3,4],["R",2],["L",5,6],["R",3],["L",7,8],["Z",2,9]],10));
 const large=denseCase(32,32,0);
 check("1024-edge source, 64 raw probes",large,(3n*(1n<<62n)).toString(),false);
 const bad=[
  small.replace("p naff","p npost"),small.replace("p naff 2 1 1 7 6","p naff 3 1 1 7 6"),
  small.replace("R 3 0","R 3 2"),small.replace("Z 6 2 5","Z 6 2 0"),
  small.replace("X 1 0 0","X 1 5 0"),small.replace("Z 6 2 5","Z 0 2 5"),
  small+"C 8 0 0\n",small.replace("E 0 0 0","E 0 0 0\r"),small.replace("U 5 4","U 5 5")
 ];
 for(const src of bad){let failed=false;try{circuitCount(src);}catch(e){failed=true;}if(!failed)throw Error("Malformed accepted");invalid++;assertions++;}
 return {revision:"TMR2_AFFINE_PARITY_FASTPATH061_v1",seed:20261115,runtime:"V8 Code Mode",checks:assertions,exhaustiveComparisons:comparisons,malformedRejections:invalid,failures:0,largeCase:examples.find(e=>e.name.includes("1024-edge")),examples};
}
console.log(JSON.stringify(testAll(),null,2));
