function run(){
let seed=20261124;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>16}const bit=()=>rand()&1,par=x=>{let p=0;while(x){p^=1;x&=x-1}return p},pc=x=>{let p=0;while(x){p++;x&=x-1}return p};
function xor(S,x){if(S.has(x))S.delete(x);else S.add(x)}
function add(A,B){let C=new Set(A);for(let x of B)xor(C,x);return C}
function mul(A,B){let C=new Set();for(let x of A)for(let y of B)xor(C,x|y);return C}
function evalp(P,x){let r=0;for(let m of P)if((m&x)===m)r^=1;return r}
function gauss(P,n){let R=new Set(P),k=n,fac=1;while(true){let edge=[...R].find(x=>pc(x)===2);if(edge===undefined)break;let i=edge&-edge,j=edge^i,A=new Set(),B=new Set(),C=new Set();for(let m of R){if(m===edge)continue;if(m&i)xor(A,m^i);else if(m&j)xor(B,m^j);else xor(C,m)}R=add(C,mul(A,B));k-=2;fac*=2}return [...R].some(x=>x!==0)?0:fac*2**k*(R.has(0)?-1:1)}
function count(eq,n){let total=0;for(let mask=0;mask<2**eq.length;mask++){let P=new Set();for(let i=0;i<eq.length;i++)if(mask>>i&1)P=add(P,eq[i]);total+=gauss(P,n)}return total/2**eq.length}
function basisAdd(B,x){while(x){let j=31-Math.clz32(x);if(B[j])x^=B[j];else{B[j]=x;return true}}return false}
function insert(B,x){basisAdd(B,x)}
function nullvec(B,n){for(let i=1;i<2**n;i++)if(B.every(b=>!par(b&i)))yieldDummy(i)}
function yieldDummy(){}
function affine(n){let s=new Set();if(bit())s.add(0);for(let i=0;i<n;i++)if(bit())s.add(1<<i);return s}
function shift(P,off){return new Set([...P].map(m=>m<<off))}
function varp(i){return new Set([1<<i])}
function sum(A){return A.reduce(add,new Set())}
function constant(b){return new Set(b?[0]:[])}
function pins(n,x){return Array.from({length:n},(_,i)=>add(varp(i),constant(x>>i&1)))}
function recover(eq,p,n){let B=[],probes=0,counts=0;let dim=p.length; // enumerate dual nullspace only in tiny tests, production uses Gaussian kernel.
while(true){let grew=false;for(let f=1;f<2**dim;f++){if(!B.every(v=>!par(v&f)))continue;let probe=add(sum(p.filter((_,i)=>f>>i&1)),constant(1));probes++;let es=[...eq,probe];counts++;if(!count(es,n))continue;let x=0; // use direct feasibility scan for witness in test; exact Fourier self reduction separately tested below
for(;x<2**n;x++)if(es.every(q=>!evalp(q,x)))break;if(x===2**n)throw Error("false witness");
let v=p.reduce((a,q,i)=>a|(evalp(q,x)<<i),0);if(!basisAdd(B,v))throw Error("no growth");grew=true;break}if(!grew)break}return {B,probes,counts}}
let stats={seed:20261124,systems:0,sat:0,unsat:0,spanChecks:0,probeChecks:0,rawAssignments:0,liftAssignments:0,gaussChecks:0,hostile:0,rankExamples:[],closureChecks:0};
for(let z=0;z<160;z++){let n=3+rand()%2,P=3,u=2,a=1+rand()%2,h=1,l=1,base=n+h,ui=base,zi=ui+u,ei=zi+1,N=ei+l;
// lifted guards use arbitrary affine functions of x and y; y=x0*x1. Stable dimension 3, only first direction varies; w2,w3 arbitrary affine in x,y,u,z.
let q=new Set([(1<<0)|(1<<1)]),def=add(varp(n),q);let E=Array.from({length:a},()=>Array.from({length:u},()=>affine(base)));let v=Array.from({length:a},()=>affine(base));let leak=Array.from({length:u},()=>affine(base));for(let p of leak)p.delete(0);
let le=sum(leak.map((p,i)=>mul(p,varp(ui+i))));let eq=[def,add(varp(ei),le),...E.map((r,j)=>add(v[j],sum(r.map((p,i)=>mul(p,varp(ui+i))))))];if(z%5===0)eq.push(new Set([0])); // UNSAT control
let w=[add(affine(zi+1),varp(ei)),affine(zi+1),affine(zi+1)];let coeff=Array.from({length:P},()=>Array.from({length:3},()=>affine(base)));let offsets=Array.from({length:P},()=>affine(base));let p=[constant(1),...Array.from({length:n},(_,i)=>varp(i)),...coeff.map((r,j)=>add(offsets[j],sum(r.map((b,i)=>mul(b,w[i])))))];
let ref=[],lift=[],nr=0,nl=0;for(let x=0;x<2**N;x++){stats.liftAssignments++;if(eq.every(q=>!evalp(q,x))){nl++;insert(lift,p.reduce((v,q,i)=>v|(evalp(q,x)<<i),0))}}
// independently reconstruct y and leakage from raw x,u,z, then check only residual equations (not definitions).
for(let raw=0;raw<2**(n+u+1);raw++){stats.rawAssignments++;let x=(raw&((1<<n)-1))|((raw>>n)<<base);x|=evalp(q,x)<<n;x|=evalp(le,x)<<ei;if(eq.slice(2).every(q=>!evalp(q,x))){nr++;insert(ref,p.reduce((v,q,i)=>v|(evalp(q,x)<<i),0))}}
if(nr!==nl||count(eq,N)!==nr)throw Error("count mismatch");
let rr=recover(eq,p,N);stats.probeChecks+=rr.probes;let rank=B=>B.filter(Boolean).length;let union=[...ref];for(let b of rr.B)if(b)insert(union,b);for(let b of lift)if(b)insert(union,b);
if(rank(ref)!==rank(rr.B)||rank(ref)!==rank(lift)||rank(union)!==rank(ref))throw Error("span mismatch");
stats.systems++;stats.spanChecks++;if(nr)stats.sat++;else stats.unsat++;
// certify pins via same quadratic count; conditional query uses one quadratic phase.
for(let b=0;b<2;b++){let es=[...eq,add(varp(0),constant(b))],direct=0;for(let x=0;x<2**N;x++)if(es.every(q=>!evalp(q,x)))direct++;if(count(es,N)!==direct)throw Error("pin mismatch");stats.closureChecks++}
}
for(let t=0;t<300;t++){let n=1+rand()%8,R=affine(n);for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(bit())R.add((1<<i)|(1<<j));let exact=0;for(let x=0;x<2**n;x++)exact+=evalp(R,x)?-1:1;if(gauss(R,n)!==exact)throw Error("Gauss mismatch");stats.gaussChecks++}
// quartic/cubic leakage cannot be silently erased: u*x0*x1, choose x0=x1=u=1. y=x0*x1, eta=y*u; p=x0*eta = x0*x1*u.
let q=new Set([3]),eq=[add(varp(2),q),add(varp(4),mul(varp(2),varp(3)))],p=mul(varp(0),varp(4));let c=count([...eq,add(p,constant(1))],5);if(c!==1)throw Error("hostile mismatch");stats.hostile=c;
return stats
}
console.log(JSON.stringify(run(),null,2));
