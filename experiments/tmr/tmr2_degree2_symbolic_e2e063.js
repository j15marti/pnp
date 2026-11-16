"use strict";
console.log(JSON.stringify((function study(){
"use strict";
const REV="TMR2_D2POLY063_v1", SEED=20261116;
let seed=SEED>>>0; function rng(){seed^=(seed<<13);seed^=(seed>>>17);seed^=(seed<<5);return (seed>>>0)/4294967296;}
function req(b,msg){if(!b)throw Error(msg);}
let assertions=0,exhaustive=0,characters=0,rejected=0,cases=0;
function check(b,msg){assertions++;req(b,msg);}
function num(s){req(/^(0|[1-9]\d*)$/.test(s),"noncanonical integer");let x=Number(s);req(Number.isSafeInteger(x),"unsafe integer");return x;}
function popcount(x){let v=0;while(x){x&=x-1n;v++;}return v;}
function parity(x){let p=0;while(x){p^=1;x&=x-1n;}return p;}
function toggle(S,v){if(S.has(v))S.delete(v);else S.add(v);}
function plus(A,B){let C=new Set(A);for(const v of B)toggle(C,v);return C;}
function times(A,B){let C=new Set();for(const x of A)for(const y of B)toggle(C,x|y);return C;}
function cpoly(v){return v?new Set([0n]):new Set();}
function read(src){
 req(typeof src==="string"&&src.length>0&&/^[\x0A\x20-\x7E]+$/.test(src),"ascii");
 req(src.endsWith("\n"),"final LF");let lines=src.slice(0,-1).split("\n");req(lines.length>1,"header");
 let h=lines[0].split(" ");req(h.length===7&&h[0]==="p"&&h[1]==="d2poly","header grammar");
 let [n,a,b,g,root]=h.slice(2).map(num);
 req(a>=1&&b>=1&&n===a+b&&g>=1&&g<=src.length&&n<=2*g&&root<g,"header bounds");
 req(lines.length===g+1,"record count");
 const r=new Array(g);
 for(const line of lines.slice(1)){
  req(line!==""&&!line.includes("\r")&&!line.includes("  "),"record blanks");
  let t=line.split(" "),op=t[0],arity={E:4,X:4,I:3,N:3,A:4,O:4,P:4}[op];
  req(arity===t.length,"opcode/arity");
  let id=num(t[1]);req(id<g&&!r[id],"id duplicate/range");
  let args=t.slice(2).map(num);
  if(op==="E")req(args[0]<a&&args[1]<b,"E index");
  if(op==="I")req(args[0]<n,"I index");
  if(!["E","I"].includes(op))for(const k of args)req(k<g,"wire");
  r[id]={op,args,id};
 }
 req(r.every(Boolean),"missing record");
 let state=new Uint8Array(g),order=[];
 function dfs(i){req(state[i]!==1,"cycle");if(state[i]===2)return;state[i]=1;
  let v=r[i];if(v.op!=="E"&&v.op!=="I")for(const j of v.args)dfs(j);
  state[i]=2;order.push(i);
 }
 dfs(root);req(order.length===g,"unreachable gate");
 let seen=new Set(),deg=new Int8Array(g);
 for(let id of order){let z=r[id],op=z.op,vs=z.args;
  if(op==="E"){seen.add(vs[0]);seen.add(a+vs[1]);deg[id]=0;}
  else if(op==="I"){seen.add(vs[0]);deg[id]=1;}
  else if(op==="X"){req(["E","X"].includes(r[vs[0]].op)&&["E","X"].includes(r[vs[1]].op),"early X stage");deg[id]=0;}
  else if(op==="N")deg[id]=deg[vs[0]];
  else if(op==="P")deg[id]=Math.max(deg[vs[0]],deg[vs[1]]);
  else deg[id]=deg[vs[0]]+deg[vs[1]];
  req(deg[id]<=2,"relative degree exceeds two");
 }
 req(seen.size===n,"uncovered input");
 return {n,a,b,g,root,r,order,deg,N:src.length};
}
function msb(x){req(x>0n,"msb0");let v=-1;while(x){v++;x>>=1n;}return v;}
function basis(src){
 const {r,order,b}=src, matrices=new Array(src.g).fill(0n),pivs=new Map();let d=0;
 for(const i of order){let t=r[i];if(t.op==="E")matrices[i]=1n<<BigInt(t.args[0]*b+t.args[1]);
  else if(t.op==="X")matrices[i]=matrices[t.args[0]]^matrices[t.args[1]];
 }
 for(const i of order){if(!["E","X"].includes(r[i].op))continue;
  let x=matrices[i];while(x){const p=msb(x),o=pivs.get(p);if(o)x^=o.vec;else{pivs.set(p,{vec:x,bit:1n<<BigInt(d)});d++;break;}}
 }
 const masks=new Array(src.g).fill(0n);
 for(const i of order){if(!["E","X"].includes(r[i].op))continue;
  let x=matrices[i],mask=0n;while(x){let o=pivs.get(msb(x));req(o!==undefined,"basis reduction");x^=o.vec;mask^=o.bit;}
  masks[i]=mask;
 }
 const vec=new Array(d).fill(0n);for(const [,o] of pivs){vec[msb(o.bit)]=o.vec;}
 return {d,vec,masks};
}
function symbolic(src,bs,w){
 let p=new Array(src.g);
 for(const id of src.order){let z=src.r[id],a=z.args,op=z.op;
  if(op==="E"||op==="X")p[id]=cpoly(parity(bs.masks[id]&w));
  else if(op==="I")p[id]=new Set([1n<<BigInt(a[0])]);
  else if(op==="N")p[id]=plus(p[a[0]],new Set([0n]));
  else if(op==="P")p[id]=plus(p[a[0]],p[a[1]]);
  else if(op==="A")p[id]=times(p[a[0]],p[a[1]]);
  else if(op==="O")p[id]=plus(plus(p[a[0]],p[a[1]]),times(p[a[0]],p[a[1]]));
  req(p[id].size<=1+src.n*(src.n+1)/2,"poly overflow");
 }
 return p[src.root];
}
function gauss(poly,n){
 let P=new Set(poly),pairs=0;
 while(true){
  let edge=null;for(const z of P)if(popcount(z)===2){edge=z;break;}
  if(edge===null){for(const z of P)if(popcount(z)===1)return 0n;
   let sign=P.has(0n)?-1n:1n;return sign*(1n<<BigInt(n-pairs));}
  let i=-1,j=-1;for(let k=0;k<n;k++)if(edge&(1n<<BigInt(k))){if(i<0)i=k;else{j=k;break;}}
  req(j>=0,"pair");let bi=1n<<BigInt(i),bj=1n<<BigInt(j),A=new Set(),B=new Set(),R=new Set();
  for(const mon of P){
   if((mon&bi)!==0n){if((mon&bj)!==0n){req(mon===edge,"degree2 pair");continue;}toggle(A,mon^bi);}
   else if((mon&bj)!==0n)toggle(B,mon^bj);
   else toggle(R,mon);
  }
  P=plus(R,times(A,B));pairs++;
  req(pairs<=Math.floor(n/2),"too many pairs");
 }
}
function count(srcstr){
 let s=read(srcstr),bs=basis(s),D=1n<<BigInt(bs.d);
 req(bs.d<=8,"harness cap d>8, not theorem bound");
 let numerator=1n<<BigInt(s.n+bs.d),sum=0n;
 for(let w=0n;w<D;w++){
  let P=symbolic(s,bs,w);
  for(let lam=0n;lam<D;lam++){
   let Q=new Set(P);
   for(let j=0;j<bs.d;j++)if(lam&(1n<<BigInt(j))){
    let edgevec=bs.vec[j];for(let k=0;k<s.a;k++)for(let l=0;l<s.b;l++)
     if(edgevec&(1n<<BigInt(k*s.b+l)))toggle(Q,(1n<<BigInt(k))|(1n<<BigInt(s.a+l)));
   }
   let G=gauss(Q,s.n);sum+=(parity(lam&w)?-G:G);characters++;
  }
 }
 req((numerator-sum)%(2n*D)===0n,"noninteger count");
 let ans=(numerator-sum)/(2n*D);
 req(ans>=0n&&ans<=(1n<<BigInt(s.n)),"count range");
 return {ans,d:bs.d,N:s.N,g:s.g,n:s.n};
}
function direct(s,z){
 let v=new Array(s.g);
 for(const id of s.order){let r=s.r[id],a=r.args;
  if(r.op==="I")v[id]=Boolean(z&(1n<<BigInt(a[0])));
  else if(r.op==="E")v[id]=Boolean(z&(1n<<BigInt(a[0])))&&Boolean(z&(1n<<BigInt(s.a+a[1])));
  else if(r.op==="N")v[id]=!v[a[0]];
  else if(r.op==="X"||r.op==="P")v[id]=v[a[0]]!==v[a[1]];
  else if(r.op==="A")v[id]=v[a[0]]&&v[a[1]];
  else if(r.op==="O")v[id]=v[a[0]]||v[a[1]];
 }
 return v[s.root];
}
function brute(s){req(s.n<=10,"brute cap");let c=0n;for(let z=0n;z<(1n<<BigInt(s.n));z++)if(direct(s,z))c++;return c;}
function build(n,a,fn){let rec=[];
 function add(op,...arg){const id=rec.length;rec.push([op,id,...arg].join(" "));return id;}
 let root=fn(add),g=rec.length;
 let order=Array.from({length:g},(_,i)=>i);for(let i=g-1;i>0;i--){let j=Math.floor(rng()*(i+1));[order[i],order[j]]=[order[j],order[i]];}
 return `p d2poly ${n} ${a} ${n-a} ${g} ${root}\n`+order.map(i=>rec[i]).join("\n")+"\n";
}
function test(src,answer=null){let v=count(src),s=read(src);if(s.n<=10){let x=brute(s);check(v.ans===x,"EXHAUSTIVE mismatch "+v.ans+"/"+x);exhaustive++;}
 if(answer!==null)check(v.ans===BigInt(answer),"expected "+answer+" got "+v.ans);
 cases++;return v;
}
function reject(src,fragment){try{read(src);throw Error("rejected unexpectedly "+fragment);}catch(e){if(String(e).includes("rejected unexpectedly"))throw e;if(fragment)check(String(e).includes(fragment),"rejection incorrect: "+e);}rejected++;}
const samples=[];
for(let t=0;t<96;t++){
 let n=4+Math.floor(rng()*5),a=Math.floor(n/2),b=n-a;
 let src=build(n,a,add=>{
  let early=[];for(let j=0;j<1+Math.floor(rng()*3);j++)early.push(add("E",Math.floor(rng()*a),Math.floor(rng()*b)));
  if(t%3===0)early.push(add("X",early[0],early[0]));
  const I=Array.from({length:n},(_,i)=>add("I",i));
  const m1=add(t%2?"O":"A",I[0],I[1]);
  const m2=add("P",I[2],I[3]);
  const m3=add("A",m1,early[0]);
  const m4=add("O",m2,early[0]);
  const m5=add("A",m2,m2);
  let terms=[...early,...I,m1,m2,m3,m4,m5];
  let out=terms.shift();for(const k of terms)out=add("P",out,k);
  return out;
 });
 let v=test(src);if(t<3)samples.push({n:v.n,d:v.d,ans:v.ans.toString(),N:v.N});
}
const disj=build(8,4,add=>{let clauses=[];for(let i=0;i<4;i++)clauses.push(add("N",add("E",i,i)));let out=clauses[0];for(let i=1;i<4;i++)out=add("A",out,clauses[i]);return out;});
const cdisj=test(disj,81);
const square=build(2,1,add=>{let x=add("I",0),y=add("I",1);let e=add("E",0,0);let sq=add("A",x,x);let out=add("P",sq,e);out=add("P",out,y);return out;});test(square);
const unreach=build(4,2,add=>{let e=add("E",0,0),x=add("I",1);return add("A",e,x);});reject(unreach,"uncovered input");
const degree3=build(3,1,add=>{let a=add("I",0),b=add("I",1),c=add("I",2);return add("A",add("A",a,b),c);});reject(degree3,"relative degree");
const simple=build(2,1,add=>{let a=add("E",0,0);return add("P",a,a);});test(simple,0);
const big=build(64,32,add=>{
 let e=add("E",0,0),ix=Array.from({length:64},(_,i)=>add("I",i));
 let l1=add("P",ix[1],ix[33]),l2=add("P",ix[2],ix[34]);
 let out=add("A",e,add("A",l1,l2));
 for(let i=0;i<64;i++){let z=add("P",ix[i],ix[i]);out=add("P",out,z);}
 return out;
});const bigval=test(big,1n<<60n);
let mutated=disj.slice(0,-1);reject(mutated,"final LF");
return {revision:REV,seed:SEED,cases,exhaustive,assertions,rejected,character_calls:characters,failures:0,disj4:cdisj.ans.toString(),large:{n:bigval.n,g:bigval.g,N:bigval.N,d:bigval.d,accepts:bigval.ans.toString()},samples};
})(),null,2));
