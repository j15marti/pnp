function hostileControls(){
 const cases=[];
 for(const [B,scale,K,t,tag] of [[3,2,[3,3],0,false],[2,1,[1,1],1,true]]){
 let feasible=0;for(let x=0;x<(1<<B);x++){let load=[0,0],p=0;for(let i=0;i<B;i++){let a=(x>>i)&1;load[a]+=scale;if(tag&&a===i)p^=1;}if(load.every((v,i)=>v<=K[i])&&p===t)feasible++;}
 const halfLoad=[B*scale/2,B*scale/2],halfTagSum=tag?B/2:0;
 if(feasible!==0||!halfLoad.every((v,i)=>v<=K[i])||halfTagSum!==t)throw Error("hostile control failed");
 cases.push({B,scale,K,target:t,tagVaries:tag,feasibleIntegerAssignments:feasible,halfLoad,halfTagSum,affordabilityPrepassDeletes:0,allOnesPriceGap:K[0]+K[1]-B*scale});
 }return cases;
}
console.log(JSON.stringify(hostileControls(),null,2));
