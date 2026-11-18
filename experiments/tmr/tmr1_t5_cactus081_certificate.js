'use strict';
// TMR-1/081 public finite certificate: oriented-cycle and source gadget controls.
const S=[1,3],mod=x=>(x%5+5)%5;let assertions=0,cycles=0,brutes=0;
function check(x,msg){assertions++;if(!x)throw Error(msg)}
function cycleFactor(s){let a=[1n,0n,0n,0n,0n];for(const sign of s){const b=Array(5).fill(0n);for(let r=0;r<5;r++)for(const d of S)b[mod(r+sign*d)]+=a[r];a=b}return a[0]}
function bruteCycle(s){let ct=0n,n=s.length;for(let k=0;k<5**n;k++){
 let v=k,x=[];for(let j=0;j<n;j++){x.push(v%5);v=Math.floor(v/5)}
 let ok=true;for(let j=0;j<n;j++){const a=x[j],b=x[(j+1)%n],diff=mod(s[j]*(b-a));if(!S.includes(diff)){ok=false;break}}
 if(ok)ct++
 }return ct}
function gcdCycle(p,q){const n=p+q;let ans=0n;for(let i=0;i<=p;i++)for(let j=0;j<=q;j++)if(mod(p-q+2*(i-j))===0)ans+=binom(p,i)*binom(q,j);return ans}
function binom(n,r){let v=1n;for(let i=1;i<=r;i++)v=v*BigInt(n+1-i)/BigInt(i);return v}
for(let n=3;n<=12;n++)for(let mask=0;mask<2**n;mask++){
 const signs=Array.from({length:n},(_,j)=>(mask>>j)&1?1:-1);
 const got=cycleFactor(signs),p=signs.filter(s=>s>0).length;
 check(got>0n,'oriented cycle incorrectly UNSAT');
 check(got===gcdCycle(p,n-p),'cycle coefficient formula mismatch');
 if(n<=7){check(5n*got===bruteCycle(signs),'brute cycle mismatch');brutes++}
 cycles++;
}
const table=[];
for(let diff=0;diff<5;diff++){
 let num=0;
 for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){
  if(S.includes(mod(a))&&S.includes(mod(b-a))&&S.includes(mod(c-b))&&S.includes(mod(c))&&S.includes(mod(diff-c)))num++
 }
 table.push(num)
}
check(table.join(',')==='0,1,0,0,1','five-arc gadget table mismatch');
console.log(JSON.stringify({revision:'tmr1-t5-cactus081-certificate-v1',cycleOrientationCases:cycles,cycleBruteCases:brutes,endpointExtensionCounts:table,assertions,failures:0,scope:'finite computational checks; symbolic theorem independent'},null,2));
