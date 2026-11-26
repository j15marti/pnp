// Reproduce with Node.js
function audit(){
  const out={mode:"interleaved, deterministic reference",A:{},B:{},C:{},integrated:{},controls:{}};
  let seed=192837; const rand=(n)=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n;};
  function ck(b,msg){if(!b)throw Error(msg);}
  function* perms(a){if(!a.length){yield [];return;}for(let i=0;i<a.length;i++)for(const z of perms(a.filter((_,j)=>i!==j)))yield [a[i],...z];}
  const tours=n=>[...perms(Array.from({length:n-1},(_,i)=>i+1))].map(t=>[0,...t]);
  function edges(t){return t.map((a,i)=>[a,t[(i+1)%t.length]]);}
  function pad(M,n,one=1){const k=M.length;if(k===n)return M.map(r=>r.slice());let Z=Array.from({length:n},()=>Array(n).fill(0));for(let i=1;i<k;i++){for(let j=0;j<k;j++)if(i!==j)Z[i][j]=M[i][j];Z[n-1][i]=M[0][i];}Z[0][k]=one;for(let j=k;j<n-1;j++)Z[j][j+1]=one;return Z;}
  function contract(M,j){let ids=Array.from({length:M.length},(_,i)=>i).filter(i=>i!==j);return ids.map(a=>ids.map(b=>a===b?0:M[a===0?j:a][b]));}
  function cycleFromSucc(s){let seen=new Set(),i=0;while(!seen.has(i)&&i>=0&&i<s.length){seen.add(i);i=s[i];}return i===0&&seen.size===s.length;}
  function support(M){return tours(M.length).filter(t=>edges(t).every(([i,j])=>M[i][j]!==0));}
  // A: exhaustive structural bijection, no arithmetic.
  let padCases=0,contractCases=0;
  for(let n=2;n<=7;n++)for(let k=2;k<=n;k++){let M=Array.from({length:k},(_,i)=>Array.from({length:k},(_,j)=>+(i!==j)));let actual=support(pad(M,n)).map(t=>t.filter(i=>i<k).join(",")).sort();let expect=tours(k).map(t=>t.join(",")).sort();ck(JSON.stringify(actual)===JSON.stringify(expect),"padding");padCases+=actual.length;}
  for(let n=3;n<=7;n++){const all=tours(n);for(let j=1;j<n;j++){const ids=Array.from({length:n},(_,i)=>i).filter(i=>i!==j);const actual=all.filter(t=>t[1]===j).map(t=>t.filter(i=>i!==j).map(i=>ids.indexOf(i)).join(",")).sort();ck(JSON.stringify(actual)===JSON.stringify(tours(n-1).map(t=>t.join(",")).sort()),"contract");contractCases+=actual.length;}}
  out.A={padCases,contractCases,reference_max_n:7};
  // B: exact candidate gate arrays, separate from tour enumeration via dynamic path recursion.
  function circuit(n){let G=[],input=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>{G.push(["x",i,j]);return G.length-1;}));function op(k,a,b){G.push([k,a,b]);return G.length-1;}let memo=new Map();function paths(i,mask){let key=i+":"+mask;if(memo.has(key))return memo.get(key);if(!mask)return input[i][0];let t=-1;for(let j=1;j<n;j++)if(mask&(1<<j)){let u=op("*",input[i][j],paths(j,mask^(1<<j)));t=t===-1?u:op("+",t,u);}memo.set(key,t);return t;}let root=paths(0,(1<<n)-2);return {G,root,input};}
  function field(p,quad){let mod=x=>((x%p)+p)%p;if(!quad)return {p,q:p,add:(a,b)=>mod(a+b),neg:a=>mod(-a),mul:(a,b)=>mod(a*b)};let [u,v]=quad;return {p,q:p*p,add:(a,b)=>mod(a%p+b%p)+p*mod((a/p|0)+(b/p|0)),neg:a=>mod(-(a%p))+p*mod(-(a/p|0)),mul:(a,b)=>{let x=a%p,y=a/p|0,z=b%p,w=b/p|0;return mod(x*z-v*y*w)+p*mod(x*w+y*z-u*y*w);}};}
  let gateEvals=0;function evalC(C,M,F){let a=[];for(const [op,i,j] of C.G){gateEvals++;a.push(op==="x"?M[i][j]:op==="+"?F.add(a[i],a[j]):F.mul(a[i],a[j]));}return a[C.root];}
  function discrepancy(C,M,F){let k=M.length,n=C.input.length,a=evalC(C,pad(M,n),F);let b=0;if(k===2)b=F.mul(M[0][1],M[1][0]);else for(let j=1;j<k;j++)b=F.add(b,F.mul(M[0][j],evalC(C,pad(contract(M,j),n),F)));return F.add(a,F.neg(b));}
  function reference(M,F){let total=0;for(const t of tours(M.length)){let v=1;for(const [i,j] of edges(t))v=F.mul(v,M[i][j]);total=F.add(total,v);}return total;}
  let rec=0,evalChecks=0,counts=0;for(let n=2;n<=7;n++){let C=circuit(n);for(const p of [2,3,101]){let F=field(p);for(let k=2;k<=n;k++)for(let r=0;r<16;r++){let M=Array.from({length:k},(_,i)=>Array.from({length:k},(_,j)=>i===j?0:rand(p)));ck(evalC(C,pad(M,n),F)===reference(M,F),"eval");evalChecks++;ck(discrepancy(C,M,F)===0,"recurrence");rec++;}}}
  // All n=4 graphs: actual edge-index witness counts vs circuit in F101, no modular wrap here.
  let n=4,C=circuit(n),F=field(101),ids=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)ids.push([i,j]);let yes=0,no=0;for(let mask=0;mask<1<<ids.length;mask++){let M=Array.from({length:n},()=>Array(n).fill(0));ids.forEach(([i,j],t)=>M[i][j]=(mask>>t)&1);let w=support(M);let v=evalC(C,M,F);ck(v===w.length,"mask count");counts++;if(w.length)yes++;else no++;}
  out.B={rec,evalChecks,counts,yes,no,gateEvals};
  // C: homogeneous base-field-invisible perturbation; actual gate circuit, not a value oracle.
  let baseChecks=0,extensionChecks=0,corruptions=[],booleanInvisible=0;
  function corrupt(C,p){let G=C.G.map(x=>x.slice());let x=C.input[0][1],y=C.input[1][0];function op(k,a,b){G.push([k,a,b]);return G.length-1;}let xp=x,yp=y;for(let i=1;i<p;i++){xp=op("*",xp,x);yp=op("*",yp,y);}let a=op("*",xp,y),b=op("*",x,yp),neg=b;for(let i=1;i<p-1;i++)neg=op("+",neg,b);let root=op("+",C.root,op("+",a,neg));return {G,root,input:C.input};}
  for(const [p,quad] of [[2,[1,1]],[3,[0,1]],[5,[0,3]]]){let n=p+1,F=field(p),K=field(p,quad),C=circuit(n),bad=corrupt(C,p);for(let a=0;a<p;a++)for(let b=0;b<p;b++){let M=Array.from({length:n},()=>Array(n).fill(0));M[0][1]=a;M[1][0]=b;ck(evalC(C,M,F)===evalC(bad,M,F),"base invisible");baseChecks++;if(a<2&&b<2)booleanInvisible++;}let M=Array.from({length:n},()=>Array(n).fill(0));M[0][1]=p;M[1][0]=1;let good=discrepancy(C,M,K),wrong=discrepancy(bad,M,K);ck(good===0&&wrong!==0,"extension catches");extensionChecks++;corruptions.push({p,n,quadratic:quad,alpha:p,baseTest:"all a,b",badDiscrepancy:wrong,goodDiscrepancy:good,smallerProjectionCorruptionZero:true});}
  out.C={baseChecks,booleanInvisible,extensionChecks,corruptions};
  // Integrated: verify imported projection and extension certificate on identical candidate/IDs.
  let verified=0;for(const q of corruptions){let C=circuit(q.n),bad=corrupt(C,q.p),K=field(q.p,q.quadratic),M=Array.from({length:q.n},()=>Array(q.n).fill(0));M[0][1]=q.alpha;M[1][0]=1;let smaller=Array.from({length:q.n-1},(_,i)=>Array.from({length:q.n-1},(_,j)=>i===j?0:(i+j+1)%K.q));ck(evalC(bad,pad(smaller,q.n),K)===evalC(C,pad(smaller,q.n),K),"projection");ck(discrepancy(bad,M,K)===q.badDiscrepancy,"cert replay");verified++;}
  out.integrated={verified,scope:"bad candidate only, not graph UNSAT",totalGateEvals:gateEvals};
  // Controls: exact PM decision, entire-HC witness check, affine/equality compact products, native one-edge neighbors.
  let pm=0,pmEven=0;const pp=[...perms([0,1,2])];for(let mask=0;mask<512;mask++){let cnt=pp.filter(t=>t.every((j,i)=>(mask>>(3*i+j))&1)).length;let lap=0;for(let j=0;j<3;j++)if((mask>>j)&1){let c=[0,1,2].filter(i=>i!==j);lap+=((mask>>(3+c[0]))&1)*((mask>>(6+c[1]))&1)+((mask>>(3+c[1]))&1)*((mask>>(6+c[0]))&1);}ck(cnt===lap,"PM recurrence");pm++;if(cnt>0&&cnt%2===0)pmEven++;}
  let pairs=[];for(const n of [8,16,32,64,128,256]){let s=Array.from({length:n},(_,i)=>(i+1)%n);ck(cycleFromSucc(s),"cycle");s[n-1]=-1;ck(!cycleFromSucc(s),"deleted edge empty row");pairs.push(n);}
  let equality=0,affine=0;for(let k=1;k<=7;k++){for(let x=0;x<1<<k;x++)for(let y=0;y<1<<k;y++){let v=1;for(let i=0;i<k;i++)v*=+(((x>>i)&1)===((y>>i)&1));ck(v===+(x===y),"equality");equality++;}for(let x=0;x<1<<k;x++){let parity=0;for(let i=0;i<k;i++)parity^=(x>>i)&1;ck(parity===x.toString(2).split("1").length%2^1,"affine");affine++;}}
  out.controls={pm,pmEven,pairs,equality,affine};return out;
}
console.log(JSON.stringify(audit(),null,2));
