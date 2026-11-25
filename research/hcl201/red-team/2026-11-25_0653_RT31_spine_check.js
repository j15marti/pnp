// Finite raw-chart audit; not a production RP solver. Run: node research/hcl201/red-team/2026-11-25_0653_RT31_spine_check.js
function main(){
const mul=new Uint8Array(65536);for(let a=0;a<256;a++)for(let b=0;b<256;b++){let x=a,y=b,z=0;while(y){if(y&1)z^=x;y>>=1;x=(x<<1)^((x&128)?283:0);}mul[a*256+b]=z}
const M=(a,b)=>mul[a*256+b],inv=new Uint8Array(256);for(let a=1;a<256;a++)for(let b=1;b<256;b++)if(M(a,b)===1){inv[a]=b;break}
let seed=20261125>>>0;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
const stats={evaluationComparisons:0,determinants:0,referenceAssignments:0,hallSubsets:0,rankTwoOwnerChecks:0,verifiedWitnesses:0,nonzeroEvaluations:0,zeroEvaluations:0,cases:[],assertions:0};
function ok(t,s){stats.assertions++;if(!t)throw Error(s)}
function parity(x){let p=0;while(x){p^=1;x&=x-1}return p}
function rank(rows){const b=[];for(let x of rows){while(x){let j=31-Math.clz32(x);if(b[j])x^=b[j];else{b[j]=x;break}}}return b.filter(Boolean).length}
function det(B){stats.determinants++;let a=B.map(x=>x.slice()),v=1;for(let i=0;i<a.length;i++){let j=i;while(j<a.length&&!a[j][i])j++;if(j===a.length)return 0;[a[i],a[j]]=[a[j],a[i]];let p=a[i][i];v=M(v,p);for(j=i+1;j<a.length;j++){let f=M(a[j][i],inv[p]);if(f)for(let k=i+1;k<a.length;k++)a[j][k]^=M(f,a[i][k]);a[j][i]=0}}return v}
function choose(xs,k,cb,start=0,acc=[]){if(!k){cb(acc);return}for(let j=start;j<=xs.length-k;j++)choose(xs,k-1,cb,j+1,acc.concat(xs[j]))}
function coefficient(A,c,r){const m=A.length,d=m-r,rows=Array.from({length:m},(_,i)=>i),cols=Array.from({length:r},(_,i)=>i);let out=0;
function repeat(left,used,start,budget,v){if(!v)return;if(!budget){const cc=cols.filter(j=>!used.includes(j));ok(left.length===cc.length,"minor shape");out^=M(v,det(left.map(i=>cc.map(j=>A[i][j]))));return}for(let j=start;j<r;j++)for(let h=2;h<=Math.min(budget+1,left.length);h++)choose(left,h,ss=>{let w=v;for(const i of ss)w=M(w,A[i][j]);repeat(left.filter(i=>!ss.includes(i)),used.concat(j),j+1,budget-(h-1),w)})}
for(let k=0;k<=d;k++)choose(rows,k,ss=>{let v=1;for(const i of ss)v=M(v,c[i]);repeat(rows.filter(i=>!ss.includes(i)),[],0,d-k,v)});return out}
function coeffRows(P,w,r){let A=[],c=[];for(let i=0;i<P.length;i++){let {a,b,s}=P[i],h=[a,b,a^b],v=[s&1,s>>1,((s&1)^(s>>1))],row=Array(r).fill(0),z=0;for(let j=0;j<3;j++){if(v[j])z^=w[i][j];for(let k=0;k<r;k++)if(h[j]>>k&1)row[k]^=w[i][j]}A.push(row);c.push(z)}return [A,c]}
function evalP(P,w,r){let [A,c]=coeffRows(P,w,r);return coefficient(A,c,r)}
function direct(A,c,r){let out=0;for(let x=0;x<1<<r;x++){stats.referenceAssignments++;let p=1;for(let i=0;i<A.length;i++){let v=c[i];for(let j=0;j<r;j++)if(x>>j&1)v^=A[i][j];p=M(p,v);if(!p)break}out^=p}return out}
function legal(P,x){return P.every(({a,b,s})=>(parity(x&a)+2*parity(x&b))!==s)}
function hall(P,r){const m=P.length;let d=m-r;for(let t=0;t<1<<m;t++){let rows=[],k=0;for(let i=0;i<m;i++)if(t>>i&1){k++;rows.push(P[i].a,P[i].b)}stats.hallSubsets++;if(k-rank(rows)>d)return false}return rank(P.flatMap(q=>[q.a,q.b]))===r}
function test(P,r,label,trials=4){let m=P.length,d=m-r;for(const q of P){stats.rankTwoOwnerChecks++;ok(rank([q.a,q.b])===2,"singleton rank2 closure")};if(!hall(P,r))return false;let models=[];for(let x=0;x<1<<r;x++)if(legal(P,x))models.push(x);let hits=0;
for(let t=0;t<trials;t++){let w=P.map(()=>[rnd(256),rnd(256),rnd(256)]),[A,c]=coeffRows(P,w,r),a=coefficient(A,c,r),b=direct(A,c,r);stats.evaluationComparisons++;ok(a===b,"coefficient mismatch");if(!a){stats.zeroEvaluations++;continue}stats.nonzeroEvaluations++;hits++;ok(models.length>0,"false positive");if(hits===1){for(let i=0;i<m;i++){let found=false;for(let j=0;j<3;j++){w[i]=[0,0,0];w[i][j]=1;if(evalP(P,w,r)){found=true;break}}ok(found,"self reduction")}let sol=[];for(let x=0;x<1<<r;x++){let good=true;for(let i=0;i<m;i++){let {a,b,s}=P[i],j=w[i].indexOf(1),mask=[a,b,a^b][j],rhs=[s&1,s>>1,(s&1)^(s>>1)][j];if((parity(x&mask)^rhs)!==1){good=false;break}}if(good)sol.push(x)}ok(sol.length===1&&legal(P,sol[0]),"unique original witness");stats.verifiedWitnesses++}}stats.cases.push({label,r,m,d,models:models.length,hits,trials});return true}
let triples=[];for(let i=1;i<=7;i++)for(let j=i+1;j<=7;j++){let k=i^j;if(k>j)triples.push([i,j,k])}
const e=i=>i===1?0:1<<(i-2),F=triples.map(([i,j,k])=>({a:e(i)^e(j),b:e(i)^e(k),s:0}));test(F,6,"Fano root",8);for(let i=0;i<7;i++)for(let s=1;s<4;s++)test(F.map((q,j)=>({...q,s:i===j?s:q.s})),6,"Fano neighbor "+i+"/"+s,3);
function expansion(P,r){let a=P[0],b=1<<r,c=1<<(r+1),d=1<<(r+2);return [{a:a.a^c,b:a.b^d,s:a.s},{a:b,b:d,s:2},{a:b,b:c,s:3},{a:b^c,b:b^d,s:1},...P.slice(1)]}
const E=expansion(F,6);test(E,9,"RT21 single expansion root",4);test(expansion(F.map((q,i)=>({...q,s:i===0?1:0})),6),9,"RT21 single expansion neighbor",4);
for(const d of [0,1,2]){let done=0,attempts=0;while(done<12&&attempts++<100){let r=d===2?4+rnd(2):4+rnd(3),P=[];for(let i=0;i<r+d;i++){let a=1+rnd((1<<r)-1),b=1+rnd((1<<r)-1);while(a===b)b=1+rnd((1<<r)-1);P.push({a,b,s:rnd(4)})}if(test(P,r,"random d"+d+" #"+done,3))done++}ok(done===12,"random sample count")}
return stats
}
console.log(JSON.stringify(main(),null,2));
