// LSPV-1/420 independent finite referee. Zero Python imports, zero dependencies.
import fs from 'node:fs';
const raw=JSON.parse(fs.readFileSync(process.argv[2] || new URL('./raw420.json',import.meta.url),'utf8'));
let checks=0;
function ok(test,msg){checks++;if(!test)throw new Error('FAIL '+msg);}
function clauses2(){return [[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]]}
function clauses3(){return Array.from({length:8},(_,b)=>Array.from({length:3},(_,i)=>(b&(1<<i))?i+1:-(i+1)))}
function evaluate(F,assign){return F.every(c=>c.some(l=>l>0?assign[l-1]:!assign[-l-1]));}
function sentinel(bits){const n=bits.length;return 'p cnf '+(n+1)+' '+n+'\n'+bits.map((v,i)=>(n+1)+' '+(v?i+1:-(i+1))+' 0\n').join('')}
function parseSent(text,n){
 const all=Array.from({length:1<<n},(_,mask)=>Array.from({length:n},(_,i)=>Boolean(mask&(1<<i))));
 const match=all.filter(a=>sentinel(a)===text);
 return match.length===1?match[0]:null;
}
for(const n of [2,3]){
 let nSAT=0,nUNSAT=0,rejects=0,tests=0;
 const Universe=n===2?clauses2():clauses3();
 for(let subset=0;subset<256;subset++){
  const F=Universe.filter((_,i)=>(subset&(1<<i))!==0);
  let satCount=0,rCount=0;
  for(let m=0;m<1<<n;m++){
   const w=Array.from({length:n},(_,i)=>Boolean(m&(1<<i)));
   const source=sentinel(w),decoded=parseSent(source,n);
   ok(decoded!==null&&decoded.every((a,i)=>a===w[i]),'canonicity');
   const result=evaluate(F,w);
   const clauses=decoded.map((v,i)=>[n+1,v?i+1:-(i+1)]);
   ok(evaluate(clauses,[...w,true]),'legitimate SAT sentinel');
   if(result){satCount++;rCount++;}
   tests++;
  }
  ok((satCount===0)===(rCount===0),'one-sided theorem');
  if(satCount){nSAT++}else{nUNSAT++}
  rejects+=rCount;
 }
 ok(nSAT===raw.stats['n'+n].sat,'SAT source count');
 ok(nUNSAT===raw.stats['n'+n].unsat,'UNSAT source count');
 ok(tests===raw.stats['n'+n].sentinels,'sentinel count');
 ok(rejects===raw.stats['n'+n].rejects,'false reject count');
}
for(let n of [2,3,4]){
 let b=sentinel(Array(n).fill(false));
 for(let bad of [b+'extra\n',b.replace('p cnf','q cnf'),b.replace(' 0\n',' 1\n'),b.replaceAll('\n','\r\n'),b.slice(0,-1)])
  ok(parseSent(bad,n)===null,'mutant must not be genuine sentinel');
}
for(const r of raw.sample_records){
 let ws=[];
 for(let m=0;m<(1<<r.n);m++){
  let w=Array.from({length:r.n},(_,i)=>Boolean(m&(1<<i)));
  if(evaluate(r.clauses,w))ws.push(w.map(v=>v?'1':'0').join(''));
 }
 ok(JSON.stringify(ws.sort())===JSON.stringify(r.rejects.slice().sort()),'raw replay');
}
console.log(JSON.stringify({independent_assertions:checks,valid:true,labels:raw.stats}));
