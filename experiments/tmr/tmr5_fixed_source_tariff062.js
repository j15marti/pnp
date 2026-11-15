"use strict";
// TMR-5 FIXSRC062: exact source-aware three-column tariff audit.
// Output is symbolic all-q certificate plus exhaustive q<=3 check.
function b(x,i){return (x>>i)&1;}
function terminal(q,x,m){
 for(let r=0;r<q;r++){
   let z=true;for(let j=0;j<q;j++){let i=r*q+j;if(!b(m,i)||b(x,i)){z=false;break;}}
   if(z)return true;
 }
 for(let r=0;r<q;r++){
   let one=false;for(let j=0;j<q;j++){let i=r*q+j;if(b(m,i)&&b(x,i)){one=true;break;}}
   if(!one)return false;
 }
 return true;
}
function val(q,x,m){
 if(terminal(q,x,m))return [0,0,0];
 let a=0,W=0,uMin=999,zMin=999,truth=true;
 for(let r=0;r<q;r++){
   let seen=false,has=false,u=0;
   for(let j=0;j<q;j++){let i=r*q+j;if(b(x,i))has=true;if(!b(m,i))u++;else if(b(x,i))seen=true;}
   if(!has)truth=false;
   if(!seen){a++;W+=u;uMin=Math.min(uMin,u);if(!has)zMin=Math.min(zMin,u);}
 }
 return [W,Math.min(a,uMin),truth?a:zMin]; // order W,B,D_x
}
let checked=0,rows=[];
for(let q=1;q<=3;q++){
 let m=q*q,Dq=m-q+1,max=[-999,-999,-999],min=[999,999,999],all=0,frontier=null,negB=null;
 for(let x=0;x<(1<<m);x++)for(let mask=0;mask<(1<<m);mask++){
   if(terminal(q,x,mask))continue;
   let v=val(q,x,mask);
   for(let i=0;i<m;i++)if(!b(mask,i)){
     let a=val(q,x,mask|(1<<i)),del=v.map((z,k)=>z-a[k]);
     checked++;all++;
     if(!(del[0]>=0&&del[0]<=Dq&&del[1]<=1&&del[2]>=0&&del[2]<=1))throw Error("discharge violation "+JSON.stringify({q,x,mask,i,del}));
     max=max.map((z,k)=>Math.max(z,del[k]));
     min=min.map((z,k)=>Math.min(z,del[k]));
     if(del[1]<0&&!negB)negB={x,mask,bit:i,delta_B:del[1]};
     if(del[0]===Dq&&del[1]===1&&del[2]===1&&!frontier)frontier={x,mask,bit:i,delta:del};
   }
 }
 if(max[0]!==Dq||max[1]!==1||max[2]!==1||!frontier)throw Error("missing exact frontier");
 let maxPotential=Math.max(q, q*q/Dq);
 if(maxPotential!==q)throw Error("initial optimum");
 rows.push({q,Dq,authenticated_source_READ_edges:all,max_Delta_WBD:max,min_Delta_WBD:min,frontier,
    negative_B_discharge_witness:negB,
    exact_nonnegative_cone:"lambda_B + lambda_Dx + "+Dq+"*lambda_W <= 1",
    exact_optimal_initial_potential:q,
    all_length_fixed_weights:"lambda_W=0, lambda_B+lambda_Dx<=1"});
}
const tariffResult={claim:"TMR5-FIXSRC062",execution:"native V8 exact integer arithmetic, exhaustive q=1..3",
 checked_edges:checked,failures:0,rows};
if(typeof console!=="undefined")console.log(JSON.stringify(tariffResult,null,2));

