function supportTree(F,limit){
 let m={rows:0,visits:0,nodes:0,leaves:0,forced:0};
 function rec(pins){m.nodes++;let a=new Map(pins),live=[];for(;;){let changed=false;live=[];for(let f of F){let ok=[],given=f.vs.map(v=>a.has(v)?a.get(v):-1);for(let w of f.ok){if(++m.rows>limit)return {cap:true};if(given.every((b,j)=>b<0||((w>>j)&1)===b))ok.push(w)}if(!ok.length){m.leaves++;return {no:true}}for(let j=0;j<f.vs.length;j++){let v=f.vs[j];if(a.has(v))continue;let b=(ok[0]>>j)&1;if(ok.every(w=>{m.visits++;return ((w>>j)&1)===b})){a.set(v,b);m.forced++;changed=true}}live.push({vs:f.vs,ok})}if(!changed)break}let score=new Map();for(let f of live)for(let v of f.vs)if(!a.has(v))score.set(v,(score.get(v)||0)+1);if(!score.size)return {sat:true};let v=[...score].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let p=rec([...pins,[v,0]]);if(!p.no)return p;let q=rec([...pins,[v,1]]);return q.no?{no:true,v,p,q}:q}
 let tree=rec([]);return {status:tree.no?"UNSAT":tree.sat?"FEASIBLE":"UNKNOWN",tree,m};
}

function treeCheck(F,tree){
 let m={tests:0,nodes:0};function rec(t,pins){m.nodes++;let a=new Map(pins);while(true){let changed=false;for(let f of F){let ok=f.ok.filter(w=>{m.tests++;return f.vs.every((v,j)=>!a.has(v)||a.get(v)===((w>>j)&1))});if(!ok.length)return true;for(let j=0;j<f.vs.length;j++)if(!a.has(f.vs[j])){let b=(ok[0]>>j)&1;if(ok.every(w=>((w>>j)&1)===b)){a.set(f.vs[j],b);changed=true}}}if(!changed)break}if(!t.v||a.has(t.v)||!F.some(f=>f.vs.includes(t.v)))return false;return rec(t.p,[...pins,[t.v,0]])&&rec(t.q,[...pins,[t.v,1]])}return {valid:rec(tree,[]),...m};
}

function clauseFactor(c){let vs=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++)if(c.some(l=>((w>>vs.indexOf(Math.abs(l)))&1)===Number(l>0)))ok.push(w);return {vs,ok}}
module.exports={supportTree,treeCheck,clauseFactor};
