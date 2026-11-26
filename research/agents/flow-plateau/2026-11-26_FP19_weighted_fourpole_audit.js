'use strict';
function weightedAudit(){
 const E=[[2,3],[2,7],[3,4],[3,8],[4,9],[5,7],[5,8],[6,8],[6,9],[7,9]],P=[4,5,2,6],used=Array(10).fill(0),word=[],T=[];
 const bit=(c,d)=>d===0?c&1:d===1?(c>>1)&1:(c^(c>>1))&1;
 function visit(k){
  if(k===E.length){const B=P.map(v=>[1,2,3].find(c=>!(used[v]&(1<<c))));if(B[0]!==B[1]||B[2]!==B[3])throw Error("relation");T.push({B,W:[...word]});return;}
  const [u,v]=E[k];for(let c=1;c<=3;c++){let m=1<<c;if((used[u]|used[v])&m)continue;used[u]^=m;used[v]^=m;word.push(c);visit(k+1);word.pop();used[u]^=m;used[v]^=m;}
 }
 visit(0);const groups=new Map();
 for(const t of T){const k=t.B.join(",");if(!groups.has(k))groups.set(k,[]);groups.get(k).push(t);}
 let checks=0,counts={};
 for(const s of T)for(let d=0;d<3;d++){
  let a=Number(!bit(s.B[0],d)),b=Number(!bit(s.B[2],d));
  counts[`${a}${b}`]=(counts[`${a}${b}`]||0)+1;
  for(const ts of groups.values()){
   const u=Number(!(ts[0].B[0]&1)),v=Number(!(ts[0].B[2]&1));
   const exact=Math.min(...ts.map(t=>t.W.reduce((r,c,k)=>r+Number(!bit(s.W[k],d)&&!(c&1)),0)));
   const predicted=a&&b?u+v:a||b?u*v:0;
   if(exact!==predicted)throw Error(JSON.stringify({a,b,u,v,exact,predicted}));
   checks++;
  }
 }
 return {initialWords:T.length,boundaryFibers:groups.size,initialDirectionTypes:counts,checks};
}
console.log(JSON.stringify(weightedAudit(),null,2));
