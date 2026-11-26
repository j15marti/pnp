// node message_audit.js
// Exact bounded matching enumeration, not a polynomial FKT implementation.
function audit(){
let seed=170426,rand=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%n},checks=0;
function pm(n,E,remove=[]){let A=Array.from({length:n},()=>[]);for(let [a,b,w]of E){A[a].push([b,BigInt(w)]);A[b].push([a,BigInt(w)])}let mask=(1n<<BigInt(n))-1n;for(let v of remove)mask&=~(1n<<BigInt(v));let memo=new Map;function f(s){if(!s)return 1n;if(memo.has(s))return memo.get(s);let a=0;while(!(s>>BigInt(a)&1n))a++;let m=s^(1n<<BigInt(a)),v=0n;for(let[b,w]of A[a])if(m>>BigInt(b)&1n)v+=w*f(m^(1n<<BigInt(b)));memo.set(s,v);return v}return f(mask)}
function gadget(E,n,par,w0,w1){let a=n,b=n+1;if(!par){E.push([a,n+2,w0],[n+2,n+3,w1],[n+3,b,1]);return [a,b,n+4]}E.push([a,n+2,w1],[b,n+2,w0]);return [a,b,n+3]}
for(let par of [0,1])for(let w0=0;w0<5;w0++)for(let w1=0;w1<5;w1++){let E=[],[a,b,n]=gadget(E,0,par,w0,w1);for(let bits=0;bits<4;bits++){let r=[];if(bits&1)r.push(a);if(bits&2)r.push(b);let val=par?(bits===1?w0:bits===2?w1:0):(bits===0?w0:bits===3?w1:0);if(pm(n,E,r)!==BigInt(val))throw Error("binary response");checks++}}
let cases=0,zero=0,positive=0;
for(let d=2;d<=7;d++)for(let trial=0;trial<50;trial++){
 let N=2*d,E=[];for(let i=0;i<N;i++)E.push([i,(i+1)%N,1+rand(5)]);
 let p=[],w=[],H=E.slice(),n=N;
 for(let i=0;i<d;i++){let parity=rand(2),a=rand(5),b=rand(5),c=rand(5),e=rand(5);p.push(parity);w.push([a*c,b*e]);let [u,v,m]=gadget(H,n,parity,a*c,b*e);H.push([2*i,u,1],[2*i+1,v,1]);n=m;}
 let exact=0n;for(let z=0;z<2**d;z++){let rem=[],coef=1n;for(let i=0;i<d;i++){let k=z>>i&1;coef*=BigInt(w[i][k]);if(!p[i]){if(k)rem.push(2*i,2*i+1)}else rem.push(2*i+(k?1:0))}exact+=coef*pm(N,E,rem)}
 let got=pm(n,H);if(got!==exact)throw Error("composition");if(got===0n)zero++;else positive++;cases++;
}
return {seedInitial:170426,localSignatureChecks:checks,weightedStarCases:cases,positive,zero,maxPhases:7,backend:"bounded exact weighted perfect matching recursion"};
}
console.log(JSON.stringify(audit(),null,2));
