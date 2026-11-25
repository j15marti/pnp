function test(){
 let checks=0,out=[];
 function assert(x,m){checks++;if(!x)throw Error(m)}
 function count(k,pinA,pinB){let sum=0n,steps=0,rank=k-1+Number(pinA!==null)+Number(pinB!==null); // pins can be redundant; orthogonality holds without independence
 for(let a of pinA===null?[0]:[0,1])for(let b of pinB===null?[0]:[0,1]){
 let D=[a===0?1n:0n,a===1?1n:0n];
 for(let i=0;i<k;i++){let next=[0n,0n],end=i===k-1;for(let x=0;x<2;x++)for(let y of end?[b]:[0,1]){next[y]+=D[x]*(x===y?4n:2n);steps++}D=next}
 sum+=D[b]*((pinA!==null&&a*pinA)^(pinB!==null&&b*pinB)?-1n:1n)}
 assert(sum>=0n&&sum%(1n<<BigInt(rank))===0n,"exact dual division");return{count:sum>>BigInt(rank),steps,dualBits:rank}}
 for(let k of [2,3,4,5,6,16,32,64,128,256])for(let a of [null,0,1])for(let b of [null,0,1]){
 let {count:z,steps,dualBits}=count(k,a,b);let expected=(a!==1&&b!==1?3n**BigInt(k):0n)+(a!==0&&b!==0?1n:0n);assert(z===expected,"closed form");
 if(k<=6){let brute=0n;for(let w=0;w<2**(2*k);w++){let p=[];for(let j=0;j<k;j++)p.push(Number(((w>>(2*j))&3)===3));if(p.every(x=>x===p[0])&&(a===null||a===p[0])&&(b===null||b===p[k-1]))brute++}assert(z===brute,"brute")}
 out.push({k,pinA:a,pinB:b,count:z.toString(),steps,dualBits})}
 return{checks,jobs:out.length,results:out}
}
console.log(JSON.stringify(test(),null,2));
