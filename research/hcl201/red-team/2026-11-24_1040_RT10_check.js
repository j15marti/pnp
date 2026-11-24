function run(){
 const assert=(v,m)=>{if(!v)throw Error(m)};
 const stats={seed:1040,cover_cases:0,cover_sat:0,cover_unsat:0,cover_nodes:0,closure_scans:0,lp_witnesses:0,signed_witnesses:0,primal_witnesses:0,planted_covers:0,neighbor_cases:0,bundle_masks:0,bundle_projected_checks:0,dp_cases:0,dp_states:0,dp_sat:0,dp_unsat:0,scale:[]};
 let seed=1040;function rand(n){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%n}
 function model(n,F){
  let r=0;const C=[],blocks=[],conflicts=[],planted=[],frac=[],signed=[];
  function block(size,p,f,z){const b=Array.from({length:size},()=>r++);blocks.push(C.length);C.push(b);b.forEach((v,i)=>{planted[v]=+(i===p);frac[v]=f[i];signed[v]=z[i]});return b}
  const [off,on]=block(2,0,[0,6],[0,1]);
  const xs=Array.from({length:n},()=>block(2,0,[3,3],[1,0]));
  function conflict(a,b){const p=1-planted[a]-planted[b],f=6-frac[a]-frac[b],z=1-signed[a]-signed[b];assert(p===0||p===1,"planted conflict");const [s]=block(2,p?0:1,[f,6-f],[z,1-z]);C.push([a,b,s]);conflicts.push([a,b,s])}
  xs.forEach(v=>conflict(off,v[1]));
  F.forEach(cl=>{const b=block(4,0,[0,2,2,2],[0,1,0,0]);conflict(on,b[0]);for(let j=0;j<3;j++){conflict(off,b[j+1]);let l=cl[j],bad=xs[Math.abs(l)-1][l>0?0:1];conflict(b[j+1],bad)}});
  return {r,C,blocks,on,off,planted,frac,signed}
 }
 function check(C,x,target=1){return C.every(c=>c.reduce((a,i)=>a+x[i],0)===target)}
 function solve(r,C,guard=[]){
  function go(x){stats.cover_nodes++;let changed=true;while(changed){changed=false;for(const c of C){stats.closure_scans++;let ones=0,u=[];for(const i of c){if(x[i]===1)ones++;else if(x[i]===-1)u.push(i)}if(ones>1||(!ones&&!u.length))return null;if(ones===1||u.length===1){for(const i of u){x[i]=ones?0:1;changed=true}}}}let p=x.indexOf(-1);if(p<0)return x;let best=Infinity;for(const c of C){let u=c.filter(i=>x[i]===-1);if(u.length&&u.length<best){p=u[0];best=u.length}}for(const b of [0,1]){const y=x.slice();y[p]=b;const z=go(y);if(z)return z}return null}
  const x=Array(r).fill(-1);for(const [i,v] of guard){if(x[i]!==-1&&x[i]!==v)return null;x[i]=v}return go(x)
 }
 function brute(n,F){for(let x=0;x<2**n;x++)if(F.every(c=>c.some(l=>Boolean(x&(1<<(Math.abs(l)-1)))===(l>0))))return true;return false}
 function test(n,F,expected,neighbor=false){const m=model(n,F);assert(check(m.C,m.planted),"planted");stats.planted_covers++;
 const primal=Array(m.C.length).fill(0);m.blocks.forEach(i=>primal[i]=1);const counts=Array(m.r).fill(0);m.C.forEach((c,j)=>c.forEach(i=>counts[i]+=primal[j]));assert(counts.every(v=>v===1),"primal");stats.primal_witnesses++;
 assert(m.frac.every(v=>v>=0&&v<=6)&&m.frac[m.on]===6&&check(m.C,m.frac,6),"fraction");stats.lp_witnesses++;
 assert(m.signed[m.on]===1&&check(m.C,m.signed),"signed");stats.signed_witnesses++;
 const w=solve(m.r,m.C,[[m.on,1]]);assert(!!w===expected,"cover decision");if(w)assert(check(m.C,w)&&w[m.on]===1,"cover lift");const off=solve(m.r,m.C,[[m.on,0]]);assert(off&&off.every((v,i)=>v===m.planted[i]),"off cover");
 stats.cover_cases++;stats[expected?"cover_sat":"cover_unsat"]++;if(neighbor)stats.neighbor_cases++;return m}
 // Actual fixed-net, width-two four-class physical totals and their projections.
 const support=new Set();for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++)for(let d=0;d<3;d++){stats.bundle_masks++;if(a+b+c+d===2)support.add((a%2)|((b%2)<<1)|((c%2)<<2)|((d%2)<<3))}
 assert(support.size===7&& !support.has(15),"bundle support");
 for(let mask=1;mask<8;mask++){const proj=new Set([...support].map(v=>{let t=v&mask,k=0;while(t){k^=t&1;t>>=1}return k}));assert(proj.size===2,"one-bit");stats.bundle_projected_checks++}
 for(let a=1;a<8;a++)for(let b=a+1;b<8;b++){const parity=t=>{let k=0;while(t){k^=t&1;t>>=1}return k};assert(new Set([...support].map(v=>parity(v&a)+2*parity(v&b))).size===4,"two-bit");stats.bundle_projected_checks++}
 // Random source controls, proper 3-CNF.
 for(let t=0;t<48;t++){let n=3+rand(4),m=1+rand(18),F=[];for(let j=0;j<m;j++){let v=[];while(v.length<3){let k=1+rand(n);if(!v.some(l=>Math.abs(l)===k))v.push(rand(7)<3?-k:k)}F.push(v)}test(n,F,brute(n,F))}
 let F=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>i&(1<<j)?v:-v)),n=3;
 for(let h=0;h<=4;h++){const m=test(n,F,false);for(let j=0;j<F.length;j++){const G=F.filter((_,i)=>i!==j);assert(brute(n,G),"source neighbor");test(n,G,true,true)}stats.scale.push({splits:h,source_variables:n,source_clauses:F.length,rows:m.r,columns:m.C.length,incidences:m.C.reduce((a,c)=>a+c.length,0),sat_neighbors:F.length});const [a,b,c]=F[0];const z=++n,d=++n;F=[[a,b,z],[-z,c,d],[-z,c,-d],...F.slice(1)]}
 // FPT exceptional-column solver: singleton pins and pair edges via complementary components.
 function dp(r,C,guard=[]){const adj=Array.from({length:r},()=>[]),pins=guard.slice(),high=[];for(const c of C){if(c.length===0)return null;if(c.length===1)pins.push([c[0],1]);else if(c.length===2){adj[c[0]].push(c[1]);adj[c[1]].push(c[0])}else high.push(c)}
 const comp=Array(r).fill(-1),par=Array(r).fill(0),groups=[];for(let i=0;i<r;i++)if(comp[i]<0){let q=[i],j=groups.length;comp[i]=j;for(let a=0;a<q.length;a++){let v=q[a];for(const u of adj[v]){if(comp[u]<0){comp[u]=j;par[u]=1^par[v];q.push(u)}else if(par[u]===par[v])return null}}groups.push(q)}
 const fixed=Array(groups.length).fill(-1);for(const [i,b] of pins){let v=b^par[i],j=comp[i];if(fixed[j]>=0&&fixed[j]!==v)return null;fixed[j]=v}
 let map=new Map([[0n,[]]]);for(let j=0;j<groups.length;j++){let next=new Map();for(const b of fixed[j]<0?[0,1]:[fixed[j]]){let mask=0n,valid=true;for(let a=0;a<high.length;a++){let count=0;for(const i of high[a])if(comp[i]===j)count+=b^par[i];if(count>1){valid=false;break}if(count)mask|=1n<<BigInt(a)}if(!valid)continue;for(const [s,p] of map){stats.dp_states++;if(!(s&mask)&&!next.has(s|mask))next.set(s|mask,[...p,b])}}map=next;if(!map.size)return null}const p=map.get((1n<<BigInt(high.length))-1n);return p?comp.map((j,i)=>p[j]^par[i]):null}
 for(let t=0;t<180;t++){let r=2+rand(8),c=1+rand(10),C=[];for(let j=0;j<c;j++){let k=1+rand(Math.min(4,r)),s=new Set();while(s.size<k)s.add(rand(r));C.push([...s])}let guard=t%2?[[rand(r),rand(2)]]:[];const w=dp(r,C,guard),ref=solve(r,C,guard);assert(!!w===!!ref,"dp");if(w)assert(check(C,w)&&guard.every(([i,b])=>w[i]===b),"dp lift");stats.dp_cases++;stats[w?"dp_sat":"dp_unsat"]++}
 return stats;
}
console.log(JSON.stringify(run(),null,2));
