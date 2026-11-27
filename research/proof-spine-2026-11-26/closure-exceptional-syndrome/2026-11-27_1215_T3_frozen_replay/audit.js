function pin(F,v){return F.map(f=>{let i=f.vs.indexOf(v);if(i<0)return f;return {...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}})}

function cnf(F){let M=new Map();for(let f of F)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w)){let c=f.vs.map((v,i)=>(w>>i&1)?-v:v);M.set(c.join(),c)}return [...M.values()]}

function key(c){return c.slice().sort((a,b)=>a-b).join(",")}

function up(db,g,m,cap=1e7,reverse=false){let a=new Map();for(let l of g){if(a.has(Math.abs(l))&&a.get(Math.abs(l))!==(l>0))return null;a.set(Math.abs(l),l>0)}for(;;){let ch=false;for(let j=0;j<db.length;j++){if(++m.scans>cap)throw Error("scan cap");let c=db[reverse?db.length-1-j:j],n=0,u=0,hit=false;for(let l of c){m.lits++;if(!a.has(Math.abs(l))){n++;u=l}else if(a.get(Math.abs(l))===(l>0)){hit=true;break}}if(hit)continue;if(n===0)return null;if(n===1){a.set(Math.abs(u),u>0);ch=true}}if(!ch)return a}}

function batches(C,cap=2500000){let D=C.slice(),seen=new Set(D.map(key)),vs=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),layers=[],m={scans:0,lits:0,probes:0},status="UNKNOWN";
try{for(;;){let a=up(D,[],m,cap);if(!a){layers.push([[]]);status="UNSAT";break}let V=vs.filter(v=>!a.has(v)),P=[];const test=g=>{let c=g.map(l=>-l),k=key(c);if(seen.has(k))return;m.probes++;if(!up(D,g,m,cap)){P.push(c);seen.add(k)}};for(let v of V)for(let s of [-1,1])test([s*v]);if(!P.length)for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++)for(let s of [-1,1])for(let t of [-1,1])test([s*V[i],t*V[j]]);if(!P.length){status="UNKNOWN fixed point";break}layers.push(P);D.push(...P)}}catch(e){status="UNKNOWN "+e.message}return{status,m,layers}}

function replay(C,layers){let db=C.slice(),m={scans:0,lits:0,probes:0};for(let P of layers){for(let c of P){m.probes++;if(up(db,c.map(l=>-l),m,1e7,true)!==null)throw Error("invalid frozen layer")}db.push(...P)}return{...m,empty:layers.flat(1).some(c=>!c.length)}}

function earliest(C,P){let db=C.slice(),left=P.map((c,i)=>({c,i})),layers=[],m={scans:0,lits:0,probes:0};while(left.length){let ok=[],bad=[];for(let q of left){m.probes++;(up(db,q.c.map(l=>-l),m,1e7)===null?ok:bad).push(q)}if(!ok.length)throw Error("no topological layer");layers.push(ok.map(x=>x.i));db.push(...ok.map(x=>x.c));left=bad;if(ok.some(x=>x.c.length===0))break}return{layers,m,verification:replay(C,layers.map(L=>L.map(i=>P[i])))}}
module.exports={pin,cnf,key,up,batches,replay,earliest};
