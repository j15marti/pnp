"use strict";
function controls(){
 const I=[0,1,2],T=[0,2,1];let stats={cases:0,assignments:0,rankZeroRoots:0,contradictoryDependencies:0,parityProfiles:new Set()};
 function sat(f,p){let a=[];function dfs(i){if(i===f.length)return a[0]!==p[a[i-1]];for(let c=0;c<3;c++)if(c!==f[i]&&(i===0||c!==a[i-1])){a[i]=c;if(dfs(i+1))return true}return false}return dfs(0)}
 for(let d=1;d<=6;d++)for(let k=0;k<=d;k++)for(let odd=0;odd<=1;odd++)for(let charge=0;charge<=1;charge++){
   // constant-zero spoke ensures common excluded color is 0; repeated first form
   // with charge 1 makes the candidate forbidden equations inconsistent.
   let r=k+3;while(r%2!==odd)r++;
   let obs=[-1,...Array.from({length:k},(_,i)=>i),k?0:-1];while(obs.length<r)obs.push(-1);
   let neg=obs.map((_,i)=>i===k+1?charge:0),bad=0;
   for(let u=0;u<1<<d;u++){
     const f=obs.map((j,i)=>(j<0?0:(u>>j&1))^neg[i]);
     const expected=charge===0&&(u&((1<<k)-1))===0;
     if(!sat(f,odd?I:T)!==expected)throw Error("parity control");
     bad+=+expected;stats.assignments++;
   }
   if(bad!==(charge?0:2**(d-k)))throw Error("rank count");
   stats.cases++;stats.rankZeroRoots+=+(k===0&&!charge);stats.contradictoryDependencies+=+charge;
   stats.parityProfiles.add([d%2,k%2,(d-k)%2,odd,charge].join(":"))
 }
 return {...stats,parityProfiles:[...stats.parityProfiles].sort()};
}
console.log(JSON.stringify(controls(),null,2));
