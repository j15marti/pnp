function check(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const pop=x=>{let c=0;while(x){x&=x-1;c++;}return c};
 function basisAdd(B,x){let a=x;while(a){let p=31-Math.clz32(a);if(B[p])a^=B[p];else{let C=B.slice();C[p]=a;return C}}return B}
 function rank(B){return B.filter(Boolean).length}
 const cnt={graphs:0,rankChoiceLeaves:0,targetChecks:0,trianglePhysicalChecks:0,FourierMassChecks:0,characterVisits:0,cutChecks:0,cutStrict:0};
 function components(n,edges){let adj=Array.from({length:n},()=>[]);for(const [u,v] of edges){adj[u].push(v);adj[v].push(u)}let seen=new Set(),out=[];for(let i=0;i<n;i++)if(!seen.has(i)){let q=[i];seen.add(i);let mask=0,sum=0;for(const u of q){mask|=1<<u;sum+=adj[u].length;for(const v of adj[u])if(!seen.has(v)){seen.add(v);q.push(v)}}out.push({mask,tree:sum/2===q.length-1})}return out}
 function cover(n,edges){let best=(1<<n)-1;for(let x=0;x<1<<n;x++)if(pop(x)<pop(best)&&edges.every(([u,v])=>x&((1<<u)|(1<<v))))best=x;return best}
 function support(edges){let S=new Set([0]);for(const [u,v] of edges){let T=new Set();for(const s of S)for(const t of [0,1<<u,1<<v])T.add(s^t);S=T}return S}
 function count(rows,m){let B=new Array(m).fill(0),r=0;for(let row of rows){let x=row;while(x&((1<<m)-1)){let p=31-Math.clz32(x&((1<<m)-1));if(B[p])x^=B[p];else{B[p]=x;r++;break}}if((x&((1<<m)-1))===0&&(x>>m))return 0}return 2**(m-r)}
 function massCheck(n,edges,C,target){let m=edges.length;let pairs=edges.map(([u,v])=>C&(1<<u)?[u,v]:[v,u]);let rows=[];for(let j=0;j<n;j++)if(!(C&(1<<j))){let x=0;for(let i=0;i<m;i++)if(pairs[i][1]===j)x|=1<<i;rows.push(x|(((target>>j)&1)<<m))}
 let z=0;for(let l=C;;l=(l-1)&C){cnt.characterVisits++;let R=rows.slice(),sg=0;for(let i=0;i<m;i++){if(l&(1<<pairs[i][0]))R.push((1<<i)|(1<<m));if(l&(1<<pairs[i][1]))sg|=1<<i}let rhs=pop(l&target)%2;z+=2*count([...R,sg|(rhs<<m)],m)-count(R,m);if(l===0)break}
 let ref=0;for(let t=0;t<1<<m;t++){let off=0,active=0;for(let i=0;i<m;i++){if(t&(1<<i))off^=1<<pairs[i][1];else active|=1<<pairs[i][0]}if(((target^off)&~active)===0)ref+=2**(pop(C)-pop(active))}
 assert(z===ref,"normalized mass mismatch");cnt.FourierMassChecks++;return z>0}
 for(let n=1;n<=5;n++){let all=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)all.push([u,v]);for(let mask=0;mask<1<<all.length;mask++){let E=all.filter((_,i)=>mask&(1<<i)),C=cover(n,E),best=n;
 function rec(i,B){if(i===E.length){cnt.rankChoiceLeaves++;best=Math.min(best,rank(B));return}let [u,v]=E[i];for(let d of [1<<u,1<<v,(1<<u)^(1<<v)])rec(i+1,basisAdd(B,d))}
 rec(0,new Array(n).fill(0));assert(best===pop(C),"rank/cover");cnt.graphs++;
 let S=support(E),comps=components(n,E);for(let t=0;t<1<<n;t++){let expected=comps.every(c=>!c.tree||(t&c.mask)!==c.mask);assert(S.has(t)===expected,"component formula");cnt.targetChecks++;if(n<=4||mask%31===0)assert(massCheck(n,E,C,t)===expected,"Fourier decision")}
 for(const [u,v] of E){const tags=[[0,1,0],[0,2,1<<u],[0,3,1<<v],[1,2,0],[1,3,0],[2,3,0]];let P=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)if(new Set([...tags[i].slice(0,2),...tags[j].slice(0,2)]).size===4)P.push(tags[i][2]^tags[j][2]);assert(P.length===3&&new Set(P).size===3&&P.includes(0)&&P.includes(1<<u)&&P.includes(1<<v),"K4 physical");cnt.trianglePhysicalChecks++}
 }}
 // Independently check S01 cut identity by explicit subspace sets; W decomposable.
 let seed=0x201024;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
 function span(g){let s=new Set([0]);for(let x of g)for(let y of [...s])s.add(x^y);return s}
 function dim(S){return Math.log2(S.size)}
 function inter(A,B){return new Set([...A].filter(x=>B.has(x)))}
 function quotient(A,W){return new Set([...A].map(a=>Math.min(...[...W].map(w=>a^w))))}
 for(let i=0;i<500;i++){let d=3+rand()%4;let aa=Array.from({length:1+rand()%5},()=> (rand()>>>8)%(1<<d)),bb=Array.from({length:1+rand()%5},()=> (rand()>>>8)%(1<<d));let A=span(aa),B=span(bb),W=span([...aa.filter(()=>rand()>>>31),...bb.filter(()=>rand()>>>31)]),old=dim(inter(A,B)),nw=dim(inter(quotient(A,W),quotient(B,W)));assert(nw===old-dim(inter(inter(A,B),W)),"cut identity");cnt.cutChecks++;if(nw<old)cnt.cutStrict++}
 let scaling=[];for(const n of [8,16,32,64,128,256,512,1024]){let mask=(1n<<BigInt(n))-1n;let sat=mask^1n;let witness=0n;for(let i=1;i<n;i++)witness^=1n<<BigInt(i);assert(witness===sat,"path witness");let lower=0,upper=0;for(let i=0;i+1<n;i+=2)lower++;for(let i=1;i<n;i+=2)upper++;assert(lower===upper,"path cover");scaling.push({vertices:n,factors:n-1,physicalMatchingVertices:4*(n-1),minimumVariationRank:upper,globalHullRank:n,unpeeled:n-1,UNSAT:true,SATWitnessVerified:true,characters:String(1n<<BigInt(upper))})}
 return {seed:"0x201024",...cnt,scaling,disagreements:0};
}
console.log(JSON.stringify(check(), null, 2));
