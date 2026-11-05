// LSPV-3/414: standalone no-dependency semantic checker.
// Node usage: node experiments/arc/lspv3_414_native_gf2_affine_checker.js
function runCheck(){
 let checks=0; const yes=(v,s)=>{checks++;if(!v)throw Error('FAIL: '+s);};
 const U=n=>Array.from({length:1<<n},(_,m)=>Array.from({length:n},(_,i)=>(m>>i)&1));
 const lit=(l,a)=>l>0?Boolean(a[l-1]):!Boolean(a[-l-1]);
 const cl=(c,a)=>c.some(l=>lit(l,a));
 const av=(code,a)=>{let b=(code>>a.length)&1;for(let i=0;i<a.length;i++)b^=a[i]&((code>>i)&1);return b;};
 const vs=U(2),F=[[1],[-2],[1,2]],M=vs.filter(a=>F.every(c=>cl(c,a)));
 yes(M.length===1&&M[0][0]===1&&M[0][1]===0,'proper SAT source');
 let old=[],altered=[];
 for(const a of vs){
  const f0=cl([1],a)&&cl([1,2],a),f1=cl([1],a)&&cl([-2],a);
  const p=cl([1,2],a),q=cl([1,-2],a),qp=cl([-2],a);
  yes(f0===Boolean(a[0]),'AND3 n0');yes(!f1||p,'LOCAL P');
  yes(!f1||q,'LOCAL Q');yes(!f1||qp,'replacement LOCAL Qprime');
  yes((p&&q)===Boolean(a[0]),'AND3 n4');yes((av(5,a)===0)===(p&&q),'GF2 n4');
  yes((av(5,a)^av(5,a))===0,'XOR n5');
  if(F.every(c=>cl(c,a)))yes(q===qp,'same-source port equivalence');
  old.push(Number(p&&q));altered.push(Number(p&&qp));
 }
 yes(old.join('')==='0101'&&altered.join('')==='0100','factor truth tables');
 yes(!Array.from({length:8},(_,i)=>i).some(r=>vs.every((a,j)=>Number(av(r,a)===0)===altered[j])),'no affine row for new factor');
 const hist={};
 for(const n of [2,3]){
  const vals=U(n),functions=1<<(n+1),h={},limit=1<<vals.length;
  for(let m=0;m<limit;m++){
   const models=vals.filter((_,j)=>m&(1<<j));
   // Compute translated affine span by XOR closure, independently of row kernels.
   let span=new Set([0]);
   if(models.length) for(const a of models.slice(1)){
    const diff=a.reduce((sum,b,i)=>sum|((b^models[0][i])<<i),0);
    span=new Set([...span,...[...span].map(z=>z^diff)]);
   }
   const d=models.length?n-Math.log2(span.size):n+1;
   const kernel=[];
   for(let r=0;r<functions;r++)if(models.every(a=>av(r,a)===0))kernel.push(r);
   yes(kernel.length===(1<<d),'affine dimension');
   h[d]=(h[d]||0)+1;
   for(let p=0;p<functions;p++)for(let q=0;q<functions;q++)
    yes(models.every(a=>av(p,a)===av(q,a))===kernel.includes(p^q),'affine coset');
  }
  hist[n]=h;
 }
 const bank=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
 for(let mask=0;mask<256;mask++){
  const G=bank.filter((_,j)=>mask&(1<<j)),S=G.map(c=>[3,...c]);
  const sat=vs.some(a=>G.every(c=>cl(c,a))),gm=U(3).filter(a=>S.every(c=>cl(c,a)));
  yes(gm.some(a=>a[2]===1),'guarded SAT promise');
  yes(gm.every(a=>a[2]===1)===!sat,'guarded reduction');
 }
 return {status:'PASS',checks,strict_source_models:M,old_table:old,new_table:altered,dimension_histograms:hist,guard_reductions:256};
}
if(typeof process!=='undefined')console.log(JSON.stringify(runCheck(),null,2));
