function solveMatrix(obj){
 let cols=obj.owners.flat().map(s=>BigInt("0x"+s)),n=cols.length,d=obj.dimension,t=BigInt("0x"+obj.target),R=Array.from({length:d},(_,i)=>cols.reduce((s,c,j)=>s|(((c>>BigInt(i))&1n)<<BigInt(j)),((t>>BigInt(i))&1n)<<BigInt(n))),piv=[],xors=0;
 for(let j=0;j<n;j++){let i=R.findIndex((r,i)=>i>=piv.length&&((r>>BigInt(j))&1n));if(i<0)continue;let z=piv.length;[R[z],R[i]]=[R[i],R[z]];for(let k=0;k<d;k++)if(k!==z&&((R[k]>>BigInt(j))&1n)){R[k]^=R[z];xors++}piv.push(j)}
 let mask=(1n<<BigInt(n))-1n;if(R.some(r=>(r&mask)===0n&&(r>>BigInt(n))===1n))return{status:"UNSAT",linearInconsistent:true};
 const free=Array.from({length:n},(_,i)=>i).filter(i=>!piv.includes(i));if(free.length>20)return{status:"UNKNOWN",rank:piv.length,nullity:free.length};
 const parity=x=>{let b=0n;while(x){b^=1n;x&=x-1n}return b};let valid=0,wordChecks=0,violations=[];
 for(let k=0;k<2**free.length;k++){let y=free.reduce((s,j,i)=>s|((BigInt(k>>i&1))<<BigInt(j)),0n);for(let i=0;i<piv.length;i++){let v=((R[i]>>BigInt(n))&1n)^parity(R[i]&y&mask);y|=v<<BigInt(piv[i])}
 let t2=0n;for(let j=0;j<n;j++){wordChecks++;if(y>>BigInt(j)&1n)t2^=cols[j]}if(t2!==t)throw Error("linear lift");let bad=[];for(let j=0;j<n/2;j++)if(!(y>>BigInt(2*j)&3n))bad.push(j);if(!bad.length)valid++;else violations.push([k,bad[0]])}
 return{status:valid?"SAT":"UNSAT",rank:piv.length,nullity:free.length,candidates:2**free.length,valid,xors,wordChecks,violations}
}
