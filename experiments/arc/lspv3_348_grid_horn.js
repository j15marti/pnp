// LSPV-3 GRID-MINIMAL-HORN348; standalone Node.js (no imports).
function run(){
 const check=(v,msg)=>{if(!v)throw Error(msg||"failed");};
 const out=[];
 for(const r of [2,3,4,5]){
  const k=r*r,n=2*k+1,x=i=>i+1,y=j=>k+j+1;
  const pi=i=>((i-1)%r)*r+Math.floor((i-1)/r)+1;
  const src=[[x(0)],[-x(k)],[-y(1)]];
  for(let j=2;j<=k;j++)src.push([y(j-1),-y(j)]);
  for(let i=1;i<=k;i++)src.push([-x(i-1),x(i),y(pi(i))]);
  const m=src.length,cla=src.map(a=>a.slice()),P=[];
  const norm=a=>Array.from(new Set(a)).sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  function res(a,b,p){
   check(a<cla.length&&b<cla.length);
   const A=cla[a],B=cla[b];
   check(A.includes(p)&&B.includes(-p)||A.includes(-p)&&B.includes(p));
   const C=norm(A.concat(B).filter(z=>Math.abs(z)!==Math.abs(p)));
   P.push({a,b,p,C});cla.push(C);return cla.length-1;
  }
  const yu={1:2};
  for(let j=2;j<=k;j++)yu[j]=res(j+1,yu[j-1],y(j-1));
  let root=0;
  for(let i=1;i<=k;i++){let b=res(k+1+i,yu[pi(i)],y(pi(i)));root=res(b,root,-x(i-1));}
  res(root,1,x(k));
  check(m===2*k+2&&P.length===3*k&&cla.at(-1).length===0);
  for(let t=0;t<P.length;t++){
   const z=P[t],A=cla[z.a],B=cla[z.b];
   check(z.a<m+t&&z.b<m+t);
   check(A.includes(z.p)&&B.includes(-z.p)||A.includes(-z.p)&&B.includes(z.p));
   check(JSON.stringify(norm(A.concat(B).filter(q=>Math.abs(q)!==Math.abs(z.p))))===JSON.stringify(z.C));
  }
  const sat=(F,a)=>F.every(C=>C.some(l=>a[Math.abs(l)]===(l>0)));
  let deletions=0,signs=0;
  for(let d=0;d<m;d++){
   const a=Array(n+1).fill(false);
   if(d===1){for(let j=0;j<=k;j++)a[x(j)]=true;}
   else if(d===2){a[x(0)]=true;for(let j=1;j<=k;j++)a[y(j)]=true;}
   else if(d>=3&&d<k+2){
    const j=d-1;for(let h=j;h<=k;h++)a[y(h)]=true;
    let i=1;while(pi(i)!==j)i++;
    for(let h=0;h<i;h++)a[x(h)]=true;
   }else if(d>=k+2){for(let h=0;h<d-k-1;h++)a[x(h)]=true;}
   check(sat(src.filter((_,id)=>id!==d),a)&&!sat([src[d]],a),"deletion");
   deletions++;
   for(let j=0;j<src[d].length;j++){
    let F=src.map(C=>C.slice());F[d][j]*=-1;
    check(sat(F,a),"sign");signs++;
   }
  }
  // Primal graph contains an r by r grid minor after contracting xi-y_{pi(i)}.
  const ed=new Set();
  for(const C of src)for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){
   const a=Math.abs(C[i]),b=Math.abs(C[j]);ed.add(Math.min(a,b)+":"+Math.max(a,b));
  }
  const rep={};
  for(let i=1;i<=k;i++){rep[x(i)]=i;rep[y(pi(i))]=i;}
  const reduced=new Set();
  for(const edge of ed){let [a,b]=edge.split(":").map(Number);
   if(rep[a]&&rep[b]&&rep[a]!==rep[b])reduced.add(Math.min(rep[a],rep[b])+":"+Math.max(rep[a],rep[b]));
  }
  let gridEdges=0;
  for(let row=0;row<r;row++)for(let col=0;col<r;col++){
   const i=row*r+col+1;
   for(const j of [col+1<r?i+1:0,row+1<r?i+r:0])if(j){
    check(reduced.has(i+":"+j));gridEdges++;
   }
  }
  for(const C of src)check(C.filter(z=>(Math.abs(z)<=k+1?z:-z)>0).length<=1,"Horn rename");
  let F=src.map(C=>C.slice());F[1][0]*=-1;
  const a=Array(n+1).fill(false);for(let i=0;i<=k;i++)a[x(i)]=true;check(sat(F,a));
  let exhaustive=0;
  if(r===2)for(let mask=0;mask<(1<<n);mask++){
   const a=Array(n+1).fill(false);
   for(let i=1;i<=n;i++)a[i]=Boolean(mask&(1<<(i-1)));
   check(!sat(src,a));exhaustive++;
  }
  const dimacs="p cnf "+n+" "+m+"\n"+src.map(C=>C.join(" ")+" 0\n").join("");
  out.push({r,k,n,m,signs,deletions,q:P.length,Nbits:8*dimacs.length,proofBits:8*JSON.stringify(P).length,gridEdges,exhaustive});
 }
 return {status:"PASS",fixtures:out};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
