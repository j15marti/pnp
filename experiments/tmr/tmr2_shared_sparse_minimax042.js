/* TMR-2/031: randomized sparse-oracle minimax exact verifier.
 * Node.js or hosted V8; standard JavaScript, no dependencies. Computational only.
 */
"use strict";
function choose(n,k) {
  if(k<0||k>n)return 0n;
  k=Math.min(k,n-k);let a=1n;
  for(let i=1;i<=k;i++)a=a*BigInt(n-k+i)/BigInt(i);
  return a;
}
function pop(x){let n=0;for(;x;x>>=1)n+=x&1;return n;}
function subsets(M,r){let a=[];for(let s=0;s<(1<<M);s++)if(pop(s)===r)a.push(s);return a;}
function U(M,r,q){return [choose(M-q,r),choose(M,r)];}
function adaptive(mask,M,q,salt){
  let st=salt+17,seen=0,yes=0,queries=0;
  for(let j=0;j<q;j++){
    let at=((st*7+13*j+3)%M+M)%M;
    while((seen>>at)&1)at=(at+1)%M;
    seen|=(1<<at);queries++;
    const bit=(mask>>at)&1;
    st=(st*11+7*j+31*bit)%1000003;
    yes^=((bit*3+st+j)&1);
  }
  return {out:yes,visited:seen,queries};
}
function run(){
 let assertions=0,pairs=0,adap=0,cases=0,sharp=0;
 const ck=(b,why)=>{assertions++;if(!b)throw Error(why);};
 for(let M=1;M<=9;M++)for(let r=1;r<=M;r++){
   const Ss=subsets(M,r),denom=BigInt(Ss.length);
   ck(denom===choose(M,r),"support count");
   for(let q=0;q<=M;q++){
     const Qs=subsets(M,q),[num,den]=U(M,r,q);
     let miss=0n;
     for(const S of Ss)for(const Q of Qs){pairs++;if(!(S&Q))miss++;}
     ck(miss===denom*choose(M-r,q),"miss count");
     ck(miss*den===num*denom*BigInt(Qs.length),"hypergeometric symmetry");
     const alphaNum=num,alphaDen=num+den;
     ck(alphaNum*den===(alphaDen-alphaNum)*num,"minimax balance");
     if(q===0)ck(alphaNum*2n===alphaDen,"no-query error");
     if(q===M-r+1)ck(num===0n,"zero-error threshold");
     if(q<M-r+1)ck(num>0n,"deterministic below threshold");
     let qMin=-1;
     for(let j=0;j<=M;j++){const [u,d]=U(M,r,j);if(3n*u<=d){qMin=j;break;}}
     if(q===qMin)ck(3n*num<=den,"one quarter sufficient");
     if(q<qMin)ck(3n*num>den,"one quarter necessary");
     if(M<=8){
       for(const S of Ss){
         let m=0n;for(const Q of Qs)if(!(S&Q))m++;
         ck(m*den===num*BigInt(Qs.length),"support symmetry");
         ck((alphaDen-alphaNum)*m*den===alphaNum*den*BigInt(Qs.length),"minimax sharp");
         sharp++;
       }
       for(const salt of [0,1,7,19]){
         const z=adaptive(0,M,q,salt);
         for(const S of Ss){
           const y=adaptive(S,M,q,salt);
           ck(y.queries===q&&z.queries===q,"adaptive budget");
           if(!(S&z.visited))ck(y.out===z.out,"zero path indistinguishability");
           adap++;
         }
       }
     }
     cases++;
   }
 }
 return {tag:"TMR2_RANDOM_SHARED_MINIMAX042",engine:"hosted V8, standalone Node-compatible source",assertions,failures:0,exhaustive_support_query_pairs:pairs,adaptive_sparse_runs:adap,exact_sharpness_per_support:sharp,parameter_cases:cases,seed:"none; exact enumeration, adaptive salts 0,1,7,19",status:"COMPUTATIONAL finite checks for a separate PROVED/RESTRICTED symbolic argument",sample:{M:8,r:2,q:2,U:"15/28",minimax_error:"15/43"},scope:"source-independent randomized globally shared adaptive evaluation oracle; zero source versus r-sparse source, one-bit output"};
}
const RESULT=run();
if(typeof process!=="undefined"&&process.stdout)process.stdout.write(JSON.stringify(RESULT,null,2)+"\n");
globalThis.__TMR2_RESULT=RESULT;
