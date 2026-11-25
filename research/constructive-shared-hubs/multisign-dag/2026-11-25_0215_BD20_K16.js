// node script.js path/to/BS19_results.json (immutable commit ff92a1c3)
const j=JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'));
const k=j.common.find(x=>x.K===16),C=k.residual.C,log=k.residual.log,vars=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b);
function val(x,l){return ((x>>>(Math.abs(l)-1))&1)^(l<0?1:0)}
function nae(x,c){return c.some(l=>val(x,l)!==val(x,c[0]))}
function rank(rows){let p={};for(let x of rows){while(x){let i=31-Math.clz32(x);if(p[i])x^=p[i];else{p[i]=x;break}}}return Object.keys(p).length}
const rows=C.filter(c=>c.length>3).flatMap(c=>c.slice(1).map(v=>(1<<(Math.abs(v)-1))^(1<<(Math.abs(c[0])-1))));
let models=0,proj=new Set(),first=null;
for(let z=0;z<(1<<vars.length);z++){let x=0;vars.forEach((v,i)=>{if(z>>i&1)x|=1<<(v-1)});if(C.every(c=>nae(x,c))){models++;proj.add(x&~(1<<18));if(first===null)first=x;}}
let lift=first;for(const {v,bucket} of log.slice().reverse()){let ok=false;for(const b of [0,1]){const x=(lift&~(1<<(v-1)))|(b<<(v-1));if(bucket.every(t=>nae(x,[v,...t]))){lift=x;ok=true;break}}if(!ok)throw Error("bad lift")}
const raw=j.source.O.every(o=>{let z=0;o.t.forEach((v,i)=>z|=((lift>>>v)&1)<<i);return !o.bad.includes(z)});if(!raw)throw Error("bad source");
console.log(JSON.stringify({vars,guard:[],owners:C.length,wide_owners:C.filter(c=>c.length>3).length,wide_observation_rank:rank(rows),full_models:models,pivot19_distinct_exterior_models:proj.size,reference_first_model:first,reverse_lift:lift,source_verified:raw,reverse_log_length:log.length},null,2));