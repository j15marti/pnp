"use strict";
function independent(){
const A=(p,m)=>{if(!p)throw Error(m)};
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;};
const Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);A(d!==0n,"den");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];};
const sum=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const dif=(a,b)=>Q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
const min=(a,b)=>cmp(a,b)<0n?a:b;
const txt=x=>x[0].toString()+"/"+x[1].toString();
function exact(c,expect){
 let f=Q(1),p=Q(1),vals=[];
 for(let k=1;k<=3;k++){
  f=div(mul(c,f),sum(Q(1),f));p=div(p,c);
  const left=div(dif(div(Q(1),f),c),Q(k));
  vals.push({k,left:txt(left),second:txt(p),d:min(left,p),d_text:txt(min(left,p))});
 }
 let c4=div(p,c),d2=vals[1].d;
 A(txt(d2)===expect,"d2 value");
 A(vals.every(x=>cmp(d2,x.d)>=0n),"finite optimality");
 A(cmp(c4,d2)<0n,"infinite tail c^-(3+1) upper");
 return {c:txt(c),certified_max:txt(d2),winner:2,k1:vals[0].d_text,k2:vals[1].d_text,k3:vals[2].d_text,tail_max:txt(c4),tail_certified:true};
}
const envelope=[exact(Q(6,5),"23/45"),exact(Q(241,200),"11642479/23232400")];
const W="-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14".split(";").map(x=>x.trim().split(" ").map(Number));
const Z=W.map(x=>x.slice());Z[7][0]*=-1;Z[19][0]*=-1;
function modelcount(C){
 let count=0,zero=0,one=0;
 const tally=(m)=>C.map(c=>c.reduce((s,l)=>s+(((m>>(Math.abs(l)-1))&1)===(l>0?1:0)?1:0),0));
 for(let m=0;m<32768;m++){
  const p=tally(m),q=tally(32767^m);
  for(let i=0;i<20;i++)A(p[i]+q[i]===3,"original complement");
  if(p.every(x=>x>0))count++;
  if(m===0)zero=p.filter(x=>x===0).length;
  if(m===32767)one=p.filter(x=>x===0).length;
 }
 const quota=new Map();for(let c of C)for(let l of c)quota.set(l,(quota.get(l)||0)+1);
 for(let v=1;v<=15;v++)A(quota.get(v)===2&&quota.get(-v)===2,"signed22 quota");
 return {models:count,zero_false:zero,one_false:one};
}
const mw=modelcount(W),mz=modelcount(Z);
A(mw.models===0&&mz.models===168,"W1 matched models");
A(mw.zero_false===mz.zero_false&&mw.one_false===mz.one_false,"matched endpoints");
const choose=(n,k)=>{let r=1n;for(let i=1n;i<=BigInt(k);i++)r=r*(BigInt(n)-i+1n)/i;return r;};
const states=[[6,3,160],[12,6,59136],[15,5,96096]].map(([n,t,expect])=>{let u=choose(n,t)*2n**BigInt(t);A(u===BigInt(expect),"binomial card");let b=0;while((1n<<BigInt(b))<u)b++;return {n,t,number:u.toString(),minimum_bits:b};});
return {result:"PASS",independent_exact_arithmetic:envelope,independent_original_source_W1:mw,independent_original_source_W1_swap:mz,independent_partial_assignment_counts:states,statement:"No native FLMV Turing-machine runtime certification; this is exact arithmetic and exhaustive finite model checking."};
}
process.stdout.write(JSON.stringify(independent(),null,2)+"\n");
