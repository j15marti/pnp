function replay(){
 const pop=x=>{let n=0;while(x){n+=x&1;x>>=1}return n};
 const pair=p=>p*(p-1)/2;
 const core=[];
 for(const g of [0,3,6])core.push([[g,g+1,g+2],0]);
 for(let a=0;a<3;a++)for(let b=3;b<6;b++)for(let c=6;c<9;c++)core.push([[a,b,c],7]);
 function score(r){return core.reduce((s,[idx,h])=>s+pair(3-pop(idx.reduce((u,i,j)=>u|(((r>>i)&1)<<j),0)^h)),0)}
 let coreMin=Infinity,compatibleMin=Infinity,zero=0;
 for(let r=0;r<512;r++){let c=score(r);coreMin=Math.min(coreMin,c);if((r&1)!==((r>>1)&1)&&((r>>1)&1)===((r>>2)&1))compatibleMin=Math.min(compatibleMin,c);
 if(core.every(([ids,h])=>ids.some((i,j)=>((r>>i)&1)!==((h>>j)&1))))zero++}
 if(coreMin!==6||compatibleMin!==6||zero!==0)throw Error("core mismatch");
 let tests=0;
 for(let h=0;h<8;h++)for(let r=0;r<8;r++)for(let s=0;s<4;s++){
 let z=h;z^=(((s&1)* (h&1))<<1);z^=(((s>>1)*(h&1))<<2);z^=r;
 const u=(b)=>((r>>b)&1)^(((s>>(b-1))&1)*(h&1));
 const p=[(h&1)===(r&1),((h>>1)&1)===u(1),((h>>2)&1)===u(2)];
 if(pair(3-pop(z))!==pair(p.filter(Boolean).length))throw Error("meta mismatch");tests++}
 return {coreMin,compatibleMin,coreAttainedWords:zero,individualHoleChecks:tests,family:[1,4,16,32,64].map(s=>({s,fixedLowerBound:6+2*s,sharedShearOptimum:6}))}
}
console.log(JSON.stringify(replay(),null,2));
