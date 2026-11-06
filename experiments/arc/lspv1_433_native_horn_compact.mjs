// LSPV-1/433: independent original-source RES-only exhaustive witness (Node 22).
// Strict native RES fragment of original R_mix341; no DEF/LOCAL ambiguity.
function norm(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);}
function make(m){
 const src=[[1],[-1,2],...Array.from({length:m},(_,i)=>[-2,i+3]),Array.from({length:m},(_,i)=>-i-3)];
 const sat=(clauses,mask)=>clauses.every(c=>c.some(l=>Boolean(mask & (1<<(Math.abs(l)-1)))===(l>0)));
 let checks=0;
 for(let mask=0;mask<(1<<(m+2));mask++){if(sat(src,mask))throw Error("Unexpected source model");checks++;}
 for(let j=0;j<src.length;j++){let found=false;for(let a=0;a<(1<<(m+2));a++)if(sat(src.filter((_,i)=>i!==j),a)){found=true;break;}if(!found)throw Error("Dispensable source "+j);checks++;}
 const db=new Map(src.map((c,i)=>['C'+i,norm(c)])),proof=[];let ref='C'+(src.length-1);
 function add(id,left,right,p){let a=db.get(left),b=db.get(right);if(!a.includes(p)||!b.includes(-p))throw Error("Wrong oriented pivot");let c=norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);if(c.some(x=>c.includes(-x)))throw Error("Tautology");db.set(id,c);proof.push({id,left,right,p,clause:c});checks++;return id;}
 for(let i=0;i<m;i++)ref=add('R'+i,'C'+(2+i),ref,i+3);
 ref=add('RH','C1',ref,2);ref=add('BOTTOM','C0',ref,1);
 if(db.get(ref).length||proof.length!==src.length-1||proof.length!==m+2)throw Error('Invalid minimal proof');
 return {m,source_clauses:src,paid:proof.length,steps:proof,checks};
}
const rows=Array.from({length:7},(_,i)=>make(i+1));
if(rows[2].source_clauses.some(c=>c.length>3)||rows[2].paid!==5)throw Error('3-CNF witness failed');
console.log(JSON.stringify({status:'PASS',model:'native strict RES fragment',rows:rows.map(r=>({m:r.m,sources:r.source_clauses.length,paid:r.paid})),assertions:rows.reduce((n,r)=>n+r.checks,0)},null,2));
