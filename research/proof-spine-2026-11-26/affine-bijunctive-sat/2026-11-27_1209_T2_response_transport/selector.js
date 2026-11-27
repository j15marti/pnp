function jointAudit(a){
 const pc=x=>{let z=0;while(x){x&=x-1;z^=1}return z};
 function solve(eq,n){let B=new Map(),r=1n<<BigInt(n),lo=r-1n;for(let [m,b] of eq){let w=BigInt(m)|(b?r:0n);while(w&lo){let p=(w&-w).toString(2).length-1;if(B.has(p))w^=B.get(p);else{B.set(p,w);break}}if(w===r)return{consistent:false,rank:B.size}}
 let v=0n;for(let [p,w] of [...B].sort((a,b)=>b[0]-a[0])){let t=(w&v),z=0;while(t){t&=t-1n;z^=1}if(z!==Number(Boolean(w&r)))v|=1n<<BigInt(p)}return{consistent:true,rank:B.size,solution:v.toString()}}
 const selector=[];for(let g=1;g<64;g++){
 let independent=a.classes.every(c=>[0,1].every(b=>solve(c.forced.filter(([s])=>pc(g&s)===b).map(([s,y])=>[64+s,y]),7).consistent));
 let joint=[0,1].map(b=>{let eq=[];for(let c of a.classes)for(let [s,y] of c.forced)if(pc(g&s)===b){let row=0;for(let i=0;i<4;i++)if(c.m>>i&1)row^=(64+s)<<(7*i);eq.push([row,y])}return solve(eq,28)});
 if(independent)selector.push({g,joint});
 }
 let P=a.planes,f=Array.from({length:64},()=>new Set());for(let k=0;k<243;k++){let q=k,s=0,x=0;for(let i=0;i<5;i++){let j=q%3;q=Math.floor(q/3);s^=P[i][j];x|=(j+1)<<(2*i)}f[s].add(x&15)}
 let attempts=[];for(let {g,joint} of selector){if(!joint.every(x=>x.consistent))continue;let misses=[];for(let s=0;s<64;s++)if(f[s].size){let v=Number(joint[pc(g&s)].solution),z=0;for(let i=0;i<4;i++)z|=pc(((v>>>(7*i))&127)&(s+64))<<i;if(!f[s].has(z))misses.push([s,z,[...f[s]]])}attempts.push({g,misses})}
 return{selector,attempts};
}
const fs=require('node:fs');console.log(JSON.stringify(jointAudit(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
