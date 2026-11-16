"use strict";
console.log(JSON.stringify((function run(){
 "use strict";
 const REV="TMR2_CANCEL_SPECTRAL065_v1",SEED=20261116;
 let rng=SEED>>>0,cases=0,exhaustive=0,rejects=0,characters=0;
 function ok(v,m){if(!v)throw Error(m);}
 function rand(){rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return(rng>>>0)/4294967296;}
 function number(s){ok(/^(0|[1-9]\d*)$/.test(s),"noncanonical number");const v=Number(s);ok(Number.isSafeInteger(v),"unsafe integer");return v;}
 function bit(z,i){return (z>>BigInt(i))&1n;}
 function pc(z){let n=0;while(z){z&=z-1n;n++;}return n;}
 function toggle(S,x){if(S.has(x))S.delete(x);else S.add(x);}
 function xor(A,B){let S=new Set(A);for(const x of B)toggle(S,x);return S;}
 function prod(A,B){let S=new Set();for(const x of A)for(const y of B)toggle(S,x|y);return S;}
 function parse(src){
  ok(typeof src==="string"&&/^[\x0A\x20-\x7E]+$/.test(src)&&src.endsWith("\n"),"ASCII LF");
  const lines=src.slice(0,-1).split("\n"),h=lines.shift().split(" ");
  ok(h.length===7&&h[0]==="p"&&h[1]==="d2poly","header");
  const[n,a,b,g,root]=h.slice(2).map(number);
  ok(a>=1&&b>=1&&n===a+b&&g>=1&&root<g&&n<=2*g&&g<=src.length&&lines.length===g,"header bounds");
  const R=Array(g);
  for(const line of lines){
   ok(line&&line===line.trim()&&!line.includes("  "),"noncanonical line");
   const t=line.split(" "),op=t[0],arity={I:3,E:4,X:4,N:3,A:4,O:4,P:4};
   ok(arity[op]===t.length,"gate opcode/arity");
   const id=number(t[1]),args=t.slice(2).map(number);ok(id<g&&!R[id],"gate id");
   if(op==="I")ok(args[0]<n,"raw input range");
   else if(op==="E")ok(args[0]<a&&args[1]<b,"bipartite edge range");
   else ok(args.every(x=>x<g),"wire range");
   R[id]={op,args};
  }
  ok(R.every(Boolean),"missing gate");
  for(const q of R)if(q.op==="X")ok(q.args.every(i=>R[i].op==="E"||R[i].op==="X"),"early phase");
  const state=new Uint8Array(g),order=[],seen=new Set();
  function dfs(id){
   ok(state[id]!==1,"dependency cycle");if(state[id]===2)return;state[id]=1;
   const q=R[id];
   if(q.op==="I")seen.add(q.args[0]);
   else if(q.op==="E"){seen.add(q.args[0]);seen.add(a+q.args[1]);}
   else for(const k of q.args)dfs(k);
   state[id]=2;order.push(id);
  }
  dfs(root);ok(order.length===g&&seen.size===n,"reachability/coverage");
  return{N:src.length,n,a,b,g,root,R,order};
 }
 function span(s){
  const mat=Array(s.g),coord=Array(s.g),basis=[];
  function pivot(z){let j=-1;while(z){z>>=1n;j++;}return j;}
  for(const id of s.order){
   const q=s.R[id];let m;
   if(q.op==="E")m=1n<<BigInt(q.args[0]*s.b+q.args[1]);
   else if(q.op==="X")m=mat[q.args[0]]^mat[q.args[1]];
   else continue;
   mat[id]=m;let r=m,mask=0n;
   for(let j=0;j<basis.length;j++)if(bit(r,basis[j].pivot)){r^=basis[j].matrix;mask^=1n<<BigInt(j);}
   if(r){mask^=1n<<BigInt(basis.length);basis.push({matrix:r,pivot:pivot(r)});}
   coord[id]=mask;
  }
  for(const id of s.order)if(s.R[id].op==="E"||s.R[id].op==="X"){
   let reconstructed=0n;
   for(let j=0;j<basis.length;j++)if(bit(coord[id],j))reconstructed^=basis[j].matrix;
   ok(reconstructed===mat[id],"basis coordinate verification");
  }
  return{d:basis.length,basis,coord};
 }
 function normalize(s,sp){
  const nodes=[],cache=new Map(),vectors=Array(s.g);let attempts=0;
  function atom(key,node){
   let id=cache.get(key);
   if(id===undefined){id=nodes.length;nodes.push(node);cache.set(key,id);}
   return 1n<<BigInt(id+1);
  }
  function degree(vec){let d=0,j=0,z=vec>>1n;while(z){if(z&1n)d=Math.max(d,nodes[j].degree);z>>=1n;j++;}return d;}
  function and(x,y){
   attempts++;
   if(!x||!y)return 0n;
   if(x===1n)return y;
   if(y===1n)return x;
   if(x===y)return x;
   if((x^y)===1n)return 0n;
   if(x>y)[x,y]=[y,x];
   return atom("A:"+x.toString(16)+":"+y.toString(16),{op:"A",x,y,degree:Math.min(3,degree(x)+degree(y))});
  }
  function early(mask){let v=0n;for(let j=0;j<sp.d;j++)if(bit(mask,j))v^=atom("W:"+j,{op:"W",index:j,degree:0});return v;}
  for(const id of s.order){
   const {op,args}=s.R[id];
   if(op==="I")vectors[id]=atom("I:"+args[0],{op:"I",index:args[0],degree:1});
   else if(op==="E"||op==="X")vectors[id]=early(sp.coord[id]);
   else if(op==="N")vectors[id]=vectors[args[0]]^1n;
   else if(op==="P")vectors[id]=vectors[args[0]]^vectors[args[1]];
   else if(op==="A")vectors[id]=and(vectors[args[0]],vectors[args[1]]);
   else if(op==="O")vectors[id]=vectors[args[0]]^vectors[args[1]]^and(vectors[args[0]],vectors[args[1]]);
  }
  const root=vectors[s.root],d=degree(root),live=new Set();
  function mark(v){
   let j=0,z=v>>1n;
   while(z){if((z&1n)&&!live.has(j)){live.add(j);if(nodes[j].op==="A"){mark(nodes[j].x);mark(nodes[j].y);}}
    z>>=1n;j++;
   }
  }
  mark(root);
  const keep=[...live].sort((a,b)=>a-b);
  ok(keep.every(j=>nodes[j].degree<=d),"certificate ancestor monotonicity");
  return{root,nodes,keep,degree:d,attempts,eliminated:nodes.length-keep.length};
 }
 function specialize(s,f,u){
  ok(f.degree<=2,"OUTSIDE certified domain");
  const P=Array(f.nodes.length);
  function value(vec){
   let out=(vec&1n)?new Set([0n]):new Set(),z=vec>>1n,j=0;
   while(z){if(z&1n)out=xor(out,P[j]);z>>=1n;j++;}return out;
  }
  for(const id of f.keep){
   const q=f.nodes[id];
   P[id]=q.op==="I"?new Set([1n<<BigInt(q.index)]):
      q.op==="W"?(bit(u,q.index)?new Set([0n]):new Set()):
      prod(value(q.x),value(q.y));
   ok([...P[id]].every(m=>pc(m)<=2),"certified quadratic violation");
  }
  return value(f.root);
 }
 function H(Q,n){
  characters++;
  let P=new Set(Q),pairs=0;
  while(true){
   let edge=null;for(const m of P)if(pc(m)===2){edge=m;break;}
   if(edge===null){
    if([...P].some(m=>pc(m)===1))return 0n;
    return(P.has(0n)?-1n:1n)*(1n<<BigInt(n-pairs));
   }
   let i=-1,j=-1;
   for(let k=0;k<n;k++)if(bit(edge,k)){if(i<0)i=k;else{j=k;break;}}
   const bi=1n<<BigInt(i),bj=1n<<BigInt(j),A=new Set(),B=new Set(),R=new Set();
   for(const m of P){
    if(m&bi){if(m&bj){ok(m===edge,"pair degree");continue;}toggle(A,m^bi);}
    else if(m&bj)toggle(B,m^bj);
    else toggle(R,m);
   }
   P=xor(R,prod(A,B));pairs++;ok(pairs<=Math.floor(n/2),"pair count");
  }
 }
 function count(src){
  const s=parse(src),sp=span(s),f=normalize(s,sp);
  ok(f.degree<=2,"OUTSIDE certified domain");
  ok(sp.d<=8,"test-only character cap");
  let signed=0n,terms=0;
  for(let u=0n;u<(1n<<BigInt(sp.d));u++){
   const p=specialize(s,f,u);
   for(let lam=0n;lam<(1n<<BigInt(sp.d));lam++){
    const Q=new Set(p);let mat=0n;
    for(let j=0;j<sp.d;j++)if(bit(lam,j))mat^=sp.basis[j].matrix;
    for(let i=0;i<s.a;i++)for(let j=0;j<s.b;j++)if(bit(mat,i*s.b+j)){
     toggle(Q,(1n<<BigInt(i))|(1n<<BigInt(s.a+j)));
    }
    const h=H(Q,s.n);signed+=pc(lam&u)%2?-h:h;terms++;
   }
  }
  const numerator=(1n<<BigInt(s.n+sp.d))-signed,den=1n<<BigInt(sp.d+1);
  ok(numerator%den===0n,"character divisibility");
  const answer=numerator/den,total=1n<<BigInt(s.n);
  ok(answer>=0n&&answer<=total,"count range");
  return{answer:answer.toString(),n:s.n,g:s.g,N:s.N,d:sp.d,degree:f.degree,atoms:f.nodes.length,liveAtoms:f.keep.length,characters:terms};
 }
 function direct(s,z){
  const val=Array(s.g);
  for(const id of s.order){const {op,args}=s.R[id];
   if(op==="I")val[id]=!!Number(bit(z,args[0]));
   else if(op==="E")val[id]=!!Number(bit(z,args[0])&bit(z,s.a+args[1]));
   else if(op==="N")val[id]=!val[args[0]];
   else if(op==="A")val[id]=val[args[0]]&&val[args[1]];
   else if(op==="O")val[id]=val[args[0]]||val[args[1]];
   else val[id]=val[args[0]]!==val[args[1]];
  }return val[s.root];
 }
 function brute(s){let count=0n;for(let z=0n;z<(1n<<BigInt(s.n));z++)if(direct(s,z))count++;return count;}
 function build(n,fn){
  const rec=[];
  function add(op,...a){const id=rec.length;rec.push([op,id,...a].join(" "));return id;}
  const root=fn(add),g=rec.length,order=Array.from({length:g},(_,i)=>i);
  for(let i=g-1;i>0;i--){const j=Math.floor(rand()*(i+1));[order[i],order[j]]=[order[j],order[i]];}
  const a=Math.floor(n/2);
  return "p d2poly "+n+" "+a+" "+(n-a)+" "+g+" "+root+"\n"+order.map(i=>rec[i]).join("\n")+"\n";
 }
 function family(n,variant){
  return build(n,add=>{
   const I=Array.from({length:n},(_,i)=>add("I",i));
   const a=add("E",0,0),b=add("E",1,1),x=add("X",a,b),y=add("X",x,a);
   let high=I[0];for(let i=1;i<n;i++)high=add("A",high,I[i]);
   const dead=add("P",high,high),raw=add("A",I[3],I[4]);
   let head=variant%4===0?add("A",y,raw):variant%4===1?add("O",x,raw):
             variant%4===2?add("P",a,raw):add("A",x,raw);
   const zero=add("P",y,y),withEarly=add("P",head,zero);
   return add("P",withEarly,dead);
  });
 }
 function disj(k){return build(2*k,add=>{
  let E=Array.from({length:k},(_,i)=>add("E",i,i)),head=E[0];
  for(let i=1;i<k;i++)head=add("O",head,E[i]);
  return add("N",head);
 });}
 function check(src,expected){
  const out=count(src),s=parse(src);
  if(s.n<=10){ok(BigInt(out.answer)===brute(s),"exhaustive mismatch");exhaustive++;}
  if(expected!==undefined)ok(BigInt(out.answer)===BigInt(expected),"expected count mismatch");
  cases++;return out;
 }
 const examples=[];
 for(let k=1;k<=4;k++)examples.push({name:"DISJ_"+k,...check(disj(k),3n**BigInt(k))});
 for(let n=5;n<=10;n++)for(let variant=0;variant<4;variant++){
  const v=check(family(n,variant));if(n===5||n===10)examples.push({name:"mixed_"+n+"_"+variant,...v});
 }
 for(let j=0;j<44;j++){const n=5+Math.floor(rand()*6),variant=Math.floor(rand()*4);check(family(n,variant));}
 examples.push({name:"large64_canceled_highdegree",...check(family(64,0),1n<<60n)});
 const outside=build(6,add=>{
  const I=Array.from({length:6},(_,i)=>add("I",i)),e=add("E",0,0),x=add("X",e,e);
  let high=I[0];for(let i=1;i<6;i++)high=add("A",high,I[i]);
  return add("P",high,x);
 });
 try{count(outside);throw Error("accepted high degree");}catch(e){ok(String(e).includes("OUTSIDE certified domain"),"OUTSIDE control");rejects++;}
 try{parse(outside.replace("p d2poly","p d3poly"));throw Error("accepted header");}catch(e){ok(String(e).includes("header"),"header control");rejects++;}
 try{parse(disj(3).replace("E 0 0 0","E 0 7 0"));throw Error("accepted edge");}catch(e){ok(String(e).includes("bipartite edge"),"edge guard");rejects++;}
 return{revision:REV,seed:SEED,cases,exhaustive,rejects,characters,failures:0,examples};
})(),null,2));
