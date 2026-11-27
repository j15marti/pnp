function audit(){
const E=[[0,0,3],[0,1,0],[0,1,3],[0,2,1],[0,2,3],[1,1,2],[1,2,1],[1,4,2],[1,4,3],[1,4,4],[2,0,4],[2,3,4],[2,4,0],[2,4,2],[3,1,1],[3,1,4],[3,2,0],[3,2,4],[3,3,1],[3,4,2],[3,4,4],[4,0,2],[4,1,4],[4,3,4]];
const x0=[0,1,0,-1,1,-1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,0], frac=[2,0,0,0,1,2,1,0,0,0,0,0,3,0,1,0,0,1,1,0,0,1,0,2];
const assert=(x,msg)=>{if(!x)throw Error(msg)};
const n=5,m=E.length, A=Array.from({length:15},(_,i)=>E.map(e=>+(e[Math.floor(i/5)]===i%5)));
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
assert(A.every(r=>dot(r,x0)===1&&dot(r,frac)===3),"integer/fractional");
assert(A.every(r=>r.reduce((a,b)=>a+b,0)>=2),"unit closure");
const rank=rows=>{const p=101,mod=x=>(x%p+p)%p;let M=rows.map(r=>r.map(mod)),k=0;for(let j=0;j<(M[0]?.length??0)&&k<M.length;j++){let i=M.findIndex((r,i)=>i>=k&&r[j]);if(i<0)continue;[M[i],M[k]]=[M[k],M[i]];let a=1;while(mod(a*M[k][j])!==1)a++;M[k]=M[k].map(x=>mod(x*a));for(let t=k+1;t<M.length;t++){let c=M[t][j];if(c)M[t]=M[t].map((x,l)=>mod(x-c*M[k][l]))}k++}return k};
assert(rank(A)===13,"rank");
const out=[];
for(const [a,b,c] of [[0,1,2],[0,2,1],[1,2,0]]){
let F=new Map(), visits=0;
function walk(i,used,t){visits++;if(i===5){let s=Array(5).fill(0);for(let e of t)s[E[e][c]]++;let k=s.join(",");if(!F.has(k))F.set(k,[]);F.get(k).push(t.slice());return}for(let e=0;e<m;e++)if(E[e][a]===i&&!(used&(1<<E[e][b])))walk(i+1,used|(1<<E[e][b]),[...t,e])}
walk(0,0,[]);assert(!F.has("1,1,1,1,1"),"NO");
let all=[...F.values()].flat(),supported=new Set(all.flat());assert(supported.size===m,"all edges supported");
let D=[],pairs=[];for(let ts of F.values())for(let t of ts.slice(1)){let u=ts[0],d=E.map((_,i)=>+t.includes(i)- +u.includes(i));assert(A.every(r=>dot(r,d)===0),"kernel");if(rank([...D,d])>D.length){D.push(d);pairs.push([t,u])}}
assert(D.length===11,"full kernel");
let pair=null;const weights=Array.from({length:243},(_,i)=>Array.from({length:5},(_,j)=>Math.floor(i/3**(4-j))%3-1));
const S=[...F.keys()].map(k=>k.split(",").map(Number));let H=weights.map(w=>S.map((s,i)=>dot(w,s)===w.reduce((a,b)=>a+b,0)?i:-1).filter(i=>i>=0));
for(let i=0;i<243&&!pair;i++)if(H[i].length)for(let j=i+1;j<243;j++)if(H[j].length&&!H[i].some(x=>H[j].includes(x))){pair={w:weights[i],v:weights[j],wHits:H[i].length,vHits:H[j].length};break}
assert(pair,"joint projection");
out.push({orientation:[a,b,c],matchings:all.length,fibers:F.size,visits,supported:supported.size,rank:D.length,basisPairs:pairs,pair,syndromes:S});
}
let combinations=0,exact=0;function choose(start,t){if(t.length===5){combinations++;if([0,1,2].every(a=>new Set(t.map(i=>E[i][a])).size===5))exact++;return}for(let i=start;i<=m-(5-t.length);i++)choose(i+1,[...t,i])}choose(0,[]);assert(combinations===42504&&exact===0,"independent exact count");
return {E,x0,fracNumerator:frac,fracDenominator:3,rankA:rank(A),out,combinations,exact,guard:"all 24 IDs active",fingerprintInput:JSON.stringify(E)};
}
console.log(JSON.stringify(audit(),null,2));
