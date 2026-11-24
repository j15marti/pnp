function DR09(){
 const results={cases:[],checks:0,graphSteps:0,closureScans:0,forcedPins:0,referenceWords:0};
 function check(x){results.checks++;if(!x)throw Error("assertion "+results.checks)}
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 function compile(n,F,k,t){
   const h=k+1,l=t+1,d=n+h+l,qmask=((1<<l)-1)<<(n+h),pmask=((1<<h)-1)<<n,tests=[];
   for(let j=0;j<h;j++)tests.push({mask:1<<(n+j),v:1,yes:j+1,no:-1});
   tests.push({mask:qmask,v:0,yes:h+1,no:-2});
   for(const C of F){const start=tests.length;for(let j=0;j<C.length;j++){
     const lit=C[j];tests.push({mask:1<<(Math.abs(lit)-1),v:lit>0?1:0,yes:start+C.length,no:j+1===C.length?-2:start+j+1});
   }}
   return {d,pmask,qmask,tests,h,l,n};
 }
 function reject(G,z,b){let i=0;while(i>=0&&i<G.tests.length){const a=G.tests[i];results.graphSteps++;i=parity(z&a.mask)===(a.v^(i===G.h?b:0))?a.yes:a.no;}return +(i===-2)}
 function rank(words,d){if(!words.length)return -1;let basis=Array(d).fill(0);const a=words[0];let r=0;for(const w of words){let x=w^a;for(let i=d-1;i>=0;i--)if(x&(1<<i)){if(basis[i])x^=basis[i];else{basis[i]=x;r++;break}}}return r}
 // Scoped certified local affine-hull closure: all rejection events have
 // >=2 independent p rows, so their complements span the full chart.
 function closure(G,F){for(let j=0;j<=F.length;j++){results.closureScans++;check(G.h>=2)}}
 function run(name,n,F,k=1,t=2){
   const G=compile(n,F,k,t);closure(G,F);
   const X=1<<n,words=1<<G.d,pcount=1<<G.h,Q=1<<G.l,good=[[],[]],marg=[new Map(),new Map()],walsh=[0,0];let zf=0;
   const evalF=x=>F.every(C=>C.some(l=>!!(x&(1<<(Math.abs(l)-1)))===(l>0)));
   for(let x=0;x<X;x++)zf+=+evalF(x);
   let diff=0,mixed=0;
   const submasks=Array.from({length:Q-1},(_,i)=>i);
   for(let b=0;b<2;b++){closure(G,F);closure(G,F);
     for(let z=0;z<words;z++){
       const p=(z>>n)&(pcount-1),q=z>>(n+G.h),x=z&(X-1);
       const f=p!==pcount-1||(parity(q)===b&&evalF(x));
       const a=1-reject(G,z,b);results.referenceWords++;check(a===+f);
       if(a){good[b].push(z);walsh[b]+=parity(q)?-1:1;for(const mask of submasks){const key=((x*pcount+p)*Q+mask)*Q+(q&mask);marg[b].set(key,(marg[b].get(key)||0)+1)}}
     }
   }
   const s0=new Set(good[0]),s1=new Set(good[1]);for(let z=0;z<words;z++){diff+=+(s0.has(z)!==s1.has(z));mixed+=+(!s0.has(z)&&!s1.has(z))}
   check(good[0].length===good[1].length);check(rank(good[0],G.d)===G.d);check(rank(good[1],G.d)===G.d);
   const expected=(pcount-1)*X*Q+zf*Q/2;
   check(good[0].length===expected);check(diff===zf*Q);check(walsh[0]===zf*Q/2);check(walsh[1]===-zf*Q/2);
   check(mixed===X*Q-zf*Q);check(marg[0].size===marg[1].size);
   for(const [key,v] of marg[0])check(v===marg[1].get(key));
   results.cases.push({name,n,k,t,sourceModels:zf,branchModels:good[0].length,hullRank:G.d,disagreement:diff,mixedReject:mixed,walsh,graphTestNodes:G.tests.length,marginalEntries:marg[0].size});
 }
 const cube=Array.from({length:8},(_,i)=>Array.from({length:3},(_,j)=>(i&(1<<j)?-1:1)*(j+1)));
 for(let i=0;i<256;i++)run("cube-"+i,3,cube.filter((_,j)=>i&(1<<j)));
 const triples=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 const fano=triples.flatMap(C=>[C,C.map(x=>-x)]);
 run("fano",7,fano);for(let j=0;j<14;j++)run("fano-minus-"+j,7,fano.filter((_,i)=>i!==j));
 for(const k of [2,3]){run("higher-rank-sat-"+k,3,cube.slice(1),k,3);run("higher-rank-unsat-"+k,3,cube,k,3)}
 return results;
}
console.log(JSON.stringify(DR09(),null,2));
