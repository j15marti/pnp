"use strict";
// LSPV-2 INLINE-CONE-TRANSFER367, finite source-authenticated compiler.
// Legal paid mixed steps: RES, AND3, GF(2) XOR, and conservative AND2 VARDEF.
// This is a finite control (n<=6), not a proof of the all-size theorem.
const ck=(x,m)=>{if(!x)throw Error(m);}, b=(a,v)=>(a>>(v-1))&1;
const uniq=(...xs)=>[...new Set(xs.flat())].sort((u,v)=>u-v);
const eq=(A,B)=>A.length===B.length&&A.every(x=>B.includes(x));
const block=(a,S)=>S.map(v=>b(a,v)?-v:v),key=(a,S)=>S.reduce((z,v,i)=>z|(b(a,v)<<i),0);
function resolve(A,B,p){ck(A.includes(p)&&B.includes(-p),"bad pivot");let C=uniq(A.filter(x=>x!==p),B.filter(x=>x!==-p));ck(!C.some(x=>C.includes(-x)),"tautology");return C;}
function makeDef(){return {name:"signed_AND_DEF",n:2,defs:{3:[1,2]},root:10,lines:[
 {op:"src",C:[1]},{op:"src",C:[2]},{op:"src",C:[-1,-2]},
 {op:"slot",v:3,k:0},{op:"slot",v:3,k:1},{op:"slot",v:3,k:2},
 {op:"res",P:[0,5],pivot:1,C:[3,-2]},{op:"res",P:[1,6],pivot:2,C:[3]},
 {op:"res",P:[2,3],pivot:1,C:[-3,-2]},{op:"res",P:[1,8],pivot:2,C:[-3]},
 {op:"res",P:[7,9],pivot:3,C:[]}]};}
function makeXor(){let L=[],roots=[];
 for(let rhs of [0,1]){let ss=[];for(let a=0;a<8;a++)if((b(a,1)^b(a,2)^b(a,3))!==rhs)ss.push(L.push({op:"src",C:block(a,[1,2,3])})-1);
 let cur=ss[0];for(let j=1;j<4;j++){cur=L.push({op:"and",P:[cur,ss[j]]})-1;if(j===3)L[cur].row={mask:[1,2,3],rhs};}roots.push(cur);}
 let root=L.push({op:"xor",P:roots,mask:[],rhs:1,row:{mask:[],rhs:1}})-1;
 return {name:"opposite_XOR3",n:3,defs:{},lines:L,root};}
function C(p,z){if(z.op==="src"||z.op==="res")return z.C;if(z.op==="slot"){let [a,b]=p.defs[z.v],v=z.v;return [[-v,a],[-v,b],[v,-a,-b]][z.k];}throw Error("not clause");}
function gv(p,v,a){if(!p.defs[v])return b(a,v);let [x,y]=p.defs[v],lit=z=>{let u=gv(p,Math.abs(z),a);return z>0?u:1-u;};return lit(x)&lit(y);}
function ev(p,i,a){let z=p.lines[i];if(["src","slot","res"].includes(z.op))return C(p,z).some(l=>gv(p,Math.abs(l),a)===(l>0?1:0));
 if(z.op==="and")return z.P.every(j=>ev(p,j,a));if(z.op==="xor")return z.mask.reduce((w,v)=>w^b(a,v),0)===z.rhs;throw Error("unknown op");}
function ovars(p,v){return p.defs[v]?uniq(...p.defs[v].map(x=>ovars(p,Math.abs(x)))):[v];}
function supp(p,i){let z=p.lines[i];if(["src","slot","res"].includes(z.op))return uniq(...C(p,z).map(l=>ovars(p,Math.abs(l))));
 if(z.op==="and")return uniq(...z.P.map(j=>supp(p,j)));if(z.op==="xor")return uniq(z.mask);throw Error("support");}
function vm(p){
 let {lines:L,n}=p;ck(n>=1&&n<=6,"n cap");let q=Object.keys(p.defs).length,src=L.filter(z=>z.op==="src");
 for(let i=0;i<L.length;i++){let z=L[i],S=supp(p,i);ck(S.every(v=>v>=1&&v<=n),"bad variable");
  if(z.op==="src"||z.op==="slot")continue;
  ck(z.P.length===2&&z.P.every(j=>j>=0&&j<i),"parents");q++;
  if(z.op==="res"){let a=C(p,L[z.P[0]]),b=C(p,L[z.P[1]]);ck(eq(z.C,a.includes(z.pivot)?resolve(a,b,z.pivot):resolve(b,a,z.pivot)),"res mismatch");}
  if(z.op==="and")ck(S.length<=3,"AND arity");
  if(z.op==="xor"){let [a,b]=z.P.map(j=>L[j].row);ck(!!a&&!!b,"missing affine");
   let m=uniq(a.mask,b.mask).filter(v=>a.mask.includes(v)!==b.mask.includes(v));ck(eq(m,z.mask)&&z.rhs===(a.rhs^b.rhs),"wrong XOR");}
  for(let a=0;a<(1<<n);a++){if(z.P.every(j=>ev(p,j,a)))ck(ev(p,i,a),"unsound inference");
   if(z.row)ck(ev(p,i,a)===(z.row.mask.reduce((w,v)=>w^b(a,v),0)===z.row.rhs),"false affine tag");}
 }
 let all=Array.from({length:1<<n},(_,a)=>a);
 return {q,unsat:all.every(a=>!src.every(z=>z.C.some(l=>b(a,Math.abs(l))===(l>0?1:0)))),rootFalse:all.every(a=>!ev(p,p.root,a))};}
function compile(p){
 let v=vm(p);ck(v.unsat&&v.rootFalse,"not UNSAT/refutation");let L=p.lines,n=p.n,orig=[],raw=[],srcids=new Map();
 L.forEach((z,i)=>{if(z.op==="src"){srcids.set(i,raw.length);raw.push({op:"src",C:z.C,source:orig.length});orig.push(z.C);}});
 let maps=new Map(),supports=new Map(),profile=[];
 for(let i=0;i<L.length;i++){let z=L[i],S=supp(p,i),M=new Map();maps.set(i,M);supports.set(i,S);
  if(z.op==="src"){for(let a=0;a<(1<<n);a++)if(!ev(p,i,a)){M.set(key(a,S),srcids.get(i));break;}continue;}
  if(z.op==="slot")continue;
  let U=uniq(S,...z.P.map(j=>supports.get(j))),E=U.filter(x=>!S.includes(x));profile.push(U.length);
  for(let k=0;k<(1<<S.length);k++){
   let a=0;S.forEach((x,j)=>{if((k>>j)&1)a|=1<<(x-1);});
   if(ev(p,i,a))continue;
   function build(t,u){
    if(t===E.length){let j=z.P.find(j=>!ev(p,j,u));ck(j!==undefined,"unsound entailment");
      let idx=maps.get(j).get(key(u,supports.get(j)));ck(idx!==undefined,"absent premise blocker");
      let D=block(u,U);ck(raw[idx].C.every(l=>D.includes(l)),"not weakening");
      return eq(raw[idx].C,D)?idx:raw.push({op:"weak",parent:idx,C:D})-1;}
    let x=E[t],l=build(t+1,u&~(1<<(x-1))),r=build(t+1,u|(1<<(x-1)));
    return raw.push({op:"res",P:[l,r],pivot:x,C:resolve(raw[l].C,raw[r].C,x)})-1;
   }
   let idx=build(0,a);ck(eq(raw[idx].C,block(a,S)),"wrong blocker");M.set(k,idx);
  }
 }
 let root=maps.get(p.root).get(0);ck(root!==undefined&&raw[root].C.length===0,"missing contradiction");
 // Remove all temporary weakenings by stronger subclause representatives.
 let strict=orig.map((C,i)=>({op:"src",source:i,C})),reps=[];
 raw.forEach((z,i)=>{
  if(z.op==="src"){reps[i]=z.source;return;}if(z.op==="weak"){reps[i]=reps[z.parent];return;}
  let x=reps[z.P[0]],y=reps[z.P[1]],A=strict[x].C,B=strict[y].C;
  if(A.includes(z.pivot)&&B.includes(-z.pivot))reps[i]=strict.push({op:"res",P:[x,y],pivot:z.pivot,C:resolve(A,B,z.pivot)})-1;
  else reps[i]=A.includes(z.pivot)?y:x;
 });
 ck(strict[reps[root]].C.length===0,"erasure final");
 strict.forEach((z,i)=>{if(z.op==="src")ck(eq(z.C,orig[z.source]),"source altered");else{
   ck(z.P.every(k=>k<i),"cyclic strict");ck(eq(z.C,resolve(strict[z.P[0]].C,strict[z.P[1]].C,z.pivot)),"forged strict");}});
 let bound=profile.reduce((s,w)=>s+2**(w+1),0),paid=strict.length-orig.length;ck(paid<=bound,"scope bound exceeded");
 return {name:p.name,n,m:orig.length,q:v.q,maximum_inlined_scope:Math.max(...profile),scope_cost_bound:bound,
   strict_resolution_nodes:paid,temporary_weak_res_nodes:raw.length-orig.length,source:orig,strict};}
function main(){
 let tests=[makeDef(),makeXor()],full=tests.map(compile);
 let sat=[{C:[1,2]},{C:[-1,2]}];
 ck([0,1,2,3].some(a=>sat.every(z=>z.C.some(l=>b(a,Math.abs(l))===(l>0?1:0)))),"SAT witness absent");
 let bad=0;for(let f of [
 ()=>{let x=makeDef();x.lines[6].C=[3];vm(x);},
 ()=>{let x=makeDef();x.lines[6].pivot=2;vm(x);},
 ()=>{let x=makeDef();x.lines[0].C=[99];vm(x);},
 ()=>{let x=makeXor();x.lines.at(-1).rhs=0;vm(x);},
 ()=>{let x=makeXor();x.root=0;compile(x);}
 ])try{f();}catch(e){bad++;}
 ck(bad===5,"hostile fixtures");
 return {name:"LSPV2_INLINE_CONE_TRANSFER367",status:"finite computational controls",summary:full.map(({source,strict,...r})=>r),
   negative_rejections:bad,positive_SAT_control:true,full};
}
const OUT=main();
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(OUT,null,2));
