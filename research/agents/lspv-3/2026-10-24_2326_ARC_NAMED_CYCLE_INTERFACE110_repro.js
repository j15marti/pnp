"use strict";
// Run: node 2026-10-24_2326_ARC_NAMED_CYCLE_INTERFACE110_repro.js
const audit=function audit110(){
let checks=0;const ok=(b,m)=>{if(!b)throw Error(m);checks++};
const formulas=(r,odd)=>Array.from({length:r},(_,i)=>{let u=i+1,v=(i+1)%r+1,d=odd&&i===r-1?1:0,B=d?[[u,v],[-u,-v]]:[[-u,v],[u,-v]],c=[];for(let j=0;j<2;j++){let a=r+1+2*i+j;c.push([...B[j],a],[...B[j],-a])}return {u,v,d,c}});
const flat=mm=>mm.flatMap(e=>e.c);
const fix=(x,h)=>{let s=x.toString(2);if(s.length>h)throw Error("overflow");return s.padStart(h,"0")};
function enc(cs){let names=[...new Set(cs.flat().map(Math.abs))].sort((a,b)=>a-b),n=names.length,m=cs.length,h=Math.ceil(Math.log2(Math.max(n,m)+1)),index=new Map(names.map((x,i)=>[x,i+1]));let s="1".repeat(h)+"0"+fix(n,h)+fix(m,h);for(let c of cs){ok(c.length===3&&new Set(c.map(Math.abs)).size===3,"nonproper");for(let l of c)s+=(l<0?"1":"0")+fix(index.get(Math.abs(l)),h)}return {s,n,m,names,h}}
function dec(s){let h=0;while(s[h]==="1")h++;ok(s[h]==="0"&&h>0,"bad unary header");let p=h+1;function take(j){let t=s.slice(p,p+j);ok(t.length===j,"short");p+=j;return t}let n=parseInt(take(h),2),m=parseInt(take(h),2),cc=[];for(let i=0;i<m;i++){let c=[];for(let j=0;j<3;j++){let sign=take(1)==="1"?-1:1,id=parseInt(take(h),2);ok(id>0&&id<=n,"index");c.push(sign*id)}ok(new Set(c.map(Math.abs)).size===3,"duplicate");cc.push(c)}ok(p===s.length,"extra bytes");return {n,m,cc}}
const back=(e,names)=>e.cc.map(c=>c.map(l=>Math.sign(l)*names[Math.abs(l)-1]));
function parity(r,mm){let p=Array.from({length:r+1},(_,i)=>i),v=new Array(r+1).fill(0),rank=new Array(r+1).fill(0);function find(i){if(p[i]===i)return i;let a=p[i],root=find(a);v[i]^=v[a];p[i]=root;return root}for(let {u,v:w,d} of mm){let a=find(u),b=find(w);if(a===b){if((v[u]^v[w])!==d)return false}else if(rank[a]<rank[b]){p[a]=b;v[a]=v[u]^v[w]^d}else{p[b]=a;v[b]=v[u]^v[w]^d;if(rank[a]===rank[b])rank[a]++}}return true}
function evalC(cs,a){return cs.every(c=>c.some(l=>a[Math.abs(l)-1]===(l>0?1:0)))}
function models(r,mm){let cc=flat(mm),n=3*r,count=0;for(let x=0;x<2**n;x++){let a=Array.from({length:n},(_,i)=>Math.floor(x/2**i)%2);if(evalC(cc,a))count++}return count}
function profile(e){let {u,v,d,c}=e,aux=[...new Set(c.flat().map(Math.abs))].filter(x=>x!==u&&x!==v),bits="";for(let a=0;a<2;a++)for(let b=0;b<2;b++){let found=false;for(let q=0;q<4;q++){let vals=new Array(Math.max(...aux,u,v)).fill(0);vals[u-1]=a;vals[v-1]=b;vals[aux[0]-1]=q%2;vals[aux[1]-1]=Math.floor(q/2);if(evalC(c,vals))found=true}bits+=found?"1":"0"}return bits}
const rows=[];
for(let r of [3,4,5,6,8,12,32,128]){
 let Y=formulas(r,false),U=formulas(r,true),ey=enc(flat(Y)),eu=enc(flat(U));
 ok(ey.s.length===eu.s.length&&ey.n===3*r&&ey.m===4*r,"paired dimensions");
 ok(JSON.stringify(back(dec(ey.s),ey.names))===JSON.stringify(flat(Y)),"root YES parse");
 ok(JSON.stringify(back(dec(eu.s),eu.names))===JSON.stringify(flat(U)),"root NO parse");
 ok(parity(r,Y)&&!parity(r,U),"root labels");
 for(let mm of [Y,U]){ok(new Set(flat(mm).map(c=>c.join(","))).size===4*r,"unique clauses");for(let e of mm)ok(profile(e)===(e.d?"0110":"1001"),"module exact profile")}
 if(r<=5){ok(models(r,Y)===2**(2*r+1),"YES models");ok(models(r,U)===0,"NO models")}
 let subsets=0;
 if(r<=8){for(let mask=0;mask<2**r-1;mask++){ok(parity(r,Y.filter((_,i)=>mask&(1<<i)))&&parity(r,U.filter((_,i)=>mask&(1<<i))),"strict join SAT");subsets++}}
 else{for(let k of [1,2,3,4,8,Math.floor(r/2),r-1]){ok(parity(r,Y.slice(0,k))&&parity(r,U.slice(0,k)),"prefix SAT");subsets++}}
 let levels=[null,null];
 if(r%4===0){
  for(let mm of [Y,U]){let L1=[],L2=[];for(let s=0;s<2;s++){let chunk=mm.slice(s*r/2,(s+1)*r/2),E=enc(flat(chunk)),D=dec(E.s),unpacked=back(D,E.names);ok(JSON.stringify(unpacked)===JSON.stringify(flat(chunk)),"first level source identity");ok(parity(r,chunk),"first level SAT");L1.push(E.s.length);
   for(let q=0;q<2;q++){let cc=D.cc.slice(q*r,(q+1)*r),leaf=enc(cc),test=dec(leaf.s),actual=mm.slice(s*r/2+q*r/4,s*r/2+(q+1)*r/4);ok(JSON.stringify(back(test,leaf.names))===JSON.stringify(cc),"second level parse");ok(JSON.stringify(unpacked.slice(q*r,(q+1)*r))===JSON.stringify(flat(actual)),"second level source names");ok(parity(r,actual),"second level SAT");L2.push(leaf.s.length)}
  }if(mm===Y)levels=[L1,L2];else ok(JSON.stringify(levels)===JSON.stringify([L1,L2]),"matched child sizes")}
 }
 rows.push({edges:r,root_bits:ey.s.length,level1_bits:levels[0],level2_bits:levels[1],strict_proper_subjoins_checked:subsets,yes_root_models:r<=5?2**(2*r+1):"symbolic 2^(2r+1)",no_root_models:0});
}
return {run:"ARC-NAMED-CYCLE-INTERFACE110",checks,rows,encoding:"unary h + n,m each h bits + three signed h-bit source indices per clause, h=ceil(log2(max(n,m)+1)); N=3h+1+3m(h+1)",scope:"ordinary proper 3CNF, outside C_star",status:"PROVED/EXACT symbolic parity proof separately; finite COMPUTATIONAL; ARC-EDGE-90 OPEN"};
};
console.log(JSON.stringify(audit(),null,2));
