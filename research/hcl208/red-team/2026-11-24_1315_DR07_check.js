// DR07 standalone Node.js deterministic checker
function runDR07(){
 const stats={cases:0,sourceSAT:0,sourceUNSAT:0,rootWords:0,featureInsertions:0,featureXors:0,gaussianCalls:0,gaussianXors:0,closurePasses:0,forcedRows:0,eventDeletions:0,guardQueries:0,verifiedLifts:0,rimTruthChecks:0,assertions:0}, groups={};
 function ok(x){stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)}
 let seed=20261124;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 function pop(x){let a=0;while(x){x&=x-1;a++}return a}
 function parity(x){return pop(x)&1}
 function gauss(rows,n){stats.gaussianCalls++;const b=new Map();for(const [mask,rhs] of rows){let a=mask,v=rhs;while(a){const j=31-Math.clz32(a);if(!b.has(j)){b.set(j,[a,v]);break}const [q,w]=b.get(j);a^=q;v^=w;stats.gaussianXors++}if(!a&&v)return null}return b}
 function solve(rows,n){const b=gauss(rows,n);if(!b)return null;let x=0;for(let i=0;i<n;i++)if(b.has(i)){const [a,v]=b.get(i);if(parity(a&x)!==v)x|=1<<i}return x}
 function holds(x,rows){return rows.every(([a,v])=>parity(a&x)===v)}
 function implied(b,row){let [a,v]=row;while(a){const j=31-Math.clz32(a);if(!b.has(j))return false;const [q,w]=b.get(j);a^=q;v^=w;stats.gaussianXors++}return v===0}
 function close(G,E,n){G=G.slice();E=E.slice();while(true){stats.closurePasses++;const g=gauss(G,n);if(!g)return {unsat:true,G,E};let restart=false;const bs=[];for(let i=0;i<E.length;i++){const b=gauss(G.concat(E[i]),n);if(!b){E.splice(i,1);stats.eventDeletions++;restart=true;break}if(b.size===g.size)return {unsat:true,G,E};if(b.size===g.size+1){const [a,v]=E[i].find(row=>!implied(g,row));G.push([a,1-v]);stats.forcedRows++;restart=true;break}bs.push(b)}if(restart)continue;outer:for(let i=0;i<E.length;i++)for(let j=0;j<E.length;j++)if(i!==j&&E[j].every(row=>implied(bs[i],row))){E.splice(i,1);stats.eventDeletions++;restart=true;break outer}if(!restart)return {unsat:false,G,E}}}
 function masks(n,d){return Array.from({length:1<<n},(_,i)=>i).filter(x=>pop(x)<=d)}
 function feat(x,ms){let v=0n;for(let j=0;j<ms.length;j++)if((x&ms[j])===ms[j])v|=1n<<BigInt(j);return v}
 function rank(words,ms){const b=new Map();for(const x of words){stats.featureInsertions++;let v=feat(x,ms);while(v){const j=v.toString(2).length-1;if(!b.has(j)){b.set(j,v);break}v^=b.get(j);stats.featureXors++}}return b.size}
 function rim(bits){const vals=[0,...bits.map(v=>2*v),0];if(vals.length%2===0)vals.push(0);const lists=vals.map(a=>[0,1,2,3].filter(c=>c!==a&&c!==(a^1)));for(const first of lists[0]){let paths=new Map([[first,[first]]]);for(let i=1;i<lists.length;i++){const next=new Map();for(const [last,path] of paths)for(const c of lists[i])if(c!==last&&!next.has(c))next.set(c,path.concat(c));paths=next}for(const [last,path] of paths)if(last!==first)return path}return null}
 function lit(x,l){return ((x>>(Math.abs(l)-1))&1)^(l<0?1:0)}
 function legal(x,F){return F.every(c=>c.some(l=>lit(x,l)))}
 for(let D=1;D<=3;D++){const width=D+4;for(let v=0;v<1<<width;v++){const bits=Array.from({length:width},(_,i)=>(v>>i)&1);const p=rim(bits);ok(Boolean(p)===bits.some(Boolean));if(p){const vals=[0,...bits.map(x=>2*x),0];if(vals.length%2===0)vals.push(0);ok(p.every((x,i)=>x!==vals[i]&&x!==(vals[i]^1)&&x!==p[(i+1)%p.length]))}stats.rimTruthChecks++}}
 function one(F,n,D,group){const k=D+1,N=n+k,T=((1<<k)-1)<<n,G=Array.from({length:k},(_,i)=>[1<<(n+i),1]);const E=F.map(c=>G.concat(c.map(l=>[1<<(Math.abs(l)-1),l<0?1:0])));const root=close([],E,N);ok(!root.unsat&&root.G.length===0);const target=close(G,E,N);const source=Array.from({length:1<<n},(_,i)=>i).filter(x=>legal(x,F));const actual=Array.from({length:1<<N},(_,i)=>i).filter(x=>(x&T)!==T||legal(x,F));stats.rootWords+=1<<N;ok(actual.length===((1<<k)-1)*(1<<n)+source.length);ok(!target.unsat||source.length===0);for(let x=0;x<1<<N;x++)ok(actual.includes(x)===!E.some(e=>holds(x,e)));
 const low=masks(N,D),high=masks(N,k);ok(low.every(x=>actual.includes(x)));ok(rank(low,low)===low.length);ok(rank(actual,high)===high.length-(source.length?0:1));
 for(let j=0;j<4;j++){let A=[];for(let i=0;i<D;i++)A.push([1+rand((1<<N)-1),rand(2)]);if(!gauss(A,N))continue;let w=null;for(let i=0;i<k&&w===null;i++){w=solve(A.concat([[1<<(n+i),0]]),N);stats.guardQueries++}ok(w!==null&&holds(w,A)&&actual.includes(w));for(const c of F){const bits=[...Array.from({length:k},(_,i)=>1-((w>>(n+i))&1)),...c.map(l=>lit(w,l))];ok(rim(bits)!==null);stats.verifiedLifts++}}
 if(source.length){const w=source[0]|T;ok(holds(w,G)&&actual.includes(w));for(const c of F){ok(rim([...Array(k).fill(0),...c.map(l=>lit(w,l))])!==null);stats.verifiedLifts++}}
 stats.cases++;stats[source.length?"sourceSAT":"sourceUNSAT"]++;let g=groups[group]??={cases:0,sourceSAT:0,sourceUNSAT:0,rootFullLow:0,targetClosureReject:0};g.cases++;g[source.length?"sourceSAT":"sourceUNSAT"]++;g.rootFullLow++;if(target.unsat)g.targetClosureReject++;
 }
 const cube=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>(i>>j)&1?-v:v));for(let f=0;f<256;f++)for(let D=1;D<=2;D++)one(cube.filter((_,j)=>(f>>j)&1),3,D,"cube");
 const triples=[];for(let a=1;a<=7;a++)for(let b=a+1;b<=7;b++){const c=a^b;if(c>b)triples.push([a,b,c])}const fano=triples.flatMap(t=>[t,t.map(v=>-v)]);for(let D=1;D<=2;D++){one(fano,7,D,"fano");for(let i=0;i<fano.length;i++)one(fano.filter((_,j)=>j!==i),7,D,"fano")}
 for(let i=0;i<40;i++){const F=[];for(let j=0;j<8;j++){const vs=[];while(vs.length<3){const v=1+rand(5);if(!vs.includes(v))vs.push(v)}F.push(vs.map(v=>rand(2)?v:-v))}one(F,5,1+i%3,"random")}
 return {seed:20261124,stats,groups,limitations:"Finite exhaustive source/chart and feature rank checks; Gaussian closure and low-rank escape queries. Not a general polynomial high-feature acquisition algorithm. No measured CM, strict physical E4/B4 compiler, or full portfolio."}
}
console.log(JSON.stringify(runDR07(),null,2));
