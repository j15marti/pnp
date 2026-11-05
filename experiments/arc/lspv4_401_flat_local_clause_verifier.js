'use strict';
function local(k,mask,C){
 for(const x of C)if(!Number.isInteger(x)||x===0||Math.abs(x)>5)throw Error('bad literal');
 const s=new Set(C);if(C.some(x=>s.has(-x)))return true;
 const t=C.filter(x=>Math.abs(x)<=k);
 for(let a=0;a<(1<<k);a++)if(mask&(1<<a)){
  let ok=false;for(const x of t)if(((a>>(Math.abs(x)-1))&1)===(x>0?1:0)){ok=true;break;}
  if(!ok)return false;
 }return true;
}
function ground(k,mask,C){
 for(let a=0;a<32;a++)if(mask&(1<<(a&((1<<k)-1)))){
  if(!C.some(x=>((a>>(Math.abs(x)-1))&1)===(x>0?1:0)))return false;
 }return true;
}
function run(){
 const r={project:'LSPV4_401_flat_LOCAL',cases:0,entailed:0,not_entailed:0,tautology:0,malformed:0};
 for(let k=0;k<=3;k++)for(let mask=0;mask<(1<<(1<<k));mask++){
  for(let v=0;v<243;v++){let q=v,C=[];for(let i=1;i<=5;i++){let d=q%3;q=Math.floor(q/3);if(d)C.push(d===1?i:-i);}
   const b=local(k,mask,C);if(b!==ground(k,mask,C))throw Error('failed');
   r.cases++;if(b)r.entailed++;else r.not_entailed++;
  }
  for(let j=1;j<=5;j++){let C=[j,-j,(j%5)+1];if(!local(k,mask,C)||!ground(k,mask,C))throw Error('taut');r.tautology++;}
 }
 if(r.cases!==67554||r.entailed!==18972||r.not_entailed!==48582||r.tautology!==1390)throw Error('counts');
 for(const C of [[0],[1,0],[0,-1]])try{local(2,10,C);throw Error('accepted');}catch(e){if(e.message==='accepted')throw e;r.malformed++;}
 if(!local(2,10,[1,3])||local(2,10,[-1,3])||!local(2,10,[3,-3])||local(2,10,[]))throw Error('signed');
 function count(F,n){let z=0;for(let a=0;a<(1<<n);a++)if(F.every(C=>C.some(x=>((a>>(Math.abs(x)-1))&1)===(x>0?1:0))))z++;return z;}
 if(count([[1],[1,3],[-2]],3)!==2||count([[1],[-1]],1)!==0)throw Error('source');
 return r;
}
if(typeof module!=='undefined'&&typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
