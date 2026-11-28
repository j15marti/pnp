function checkBoundary(E,inc,BC){
const A=(x,m)=>{if(!x)throw Error(m)};
function rank(R){let b=new Map();for(let x of R)while(x){let p=x.toString(2).length;if(!b.has(p)){b.set(p,x);break}x^=b.get(p)}return b.size}
let out=[];for(let e of Object.values(E)){let b=BC.find(x=>x.instance===e.instance),s=inc.find(x=>x.instance===e.instance);
for(let a of b.arms){let p=s.arms.find(x=>x.mode===a.mode),F=e.F.concat(p.proof.slice(0,a.last.prefix).map(x=>x.clause)),rows=[],checks=0;
for(let r of a.last.rows){let first=r.ends[0],x=first[0],y=first[1],ix=a.boundary.indexOf(Math.abs(x)),iy=a.boundary.indexOf(Math.abs(y));A(ix>=0&&iy>=0,"boundary coordinate");let row=ix===iy?1n<<BigInt(ix):(1n<<BigInt(ix))^(1n<<BigInt(iy)),rhs=ix===iy?Number(x<0):Number((x<0)!==(y<0));A(row===BigInt("0x"+r.row)&&rhs===r.rhs,"encoded row");if(ix===iy)A(x===-y&&r.ends.length===1,"unit");else A(r.ends.length===2&&r.ends[1][0]===y&&r.ends[1][1]===x,"equivalence");
for(let i=0;i<r.ends.length;i++){let [u,v]=r.ends[i],P=r.paths[i];A(P.length&&P[0][0]===u&&P.at(-1)[1]===v,"endpoints");let q=u;for(let [a,b,j] of P){A(a===q&&F[j].length===2&&F[j].includes(-a)&&F[j].includes(b),"path step");q=b;checks++}}
rows.push([row,rhs])}
A(rank(rows.map(r=>r[0]))===a.last.rank&&rank(rows.map(([r,b])=>(r<<1n)|BigInt(b)))===a.last.rank,"rank/consistency");
out.push({instance:e.instance,mode:a.mode,prefix:a.last.prefix,rank:a.last.rank,effectiveWidth:a.cutWidth-a.last.rank,checkedEdges:checks})
}}return out}
if(typeof require==="function"){let fs=require("fs"),inc=JSON.parse(fs.readFileSync(process.argv[2],"utf8")),BC=JSON.parse(fs.readFileSync(process.argv[3],"utf8")),E=Object.fromEntries(process.argv.slice(4).map(p=>{let e=JSON.parse(fs.readFileSync(p,"utf8"));return[e.id,e]}));console.log(JSON.stringify(checkBoundary(E,inc,BC)))}
