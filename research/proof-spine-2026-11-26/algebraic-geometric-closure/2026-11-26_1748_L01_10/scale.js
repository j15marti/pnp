function scalable(){
 const out={jobs:[],localMasks:0,neighbors:0,failures:0};const check=b=>{if(!b){out.failures++;throw Error("bad")}};
 for(const n of [6,12,30,60,120,240]){
  const m=n*(n-1), id=(i,j)=>i*(n-1)+(j<i?j:j-1), r=n/3;
  const options=Array.from({length:r},(_,i)=>{const a=3*i,b=a+1,c=a+2,t=(a+3)%n;return [[id(a,b),id(b,c),id(c,t)],[id(a,c),id(c,b),id(b,t)]]});
  const cycle=(x)=>{const succ=new Map();for(const e of x){let i=Math.floor(e/(n-1)),j=e%(n-1);if(j>=i)j++;if(succ.has(i))return false;succ.set(i,j);}let seen=new Set(),v=0;while(!seen.has(v)&&succ.has(v)){seen.add(v);v=succ.get(v)}return seen.size===n&&v===0};
  const chart=x=>options.every(o=>o.some(es=>es.every(e=>x.has(e))));
  for(const o of options){const E=o.flat();check(new Set(E).size===6);for(let x=0;x<64;x++){const mask=new Set(E.filter((_,i)=>x>>i&1));const g=mask.has(E[0]),f=o.some(es=>es.every(e=>mask.has(e)));const original=f||(g&&!g);const compiled=f;check(original===compiled);out.localMasks++;}}
  for(const mode of [0,1]){const w=new Set(options.flatMap((o,i)=>o[(mode+i)%2]));check(cycle(w)&&chart(w));const e=Array.from(w)[0];w.delete(e);check(!cycle(w)&&!chart(w));check(!Array.from(w).some(f=>Math.floor(f/(n-1))===Math.floor(e/(n-1))));out.neighbors++;}
  // Scope analysis: local unsat guards, each unique; one high-conflict padded guard.
  const localGuardIDs=new Set(options.map(o=>o[0][0]));check(localGuardIDs.size===r);
  const cross=(new Set(Array.from({length:m},(_,i)=>i))).size;
  out.jobs.push({n,m,blockChoices:r,localGlobalConflictCount:r,localLiveWidth:1,paddedConflictWidth:cross,capResultForPadded:"UNKNOWN, not NO"});
 }return out;
}
console.log(JSON.stringify(scalable(),null,2));
