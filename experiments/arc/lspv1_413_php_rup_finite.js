// LSPV-1/413 independent compact PHP RES -> RUP finite checker; node >=18.
const assert=require('assert');
function php(P,H){const c=[];for(let p=0;p<P;p++)c.push(Array.from({length:H},(_,h)=>p*H+h+1));for(let h=0;h<H;h++)for(let p=0;p<P;p++)for(let q=p+1;q<P;q++)c.push([-p*H-h-1,-q*H-h-1]);return c}
function rup(db,C){const a=new Map();for(const l of C.map(x=>-x)){const v=Math.abs(l),value=l>0;if(a.has(v)&&a.get(v)!==value)return true;a.set(v,value)}let changed=true;while(changed){changed=false;for(const cl of db){if(cl.some(x=>a.has(Math.abs(x))&&a.get(Math.abs(x))===(x>0)))continue;const free=cl.filter(x=>!a.has(Math.abs(x)));if(!free.length)return true;if(free.length===1){const v=Math.abs(free[0]),value=free[0]>0;if(!a.has(v)){a.set(v,value);changed=true}}}}return false}
function truth(cs,n){for(let mask=0;mask<2**n;mask++)if(cs.every(c=>c.some(l=>Boolean(mask&(1<<(Math.abs(l)-1)))===(l>0))))return mask;return null}
let assertions=0,out=[];
for(let h=1;h<=3;h++)for(const pigeons of [h,h+1]){const src=php(pigeons,h),SAT=truth(src,pigeons*h)!==null;assert.strictEqual(SAT,pigeons===h);assertions++;let clauses=src.map(c=>new Set(c)), active=new Set(clauses.keys()), seen=new Map(clauses.map((c,i)=>[ [...c].sort((a,b)=>a-b).join(','),i])),steps=0;
outer:for(let v=1;v<=pigeons*h;v++){const pos=[...active].filter(i=>clauses[i].has(v)),neg=[...active].filter(i=>clauses[i].has(-v));for(const i of [...pos,...neg])active.delete(i);for(const i of pos)for(const j of neg){const cl=new Set([...clauses[i],...clauses[j]]);cl.delete(v);cl.delete(-v);if([...cl].some(l=>cl.has(-l)))continue;const key=[...cl].sort((a,b)=>a-b).join(',');let k=seen.get(key);if(k===undefined){assert(rup(clauses.map(c=>[...c]),[...cl]));assertions++;k=clauses.length;clauses.push(cl);seen.set(key,k);steps++}active.add(k);if(!cl.size)break outer}}
assert.strictEqual(clauses.some(c=>!c.size),!SAT);assertions++;out.push({holes:h,pigeons,SAT,source_clauses:src.length,derived_RUP_steps:steps})}
assert(!rup([[1]],[]));assertions++;assert(rup([[1]],[1]));assertions++;assert(!rup([[1]],[2]));assertions++;
console.log(JSON.stringify({status:'PASS',assertions,rows:out},null,2));
