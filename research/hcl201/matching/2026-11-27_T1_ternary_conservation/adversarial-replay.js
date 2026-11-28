module.exports=function verify(fano,stall,sha){
let M=x=>(x%3+3)%3,checks=0;function req(x){checks++;if(!x)throw Error("check "+checks)}
let A=fano.groups,C=fano.dimacs.trimEnd().split("\n").slice(1).map(l=>l.split(" ").map(Number).slice(0,-1));req(C.length===4*A.length);for(let i=0;i<A.length;i++){let v=A[i],block=C.slice(4*i,4*i+4);for(let k=0;k<8;k++){let b=new Map(v.map((x,j)=>[x,+(Boolean(k>>j&1))]));req(block.every(c=>c.some(l=>b.get(Math.abs(l))===+(l>0)))===(v.reduce((s,x)=>s+b.get(x),0)===1))}}
for(let v=1;v<=7;v++)req(A.filter(c=>c.includes(v)).length===3);req(A.length%3===1);
function fcheck(a){let C=a.dimacs.trimEnd().split("\n").slice(1).map(l=>l.split(" ").map(Number).slice(0,-1)),sat=[],parity=[];for(let x=0;x<128;x++){if(C.every(c=>c.some(l=>+(l>0)===(x>>(Math.abs(l)-1)&1))))sat.push(x);if(a.groups.every(c=>c.reduce((s,v)=>s+(x>>(v-1)&1),0)%2===1))parity.push(x)}req(JSON.stringify(sat)===JSON.stringify(a.exactSolutions));req(JSON.stringify(parity)===JSON.stringify(a.paritySolutions));req(a.instance_id.endsWith(sha(a.dimacs)));return{sat,parity}}
let low=[];for(let a of [stall,stall.control]){let x=a.input,d=x.d,n=x.directions.length,sat=0,words=0,pairSupports=Array.from({length:n},()=>Array(n).fill(0)),triples=0;
function dot(a,z){return M(a.reduce((s,c,i)=>s+c*z[i],0))}
function rec(z){if(z.length<d){for(let v=0;v<3;v++)rec([...z,v]);return}words++;let y=x.directions.map((a,i)=>M(dot(a,z)+x.offsets[i]));if(y.every(v=>v!==2))sat++;for(let i=0;i<n;i++)for(let j=0;j<i;j++)pairSupports[i][j]|=1<<(y[i]*3+y[j])}
rec([]);
for(let i=0;i<n;i++)for(let j=0;j<i;j++){req(pairSupports[i][j]===511);for(let k=0;k<j;k++){triples++;let directions=[x.directions[i],x.directions[j],x.directions[k]];for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++)if(a||b||c)req(directions[0].some((v,t)=>M(a*v+b*directions[1][t]+c*directions[2][t])!==0))}}
req(a.instance_id.endsWith(sha(JSON.stringify(x)+"\n")));req(sat===(a.result?.count??a.count));low.push({sat,words,triples,pairs:n*(n-1)/2})}
return{fano:fcheck(fano),fanoNeighbor:fcheck(fano.control),low,checks}
}
