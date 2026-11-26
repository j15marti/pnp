// NAE4A9 degree-d pivot projection and prime CNF audit. node-compatible.
let checks=0;function ok(x){checks++;if(!x)throw Error("assertion "+checks)}
function bit(w,i){return (w>>i)&1}
function good(a){return a.some(x=>x!==a[0])}
let results=[];
for(let d=2;d<=4;d++){
 let n=2*d, prime=[];for(let i=0;i<d;i++)for(let j=i+1;j<d;j++)for(let c=0;c<2;c++)prime.push({mask:(3<<(2*i))|(3<<(2*j)),value:(c?3<<(2*i):3<<(2*j))});
 let full=1<<n,sat=0,unsat=0,privateWitness=Array(prime.length).fill(0);
 for(let w=0;w<full;w++){let original=[0,1].some(x=>Array.from({length:d},(_,i)=>good([bit(w,2*i),bit(w,2*i+1),x])).every(Boolean));let violated=prime.map((p,i)=>(w&p.mask)===p.value?i:-1).filter(i=>i>=0);ok(original===(violated.length===0));if(original)sat++;else unsat++;if(violated.length===1)privateWitness[violated[0]]++}
 ok(privateWitness.every(x=>x>0));
 let partial=0,nonextend=0,minimal=0;
 for(let t=0;t<3**n;t++){let u=t,mask=0,value=0;for(let i=0;i<n;i++){let a=u%3;u=(u-a)/3;if(a){mask|=1<<i;if(a===2)value|=1<<i}}let extend=false;for(let w=0;w<full;w++)if((w&mask)===value&&!prime.some(p=>(w&p.mask)===p.value)){extend=true;break}let hit=prime.some(p=>(mask&p.mask)===p.mask&&(value&p.mask)===p.value);ok(extend!==hit);partial++;if(!extend){nonextend++;if(prime.some(p=>mask===p.mask&&value===p.value))minimal++}}
 ok(minimal===prime.length);results.push({d,n,sat,unsat,partial,nonextend,minimal,privateWitness});
}
console.log(JSON.stringify({checks,results}));