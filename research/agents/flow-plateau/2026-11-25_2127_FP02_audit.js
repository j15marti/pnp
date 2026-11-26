// FP02 independent gadget enumeration and source-authenticated staged lifts. Node.js, no dependencies.
// Source(k) is EXPONENTIAL reference backtracking, not a polynomial repair algorithm.
console.log(JSON.stringify((function audit(){
const E=[[2,3],[2,7],[3,4],[3,8],[4,9],[5,7],[5,8],[6,8],[6,9],[7,9]], P=[4,5,2,6];
const W=new Map();let states=0;
function gadget(s){
 let sum=Array(10).fill(0),left=Array(10).fill(0),out=[],best=11,word;
 for(const [u,v] of E){left[u]++;left[v]++} P.forEach((v,i)=>sum[v]^=s[i]);
 function rec(i,zeros){if(zeros>=best)return;if(i===E.length){if(sum.every(x=>!x)){best=zeros;word=out.slice()}return}
 const [u,v]=E[i];left[u]--;left[v]--;
 for(let c=0;c<4;c++){states++;sum[u]^=c;sum[v]^=c;out[i]=c;if((left[u]||!sum[u])&&(left[v]||!sum[v]))rec(i+1,zeros+(c===0));sum[u]^=c;sum[v]^=c}left[u]++;left[v]++;
 }rec(0,0);return {best,word};
}
let counts={};
for(let a=1;a<=3;a++)for(let b=1;b<=3;b++)for(let c=1;c<=3;c++)for(let d=1;d<=3;d++){let s=[a,b,c,d];if(a^b^c^d)continue;let r=gadget(s);if(r.best!==((a===b&&c===d)?0:1))throw Error("gadget");W.set(s.join(","),r.word);counts[r.best]=(counts[r.best]||0)+1}
const permutations=[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]];
function test(name,n,edges){
 const inc=Array.from({length:n},()=>[]);edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});if(inc.some(x=>x.length!==3))throw Error("degree");
 function source(k){const q=Array(n).fill(null);function rec(v){if(v===n)return q.map(x=>x.slice());for(const x of permutations){let ok=true;for(let j=0;j<3;j++){const i=inc[v][j],[a,b]=edges[i],u=a===v?b:a;if(i<k&&q[u]&&q[u][inc[u].indexOf(i)]!==x[j])ok=false}if(ok){q[v]=x;const r=rec(v+1);if(r)return r;q[v]=null}}return null}return rec(0)}
 // Compile stage on halfedge colors from a solution of stage k or k-1.
 function compile(k,q){const G=[],color=(u,i)=>q[u][inc[u].indexOf(i)],add=(u,v,c)=>G.push([u,v,c]);let V=2*n;
 edges.forEach(([u,v],i)=>{const a=color(u,i),b=color(v,i);
 if(i<k){let t=V;V+=8;const id=x=>t+x-2;const s=[a,b,a,b];E.forEach(([x,y],j)=>add(id(x),id(y),W.get(s.join(","))[j]));[u,v,n+u,n+v].forEach((x,j)=>add(x,id(P[j]),s[j]));}
 else for(const [x,c] of [[u,a],[v,b]]){let t=V;V+=4;let d=c===1?2:1,e=c^d;add(x,t,c);add(n+x,t+1,c);add(t,t+2,d);add(t+1,t+3,d);add(t,t+3,e);add(t+1,t+2,e);add(t+2,t+3,c);}
 });
 const degree=Array(V).fill(0),sum=Array(V).fill(0),seen=new Set();let zeros=0;for(const [u,v,c] of G){let key=[Math.min(u,v),Math.max(u,v)].join(",");if(u===v||seen.has(key))throw Error("not simple");seen.add(key);degree[u]++;degree[v]++;sum[u]^=c;sum[v]^=c;zeros+=c===0}if(degree.some(x=>x!==3)||sum.some(Boolean))throw Error("invalid flow");return {V,zeros};}
 let q=source(0),repairs=0,stages=0,firstFailure=null,largest=0;
 if(compile(0,q).zeros!==0)throw Error("initial");
 for(let k=1;k<=edges.length;k++){let r=compile(k,q);largest=Math.max(largest,r.V);if(r.zeros>1)throw Error("repair bound");repairs+=r.zeros;stages++;const p=source(k);if(!p){if(r.zeros!==1)throw Error("failure without defect");firstFailure=k;break}if(compile(k,p).zeros!==0)throw Error("lift");q=p}
 return {name,stages,repairs,firstFailure,largest,sourceSAT:!!source(edges.length)};
}
const k4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const prism=k=>[...Array.from({length:k},(_,i)=>[i,(i+1)%k]),...Array.from({length:k},(_,i)=>[k+i,k+(i+1)%k]),...Array.from({length:k},(_,i)=>[i,k+i])];
const pet=[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i+5,(i+2)%5+5]),...Array.from({length:5},(_,i)=>[i,i+5])];
let tests=[test("K4",4,k4),test("triangular prism",6,prism(3)),test("cube",8,prism(4)),test("pentagonal prism",10,prism(5)),test("Petersen",10,pet)];
return {balancedBoundaryWords:W.size,counts,states,tests};
})(),null,2));
