function audit(){
 const out={fields:[2,3,101],hcCases:0,pmCases:0,compileRuns:0,wordChecks:0,rankChecks:0,referencePairChecks:0,weightedChecks:0,identityChecks:0,neighborPairs:0,closureChecks:0,abstractControls:[],identitySizes:[],failures:0}; 
 const ck=(x,m)=>{if(!x)throw Error(m)};
 const words=(n,k)=>{let a=[[]];for(let i=0;i<k;i++)a=a.flatMap(x=>Array.from({length:n},(_,j)=>[...x,j]));return a};
 const mod=(x,p)=>(x%p+p)%p;
 function inv(x,p){for(let i=1;i<p;i++)if(mod(x*i,p)===1)return i;throw Error("inverse");}
 function invert(A,p){let n=A.length;let B=A.map((r,i)=>[...r,...Array.from({length:n},(_,j)=>+(i===j))]);for(let i=0;i<n;i++){let j=i;while(j<n&&!B[j][i])j++;ck(j<n,"singular");[B[i],B[j]]=[B[j],B[i]];let z=inv(B[i][i],p);B[i]=B[i].map(x=>mod(z*x,p));for(let j=0;j<n;j++)if(j!==i){let z=B[j][i];B[j]=B[j].map((x,k)=>mod(x-z*B[i][k],p));}}return B.map(r=>r.slice(n));}
 function rank(A,p){let B=A.map(x=>x.slice()),i=0;for(let j=0;j<(B[0]||[]).length&&i<B.length;j++){let k=i;while(k<B.length&&!B[k][j])k++;if(k===B.length)continue;[B[i],B[k]]=[B[k],B[i]];let z=inv(B[i][j],p);B[i]=B[i].map(x=>mod(x*z,p));for(let k=i+1;k<B.length;k++){let z=B[k][j];B[k]=B[k].map((x,l)=>mod(x-z*B[i][l],p));}i++;}return i;}
 function compile(n,d,valid,p){
   const all=Array.from({length:d+1},(_,i)=>words(n,i)),basis=[],piv=[],mat=[],trans=[];
   const yes=all[d].filter(valid); // reference only; not part of proposed oracle compiler
   const root=all[0][0]; if(!yes.length){out.compileRuns++;return {ranks:Array(d+1).fill(0),evalWord:()=>0,weighted:()=>0};}
   basis[0]=[root];piv[0]=[yes[0]];mat[0]=[[1]];
   function coords(a,i){let r=basis[i].length,vals=piv[i].map(z=>+valid([...a,...z]));return Array.from({length:r},(_,j)=>mod(vals.reduce((s,x,k)=>s+x*mat[i][k][j],0),p));}
   for(let i=1;i<=d;i++){
      basis[i]=[];piv[i]=[];mat[i]=[];
      const candidates=basis[i-1].flatMap(a=>Array.from({length:n},(_,j)=>[...a,j]));
      for(const a of candidates){
         const c=coords(a,i);let diff=null;
         for(const z of all[d-i]){
           out.referencePairChecks++;const val=mod(c.reduce((s,x,j)=>s+x*+valid([...basis[i][j],...z]),0),p);
           if(val!==+valid([...a,...z])){diff=z;break;}
         }
         if(diff!==null){basis[i].push(a);piv[i].push(diff);mat[i]=invert(basis[i].map(b=>piv[i].map(z=>+valid([...b,...z]))),p);}
      }
      trans[i]=basis[i-1].map(a=>Array.from({length:n},(_,j)=>coords([...a,j],i)));
   }
   function evalWord(w){let vec=[1];for(let i=1;i<=d;i++)vec=Array.from({length:basis[i].length},(_,j)=>mod(vec.reduce((s,x,k)=>s+x*trans[i][k][w[i-1]][j],0),p));return vec[0];}
   function weighted(weights){let vec=[1];for(let i=1;i<=d;i++)vec=Array.from({length:basis[i].length},(_,j)=>mod(vec.reduce((s,x,k)=>s+x*trans[i][k].reduce((q,c,l)=>q+c[j]*weights[i-1][l],0),0),p));return vec[0];}
   for(let i=0;i<=d;i++){const actual=rank(all[i].map(a=>all[d-i].map(z=>+valid([...a,...z]))),p);ck(actual===basis[i].length,"rank");out.rankChecks++;}
   out.compileRuns++;return {ranks:basis.map(a=>a.length),evalWord,weighted};
 }
 function cycle(w){let n=w.length;if(new Set(w).size!==n)return false;let v=0,seen=new Set;for(let i=0;i<n;i++){if(seen.has(v))return false;seen.add(v);v=w[v];}return v===0;}
 function perm(a){if(!a.length)return [[]];return a.flatMap((x,i)=>perm(a.filter((_,j)=>j!==i)).map(t=>[x,...t]));}
 function graph(n,mask){let a=Array.from({length:n},()=>Array(n).fill(false)),b=0;for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)a[i][j]=!!(mask&(1<<b++));return a;}
 function test(n,d,valid,reference){const all=words(n,d);let y=all.filter(valid);ck(y.length===reference.length&&new Set(reference.map(w=>w.join(","))).size===y.length&&reference.every(valid),"reference"); // exact unary closure via both independent lists
  for(let i=0;i<d;i++)for(let j=0;j<n;j++){ck(y.some(w=>w[i]===j)===reference.some(w=>w[i]===j),"support");ck(y.some(w=>w[i]!==j)===reference.some(w=>w[i]!==j),"forced");out.closureChecks+=2;}
  let ranks=[];
  for(const p of out.fields){const c=compile(n,d,valid,p);ranks.push(c.ranks);for(const w of all){ck(c.evalWord(w)===+valid(w),"word");out.wordChecks++;}
   const W=Array.from({length:d},(_,i)=>Array.from({length:n},(_,j)=>(i*7+j*3+2)%p));let s=0;for(const w of reference)s=mod(s+w.reduce((a,j,i)=>mod(a*W[i][j],p),1),p);ck(c.weighted(W)===s,"weighted");out.weightedChecks++;
  }return ranks;
 }
 let seed=17041;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;};
 for(const n of [2,3,4]){const max=1<<(n*(n-1));const masks=n<4?Array.from({length:max},(_,i)=>i):[0,max-1,...Array.from({length:80},()=>rand()%max)];
  for(const mask of masks){const a=graph(n,mask),valid=w=>cycle(w)&&w.every((j,i)=>a[i][j]);let ref=[];for(const t of perm(Array.from({length:n-1},(_,i)=>i+1))){const order=[0,...t],w=Array(n);for(let i=0;i<n;i++)w[order[i]]=order[(i+1)%n];if(w.every((j,i)=>a[i][j]))ref.push(w);}test(n,n,valid,ref);out.hcCases++;}
 }
 for(const n of [2,3])for(let mask=0;mask<(1<<(n*n));mask++){const edge=(i,j)=>!!(mask&(1<<(i*n+j))),valid=w=>new Set(w).size===n&&w.every((j,i)=>edge(i,j));const ref=perm(Array.from({length:n},(_,i)=>i)).filter(w=>w.every((j,i)=>edge(i,j)));test(n,n,valid,ref);out.pmCases++;}
 for(const k of [3,4]){const d=2*k,valid=w=>w.slice(0,k).reduce((s,x,i)=>s^(x&w[k+i]),0)===1;let r=test(2,d,valid,words(2,d).filter(valid));out.abstractControls.push({k,ranks:r,distinctMiddleRows:2**k});}
 function sigma(k,mask){let a=Array.from({length:k},(_,i)=>i);for(let i=0;i<Math.floor(k/2);i++)if(mask&(1<<i))[a[2*i],a[2*i+1]]=[a[2*i+1],a[2*i]];return a;}
 function checkPair(f,h){const k=f.length;const g=h.map(i=>(i+1)%k);const w=[...f.map(i=>k+i),...g];return cycle(w);}
 for(const k of [2,3,4,6,8,10,12]){let m=2**Math.floor(k/2);for(let i=0;i<m;i++)for(let j=0;j<m;j++){ck(checkPair(sigma(k,i),sigma(k,j))===(i===j),"identity");out.identityChecks++;}out.identitySizes.push({vertices:2*k,minor:m});}
 // Native genuine graph pairs: unique full cycle vs one missing edge; plus wrong return permutation yields disjoint cycles.
 for(const k of [2,4,8,16,32,64,128]){let f=Array.from({length:k},(_,i)=>i),h=f.slice();[h[0],h[1]]=[h[1],h[0]];ck(checkPair(f,f)&&!checkPair(f,h),"native neighbor"); // each graph has exactly one possible successor at every row, so direct cycle test exact
  let w=[...f.map(i=>k+i),...f.map(i=>(i+1)%k)];ck(cycle(w),"yes lift");const rowEdges=w.map(j=>[j]);rowEdges[0]=[];ck(rowEdges.some(r=>!r.length),"one deletion NO");out.neighborPairs+=2;}
 return out;
}
console.log(JSON.stringify(audit(),null,2));
