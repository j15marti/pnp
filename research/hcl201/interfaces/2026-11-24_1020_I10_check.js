// Node.js standalone; no external dependencies
function experiment(){
let seed=102024;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const P=1000003, mod=x=>((x%P)+P)%P, mul=(x,y)=>mod(x*y), pow=(a,b)=>{let r=1;while(b){if(b%2)r=mul(r,a);a=mul(a,a);b=Math.floor(b/2)}return r};
const parity=x=>{let a=0;while(x){a^=1;x&=x-1}return a};
let stats={seed:102024,instances:0,sat:0,unsat:0,states:0,closureRejects:0,closureCalls:0,closureFacts:0,pfaffians:0,lifts:0,referenceWords:0,etaZero:0,exceptional:0,etaOnlyBarrier:[]};
function pf(n,edges,verts,u){stats.pfaffians++;let a=Array.from({length:verts.length},()=>Array(verts.length).fill(0));let ix=new Map(verts.map((v,i)=>[v,i]));for(const e of edges){let i=ix.get(e.u),j=ix.get(e.v);if(i===undefined||j===undefined)continue;let w=parity(u&e.tag)?mod(-e.w):e.w;a[i][j]=mod(a[i][j]+w);a[j][i]=mod(a[j][i]-w)}
let z=1;for(let k=0;k<a.length;k+=2){let j=k+1;while(j<a.length&&!a[k][j])j++;if(j===a.length)return 0;if(j!==k+1){[a[j],a[k+1]]=[a[k+1],a[j]];for(let i=0;i<a.length;i++)[a[i][j],a[i][k+1]]=[a[i][k+1],a[i][j]];z=mod(-z)}
let v=a[k][k+1];z=mul(z,v);let inv=pow(v,P-2);for(let i=k+2;i<a.length;i++)for(let l=i+1;l<a.length;l++){a[i][l]=mod(a[i][l]-mul(inv,mod(mul(a[k][i],a[k+1][l])-mul(a[k][l],a[k+1][i]))));a[l][i]=mod(-a[i][l])}}return z}
function coeff(g,vs,r,y){let z=0;for(let u=0;u<(1<<r);u++){let v=pf(g.n,g.edges,vs,u);z=mod(z+(parity(u&y)?-v:v))}return mul(z,pow(1<<r,P-2))}
function consistent(eq,bits){let piv=Array(bits).fill(0);for(let [a,b] of eq){let v=a|(b<<bits);for(let j=bits-1;j>=0;j--)if(v&(1<<j)){if(piv[j])v^=piv[j];else{piv[j]=v;v=0;break}}if(v)return false}return true}
function closure(rows,offset,masks,pins,bits){stats.closureCalls++;let eq=pins.slice(),changed=true;while(changed){changed=false;if(!consistent(eq,bits))return false;for(let j=0;j<masks.length;j++){let allowed=[];for(let c=0;c<4;c++)if(masks[j]&(1<<c)){let a=2*j,b=a+1;if(consistent(eq.concat([[rows[a],(c&1)^offset[a]],[rows[b],(c>>1)^offset[b]]]),bits))allowed.push(c)}if(!allowed.length)return false;for(let f=1;f<4;f++){let t=parity(f&allowed[0]);if(allowed.every(c=>parity(f&c)===t)){let a=0,b=t;for(let k=0;k<2;k++)if(f&(1<<k)){a^=rows[2*j+k];b^=offset[2*j+k]}if(consistent(eq.concat([[a,b^1]]),bits)){eq.push([a,b]);stats.closureFacts++;changed=true}}}}}return true}
function run(nx,nr,rows,offset,masks){let q=rows.length,bits=nx+nr,hidden=rows.map(x=>x>>nx),base=[], comb=new Map([[0,0]]);for(let j=0;j<q;j++)if(!comb.has(hidden[j])){let old=[...comb];let b=1<<base.length;base.push(j);for(let [v,w] of old)comb.set(v^hidden[j],w^b)}let eta=base.length;if(!eta)stats.etaZero++;
let repr=[],used=new Set(),extra=[];for(let j=0;j<q;j++){let a=rows[j],c=offset[j],h=comb.get(hidden[j]);for(let k=0;k<eta;k++)if(h&(1<<k)){a^=rows[base[k]];c^=offset[base[k]]}if(a===0)repr.push({owner:-1,c,h});else if((a&(a-1))===0&&!used.has(a)){used.add(a);repr.push({owner:Math.log2(a),c,h})}else{extra.push(j);repr.push({owner:-1,c:0,h:1<<(eta+extra.length-1)})}}
if(extra.length)stats.exceptional++;let chosen=base.concat(extra),r=chosen.length;
let ref=false;for(let x=0;x<(1<<bits);x++){stats.referenceWords++;if(masks.every((m,j)=>m&(1<<((parity(rows[2*j]&x)^offset[2*j])|((parity(rows[2*j+1]&x)^offset[2*j+1])<<1))))){ref=true;break}}
stats.instances++;stats[ref?"sat":"unsat"]++;
if(!closure(rows,offset,masks,[],bits)){stats.closureRejects++;if(ref)throw Error("bad closure");return false}
let found=false;
for(let y=0;y<(1<<r);y++){stats.states++;let pins=chosen.map((j,k)=>[rows[j],((y>>k)&1)^offset[j]]);if(!closure(rows,offset,masks,pins,bits)){stats.closureRejects++;continue}
let g={n:0,edges:[],optional:[]};let node=(optional=false)=>{let v=g.n++;if(optional)g.optional.push(v);return v},edge=(u,v,tag=0,id=-1)=>{if(u===v)throw Error("loop");if(u>v)[u,v]=[v,u];g.edges.push({u,v,tag,id,w:rnd(P-1)+1})};
let labels=Array(bits).fill(0),shift=0;for(let k=0;k<r;k++){let j=chosen[k];shift^=(offset[j]^parity(rows[j]&((1<<nx)-1)))<<k;for(let i=0;i<bits;i++)if(rows[j]&(1<<i))labels[i]^=1<<k}
let ports=[];for(let i=0;i<nx;i++){let own=used.has(1<<i),u=node(!own),v=node(true);edge(u,v,labels[i],i);if(own){let s=node(),f=node(),p=node();edge(u,s);edge(s,f);edge(f,p);ports[i]=p}}
for(let i=0;i<nr;i++){let a=node(),b=node(),c=node(),d=node();edge(a,c,labels[nx+i],nx+i);edge(b,d);edge(a,d);edge(b,c)}
let ok=true;for(let j=0;j<masks.length;j++){let A=repr[2*j],B=repr[2*j+1],active=[A,B].filter(a=>a.owner>=0),allowed=[];for(let z=0;z<(1<<active.length);z++){let color=0,idx=0;for(let k=0;k<2;k++){let a=k?B:A;let b=a.c^parity(a.h&y);if(a.owner>=0)b^=(z>>idx++)&1;color|=b<<k}if(masks[j]&(1<<color))allowed.push(z)}
if(!allowed.length){ok=false;break}if(active.length===0)continue;
if(active.length===1){let p=ports[active[0].owner];if(allowed.length===2)g.optional.push(p);else if(allowed[0]===0)edge(p,node());continue}
let s=allowed[0],ts=active.map((a,k)=>{let p=ports[a.owner];if((s>>k)&1)return p;let t=node();edge(p,t);return t});let w=node(true);for(let z of allowed){let c=z^s;if(c===1)edge(ts[0],w);if(c===2)edge(ts[1],w);if(c===3)edge(ts[0],ts[1])}}
if(!ok)continue;let old=g.n,ds=Array.from({length:g.optional.length+((old+g.optional.length)%2)},()=>node());for(let u of g.optional)for(let d of ds)edge(u,d);for(let i=0;i<ds.length;i++)for(let j=i+1;j<ds.length;j++)edge(ds[i],ds[j]);let vs=Array.from({length:g.n},(_,i)=>i),target=y^shift;
if(!coeff(g,vs,r,target))continue;
let chosenEdges=[];while(vs.length){let v=vs[0],e=g.edges.find(e=>(e.u===v||e.v===v)&&vs.includes(e.u)&&vs.includes(e.v)&&coeff(g,vs.filter(a=>a!==e.u&&a!==e.v),r,target^e.tag));if(!e)throw Error("lift failed");chosenEdges.push(e);target^=e.tag;vs=vs.filter(a=>a!==e.u&&a!==e.v)}
let x=(1<<nx)-1;for(let e of chosenEdges)if(e.id>=0)x^=1<<e.id;if(target||!masks.every((m,j)=>m&(1<<((parity(rows[2*j]&x)^offset[2*j])|((parity(rows[2*j+1]&x)^offset[2*j+1])<<1))))||chosen.some((j,k)=>(parity(rows[j]&x)^offset[j])!==((y>>k)&1)))throw Error("bad witness");
stats.lifts++;found=true;break}
if(found!==ref)throw Error("decision discrepancy");return found}
for(let i=0;i<100;i++){let nx=3+(i%2),nr=i%3,q=4+2*(i%2),rows=[],off=[],m=[];for(let j=0;j<q;j++){let x=(i%3===0)?rnd(1<<nx):1<<rnd(nx);if(i%5===0)x=0;rows.push(x|(rnd(1<<nr)<<nx));off.push(rnd(2))}for(let j=0;j<q/2;j++)m.push(i%7===0?1<<rnd(4):1+rnd(15));run(nx,nr,rows,off,m)}
// 3-colour reduction check independently on every graph on four vertices.
for(let em=0;em<64;em++){let es=[],k=0;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++,k++)if(em&(1<<k))es.push([i,j]);let rows=[],m=[];for(let i=0;i<4;i++){rows.push(1<<(2*i),1<<(2*i+1));m.push(7)}for(let [i,j] of es){rows.push((1<<(2*i))^(1<<(2*j)),(1<<(2*i+1))^(1<<(2*j+1)));m.push(14)}
let direct=0,compiled=0;for(let w=0;w<256;w++){let c=Array.from({length:4},(_,i)=>(w>>(2*i))&3);if(c.every(v=>v!==3)&&es.every(([i,j])=>c[i]!==c[j]))direct++;if(m.every((v,j)=>v&(1<<(parity(rows[2*j]&w)|parity(rows[2*j+1]&w)<<1))))compiled++}if(direct!==compiled)throw Error("color reduction");if(em===63||em===62)stats.etaOnlyBarrier.push({edges:es.length,models:direct,eta:0,affineClosureSurvives:closure(rows,rows.map(()=>0),m,[],8)})}
return stats
}
console.log(JSON.stringify(experiment(),null,2));
