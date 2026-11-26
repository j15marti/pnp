function main(){
const CT=`a2 d6 k1,a4 d4 k4|a2 d3 k1,a4 d5 k4|a2 d3 k2,a3 d6 k1|a2 d2 k2,a3 d3 k1
a5 d5 k3,a6 b1 f|a5 d4 k3,a6 b2 f|a4 b2 f,a5 d5 k4|a4 b1 f,a5 d4 k4
b2 d3 e2,e1 h k2|d2 e1 g2,e2 h k2|d4 e1 g2,e2 h k3|b2 d5 e2,e1 h k3
a1 p2 z2,a3 p4 z1|a3 p2 z1,a7 p4 z4|a6 p3 z4,a7 p4 z5|a1 p1 z2,a6 p4 z4
a7 p3 z4,a8 p1 z6|a8 p1 z2,g1 p3 z3|a8 p2 z2,g1 p1 z3|a7 p3 z3,a8 p2 z1
z3 z5 o1,z7 z8 o2|z5 z8 o1,z6 z7 o2|z1 z6 o2,z7 z8 o1|z5 z8 o2,z6 z7 o1
d1 q2 z10,d2 q4 z9|d6 q3 z12,d7 q4 z13|d2 q2 z9,d7 q4 z12|d1 q1 z10,d6 q4 z12
d7 q3 z12,d8 q1 z14|d8 q2 z10,g3 q1 z11|d8 q1 z10,g3 q3 z11|d7 q3 z11,d8 q2 z9
z11 z13 o3,z15 z16 o4|z9 z14 o4,z15 z16 o3|z13 z16 o3,z14 z15 o4|z13 z16 o4,z14 z15 o3`;
const XT=`i1 b2 z2,i2 b5 z3|i5 b5 z6,i7 b2 z4|i5 b5 z3,i7 b2 z5|i1 b2 z4,i2 b5 z7
i5 b4 z6,i6 b3 z5|i8 b3 z1,i9 b1 z5|i8 b3 z8,i9 b1 z4|i5 b4 z3,i6 b3 z1
i7 b1 z4,i8 b6 z1|l1 b4 z3,l2 b6 z7|l1 b4 z2,l2 b6 z1|i7 b1 z5,i8 b6 z8
z7 z8 o1|z2 z8 o1|z6 z7 o1|z2 z6 o1
i9 b8 z10,i11 b9 z12|i6 b9 z11,i11 b10 z12|i6 b7 z11,i10 b9 z12|i9 b7 z10,i10 b10 z12
i12 b7 z14,i14 b10 z9|i12 b7 z10,i14 b8 z9|i11 b10 z13,i12 b8 z10|i11 b9 z11,i12 b8 z9
z11 z13 o2,z15 z16 o3|z13 z16 o2,z14 z15 o3|z9 z14 o3,z15 z16 o2|z13 z16 o3,z14 z15 o2
i10 b14 z17,i13 b12 z18|i10 b12 z17,i15 b14 z20|i14 b13 z20,i15 b14 z21|i13 b11 z18,i14 b14 z20
i15 b13 z20,i16 b11 z22|i16 b11 z18,i17 b13 z19|i16 b12 z18,i17 b11 z19|i15 b13 z19,i16 b12 z17
z19 z21 o4,z23 z24 o5|z21 z24 o4,z22 z23 o5|z17 z22 o5,z23 z24 o4|z21 z24 o5,z22 z23 o4
i3 b19 z27,i4 b17 z29|i13 b18 z27,i18 b19 z30|i13 b18 z26,i18 b19 z27|i3 b19 z31,i4 b17 z25
i17 b16 z26,i18 b18 z30|i19 b16 z28,i20 b17 z25|i19 b16 z29,i20 b17 z32|i17 b16 z28,i18 b18 z27
i19 b15 z28,i20 b20 z25|l3 b20 z31,l4 b15 z29|l3 b20 z25,l4 b15 z28|i19 b15 z29,i20 b20 z32
z31 z32 o6|z26 z32 o6|z30 z31 o6|z26 z30 o6`;
const UP='r s A,r t E,s t F,A B C,A B E,A C F,B C D,B D E,C D F,D E F';
const parse=s=>s.split('\n').flatMap(line=>line.split('|').flatMap((cell,c)=>cell.split(',').map(r=>[c,r.split(' ')])));
const ck=(x,msg)=>{if(!x)throw Error(msg)};
const data=[['3to4',parse(UP),['r','s','t'],['001','010','100']],['C',parse(CT),['a1','g1','b1','g2','d1','g3'],['000011','001100','110000']],['X',parse(XT),['i1','l1','i2','l2','i3','l3','i4','l4'],['11111111','10011111','11111001','10011001','01100110','00000110','01100000','00000000']]];
return data.map(([name,raw,P,expected])=>{
const V=[...new Set(raw.flatMap(r=>r[1]))].sort(),n=V.length,m=raw.length,ix=new Map(V.map((v,i)=>[v,i])),R=raw.map(r=>r[1].map(v=>ix.get(v))),A=Array.from({length:n+m},()=>[]),ports=P.map(v=>ix.get(v)),portSet=new Set(ports);
R.forEach((r,j)=>{ck(new Set(r).size===3,'row arity');r.forEach(i=>{A[i].push(n+j);A[n+j].push(i)})});
ck(new Set(R.map(r=>r.slice().sort((a,b)=>a-b).join(','))).size===m,'distinct local rows');
const fullSigs=[];
for(let i=0;i<n;i++){
 const p=ports.indexOf(i),d=p<0?4:2;
 ck(A[i].length===d,'degree');
 if(d===4)fullSigs.push(A[i].join(','));
 if(name!=='3to4'){
 const want=p<0?'0,1,2,3':p%2===0?'0,3':'1,2';
 ck(A[i].map(j=>raw[j-n][0]).sort().join(',')===want,'partition');
 }
}
ck(fullSigs.length===new Set(fullSigs).size,'duplicate full tuple');
let checks=0,disconnected=0;
function deleted(u,v){
 const seen=new Uint8Array(n+m);if(u>=0)seen[u]=1;if(v>=0)seen[v]=1;
 let comps=0;
 for(let i=0;i<n+m;i++)if(!seen[i]){
  comps++;let hit=false,q=[i];seen[i]=1;
  for(let j=0;j<q.length;j++){const a=q[j];hit=hit||portSet.has(a);for(const b of A[a])if(!seen[b]){seen[b]=1;q.push(b)}}
  ck(hit,'component without live port');
 }
 if(v<0)ck(comps===1,'not two connected');
 if(comps>1)disconnected++;checks++;
}
deleted(-1,-1);
for(let u=0;u<n+m;u++){deleted(u,-1);for(let v=u+1;v<n+m;v++)deleted(u,v)}
const solutions=[];let calls=0;
function solve(p){
 calls++;p=p.slice();
 for(;;){let change=false;
  for(const r of R){const one=r.filter(i=>p[i]===1).length,free=r.filter(i=>p[i]===-1);
   if(one>1||(!one&&!free.length))return;
   if(one){for(const i of free){p[i]=0;change=true}}
   else if(free.length===1){p[free[0]]=1;change=true}
  }
  if(!change)break;
 }
 const i=p.indexOf(-1);
 if(i<0){solutions.push(p);return}
 for(const b of [0,1]){p[i]=b;solve(p)}
}
solve(Array(n).fill(-1));
const masks=solutions.map(p=>ports.map(i=>p[i]).join('')).sort();
ck(masks.join(',')===expected.slice().sort().join(','),'exact local words');
const words={};
V.forEach((v,i)=>{const key=solutions.map(p=>p[i]).join('');(words[key]??=[]).push(v)});
const allowed=name==='X'?masks.filter(w=>[0,2,4,6].every(i=>w[i]===w[i+1])):masks;
if(name==='X')ck(allowed.join(',')==='00000000,11111111','conditional X');
return {name,variables:n,rows:m,rawWords:masks,pairedWords:allowed,deletionChecks:checks,disconnectedAfterTwo:disconnected,searchCalls:calls,truthPatterns:words};
});
}
console.log(JSON.stringify(main(),null,2));
