// N4FN01. Run with node. No input decomposition hints are given to solve().
let seed=20261125,checks=0;
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function ck(x){checks++;if(!x)throw Error("assertion "+checks)}
function nae(c,x){return c.some(v=>x[v]!==x[c[0]])}
class DSU{
 constructor(n){this.p=Array.from({length:n},(_,i)=>i);this.q=Array(n).fill(0)}
 find(x){if(this.p[x]===x)return [x,0];let [r,b]=this.find(this.p[x]);this.q[x]^=b;this.p[x]=r;return [r,this.q[x]]}
 join(x,y,b){let [r,a]=this.find(x),[s,c]=this.find(y);if(r===s)return (a^c)===b?0:-1;this.p[r]=s;this.q[r]=a^c^b;return 1}
}
function verify(P,n){let pairs=new Set;ck(P.length===4);for(let S of P){let count=Array(n).fill(0);for(let c of S){ck(c.length===3&&new Set(c).size===3&&c.every(v=>v>=0&&v<n));for(let x of c)count[x]++;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let z=[c[i],c[j]].sort((a,b)=>a-b).join(",");ck(!pairs.has(z));pairs.add(z)}}ck(count.every(v=>v===1))}}
function plane(){let P=[[],[],[],[]];for(let x=0;x<3;x++)P[0].push([3*x,3*x+1,3*x+2]);for(let a=0;a<3;a++)for(let b=0;b<3;b++)P[a+1].push([0,1,2].map(x=>3*x+(a*x+b)%3));return P}
const D=[[[1,9,11],[0,2,5],[6,7,8],[3,4,10]],[[0,6,10],[3,7,9],[2,8,11],[1,4,5]],[[3,5,11],[0,4,7],[2,6,9],[1,8,10]],[[5,8,9],[4,6,11],[0,1,3],[2,7,10]]];
function ring(k,rewire=false){let P=[[],[],[],[]],H=plane(),R=[];for(let i=0;i<k;i++){let b=33*i;for(let a=0;a<4;a++){for(let c of H[a].slice(a===0?2:0))P[a].push(c.map(x=>x+b));for(let off of [9,21])for(let c of D[a].slice(a===0?1:0))P[a].push(c.map(x=>x+b+off))}for(let j=0;j<3;j++)P[0].push([b+3+j,b+9+D[0][0][j],b+21+D[0][0][j]]);R.push([b,33*((i+1)%k)+1,33*((i+1)%k)+2])}if(rewire){let t=R[0][0];R[0][0]=R[1][1];R[1][1]=t}P[0].push(...R);return P}
function cyclic(p){return [0,1,2,3].map(j=>Array.from({length:p},(_,i)=>[i,p+(i+j)%p,2*p+(i+2*j)%p]))}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function relabel(P,n){let q=shuffle(Array.from({length:n},(_,i)=>i));return shuffle(P.map(S=>shuffle(S.map(c=>shuffle(c.map(v=>q[v]))))))}
function solve(P,n,cap=12){verify(P,n);let F=P.flat(),start=[];let o=0;for(let S of P){start.push(o);o+=S.length}let attempts=[];
 for(let a=0;a<4;a++){let B=new DSU(n),lo=start[a],hi=lo+P[a].length;for(let i=0;i<F.length;i++)if(i<lo||i>=hi){let c=F[i];B.join(c[0],c[1],0);B.join(c[0],c[2],0)}
 let C=new Map,at=[];for(let v=0;v<n;v++){let r=B.find(v)[0];if(!C.has(r))C.set(r,{V:[],I:[],E:[],rows:null});let b=C.get(r);b.V.push(v);at[v]=b}
 for(let i=0;i<F.length;i++){let cs=[...new Set(F[i].map(v=>at[v]))];if(cs.length===1)cs[0].I.push(i);else for(let b of cs)b.E.push(i)}
 let groups=[...C.values()],stats={omitted:a,components:groups.length,maxsize:Math.max(...groups.map(b=>b.V.length)),tables:0,visits:0,neutral:0,affine:0,defectCredit:0,forced:0,remaining:null,rank:null};attempts.push(stats);
 let G=new DSU(n),active=new Set(F.map((_,i)=>i)),removed=new Set,records=[];
 // Initial signed NAE closure: without guards all original owners have three distinct positive variables.
 for(let b of groups){if(b.V.length>cap)continue;b.idx=new Map(b.V.map((v,i)=>[v,i]));b.rows=[];stats.tables++;
 let cs=b.I.map(i=>F[i].map(v=>b.idx.get(v)));for(let x=0;x<2**b.V.length;x++){stats.visits++;if(cs.every(c=>((x>>c[0])&1)!==((x>>c[1])&1)||((x>>c[0])&1)!==((x>>c[2])&1)))b.rows.push(x)}
 if(!b.rows.length)return {answer:false,method:"empty_local",attempts};
 // All certified local pair consequences, not a replacement by the affine hull.
 for(let i=0;i<b.V.length;i++)for(let j=i+1;j<b.V.length;j++){let p=((b.rows[0]>>i)^(b.rows[0]>>j))&1;if(b.rows.every(x=>(((x>>i)^(x>>j))&1)===p)){let z=G.join(b.V[i],b.V[j],p);if(z<0)return {answer:false,method:"local_parity",attempts};stats.forced+=z}}
 }
 // Neutral paired attachments, discovered by identical exterior-owner-ID lists.
 let bins=new Map;for(let b of groups)if(b.rows&&b.E.length){let s=b.E.join(",");if(!bins.has(s))bins.set(s,[]);bins.get(s).push(b)}
 for(let L of bins.values())for(let j=0;j<L.length;j++)for(let k=j+1;k<L.length;k++){let b=L[j],c=L[k];if(removed.has(b)||removed.has(c)||b.E.some(i=>!active.has(i)))continue;
 if(b.E.some(i=>F[i].filter(v=>at[v]===b).length!==1||F[i].filter(v=>at[v]===c).length!==1))continue;
 let u=b.E.map(i=>b.idx.get(F[i].find(v=>at[v]===b))),v=c.E.map(i=>c.idx.get(F[i].find(v=>at[v]===c)));
 let key=(x,L,flip)=>L.map(i=>((x>>i)&1)^flip).join("");let M=new Map(c.rows.map(x=>[key(x,v,0),x]));let x=b.rows.find(x=>M.has(key(x,u,1)));if(x===undefined)continue;let y=M.get(key(x,u,1));
 for(let i of [...b.I,...c.I,...b.E])active.delete(i);removed.add(b);removed.add(c);records.push({b,fixed:x},{b:c,fixed:y});stats.neutral++;
 // Actual region rank: the two connected blocks and one exterior vertex per shared clause.
 let ext=new Set(b.E.map(i=>F[i].find(v=>at[v]!==b&&at[v]!==c)));
 stats.defectCredit+=b.I.length+c.I.length+b.E.length-(b.V.length+c.V.length+ext.size-1);
 }
 // Exact signed-equality projection of each remaining local table.
 for(let b of groups){if(!b.rows||removed.has(b))continue;let boundary=[...new Set(b.E.filter(i=>active.has(i)).flatMap(i=>F[i].filter(v=>at[v]===b)))].sort((x,y)=>x-y);
 let pos=boundary.map(v=>b.idx.get(v)),key=x=>pos.map(i=>(x>>i)&1).join("");let M=new Map(b.rows.map(x=>[key(x),x]));
 let H=new DSU(boundary.length);for(let i=0;i<boundary.length;i++)for(let j=i+1;j<boundary.length;j++){let p=((b.rows[0]>>pos[i])^(b.rows[0]>>pos[j]))&1;if(b.rows.every(x=>(((x>>pos[i])^(x>>pos[j]))&1)===p))H.join(i,j,p)}
 let classes=new Set(boundary.map((_,i)=>H.find(i)[0])).size;if(M.size!==2**classes)continue; // exact by containment and equal cardinality
 for(let i of b.I)active.delete(i);removed.add(b);records.push({b,boundary,M});stats.affine++;stats.defectCredit+=b.I.length-b.V.length+1;
 }
 // Record actual rank before rank-one closure. Every remaining owner is a signed triangle on DSU classes.
 let V=new Set,rankUF=new DSU(n),rr=0;for(let i of active){let c=F[i].map(v=>G.find(v)[0]);for(let v of c)V.add(v);for(let j=1;j<3;j++)rr+=rankUF.join(c[0],c[j],0)}
 stats.remaining=active.size;stats.rank=rr;stats.fullDefect=active.size-rr;
 // Reclose all remaining owners using actual signed equality information; no local table is taken as a proof of global SAT.
 let changed=true;while(changed){changed=false;for(let i of [...active]){let L=F[i].map(v=>G.find(v)),M=new Map,taut=false;for(let [r,p] of L){if(M.has(r)&&M.get(r)!==p)taut=true;M.set(r,p)}if(taut){active.delete(i);changed=true;continue}if(M.size===1)return {answer:false,method:"signed_closure",attempts};if(M.size===2){let [[u,p],[v,q]]=[...M];let z=G.join(u,v,1^p^q);if(z<0)return {answer:false,method:"signed_closure",attempts};stats.forced+=z;active.delete(i);changed=true}}}
 if(active.size)continue;
 let x=Array.from({length:n},(_,v)=>G.find(v)[1]);
 // Local witnesses reconstruct removed private variables, never change any surviving port.
 for(let rec of records){let {b}=rec;let w=rec.fixed;if(w===undefined)w=rec.M.get(rec.boundary.map(v=>x[v]).join(""));ck(w!==undefined);for(let i=0;i<b.V.length;i++){let v=b.V[i],z=(w>>i)&1;if(rec.boundary?.includes(v))ck(x[v]===z);else x[v]=z}}
 ck(F.every(c=>nae(c,x)));return {answer:true,method:"lift",attempts,witness:x.join("")};
 }return {answer:null,method:"unknown",attempts}
}
function rank(A){let B=new Map;for(let x of A)while(x){let i=31-Math.clz32(x);if(B.has(i))x^=B.get(i);else{B.set(i,x);break}}return B.size}
function Dmax(A,W=[]){let d=0,r=rank(W);for(let s=0;s<2**A.length;s++){let L=[...W],k=0;for(let i=0;i<A.length;i++)if((s>>i)&1){k++;L.push(...A[i])}d=Math.max(d,k-rank(L)+r)}return d}
let rankTests=0,positive=0;
for(let j=0;j<600;j++){let m=2+rnd(6),A=Array.from({length:m},()=>[1+rnd(15),1+rnd(15)]),k=1+rnd(m),R=A.slice(0,k),S=A.slice(k),W=R.flat().filter(()=>rnd(2));let d=k-rank(R.flat());ck(Dmax(A)>=Dmax(S,W)+d);positive+=d>0;rankTests++}
let jobs=[];
for(let k of [3,5,9,17,33,65,4,16])for(let v of (k%2?[false,true]:[false])){let n=33*k,P=relabel(ring(k,v),n),a=solve(P,n);ck(a.answer===(v||k%2===0));jobs.push({name:"ring",k,rewired:v,n,m:4*n/3,answer:a.answer,method:a.method,attempts:a.attempts})}
for(let [name,P,n,label] of [["AG",plane(),9,false],["aux",D,12,true]]){let a=solve(relabel(P,n),n);ck(a.answer===label);jobs.push({name,n,answer:a.answer,method:a.method,attempts:a.attempts})}
for(let p of [7,11,31,101]){let n=3*p,P=relabel(cyclic(p),n),a=solve(P,n);ck(a.answer===null);jobs.push({name:"cyclic",p,n,answer:a.answer,method:a.method,attempts:a.attempts})}
console.log(JSON.stringify({seed:20261125,checks,rankTests,positive,jobs}));
