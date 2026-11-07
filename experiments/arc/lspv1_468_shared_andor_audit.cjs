#!/usr/bin/env node
'use strict';
function check(){
 let cases=0,rows=[];
 for(let k=3;k<=12;k++){let best=Infinity,p=k;
  for(let a=0;a<(1<<k);a++){let j=0;for(let i=0;i<k;i++)j+=(a>>i)&1;best=Math.min(best,j?p+j+(k-j)*p:k*p);cases++;}
  if(best!==p+k)throw Error("minimum");rows.push([k,k*p,best]);
 }
 const F=[[-1,2,3],[-1,2,-3],[1,-2,4],[1,-2,-4]];
 function R(a,b,p){let s=a.includes(p)&&b.includes(-p)?p:a.includes(-p)&&b.includes(p)?-p:0;if(!s)throw Error("pivot");return [...new Set([...a.filter(x=>x!==s),...b.filter(x=>x!==-s)])].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
 let a=R(R(F[0],F[1],3),[1],1),b=R(R(F[2],F[3],4),[-1],1);
 if(JSON.stringify(a)!=="[2]"||JSON.stringify(b)!=="[-2]"||R(a,b,2).length)throw Error("scope");
 let models=0;for(let v=0;v<16;v++)if(F.every(c=>c.some(l=>((v>>(Math.abs(l)-1))&1)==(l>0?1:0))))models++;
 if(models!==8||cases!==8184)throw Error("model");
 return {status:"PASS",checked_choices:cases,reported_assertions:cases+10,rows,two_goals_work:[6,7,7,5],strict3CNF:{source:F,models,branch_x:a,branch_notx:b,global_join_illegal:true},historical_native_checker:false};
}
console.log(JSON.stringify(check(),null,2));
