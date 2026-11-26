/* Independent P4SW10 certificate; Node.js 18+. */
function audit(C){
 const ck=(x,m)=>{if(!x)throw Error(m)},bit=i=>1n<<BigInt(i);
 const rows=Array.from({length:72},()=>[]),cols=[];let holes=bit(0)|bit(6);
 C.forEach((t,j)=>{let b=0n;t.forEach((v,c)=>{let i=18*c+v;rows[i].push(j);b|=bit(i)});cols.push(b&~holes)});ck(rows.every(r=>r.length===3),"E3");
 let W=[];function rec(left,s){if(!left){W.push(s);return}let best=null;for(let i=0;i<72;i++)if(left&bit(i)){let a=rows[i].filter(j=>(cols[j]&left)===cols[j]);if(best===null||a.length<best.length)best=a}for(let j of best)rec(left^cols[j],s|bit(j))}
 rec((bit(72)-1n)&~holes,0n);ck(W.length===51,"local 51");
 const pairs=[[0,18],[1,19],[1,20],[2,19],[2,20]], masks=pairs.map(p=>p.reduce((s,j)=>s|bit(j),0n)),P=masks.reduce((s,j)=>s|j,0n);
 const fibers=masks.map(m=>W.filter(w=>(w&P)===m));ck(fibers.map(x=>x.length).join()==="5,12,11,12,11","fiber counts");
 let cross=0;for(let [i,j] of [[1,4],[2,3]])for(let u of fibers[i])for(let v of fibers[j])for(let k of [1,2,3,4].filter(k=>k!==i&&k!==j)){ck(fibers[k].some(w=>(w&(u&v))===(u&v)&&(w&~(u|v))===0n),"rectangle witness");cross++}
 let F=bit(W.length)-1n,A=Array.from({length:54},(_,j)=>W.reduce((s,w,i)=>s|((w&bit(j))?bit(i):0n),0n)),M=masks.map(m=>W.reduce((s,w,i)=>s|((w&P)===m?bit(i):0n),0n));
 let seen=new Set([F]),todo=[F],types=new Set(),transitions=0;while(todo.length){let s=todo.pop(),b=0,live=0n;M.forEach((m,i)=>{if(m&s){b|=1<<i;live|=masks[i]}});M.forEach((m,i)=>ck(Boolean(m&s)===((live&masks[i])===masks[i]),"live support equivalence"));types.add(b);for(let a of A)for(let t of [s&a,s&(F^a)]){transitions++;if(t&&!seen.has(t)){seen.add(t);todo.push(t)}}}
 let seed=26112610;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 function mesh(k){
  const slots=[],at=new Map(),groups=[],dirs=[[0,1],[1,0],[0,-1],[-1,0]],K=(v,u)=>v.join(",")+":"+u.join(",");
  for(let x=0;x<k;x++)for(let y=0;y<k;y++){let v=[x,y],s=[];for(let [a,b] of dirs){let u=[x+a,y+b];if(u.some(z=>z<0||z>=k))continue;let j=slots.length;slots.push({v,u});at.set(K(v,u),j);s.push(j)}for(let i=0;i<s.length;i+=2)groups.push(s.slice(i,i+2));s.forEach((j,i)=>{slots[j].prev=s[(i+s.length-1)%s.length];slots[j].next=s[(i+1)%s.length]})}
  const n=slots.length, E=[],rot=Array.from({length:2*n},()=>[]),eq=[];
  slots.forEach((s,i)=>{let j=at.get(K(s.u,s.v));s.ext=j;E.push([i,n+s.prev],[i,n+j],[i,n+i]);rot[i]=[n+s.prev,n+j,n+i];rot[n+i]=[i,j,s.next]});
  for(let g of groups)if(g.length===2)eq.push(g.map(i=>3*i+2));
  const side=new Map();let f=0;for(let u=0;u<rot.length;u++)for(let v of rot[u]){let key=u+":"+v;if(side.has(key))continue;let a=u,b=v;do{let key=a+":"+b;ck(!side.has(key),"face walk");side.set(key,f);let z=rot[b],c=z[(z.indexOf(a)+z.length-1)%z.length];a=b;b=c}while(a!==u||b!==v);f++}
  ck(f===E.length-2*n+2,"Euler planar");const sides=E.map(([u,v])=>[side.get(u+":"+v),side.get(v+":"+u)]);
  // arbitrary raw PM acquired by augmenting, no coupled/source target.
  let match=Array(n).fill(-1);function aug(i,seen){for(let t=0;t<3;t++){let j=3*i+t,r=E[j][1]-n;if(seen.has(r))continue;seen.add(r);if(match[r]<0||aug(Math.floor(match[r]/3),seen)){match[r]=j;return true}}return false}
  for(let i=0;i<n;i++)ck(aug(i,new Set()),"raw PM");const ref=new Set(match);
  for(let [a,b] of eq)ck(sides[a][0]===sides[b][0]||sides[a][1]===sides[b][1],"common face");
  return {n,E,groups,eq,f,sides,ref}
 }
 function join(H,pins){
  let {n,E,eq,f,sides,ref}=H,D=[];const add=(a,b,c)=>D.push([a,b,c]);
  sides.forEach(([a,b],j)=>{let m=+ref.has(j),l=pins.has(j)?pins.get(j):0,u=pins.has(j)?pins.get(j):1;add(b,a,u-m);add(a,b,m-l)});
  for(let [j,k] of eq){let [a,b]=sides[j],[c,d]=sides[k],r=+ref.has(k)- +ref.has(j);let [u,v]=a===c?[b,d]:[c,a];add(u,v,r);add(v,u,-r)}
  let h=Array(f).fill(0),changed;for(let i=0;i<f;i++){changed=false;for(let [u,v,c] of D)if(h[v]>h[u]+c){h[v]=h[u]+c;changed=true}if(!changed)break}if(changed)return null;
  let x=sides.map(([a,b],j)=>+ref.has(j)+h[a]-h[b]),occ=Array(2*n).fill(0);
  ck(x.every(v=>v===0||v===1),"Boolean");x.forEach((v,j)=>{if(v)for(let a of E[j])occ[a]++});ck(occ.every(v=>v===1)&&eq.every(([a,b])=>x[a]===x[b])&&[...pins].every(([j,v])=>x[j]===v),"lift");return x
 }
 function brute(H,pins){let {groups,E}=H;let T=groups.map(g=>{let a=g[0];if(g.length===1)return [0,1,2].map(t=>[3*a+t]);let b=g[1];return [[3*a+2,3*b+2],...[0,1].flatMap(i=>[0,1].map(j=>[3*a+i,3*b+j]))]}).map((A,i)=>A.filter(s=>groups[i].every(g=>[0,1,2].every(t=>!pins.has(3*g+t)||+s.includes(3*g+t)===pins.get(3*g+t)))));
 function rec(i,U){if(i===T.length)return true;for(let s of T[i]){let R=s.map(j=>E[j][1]);if(new Set(R).size!==R.length||R.some(r=>U.has(r)))continue;if(rec(i+1,new Set([...U,...R])))return true}return false}return rec(0,new Set())}
 let tests=[],yes=0,no=0;
 for(let k of [2,3,4,8,16]){let H=mesh(k),w=join(H,new Map());ck(w!==null,"raw mesh");tests.push({k,slots:H.n,faces:H.f,edges:H.E.length,equalities:H.eq.length,base:true});if(k<=3)for(let i=0;i<200;i++){let p=new Map();for(let j=0;j<2+Math.floor(rnd()*9);j++)p.set(Math.floor(rnd()*H.E.length),+(rnd()<.3));let w=join(H,p),b=brute(H,p);ck(Boolean(w)===b,"guarded reference");if(b)yes++;else no++}}
 return {local_words:W.length,counts:fibers.map(x=>x.length),rectangle_cross_witness_checks:cross,guard_fibers:seen.size,guard_types:[...types].sort((a,b)=>a-b),guard_transitions:transitions,mesh_tests:tests,abstract_guarded_yes:yes,abstract_guarded_no:no,scope:"JS independent finite source and macro embedding/height audit; native recovery and original source witnesses in Python archive."}
}
const C=[[6,0,5,1],[0,1,0,1],[0,1,1,0],[1,0,0,1],[1,0,1,0],[1,1,0,0],[2,2,3,3],[2,3,2,3],[2,4,3,2],[3,2,2,3],[3,2,3,2],[3,3,2,13],[4,3,5,5],[4,5,4,5],[4,5,5,4],[5,4,4,5],[5,4,11,4],[5,5,4,4],[0,12,1,7],[6,7,6,7],[6,7,7,6],[7,12,6,7],[7,6,7,6],[7,7,6,6],[8,8,9,9],[8,9,8,9],[8,10,9,8],[9,8,8,9],[9,8,9,8],[9,6,8,8],[10,9,11,11],[10,11,10,11],[10,11,11,10],[11,10,10,11],[11,10,7,10],[11,11,10,10],[12,9,17,2],[12,13,12,13],[12,13,17,12],[13,12,12,13],[13,6,13,12],[13,13,12,12],[14,14,15,15],[14,15,14,15],[14,16,15,14],[15,14,14,15],[15,14,15,14],[15,15,14,14],[16,15,13,17],[16,17,16,17],[16,17,17,16],[17,16,16,17],[17,16,13,16],[17,17,16,16]];
console.log(JSON.stringify(audit(C),null,2));
