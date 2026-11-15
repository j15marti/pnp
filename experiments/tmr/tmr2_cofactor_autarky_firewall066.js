'use strict';
function main(){
 let checks=0;
 function ok(v,m){checks++;if(!v)throw Error(m);}
 function construct(k){
   const X=i=>i+1,Y=i=>k+i+1,Z=i=>2*k+i+1;
   const clauses=[];
   for(let i=0;i<k;i++){
     clauses.push([-X(i),Y(i),Z(i)]);
     clauses.push([-X(i),Y(i),-Z(i)]);
     clauses.push([X(i),Z(i),-Y(i)]);
   }
   for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)
     clauses.push([Z(0),-Y(i),-Y(j)]);
   return {k,X,Y,Z,clauses};
 }
 function sat(F,a){
   return F.clauses.every(cl=>cl.some(t=>t>0?a[t-1]===1:a[-t-1]===0));
 }
 function state(F,{x=[],y=[],z=[]}={}){
   let a=Array(3*F.k).fill(0);
   for(let i=0;i<F.k;i++){a[F.X(i)-1]=x[i]||0;a[F.Y(i)-1]=y[i]||0;a[F.Z(i)-1]=z.length?z[i]:1;}
   return a;
 }
 function countLen(F){
   let k=F.k,m=F.clauses.length;
   let b=Math.ceil(Math.log2(3*k+1)),h=Math.ceil(Math.log2(m+1));
   return 2*b+2*h+2+3*m*(b+1);
 }
 function combine(op,arrays){return arrays[0].map((_,i)=>op(arrays.map(a=>a[i])));}
 let records=[];
 for(let k of [3,4,5,6,7,8,10,12,16,20,30]){
   let F=construct(k),n=3*k,m=F.clauses.length;
   ok(m===3*k+k*(k-1)/2,'m '+k);
   const pos=Array(n).fill(0),neg=Array(n).fill(0);
   for(const cl of F.clauses){
     ok(cl.length===3,'arity '+k);
     ok(new Set(cl.map(Math.abs)).size===3,'distinct '+k);
     ok(cl.some(t=>t>0),'positive '+k);
     for(const t of cl){(t>0?pos:neg)[Math.abs(t)-1]++;}
   }
   for(let u=0;u<n;u++){ok(pos[u]>0&&neg[u]>0,'no pure '+k+' '+u);}
   for(let i=0;i<k;i++)for(let j=i+1;j<k;j++){
     ok(F.clauses.some(cl=>cl.includes(-F.Y(i))&&cl.includes(-F.Y(j))),'clique '+k);
   }
   let ones=Array(n).fill(1);
   ok(sat(F,ones),'all ones '+k);
   let partial=Array(n).fill(null);
   for(let i=0;i<k;i++){partial[F.Y(i)-1]=1;partial[F.Z(i)-1]=1;}
   ok(F.clauses.every(cl=>cl.some(t=>partial[Math.abs(t)-1]!==null&&(t>0?partial[t-1]===1:partial[-t-1]===0))),'autarky '+k);
   if(k<=10){
     let seen=new Set();
     for(let xmask=0;xmask<2**k;xmask++){
       let xa=Array.from({length:k},(_,i)=>(xmask>>i)&1);
       let signature='';
       for(let j=0;j<k;j++){
         let y=Array(k).fill(1);y[j]=0;
         let val=sat(F,state(F,{x:xa,y,z:Array(k).fill(1)}))?1:0;
         ok(val===1-xa[j],'cofactor '+k+' '+xmask+' '+j);
         signature+=val;
       }
       ok(!seen.has(signature),'distinct '+k);
       seen.add(signature);
     }
     ok(seen.size===2**k,'count '+k);
   }
   const zzero=[0,...Array(k-1).fill(1)];
   const yz=(ys,zs,xs=Array(k).fill(0))=>state(F,{x:xs,y:ys,z:zs});
   const y2=Array(k).fill(0);y2[1]=1;
   const y3=Array(k).fill(0);y3[2]=1;
   const y23=Array(k).fill(0);y23[1]=y23[2]=1;
   const A=yz(y2,zzero),B=yz(y3,zzero),C=yz(y23,Array(k).fill(1));
   const zero=yz(Array(k).fill(0),zzero);
   for(let [label,t] of [['A',A],['B',B],['C',C],['zero',zero]])ok(sat(F,t),label+' witness k='+k);
   let OR=combine(v=>Number(v.some(Boolean)),[A,B]);
   let MAJ=combine(v=>Number(v.reduce((a,b)=>a+b,0)>=2),[A,B,C]);
   let XOR=combine(v=>v.reduce((a,b)=>a^b,0),[A,B,zero]);
   for(let [label,t] of [['OR',OR],['MAJ',MAJ],['XOR',XOR]])ok(!sat(F,t),label+' violation k='+k);
   let yh=Array(k).fill(0);yh[0]=1;
   let xh=Array(k).fill(0);xh[0]=1;
   let HA=yz(yh,zzero,xh),HB=yz(yh,Array(k).fill(1));
   let AND=combine(v=>Number(v.every(Boolean)),[HA,HB]);
   ok(sat(F,HA)&&sat(F,HB)&&!sat(F,AND),'AND violation '+k);
   if(k<=4){
     let tally=0;
     for(let bits=0;bits<2**n;bits++){
       let q=Array.from({length:n},(_,i)=>(bits>>i)&1);
       if(sat(F,q))tally++;
     }
     ok(tally>0,'exhaust '+k);
   }
   records.push({k,variables:n,clauses:m,encoded_bits:countLen(F),cofactor_count:k<=10?2**k:'symbolic 2^k',primal_treewidth_lower_bound:k-1,all_one_sat:true,autarky_size:2*k,nonhorn_and_violation:true,nondualhorn_or_violation:true,nonbijunctive_majority_violation:true,nonaffine_xor_violation:true});
 }
 return {schema:'TMR2_COFSEP066',status:'finite/computational; algebraic all-k theorem separately proved',checks,failures:0,records};
}
console.log(JSON.stringify(main(),null,2));
