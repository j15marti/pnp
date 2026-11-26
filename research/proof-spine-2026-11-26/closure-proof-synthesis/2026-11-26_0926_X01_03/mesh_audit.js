function meshAudit(){
let checks=0;const ok=(v,m)=>{checks++;if(!v)throw Error(m||"check "+checks)};let seed=9272026;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
const G=[[0,2,1],[1,2,0],[2,0,1]],R=[0,2,1],A3=[[1,1,1],[1,0,1],[1,1,0]];
function run(k){
 const z=k*k,a=z+1,b=z+2,V=b+1,F=[],edge=new Map(),add=(u,v)=>{edge.set(`${Math.min(u,v)},${Math.max(u,v)}`,F.length);F.push([u,v,z].map(x=>x+1))};
 for(let i=0;i<k;i++)for(let j=0;j<k;j++){let u=i*k+j;if(i+1<k)add(u,u+k);if(j+1<k)add(u,u+1)}
 let base=F.length;for(let p=0;p<8;p++)F.push([a,b,z].map((x,i)=>(p>>i&1?1:-1)*(x+1)));
 const U=F.map(x=>x.slice()),Y=F.map(x=>x.slice());Y[base][0]*=-1;
 // Guard-class vertices x_v and s_{c,j}; matching blocks V variable + 4 per clause.
 const B=V+4*F.length,h=V+3*F.length,P=Array.from({length:B},()=>[]);
 for(let v=0;v<V;v++)P[v].push(v);
 for(let c=0;c<F.length;c++){let S=V+4*c;for(let j=0;j<3;j++){let g=V+3*c+j;P[S].push(g);P[S+1+j].push(g,Math.abs(F[c][j])-1)}}
 let A=Array.from({length:B+h},()=>[]),par=A.map((_,i)=>i),K=new Set();
 function rt(x){while(par[x]!==x){par[x]=par[par[x]];x=par[x]}return x}
 for(let i=0;i<B;i++)for(let g of P[i]){A[i].push(B+g);A[B+g].push(i);let u=rt(i),v=rt(B+g);if(u===v)K.add(g);else par[u]=v}
 const chosen=[];
 for(let i=0;i+1<k;i+=2)for(let j=0;j+1<k;j+=2){
   let cycle=[i*k+j,i*k+j+1,(i+1)*k+j+1,(i+1)*k+j],nodes=new Set();
   for(let t=0;t<4;t++){let u=cycle[t],v=cycle[(t+1)%4],c=edge.get(`${Math.min(u,v)},${Math.max(u,v)}`),S=V+4*c,p=F[c].indexOf(u+1),q=F[c].indexOf(v+1);
     let path=[B+u,S+1+p,B+V+3*c+p,S,B+V+3*c+q,S+1+q,B+v];for(let j=0;j+1<path.length;j++)ok(A[path[j]].includes(path[j+1]));for(let x of path)nodes.add(x)
   }
   let candidates=[...nodes].filter(x=>x>=B&&K.has(x-B));ok(candidates.length>0);chosen.push(candidates[0]-B)
 }
 ok(new Set(chosen).size===chosen.length);
 // distinct physical block neighborhoods for the chosen direction from each disjoint square
 let used=new Set();for(let g of chosen){for(let owner of A[B+g]){ok(!used.has(owner));used.add(owner)}}
 function core(F){let out=[];for(let p=0;p<8;p++){let vals=new Map([[a,p&1],[b,p>>1&1],[z,p>>2&1]]);if(F.slice(base).every(C=>C.some(l=>vals.get(Math.abs(l)-1)===(l>0?1:0))))out.push(vals)}return out}
 ok(core(U).length===0);ok(core(Y).length===1);ok(core(Y)[0].get(z)===1);
 let tests=chosen.length<=8?2**chosen.length:32;for(let p=0;p<tests;p++){
   let x=Array(V).fill(1),s=new Map(),word=chosen.map((_,i)=>chosen.length<=8?p>>i&1:rnd(2));chosen.forEach((g,i)=>{if(g<V)x[g]=word[i];else s.set(g,word[i])});
   let states=[];for(let v=0;v<V;v++)states.push(x[v]===1?0:1);
   for(let c=0;c<Y.length;c++){let lit=Y[c].map(l=>x[Math.abs(l)-1]^(l<0?1:0)),j=-1;for(let p=0;p<3;p++)if(s.get(V+3*c+p)===1)j=p;
     if(j<0)j=lit.findIndex((v,p)=>v===1&&s.get(V+3*c+p)!==0);ok(j>=0&&lit[j]===1);states.push(j);
     for(let p=0;p<3;p++){let a=+(j===p),b=1-lit[p],cbit=1-a-b;ok(cbit===0||cbit===1);states.push(a?0:b?1:2)}
   }
   // Verify all chosen guards and actual matching choices.
   let M=states.map((s,i)=>i<V?(s===0?[0,1]:[1,0]):G[s]);
   for(let c=0;c<Y.length;c++){let S=V+4*c;for(let p=0;p<3;p++){let I=S+1+p,lit=Y[c][p],v=Math.abs(lit)-1;
      let ss=+(M[S][R[p]]===0),aa=+(M[I][R[0]]===0),bb=+(M[I][R[1]]===0),xx=+(M[v][0]===0);ok(aa===ss&&bb===(xx^(lit>0?1:0)));
      ok(G[states[I]].every((j,i)=>A3[i][j]));
   }}
   chosen.forEach((g,i)=>{let val=g<V?x[g]:+(states[V+4*Math.floor((g-V)/3)]===(g-V)%3);ok(val===word[i])})
 }
 return {gridSide:k,formulaClauses:F.length,matchingGridSide:2*V+12*F.length,feedback:K.size,disjointCycles:chosen.length,minCandidateExponent:chosen.length,actualSATPatternChecks:tests,NOcore:true};
}
let scales=[2,4,6,8,12].map(run);return{checks,scales,seed:9272026,limits:"symbolic native grid construction; actual matching blocks and physical prefix guard bits checked, not every cell of the larger mesh grids; no exhaustive large UNSAT candidate enumeration"}
}
console.log(JSON.stringify(meshAudit(),null,2));
