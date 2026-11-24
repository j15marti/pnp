function run(){
 let seed=241110,stats={random:0,queries:0,sat:0,unsat:0,referenceChecks:0,closureScans:0,deletions:0,nodes:0,greedyWitnesses:0,starQueries:0,starSat:0,starUnsat:0,sourceWords:0,sourceLifts:0,liftEdges:0,kempeChecks:0,starScales:[],k5:[],fano:[]};
 function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)}
 function assert(x){if(!x)throw Error("assertion")}
 function verify(E,x){return E.every(([u,v,s])=>(x[u]^x[v])!==s)}
 function solve(n,E,pins={}){
   function visit(D){
    stats.nodes++;
    for(;;){stats.closureScans++;let change=false;
      for(const [u,v,s] of E)for(const [a,b] of [[u,v],[v,u]])if(D[b]&&(D[b]&(D[b]-1))===0){let z=31-Math.clz32(D[b]),m=D[a]&~(1<<(z^s));if(m!==D[a]){D[a]=m;stats.deletions++;change=true;if(!m)return null;break}} 
      if(D.some(m=>!m))return null;if(!change)break;
    }
    let i=D.findIndex(m=>(m&(m-1))!==0);
    if(i<0){const x=D.map(m=>31-Math.clz32(m));assert(verify(E,x));return x;}
    for(let a=0;a<4;a++)if(D[i]&(1<<a)){let C=D.slice();C[i]=1<<a;let w=visit(C);if(w)return w;}return null;
   }
   let D=Array(n).fill(15);for(const [i,a] of Object.entries(pins))D[i]=1<<a;return visit(D);
 }
 function brute(n,E,pins){for(let z=0;z<4**n;z++){stats.referenceChecks++;let x=Array.from({length:n},(_,i)=>(z>>>(2*i))&3);if(Object.entries(pins).every(([i,a])=>x[i]===a)&&verify(E,x))return true;}return false;}
 function deg(n,E){let d=Array(n).fill(0);for(const [u,v] of E){d[u]++;d[v]++;}return d;}
 function comps(n,E,skip=new Set()){let a=Array.from({length:n},()=>[]);for(const [u,v] of E)if(!skip.has(u)&&!skip.has(v)){a[u].push(v);a[v].push(u)}let seen=new Set(skip),C=[];for(let i=0;i<n;i++)if(!seen.has(i)){let q=[i];seen.add(i);for(let j=0;j<q.length;j++)for(const v of a[q[j]])if(!seen.has(v)){seen.add(v);q.push(v)}C.push(q)}return C;}
 function greedy(n,E,ports,u,v,d){let F=E.concat([[u,v,d]]),D=deg(n,F);if(D.some(x=>x>4))return;let C=comps(n,F);if(C.length!==1)return;let root=D.findIndex(x=>x<4);if(root<0)return;let q=[root],seen=new Set(q);for(let i=0;i<q.length;i++)for(const [a,b] of F){let w=a===q[i]?b:b===q[i]?a:-1;if(w>=0&&!seen.has(w)){seen.add(w);q.push(w)}}let x=Array(n).fill(-1);for(const i of q.reverse()){for(let c=0;c<4;c++){if(F.every(([a,b,s])=>a===i?x[b]<0||(c^x[b])!==s:b===i?x[a]<0||(c^x[a])!==s:true)){x[i]=c;break}}assert(x[i]>=0)}assert(verify(F,x));stats.greedyWitnesses++;}
 function kempe(n,E,x,ports){for(let d=1;d<4;d++){let C=comps(n,E.filter(([u,v,s])=>(x[u]^x[v]^s)===d));assert(C.some(c=>ports.every(p=>c.includes(p))));stats.kempeChecks++;}}
 function wheel(E,a,b,r,offset){for(let i=0;i<3;i++){E.push([r+i,r+(i+1)%3,0],[a,r+i,0],[b,r+i,offset]);}}
 function star(p){let E=[],off=Array.from({length:p},(_,i)=>i%4);for(let i=0;i<p;i++)wheel(E,0,i+1,p+1+3*i,off[i]);return {n:1+4*p,E,off,ports:Array.from({length:p},(_,i)=>i+1)};}
 function liftStar(S,c){let x=Array(S.n).fill(-1);x[0]=c;for(let i=0;i<S.off.length;i++){x[i+1]=c^S.off[i];let z=[0,1,2,3].filter(a=>a!==c);for(let j=0;j<3;j++)x[S.off.length+1+3*i+j]=z[j];}assert(verify(S.E,x));stats.liftEdges+=S.E.length;return x;}
 for(let t=0;t<140;t++){let n=4+rnd(3),E=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(rnd(100)<45)E.push([i,j,rnd(4)]);let D=deg(n,E),P=Array.from({length:n},(_,i)=>i).filter(i=>D[i]<=3).slice(0,3);if(P.length<3)continue;stats.random++;
  let support=[];for(let a=0;a<4;a++)for(let b=0;b<4;b++){let pins={[P[0]]:0,[P[1]]:a,[P[2]]:b};let w=solve(n,E,pins);assert(!!w===brute(n,E,pins));stats.queries++;if(w){stats.sat++;support.push([a,b,w]);}else stats.unsat++;}
  if(support.length===1){let H=new Set(D.map((d,i)=>d>4?i:-1).filter(i=>i>=0));assert(H.size>0);let C=comps(n,E,H);assert(C.every(c=>c.filter(i=>P.includes(i)).length<=1));let cut=E.filter(([u,v])=>H.has(u)!==H.has(v)).length;assert(cut>=9);kempe(n,E,support[0][2],P);}
  if(D.every(x=>x<=4)&&comps(n,E).length===1)for(let d=0;d<4;d++)greedy(n,E,P,P[0],P[1],d);
 }
 for(const p of [2,3,4,8,16,32,64]){let S=star(p),D=deg(S.n,S.E),H=new Set(D.map((d,i)=>d>4?i:-1).filter(i=>i>=0));let x=liftStar(S,0);kempe(S.n,S.E,x,S.ports);
   if(p>=3){let C=comps(S.n,S.E,H);assert(C.filter(c=>c.some(i=>S.ports.includes(i))).length===p);assert(S.E.filter(([u,v])=>H.has(u)!==H.has(v)).length===3*p);}
   if(p<=4){for(let z=0;z<4**(p-1);z++){let pins={1:S.off[0]};for(let i=1;i<p;i++)pins[i+1]=(z>>>(2*(i-1)))&3;let expected=S.ports.every((v,i)=>pins[v]===S.off[i]);let w=solve(S.n,S.E,pins);assert(!!w===expected);stats.starQueries++;if(w)stats.starSat++;else stats.starUnsat++;}}
   stats.starScales.push({ports:p,vertices:S.n,edges:S.E.length,deficient:H.size,excess:D.reduce((s,d)=>s+Math.max(0,d-4),0)});
 }
 // Exact source projection and constructive sharded lift for K5 and all deletion neighbors.
 let E0=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)E0.push([i,j,0]);
 for(let omit=-1;omit<10;omit++){let E=E0.filter((_,i)=>i!==omit),F=[],next=5,ports=[];for(const [u,v,s] of E){let a=next++,b=next++,r=next;next+=3;wheel(F,u,a,r,0);r=next;next+=3;wheel(F,v,b,r,0);F.push([a,b,s]);ports.push([u,v,a,b,r-3,r]);}
   let count=0;for(let z=0;z<1024;z++){stats.sourceWords++;let x=Array.from({length:5},(_,i)=>(z>>>(2*i))&3);if(!verify(E,x))continue;count++;let y=Array(next).fill(-1);x.forEach((v,i)=>y[i]=v);for(const [u,v,a,b,r,t] of ports){y[a]=x[u];y[b]=x[v];[0,1,2,3].filter(c=>c!==x[u]).forEach((c,i)=>y[r+i]=c);[0,1,2,3].filter(c=>c!==x[v]).forEach((c,i)=>y[t+i]=c);}assert(verify(F,y));stats.sourceLifts++;stats.liftEdges+=F.length;}
   assert(count===(omit<0?0:24));stats.k5.push({omit,count,vertices:next,edges:F.length});
 }
 const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];for(let omit=-1;omit<14;omit++){let count=0;for(let x=0;x<128;x++){let ok=true;for(let i=0;i<7;i++)for(let b=0;b<2;b++)if(2*i+b!==omit&&triples[i].every(v=>((x>>v)&1)===b))ok=false;if(ok)count++;}assert(count===(omit<0?0:5));stats.fano.push(count);}
 return stats;
}
console.log(JSON.stringify(run(),null,2));
