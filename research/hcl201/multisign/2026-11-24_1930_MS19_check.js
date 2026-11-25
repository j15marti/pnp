function experiment(){
let seed=20261124, stats={tests:0,SAT:0,UNSAT:0,latticeRejected:0,unknown:0,closureRows:0,passes:0,joins:0,peakKeys:0,basisCalls:0,euclid:0,assertions:0,maxBits:0}, controls=[];
const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}, assert=(v)=>{stats.assertions++;if(!v)throw Error("assertion")};
const add=(a,b)=>a.map((v,i)=>v+b[i]), sub=(a,b)=>a.map((v,i)=>v-b[i]), mul=(a,q)=>a.map(v=>v*q), zero=n=>Array(n).fill(0n);
const bits=a=>a.reduce((s,x,i)=>s|((x&1n)<<BigInt(i)),0n);
const parity=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
function basis(rows,d){stats.basisCalls++;let a=rows.filter(v=>v.some(x=>x!==0n)).map(v=>v.slice()),k=0;
 for(let j=0;j<d&&k<a.length;j++){let p=a.findIndex((v,i)=>i>=k&&v[j]!==0n);if(p<0)continue;[a[k],a[p]]=[a[p],a[k]];
 for(let i=k+1;i<a.length;i++)while(a[i][j]!==0n){const q=a[k][j]/a[i][j];const v=sub(a[k],mul(a[i],q));a[k]=a[i];a[i]=v;stats.euclid++;}
 if(a[k][j]<0n)a[k]=mul(a[k],-1n); k++;}
 a=a.slice(0,k);for(const v of a)for(const x of v)stats.maxBits=Math.max(stats.maxBits,(x<0n?-x:x).toString(2).length);return a}
function gf(rows,d){let a=rows.filter(x=>x!==0n),k=0,piv=[];for(let j=0;j<d;j++){let b=1n<<BigInt(j),i=a.findIndex((v,i)=>i>=k&&(v&b));if(i<0)continue;[a[i],a[k]]=[a[k],a[i]];for(let z=0;z<a.length;z++)if(z!==k&&(a[z]&b))a[z]^=a[k];piv.push(j);k++}return {a:a.slice(0,k),piv}}
function nulls(rows,d){const {a,piv}=gf(rows,d);return Array.from({length:d},(_,j)=>j).filter(j=>!piv.includes(j)).map(j=>{let v=1n<<BigInt(j);for(let i=0;i<a.length;i++)if(a[i]&v)v|=1n<<BigInt(piv[i]);return v})}
function member(v,B){for(const b of B){let j=b.findIndex(x=>x!==0n);if(v[j]%b[j]!==0n)return false;v=sub(v,mul(b,v[j]/b[j]))}return v.every(x=>x===0n)}
function fiber(P,Q,k){let a=P.a.slice(),B=P.B;for(const b of B){let j=b.findIndex(x=>x!==0n);if(j>=k)continue;let v=Q[j]-a[j];if(v%b[j]!==0n)return null;a=add(a,mul(b,v/b[j]));}if(Q.some((q,j)=>a[j]!==q))return null;return {a:bits(a.slice(k)),B:B.filter(b=>b.slice(0,k).every(x=>x===0n)).map(b=>bits(b.slice(k)))}}
function solve(blocks,target,Q,guard=[]){const n=blocks.length,d=3*n,k=Q.length,D=k+d;
 const code=(i,o)=>1n<<BigInt(3*i+o);
 function leaf(i,o){let a=zero(D);blocks[i][o].w.forEach((v,j)=>a[j]=BigInt(v));a[k+3*i+o]=1n;let tag=BigInt(blocks[i][o].tag);for(let j=0;j<guard.length;j++)if(parity(guard[j][0]&code(i,o)))tag|=1n<<BigInt(j+4);return {a,tag}}
 function merge(P,R){if(!P)return R;return {a:P.a,B:basis([...P.B,...R.B,sub(R.a,P.a)],D)}}
 function dp(l,r){if(r-l===1){let out=new Map();for(let o=0;o<blocks[l].length;o++){let {a,tag}=leaf(l,o);out.set(tag,merge(out.get(tag),{a,B:[]}))}stats.peakKeys=Math.max(stats.peakKeys,out.size);return out}
 let mid=(l+r)>>1,L=dp(l,mid),R=dp(mid,r),out=new Map();for(const [x,P] of L)for(const [y,S] of R){stats.joins++;let tag=x^y;out.set(tag,merge(out.get(tag),{a:add(P.a,S.a),B:basis([...P.B,...S.B],D)}))}stats.peakKeys=Math.max(stats.peakKeys,out.size);return out}
 let root=BigInt(target);for(let j=0;j<guard.length;j++)if(guard[j][1])root|=1n<<BigInt(j+4);return dp(0,n).get(root)}
function ref(blocks,target,Q){let out=[],coarse=[];function rec(i,t,c,x){if(i===blocks.length){if(t===target){coarse.push({c,x});if(c.every((v,j)=>v===Q[j]))out.push(x)}return}for(let j=0;j<blocks[i].length;j++){let o=blocks[i][j];rec(i+1,t^o.tag,c.map((v,h)=>v+BigInt(o.w[h])),x|(1n<<BigInt(3*i+j)))}}rec(0,0,zero(Q.length),0n);return {out,coarse}}
function run(name,blocks,target,quota,check=true){let Q=quota.map(BigInt),d=3*blocks.length,k=Q.length,R=check?ref(blocks,target,Q):null,guard=[],reason="UNKNOWN",first=null,last=null,rounds=0,rankDrop=0;
 if(R){stats.tests++;if(R.out.length)stats.SAT++;else stats.UNSAT++}
 while(true){stats.passes++;rounds++;let P=solve(blocks,target,Q,guard);
 if(!P){reason="UNSAT-coarse";break}
 let coarseA=bits(P.a.slice(k)),coarseB=P.B.map(b=>bits(b.slice(k))),coarseRank=gf(coarseB,d).a.length;if(first===null)first=coarseRank;last=coarseRank;
 if(R){let actual=R.coarse.filter(v=>guard.every(([a,b])=>parity(a&v.x)===b));assert(actual.length>0);let vectors=actual.map(v=>[...v.c,...Array.from({length:d},(_,i)=>(v.x>>BigInt(i))&1n)]);let direct=basis(vectors.map(v=>sub(v,vectors[0])),k+d);
 assert(member(sub(P.a,vectors[0]),direct));for(const b of P.B)assert(member(b,direct));for(const b of direct)assert(member(b,P.B));for(const v of vectors)assert(member(sub(v,P.a),P.B))}
 let F=fiber(P,Q,k);if(!F){reason="UNSAT-lattice";stats.latticeRejected++;break}
 let equations=nulls(F.B,d).map(a=>[a,parity(a&F.a)]);
 if(R)for(const x of R.out)for(const [a,b] of equations)assert(parity(x&a)===b);
 let next=equations.find(([a,b])=>parity(a&coarseA)!==b||coarseB.some(v=>parity(v&a)));
 if(next){guard.push(next);stats.closureRows++;continue}
 let actualCosts=P.a.slice(0,k);if(P.B.every(b=>b.slice(0,k).every(x=>x===0n))&&actualCosts.every((v,i)=>v===Q[i])){reason="SAT-anchor";if(R)assert(R.out.includes(coarseA));break}
 // Actual anchor is always a matching; its exact quota can also certify SAT.
 if(actualCosts.every((v,i)=>v===Q[i])){reason="SAT-anchor";if(R)assert(R.out.includes(coarseA));break}
 stats.unknown++;break}
 if(R){if(reason.startsWith("UNSAT"))assert(R.out.length===0);if(reason.startsWith("SAT"))assert(R.out.length>0)}
 rankDrop=first===null||last===null?0:first-last;
 return {name,blocks:blocks.length,reference:R?R.out.length:null,reason,rounds,newRows:guard.length,rankDrop,firstRank:first,lastRank:last}}
 const block=(w0,w1,t0=0,t1=0)=>[{w:w0,tag:t0},{w:w1,tag:t1}];
 controls.push(run("joint parity hole",[block([0,0],[1,1]),block([0,0],[1,-1])],0,[1,0]));
 controls.push(run("higher congruence closure",[block([0,0],[1,1]),block([0,0],[1,-1]),block([0,0],[0,4])],0,[1,1]));
 controls.push(run("lattice false positive",[block([0],[2]),block([0],[3])],0,[1]));
 for(let n of [4,8,16,32]){let M=1n<<BigInt(n*8);let B=[block([0n,0n],[M,M]),block([0n,0n],[M,-M]),block([0n,0n],[0n,4n*M])];while(B.length<n)B.push(block([0n,0n],[0n,0n]));controls.push(run("scaled SAT "+n,B,0,[M,M],n<=8));controls.push(run("scaled UNSAT "+n,B,0,[M,0n],n<=8))}
 for(let i=0;i<100;i++){let n=2+rnd(4),k=1+rnd(2),blocks=Array.from({length:n},()=>Array.from({length:2+rnd(2)},()=>({w:Array.from({length:k},()=>rnd(11)-5),tag:rnd(4)})));let target=rnd(4),Q=Array.from({length:k},()=>rnd(13)-6);if(i%2===0){let chosen=blocks.map(b=>b[rnd(b.length)]);target=chosen.reduce((x,o)=>x^o.tag,0);Q=Array.from({length:k},(_,j)=>chosen.reduce((s,o)=>s+o.w[j],0))}run("random "+i,blocks,target,Q)}
 return {seed:20261124,stats,controls}
}
console.log(JSON.stringify(experiment(),null,2));
