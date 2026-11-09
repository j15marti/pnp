'use strict';
// LSPV-1/519 finite verifier. No R_mix341 native checker is executed.
let checks=0;
const ok=(c,m)=>{checks++;if(!c)throw Error(m)};
const mod=x=>((x%3)+3)%3,cs=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
function build(name,odd){
 let h=name==='K4'?4:name==='K33'?6:8,E=[];
 if(name==='K4')for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E.push([i,j]);
 if(name==='K33')for(let i=0;i<3;i++)for(let j=3;j<6;j++)E.push([i,j]);
 if(name==='Q3')for(let i=0;i<8;i++)for(let k=0;k<3;k++){let j=i^(1<<k);if(i<j)E.push([i,j])}
 let inc=Array.from({length:h},()=>[]);E.forEach(([u,v],e)=>{inc[u].push([e,1]);inc[v].push([e,-1])});
 ok(inc.every(x=>x.length===3),'cubic');let b=Array(h).fill(0);if(odd)b[0]=1;
 let old=[];for(let e=0;e<E.length;e++){let a=[3*e+1,3*e+2,3*e+3];old.push(a);
 for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)old.push(cs([-a[i],-a[j]]))}
 for(let v=0;v<h;v++)for(let a=0;a<3;a++)for(let d=0;d<3;d++)for(let f=0;f<3;f++){
 let t=[a,d,f];if(mod(t.reduce((s,x,i)=>s+inc[v][i][1]*x,0))!==b[v])
 old.push(cs(t.map((x,i)=>-3*inc[v][i][0]-x-1)))}
 const z=3*E.length+1;let strict=[],pairs=0;
 for(let C of old)if(C.length===2){let A=cs([...C,z]),B=cs([...C,-z]);strict.push(A,B);
  ok(JSON.stringify(cs([...A.filter(x=>x!==z),...B.filter(x=>x!==-z)]))===JSON.stringify(C),'RES pivot');pairs++}
 else strict.push(C);
 ok(old.length===24*h&&strict.length===57*h/2&&pairs===9*h/2,'counts');
 ok(strict.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'proper');
 const sat=(clauses,bits)=>clauses.every(C=>C.some(x=>x>0?bits[x-1]:!bits[-x-1]));
 for(let seed=0;seed<90;seed++){let a=E.map((_,i)=>mod(seed*7+i*11+(seed>>(i%4))));
 let expected=inc.every((row,v)=>mod(row.reduce((s,[e,sg])=>s+sg*a[e],0))===b[v]);
 for(let Z of [0,1]){let bits=Array(z).fill(false);a.forEach((x,e)=>bits[3*e+x]=true);bits[z-1]=Boolean(Z);
 ok(sat(old,bits)===expected&&sat(strict,bits)===expected,'padding truth')}
 ok(mod(inc.flat().reduce((s,[e,sg])=>s+sg*a[e],0))===0,'flow cancellation')}
 let arr=inc.flat().map(x=>x.join(',')),end=E.flatMap((_,e)=>[[e,1].join(','),[e,-1].join(',')]),swaps=0;
 for(let i=0;i<end.length;i++){let j=arr.indexOf(end[i],i);ok(j>=i,'term');
 while(j>i){let t=arr[j];arr[j]=arr[j-1];arr[j-1]=t;j--;swaps++}}
 ok(JSON.stringify(arr)===JSON.stringify(end)&&swaps<=3*h*(3*h-1)/2,'reorder');
 return {name,charge:odd?'nonzero':'zero',vertices:h,edges:E.length,old_clauses:old.length,strict_clauses:strict.length,paid_depadding_RES:pairs,swaps}
}
for(let a=0;a<3;a++)for(let b=0;b<3;b++){let X=[0,1,2].map(i=>+(i===a)),Y=[0,1,2].map(i=>+(i===b));
 let Z=[0,1,2].map(r=>+(X.some((x,i)=>x&&Y.some((y,j)=>y&&mod(i+j)===r))));
 ok(Z.reduce((s,t)=>s+t,0)===1&&Z[mod(a+b)]===1,'adder')}
for(let p=0;p<3;p++)for(let a=0;a<3;a++)for(let b=0;b<3;b++)
 ok(mod(mod(p+a)+b)===mod(mod(p+b)+a),'swap identity');
for(let p=0;p<3;p++)for(let a=0;a<3;a++)ok(mod(mod(p+a)-a)===p,'cancel');
const cases=['K4','K33','Q3'].flatMap(g=>[false,true].map(odd=>build(g,odd)));
let result={id:'LSPV-1/519',status:'COMPUTATIONAL',checks,cases,
 native_checker_executed:false,limitation:'No complete historical ER2 certificate verified'};
if(require.main===module)process.stdout.write(JSON.stringify(result,null,2)+'\n');
module.exports=result;
