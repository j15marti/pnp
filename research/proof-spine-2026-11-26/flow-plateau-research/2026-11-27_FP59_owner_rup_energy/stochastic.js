function stochastic(F,V,seed=137){
 let work=0,restarts=[],best=null;const inc=new Map(V.map(v=>[v,F.filter(f=>f.vs.includes(v))]));let rng=seed>>>0;function rand(){rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return (rng>>>0)/4294967296}
 let cost=(f,A)=>{work+=f.vs.length+1;return f.cost[f.vs.reduce((s,v,j)=>s|(A.get(v)<<j),0)]};
 for(let k=0;k<8;k++){let A=new Map(V.map(v=>[v,Number(rand()>=.5)])),e=F.reduce((s,f)=>s+cost(f,A),0),initial=e,steps=0;
 for(;steps<64;steps++){let d=0,choices=[];for(let v of V){let prev=inc.get(v).reduce((s,f)=>s+cost(f,A),0);A.set(v,1-A.get(v));let q=inc.get(v).reduce((s,f)=>s+cost(f,A),0);A.set(v,1-A.get(v));if(q-prev<d){d=q-prev;choices=[v]}else if(q-prev===d&&d<0)choices.push(v)}if(!choices.length)break;let v=choices[Math.floor(rand()*choices.length)];A.set(v,1-A.get(v));e+=d}
 let q=F.reduce((s,f)=>s+cost(f,A),0);if(e!==q)throw Error("score drift");restarts.push({initial,e,steps});if(!best||e<best.best)best={best:e,assignment:[...A]}}
 return {best,restarts,work,seed};
}
if(typeof module!=="undefined")module.exports={stochastic};
