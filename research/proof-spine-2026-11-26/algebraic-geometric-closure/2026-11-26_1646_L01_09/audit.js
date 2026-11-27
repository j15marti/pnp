'use strict';
function audit(){
 const R={A:{},B:{},C:{},integrated:{},assertions:0};
 const ok=(x,m)=>{R.assertions++;if(!x)throw Error(m)};
 const id=(n,i,j)=>i*n+j;
 function perms(a){if(a.length===0)return [[]];let out=[];for(let i=0;i<a.length;i++)for(const p of perms(a.slice(0,i).concat(a.slice(i+1))))out.push([a[i],...p]);return out}
 function allTours(n){return perms(Array.from({length:n-1},(_,i)=>i+1)).map(p=>{let a=[0,...p],m=0n;for(let i=0;i<n;i++)m|=1n<<BigInt(id(n,a[i],a[(i+1)%n]));return m})}
 function valid(n,S){let next=Array(n).fill(-1),ind=Array(n).fill(0);if(S.size!==n)return false;for(const e of S){let a=Math.floor(e/n),b=e%n;if(a===b||next[a]!==-1)return false;next[a]=b;ind[b]++}if(ind.some(x=>x!==1))return false;let seen=new Set(),v=0;for(let k=0;k<n;k++){if(seen.has(v))return false;seen.add(v);v=next[v]}return v===0&&seen.size===n}
 function toSet(n,m){let s=new Set();for(let e=0;e<n*n;e++)if((m>>BigInt(e))&1n)s.add(e);return s}
 function maskOf(s){let m=0n;for(const e of s)m|=1n<<BigInt(e);return m}
 function block(n){let k=Math.floor(n/3),pairs=[],tail=[];for(let i=0;i<k;i++){let a=3*i,b=a+1,c=a+2,t=(a+3)%n;pairs.push([[id(n,a,b),id(n,b,c),id(n,c,t)],[id(n,a,c),id(n,c,b),id(n,b,t)]])}for(let i=3*k;i<n;i++)tail.push(id(n,i,(i+1)%n));return {pairs,tail}}
 function accepts(B,S){return B.tail.every(x=>S.has(x))&&B.pairs.every(p=>p.some(q=>q.every(x=>S.has(x))))}
 function lift(B,choose){let s=new Set(B.tail);for(let i=0;i<B.pairs.length;i++)for(let e of B.pairs[i][choose(i)])s.add(e);return s}
 function availableLift(B,S){return lift(B,i=>B.pairs[i][0].every(e=>S.has(e))?0:1)}
 function majority(a,b,c){return (a&b)|(a&c)|(b&c)}
 function countBits(x){let n=0;while(x){x&=x-1n;n++}return n}
 function isClosed(T){let set=new Set(T);for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++)for(let k=j+1;k<T.length;k++)if(!set.has(majority(T[i],T[j],T[k])))return false;return true}
 function verifyCapacity(n,T){if(T.length===0)return;ok(isClosed(T),"input not majority closed");let U=0n,I=T[0];for(const t of T){U|=t;I&=t}let free=U^I,groups=new Map();for(let e=0;e<n*n;e++){if(!(free&(1n<<BigInt(e))))continue;let signature=T.map(t=>Number((t>>BigInt(e))&1n)).join(""),comp=signature.replace(/[01]/g,x=>x==="0"?"1":"0"),key=signature<comp?signature:comp;groups.set(key,(groups.get(key)??0n)|(1n<<BigInt(e)))}ok(countBits(free)<=2*n,"free bits cap");for(let g of groups.values()){ok(countBits(g)>=6,"group smaller than 6");ok(T.some(t=>T.includes(t^g)),"no single equivalence-group flip")}ok(groups.size<=Math.floor(n/3),"group cap");ok(T.length<=2**groups.size,"solution cap");}
 let smallMasks=0,smallSources=0,tightCount=0;
 for(let n=2;n<=4;n++){let B=block(n),tours=allTours(n),E=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)E.push(id(n,i,j));let chartTours=[];for(let i=0;i<2**B.pairs.length;i++)chartTours.push(maskOf(lift(B,j=>(i>>j)&1)));for(let m=0;m<2**E.length;m++){let S=new Set(E.filter((_,j)=>(m>>j)&1)),m0=maskOf(S),pred=accepts(B,S),ref=chartTours.some(t=>(t&m0)===t),hc=tours.some(t=>(t&m0)===t);ok(pred===ref,"chart vs enumeration");if(pred){ok(hc,"unsound constructive chart");let w=availableLift(B,S);ok(valid(n,w)&&[...w].every(e=>S.has(e)),"witness lift")}smallMasks++;smallSources++}}
 for(let n=2;n<=15;n++){let B=block(n),T=[];for(let c=0;c<2**B.pairs.length;c++){let s=lift(B,i=>(c>>i)&1);ok(valid(n,s)&&accepts(B,s),"tight chart tour");T.push(maskOf(s));tightCount++}ok(new Set(T).size===2**Math.floor(n/3),"duplicate tight tours");verifyCapacity(n,T)}
 R.A={smallMasks,smallSourceReferenceComparisons:smallSources,tightWitnesses:tightCount,largestExhaustiveTightN:15};
 let subsetCounts=[],tripleCounts=[],closedTripleHulls=0;
 for(let n=2;n<=4;n++){let T=allTours(n),max=0,closed=0;for(let m=0;m<2**T.length;m++){let S=T.filter((_,j)=>(m>>j)&1);if(isClosed(S)){closed++;verifyCapacity(n,S);max=Math.max(max,S.length)}}ok(max===2**Math.floor(n/3),"exhaustive maximum");subsetCounts.push({n,tours:T.length,subsets:2**T.length,closed,max})}
 for(let n=3;n<=6;n++){let T=allTours(n),U=new Set(T),total=0,validMaj=0,missing=0,hulls=new Set();for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++)for(let k=j+1;k<T.length;k++){let a=T[i],b=T[j],c=T[k],m=majority(a,b,c);total++;if(U.has(m)){validMaj++;let S=[...new Set([a,b,c,m])];let key=S.map(x=>x.toString()).sort().join(",");if(!hulls.has(key)){hulls.add(key);ok(isClosed(S),"triple hull not closed");verifyCapacity(n,S);closedTripleHulls++}}else{missing++;ok(!valid(n,toSet(n,m)),"majority reference disagreement")}}ok(total===validMaj+missing,"triple accounting");tripleCounts.push({n,total,validMaj,nonTourMaj:missing,distinctValidHulls:hulls.size})}
 R.B={subsetCounts,tripleCounts,closedTripleHulls};
 let faceTests=0,faceTriples=0,projectedMasks=0,projectedTriples=0,plainComparisons=0;
 for(let em=0;em<16;em++){let E=[];for(let i=0;i<2;i++)for(let j=0;j<2;j++)if((em>>(2*i+j))&1)E.push([i,2+j]);let T=[];for(let z=0;z<16;z++)if(E.every(([i,j])=>!((z>>i)&1)||!((z>>j)&1)))T.push(z);
 for(let q=0;q<81;q++){let tmp=q,weights=[];for(let i=0;i<4;i++){weights.push(tmp%3-1);tmp=Math.floor(tmp/3)}let score=z=>weights.reduce((s,w,i)=>s+w*((z>>i)&1),0),mn=Math.min(...T.map(score)),F=T.filter(z=>score(z)===mn);let fs=new Set(F);for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++)for(let k=j+1;k<F.length;k++){let a=F[i],b=F[j],c=F[k];ok(fs.has((a&b)|(a&c)|(b&c)),"fixed optimum face majority");faceTriples++}faceTests++;
 let req=Array.from({length:4},(_,v)=>[0,1].map(l=>(em*13+q*7+v*5+l*3+v*l)%8));
 let A=[];for(let m=0;m<8;m++){let av=(v,l)=>(req[v][l]&m)===req[v][l],adm=z=>Array.from({length:4},(_,v)=>v).every(v=>av(v,(z>>v)&1)),plain=T.some(adm),formula=Array.from({length:4},(_,v)=>v).every(v=>av(v,0)||av(v,1))&&E.every(([u,v])=>av(u,0)||av(v,0));ok(plain===formula,"mask projection");plainComparisons++;if(F.some(adm))A.push(m);projectedMasks++}
 let as=new Set(A);for(let i=0;i<A.length;i++)for(let j=i+1;j<A.length;j++)for(let k=j+1;k<A.length;k++){let a=A[i],b=A[j],c=A[k];ok(as.has((a&b)|(a&c)|(b&c)),"optimum-mask projection not majority closed");projectedTriples++}}}
 // Independent 2x2 perfect matching blocks and exhaustive 3x3 matching control.
 function matching(n,E){let mt=Array(n).fill(-1);function aug(i,seen){for(let j=0;j<n;j++)if(E.has(i*n+j)&&!seen.has(j)){seen.add(j);if(mt[j]===-1||aug(mt[j],seen)){mt[j]=i;return true}}return false}for(let i=0;i<n;i++)if(!aug(i,new Set()))return false;return true}
 let matchChecks=0;let P=perms([0,1,2]);for(let m=0;m<512;m++){let E=new Set(Array.from({length:9},(_,i)=>i).filter(i=>(m>>i)&1));ok(matching(3,E)===P.some(p=>p.every((j,i)=>E.has(3*i+j))),"matching control");matchChecks++}
 let matchBlockWitnesses=0;for(let n of [2,4,6,8]){let count=2**(n/2);for(let m=0;m<count;m++){let p=[];for(let i=0;i<n;i+=2){let f=(m>>(i/2))&1;p.push(i+f,i+1-f)}ok(new Set(p).size===n,"matching block lift");matchBlockWitnesses++}}
 let parity=new Set([0,3,5,6]);ok(!parity.has((3&5)|(3&6)|(5&6)),"affine majority counterexample");
 // A single incidence edge in signed projection: fixing original-side labels selected
 // leaves a nonzero term of weight 1, even when a projected input variable is zero.
 let signedWeights=[];for(let z=0;z<8;z++){let a=z&1,b=(z>>1)&1,h=(z>>2)&1;if(h&&(a||b))continue;let w=(a?1:0)*(b?1:1)*(h?-1:1);signedWeights.push({z,w})}ok(signedWeights.some(x=>x.z===3&&x.w===1),"signed term");
 R.C={faceTests,faceTriples,projectedMasks,projectedTriples,plainComparisons,matchChecks,matchBlockWitnesses,affineMajorityFalsifier:true,signedWeights};
 // Integration: same complete source, tight chart, exact reconstruction and guarded neighbors.
 let rows=[];
 for(let n of [6,12,32,64,128,256]){let B=block(n),S=lift(B,i=>i%2),union=new Set(B.tail);for(let p of B.pairs)for(let q of p)for(let e of q)union.add(e);let w=availableLift(B,union);ok(valid(n,w)&&accepts(B,union),"union lift");let bad=new Set(S),removed=[...S].find(e=>Math.floor(e/n)===0);bad.delete(removed);ok(!accepts(B,bad)&&![...bad].some(e=>Math.floor(e/n)===0),"exact cycle NO");let badU=new Set(union);for(let e of union)if(Math.floor(e/n)===0)badU.delete(e);ok(!accepts(B,badU)&&![...badU].some(e=>Math.floor(e/n)===0),"union NO");let restored=new Set(badU);restored.add(removed);ok(accepts(B,restored),"restored YES");let wr=availableLift(B,restored);ok(valid(n,wr)&&[...wr].every(e=>restored.has(e)),"restored lift");let units=0,variable=0;for(let p of B.pairs){let supports=p.filter(q=>q.every(e=>restored.has(e)));ok(supports.length>0,"closure failed");if(supports.length===1)units+=3;else variable+=3}ok(units===3,"expected fixed block");rows.push({n,originalBits:n*(n-1),tightWitnessCount:(1n<<BigInt(B.pairs.length)).toString(),unionEdges:union.size,exactNeighborYES:true,exactNeighborNO:true,unionNeighborYES:true,unionNeighborNO:true,restoredForcedBlockRows:units,restoredVariableBlockRows:variable})}
 R.integrated={rows,neighborPairs:2*rows.length,originalIdConvention:"edge (i,j), i*n+j internal sparse index; original loopless adjacency bit list lexicographic"};
 return R
}
console.log(JSON.stringify(audit(),null,2));
