// LSPV-1/399 independent readback verifier; run: node script.js raw.json
const fs=require('node:fs'),r=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let checks=0;const ok=(x,m)=>{if(!x)throw Error(m);checks++};
function gamma(n){let s=n.toString(2);return '0'.repeat(s.length-1)+s}
function w(k){return Math.ceil(Math.log2(k+1))}
function h(k){return '1011'+gamma(k+1)+gamma(k+1)}
function encode(k,e,i){let s=h(k);for(let j=1;j<=k;j++)
s+='010'+(j<=e?((i>>(j-1))&1):1)+j.toString(2).padStart(w(k),'0');return s}
function label(bits,k){
 if(!bits.startsWith(h(k))||bits.length!==h(k).length+k*(4+w(k)))return null;
 let cls=[];
 for(let p=h(k).length;p<bits.length;p+=4+w(k)){
  const c=bits.slice(p,p+4+w(k)),id=parseInt(c.slice(4),2);
  if(c.slice(0,3)!=='010'||!['0','1'].includes(c[3])||id<1||id>k)return null;
  cls.push([id,c[3]==='1']);
 }
 for(let a=0;a<2**k;a++)if(cls.every(([id,s])=>Boolean(a&(1<<(id-1)))===s))return true;
 return false;
}
let views=0,unsat=0;
for(const f of r.fixtures){
 ok(f.length===h(f.k).length+f.k*(4+w(f.k)),'length');
 if('bits' in f){
  ok(f.bits===encode(f.k,f.ell,f.i),'stored bytes');
  ok(label(f.bits,f.k)===true,'SAT witness');views++;
 }else{
  ok(label(f.unsat_bits,f.k)===false,'UNSAT witness');unsat++;
  ok(label('0000'+f.unsat_bits.slice(4),f.k)===null,'malformed');
 }
}
for(const K of [2,3,4,8,16,32]){
 const o=r.exponent.find(x=>x.K===K);ok(!!o,'missing K');
 const [a,b]=o.lambda,[c,d]=o.M_exponent;
 ok(a*d+c*b===11*b*d/10,'boundary');
 ok(o.peak_exponent[0]===a&&o.peak_exponent[1]===b,'peak');
}
let total=0;
for(const k of [2,3,4,5,6,8,10,12])for(let ell=1;ell<=Math.min(k,4);ell++){
 const all=new Set();for(let i=0;i<2**ell;i++){
  const s=encode(k,ell,i);ok(label(s,k)===true,'all SAT');all.add(s);total++;
 }
 ok(all.size===2**ell,'distinct');
}
ok(total===r.satCount,'total SAT');
ok(unsat===r.unsatCount,'UNSAT count');
ok(r.malformed===16,'malformed count');
ok(r.checks===665,'producer checks');
console.log(JSON.stringify({checks,views:total,UNSAT:unsat,fixtures:r.fixtures.length}));
