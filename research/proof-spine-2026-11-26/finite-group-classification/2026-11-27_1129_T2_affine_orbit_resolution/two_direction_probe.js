function probe(F,B){
 // For each pair of coordinate directions compute exact number of affected events. Also rank of stacked normals.
 let best=Infinity,eligible=0,tested=0,checks=0,example=null;
 for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){tested++;let k=0;for(const E of F){checks++;if(E.some(r=>Boolean(r&B[i])!==Boolean(r&B[j])))k++}if(k<best){best=k;example=[B[i].toString(16),B[j].toString(16)]}if(k<=3)eligible++}
 return {tested,checks,minAffected:best,eligible,example}
}
module.exports={probe};
