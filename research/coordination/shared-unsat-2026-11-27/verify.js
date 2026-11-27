// Verify exact source encodings and reference refutations. Usage: node verify.js benchmarks.json
const fs = require("node:fs");
function audit(bundle){
 const results=[];
 function same(a,b){return JSON.stringify(a)===JSON.stringify(b)}
 function exactlyOne(a,C){C.push(a);for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)C.push([-a[i],-a[j]])}
 for(const x of bundle.instances){
  const lines=x.dimacs.trimEnd().split("\n"),head=lines.shift().split(" "),C=lines.map(l=>l.trim().split(/\s+/).map(Number));
  if(head[0]!=="p"||head[1]!=="cnf"||Number(head[2])!==x.nvars||Number(head[3])!==x.nclauses||C.length!==x.nclauses||x.dimacs.length*8!==x.encoded_bits_ascii)throw Error(x.id+" header");
  for(const c of C){if(c.pop()!==0||c.some(l=>!Number.isInteger(l)||l===0||Math.abs(l)>x.nvars))throw Error(x.id+" literal")}
  const D=[],s=x.source;let nodes=0;
  if(x.id.startsWith("PHP-")){const k=s.holes;for(let i=0;i<k+1;i++)exactlyOne(Array.from({length:k},(_,j)=>i*k+j+1),D);for(let j=0;j<k;j++)for(let a=0;a<k+1;a++)for(let b=a+1;b<k+1;b++)D.push([-(a*k+j+1),-(b*k+j+1)])}
  else if(x.id.startsWith("TSEITIN-")){const I=Array.from({length:s.side*s.side},()=>[]);s.edges.forEach(([a,b],j)=>{if(a===b)throw Error("loop");I[a].push(j+1);I[b].push(j+1)});for(let v=0;v<I.length;v++){if(I[v].length!==4)throw Error("degree");for(let k=0;k<16;k++){const bits=Array.from({length:4},(_,i)=>(k>>i)&1);if(bits.reduce((a,b)=>a^b,0)!==Number(v===0))D.push(I[v].map((e,i)=>bits[i]?-e:e))}}}
  else if(x.id.startsWith("ODD-WHEEL-")){if(s.rim%2!==1)throw Error("even rim");const E=[];for(let i=1;i<=s.rim;i++)E.push([0,i]);for(let i=1;i<=s.rim;i++)E.push([i,1+i%s.rim]);if(!same(E,s.edges))throw Error("wheel");for(let v=0;v<=s.rim;v++)exactlyOne([3*v+1,3*v+2,3*v+3],D);for(const [a,b] of E)for(let c=1;c<=3;c++)D.push([-(3*a+c),-(3*b+c)])}
  else if(x.id.startsWith("CYCLIC-3DM-")||x.id==="JOINT-24"){const n=s.order,E=s.triples;for(let p=0;p<3;p++)for(let v=0;v<n;v++)exactlyOne(E.map((e,j)=>e[p]===v?j+1:0).filter(Boolean),D);if(x.id.startsWith("CYCLIC-")){if(n%2||E.some(([a,b,c])=>(a+b-c)%n!==0))throw Error("modular proof")}else{let count=0;function rec(row,usedY,usedZ){nodes++;if(row===n){count++;return}for(const [a,b,c] of E)if(a===row&&!usedY.has(b)&&!usedZ.has(c))rec(row+1,new Set([...usedY,b]),new Set([...usedZ,c]))}rec(0,new Set(),new Set());if(count)throw Error("joint cover")}}
  else if(x.id.startsWith("EQUALITY-")){const k=s.chain;for(let i=1;i<k;i++)D.push([-i,i+1],[i,-i-1]);D.push([-k,-1],[k,1])}
  else if(x.id.startsWith("RANDOM-")){function walk(t,a){nodes++;while(true){let changed=false;for(let j=0;j<C.length;j++){let un=[];let sat=false;for(const l of C[j]){if(!a[Math.abs(l)])un.push(l);else if(a[Math.abs(l)]===Math.sign(l)){sat=true;break}}if(sat)continue;if(!un.length)return t.conflict===j+1;if(un.length===1){a[Math.abs(un[0])]=Math.sign(un[0]);changed=true}}if(!changed)break}const v=t.split;if(!Number.isInteger(v)||v<1||v>x.nvars||a[v])return false;const p=a.slice(),q=a.slice();p[v]=1;q[v]=-1;return walk(t.positive,p)&&walk(t.negative,q)}if(!walk(x.reference_tree,new Int8Array(x.nvars+1)))throw Error("tree");results.push({id:x.id,status:"verified tree",nodes});continue}
  else throw Error("unknown instance");
  if(!same(C,D))throw Error(x.id+" reconstruction mismatch");results.push({id:x.id,status:"verified structural encoding",...(nodes?{reference_nodes:nodes}:{})});
 }
 return results;
}
console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2], "utf8"))), null, 2));
