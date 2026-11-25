// node S23_check.js S23_inputs.json
const fs=require('fs'), data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
function run(data){
let seed=20261125, tests=0, rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n);};
function ok(x){tests++;if(!x)throw Error('assertion '+tests);}
function basis(rows){let b=[];for(let x of rows){for(const y of b)if((x^y)<x)x^=y;if(x){b.push(x);b.sort((a,b)=>a>b?-1:a<b?1:0);}}return b;}
function span(b){let s=[0n];for(let x of b)s=s.concat(s.map(y=>x^y));return s;}
function bit(x){let p=0;while(x){p^=1;x&=x-1n;}return p;}
function obs(rows,x){return rows.reduce((z,r,i)=>z|(bit(r&x)<<i),0);}
function accept(o,x){return o.allowed.includes(obs(o.rows,x));}
function gate(a,t,d){let q=1n<<BigInt(d),p=x=>BigInt(x)**4n;return t>0&&q*p(t+1)+p(a+1)<p(a+t+1);}
function old(a,b,d){let q=1n<<BigInt(d);return q*BigInt(b+1)<=BigInt(a+b+1)&&2n*BigInt(d)*q<=BigInt(b-1);}
let result={seed:20261125,random:{sat:0,unsat:0,queries:0,lifts:0,closureScans:0,forces:0,rankMassFailures:0},shared:[],gates:{newOnly:0,oldOnly:0}};
for(let t=0;t<240;t++){
 let n=3+rand(5), N=1<<n, sides=[[],[]];
 for(let j=0;j<2;j++)for(let k=0;k<1+rand(6);k++){
  let rows=basis(Array.from({length:1+rand(3)},()=>BigInt(1+rand(N-1))));
  let allowed=Array.from({length:1<<rows.length},(_,i)=>i).filter(()=>rand(3)!==0);
  sides[j].push({rows,allowed});
 }
 let all=Array.from({length:N},(_,i)=>BigInt(i)), words=all.slice(), force=[];
 let changed=true;while(changed&&words.length){changed=false;outer:for(let o of sides.flat()){
  result.random.closureScans++;let local=words.filter(x=>accept(o,x));
  if(!local.length){words=[];changed=true;break;}
  for(let r=1n;r<BigInt(N);r++){let v=bit(r&local[0]);if(local.every(x=>bit(r&x)===v)&&words.some(x=>bit(r&x)!==v)){
   words=words.filter(x=>bit(r&x)===v);force.push(r);result.random.forces++;changed=true;break outer;
  }}
 }}
 let ref=all.filter(x=>sides.flat().every(o=>accept(o,x)));ok(ref.every(x=>words.includes(x)));
 let H=basis(force), reduce=x=>{for(let y of H)if((x^y)<x)x^=y;return x;};
 let projected=sides.map(os=>os.map(o=>basis(o.rows.map(reduce))));
 let [u,v]=projected.map(os=>basis(os.flat()));let vs=new Set(span(v));let I=basis(span(u).filter(x=>vs.has(x)));
 let h=basis([...H,...I]), d=I.length, tprivate=v.length-d;
 ok(basis([...h,...sides[1].flatMap(o=>o.rows)]).length-h.length===tprivate);
 let b=projected[1].reduce((s,r)=>s+r.length,0);
 let b2=sides[1].reduce((s,o)=>s+basis([...h,...o.rows]).length-h.length,0);
 if(b2>b-d)result.random.rankMassFailures++;
 let table=new Map();for(let k=0;k<(1<<d);k++){
  result.random.queries++;let x=words.find(x=>obs(I,x)===k&&sides[1].every(o=>accept(o,x)));if(x!==undefined)table.set(k,x);
 }
 let a=words.find(x=>sides[0].every(o=>accept(o,x))&&table.has(obs(I,x)));
 ok((a!==undefined)===(ref.length>0));
 if(a!==undefined){let z=table.get(obs(I,a));let lift=words.find(x=>obs(u,x)===obs(u,a)&&obs(v,x)===obs(v,z));ok(lift!==undefined&&sides.flat().every(o=>accept(o,lift)));result.random.sat++;result.random.lifts++;}
 else result.random.unsat++;
}
for(const {id,n,O,pins} of data){
 let m=O.length,rows=O.map(o=>[(1n<<BigInt(o.t[0]))^(1n<<BigInt(o.t[1])),(1n<<BigInt(o.t[0]))^(1n<<BigInt(o.t[2]))]);
 let sets=new Map(),add=L=>{if(!L.length||L.length===m)return;let S=new Set(L);if(S.size>m/2)S=new Set(Array.from({length:m},(_,i)=>i).filter(i=>!S.has(i)));let k=[...S].sort((a,b)=>a-b).join(',');sets.set(k,S);};
 for(let i=0;i<m;i++){add([i]);for(let j=i+1;j<m;j++){add([i,j]);for(let k=j+1;k<m;k++)add([i,j,k]);}}
 for(let v=0;v<n;v++)add(O.map((o,i)=>o.t.includes(v)?i:-1).filter(i=>i>=0));
 for(let i=0;i<m;i++){let order=[i],seen=new Set(order);for(let p=0;p<order.length;p++){let v=O[order[p]].t;for(let j=0;j<m;j++)if(!seen.has(j)&&O[j].t.some(t=>v.includes(t))){seen.add(j);order.push(j);}}for(let k=1;k<order.length;k++)add(order.slice(0,k));}
 for(let mask=1;mask<15;mask++)add(O.map((o,i)=>mask>>o.p&1?i:-1).filter(i=>i>=0));
 let s={id,n,m,cuts:sets.size,newEligible:0,oldEligible:0,examples:[],guardJobs:pins.length,closureScans:0};
 for(let pin of pins)for(let o of O){s.closureScans++;ok(o.t.filter(v=>pin!==-1&&v===0).length<=1);}
 let total=basis(rows.flat()).length;
 for(let S of sets.values()){let A=[],B=[];for(let i=0;i<m;i++)(S.has(i)?B:A).push(...rows[i]);let a=basis(A).length,b=basis(B).length,d=a+b-total;
 if(gate(a,b-d,d)||gate(b,a-d,d)){s.newEligible++;if(s.examples.length<4)s.examples.push({owners:[...S],a,b,d});}if(old(A.length,B.length,d))s.oldEligible++;
 }
 result.shared.push(s);
}
// Local rank-mass counterexample: two independent rank-one owners, seam their sum.
ok(basis([1n,2n]).length===2&&basis([3n,1n]).length===2&&basis([3n,2n]).length===2);
result.assertions=tests;return result;
}
if(require.main===module)console.log(JSON.stringify(run(data),null,2));
