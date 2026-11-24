function nonaffineScale(){
const out=[];for(const r of [8,16,32,64,128,256]){
 const thick=Array.from({length:r+1},(_,i)=>[0,1,8,i===0?0n:1n<<BigInt(i-1)]);
 const thin=[[0,2,1,0n],[0,2,1,1n<<BigInt(r)],[1,2,1,1n<<BigInt(r+1)]];
 const A=thick.concat(thin), b=[-4*(r+1)-1,4*(r+1),1], ok=(x,t)=>{let a=[0,0,0],g=0n;A.forEach(([u,v,c,l],i)=>{if(x[i]<0||x[i]>c)throw Error("capacity");a[u]-=x[i];a[v]+=x[i];if(x[i]%2)g^=l});if(!a.every((v,i)=>v===b[i])||g!==t)throw Error("lift")};
 let sat=0,unsat=0,quotient=new Set();for(let mask=0;mask<8;mask++){let y=[mask&1,(mask>>1)&1,(mask>>2)&1];if(y.reduce((a,z)=>a+z,0)===1)quotient.add(y[1]+2*y[2])}
 for(let q=0;q<4;q++)for(const w of [0n,(1n<<BigInt(r))-1n,0x5555n&((1n<<BigInt(r))-1n)]){
 if(!quotient.has(q)){if(q!==3)throw Error("unexpected rejection");unsat++;continue}
 let y=[q===0?1:0,q===1?1:0,q===2?1:0],x=thick.map((_,i)=>i===0?4+y[2]:4),d=0;
 for(let i=1;i<=r;i++)if((w>>BigInt(i-1))&1n){let s=d===0?1:-1;x[i]+=s;d+=s}x[0]-=d;
 ok(x.concat(y),w^(BigInt(q)<<BigInt(r)));sat++;
 }
 out.push({r,arcs:A.length,originalCycleRank:r+2,quotientCycleRank:2,tagHullRank:r+2,treeFlowRange:[4,5],sat,unsat})
}return out
}
console.log(JSON.stringify(nonaffineScale(),null,2));
