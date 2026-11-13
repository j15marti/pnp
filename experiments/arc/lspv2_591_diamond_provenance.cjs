'use strict';
// SEPARATE SOURCE/RES reference, not an authoritative R_mix341 checker.
const a=require('node:assert/strict'),fs=require('node:fs'),h=require('node:crypto');
const hash=s=>h.createHash('sha256').update(s).digest('hex');
const sort=c=>[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const eq=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
function make(k){
 const C=[[1]],opt=[];
 for(let i=0;i<k;i++){
  const pair=[];
  for(let b=0;b<2;b++){
   const y=k+2+2*i+b;
   const first=C.push(sort([-(i+1),y]))-1;
   const second=C.push(sort([-y,i+2]))-1;
   pair.push([first,second,y]);
  }opt.push(pair);
 }
 const neg=C.push([-(k+1)])-1,n=3*k+1;
 const source=Buffer.from('p cnf '+n+' '+C.length+'\n'+C.map(c=>c.join(' ')+' 0\n').join(''));
 return {C,opt,neg,n,source};
}
function cert(k,z,choice){
 const rec=z.C.map((c,source)=>({kind:'SOURCE',source,c,parents:[]}));
 let unit=0;
 for(let i=0;i<k;i++){
  const [p,q,y]=z.opt[i][(choice>>i)&1];
  const v=rec.push({kind:'RES',parents:[unit,p],pivot:i+1,c:[y]})-1;
  unit=rec.push({kind:'RES',parents:[v,q],pivot:y,c:[i+2]})-1;
 }
 rec.push({kind:'RES',parents:[unit,z.neg],pivot:k+1,c:[]});
 return {format:'LSPV2-591-DIAMOND-REF/v1',source_sha256:hash(z.source),records:rec,summary:{source:z.C.length,resolution:2*k+1,paid_total:2*k+1,live_records:rec.length}};
}
function check(z,p){
 a.equal(p.format,'LSPV2-591-DIAMOND-REF/v1');a.equal(p.source_sha256,hash(z.source));
 const seen=new Set(),known=[];let res=0;
 for(let i=0;i<p.records.length;i++){
  const r=p.records[i];a(eq(r.c,sort(r.c)));
  a(r.c.every(t=>Number.isSafeInteger(t)&&t!==0&&Math.abs(t)<=z.n&&!r.c.includes(-t)));
  a(Array.isArray(r.parents)&&r.parents.every(t=>Number.isSafeInteger(t)&&t>=0&&t<i));
  if(r.kind==='SOURCE'){
   a.equal(r.parents.length,0);a(Number.isSafeInteger(r.source)&&r.source>=0&&r.source<z.C.length);
   a(!seen.has(r.source));seen.add(r.source);a(eq(r.c,z.C[r.source]));
  }else if(r.kind==='RES'){
   res++;a.equal(r.parents.length,2);const [left,right]=r.parents.map(t=>known[t]);
   a(Number.isSafeInteger(r.pivot)&&r.pivot!==0&&left.includes(r.pivot)&&right.includes(-r.pivot));
   const out=sort([...left.filter(t=>t!==r.pivot),...right.filter(t=>t!==-r.pivot)]);
   a(!out.some(t=>out.includes(-t)));a(eq(out,r.c));
  }else throw Error('unsupported reference-only rule');
  known.push(r.c);
 }
 a.equal(seen.size,z.C.length);a(eq(known.at(-1),[]));
 a.deepEqual(p.summary,{source:seen.size,resolution:res,paid_total:res,live_records:known.length});
}
function sem(z,s){
 const reached=new Set();if(s&1)reached.add(1);
 let changed=true;
 while(changed){changed=false;
  for(let i=1;i<z.C.length-1;i++)if(s&(1<<i)){
   const row=z.C[i],neg=row.find(v=>v<0),pos=row.find(v=>v>0);
   if(neg!==undefined&&pos!==undefined&&reached.has(-neg)&&!reached.has(pos)){
    reached.add(pos);changed=true;
   }
  }
 }
 return reached.has(z.opt.length+1);
}
function symbolic(z,s){
 if(!(s&1))return false;
 return z.opt.every(pair=>pair.some(([p,q])=>(s&(1<<p))&&(s&(1<<q))));
}
function run(){
 const result={scope:'separate SOURCE/RES reference, not historical R_mix341',accepted:0,rejected:0,exhaustive:[],source_sha256:[]};
 for(let k=1;k<=7;k++){
  const z=make(k);result.source_sha256.push({k,sha256:hash(z.source)});
  for(let c=0;c<(1<<k);c++){check(z,cert(k,z,c));result.accepted++}
  const bad=[
   p=>{p.records[1].c=[-1]},
   p=>{p.records.at(-1).pivot=999},
   p=>{p.summary.paid_total--},
   p=>{p.records.at(-1).parents[0]=p.records.length},
   p=>{p.records=p.records.filter(r=>r.kind==='SOURCE');p.records.push({kind:'RES',parents:[0,z.neg],pivot:1,c:[]});p.summary.resolution=1;p.summary.paid_total=1;p.summary.live_records=p.records.length}
  ];
  for(const change of bad){const p=cert(k,z,0);change(p);let rejects=false;
   try{check(z,p)}catch(e){rejects=true}a(rejects);result.rejected++;
  }
  if(k<=4){const mins=[];
   for(let s=0;s<(1<<z.C.length);s++){
    const v=sem(z,s);a.equal(v,symbolic(z,s));if(!v)continue;
    let minimal=true;for(let j=0;j<z.C.length;j++)if((s&(1<<j))&&sem(z,s^(1<<j))){minimal=false;break}
    if(minimal)mins.push(s);
   }
   a.equal(mins.length,1<<k);
   result.exhaustive.push({k,source_subsets:1<<z.C.length,minimum_source_supports:mins.length});
  }
 }
 a.equal(result.accepted,254);a.equal(result.rejected,35);
 const output=JSON.stringify(result,null,2)+'\n';
 if(process.argv[2])fs.writeFileSync(process.argv[2],output);
 console.log(output);
}
run();
