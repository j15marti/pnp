function boundary(E,inc){
const A=(x,m)=>{if(!x)throw Error(m)},vars=F=>[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);
function one(e,a){let F=e.F.slice(),V=vars(F),B=a.mode==="spectral"?e.cut1.boundary:e.cut0.boundary,L=V.flatMap(v=>[v,-v]),ix=new Map(L.map((l,i)=>[l,i])),bits=L.map((l,i)=>1n<<BigInt(i)),reach=bits.slice(),adj=L.map(()=>[]),ops={edge:0,tests:0,rowXor:0,paths:0},timeline=[],old=-1,last=null;
function edge(u,v,j){let i=ix.get(u),k=ix.get(v);adj[i].push([v,j]);let S=reach[k];for(let t=0;t<L.length;t++){ops.edge++;if(reach[t]&bits[i])reach[t]|=S}}
function add(c,j){if(c.length===1)edge(-c[0],c[0],j);if(c.length===2){edge(-c[0],c[1],j);edge(-c[1],c[0],j)}}
function hit(u,v){ops.tests++;return !!(reach[ix.get(u)]&bits[ix.get(v)])}
function path(u,v){let q=[u],p=new Map([[u,null]]);for(let i=0;i<q.length;i++){let x=q[i];if(x===v){let R=[];while(p.get(x)){let [y,j]=p.get(x);A(F[j].includes(-y)&&F[j].includes(x),"path");R.push([y,x,j]);x=y}return R.reverse()}for(let [y,j] of adj[ix.get(x)]){ops.paths++;if(!p.has(y)){p.set(y,[x,j]);q.push(y)}}}throw Error("path missing")}
function snap(t){for(let v of V)if(hit(v,-v)&&hit(-v,v))return {terminal:true,prefix:t};
let basis=new Map(),rows=[];function test(row,rhs,ends){let x=row;while(x){let p=x&-x;if(!basis.has(p)){basis.set(p,x);rows.push({row:row.toString(16),rhs,ends});return}x^=basis.get(p);ops.rowXor++}}
for(let i=0;i<B.length;i++){let u=B[i],b=1n<<BigInt(i);if(hit(u,-u))test(b,0,[[u,-u]]);if(hit(-u,u))test(b,1,[[-u,u]]);for(let j=i+1;j<B.length;j++){let v=B[j],c=b|(1n<<BigInt(j));if(hit(u,v)&&hit(v,u))test(c,0,[[u,v],[v,u]]);if(hit(u,-v)&&hit(-v,u))test(c,1,[[u,-v],[-v,u]])}}
return {terminal:false,prefix:t,rank:basis.size,rows}}
for(let j=0;j<F.length;j++)add(F[j],j);
for(let i=0;i<=a.proof.length;i++){if(i){let p=a.proof[i-1];A(p.index===F.length,"proof index");F.push(p.clause);add(p.clause,p.index)}let s=snap(i);if(s.terminal){timeline.push(s);break}if(s.rank!==old){timeline.push({prefix:i,rank:s.rank});old=s.rank;last={...s,rows:s.rows.map(r=>({...r,paths:r.ends.map(([u,v])=>path(u,v))}))}}}
return {mode:a.mode,cutWidth:B.length,boundary:B,timeline,last,ops,scope:"exact independent boundary equations from the already-verified prefix; effective outer carrier dimension, not recompiled syndrome connectivity"}
}
return Object.values(E).map(e=>({instance:e.instance,guard:e.guard_id,residual:e.residual_id,arms:inc.find(x=>x.instance===e.instance).arms.filter(a=>a.status==="SCC").map(a=>one(e,a))}))}
if(typeof require==="function"){let fs=require("fs"),inc=JSON.parse(fs.readFileSync(process.argv[2],"utf8")),E=Object.fromEntries(process.argv.slice(3).map(p=>{let e=JSON.parse(fs.readFileSync(p,"utf8"));return[e.id,e]}));console.log(JSON.stringify(boundary(E,inc)))}
