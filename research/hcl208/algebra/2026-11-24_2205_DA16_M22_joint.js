const run=function(){
const n=9,N=1<<n,bit=i=>1n<<BigInt(i),pop=x=>{let k=0;while(x){x&=x-1;k++}return k},top=x=>x.toString(2).length-1;
const contains=Array(n).fill(0n);for(let m=0;m<N;m++)for(let j=0;j<n;j++)if(m&(1<<j))contains[j]|=bit(m);
const mul=(p,q)=>{let r=0n;for(let a=0;a<N;a++)if(p&bit(a))for(let b=0;b<N;b++)if(q&bit(b))r^=bit(a|b);return r};
const pol=([a,b,c])=>mul(1n^bit(1<<a)^bit(1<<b),1n^bit(1<<a)^bit(1<<c));
const val=(p,x)=>{let z=0;for(let m=x;;m=(m-1)&x){if(p&bit(m))z^=1;if(!m)return z}};
const partitions=[Array.from({length:3},(_,j)=>[3*j,3*j+1,3*j+2])];
for(let a=0;a<3;a++)partitions.push(Array.from({length:3},(_,b)=>[0,1,2].map(x=>3*x+(a*x+b)%3)));
const pairings=[[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]];
let products=0,ins=0,checks=0,scans=0;
function check(b){checks++;if(!b)throw Error("assertion")}
function satps(P,D,pin){
 let cap=0n;for(let m=0;m<N;m++)if(pop(m)<=D)cap|=bit(m);
 let B=Array(N).fill(0n),change=false;
 function add(p){while(p){let k=top(p);if(B[k])p^=B[k];else{B[k]=p;change=true;ins++;return}}}
 for(let p of P)add(p);if(pin!==null)add(bit(1)^BigInt(pin));
 if(B[0])return true;
 do{change=false;for(let j=0;j<n;j++){
 const H=Array(N).fill(0n);
 for(let p of B.filter(Boolean)){
  products++;let q=(p&contains[j])^((p&~contains[j])<<BigInt(1<<j));
  while(q&~cap){let k=top(q&~cap);if(H[k])q^=H[k];else{H[k]=q;break}}
  if(!(q&~cap))add(q);if(B[0])return true;
 }
 }}while(change);return false
}
function hull(words){if(!words.length)return [];let a=[0],s=new Set(a);for(let x of words){let d=x^words[0];if(!s.has(d)){a.push(...a.map(y=>y^d));s=new Set(a)}}return a.map(x=>x^words[0])}
function closure(P,pin){let A=Array.from({length:N},(_,x)=>x).filter(x=>pin===null||(x&1)===pin);
const models=A.filter(x=>P.every(p=>!val(p,x)));
while(A.length){scans++;let changed=false;for(let p of P){let h=hull(A.filter(x=>!val(p,x)));let s=new Set(h);let next=A.filter(x=>s.has(x));if(next.length<A.length){A=next;changed=true;break}}if(!changed)break}
check(models.every(x=>A.includes(x)));return {ambient:A.length,models:models.length,affineHull:hull(models).length};
}
let rows=[];
for(let pair of pairings)for(let pin of [null,0,1]){
 const side=pair.map(S=>S.flatMap(i=>partitions[i]).map(pol));let rs=side.map(P=>{const c=closure(P,pin);check(c.models>0);check(c.affineHull===(pin===null?512:256));let d2=satps(P,2,pin),d3=satps(P,3,pin);check(!d2&&!d3);return {...c,d2,d3}});
 const joint=side.flat();const c=closure(joint,pin);let d2=satps(joint,2,pin),d3=satps(joint,3,pin);check(c.models===0&&d3);
 rows.push({pair,pin,side:rs,joint:{...c,d2,d3}});
}
return {rows,ledger:{checks,scans,products,ins}};
};
console.log(JSON.stringify(run(),null,2));
