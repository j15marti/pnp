/* ARC-TYPED-LASSO169 reproducibility audit.
   Node.js >= 18; no dependencies. Exact BigInt rational profiles.
   This tests conditional exponent identities and actual finite CNF
   recursion, not FLMV machine bit-work or an all-input ARC edge. */
(function main(){
"use strict";
let checks=0;
function ok(p,m){checks++; if(!p)throw new Error("assertion "+checks+": "+m);}
function gcd(a,b){while(b!==0n){let t=a%b;a=b;b=t;}return a<0n?-a:a;}
function R(n,d){let a=BigInt(n),b=d===undefined?1n:BigInt(d);if(b===0n)throw Error("division by zero");if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return {n:a/g,d:b/g};}
function add(x,y){return R(x.n*y.d+y.n*x.d,x.d*y.d);}
function sub(x,y){return R(x.n*y.d-y.n*x.d,x.d*y.d);}
function mul(x,y){return R(x.n*y.n,x.d*y.d);}
function div(x,y){return R(x.n*y.d,x.d*y.n);}
function cmp(x,y){let v=x.n*y.d-y.n*x.d;return v<0n?-1:v>0n?1:0;}
function mx(x,y){return cmp(x,y)>=0?x:y;}
function str(x){return String(x.n)+"/"+String(x.d);}
const z=R(0),one=R(1),c=R(241,200),d=R(11642479,23232400);
ok(cmp(d,R(1,2))>0,"FLMV d above half");
function step(e,p){return [mx(e.L,add(e.u,mul(e.l,p[0]))),mx(e.V,mul(e.nu,p[1]))];}
function run(word,p){for(let e of word)p=step(e,p);return p;}
function profile(word){
  let A=z,lam=one,Q=null,nu=one,P=null;
  for(let e of word){
    Q=Q===null?e.L:mx(e.L,add(e.u,mul(e.l,Q)));
    A=add(e.u,mul(e.l,A));
    lam=mul(e.l,lam);
    P=P===null?e.V:mx(e.V,mul(e.nu,P));
    nu=mul(e.nu,nu);
  }
  return {A:A,lam:lam,Q:Q,P:P,nu:nu};
}
function fixed(word){
  let p=profile(word);
  ok(cmp(p.lam,one)<0&&cmp(p.nu,one)<0,"strict composite slope");
  return [mx(p.Q,div(p.A,sub(one,p.lam))),p.P];
}
function edge(from,to,ln,ld,un,ud,Ln,Ld,Vn,Vd,nun,nud){
  return {from:from,to:to,l:R(ln,ld),u:R(un,ud),L:R(Ln,Ld),V:R(Vn,Vd),nu:R(nun,nud)};
}
let e01=edge(0,1,1,2,1,10,1,1,1,3,1,2);
let e10=edge(1,0,2,3,1,5,1,1,1,3,2,3);
let ex=edge(0,2,3,4,1,4,11,10,2,5,3,4);
let cycle=[e01,e10], k0=R(1000),start=[k0,k0];
let original=[];for(let j=0;j<20;j++)original.push(...cycle);original.push(ex);
let seedOutput=run(original,start);
ok(cmp(seedOutput[0],c)<0&&cmp(seedOutput[1],d)<0,"reference typed route strict hit");
let fixedCycle=fixed(cycle);
ok(cmp(fixedCycle[0],start[0])<0&&cmp(fixedCycle[1],start[1])<0,"first cycle decreases both");
const pumped=[];
for(let K of [1000,10000,1000000,1000000000]){
  let pre=[R(K),R(K)],m=0;
  while(cmp(pre[0],start[0])>0||cmp(pre[1],start[1])>0){
    pre=run(cycle,pre);m++;
    ok(m<100,"typed cycle reaches original pre-cycle envelope");
  }
  let after=run(original,pre);
  ok(cmp(after[0],c)<0&&cmp(after[1],d)<0,"pumped full route strict hit");
  pumped.push({K:K,extra_cycles:m,time:str(after[0]),space:str(after[1])});
}
let rng=20261025;function randomInt(n){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng%n;}
let algebraCases=0;
for(let t=0;t<100;t++){
  let word=[];
  for(let j=0;j<1+randomInt(6);j++){
    let den=2+randomInt(5),ln=1+randomInt(den-1);
    let sn=1+randomInt(den-1);
    word.push(edge(0,0,ln,den,randomInt(9),10,randomInt(15),10,randomInt(11),10,sn,den));
  }
  let p=profile(word);
  for(let K of [2,3,10,100,1000]){
    let q=run(word,[R(K),R(K)]);
    let q2=[mx(p.Q,add(p.A,mul(p.lam,R(K)))),mx(p.P,mul(p.nu,R(K)))];
    ok(cmp(q[0],q2[0])===0&&cmp(q[1],q2[1])===0,"composite path max-affine identity");
    algebraCases++;
  }
  let f=fixed(word);
  let at=run(word,f);
  ok(cmp(f[0],at[0])===0&&cmp(f[1],at[1])===0,"fixed point exact");
}
let boundary=edge(0,0,1,2,241,400,0,1,1,5,1,2);
let br=[R(1000),R(1000)];
for(let j=0;j<36;j++){br=step(boundary,br);ok(cmp(br[0],c)>0,"boundary fixed point is not strict entry");}
let acyclic=edge(0,1,1,1000,0,1,11,10,2,5,1,1000);
ok(cmp(run([acyclic],[R(100),R(100)])[0],c)<0,"one small-K acyclic hit");
ok(cmp(run([acyclic],[R(1000000),R(1000000)])[0],c)>0,"one-shot edge not cofinal");
function encode(F,n){
  let s="p cnf "+n+" "+F.length+"\n";
  for(let C of F)s+=C.join(" ")+(C.length?" ":"")+"0\n";
  return s;
}
function parse(s){
  let lines=s.trimEnd().split("\n"),m=/^p cnf ([0-9]+) ([0-9]+)$/.exec(lines[0]);
  if(!m)throw Error("invalid CNF header");
  let n=Number(m[1]),size=Number(m[2]);
  if(n>20||size!==lines.length-1)throw Error("invalid CNF size");
  let F=[];
  for(let raw of lines.slice(1)){
    let t=raw.trim().split(/\s+/).map(Number);
    if(t[t.length-1]!==0||t.slice(0,-1).some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>n))throw Error("invalid literal");
    F.push(t.slice(0,-1));
  }
  return {F:F,n:n};
}
function sat(F,n){
  for(let m=0;m<(1<<n);m++){
    if(F.every(C=>C.some(l=>{let bit=((m>>(Math.abs(l)-1))&1)===1;return l>0?bit:!bit;})))return true;
  }
  return false;
}
function pin(F,v,b){
  let G=[];
  for(let C of F){
    if(C.some(l=>Math.abs(l)===v&&((l>0)===b)))continue;
    G.push(C.filter(l=>Math.abs(l)!==v));
  }
  return G;
}
let rootSAT=0,rootUNSAT=0,firstChildren=0,grandchildren=0,serializedBytes=0,leafDecisions=0;
function twoLevels(F,n){
  let root=encode(F,n),a=parse(root);ok(a.F.length===F.length,"root ordinary parse");
  let result=false;
  for(let b of [false,true]){
    let first=encode(pin(a.F,1,b),n),parsed=parse(first);
    firstChildren++;serializedBytes+=first.length;
    for(let d0 of [false,true]){
      let second=encode(pin(parsed.F,2,d0),n),g=parse(second);
      grandchildren++;serializedBytes+=second.length;
      result=result||sat(g.F,n);leafDecisions++;
    }
  }
  let expected=sat(a.F,n);
  ok(result===expected,"two REAL recursive levels preserve both labels");
  if(expected)rootSAT++;else rootUNSAT++;
}
let cube=[];
for(let a=0;a<8;a++){let C=[];for(let j=0;j<3;j++)C.push((a>>j)&1?-(j+1):j+1);cube.push(C);}
for(let mask=0;mask<256;mask++){let F=[];for(let j=0;j<8;j++)if((mask>>j)&1)F.push(cube[j]);twoLevels(F,3);}
function parityCycle(seed,n){
  let F=[];
  for(let i=0;i<n;i++){
    let x=i+1,y=((i+1)%n)+1,b=(seed>>i)&1;
    if(b===0)F.push([-x,y],[x,-y]);
    else F.push([x,y],[-x,-y]);
  }
  return F;
}
let paritySAT=0,parityUNSAT=0;
for(let s=0;s<128;s++){
  let F=parityCycle(s,7),b=s.toString(2).split("1").length-1;
  ok(sat(F,7)===(b%2===0),"cycle parity independent control");
  if(b%2===0)paritySAT++;else parityUNSAT++;
  twoLevels(F,7);
}
for(let F of [[[1],[-1]],[[1],[-1,2],[-2]],[[1,2],[1,-2]],[[1,2,3]],[]])twoLevels(F,3);
ok(sat([[1]],1)&&sat([[-1]],1)&&!sat([[1],[-1]],1),"independent child SAT bits cannot be AND-joined");
let invalidRejected=false;try{parse("p cnf 3 1\n1 2 4 0\n");}catch(_){invalidRejected=true;}ok(invalidRejected,"malformed ordinary source rejected");
let scales=[];
for(let count of [16,32,64,128,256,512]){
  let F=[];for(let j=0;j<count;j++){F.push([1,2,3]);F.push([-1,-2,3]);}
  let n0=encode(F,3).length,n1=encode(pin(F,1,false),3).length;
  scales.push({copies:count,length_root:n0,length_first:n1,effective_lambda:Math.log(n1)/Math.log(n0)});
  ok(n1>Math.sqrt(n0),"fixed guard is not power-short lambda=1/2");
}
let result={run_id:"ARC-TYPED-LASSO169",status:"COMPUTATIONAL plus conditional exact mathematics",
checks:checks,failures:0,seed:20261025,algebra_cases:algebraCases,
graph_types:3,graph_edges:3,typed_reference_route_edges:original.length,
reference_time:str(seedOutput[0]),reference_space:str(seedOutput[1]),
cycle_fixed_time:str(fixedCycle[0]),cycle_fixed_space:str(fixedCycle[1]),
pumped:pumped,boundary_steps:36,cnf_roots:rootSAT+rootUNSAT,
cnf_sat:rootSAT,cnf_unsat:rootUNSAT,parity_sat:paritySAT,parity_unsat:parityUNSAT,
first_ordinary_children:firstChildren,second_ordinary_children:grandchildren,
independent_leaf_decisions:leafDecisions,ordinary_child_bytes_written:serializedBytes,
fixed_guard_scales:scales,
limits:"No all-input contractor; profiles abstract not FLMV machine steps; CNF tests small/easy; two real ordinary serialization levels; no physical bit-time/flip/switch trace."};
if(typeof process!=="undefined"&&process.stdout)process.stdout.write(JSON.stringify(result,null,2)+"\n");
return result;
})()