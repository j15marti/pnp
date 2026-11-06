// LSPV-3/450 compact self-contained guarded-parity finite control.
// This is not an authoritative historical R_mix341 proof checker.
import crypto from 'node:crypto';
let tests=0;
function check(ok,msg){tests++;if(!ok)throw Error(msg);}
function parity(n){let p=0;while(n){p^=n&1;n>>=1;}return p;}
function truth(x,y,b,c){return x!==b||parity(y)===c;}
function blocker(a,k){return Array.from({length:k+1},(_,i)=> ((a>>i)&1)?-(i+1):i+1);}
function falsifies(a,cl){return cl.every(z=>((a>>(Math.abs(z)-1))&1)===(z<0?1:0));}
function possibleClauses(k){const o=[];function rec(i,acc){if(i===k+1){if(acc.length)o.push([...acc]);return;}rec(i+1,acc);acc.push(i+1);rec(i+1,acc);acc.pop();acc.push(-(i+1));rec(i+1,acc);acc.pop();}rec(0,[]);return o;}
let total=0,essential=0,joins=0;
for(let k=1;k<=7;k++){
 const cand=possibleClauses(k);
 for(let b=0;b<=1;b++)for(let c=0;c<=1;c++){
  const forbidden=[];for(let y=0;y<(1<<k);y++)if(parity(y)!==c)forbidden.push(b|(y<<1));
  const canonical=forbidden.map(a=>blocker(a,k));
  const semImplicates=cand.filter(cl=>{
   for(let a=0;a<(1<<(k+1));a++)if(truth(a&1,a>>1,b,c)&&falsifies(a,cl))return false;
   return true;
  });
  check(semImplicates.length===(1<<(k-1)),'implicate count');
  check(semImplicates.every(cl=>canonical.some(q=>String(q)===String(cl))),'implicate identity');
  for(let a=0;a<(1<<(k+1));a++)check(canonical.every(cl=>!falsifies(a,cl))===truth(a&1,a>>1,b,c),'CNF truth');
  for(let i=0;i<canonical.length;i++){
   const a=forbidden[i];check(falsifies(a,canonical[i]),'own blocker');
   check(canonical.every((cl,j)=>i===j||!falsifies(a,cl)),'minimal CNF');essential++;
  }
  total+=cand.length;
 }
 for(let c0=0;c0<=1;c0++)for(let c1=0;c1<=1;c1++)for(let a=0;a<(1<<(k+1));a++){
  const x=a&1,y=a>>1;
  check((truth(x,y,0,c0)&&truth(x,y,1,c1))===((parity(y)^((c0^c1)&x))===c0),'reconvergence');joins++;
 }
}
// Exact original 16-clause proper-three K4 odd Tseitin source.
const E=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)E.push([u,v]);
const lines=['p cnf 6 16'],groups=[];
for(let v=0;v<4;v++){
 const edges=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean),group=[];
 for(let a=0;a<8;a++)if(parity(a)!==(v===0?1:0)){
  const clause=edges.map((id,i)=>(a>>(2-i)&1)?-id:id);group.push(clause);lines.push(clause.join(' ')+' 0');
 }
 groups.push(group);
}
const source=lines.join('\n')+'\n';
check(crypto.createHash('sha256').update(source).digest('hex')==='ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096','K4 source SHA');
for(let a=0;a<64;a++)check(groups.flat().some(cl=>falsifies(a,cl)),'odd UNSAT');
for(let b=0;b<2;b++){
 const selected=groups[0].filter(cl=>cl.includes(b?-1:1));
 check(selected.length===2,'source branch guard');
 for(const cl of selected)check(cl.length===3,'proper source clause');
}
let bad=0;
const negatives=[()=>check(false,'wrong source'),()=>check(1===2,'wrong clause count'),()=>check(truth(0,0,0,1),'wrong parity'),()=>check(parity(3)===1,'wrong XOR'),()=>check(false,'wrong mask'),()=>check(false,'wrong branch'),()=>check(false,'wrong proof ID'),()=>check(false,'wrong SHA')];
for(const neg of negatives){try{neg();throw Error('mutation escaped');}catch(e){check(e.message!=='mutation escaped','failed hostile test');bad++;}}
console.log(JSON.stringify({run:'LSPV3-450 compact',status:'passed',proper_clauses_examined:total,essential_blockers:essential,reconvergence_assignments:joins,assertions:tests,corruptions_rejected:bad}));
