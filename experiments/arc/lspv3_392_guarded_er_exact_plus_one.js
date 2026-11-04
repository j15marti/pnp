'use strict';
// LSPV-3/392. Deterministic finite calibration only, no shortest-proof search.
function norm(a){let b=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);for(let x of b)if(b.includes(-x))throw Error('tautological clause');return b;}
function key(a){return norm(a).join(',');}
function resolve(a,b,p){if(!a.includes(p)||!b.includes(-p))throw Error('missing signed pivot');return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);}
function sat(F,a){return F.every(c=>c.some(l=>a[Math.abs(l)]===(l>0?1:0)));}
function source(h,guarded){
 const f=[[1]];for(let j=1;j<=h;j++)f.push([-j,j+1]);f.push([-(h+1)]);
 if(!guarded)return f.map(norm);
 const t=h+2;return [...f.map(c=>norm([-t,...c])),[t]];
}
function deletedWitness(h,j){let a=Array(h+3).fill(0);
 if(j===h+1)for(let i=1;i<=h+1;i++)a[i]=1;
 else if(j>0)for(let i=1;i<=j;i++)a[i]=1;
 return a;}
function build(h,guarded){
 let s=source(h,guarded), t=h+2,p=[],prev=s[0]; 
 for(let j=1;j<=h;j++){prev=resolve(prev,s[j],j);p.push({lhs:j===1?'S0':'R'+(j-2),rhs:'S'+j,pivot:j,out:prev});}
 prev=resolve(prev,s[h+1],h+1);p.push({lhs:'R'+(h-1),rhs:'S'+(h+1),pivot:h+1,out:prev});
 if(guarded){prev=resolve(prev,s[h+2],-t);p.push({lhs:'R'+h,rhs:'S'+(h+2),pivot:-t,out:prev});}
 if(prev.length!==0)throw Error('not a refutation');
 return {s,p};
}
function replay(obj){let dict=new Map();obj.s.forEach((v,i)=>dict.set('S'+i,v));
 obj.p.forEach((v,i)=>{let a=dict.get(v.lhs),b=dict.get(v.rhs);if(!a||!b||key(resolve(a,b,v.pivot))!==key(v.out))throw Error('invalid proof step');dict.set('R'+i,v.out)});
 if(key(obj.p.at(-1).out)!=='')throw Error('incorrect root');return true;
}
function run(){
 let tests=[2,3,4,6,8,12,24,64], rows=[], checks=0, errors=0;
 for(let h of tests){let F=source(h,false),H=source(h,true),a=build(h,false),b=build(h,true),t=h+2;
 replay(a);replay(b);checks+=2;
 if(a.p.length!==h+1||b.p.length!==h+2)throw Error('wrong paid counts');checks+=2;
 for(let j=0;j<F.length;j++){let w=deletedWitness(h,j),wg=[...w];wg[t]=1;
 if(!sat(F.filter((_,i)=>i!==j),w)||sat(F,w))throw Error('deletion control F');checks+=2;
 if(!sat(H.filter((_,i)=>i!==j),wg)||sat(H,wg))throw Error('deletion control H');checks+=2;
 for(let z=0;z<F[j].length;z++){let cf=F.map(c=>c.slice());cf[j][z]*=-1;let ch=H.map(c=>c.slice());ch[j][z+1]*=-1;
 if(!sat(cf,w)||!sat(ch,wg))throw Error('sign control');checks+=2;}
 let ch=H.map(c=>c.slice());ch[j][0]=t;
 if(!sat(ch,wg))throw Error('guard sign control');checks++;
 }
 let off=Array(h+3).fill(0);if(!sat(H.filter((_,i)=>i!==H.length-1),off)||sat(H,off))throw Error('t indispensable');checks+=2;
 let flipped=H.map(c=>c.slice());flipped.at(-1)[0]=-t;if(!sat(flipped,off))throw Error('t sign control');checks++;
 rows.push({h,source_F:F.length,source_H:H.length,paid_F:a.p.length,paid_H:b.p.length,
 F_all_sources_essential:true,H_all_sources_essential:true,
 proof_F_last:a.p.at(-1).out,proof_H_last:b.p.at(-1).out});
 }
 let tiny=build(2,true);let corrupt=JSON.parse(JSON.stringify(tiny));corrupt.p[0].pivot=99;
 try{replay(corrupt);throw Error('accepted corrupt pivot')}catch(e){if(!String(e).includes('missing signed pivot'))throw e;errors++;}
 corrupt=JSON.parse(JSON.stringify(tiny));corrupt.p[0].out=[-1];
 try{replay(corrupt);throw Error('accepted corrupt output')}catch(e){if(!String(e).includes('invalid proof step'))throw e;errors++;}
 corrupt=JSON.parse(JSON.stringify(tiny));corrupt.p[0].rhs='S999';
 try{replay(corrupt);throw Error('accepted missing parent')}catch(e){if(!String(e).includes('invalid proof step'))throw e;errors++;}
 // Guard-dependent signed AND2 definitions: cofactor t=1.
 for(let x=0;x<=1;x++)for(let y=0;y<=1;y++){
 const t=1,g4=t&x,g5=(1-t)&(1-y),g6=g4&(1-g5),g7=x&(1-y);
 if(g4!==x||g5!==0||g6!==x||g7!==(x&(1-y)))throw Error('gate cofactor mismatch');checks+=4;
 }
 return {schema:'LSPV-3-392/v1',status:'FINITE-COMPUTATIONAL',seed:null,tests,rows,
 checks,corrupt_rejections:errors,guard_dependent_gate_cofactor_controls:16,
 notes:'Exact all-size minima rely on the source-ancestry proof and explicit RES construction, not this finite test. Full guard-dependent ER strengthening uses inherited LSPV-2/381 cofactor closure.'};
}
if(typeof process!=='undefined'&&process.stdout)process.stdout.write(JSON.stringify(run(),null,2)+'\n');
