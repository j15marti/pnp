// LSPV-1/399: independent explicit/lazy CNF interface cost controls.
// Run: node lspv1_399_virtual_batch_producer.js [output.json]
const fs=require('node:fs');
const gamma=n=>{const b=n.toString(2);return '0'.repeat(b.length-1)+b};
const width=k=>Math.ceil(Math.log2(k+1));
const head=k=>'1011'+gamma(k+1)+gamma(k+1);
function enc(k,ell,i){
  let s=head(k), w=width(k);
  for(let j=1;j<=k;j++){
    let bit=j<=ell?((i>>(j-1))&1):1;
    s+='010'+bit+j.toString(2).padStart(w,'0');
  }
  return s;
}
function vbit(k,ell,i,p){
  let h=head(k);if(p<h.length)return h[p];
  const w=width(k),t=4+w,z=p-h.length,j=Math.floor(z/t)+1,r=z%t;
  if(r<3)return '010'[r];
  if(r===3)return String(j<=ell?((i>>(j-1))&1):1);
  return j.toString(2).padStart(w,'0')[r-4];
}
function sat(bits,k){
  const h=head(k),w=width(k);
  if(!bits.startsWith(h)||bits.length!==h.length+k*(4+w))return null;
  const cs=[];
  for(let p=h.length;p<bits.length;p+=4+w){
    const field=bits.slice(p,p+4+w),id=parseInt(field.slice(4),2);
    if(field.slice(0,3)!=='010'||!['0','1'].includes(field[3])||id<1||id>k)return null;
    cs.push([id,field[3]==='1']);
  }
  for(let a=0;a<(1<<k);a++)if(cs.every(([v,s])=>Boolean(a&(1<<(v-1)))===s))return true;
  return false;
}
function main(){
 let checks=0, satCount=0,unsatCount=0, malformed=0;const fixtures=[];
 const assert=(cond,msg)=>{if(!cond)throw Error(msg);checks++};
 for(const k of [2,3,4,5,6,8,10,12]){
  for(let ell=1;ell<=Math.min(k,4);ell++){
   const seen=new Set();
   for(let i=0;i<(1<<ell);i++){
    const str=enc(k,ell,i);
    assert([...str].every((c,j)=>c===vbit(k,ell,i,j)), 'virtual mismatch');
    assert(sat(str,k)===true,'bad SAT view');
    assert(!seen.has(str),'duplicate');
    seen.add(str);satCount++;
    if(i===0||i===(1<<ell)-1)fixtures.push({k,ell,i,bits:str,length:str.length});
   }
   assert(seen.size===(1<<ell),'view count');
  }
  let u=enc(k,1,1),w=width(k),p=head(k).length+(k-1)*(4+w);
  u=u.slice(0,p+3)+'0'+(1).toString(2).padStart(w,'0')+u.slice(p+4+w);
  assert(sat(u,k)===false,'bad UNSAT');unsatCount++;
  assert(sat('0000'+u.slice(4),k)===null,'bad tag accepted');malformed++;
  assert(sat(u.slice(0,-1),k)===null,'truncated accepted');malformed++;
  fixtures.push({k,unsat_bits:u,length:u.length});
 }
 const exponent=[];
 for(const K of [2,3,4,8,16,32]){
  const den=5*K;const rDen=10*den;
  const num=11*den-10;
  assert(num+10===11*den,'non-exact exponent');
  assert(den>5,'no space slack');
  exponent.push({K,lambda:[1,den], M_exponent:[num,rDen],
   product_exponent:[11,10],peak_exponent:[1,den]});
 }
 return {tag:'LSPV1_399_EXPLICIT_VIRTUAL_BATCH',
  encoding:'tag1011,gamma(V+1),gamma(k+1),unit gamma(2),polarity,fixed-width IDs',
  checks,satCount,unsatCount,malformed,exponent,fixtures,
  provenance:'finite independent grammar checks; symbolic exponent theorem separate'};
}
const obj=main();
fs.writeFileSync(process.argv[2]||'/tmp/lspv1_399_raw.json',JSON.stringify(obj,null,2)+'\n');
console.log(JSON.stringify({checks:obj.checks,sat:obj.satCount,unsat:obj.unsatCount,malformed:obj.malformed,fixtures:obj.fixtures.length}));
