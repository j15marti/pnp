function experiment(C,V,owners,cap=2500000){
 let work=0, events={index:0,queue:0,reads:0,parents:0,replay:0,filter:0,tries:0,maskBits:0},peakEntries=0;
 function tick(k,n=1){if(work+n>cap)throw Error("cap");work+=n;events[k]+=n}
 const key=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
 const rows=C.map((c,i)=>({c,mask:1n<<BigInt(owners[i]),p:[],original:i})),base=rows.length;
 const R=rows.slice(),idx=new Map(),units=[],seen=new Set();
 function index(row,i){seen.add(key(row.c));for(let l of row.c){tick("index");if(!idx.has(l))idx.set(l,[]);idx.get(l).push(i)}if(row.c.length<=1)units.push(i)}
 R.forEach(index);peakEntries=R.reduce((s,x)=>s+x.c.length,0);
 function up(target,rs=R,ix=idx,us=units){
   let A=new Map(),Q=[],reason=new Map();
   function set(l,j){if(A.has(-l))return [reason.get(-l),j];if(!A.has(l)){A.set(l,true);Q.push(l);reason.set(l,j)}return null}
   function parents(js){let S=new Set(),stack=js.filter(j=>j>=0);while(stack.length){let j=stack.pop();if(S.has(j))continue;S.add(j);tick("parents");for(let l of rs[j].c){tick("parents");let q=reason.get(-l);if(q>=0)stack.push(q)}}return [...S].sort((a,b)=>a-b)}
   for(let l of target){let z=set(-l,-1);if(z)return []}
   for(let j of us){tick("queue");let c=rs[j].c;if(!c.length)return parents([j]);let z=set(c[0],j);if(z)return parents(z)}
   for(let h=0;h<Q.length;h++){tick("queue");for(let j of ix.get(-Q[h])||[]){let c=rs[j].c,k=0,u=0,sat=false;for(let l of c){tick("reads");if(A.has(l)){sat=true;break}if(!A.has(-l)){k++;u=l}}if(sat)continue;if(!k)return parents([j]);if(k===1){let z=set(u,j);if(z)return parents(z)}}}
   return null
 }
 function verify(target,ps,rs){let A=new Set(target.map(l=>-l));for(;;){let ch=false;for(let j of ps){let c=rs[j].c,k=0,u=0,sat=false;for(let l of c){tick("replay");if(A.has(l)){sat=true;break}if(!A.has(-l)){k++;u=l}}if(sat)continue;if(!k)return true;if(k===1&&!A.has(u)){if(A.has(-u))return true;A.add(u);ch=true}}if(!ch)return false}}
 function add(c,ps){if(!verify(c,ps,R))throw Error("local RUP replay failure");let mask=0n;for(let j of ps){tick("maskBits",Math.max(1,Math.ceil((Math.max(...owners)+1)/64)));mask|=R[j].mask}let row={c,mask,p:ps};index(row,R.length);R.push(row);peakEntries=Math.max(peakEntries,R.reduce((s,x)=>s+x.c.length,0));return row}
 const lits=V.flatMap(v=>[v,-v]),U=[[],...lits.map(l=>[l])];for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++)for(let a of [1,-1])for(let b of [1,-1])U.push([a*V[i],b*V[j]]);
 let status="UNKNOWN",epochs=0,why=null;
 try{for(;;){epochs++;let before=R.length;for(let c of U){tick("tries");if(seen.has(key(c)))continue;let ps=up(c);if(ps!==null){add(c,ps);if(!c.length){status="UNSAT";break}}}if(status==="UNSAT"||before===R.length)break}}catch(e){if(String(e)!=="Error: cap")throw e;why="cap"}
 const initial={status,epochs,why,work,events:{...events},learned:R.length-base,peakEntries};
 // Do not use any learned row if any deleted owner is in its recursively reconstructed support.
 const candidates=[...new Set(owners)],results=[];
 // Baseline and hybrid use exact same UP test (no new learned candidates). Separate cap on each set; retain prior work.
 const limits=5000000;cap=limits;
 for(let i of candidates){
  let row={owner:i};
  for(let mode of ["baseline","hybrid"]){
   let start=work;
   try{let S=[],I=new Map(),Z=[];let bit=1n<<BigInt(i);for(let j=0;j<(mode==="baseline"?base:R.length);j++){tick("filter");let x=R[j];if(x.mask&bit)continue;let k=S.length;S.push(x);for(let l of x.c){tick("index");if(!I.has(l))I.set(l,[]);I.get(l).push(k)}if(x.c.length<=1)Z.push(k)}
   let ps=up([],S,I,Z);if(ps!==null&&!verify([],ps,S))throw Error("context replay failed");let root=0n;if(ps)for(let j of ps){tick("maskBits",Math.max(1,Math.ceil((Math.max(...owners)+1)/64)));root|=S[j].mask}if(root&bit)throw Error("owner leak");
   row[mode]={status:ps!==null?"UNSAT":"UNKNOWN",work:work-start,retained:S.length,core:ps!==null?root.toString(16):null};
   }catch(e){if(String(e)!=="Error: cap")throw e;row[mode]={status:"UNKNOWN_CAP",work:work-start}}
  }results.push(row)
 }
 return {initial,work,events,cap,base,proof:R.slice(base).map(x=>({c:x.c,p:x.p,mask:x.mask.toString(16)})),results};
}
if(typeof module!=="undefined")module.exports={experiment};
