"use strict";
function audit(){
let seed=20261014>>>0, checks=0, failures=[], cases=0, easy=0, empty=0, hard=[], rankDistribution={};
function random(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
function rnd(n){return random()%n;}
function assert(cond,msg){checks++;if(!cond){failures.push(msg);if(failures.length>10)throw Error("Too many failures: "+failures.join(";"));}}
function parity(x){let p=0;while(x){p^=1;x&=x-1;}return p;}
function applyA(rows,x){let y=0;for(let i=0;i<rows.length;i++)y|=parity(rows[i]&x)<<i;return y;}
function rankBasis(vecs,m){let arr=Array(m).fill(0);for(let v of vecs){let x=v;for(let bit=m-1;bit>=0&&x;bit--){if(!((x>>>bit)&1))continue;if(arr[bit])x^=arr[bit];else{arr[bit]=x;break;}}}return arr.filter(x=>x!==0);}
function combine(basis,z){let x=0;for(let i=0;i<basis.length;i++)if((z>>>i)&1)x^=basis[i];return x;}
function isInSpan(basis,x,m){return rankBasis([...basis,x],m).length===basis.length;}
function buildKrylov(A,e0,E,m){let vecs=[];for(let v of [e0,...E]){for(let j=0;j<m;j++){vecs.push(v);v=applyA(A,v);}}return rankBasis(vecs,m);}
function solveGF2(eq,d){let rows=eq.map(v=>({...v})), piv=[], k=0;for(let bit=0;bit<d;bit++){let p=k;while(p<rows.length&&!((rows[p].mask>>>bit)&1))p++;if(p===rows.length)continue;[rows[k],rows[p]]=[rows[p],rows[k]];for(let j=0;j<rows.length;j++)if(j!==k&&((rows[j].mask>>>bit)&1)){rows[j].mask^=rows[k].mask;rows[j].rhs^=rows[k].rhs;}piv.push(bit);k++;}
for(let i=k;i<rows.length;i++)if(rows[i].mask===0&&rows[i].rhs)return null;
let z0=0;for(let j=0;j<k;j++)if(rows[j].rhs)z0|=1<<piv[j];
let free=[];for(let j=0;j<d;j++)if(!piv.includes(j))free.push(j);
let ker=[];for(let f of free){let z=1<<f;for(let j=0;j<k;j++)if((rows[j].mask>>>f)&1)z|=1<<piv[j];ker.push(z);}return {z0,ker};}
for(let m=2;m<=7;m++){
let size=1<<m, total=155;for(let it=0;it<total;it++){
let A=Array.from({length:m},()=>rnd(size)), b=rnd(size), r=1+rnd(Math.min(3,m)), E=Array.from({length:r},()=>rnd(size)), s0=rnd(size);
let params=Array.from({length:r},()=>({i:rnd(m),j:rnd(m),k:rnd(m),offset:rnd(2)}));
function f(s){let y=0;for(let i=0;i<r;i++){let p=params[i],v=(((s>>>p.i)&1)&((s>>>p.j)&1))^((s>>>p.k)&1)^p.offset;y|=v<<i;}return y;}
function T(s){let ff=f(s), x=applyA(A,s)^b;for(let i=0;i<r;i++)if((ff>>>i)&1)x^=E[i];return x;}
let e0=applyA(A,s0)^b^s0,W=buildKrylov(A,e0,E,m),d=W.length;
let states=[];for(let z=0;z<(1<<d);z++)states.push(s0^combine(W,z));
let stateSet=new Set(states);assert(stateSet.size===(1<<d),"affine span distinctness "+m+":"+it);
for(let s of states)assert(stateSet.has(T(s)),"closure "+m+":"+it);
let orbit=[],seen=new Set(),s=s0;while(!seen.has(s)){seen.add(s);orbit.push(s);assert(stateSet.has(s),"orbit contained "+m+":"+it);s=T(s);}
assert(orbit.length<=size,"cycle bounded");
let oDim=1+rnd(Math.min(4,m)), C=Array.from({length:oDim},()=>rnd(size)),offset=rnd(1<<oDim), out=(s)=>applyA(C,s)^offset;
let gNum=rnd(Math.min(m,4)+1),G=Array.from({length:gNum},()=>rnd(size)), h=Array.from({length:gNum},()=>rnd(2));
let eq=G.map((row,i)=>({mask:W.reduce((a,w,j)=>a|(parity(row&w)<<j),0),rhs:h[i]^parity(row&s0)}));
let sol=solveGF2(eq,d), guard=s=>G.every((row,i)=>parity(row&s)===h[i]);
let exact=new Set(states.filter(guard).map(out)), reachable=new Set(orbit.filter(guard).map(out));
if(sol===null){assert(exact.size===0,"guard empty");empty++;}
else{
let start=s0^combine(W,sol.z0), v=out(start),outBasis=rankBasis(sol.ker.map(z=>applyA(C,combine(W,z))),oDim),rho=outBasis.length;
assert(exact.size===(1<<rho),"output cardinality "+m+":"+it);
for(let z=0;z<(1<<rho);z++)assert(exact.has(v^combine(outBasis,z)),"affine image exact");
rankDistribution[rho]=(rankDistribution[rho]||0)+1;if(rho<=1)easy++;
}
for(let x of reachable)assert(exact.has(x),"reachable guard sound");
cases++;
}}
let latchCases=0;
for(let m=2;m<=7;m++){let max=1<<m;for(let it=0;it<90;it++){
let stop=rnd(max),target=rnd(max), seen=new Set(), work=0, flag=0;
while(!seen.has(work+"|"+flag)){seen.add(work+"|"+flag);let nextFlag=flag||(work===target)?1:0, nextWork=work<stop?work+1:work;work=nextWork;flag=nextFlag;}
assert(seen.has("0|0"),"initial latch");assert([...seen].some(x=>x.endsWith("|1"))===(target<=stop),"latch iff target visited "+m);
latchCases++;
}}
let shiftControls=0;
for(let m=3;m<=8;m++){let E=1<<(m-1), A=Array.from({length:m},(_,i)=>i<m-1?(1<<(i+1)):0);
let W=buildKrylov(A,0,[E],m);
assert(W.length===m,"shift cyclic span full");
let z=0;for(let i=0;i<10;i++){let f=((z&1)&&((z>>1)&1))?1:0;z=applyA(A,z)^(f?E:0);assert(z===0,"zero orbit stays fixed");}
shiftControls++;
}
return {run_id:"KRYLOVPSPACE1",seed_initial:20261014,scope:"Finite transition matrices with arbitrary small nonlinear Boolean feedback; no PSPACE-hardness inference from tests",total_cases:cases,checks,failures,affine_output_small:easy,empty_guard:empty,rank_distribution:rankDistribution,latch_cases:latchCases,shift_controls:shiftControls,methods:"Exact full affine-state closure; orbit enumeration; affine Gaussian guarded image; deterministic fixed LCG; 155 cases per state dimension 2-7 and 90 latch tests per dimension", status:failures.length?"FAILED":"PASS"};
}

const report=audit();
if(typeof console!=="undefined")console.log(JSON.stringify(report,null,2));
