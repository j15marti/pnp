// Independently implemented source, signed neighbor, and proof checker for LSPV-2 349.
'use strict';
function test(x,m){if(!x)throw Error(m||'failed assertion');}
function verify(j){
let t=0;
const chk=(v,m)=>{test(v,m);t++;};
const F=j.source,G=j.guarded_source;
function models(clauses,n){let z=0;for(let a=0;a<(1<<n);a++){let all=true;for(const clause of clauses){let some=false;for(const l of clause){if(Boolean(a&(1<<(Math.abs(l)-1)))===(l>0)){some=true;break;}}if(!some){all=false;break;}}if(all)z++;}return z;}
function proof(clauses,nodes){const c=clauses.map(x=>new Set(x));for(const [a,b,v] of nodes){chk(a>0&&b>0&&a<=c.length&&b<=c.length&&a!==b,'parent');const x=c[a-1],y=c[b-1];chk((x.has(v)&&y.has(-v))||(y.has(v)&&x.has(-v)),'pivot');const z=new Set();for(const l of x)if(Math.abs(l)!==v)z.add(l);for(const l of y)if(Math.abs(l)!==v)z.add(l);chk(![...z].some(l=>z.has(-l)),'tautological resolvent');c.push(z);}chk(c[c.length-1].size===0,'not contradiction');return c;}
chk(F.length===7&&G.length===14,'source count');
for(let i=0;i<F.length;i++){chk(G[i][0]===6&&G[i+7][0]===-6,'guard');chk(JSON.stringify(G[i].slice(1))===JSON.stringify(F[i]),'positive');chk(JSON.stringify(G[i+7].slice(1))===JSON.stringify(F[i]),'negative');}
chk(models(F,5)===0&&models(G,6)===0,'UNSAT');
for(const [a,n,del] of [[F,5,j.source_deletion_models],[G,6,j.guard_deletion_models]]){
 for(let i=0;i<a.length;i++){
   chk(models(a.filter((_,k)=>i!==k),n)===del[i],'deletion');
   for(let k=0;k<a[i].length;k++){const b=a.map(cl=>cl.slice());b[i][k]*=-1;chk(models(b,n)>0,'signed flip');}
 }
}
proof(F,j.source_proof);proof(G,j.guarded_proof);
chk(j.source_proof.length===9&&j.guarded_proof.length===19,'cost');
const encode=(c,n)=>'p cnf '+n+' '+c.length+'\n'+c.map(v=>[...v,0].join(' ')+'\n').join('');
chk(encode(F,5).length===74&&encode(G,6).length===174,'bytes');
let rejected=0;for(const malformed of [j.guarded_proof.slice(0,-1),[[2,4,3],...j.guarded_proof.slice(1)],[[99,1,1],...j.guarded_proof.slice(1)]])try{proof(G,malformed);}catch(e){rejected++;}
chk(rejected===3,'corrupted proof');
return {independent_assertions:t,costs:[j.source_proof.length,j.guarded_proof.length],source_bytes:74,guarded_bytes:174,guarded_single_source_deletions:j.guard_deletion_models.length,rejected};
}
if(typeof require!=='undefined'&&typeof module!=='undefined'&&require.main===module){const fs=require('fs');console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));}
