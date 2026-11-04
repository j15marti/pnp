// LSPV-4/388 independent Node verifier. Usage: node script.js raw.json
const fs=require('fs'),a=require('assert');
const result=JSON.parse(fs.readFileSync(process.argv[2]||'lspv4_388_results.json','utf8'));
let checks=0;function yes(v){a.ok(v);checks++}
function bits(i,n){return Array.from({length:n},(_,j)=>(i>>j)&1)}
function ev(cs,b){return cs.every(c=>c.some(l=>((b[Math.abs(l)-1]===1)===(l>0))))}
function proj(u,e,cs){const ans=[];for(let i=0;i<(1<<u);i++){let found=0;for(let j=0;j<(1<<e);j++)if(ev(cs,bits(i,u).concat(bits(j,e)))){found=1;break}ans.push(found)}return ans}
const base=[];for(const t of [1,-1,2,-2])base.push([t]);for(const x of [1,-1])for(const y of [2,-2])base.push([x,y]);
let sat=0,unsat=0;
for(let mask=0;mask<(1<<base.length);mask++){
 const H=base.filter((_,j)=>(mask>>j)&1);
 let b=false;for(let i=0;i<4;i++)if(ev(H,bits(i,2)))b=true;
 const guarded=H.map(c=>[-1,...c.map(l=>l>0?l+1:l-1)]);
 const relation=proj(1,2,guarded);
 yes(relation[0]===1);yes(relation[1]===Number(b));
 if(b)sat++;else unsat++;
}
yes(sat===result.counts.guard_sat);yes(unsat===result.counts.guard_unsat);
for(const f of result.fixtures){
 const v=proj(f.u,f.e,f.clauses);
 const lexico=Array.from({length:1<<f.u},(_,j)=>{
  const index=Array.from({length:f.u},(_,i)=>((j>>(f.u-i-1))&1)<<i).reduce((s,x)=>s+x,0);
  return v[index];
 });
 yes(JSON.stringify(lexico)===JSON.stringify(f.projected_relation));
}
for(const o of [{u:1,e:1,clauses:[[-1,2],[1,-2]]},{u:1,e:1,clauses:[[1,2],[1,-2]]},{u:1,e:1,clauses:[[2],[-2]]},{u:1,e:1,clauses:[]}])yes(proj(o.u,o.e,o.clauses).length===2);
console.log(JSON.stringify({independent_checks:checks,guard_sat:sat,guard_unsat:unsat,verified_fixtures:result.fixtures.length}));
