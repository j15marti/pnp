'use strict';
/* Independently checks the repository's 2026-10-31 FARBLANK274 raw JSON.
   No dependency on the producer. Node.js 18+. */
function verify(R) {
 let tests=0;const ok=(v,s)=>{tests++;if(!v)throw Error("FARBLANK274 VERIFY: "+s)};
 const count=(C,a)=>C.filter(l=>(((a>>(Math.abs(l)-1))&1)===(l>0?1:0))).length;
 const sat=(F,a)=>F.every(C=>count(C,a)>0);
 const tab=(F,a)=>[0,1,2,3].map(k=>F.filter(C=>count(C,a)===k).length);
 const fmt=(n,F)=>"p cnf "+n+" "+F.length+"\n"+F.map(C=>C.join(" ")+" 0\n").join("");
 for (const X of R.cases) {
  const F=X.original,n=X.n,MASK=(1<<n)-1,models=[];
  for(let a=0;a<=MASK;a++)if(sat(F,a))models.push(a);
  ok(JSON.stringify(models)===JSON.stringify(X.models),"models");
  ok((models.length>0)===(X.label==="SAT"),"label");
  const child=[...new Map(F.map(C=>[C.join(","),C])).values()];
  const bytes=fmt(n,child),M=bytes.length;
  ok(fmt(n,F).length===X.originalBytes&&M===X.childBytes,"physical byte encoding");
  for(let a=0;a<=MASK;a++){
   ok(sat(F,a)===sat(child,a),"source-child exact both labels");
   for(let k=0;k<4;k++)ok(tab(F,a)[k]===tab(F,MASK^a)[3-k],"complement");
  }
  ok(JSON.stringify(tab(F,0))===JSON.stringify(X.endpoint0),"zero endpoint");
  ok(JSON.stringify(tab(F,MASK))===JSON.stringify(X.endpoint1),"one endpoint");
  for(let j=0;j<F.length;j++){
   const orig=X.occ[j],C=F[j];
   ok(orig.j===j+1&&JSON.stringify(orig.original)===JSON.stringify(C),"source clause");
   for(let k=0;k<3;k++){const l=C[k],q=orig.occurrences[k],v=l>0?1:0;
    ok(q.j===j+1&&q.k===k+1&&q.l===l&&q.S===v&&q.invS===1-v&&q.U===1-v&&q.invU===v,"indexed S/U inversions")}
  }
  ok(X.pairs.length===F.length*(F.length-1)/2,"number of original pairs");
  for(const p of X.pairs){
   const C=F[p.j-1],D=F[p.k-1],st={SS:false,SU:false,US:false,UU:false};
   for(let a=0;a<=MASK;a++){const x=count(C,a),y=count(D,a);
    if(x===3&&y===3)st.SS=true;if(x===3&&y===0)st.SU=true;
    if(x===0&&y===3)st.US=true;if(x===0&&y===0)st.UU=true;}
   ok(JSON.stringify(st)===JSON.stringify(p.states),"four-way compatibility");
  }
  let mask=0;for(const [i,t] of X.flips.entries()){
   if(i)mask^=1<<(i-1);
   ok(t.mask===mask&&JSON.stringify(t.counts)===JSON.stringify(tab(F,mask)),"coherent flip");
  }
  for(const q of X.res){const C=F[q.parents[0]-1],D=F[q.parents[1]-1],x=q.pivot;
   ok(C.includes(x)&&D.includes(-x),"resolution pivot");
   const clause=[...new Set(C.filter(l=>l!==x).concat(D.filter(l=>l!==-x)))];
   ok(JSON.stringify(clause)===JSON.stringify(q.clause)&&!clause.some(l=>clause.includes(-l)),"authentic resolvent");
   for(const a of models)ok(clause.some(l=>(((a>>(Math.abs(l)-1))&1)===(l>0?1:0))),"forbidden cube");
  }
  const h=2*Math.ceil(Math.log2(M+2))+4,far=(1n<<BigInt(h))-1n,V=X.vm;
  ok(V.h===h&&V.far===String(far)&&far>BigInt(M*M),"superlinear far-address index");
  ok(V.indexEraseCells===4*h&&V.childBufferCells===M,"charged erasures and child buffer");
  ok(V.childAddressBits===3*Math.ceil(Math.log2(M+2)),"charged child address writes");
  const J=V.trace.filter(t=>t.type==="jump"),A=V.trace.filter(t=>t.type==="read");
  ok(JSON.stringify(J.map(v=>v.indexHead))===JSON.stringify([h-1,0,h-1,0]),"input-index head preserved");
  ok(JSON.stringify(A.map(v=>v.address))===JSON.stringify([String(far),"1","2",String(far-1n),"0"]),"address trace");
  ok(JSON.stringify(A.map(v=>v.value))===JSON.stringify([null,bytes[1],bytes[2],null,bytes[0]]),"input characters and far blank");
  ok(X.baseline.sat===X.guest.sat&&X.guest.sat===(models.length>0),"both-label solver result");
 }
 const gcd=(a,b)=>b?gcd(b,a%b):a;
 const f=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);const g=gcd(a<0n?-a:a,b);return [a/g,b/g]};
 const add=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const sub=(a,b)=>f(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
 const mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
 const div=(a,b)=>f(a[0]*b[1],a[1]*b[0]);
 const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1],rep=a=>String(a[0])+"/"+String(a[1]);
 for(const e of R.bounds){const [p,q]=e.c.split("/").map(BigInt),c=f(p,q);let v=f(1),power=f(1),best=f(-1),bestK=0,K=0,tail=f(1);
  for(let k=1;k<100;k++){v=div(mul(c,v),add(f(1),v));power=div(power,c);const d1=div(sub(div(f(1),v),c),f(k)),d=cmp(d1,power)<0n?d1:power;
   if(cmp(d,best)>0n){best=d;bestK=k}tail=div(power,c);if(cmp(tail,best)<0n){K=k;break}}
  ok(K>0&&rep(best)===e.best&&bestK===e.kbest&&K===e.checkedK&&rep(tail)===e.tailMax,"FLMV complete infinite tail");
 }
 return {result:"PASS",checks:tests,sources:R.cases.length,flmv:R.bounds.map(x=>({c:x.c,d:x.best,k:x.kbest}))};
}
if(require.main===module){const fs=require("fs");const file=process.argv[2];if(!file)throw Error("Pass raw JSON file");console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8"))),null,2));}
module.exports={verify};
