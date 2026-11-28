// Independent root spectral-scope checker, Node.js standard library.
const fs=require('fs'),crypto=require('crypto'),assert=require('assert');
const [input,record]=process.argv.slice(2);const bytes=fs.readFileSync(input),cert=JSON.parse(fs.readFileSync(record));
assert.equal('STRICT-EB4-v1:sha256:'+crypto.createHash('sha256').update(bytes).digest('hex'),cert.instance_id);assert.equal(bytes.length*8,cert.original_N_bits);assert.equal(cert.guard_id,'EMPTY');assert.equal(cert.residual_id,'ROOT');
const g=JSON.parse(bytes),n=4*g.types.length;assert.equal(g.format,'STRICT-EB4-v1');let par=Array.from({length:n},(_,i)=>i),ph=new Uint8Array(n),ports=new Set(),pairs=new Set();
function find(i){let z=0;while(par[i]!==i){z^=ph[i];i=par[i]}return [i,z]}
function join(i,j,b){let [u,x]=find(i),[v,y]=find(j);if(u===v){assert.equal(x^y,b);return}if(u>v){[u,v]=[v,u];[x,y]=[y,x]}par[v]=u;ph[v]=x^y^b}
for(const [u,v,b] of g.edges){assert(u>=0&&v>=0&&u<n&&v<n&&!ports.has(u)&&!ports.has(v));assert(b===0||b===1);let a=Math.floor(u/4),c=Math.floor(v/4);assert.notEqual(a,c);let k=[a,c].sort((x,y)=>x-y).join(',');assert(!pairs.has(k));pairs.add(k);ports.add(u);ports.add(v);join(u,v,b)}assert.equal(ports.size,n);
for(let i=0;i<g.types.length;i++){assert(['E','B'].includes(g.types[i]));if(g.types[i]==='E')for(let j=1;j<4;j++)join(4*i,4*i+j,0)}
const uniq=new Map();for(let i=0;i<g.types.length;i++){if(g.types[i]!=='B')continue;let m=new Map();for(let j=0;j<4;j++){let [u,b]=find(4*i+j);u++;m.set(u,(m.get(u)||0)+(b?-1:1))}let row=[...m].filter(x=>x[1]!==0).sort((a,b)=>a[0]-b[0]);if(row.length)uniq.set(JSON.stringify(row),new Map(row))}
const rows=[...uniq.values()];let blocks=0,tests=0,facts=0;
for(let i=0;i<rows.length;i++)for(let j=i;j<rows.length;j++){const a=rows[i],b=rows[j];if(![...a.keys()].some(x=>b.has(x)))continue;const S=[...new Set([...a.keys(),...b.keys()])],m=S.length,A=S.map(x=>BigInt(a.get(x)||0)),B=S.map(x=>BigInt(b.get(x)||0));const dot=(a,b)=>a.reduce((z,x,k)=>z+x*b[k],0n);const aa=dot(A,A),ab=dot(A,B);const O=B.map((x,k)=>aa*x-ab*A[k]);const oo=dot(O,O);blocks++;
// Orthogonal row-space decomposition, independently of the Gram determinant formula.
function check(u,v,sign){tests++;const ac=A[u]+(v<0?0n:sign*A[v]),oc=O[u]+(v<0?0n:sign*O[v]);const norm=v<0?1n:2n,t=v<0?1n:4n;const den=oo===0n?aa:aa*oo;const num=oo===0n?norm*aa-ac*ac:norm*den-ac*ac*oo-oc*oc*aa;assert(num>=0n);if(BigInt(m)*num<t*den)facts++}
for(let u=0;u<m;u++){check(u,-1,1n);for(let v=u+1;v<m;v++){check(u,v,1n);check(u,v,-1n)}}}
assert.equal(blocks,cert.blocks);assert.equal(tests,cert.tests);assert.equal(facts,cert.facts);console.log(JSON.stringify({blocks,tests,facts,verified:true}));
