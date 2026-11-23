"use strict";
const main = function(){
const A=(p,m="assert")=>{if(!p)throw Error(m)}, b=i=>1n<<BigInt(i);
function rank(rows){let B={};for(let v of rows)while(v){let k=v.toString(2).length;if(B[k])v^=B[k];else{B[k]=v;break}}return Object.keys(B).length}
function par(v){let x=0;while(v){v&=v-1n;x^=1}return x}
const good=(f,x)=>f.rows.some((v,j)=>par(v&x)!==f.rhs[j]),valid=(F,x)=>F.every(f=>good(f,x));
let F=[];for(let i=1;i<=7;i++)for(let j=i+1;j<=7;j++){let k=i^j;if(k>j)F.push({rows:[b(i-1)^b(j-1),b(i-1)^b(k-1)],rhs:[0,0],line:[i,j,k]})}
const R=rank(F.flatMap(f=>f.rows));A(R===6);
let signFlips=0,gauge=0,pairChecks=0,cuts=0,oddCore=0;
for(let i=0;i<7;i++)for(let j=0;j<2;j++){let G=F.map((f,k)=>({...f,rhs:f.rhs.map((x,z)=>x^((i===k&&j===z)?1:0))}));let witness=F[i].line.reduce((x,v)=>x^b(v-1),0n);A(valid(G,witness));let rows=G.flatMap(f=>f.rows),rhs=G.flatMap(f=>f.rhs);A(rank(rows.map((v,k)=>v^(rhs[k]?b(7):0n)))===R+1);signFlips++}
for(let x=0n;x<128n;x++){let G=F.map(f=>({...f,rhs:f.rows.map(v=>par(v&x))}));for(let y=0n;y<128n;y++)A(!valid(G,y));gauge++}
for(let t=3;t<=8;t++)for(let k=0;k<=3;k++)for(let e=0;e<=1;e++){
 let H=[b(0)^b(1),b(0)^b(3),b(0)^b(4)].slice(0,k),O=Array.from({length:t},(_,i)=>({rows:[b(7+i),b(7+(i+1)%t),...H],rhs:Array(k+2).fill(0)}));
 let r=rank(F.concat(O).flatMap(f=>f.rows)),ro=rank(O.flatMap(f=>f.rows));A(r===6+t&&ro===t+k&&R+ro-r===k);A((7+t+e-r)===1+e);
 // Removing an outside factor never removes a row-space direction because cycle shares both endpoints.
 A(O.every((_,i)=>rank(F.concat(O.filter((_,j)=>i!==j)).flatMap(f=>f.rows))===r));
 // For k<=2 the shared H contains no entire Fano line rowspace.
 if(k<=2){
 let G=F.concat(O);for(let i=0;i<G.length;i++)for(let j=i+1;j<G.length;j++){
 const a=G[i].rows,c=G[j].rows,ri=rank(a),rj=rank(c),u=rank(a.concat(c));
 // Both forbidden spaces contain zero; non-contained union cannot be affine.
 A(u>ri&&u>rj);pairChecks++;
 }}
 cuts++;
}
// Odd core-rank control: 8 distinct forbidden singleton assignments on 3 bits.
// Each proper subset has smaller deficiency; all eight cover, single deletion SAT.
let C=Array.from({length:8},(_,i)=>({rows:[1n,2n,4n],rhs:[i&1,(i>>1)&1,(i>>2)&1]}));
for(let mask=0;mask<256;mask++){let S=C.filter((_,i)=>(mask>>i)&1);let d=S.length-rank(S.flatMap(f=>f.rows));A(d<=5&&(d===5)===(mask===255));let count=0;for(let x=0n;x<8n;x++)if(valid(S,x))count++;A(count===8-S.length);oddCore++}
return {signFlips,gaugeRoots:gauge,gaugeAssignments:gauge*128,separatorControls:cuts,nonmergeablePairs:pairChecks,oddCoreSubsetChecks:oddCore};
};
console.log(JSON.stringify(main(),null,2));
