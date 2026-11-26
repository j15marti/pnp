/* P4SW03 full attainable affine hull audit. Requires sibling certificate_results.json. */
function hull(data){
 const groups=[[0,5,13,16,18,23,31,34],[1,4],[2,3],[6,11,24,29,36,41],[7,10],[8,9,12,17],[14,15],[19,22,38,39],[20,21],[25,28],[26,27,30,35],[32,33],[37,40,50,51],[42,47],[43,46],[44,45,48,53],[49,52]];
 const S=data.standard,core=data.core;let rows=Array.from({length:72},()=>[]);
 core.forEach((t,i)=>t.forEach((a,c)=>rows[18*c+a].push(i)));
 const id=Array(54).fill(-1);groups.forEach((g,j)=>g.forEach(i=>{if(id[i]!==-1)throw Error('overlap');id[i]=j}));if(id.some(i=>i<0))throw Error('partition');
 let covers=[],parity=0;
 for(let u=0;u<1<<17;u++){let z=0,w=0;for(let j=0;j<17;j++)if(u>>j&1){z^=S[j];w+=groups[j].length}if(z!==485)continue;parity++;if(w!==18)continue;if(!rows.every(r=>r.reduce((v,i)=>v+((u>>id[i])&1),0)===1))throw Error('false cover');covers.push(u)}
 let g0=covers.filter(u=>!(u&1));let B=new Map(),basisWords=[g0[0]];
 for(let u of g0.slice(1)){let x=u^g0[0];while(x){let k=31-Math.clz32(x);if(!B.has(k)){B.set(k,x);basisWords.push(u);break}x^=B.get(k)}}
 let g1=covers.find(u=>u&1);basisWords.push(g1);if(parity!==256||covers.length!==51||g0.length!==46||B.size!==7||!g1)throw Error('unexpected result');
 return {parity_words:parity,exact_covers:covers.length,hub0_covers:g0.length,hub1_covers:covers.length-g0.length,hub0_affine_rank:B.size,full_affine_rank:B.size+1,witness_words:basisWords,groups,weights:groups.map(g=>g.length),target:485};
}
const fs=require('node:fs');console.log(JSON.stringify(hull(JSON.parse(fs.readFileSync(__dirname+'/certificate_results.json','utf8'))),null,2));
