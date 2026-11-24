// RT04 independent controls. Node.js, no dependencies.
function run(){
const assert=(x,m)=>{if(!x)throw Error(m)};
let seed=0x2010440;
function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
const bit=i=>1n<<BigInt(i);
function parity(x){let p=0;while(x){x&=x-1n;p^=1;}return p;}
function rref(rows,n){rows=rows.slice();let k=0,piv=[];
 for(let j=0;j<n;j++){let z=rows.findIndex((x,i)=>i>=k&&Boolean(x&bit(j)));if(z<0)continue;
 [rows[k],rows[z]]=[rows[z],rows[k]];for(let i=0;i<rows.length;i++)if(i!==k&&(rows[i]&bit(j)))rows[i]^=rows[k];piv.push(j);k++;}
 return {rows:rows.slice(0,k),piv};}
function kernel(rows,n){const R=rref(rows,n),out=[];for(let j=0;j<n;j++)if(!R.piv.includes(j)){let v=bit(j);for(let i=0;i<R.piv.length;i++)if(R.rows[i]&bit(j))v|=bit(R.piv[i]);out.push(v);}return out;}
function graph(n,E){let a=Array.from({length:n},()=>[]);for(const [u,v] of E){a[u].push(v);a[v].push(u);}return a;}
function forest(n,E){let p=Array.from({length:n},(_,i)=>i);function f(x){while(p[x]!==x)x=p[x];return x;}let I=[];E.forEach(([u,v],i)=>{let a=f(u),b=f(v);if(a!==b){p[a]=b;I.push(i);}});return I;}
function cross(n,E,I){let rows=Array(n).fill(0n);for(const i of I){let [u,v]=E[i];rows[u]^=bit(u)|bit(n+i);rows[v]^=bit(v)|bit(n+i);}return rows;}
function polarRank(n,E,I){const C=cross(n,E,I),d=n+n+E.length;let R=Array(d).fill(0n);for(let i=0;i<n;i++){R[i]=C[i]<<BigInt(n);for(let j=0;j<n+E.length;j++)if(C[i]&bit(j))R[n+j]|=bit(i);}return rref(R,d).piv.length;}
function form(n,E,i,u,v){const [a,b]=E[i];let p=0;for(const [s,t] of [[a,n+a],[b,n+b],[a,2*n+i],[b,2*n+i]])p^=Number(Boolean(u&bit(s))&&Boolean(v&bit(t)))^Number(Boolean(v&bit(s))&&Boolean(u&bit(t)));return p;}
function greedy(n,E){let d=2*n+E.length,U=Array.from({length:d},(_,i)=>bit(i));
 while(true){let R=null;for(let i=0;i<E.length;i++){let rows=U.map(u=>U.reduce((a,v,j)=>a|(form(n,E,i,u,v)?bit(j):0n),0n));if(rows.some(x=>x!==0n)){R=rows;break;}}
 if(!R)break;U=kernel(R,U.length).map(x=>U.reduce((a,v,j)=>a^((x&bit(j))?v:0n),0n));}
 return d-U.length;}
const stats={graphs:0,forest_rank_checks:0,projected_rank_checks:0,greedy_checks:0,selector_tuple_checks:0,selector_sat:0,selector_unsat:0,mask_checks:0};
function colors(n,E,limit=3){let a=graph(n,E),c=Array(n).fill(-1);let nodes=0;function dfs(k){nodes++;if(k===n)return c.slice();let v=-1,bs=-1,bd=-1;for(let i=0;i<n;i++)if(c[i]<0){let s=new Set(a[i].map(j=>c[j]).filter(x=>x>=0)).size;if(s>bs||(s===bs&&a[i].length>bd)){v=i;bs=s;bd=a[i].length;}}let forbidden=new Set(a[v].map(j=>c[j]));for(let x=0;x<limit;x++)if(!forbidden.has(x)){c[v]=x;let r=dfs(k+1);if(r)return r;c[v]=-1;}return null;}return {w:dfs(0),nodes};}
function valid(n,E,w){return w&&w.length===n&&w.every(x=>x>=0&&x<3)&&E.every(([u,v])=>w[u]!==w[v]);}
for(let n=2;n<=5;n++){let all=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)all.push([u,v]);
 for(let h=0;h<(1<<all.length);h++){let E=all.filter((_,i)=>h&(1<<i)),F=forest(n,E),active=graph(n,E).filter(a=>a.length).length;stats.graphs++;
 assert(polarRank(n,E,F)===2*active,'forest full rank');
 for(let mask=0;mask<(1<<F.length);mask++){let I=F.filter((_,i)=>mask&(1<<i)),a=graph(n,I.map(i=>E[i])).filter(x=>x.length).length;assert(polarRank(n,E,I)===2*a,'forest subset rank');stats.forest_rank_checks++;}
 // Arbitrary random constraints on edge-combination coefficients, restricted to forest.
 for(let t=0;t<3;t++){let r=F.length? rng()%(F.length+1):0;let rows=Array.from({length:r},()=>F.reduce((a,_,j)=>a|((rng()>>>17&1)?bit(j):0n),0n));let K=kernel(rows,F.length),R=rref(K,F.length);let x=R.rows.reduce((a,v)=>a^v,0n);assert(rows.every(z=>parity(z&x)===0),'kernel');let I=F.filter((_,i)=>x&bit(i));assert(I.length>=F.length-r,'pivot weight');let rank=polarRank(n,E,I);assert(rank>=2*I.length,'projected rank lower');if(I.length)assert(rank>=2*(I.length+1),'nonempty forest');stats.projected_rank_checks++;}
 if(n<=4||h%31===0){let b=greedy(n,E);assert(b>=active&&b<=2*active,'MS04 greedy bound');stats.greedy_checks++;}
 if(n<=4){let sat=Boolean(colors(n,E).w),exists=false;for(let mask=0;mask<(1<<(2*n+E.length));mask++){let s=i=>(mask>>i)&1,t=i=>(mask>>(n+i))&1,te=i=>(mask>>(2*n+i))&1;
 let ok=E.every(([u,v],i)=>(1^s(u)*t(u)^s(v)*t(v)^(s(u)^s(v))*te(i))===0);if(ok){exists=true;let c=Array.from({length:n},(_,i)=>2*s(i)+(1^s(i)^s(i)*t(i)));assert(E.every(([u,v])=>c[u]!==c[v]),'selector lift');}stats.selector_tuple_checks++;}assert(exists===sat,'color equivalence');stats[sat?'selector_sat':'selector_unsat']++;}
 }}
// I04 translated even-triple support: check every nonempty pair mask and all translations.
for(let m=1;m<16;m++){let B=[0,1,2,3].filter(x=>m>>x&1),E=B.map(x=>x|((parity(BigInt(x)))<<2));for(const s of E){let A=E.map(x=>x^s);assert(A.includes(0)&&A.every(x=>parity(BigInt(x))===0),'even translation');let match=[0,...[3,5,6].filter(x=>A.includes(x))].map(x=>x^s).sort((a,b)=>a-b);assert(JSON.stringify(match)===JSON.stringify(E.slice().sort((a,b)=>a-b)),'I04 mask');stats.mask_checks++;}}
// Public 21-vertex girth-5 seed from G. Royle's MO answer 193716.
const adj=[[7,13,18,19],[8,15,17,19],[9,10,19,20],[9,11,14,18],[10,12,13,15],[11,13,17,20],[12,14,16,19],[0,14,15,20],[1,16,18,20],[2,3,15,16],[2,4,17,18],[3,5,19],[4,6,20],[0,4,5,16],[3,6,7,17],[1,4,7,9],[6,8,9,13],[1,5,10,14],[0,3,8,10],[0,1,2,6,11],[2,5,7,8,12]];
function noShort(n,E){let a=graph(n,E);for(let u=0;u<n;u++){let seen=new Set();for(const v of a[u])for(const w of a[v])if(w!==u){if(a[u].includes(w)||seen.has(w))return false;seen.add(w);}}return true;}
let base=adj.flatMap((a,u)=>a.filter(v=>v>u).map(v=>[u,v]));let initial=colors(21,base);assert(!initial.w&&noShort(21,base),'seed');
let criticalizationCalls=0;for(let i=0;i<base.length;){let e=base.filter((_,j)=>j!==i);criticalizationCalls++;if(!colors(21,e).w)base=e;else i++;}
let witnesses=base.map((_,i)=>colors(21,base.filter((_,j)=>j!==i)).w);assert(witnesses.every((w,i)=>valid(21,base.filter((_,j)=>i!==j),w)),'critical base');
assert(graph(21,base).every(a=>a.length>=3),'min degree');
const f=0,g=base.findIndex(([u,v],i)=>i!==f&&!base[f].includes(u)&&!base[f].includes(v));assert(g>=0,'disjoint join edges');
let G=base.slice(),n=21,active=base[g],w=witnesses[g].slice(),scaling=[],anchorChecks=0;
const same=(e,f)=>e[0]===f[0]&&e[1]===f[1]||e[0]===f[1]&&e[1]===f[0];
for(let h=1;h<=16;h++){
 if([1,2,4,8,16].includes(h)){assert(noShort(n,G)&&valid(n,G.filter(e=>!same(e,active)),w),'chain neighbor');let a=graph(n,G),D=Math.max(...a.map(x=>x.length)),minU=n,minLower=n,minGreedy=n;
 for(let v=0;v<n;v++){let U=Array.from({length:n},(_,i)=>i).filter(i=>i!==v&&!a[v].includes(i)),S=new Set(U),E=G.filter(([u,z])=>S.has(u)&&S.has(z));assert(U.every(u=>a[u].filter(z=>S.has(z)).length>=2),'anchor residual min degree');assert(U.length>=2*(n-1)/3,'anchor size');let used=new Set(),gmatch=0;for(const [u,z] of E)if(!used.has(u)&&!used.has(z)){used.add(u);used.add(z);gmatch++;}
 minU=Math.min(minU,U.length);minLower=Math.min(minLower,Math.ceil(2*U.length/(D+2)));minGreedy=Math.min(minGreedy,gmatch);anchorChecks++;}
 scaling.push({copies:h,n,m:G.length,maxDegree:D,minU,minCoverLower:minLower,minGreedyMatching:minGreedy,k:n,q:G.length,satNeighborVerified:true});}
 if(h===16)break;
 const [a,b]=active,[c,d]=base[f],map=Array(21);let nn=n;for(let i=0;i<21;i++)map[i]=i===c?a:nn++;
 // Join G-active and fresh base-f. New deletion is g in fresh base.
 const W=witnesses[g],shift=(w[a]-W[c]+3)%3;assert(w[a]===w[b]&&W[c]!==W[d],'join witness conditions');
 const nextW=w.slice();for(let i=0;i<21;i++)nextW[map[i]]=(W[i]+shift)%3;
 G=G.filter(e=>!same(e,active)).concat(base.filter((_,i)=>i!==f).map(([u,v])=>[map[u],map[v]]),[[b,map[d]]]);active=base[g].map(i=>map[i]);n=nn;w=nextW;
}
return {seed:0x2010440,stats,base:{n:21,m:base.length,edges:base,initialSearchNodes:initial.nodes,criticalizationCalls,verifiedEdgeDeletionWitnesses:witnesses.length,joinEdges:[base[f],base[g]]},anchorChecks,scaling};}
if(typeof module!=='undefined') console.log(JSON.stringify(run(),null,2));
