function algebra(records){
function one(V,guards,d,cap=1000000){
const ix=new Map(V.map((v,i)=>[v,i])),mask=v=>1n<<BigInt(ix.get(v)),basis=new Map(),history=[];let work=0,rows=0,peak=0,totalTerms=0;
function tick(n=1){work+=n;if(work>cap)throw Error("cap")}
function terms(g,m){let S=[m];for(let l of g){let z=mask(Math.abs(l));if(l>0)S=S.map(a=>a|z);else S=S.concat(S.map(a=>a|z))}return new Set(S)}
function process(g,m){rows++;let S=terms(g,m),parent=[];tick(S.size);while(S.size){let p=-1n;for(let x of S){tick();if(x>p)p=x}if(!basis.has(p)){let node={g,m:String(m),parent,S};let id=history.length;history.push(node);basis.set(p,id);totalTerms+=S.size;peak=Math.max(peak,S.size);return p===0n?id:-1}let j=basis.get(p);parent.push(j);for(let x of history[j].S){tick();if(S.has(x))S.delete(x);else S.add(x)}}return -1}
let terminal=-1;try{outer:for(let g of guards){if(g.length>d)continue;let free=V.filter(v=>!g.some(l=>Math.abs(l)===v));function gen(start,left,m){let hit=process(g,m);if(hit>=0)return hit;if(left>0)for(let j=start;j<free.length;j++){let q=gen(j+1,left-1,m|mask(free[j]));if(q>=0)return q}return -1}terminal=gen(0,d-g.length,0n);if(terminal>=0)break outer}}catch(e){if(e.message!=="cap")throw e;return{d,status:"UNKNOWN cap",work,rows,rank:basis.size,peak,totalTerms}}
let certificate=null,verifyTerms=0;if(terminal>=0){let parity=new Set([terminal]);for(let i=terminal;i>=0;i--)if(parity.has(i)){for(let j of history[i].parent){if(parity.has(j))parity.delete(j);else parity.add(j)}}// parity currently denotes coefficient of each original generator, not just leaves; every node contributes its own row.
let P=new Set();certificate=[...parity].map(i=>({g:history[i].g,m:history[i].m}));for(let {g,m} of certificate){let S=new Set([BigInt(m)]);for(let l of g){let z=mask(Math.abs(l)),T=new Set();for(let x of S){let add=y=>{if(T.has(y))T.delete(y);else T.add(y);verifyTerms++};if(l<0)add(x);add(x|z)}S=T}for(let x of S){if(P.has(x))P.delete(x);else P.add(x);verifyTerms++}}if(P.size!==1||!P.has(0n))throw Error("certificate failed")}
return{d,status:terminal>=0?"NO":"UNKNOWN complete span",work,rows,rank:basis.size,peak,totalTerms,verifyTerms,certificate}
}
let output=[];for(let r of records){let V=r.chart.V,local=[];for(let f of r.chart.F)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))local.push(f.vs.map((v,i)=>(w>>i&1)?v:-v));let broad=r.broad.map(z=>z.g),peer=r.peer.status==="NO guard"?r.peer.split.map(z=>z.g):[];let lanes=[];for(let [mode,G] of [["local",local],["cooperative",local.concat(broad,peer)]])for(let d of [2,3,4,5])lanes.push({mode,...one(V,G,d)});output.push({instance:r.entry.instance_id,chartId:r.chartId,lanes})}
return output
}
console.log(JSON.stringify(algebra(JSON.parse(require('node:fs').readFileSync(process.argv[2],'utf8'))),null,2));
