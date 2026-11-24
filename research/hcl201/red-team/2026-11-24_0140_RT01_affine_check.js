function run(){
 const parity=x=>{let p=0;while(x){p^=x&1;x>>>=1;}return p;};
 const rank=S=>{let b=Array(16).fill(0),r=0;for(let v of S){while(v){let i=31-Math.clz32(v);if(b[i])v^=b[i];else{b[i]=v;r++;break;}}}return r;};
 const hull=S=>{let a=S[0],R=rank(S.map(x=>x^a));return Array.from({length:16},(_,i)=>i).filter(x=>rank([...S.map(y=>y^a),x^a])===R);};
 let B=Array.from({length:16},(_,i)=>i).filter(i=>i.toString(2).replace(/0/g,"").length===2);
 let hullChecks=0;
 if(hull(B).length!==8||hull(B).some(parity))throw Error("B4 hull");hullChecks++;
 for(let f=0;f<2;f++){let S=B.filter(x=>((x>>2)&1)===f);let H=hull(S);if(H.length!==4||H.some(x=>parity(x)||((x>>2)&1)!==f))throw Error("fixed anchor hull");hullChecks++;}
 const family=n=>{let F=[],next=n+1;function unit(l){let a=next++,b=next++;for(let s of [1,-1])for(let t of [1,-1])F.push([l,s*a,t*b]);}unit(1);for(let i=1;i<n;i++){let a=next++;F.push([-i,i+1,a],[-i,i+1,-a]);}unit(-n);return {F,nv:next-1};};
 const ok=(F,m)=>F.every(c=>c.some(l=>Boolean((m>>(Math.abs(l)-1))&1)===(l>0)));
 let small=[],large=[];
 for(let n of [2,3,4,5,8,16,32,64,128]){
  const {F,nv}=family(n),m=F.length;
  if(F.some(c=>new Set(c.map(Math.abs)).size!==3))throw Error("not distinct");
  // One z per clause, two slack variables per clause, each with a distinct pivot.
  // Fix f=0; all original variables and z freely choose; compute w by parity.
  // Verify all local projections over relevant independent bits with signs for each clause.
  let localChecks=0;
  for(let [a,b,c] of F){for(let f of [0,1]){
   let S1=new Set(),S2=new Set();
   for(let p=0;p<16;p++){let A=(p&1)^f^+(a<0),B=((p>>1)&1)^f^+(b<0),C=((p>>2)&1)^f^+(c<0),z=(p>>3)&1;
    S1.add(A+2*B+4*z+8*(A^B^z));S2.add((z^1)+2*C+4*f+8*((z^1)^C^f));
   }
   let H1=hull(B4()),H2=hull(B4().filter(x=>((x>>2)&1)===f));
   if(S1.size!==H1.length||H1.some(x=>!S1.has(x))||S2.size!==H2.length||H2.some(x=>!S2.has(x)))throw Error("local projection");localChecks+=2;
  }}
  large.push({chain:n,originalIncludingPadding:nv,clauses:m,freeDimensionsWithAnchorFixed:nv+m,independentSlackPivots:2*m,localChecks});
  if(n<=5){let solutions=0,neighbor=Array(m).fill(0);for(let x=0;x<(1<<nv);x++){let bad=[];for(let i=0;i<m;i++)if(!ok([F[i]],x))bad.push(i);if(bad.length===0)solutions++;if(bad.length===1)neighbor[bad[0]]++;}if(solutions||neighbor.some(v=>v===0))throw Error("minimal unsat");small.push({n,nv,m,assignments:1<<nv,solutions,deletionNeighborCounts:neighbor});}
 }
 function B4(){return B;}
 return {hullChecks,small,large,errors:0};
}
console.log(JSON.stringify(run(),null,2));
