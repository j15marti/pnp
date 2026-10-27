'use strict';
// LSPV-4 TWO-RW-CRITICAL-AUX-WRITE161: reproducible abstract native
// unit-head/two-writable-tape model. Separate from the mathematical proof.
// The host enumerates inputs; simulated heads move at most one cell per step.
let assertions=0;
function ck(test,msg){assertions++;if(!test)throw new Error(msg);}
function bits(n,m){return n.toString(2).padStart(m,'0');}
function comp(a){return a.split('').map(c=>c==='0'?'1':'0').join('');}
function disj(a,b){for(let i=0;i<a.length;i++)if(a[i]==='1'&&b[i]==='1')return false;return true;}
class Run {
 constructor(a,b){
  this.x=('^'+a+'#'+'X'.repeat(8*a.length)+'#'+b+'$').split('');
  this.w=new Map();this.i=0;this.j=0;this.maxj=0;
  this.cut=2+a.length+Math.floor(8*a.length/2);
  this.T=0;this.H1=0;this.R1=0;this.dir=0;this.D1=0;this.D2=0;this.E=[];this.C=[];
 }
 r1(){return this.x[this.i];}
 r2(){return this.w.get(this.j)||'_';}
 m1(d,q){
  ck(d===1||d===-1,'unit tape1 move');
  const o=this.i,n=o+d;ck(n>=0&&n<this.x.length,'tape1 bounds');
  this.i=n;this.T++;this.H1++;
  if(this.dir!==0&&this.dir!==d)this.R1++;
  this.dir=d;
  if((o===this.cut-1&&n===this.cut)||(o===this.cut&&n===this.cut-1)){
   const tag='C'+(d>0?'R':'L')+':'+q+':'+this.j;
   this.E.push(tag);
   this.C.push({tag,snap:[...this.w.entries()].sort((a,b)=>a[0]-b[0])});
  }
 }
 m2(d){ck(d===1||d===-1,'unit tape2 move');ck(this.j+d>=0,'left boundary');this.j+=d;this.maxj=Math.max(this.maxj,this.j);this.T++;}
 w1(c){if(this.r1()!==c){this.x[this.i]=c;this.D1++;this.E.push('W1');}this.T++;}
 w2(c){if(this.r2()!==c){this.w.set(this.j,c);this.D2++;this.E.push('W2:'+this.j+':'+c);}this.T++;}
 rewind(){while(this.r1()!=='^')this.m1(-1,'rewind');}
 seekA(){
  this.rewind();this.m1(1,'scanAlice');
  while(this.r1()!=='#'){
   if(this.r1()==='0'||this.r1()==='1'){
    const v=this.r1();this.w1(v==='0'?'u':'v');return v;
   }
   this.m1(1,'scanAlice');
  }
  return null;
 }
 seekB(carry){
  while(this.r1()!=='#')this.m1(1,'seekBob'+carry);
  this.m1(1,'seekBob'+carry);
  while(this.r1()!=='#')this.m1(1,'seekBob'+carry);
  this.m1(1,'scanBob');
  while(this.r1()!=='$'){
   if(this.r1()==='0'||this.r1()==='1'){
    const v=this.r1();this.w1(v==='0'?'u':'v');return v;
   }
   this.m1(1,'scanBob');
  }
  throw Error('unmatched Bob length');
 }
 marker(){
  for(;;){const a=this.seekA();if(a===null)return true;
   const b=this.seekB(a);if(a==='1'&&b==='1')return false;}
 }
 buffer(){
  this.m1(1,'copyA');
  while(this.r1()!=='#'){
   const c=this.r1();ck(c==='0'||c==='1','read Alice symbol');
   this.w2(c);this.m2(1);this.m1(1,'copyA');
  }
  while(this.j>0)this.m2(-1);
  this.m1(1,'seekBob');while(this.r1()!=='#')this.m1(1,'seekBob');
  this.m1(1,'cmpBob');
  while(this.r1()!=='$'){
   const a=this.r2(),b=this.r1();
   ck((a==='0'||a==='1')&&(b==='0'||b==='1'),'read Bob symbol');
   if(a==='1'&&b==='1')return false;
   this.m1(1,'cmpBob');this.m2(1);
  }
  return true;
 }
 replay(){
  const v=new Map();let cursor=0;
  for(const e of this.E){
   if(e.startsWith('W2:')){const p=e.split(':');v.set(+p[1],p[2]);}
   else if(e.startsWith('C')){
    const c=this.C[cursor++];
    ck(c.tag===e,'cross direction/control/position including carry');
    ck(JSON.stringify([...v.entries()].sort((a,b)=>a[0]-b[0]))===
       JSON.stringify(c.snap),'full tape2 crossing state reconstructed');
   }
  }
  ck(cursor===this.C.length,'all crossings reconstructed');
 }
 get S2(){return this.maxj+1;}
 get code(){return this.E.join('|');}
}
const summaries=[],hostile=[];let total=0,accepted=0,distinct=0;
for(let m=1;m<=6;m++){
 const n=1<<m,diags=new Set();let maxTm=0,maxTb=0,maxD1=0;
 for(let ai=0;ai<n;ai++)for(let bi=0;bi<n;bi++){
  const a=bits(ai,m),b=bits(bi,m),expected=disj(a,b);
  const A=new Run(a,b);ck(A.marker()===expected,'mark correct');A.replay();
  ck(A.D2===0&&A.S2===1&&A.D1<=2*m,'marker native budgets');
  ck(A.T<=8*m*(A.x.length+5),'marker polynomial time');
  const B=new Run(a,b);ck(B.buffer()===expected,'buffer correct');B.replay();
  ck(B.D1===0&&B.D2===m&&B.S2<=m+1,'buffer native budgets');
  ck(B.T<=5*(B.x.length+m+5),'buffer linear time');
  total+=2;if(expected)accepted+=2;
  maxTm=Math.max(maxTm,A.T);maxTb=Math.max(maxTb,B.T);maxD1=Math.max(maxD1,A.D1);
 }
 for(let i=0;i<n;i++){
  const a=bits(i,m),d=new Run(a,comp(a));
  ck(d.marker(),'diagonal acceptance');
  ck(!diags.has(d.code),'cross-history injection including carried bit');
  diags.add(d.code);distinct++;
 }
 summaries.push({m,ordered_pairs:n*n,runs:2*n*n,mark_max_T:maxTm,
  mark_max_D1:maxD1,mark_D2:0,mark_S2:1,buffer_max_T:maxTb,
  buffer_D1:0,buffer_D2:m,buffer_S2:m+1,diagonal_distinct:diags.size});
}
for(const m of [8,16,32,64,128]){
 const a='0'.repeat(m),b='1'.repeat(m);
 const A=new Run(a,b);ck(A.marker(),'all-zero Alice, all-one Bob');
 ck(A.D1===2*m&&A.D2===0&&A.S2===1,'W1-only falsifier');
 ck(A.T>m*m,'quadratic marker time');
 const B=new Run(a,b);ck(B.buffer(),'buffered comparator');
 ck(B.D2===m&&B.T<12*(10*m+10),'linear tape2 buffer');
 hostile.push({m,N:A.x.length,marker_T:A.T,marker_D1:A.D1,
  marker_D2:A.D2,marker_S2:A.S2,marker_R1:A.R1,
  buffer_T:B.T,buffer_D2:B.D2,buffer_S2:B.S2});
}
const result={run_id:'TWO-RW-CRITICAL-AUX-WRITE161',
 date:'2026-10-27',type:'exhaustive unit-head abstract-DISJ',
 seed:null,assertions,failures:0,simulated_runs:total,
 accepting_runs:accepted,diagonal_distinct:distinct,
 summaries,hostile,
 caveats:['Not a general SAT solver','Input is abstract bit-serialized easy DISJ promise',
 'Mathematical lower bound requires the separate proof','Every tape2 WRITE and all boundary states replayed']};
if(typeof console!=='undefined') console.log(JSON.stringify(result,null,2));
