"use strict";
const range=n=>Array.from({length:n},(_,i)=>i);
function assert(b,s){if(!b)throw Error(s)}
function xorParity(x){let z=0;while(x){z^=1;x&=x-1}return z}
function build(m,control=false){
 let n=4*m,G=[],layers=[],pins=[],mk=(op,a,b,stage)=>{let z=n++;G.push({op,a,b,z,stage});return z};
 let P,Q,S,T,old;
 for(let i=0;i<m;i++){
  let [x,y,u,v]=range(4).map(j=>4*i+j), start=G.length;
  let L=mk("xor",x,y,i),M=mk("xor",u,v,i);
  let l=mk("xor",x,y,i),t=mk("xor",u,v,i);
  old=i?[P,Q,S,T]:[];
  if(i===0){P=L;Q=M;S=mk("xor",l,t,i);T=t}
  else {let a=mk("and",S,l,i),d=mk("xor",l,t,i),b=mk("and",T,d,i);
   S=mk("xor",a,b,i);T=mk("and",T,t,i);P=mk("and",P,L,i);Q=mk("and",Q,M,i)}
  layers.push({input:[x,y,u,v],old,next:[P,Q,S,T],gates:G.slice(start)});
 }
 let A=mk("xor",P,Q,m);pins=[[A,1],[S,control?1:0]];
 return {m,n,G,layers,pins,outputs:[P,Q,S,T],A,control};
}
function clauses(F){
 let C=[];for(let {op,a,b,z} of F.G){
  assert(new Set([a,b,z]).size===3,"distinct");
  if(op==="and")C.push([-a-1,-b-1,z+1],[a+1,-z-1],[b+1,-z-1]);
  else for(let w=0;w<8;w++)if(xorParity(w))C.push([a,b,z].map((v,j)=>w>>j&1?-v-1:v+1));
 }for(let [v,b] of F.pins)C.push([b?v+1:-v-1]);return C;
}
function native(F){
 let C=clauses(F),k=Math.max(F.n,C.length,2),masks=[0,0,0];
 for(let h=0;h<3;h++)for(let w=0;w<16;w++){let n=w&1,e=w>>1&1,s=w>>2&1,b=w>>3&1;if(e===b&&s===(n|[0,b,1-b][h]))masks[h]|=1<<w}
 let grid=new Uint16Array(k*k);grid.fill(masks[0]);let south=new Uint8Array(k);
 C.forEach((L,j)=>{south[j]=1;for(let l of L)grid[(Math.abs(l)-1)*k+j]=masks[l>0?1:2]});
 let D=range(C.length).map(()=>[]),h=2166136261;
 for(let i=0;i<k;i++)for(let j=0;j<k;j++){let v=grid[i*k+j];h=Math.imul(h^v,16777619)>>>0;if(v!==masks[0]){assert(j<C.length&&i<F.n,"padding");D[j].push(v===masks[1]?i+1:-i-1)}}
 for(let v of south)h=Math.imul(h^v,16777619)>>>0;
 let key=L=>L.slice().sort((a,b)=>a-b).join(",");
 assert(D.every((L,j)=>key(L)===key(C[j])),"native decode");
 return {C:D,k,N:16*k*k+8*k+Math.floor(Math.log2(k))+1,hash:h.toString(16)};
}
function closure(F,extra=[]){
 let D=range(F.n).map(()=>3),visits=0,removed=0;
 for(let [v,b] of F.pins.concat(extra)){if(!(D[v]&(1<<b)))return {no:true,visits,removed};D[v]=1<<b}
 for(;;){let last=removed;for(let g of F.G){visits++;let V=[g.a,g.b,g.z],W=range(4).map(w=>[w&1,w>>1,g.op==="and"?(w&1)&(w>>1):(w&1)^(w>>1)]).filter(t=>t.every((b,j)=>D[V[j]]&(1<<b)));if(!W.length)return {no:true,visits,removed};V.forEach((v,j)=>{let b=W.reduce((s,t)=>s|(1<<t[j]),0);if(b!==D[v]){D[v]=b;removed++}})}if(last===removed)return {no:false,visits,removed,fullInputs:D.slice(0,4*F.m).filter(d=>d===3).length}}
}
function evalGate(g,a,b){return g.op==="and"?a&b:a^b}
function evaluate(F,w){let x=range(F.n).map(i=>i<4*F.m?Number(w>>BigInt(i)&1n):0);for(let g of F.G)x[g.z]=evalGate(g,x[g.a],x[g.b]);return x}
function scan(F,C,cap=4096){let total=1n<<BigInt(4*F.m),checks=0;for(let w=0n;w<total&&checks<cap;w++){checks++;let x=evaluate(F,w);if(C.every(L=>L.some(l=>x[Math.abs(l)-1]===Number(l>0))))return {status:"WITNESS",checks,word:w.toString()}}return {status:BigInt(checks)===total?"NO":"UNKNOWN",checks}}
function anf(F,degree=3,cap=512){
 let A=range(4*F.m).map(i=>new Set([1n<<BigInt(i)])),work=0,peak=1;
 const deg=x=>{let n=0;while(x){x&=x-1n;n++}return n};
 for(let g of F.G){let L=A[g.a],R=A[g.b],S=new Set(),add=x=>S.has(x)?S.delete(x):S.add(x);
 if(g.op==="xor"){for(let x of L){add(x);work++}for(let x of R){add(x);work++}}
 else for(let x of L)for(let y of R){work++;let z=x|y;if(deg(z)>degree)return {status:"UNKNOWN",reason:"degree",work,peak};add(z);if(S.size>cap)return {status:"UNKNOWN",reason:"terms",work,peak}}
 if(S.size>cap)return {status:"UNKNOWN",reason:"terms",work,peak};peak=Math.max(peak,S.size);A[g.z]=S}
 let a=A[F.pins[0][0]],b=A[F.pins[1][0]],eq=a.size===b.size&&[...a].every(x=>b.has(x));
 return {status:eq&&F.pins[0][1]!==F.pins[1][1]?"NO":"UNKNOWN",work,peak};
}
function localEval(layer,s,w){
 let a=new Map();layer.input.forEach((v,i)=>a.set(v,w>>i&1));layer.old.forEach((v,i)=>a.set(v,s>>i&1));
 for(let g of layer.gates){assert(a.has(g.a)&&a.has(g.b),"nonlocal gate");a.set(g.z,evalGate(g,a.get(g.a),a.get(g.b)))}
 return layer.next.reduce((z,v,i)=>z|(a.get(v)<<i),0)
}
function acquire(F){
 let out=[],checks=0;for(let l of F.layers){let A=[];for(let w=0;w<16;w++){let c=localEval(l,0,w),M=range(l.old.length).map(i=>localEval(l,1<<i,w)^c);
 let apply=s=>M.reduce((v,b,i)=>s>>i&1?v^b:v,c);
 for(let s=0;s<1<<l.old.length;s++){checks++;assert(apply(s)===localEval(l,s,w),"not affine")}
 A.push({c,M})}out.push(A)}return {out,checks}
}
function basis(vs){let B=new Map();for(let w of vs){let v=w;while(v){let p=v&-v;if(!B.has(p)){B.set(p,v);break}v^=B.get(p)}}return [...B.values()]}
function joint(F,A){
 // State (1,P,Q,S,T) -> tensor of two augmented regional states (1,P,Q) and (1,S,T).
 // All vectors evaluated on the SAME prefix, no independent span product.
 const tensor=s=>{let a=1|((s&3)<<1),b=1|((s>>2)<<1),z=0;for(let i=0;i<3;i++)for(let j=0;j<3;j++)if((a>>i&1)&&(b>>j&1))z|=1<<(3*i+j);return z};
 function image(v,mat){let z=0;for(let i=0;i<9;i++)if(v>>i&1)z^=mat[i];return z}
 let B=[1],ranks=[],ops=0,checks=0;
 for(let i=0;i<A.length;i++){let next=[];for(let {c,M} of A[i]){
  if(i===0){next.push(tensor(c));ops++;continue}
  // Affine block independence checked on all inputs: A's outputs depend on old P,Q only, B's on S,T only.
  assert(M.length===4&&!(M[0]&12)&&!(M[1]&12)&&!(M[2]&3)&&!(M[3]&3),"cross state");
  const colsA=[1|((c&3)<<1),(M[0]&3)<<1,(M[1]&3)<<1],colsB=[1|((c>>2)<<1),(M[2]>>2)<<1,(M[3]>>2)<<1];
  let mat=range(9).map(k=>{let a=colsA[Math.floor(k/3)],b=colsB[k%3],z=0;for(let h=0;h<3;h++)for(let j=0;j<3;j++)if((a>>h&1)&&(b>>j&1))z|=1<<(3*h+j);return z});
  for(let s=0;s<16;s++){let t=M.reduce((z,m,j)=>s>>j&1?z^m:z,c);checks++;assert(image(tensor(s),mat)===tensor(t),"tensor adapter")}
  for(let v of B){next.push(image(v,mat));ops++}
 }B=basis(next);ranks.push(B.length)}
 // acceptance indicator (1+a+P+Q)(1+b+S)
 let a=F.pins[0][1],b=F.pins[1][1],ca=(1^a)|6,cb=(1^b)|2,mask=0;
 for(let i=0;i<3;i++)for(let j=0;j<3;j++)if((ca>>i&1)&&(cb>>j&1))mask|=1<<(3*i+j);
 return {status:B.every(v=>xorParity(v&mask)===0)?"NO":"UNKNOWN",ranks,ops,checks,mask,basis:B};
}
function adversary(F){
 // Independently evaluate actual local gates, prove invariant P=S+T and Q=T inductively for all local words.
 let checks=0;
 for(let i=0;i<F.layers.length;i++)for(let w=0;w<16;w++)for(let s=0;s<(i?16:1);s++){
 if(i&&(((s&1)!==((s>>2&1)^(s>>3&1)))||((s>>1&1)!==(s>>3&1))))continue;
 let t=localEval(F.layers[i],s,w);checks++;
 assert((t&1)===((t>>2&1)^(t>>3&1))&&(t>>1&1)===(t>>3&1),"invariant");
 }
 return {status:F.pins[0][1]!==F.pins[1][1]?"NO":"UNKNOWN",checks};
}
function audit(){
 let out=[];for(let m of [2,4,8,16,32,64]){
 let F=build(m),G=native(F),I=closure(F),E=scan(F,G.C),D=anf(F),T=anf(F,4*m,512),A=acquire(F),J=joint(F,A.out),V=adversary(F),reclosed=closure(F);
 assert(!I.no&&I.fullInputs===4*m&&J.status==="NO"&&V.status==="NO"&&E.status!=="WITNESS","unexpected");
 out.push({m,N:G.N,k:G.k,hash:G.hash,n:F.n,clauses:G.C.length,initial:I,scan:E,anf3:D,anfCap512:T,acquireChecks:A.checks,joint:J,adversary:V,reclosed,rectangleLB:(1n<<BigInt(m)).toString(),ANFterms:(2n<<BigInt(m)).toString()});
 }
 let F=build(2,true),G=native(F),S=scan(F,G.C),A=acquire(F),J=joint(F,A.out);assert(S.status==="WITNESS"&&J.status==="UNKNOWN"&&adversary(F).status==="UNKNOWN","false rejection");
 return {out,control:{m:2,scan:S,joint:J}};
}
const result=audit();console.log(JSON.stringify(result,null,2));
