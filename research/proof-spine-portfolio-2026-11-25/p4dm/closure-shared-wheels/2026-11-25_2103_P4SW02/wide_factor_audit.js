/* P4SW02 independent exact arithmetic audit. Node.js 18+. Planarity follows from disk two-edge splice; separate Python audit used NetworkX. */
function audit(){
 const Q=[];for(let i=0;i<16;i++){let t=[3,2,1,0].map(k=>(i>>k)&1);if(t.reduce((a,b)=>a+b,0)===2)Q.push(t)}
 function chain(k){let t=[];for(let i=0;i<k;i++)for(const q of Q)t.push(q.map(x=>x+2*i));for(let i=0;i<k-1;i++){let c=i%2,a=6*i,b=6*(i+1),z=t[a][c];t[a][c]=t[b][c];t[b][c]=z}return t}
 function rank(xs){let B=new Map();for(let x of xs){while(x){let k=x.toString(2).length-1;if(B.has(k))x^=B.get(k);else{B.set(k,x);break}}}return B.size}
 function check(T,S){let n=T.length/3,R=Array(4*n).fill(0);for(let j of S)T[j].forEach((v,c)=>R[c*n+v]++);if(R.some(x=>x!==1))throw Error("invalid source witness")}
 let data=[];
 for(let k of [2,4,8,16,32,64,128]){
  let T=chain(k),n=T.length/3,C=T.map(t=>t.reduce((s,v,c)=>s^(1n<<BigInt(c*n+v)),0n));
  let X=0n,A=[],B=[];for(let i=0;i<k;i++){X^=C[6*i]^C[6*i+5];A.push(C[6*i+1]^C[6*i+4]);B.push(C[6*i+2]^C[6*i+3])}
  let w=rank(A)+rank([X,...B])-rank([X,...A,...B]);if(w!==k)throw Error("rank");
  if(new Set(T.map(t=>t.join(','))).size!==T.length)throw Error("duplicate");
  for(let c=0;c<4;c++){let d=Array(n).fill(0);for(let t of T)d[t[c]]++;if(d.some(x=>x!==3))throw Error("degree")}
  let checks=0;let masks=k<=8?1<<k:32;
  for(let m=0;m<masks;m++){let S=[];for(let i=0;i<k;i++){let b=k<=8?(m>>i)&1:((i*37+m*11+i*m)%17)&1;S.push(6*i+(b?1:2),6*i+(b?4:3))}check(T,S);checks++}
  check(T,Array.from({length:k},(_,i)=>[6*i,6*i+5]).flat());checks++;
  data.push({k,tuples:T.length,rank:w,flat_states:(1n<<BigInt(w)).toString(),factor_count:k,witness_checks:checks})
 }
 return data
}
console.log(JSON.stringify(audit(),null,2));
