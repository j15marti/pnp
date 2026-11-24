const run = function(){
 const A=(x,m="assert")=>{if(!x)throw Error(m)};
 const stat={physicalGraphs:0,physicalMatchings:0,closureCalls:0,deletedRows:0,joinAttempts:0,peakStates:0,witnesses:0};
 function basis(vs){let b=new Map();for(let x of vs){while(x){let k=x.toString(2).length-1;if(b.has(k))x^=b.get(k);else{b.set(k,x);break}}}return b}
 function contains(b,x){while(x){let k=x.toString(2).length-1;if(!b.has(k))return false;x^=b.get(k)}return true}
 function aff(rows){let a=0n,ds=[];for(const r of rows){a^=r[0].tag;for(const x of r)ds.push(x.tag^r[0].tag)}return {a,b:basis(ds)}}
 // k internally disjoint length-three paths. All vertices required.
 function selector(tags){const k=tags.length,n=2+2*k,edges=[];for(let i=0;i<k;i++){let a=2+2*i,b=a+1;edges.push([0,a,tags[i]],[a,b,0n],[b,1,0n])}let found=new Map(),count=0;
 function rec(rem,s,path){if(!rem){count++;let old=found.get(s);if(old)old.mult++;else found.set(s,{tag:s,mult:1n,path:[...path]});return}let u=0;while(!(rem&(1<<u)))u++;for(let i=0;i<edges.length;i++){let [a,b,t]=edges[i];let v=a===u?b:b===u?a:-1;if(v>=0&&(rem&(1<<v)))rec(rem^(1<<u)^(1<<v),s^t,[...path,i])}}
 rec((1<<n)-1,0n,[]);A(count===k);stat.physicalGraphs++;stat.physicalMatchings+=count;let want=new Map();for(const t of tags)want.set(t,(want.get(t)||0n)+1n);A(want.size===found.size);for(const [t,c] of want)A(found.get(t).mult===c);return [...found.values()].map(r=>({...r,edges,n}));
 }
 function verify(r){let used=0,s=0n;for(const i of r.path){let [a,b,t]=r.edges[i];A(!(used&(1<<a))&&!(used&(1<<b)));used|=(1<<a)|(1<<b);s^=t}A(used===(1<<r.n)-1&&s===r.tag)}
 function close(rows,target){rows=rows.map(r=>r.slice());while(true){stat.closureCalls++;if(rows.some(r=>!r.length))return null;let changed=false;for(let i=0;i<rows.length&&!changed;i++){let {a,b}=aff(rows.filter((_,j)=>j!==i));for(let j=0;j<rows[i].length;j++){if(!contains(b,target^a^rows[i][j].tag)){rows[i].splice(j,1);stat.deletedRows++;changed=true;break}}}if(!changed)return rows}}
 function solve(rows,target=0n){const all=aff(rows),rnk=all.b.size;let q=close(rows,target);if(!q)return {count:0n,width:0,rank:rnk,peak:0};let suffix=[];for(let i=0;i<=q.length;i++)suffix.push(aff(q.slice(i)));let width=0,peak=1;let tab=new Map([[0n,{count:1n,prev:null}]]);
 for(let i=0;i<q.length;i++){let p=aff(q.slice(0,i+1));let w=p.b.size+suffix[i+1].b.size-aff(q).b.size;width=Math.max(width,w);let next=new Map();for(const [s,entry] of tab)for(const r of q[i]){stat.joinAttempts++;let t=s^r.tag;if(!contains(suffix[i+1].b,target^t^suffix[i+1].a))continue;let old=next.get(t);let c=entry.count*r.mult;if(old)old.count+=c;else next.set(t,{count:c,prev:entry,row:r})}tab=next;A(tab.size<=2**w);peak=Math.max(peak,tab.size);if(!tab.size)break}
 stat.peakStates=Math.max(stat.peakStates,peak);let end=tab.get(target);if(!end)return {count:0n,width,rank:rnk,peak};let s=0n,n=0;for(let x=end;x.row;x=x.prev){verify(x.row);s^=x.row.tag;n++}A(s===target&&n===q.length);stat.witnesses++;return {count:end.count,width,rank:rnk,peak}
 }
 function compile(n,E,k){let rows=[];for(let v=0;v<n;v++){let t=[];for(let c=0;c<k;c++){let x=0n;E.forEach(([a,b],i)=>{if(a===v||b===v)x^=BigInt(c)<<BigInt(2*i)});t.push(x)}rows.push(selector(t))}
 E.forEach(([a,b,s=0],i)=>{rows.push(selector([0,1,2,3].filter(c=>c!==s).map(c=>BigInt(c)<<BigInt(2*i))))});return rows}
 function ref(n,E,k){let cnt=0n,x=Array(n).fill(0);function visit(i){if(i===n){if(E.every(([a,b,s=0])=>(x[a]^x[b])!==s))cnt++;return}for(let c=0;c<k;c++){x[i]=c;visit(i+1)}}visit(0);return cnt}
 function edges(n){let a=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)a.push([i,j,0]);return a}
 let seed=11241120;function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 let random={cases:0,sat:0,unsat:0};for(let k of [3,4])for(let z=0;z<60;z++){let n=3+rng()%4,E=edges(n).filter(()=>rng()%5<3).map(([a,b])=>[a,b,z%2?rng()%4:0]);let got=solve(compile(n,E,k)),want=ref(n,E,k);A(got.count===want,"random count");random.cases++;random[want?"sat":"unsat"]++}
 let controls=[];for(let k of [3,4]){let E=edges(k+1);for(let d=-1;d<E.length;d++){let F=E.filter((_,j)=>j!==d),got=solve(compile(k+1,F,k)),want=ref(k+1,F,k);A(got.count===want);A((want>0n)===(d>=0));controls.push({k,deleted:d,count:String(want),rank:got.rank,width:got.width,peak:got.peak})}}
 // Every component has rank <=1; no enumeration of global words: Gaussian membership.
 let linear={cases:0,sat:0,unsat:0};for(let z=0;z<100;z++){let rows=[];for(let i=0;i<8;i++)rows.push(selector([BigInt(rng()%64),BigInt(rng()%64)]));let target=BigInt(rng()%128),{a,b}=aff(rows);let got=solve(rows,target);A((got.count>0n)===contains(b,target^a));linear.cases++;linear[got.count?"sat":"unsat"]++}
 // Process disconnected graph copies in contiguous order, with globally distinct syndrome coordinates.
 let scales=[];for(let copies of [1,4,8,16])for(let bad of [false,true]){let rows=[],offset=0,expected=1n;for(let j=0;j<copies;j++){let E=edges(5);if(!bad||j!==copies-1)E.pop();let local=compile(5,E,4);for(let r of local){for(let x of r){x.tag<<=BigInt(offset);x.edges=x.edges.map(([a,b,t])=>[a,b,t<<BigInt(offset)])}rows.push(r)}offset+=2*E.length;expected*=ref(5,E,4)}let got=solve(rows);A(got.count===expected);scales.push({copies,bad,rank:got.rank,width:got.width,peak:got.peak,count:String(got.count)})}
 return {seed:11241120,random,linear,controls,scales,stat};
};
console.log(JSON.stringify(run(),null,2));
