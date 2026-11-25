const results=(function run(){
let C={assertions:0,geometry:0,controls:0,sat:0,unsat:0,decline:0,scans:0,forced:0,reachCalls:0,referenceWords:0,grids:[],fano:[]};
function ok(x){C.assertions++;if(!x)throw Error("assertion "+C.assertions)}
let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
const bit=i=>1n<<BigInt(i), par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p}, pivot=x=>x.toString(2).length-1;
function gauss(rows){let B=new Map();for(let [a,b] of rows){for(const [p,[v,c]] of [...B].sort((x,y)=>y[0]-x[0]))if(a&bit(p)){a^=v;b^=c}if(!a){if(b)return null;continue}let p=pivot(a);for(const [q,[v,c]] of B)if(v&bit(p))B.set(q,[v^a,c^b]);B.set(p,[a,b])}return [...B].sort((x,y)=>y[0]-x[0]).map(x=>x[1])}
function red(a,b,G){for(const [v,c] of G)if(a&bit(pivot(v))){a^=v;b^=c}return [a,b]}
function span(P){let [a,b]=P.map(x=>x[0]);return [a,b,a^b].sort((x,y)=>x<y?-1:x>y?1:0)}
const key=S=>S.join(",");
function basis(P){let D=new Map();for(let p of P){let s=span(p);D.set(key(s),s)}let count=new Map();for(let s of D.values())for(let a of s)count.set(a,(count.get(a)||0)+1);let B=new Set([...count].filter(x=>x[1]>1).map(x=>x[0]));for(let s of D.values()){let t=s.filter(a=>B.has(a));if(t.length>2)return null;for(let a of s)if(t.length<2&&!t.includes(a)){t.push(a);B.add(a)}}let out=[...B];if(gauss(out.map(a=>[a,0])).length!==out.length)return null;return out}
function feasible(P,x){return P.every(p=>!p.every(([a,b])=>par(a&x)===b))}
function close(P,G){while(true){C.scans++;G=gauss(G);if(!G)return null;let Q=[],f=null;for(let p of P){let q=gauss(p.map(([a,b])=>red(a,b,G)));if(!q)continue;if(!q.length)return null;if(q.length===1){f=[q[0][0],q[0][1]^1];break}Q.push(q)}if(f){G.push(f);C.forced++;continue}
let D=new Map();for(let q of Q){let k=key(span(q));if(!D.has(k))D.set(k,[]);D.get(k).push(q)}for(let group of D.values()){let [a,b]=group[0].map(x=>x[0]), A=[];for(let u=0;u<2;u++)for(let v=0;v<2;v++){let val=new Map([[a,u],[b,v],[a^b,u^v]]);if(group.every(q=>!q.every(([z,c])=>val.get(z)===c)))A.push(val)}if(!A.length)return null;for(let z of [a,b,a^b])if(A.every(v=>v.get(z)===A[0].get(z))){f=[z,A[0].get(z)];break}if(f)break}if(f){G.push(f);C.forced++;continue}return {P:Q,G}}}
function decision(k,clauses){C.reachCalls++;let A=Array.from({length:2*k},()=>[]);for(let [a,b] of clauses){A[a^1].push(b);A[b^1].push(a)}function reach(s,t){let seen=new Set([s]),Q=[s];for(let i=0;i<Q.length;i++){if(Q[i]===t)return true;for(let j of A[Q[i]])if(!seen.has(j)){seen.add(j);Q.push(j)}}return false}for(let i=0;i<2*k;i+=2)if(reach(i,i+1)&&reach(i+1,i))return false;return true}
function solve(P,G=[]){let c=close(P,G);if(!c)return {status:"unsat"};let B=basis(c.P);if(!B)return {status:"decline"};let clauses=c.P.map(p=>{let forms=span(p).filter(x=>B.includes(x));ok(forms.length===2);let bad=new Map(p.map(([a,b])=>[a,b]));let [a,b]=p.map(x=>x[0]);bad.set(a^b,p[0][1]^p[1][1]);return forms.map(a=>2*B.indexOf(a)+(bad.get(a)^1))});if(!decision(B.length,clauses))return {status:"unsat"};let E=[...c.G];for(let i=0;i<B.length;i++){let l=2*i;if(!decision(B.length,[...clauses,[l,l]]))l^=1;clauses.push([l,l]);E.push([B[i],l&1])}let g=gauss(E);ok(g!==null);let x=0n;for(let [a,b] of g)if(b)x|=bit(pivot(a));ok(feasible(P,x)&&G.every(([a,b])=>par(a&x)===b));return {status:"sat",x}}
function test(n,P,G=[]){C.controls++;let count=0;for(let x=0n;x<bit(n);x++){C.referenceWords++;if(feasible(P,x)&&G.every(([a,b])=>par(a&x)===b))count++}let a=solve(P,G);C[a.status]++;if(a.status!=="decline")ok((a.status==="sat")===(count>0));return {status:a.status,count}}
function bruteGeom(n,P){let S=[...new Set(P.flatMap(span))];let t=gauss(S.map(a=>[a,0])).length;function dfs(i,L){if(L.length===t)return P.every(p=>span(p).filter(a=>L.includes(a)).length===2);for(let j=i;j<S.length;j++){let Q=[...L,S[j]];if(gauss(Q.map(a=>[a,0])).length===Q.length&&dfs(j+1,Q))return true}return false}return dfs(0,[])}
let planes=[];for(let a=1n;a<8n;a++)for(let b=a+1n;b<8n;b++){let p=[[a,0],[b,0]];if(!planes.some(q=>key(span(q))===key(span(p))))planes.push(p)}
for(let s=0;s<1<<planes.length;s++){let P=planes.filter((_,i)=>s>>i&1);ok(!!basis(P)===bruteGeom(3,P));C.geometry++}
for(let t=0;t<240;t++){let P=[];for(let j=0;j<1+rnd(7);j++){let a=BigInt(1+rnd(15)),b=BigInt(1+rnd(15));if(a===b)b=b===15n?1n:b+1n;P.push([[a,rnd(2)],[b,rnd(2)]])}ok(!!basis(P)===bruteGeom(4,P));C.geometry++;test(4,P,t%3===0?[[BigInt(1+rnd(15)),rnd(2)]]:[])}
// All rank-two coordinate systems on a triangle with randomized signed exclusions; include distinct-plane UNSAT.
for(let t=0;t<160;t++){let n=5,P=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(rnd(5)!==0)P.push([[bit(i)^bit(5),rnd(2)],[bit(j)^bit(5),rnd(2)]]);test(6,P,t%4===0?[[bit(5),rnd(2)]]:[])}
// A known contradiction from four two-literal clauses, plus a one-deletion SAT neighbor.
let four=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)four.push([[1n,a],[2n,b]]);test(2,four);test(2,four.slice(1));
// Fano root and signed/one-budget neighbors.
let E=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function nae(e,sign=0){let [a,b,c]=e;return [[bit(a)^bit(b),((sign>>0)^(sign>>1))&1],[bit(a)^bit(c),((sign>>0)^(sign>>2))&1]]}
let F=E.map(e=>nae(e));C.fano.push(test(7,F));for(let i=0;i<7;i++)for(let j=0;j<3;j++){let P=F.map((p,k)=>k===i?nae(E[k],1<<j):p);let a=test(7,P);ok(a.count===10);C.fano.push(a)}
// Budget neighbors have a rank-three packet for the remaining monochromatic word; reference only.
for(let i=0;i<7;i++)for(let b=0;b<2;b++){let P=F.map((p,k)=>k===i?E[k].map(v=>[bit(v),b]):p);let count=0;for(let x=0n;x<128n;x++){C.referenceWords++;if(feasible(P,x))count++}ok(count===5)}
// Grid controls: all actual source variables except the shared reference can be set to 1.
for(let L of [2,4,6,8]){let n=L*L,r=bit(n),P=[],edges=[];for(let i=0;i<n;i++)for(let j of [i%L<L-1?i+1:-1,i+L<n?i+L:-1])if(j>=0){edges.push([i,j]);P.push([[bit(i)^r,0],[bit(j)^r,0]])}let a=solve(P);ok(a.status==="sat");let A=new Set(Array.from({length:n/2},(_,i)=>i));let cross=edges.filter(([i,j])=>A.has(i)!==A.has(j));let adj=Array.from({length:n},()=>new Set());for(let [i,j] of edges){adj[i].add(j);adj[j].add(i)}let M=[];while(cross.length){let [i,j]=cross.shift();M.push([i,j]);cross=cross.filter(([u,v])=>![i,j].some(w=>w===u||w===v||adj[w].has(u)||adj[w].has(v)))}let k=M.length;let mat=[];for(let x=0;x<1<<k;x++){let row=0n;for(let y=0;y<1<<k;y++)if((x|y)===(1<<k)-1)row|=bit(y);mat.push([row,0])}let rank=gauss(mat).length;ok(rank===2**k);C.grids.push({L,n,packets:P.length,basis:basis(P).length,inducedMatching:k,submatrixRank:rank})}
return C
})();
console.log(JSON.stringify(results,null,2));
