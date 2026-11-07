'use strict';
// LSPV-3/470 compact independently reproducible cubic-Tseitin cut firewall.
// Run: node experiments/arc/lspv3_470_cut_parity_compact.cjs
// This is a DECLARED-SEMANTIC check, not the historical R_mix341 byte checker.
function graphs(){
 const K4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K4.push([i,j]);
 const K33=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)K33.push([i,j]);
 const cube=[];for(let v=0;v<8;v++)for(let bit=0;bit<3;bit++){let w=v^(1<<bit);if(v<w)cube.push([v,w]);}
 const prism=[];for(let i=0;i<6;i++){for(const [a,b] of [[i,(i+1)%6],[i+6,(i+1)%6+6],[i,i+6]])prism.push([Math.min(a,b),Math.max(a,b)]);}
 prism.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 return [['K4',4,K4],['K33',6,K33],['cube',8,cube],['prism6',12,prism]];
}
function pc(x){let q=0;for(;x;x&=x-1)q++;return q}
function check(name,h,edges){
 const m=edges.length;if(m*2!==3*h)throw Error('not cubic');
 const inc=Array.from({length:h},()=>[]);
 edges.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i)});
 if(inc.some(t=>t.length!==3))throw Error('not 3 regular');
 const chi=Array(h).fill(0);chi[0]=1;
 const side=Array(h).fill(0);let flips=0;
 for(;;){let chosen=-1;for(let v=0;v<h;v++){
   let cross=inc[v].filter(e=>side[edges[e][0]]!==side[edges[e][1]]).length;
   if(cross<=1){chosen=v;break;}
 }if(chosen<0)break;side[chosen]^=1;if(++flips>m)throw Error('cut potential failed');}
 const cut=edges.map(([a,b],i)=>side[a]!==side[b]?i: -1).filter(i=>i>=0);
 if(cut.length<h)throw Error('degree-3 maximal cut bound failed');
 let localSourceCount=0;
 for(let v=0;v<h;v++){
   let allowed=255,forbiddenCount=0;
   for(let a=0;a<8;a++)if((pc(a)&1)!==chi[v]){allowed&=~(1<<a);forbiddenCount++;}
   for(let a=0;a<8;a++)if(Boolean((allowed>>a)&1)!==((pc(a)&1)===chi[v]))throw Error('AND3/local GF2 mismatch');
   if(forbiddenCount!==4)throw Error('source clauses');
   localSourceCount+=forbiddenCount;
 }
 let odd=0,even=0;
 for(let a=0;a<(1<<m);a++){
   let mismatch=0;
   for(let v=0;v<h;v++){let p=0;for(const e of inc[v])p^=(a>>e)&1;if(p!==chi[v])mismatch++;}
   if(mismatch===0)odd++;
   mismatch=0;for(let v=0;v<h;v++){let p=0;for(const e of inc[v])p^=(a>>e)&1;if(p) mismatch++;}
   if(mismatch===0)even++;
 }
 if(odd!==0||even!==(1<<(m-h+1)))throw Error('SAT/UNSAT control');
 const bits=cut.length,rhs=side.indexOf(0)===0?1:0;
 let implicates=null,ternaryTested=0;
 if(bits<=9){let count=0;for(let t=1;t<3**bits;t++){
   let temp=t,pos=0,neg=0;
   for(let j=0;j<bits;j++){let d=temp%3;temp=Math.floor(temp/3);if(d===1)pos|=1<<j;if(d===2)neg|=1<<j;}
   let valid=true;
   for(let a=0;a<(1<<bits);a++){if((pc(a)&1)!==rhs)continue;
     if((a&pos)===0&&((~a)&neg)===0){valid=false;break;}
   }
   if(valid){if((pos|neg)!==(1<<bits)-1)throw Error('short parity implicate');count++;}
   ternaryTested++;
 }if(count!==2**(bits-1))throw Error('parity CNF minimum');
 implicates=count;}
 return {graph:name,h,variables:m,source_clauses:localSourceCount,cut_width:bits,declared_paid_nodes:4*h-1,flat_CNF_min_clauses:2**(bits-1),odd_SAT_models:odd,even_SAT_models:even,ternaryTested,implicates};
}
function run(){return graphs().map(([name,h,edges])=>check(name,h,edges));}
if(typeof require!=='undefined' && typeof process!=='undefined' && require.main===module)console.log(JSON.stringify(run(),null,2));
