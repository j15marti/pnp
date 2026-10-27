// Standalone Node.js reproducer; node 2026-10-27_0136_UTM_JUMP_CHANGE150_repro.js
// One READ-ONLY bounded input head and ONE initially blank work-head position.
// Source is ^a#X^(4m)#b$, work head has a built-in left endmarker, D=0.
'use strict';
let checks=0;
function ok(test,note){checks++;if(!test)throw Error("ASSERT "+checks+" "+note)}
function run(a,b){
 const m=a.length, src='^'+a+'#'+'X'.repeat(4*m)+'#'+b+'$';
 let p=0,w=0,T=0,R=0,prev=0,peak=0,loops=0;
 function move(di,dw=0){
   ok(p+di>=0 && p+di<src.length && w+dw>=0,'endmarkers');
   if(di&&prev&&prev!==di)R++;
   if(di)prev=di;p+=di;w+=dw;T++;peak=Math.max(peak,w);
 }
 while(true){
  ok(p===0 && src[p]==='^','start');
  while(w>0)move(1,-1);
  move(1);let left=src[p];loops++;
  if(left==='#')return {accept:true,T,R,S:peak+1,D:0,loops};
  ok(left==='0'||left==='1','Alice');
  move(-1);
  while(src[p]!=='^')move(-1,1);
  let separators=0;
  while(separators<2){move(1);if(src[p]==='#')separators++}
  while(w>0)move(1,-1);
  move(1);let right=src[p];ok(right==='0'||right==='1','Bob');
  if(left==='1'&&right==='1')return {accept:false,T,R,S:peak+1,D:0,loops};
  move(-1);
  while(src[p]!=='#')move(-1,1);
  while(src[p]!=='^')move(-1);
  move(0,1);
 }
}
function choose(n,r){let v=1;for(let i=1;i<=r;i++)v=v*(n-i+1)/i;return Math.round(v)}
function alphabet(q,k,S,D,J,g=2,sigma=5){
 const h=2*S+3;let Z=0;for(let r=0;r<=Math.min(D,k*h);r++)Z+=choose(k*h,r)*(g-1)**r;
 return {A:2*q*q*sigma*sigma*(J+1)**2*h**(2*k)*Z*Z,
         V:2*q*(J+1)*h**k,Z};
}
function audit(){
 const rows=[];let total=0,accepted=0;
 for(let m=1;m<=6;m++){
  let maxT=0,maxR=0,maxS=0,cases=0;
  for(let x=0;x<1<<(2*m);x++){
   const a=(x&((1<<m)-1)).toString(2).padStart(m,'0');
   const b=(x>>m).toString(2).padStart(m,'0');
   const z=run(a,b);let truth=true;
   for(let i=0;i<m;i++)if(a[i]==='1'&&b[i]==='1')truth=false;
   ok(z.accept===truth,'DISJ');
   ok(z.D===0&&z.S<=m+1,'write-free unary position');
   ok(z.T<=12*m*(6*m+4)+20*m+20,'clock');
   ok(z.R<=6*m+2,'reversals');
   maxT=Math.max(maxT,z.T);maxR=Math.max(maxR,z.R);maxS=Math.max(maxS,z.S);
   cases++;total++;if(z.accept)accepted++;
  }
  rows.push({m,cases,source_bits:6*m+4,maxT,maxR,maxS});
 }
 let entropyCases=0;
 for(const [q,k] of [[2,1],[3,2]])for(let S=0;S<=6;S++)
 for(let D=0;D<=6;D++)for(const J of [1,2,3,8]){
  const z=alphabet(q,k,S,D,J);
  ok(z.A>=2&&z.V>=2*q,'event alphabet');
  ok(alphabet(q,k,S,D,J+1).A>=z.A,'jump monotonic');
  ok(alphabet(q,k,S,D+1,J).A>=z.A,'change monotonic');
  ok((D+1)*z.V+D<=(D+1)*(z.V+1),'change crossings charged');
  entropyCases++;
 }
 let collision=[];
 for(let x=0;x<2;x++)for(let y=0;y<2;y++){
  const bob=(y===0?'10':'01'),right=bob[x]==='1';
  ok(right===(x===y),'jump equality');
  if(right)collision.push({x,y,naive_label:'q_final;blank;right',
                                  correct_label:'q_final;blank;right;landing='+x});
 }
 ok(collision.length===2&&collision[0].naive_label===collision[1].naive_label,
   'landing omitted creates false history collision');
 ok(collision[0].correct_label!==collision[1].correct_label,'endpoint disambiguates');
 return {run:'UTM-JUMP-CHANGE150',status:'COMPUTATIONAL; theory separately proved',
  assertions:checks,unary_cases:total,unary_accepts:accepted,unary_rows:rows,
  finite_entropy_parameter_cases:entropyCases,collision,
  write_change_cut_warning:'changing transitions must contribute +D to finite crossing cap',
  limits:'DISJ promise, one bounded input head; no unrestricted SAT or RAM bound'};
}
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
module.exports={audit,run,alphabet};
