function refusal(F){
 let pairs=0,rows=0,nonzero=[],cert=[];
 for(let i=0;i<F.length;i++)for(let j=0;j<F.length;j++){if(i===j)continue;let a=F[i],I=a.vs.filter(v=>F[j].vs.includes(v));if(!I.length)continue;pairs++;let zero=Array(2**I.length).fill(-1);
 for(let w=0;w<a.cost.length;w++){rows++;if(a.cost[w]!==0)continue;let p=I.reduce((s,v,k)=>s|(((w>>a.vs.indexOf(v))&1)<<k),0);zero[p]=w}
 if(zero.includes(-1))nonzero.push([i,j,I,zero]);else cert.push([i,j,zero])}
 let checks=0;for(let [i,j,Z] of cert){let a=F[i],I=a.vs.filter(v=>F[j].vs.includes(v));for(let k=0;k<Z.length;k++){let w=Z[k];checks++;if(a.cost[w]||I.some((v,t)=>((w>>a.vs.indexOf(v))&1)!==((k>>t)&1)))throw Error("bad projection cert")}}
 return {pairs,rows,nonzero,cert,checks,allZero:!nonzero.length};
}
function rup(C,P){
 let scans=0,reads=0,ok=0;
 for(const q of P){let A=new Map(),dead=false;for(let l of q){let v=Math.abs(l),b=Number(l<0);if(A.has(v)&&A.get(v)!==b)dead=true;A.set(v,b)}while(!dead){let change=false;for(let c of C){scans++;let u=[],sat=false;for(let l of c){reads++;let v=Math.abs(l);if(!A.has(v))u.push(l);else if(A.get(v)===Number(l>0)){sat=true;break}}if(sat)continue;if(!u.length){dead=true;break}if(u.length===1){A.set(Math.abs(u[0]),Number(u[0]>0));change=true}}if(!change)break}if(!dead)return {status:"REFUSED",ok,failed:q,scans,reads};C.push(q);ok++}
 return {status:P.at(-1).length===0?"UNSAT":"PARTIAL",ok,scans,reads};
}
module.exports={refusal,rup};
