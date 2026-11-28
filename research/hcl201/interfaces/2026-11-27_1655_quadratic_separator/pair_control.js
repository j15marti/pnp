function pairControl(){
 const clauses=[];for(let a=1;a<=6;a++)for(let b=a+1;b<=6;b++)for(let c=b+1;c<=6;c++)for(let z=0;z<8;z++)clauses.push([a,b,c].map((v,i)=>(z>>i&1)?-v:v));
 let pairCount=0,checks=0,implied=0,distinctSupport=0;
 const sat=(c,w)=>c.some(l=>((w>>(Math.abs(l)-1))&1)===+(l>0));
 for(let i=0;i<clauses.length;i++)for(let j=i+1;j<clauses.length;j++){const a=clauses[i],b=clauses[j],vs=[...new Set([...a,...b].map(Math.abs))];pairCount++;let models=[];for(let w=0;w<64;w++)if(sat(a,w)&&sat(b,w))models.push(w);let same=a.map(Math.abs).join(",")===b.map(Math.abs).join(","),h=a.filter((l,k)=>l===-b[k]).length;if(!same)distinctSupport++;
  for(let u=0;u<vs.length;u++)for(let v=u+1;v<vs.length;v++)for(let z=0;z<4;z++){checks++;let excluded=!models.some(w=>((w>>(vs[u]-1))&1)===(z&1)&&((w>>(vs[v]-1))&1)===(z>>1));if(excluded){implied++;if(!same||h!==1)throw Error("lemma fail")}}
 }
 return {pairCount,checks,implied,distinctSupport};
}
module.exports=pairControl;
