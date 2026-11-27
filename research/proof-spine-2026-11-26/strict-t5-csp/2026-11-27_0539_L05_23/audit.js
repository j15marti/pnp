function main(){
const cap=65536;
function assert(x,msg){if(!x)throw Error(msg)}
function bareiss(A){A=A.map(r=>r.slice());let sign=1n,p=1n,ops=0,maxbits=0,n=A.length;for(let k=0;k<n-1;k++){let i=k;while(i<n&&A[i][k]===0n)i++;if(i===n)return {v:0n,ops,maxbits};if(i!==k){[A[i],A[k]]=[A[k],A[i]];sign=-sign}let z=A[k][k];for(i=k+1;i<n;i++){for(let j=k+1;j<n;j++){let v=A[i][j]*z-A[i][k]*A[k][j];assert(v%p===0n,"division");maxbits=Math.max(maxbits,(v<0n?-v:v).toString(2).length);A[i][j]=v/p;ops++}A[i][k]=0n}p=z}return {v:sign*A[n-1][n-1],ops,maxbits}}
function make(R,C,a,hostile=false){
const q=R*C/2,hub=C/2,rank=i=>i===hub?q:i,edges=[],adj=Array.from({length:R*C},()=>[]),A=Array.from({length:q},()=>[]);
function id(r,c){return r*(C/2)+Math.floor(c/2)}
for(let r=0;r<R;r++)for(let c=0;c<C;c++)if((r+c)%2===0){for(const [dr,dc] of [[0,1],[0,-1],[1,0],[-1,0]]){let s=r+dr,z=c+dc;if(s<0||s>=R||z<0||z>=C)continue;let i=id(r,c),j=id(s,z),w=i===j||rank(i)<rank(j)?0:a+1;
if(i===hub&&(j===0||j===C))w=a;
if(hostile&&i===q-1&&j===q-1-C/2)w=a;
let e={i,j,w,sgn:dc===0&&c%2===1?-1:1,u:r*C+c,v:s*C+z};edges.push(e);A[i].push(e);adj[e.u].push(e);adj[e.v].push(e)}}
return {R,C,a,q,hub,edges,A,adj}}
function determinant(g){let B=1n;for(let j=2;j<=g.q;j++)B*=BigInt(j);B++;let mat=Array.from({length:g.q},()=>Array(g.q).fill(0n));for(const e of g.edges)mat[e.i][e.j]=BigInt(e.sgn)*B**BigInt(e.w);let r=bareiss(mat),v=r.v<0n?-r.v:r.v,counts=[];while(v){counts.push((v%B).toString());v/=B}return {counts,ops:r.ops,maxbits:r.maxbits,baseBits:B.toString(2).length}}
function reference(g){let visits=0,counts=[],limit=false;function rec(i,mask,w){if(++visits>cap){limit=true;return}if(i===g.q){counts[w]=(counts[w]||0n)+1n;return}for(const e of g.A[i]){let b=1n<<BigInt(e.j);if(!(mask&b)){rec(i+1,mask|b,w+e.w);if(limit)return}}}rec(0,0n,0);return {visits,limit,counts:Array.from(counts,x=>String(x||0n))}}
function domino(g){let visits=0,mem=new Map();const all=(1n<<BigInt(g.R*g.C))-1n;function rec(mask){if(mem.has(mask))return mem.get(mask);if(++visits>cap)throw Error("cap");if(mask===all)return [1n];let u=0;while(mask&(1n<<BigInt(u)))u++;let out=[];for(const e of g.adj[u]){let v=e.u===u?e.v:e.u,b=1n<<BigInt(v);if(mask&b)continue;let z=rec(mask|b|(1n<<BigInt(u)));for(let j=0;j<z.length;j++)if(z[j])out[j+e.w]=(out[j+e.w]||0n)+z[j]}mem.set(mask,out);return out}try{return {visits:0,counts:Array.from(rec(0n),x=>String(x||0n)),get states(){return visits}}}catch(e){return {states:visits,limit:true}}}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function size(g){let L=2*g.a+3,k=L*g.q-2*g.a,t=g.q*L,arcs=t;for(const e of g.edges)if(e.i!==e.j){t+=L-e.w-1;arcs+=L-e.w}let E=t*(1+k*k)+k*arcs,O=3*(t+k),n=64*E-20*O+5,m=78*E-24*O+5,N=n+2+2*Math.floor(Math.log2(m+1))+3*m*Math.ceil(Math.log2(n+1));return {L,k,t,arcs,E,O,n,m,N}}
function check(R,C,a,hostile=false){let g=make(R,C,a,hostile),d=determinant(g),r=reference(g),b=domino(g);assert(!b.limit&&same(b.counts,d.counts),"domino/det");if(!r.limit)assert(same(r.counts,d.counts),"enum/det");let target=d.counts[2*a]||"0";assert((target!=="0")===hostile,"target");assert(d.counts[a]!=="0"&&d.counts[a+1]!=="0","nearby");let f=0;for(let row=0;row<R-1;row+=2)for(let col=0;col<C/2;col++){let i=row*C/2+col,j=i+C/2;assert(g.A[i].some(e=>e.j===j)&&g.A[j].some(e=>e.j===i),"pair");f++}
let reach=(reverse)=>{let s=new Set([0]),todo=[0];while(todo.length){let u=todo.pop();for(const e of g.edges)if((reverse?e.j:e.i)===u){let v=reverse?e.i:e.j;if(!s.has(v)){s.add(v);todo.push(v)}}}return s.size};assert(reach(false)===g.q&&reach(true)===g.q,"SCC");
return {R,C,a,hostile,q:g.q,edgeCount:g.edges.length,disjointCycles:f,size:size(g),target,shortSupport:d.counts.map((x,i)=>x!=="0"&&i<=2*a?i:null).filter(x=>x!==null),total:d.counts.reduce((s,x)=>s+BigInt(x),0n).toString(),det:d,reference:r,domino:b}}
let rows=[[4,4,2],[4,6,3],[6,6,4],[8,8,5]].map(x=>check(...x));let hostile=check(4,4,2,true);
let C=(x,y,z)=>{let a=[x,y,z].sort().join("");return ["012","123","234","034","014"].includes(a)},beats=(x,y)=>[1,3].includes((y-x+5)%5),R=(x,y,z)=>x!==y&&x!==z&&y!==z&&(beats(x,y)!==beats(x,z));let relationRows=0;for(let x=0;x<5;x++)for(let y=0;y<5;y++)for(let z=0;z<5;z++){assert(C(x,y,z)===(R(x,y,z)&&R(y,x,z)),"C/R");relationRows++}
let unsigned=bareiss([[1n,1n],[1n,1n]]).v.toString();assert(unsigned==="0","cancellation");
return {cap,rows,hostile,relationRows,unsignedK22:unsigned}}

console.log(JSON.stringify(main(),null,2));
