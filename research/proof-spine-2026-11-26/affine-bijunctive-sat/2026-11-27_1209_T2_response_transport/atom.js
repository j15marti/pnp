function atom(){
 const planes=[[15,32,47],[13,17,28],[14,36,42],[11,53,62],[10,39,45]],A=planes.flatMap(p=>p.slice(0,2)),pc=x=>{let z=0;while(x){z^=1;x&=x-1}return z},f=Array.from({length:64},()=>[]),L=planes.flatMap(([a,b],i)=>{let u=1<<(6+2*i),v=u<<1;return [[u,v^a,u^v^a],[v,u^b,u^v^b]]});
 for(let k=0;k<243;k++){let q=k,x=0,s=0;for(let i=0;i<5;i++){let j=q%3;q=Math.floor(q/3);x|=(j+1)<<(2*i);s^=planes[i][j]}f[s].push(x)}
 let lifted=Array.from({length:64},()=>[]);for(let k=0;k<59049;k++){let q=k,t=0,u=[];for(let i=0;i<10;i++){let j=q%3;q=Math.floor(q/3);t^=L[i][j];u.push(j+1)}if(t>=64)continue;let x=0;for(let i=0;i<5;i++){let a=u[2*i],b=u[2*i+1];if((a&1)!==(b>>1)||(b&1)!==(a>>1))throw Error("reciprocal");x|=((a>>1)+2*(b>>1))<<(2*i)}lifted[t].push(x)}
 if(JSON.stringify(f.map(a=>a.sort((a,b)=>a-b)))!==JSON.stringify(lifted.map(a=>a.sort((a,b)=>a-b))))throw Error("fiber");
 const rows=Array.from({length:64},(_,m)=>A.reduce((v,a,i)=>v|(pc(m&a)<<i),0)),reps=[...new Set(Array.from({length:1024},(_,m)=>Math.min(...rows.map(r=>m^r))))].sort((a,b)=>a-b);
 const aff=Array.from({length:128},(_,a)=>Array.from({length:64},(_,s)=>pc((a&63)&s)^(a>>6))), out=[];
 let comparisons=0;
 for(let m of reps){let forced=f.flatMap((w,s)=>w.length&&w.every(x=>pc(m&x)===pc(m&w[0]))?[[s,pc(m&w[0])]]:[]);let pat=v=>forced.reduce((p,[s],i)=>p+(v[s]<<i),0); // only use bitwise patterns for nontrivial classes (<=11 forced points)
 const exact=(a,b,c)=>forced.every(([s,y])=>(aff[a][s]^(aff[b][s]&aff[c][s]))===y);
 let linear=aff.map((v,i)=>i).filter(i=>forced.every(([s,y])=>aff[i][s]===y));
 if(linear.length){out.push({m,forced,linear,degree:linear.includes(0)||linear.includes(64)?0:1});continue}
 let D=new Map();for(let i=0;i<128;i++){let k=pat(aff[i]);if(!D.has(k))D.set(k,i)}
 let target=forced.reduce((p,[s,y],i)=>p+(y<<i),0),candidate=null,found=0;
 for(let b=0;b<128;b++)for(let c=b;c<128;c++){comparisons++;let t=forced.reduce((p,[s],i)=>p+((aff[b][s]&aff[c][s])<<i),0),a=D.get(target^t);if(a!==undefined){found++;if(!exact(a,b,c))throw Error("direct eval");if(!candidate)candidate=[a,b,c]}}
 out.push({m,forced,linear,degree:candidate?2:null,oneProduct:candidate,productPairs:found})
 }
 return{planes,classes:out,comparisons,missing:f.flatMap((a,i)=>a.length?[]:[i]),liftedAssignments:59049,liftedWitnesses:lifted.flat().length}
}
console.log(JSON.stringify(atom(),null,2));
