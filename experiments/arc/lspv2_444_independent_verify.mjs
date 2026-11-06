// LSPV-2/444: independent host-language source-bit sensitivity referee.
// NOT a Reingold implementation and NOT an FLMV native-machine measurement.
import fs from 'node:fs';
import crypto from 'node:crypto';
const file=process.argv[2]||new URL('./results.json',import.meta.url).pathname;
const raw=JSON.parse(fs.readFileSync(file,'utf8'));
let checks=0, flips=0, outcomes={MALFORMED:0,OUTSIDE:0};
function check(ok,what){checks++;if(!ok)throw Error(`check ${checks}: ${what}`)}
function decode(bitstr){
 if(!/^[01]+$/.test(bitstr)||!bitstr.startsWith('10110011'))return null;
 let i=8;let unary=()=>{const from=i;while(bitstr[i]==='1')i++;if(bitstr[i]!=='0')throw Error('bad unary');i++;return i-from-1;};
 try{
  const h=unary(), n=unary(),w=Math.floor(Math.log2(3*h))+1;
  const len=8+(h+1)+(3*h+1)+12*h*(w+1)+2;
  if(h<4||h%2||n!==3*h||bitstr.length!==len||bitstr.slice(-2)!=='01')return null;
  const quartets=[],fieldpos=[];
  for(let v=0;v<h;v++){
   let q=[];
   for(let c=0;c<4;c++){
    let row=[];
    for(let j=0;j<3;j++){
      fieldpos.push(...Array.from({length:w+1},(_,k)=>i+k));
      const sign=Number(bitstr[i]),id=parseInt(bitstr.slice(i+1,i+1+w),2);i+=w+1;
      if(!(id>=1&&id<=n))return null;
      row.push([id,sign]);
    }
    if(new Set(row.map(x=>x[0])).size!==3)return null;
    q.push(row);
   }
   quartets.push(q);
  }
  return {h,quartets,fieldpos};
 }catch{return null;}
}
function classify(src){
 const parsed=decode(src);if(!parsed)return 'MALFORMED';
 const {h,quartets}=parsed, owners=new Map(),edges=[];
 for(let v=0;v<h;v++){
  const rows=quartets[v].map(r=>r.slice().sort((a,b)=>a[0]-b[0]));
  const ids=rows[0].map(x=>x[0]);
  if(rows.some(r=>r.some((x,j)=>x[0]!==ids[j])))return 'OUTSIDE';
  const seen=new Set(rows.map(r=>r.map(x=>x[1]).join('')));
  if(seen.size!==4)return 'OUTSIDE';
  let ps=Array.from(seen,x=>[...x].reduce((a,b)=>a^Number(b),0));
  if(!ps.every(x=>x===ps[0]))return 'OUTSIDE';
  for(const id of ids){if(!owners.has(id))owners.set(id,[]);owners.get(id).push(v)}
 }
 let adj=Array.from({length:h},()=>[]);
 for(const [id,ends] of owners){
  if(ends.length!==2||ends[0]===ends[1])return 'OUTSIDE';
  const [u,v]=ends;adj[u].push([v,id]);adj[v].push([u,id]);
 }
 for(let v=0;v<h;v++){
  adj[v].sort((a,b)=>a[0]-b[0]);
  if(adj[v].length!==3||new Set(adj[v].map(x=>x[0])).size!==3)return 'OUTSIDE';
  for(let j=0;j<3;j++){
   const [nb,id]=adj[v][j];if(v<nb&&id!==3*v+j+1)return 'OUTSIDE';
  }
 }
 return 'TSEITIN';
}
check(raw.status==='PASS','producer status');
for(const c of raw.cases){
 const src=c.source_bits,p=decode(src);
 check(p!==null,'packet');
 check(crypto.createHash('sha256').update(src).digest('hex')===c.sha256,'source integrity');
 check(classify(src)==='TSEITIN','valid original member');
 check(p.fieldpos.length===c.literal_bit_mutants,'position cardinality');
 const nonmembers=new Set();
 for(const pos of p.fieldpos){
  const altered=src.slice(0,pos)+(src[pos]==='1'?'0':'1')+src.slice(pos+1);
  const result=classify(altered);
  check(result!=='TSEITIN',`single bit ${pos} must break exact membership`);
  outcomes[result]++;nonmembers.add(pos);flips++;
 }
 check(nonmembers.size===p.fieldpos.length,'unique fields');
 check(classify(src.slice(0,-1)+'0')==='MALFORMED','trailer');
 check(classify(src+'1')==='MALFORMED','length');
}
check(flips===raw.counters.single_literal_bit_mutants,'mutation total');
console.log(JSON.stringify({status:'PASS',cases:raw.cases.length,bit_flips:flips,checks,outcomes}));
