// C02-07 independent exact enumeration of all guarded L/U pair cases and actual 80-tuple obstruction.
const fixture={"source_triples":[[0,0,8],[16,8,1],[16,8,8],[1,8,8],[16,0,1],[3,0,9],[17,9,0],[17,9,9],[2,9,9],[17,0,0],[4,1,10],[18,10,0],[18,10,10],[5,10,10],[18,1,0],[7,1,11],[19,11,1],[19,11,11],[6,11,11],[19,1,1],[3,12,13],[20,2,3],[20,13,12],[20,12,13],[0,13,12],[8,14,15],[21,2,2],[21,15,14],[21,14,15],[5,15,14],[7,16,17],[22,3,2],[22,17,16],[22,16,17],[4,17,16],[6,18,19],[23,3,3],[23,19,18],[23,18,19],[1,19,18],[8,4,20],[24,20,5],[24,20,20],[9,20,20],[24,4,5],[11,4,21],[25,21,4],[25,21,21],[10,21,21],[25,4,4],[12,5,22],[26,22,4],[26,22,22],[13,22,22],[26,5,4],[15,5,23],[27,23,5],[27,23,23],[14,23,23],[27,5,5],[11,24,25],[28,6,7],[28,25,24],[28,24,25],[2,25,24],[10,26,27],[29,6,6],[29,27,26],[29,26,27],[13,27,26],[15,28,29],[30,7,6],[30,29,28],[30,28,29],[12,29,28],[14,30,31],[31,7,7],[31,31,30],[31,30,31],[9,31,30]],"n":32,"regions":[[0,[1,0,0,1],[0,1,2,3,4]],[0,[2,3,0,0],[5,6,7,8,9]],[0,[5,4,1,0],[10,11,12,13,14]],[0,[6,7,1,1],[15,16,17,18,19]],[1,[0,3,2,3],[20,21,22,23,24]],[1,[5,8,2,2],[25,26,27,28,29]],[1,[4,7,3,2],[30,31,32,33,34]],[1,[1,6,3,3],[35,36,37,38,39]],[0,[9,8,4,5],[40,41,42,43,44]],[0,[10,11,4,4],[45,46,47,48,49]],[0,[13,12,5,4],[50,51,52,53,54]],[0,[14,15,5,5],[55,56,57,58,59]],[1,[2,11,6,7],[60,61,62,63,64]],[1,[13,10,6,6],[65,66,67,68,69]],[1,[12,15,7,6],[70,71,72,73,74]],[1,[9,14,7,7],[75,76,77,78,79]]],"supports":[[0,0,0,0],[0,0,1,0],[0,0,1,1],[0,1,0,0],[0,1,1,0],[0,1,1,1],[1,0,0,1],[1,1,0,0],[1,1,1,0],[1,1,1,1]],"majority_inputs":[[0,0,0,0],[0,0,1,1],[1,0,0,1]],"majority":[0,0,0,1],"source_witness_ids":[[3,4,7,13,14,17,20,21,24,25,27,30,31,34,35,37,43,44,47,53,54,57,60,61,64,65,67,70,71,74,75,77],[3,4,7,13,14,17,20,21,24,25,27,30,31,34,35,37,42,45,46,52,55,56,63,64,65,66,69,73,74,75,76,79],[2,8,9,12,18,19,20,21,24,28,29,30,31,34,38,39,40,41,47,50,51,57,60,62,65,66,69,70,72,75,76,79]]};
const audit=(F)=>{
let checks=0;const ok=(v)=>{checks++;if(!v)throw Error("failed "+checks)};
const L=[0,13,14],U=[1,2,15],sub=a=>Array.from({length:7},(_,m)=>a.filter((_,i)=>((m+1)>>i)&1));
let cases=0,wordCases=0,zeroDrift=0;
for(const [A,B] of [[L,U],[U,L]])for(const R of sub(A))for(const S of sub(B))for(const sa of [0,1])for(const sb of [0,1]){
  cases++;
  for(let z=0;z<2;z++){
    let x=R.filter(m=>(m>>2&1)===z),y=S.filter(m=>(m>>2&1)===(1-z));
    for(let a of x)for(let b of y){
      let incoming=1-((a>>sa)&1),internal=(a>>(1-sa))&1,secondIn=(b>>sb)&1,out=(b>>(1-sb))&1;
      if(internal+secondIn!==1)continue;
      ok(incoming===out);zeroDrift++;
    }
    for(let e=0;e<2;e++){
      const direct=x.some(a=>y.some(b=>(1-((a>>sa)&1))===e&&((b>>(1-sb))&1)===e&&((a>>(1-sa))&1)+((b>>sb)&1)===1));
      let q=false;
      for(let t=0;t<2;t++){
        let am=((1-e)<<sa)|(t<<(1-sa))|(z?12:0),bm=((1-t)<<sb)|(e<<(1-sb))|(!z?12:0);
        if(R.includes(am)&&S.includes(bm))q=true;
      }
      ok(direct===q);wordCases++;
    }
  }
}
const T=F.source_triples,n=F.n,R=F.regions;
const owner=(c,x)=>c*n+x;const Trows=T.map(t=>t.map((x,c)=>owner(c,x)));const witness=W=>{let count=Array(3*n).fill(0);for(const i of W)for(const v of Trows[i])count[v]++;return count.every(x=>x===1)};
const tab=[];
for(const [e,ps,ids] of R){
 let ports=ps.map((x,i)=>owner([0,0,1,2][i],x));let privateO=new Set(ids.flatMap(i=>Trows[i]).filter(u=>!ports.includes(u)));let M=new Map();
 for(let b=0;b<2**ids.length;b++){
   const W=ids.filter((_,i)=>(b>>i)&1),v=W.flatMap(i=>Trows[i]),S=new Set(v);
   if(v.length!==S.size||[...privateO].some(u=>!S.has(u)))continue;
   let m=ports.reduce((a,u,j)=>a+(S.has(u)?2**j:0),0);ok(!M.has(m));M.set(m,W);
 }
 ok(JSON.stringify([...M.keys()].sort((a,b)=>a-b))===JSON.stringify(e?U:L));tab.push(M);
}
// Independently derive BC complement graph and assign each component's gauge by first witness.
const adj=R.map(()=>[]),oc=new Map();
for(let i=0;i<R.length;i++)for(let p=2;p<=3;p++){
 const k=owner(p-1,R[i][1][p]);if(!oc.has(k))oc.set(k,[]);oc.get(k).push(i);
}
for(const s of oc.values()){ok(s.length===2);adj[s[0]].push(s[1]);adj[s[1]].push(s[0])}
let comp=R.map(()=>-1),sgn=R.map(()=>-1),k=0;
const W0=new Set(F.source_witness_ids[0]);
for(let i=0;i<R.length;i++)if(comp[i]<0){let m=[...tab[i]].find(([m,w])=>w.every(t=>W0.has(t)))[0];comp[i]=k;sgn[i]=(m>>2)&1;let Q=[i];
while(Q.length){let v=Q.pop();for(let u of adj[v]){if(comp[u]<0){comp[u]=k;sgn[u]=sgn[v]^1;Q.push(u)}else ok(sgn[u]!==sgn[v]&&comp[u]===k)}}k++}
ok(k===4);
let support=[],nativeJoinTests=0;
for(let word=0;word<16;word++){
  let b=Array.from({length:4},(_,i)=>(word>>(3-i))&1),options=R.map((r,i)=>[...tab[i]].filter(([m,w])=>(m>>2&1)===(b[comp[i]]^sgn[i])));
  function visit(i,used,W){nativeJoinTests++;if(i===R.length){ok(witness(W));return W;}
     for(const [m,w] of options[i]){let a=[0,1].filter(j=>(m>>j)&1).map(j=>R[i][1][j]);if(a.some(x=>used.has(x)))continue;
       let ans=visit(i+1,new Set([...used,...a]),[...W,...w]);if(ans)return ans;}return null;
  }
  let w=visit(0,new Set(),[]);if(w)support.push(b);
}
ok(JSON.stringify(support)===JSON.stringify(F.supports));
for(let j=0;j<3;j++){
 let W=F.source_witness_ids[j];ok(witness(W));const Wset=new Set(W);
 for(let i=0;i<R.length;i++){let m=[...tab[i]].find(([m,w])=>w.every(t=>Wset.has(t)))[0];ok(((m>>2&1)^sgn[i])===F.majority_inputs[j][comp[i]]);}
}
const M=F.majority_inputs[0].map((_,i)=>+(F.majority_inputs.reduce((a,w)=>a+w[i],0)>=2));ok(JSON.stringify(M)===JSON.stringify(F.majority));ok(!support.some(w=>JSON.stringify(w)===JSON.stringify(M)));
return {checks,localGuardedPairCases:cases,pairedWordTests:wordCases,compatiblePairZeroDriftChecks:zeroDrift,nativeJoinTests,nativeSupport:support,majority:M};
};
console.log(JSON.stringify(audit(fixture),null,2));
