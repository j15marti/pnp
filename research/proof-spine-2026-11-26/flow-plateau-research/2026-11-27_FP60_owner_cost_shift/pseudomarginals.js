function parityMeasure(F){
 const support=[],types={},parity=w=>{let b=0;while(w){b^=1;w&=w-1}return b};let rowChecks=0,checks=0,pairs=0;
 for(const f of F){let bad=f.cost.map((c,w)=>c? w:-1).filter(w=>w>=0),key=f.vs.length+":"+bad.length;types[key]=(types[key]||0)+1;if(f.vs.length<2||bad.length!==1)return {status:"NOT_APPLICABLE",types};let z=bad[0],S=f.cost.map((c,w)=>parity(w)!==parity(z)?w:-1).filter(w=>w>=0);for(let w of S){rowChecks++;if(f.cost[w]!==0)throw Error("positive support")};support.push(S)}
 for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){let a=F[i],b=F[j],I=a.vs.filter(v=>b.vs.includes(v));if(!I.length)continue;pairs++;let project=(f,S)=>{let P=Array(2**I.length).fill(0);for(let w of S){checks++;P[I.reduce((z,v,k)=>z|(((w>>f.vs.indexOf(v))&1)<<k),0)]++}return P};let A=project(a,support[i]),B=project(b,support[j]);if(A.some((z,k)=>z*support[j].length!==B[k]*support[i].length))return {status:"NOT_APPLICABLE",types,pair:[i,j],A,B}}
 return {status:"CERTIFIED",types,support,rowChecks,checks,pairs};
}
module.exports={parityMeasure};
