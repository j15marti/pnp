function certify(){
 const planes=[[15,32,47],[13,17,28],[14,36,42],[11,53,62],[10,39,45]],p=x=>{let q=0;for(;x;x>>>=1)q^=x&1;return q},f=Array.from({length:64},()=>[]);
 for(let x=0;x<1024;x++){let s=0,ok=true;for(let i=0;i<5;i++){let q=(x>>(2*i))&3;if(!q){ok=false;break}s^=planes[i][q-1]}if(ok)f[s].push(x)}
 const F=[];for(let m=1;m<16;m++)for(let s=0;s<64;s++){let a=f[s];if(a.length&&a.every(x=>p(m&x)===p(m&a[0])))F.push([m,s,p(m&a[0])])}
 const row=(m,s)=>{let z=0;for(let j=0;j<4;j++)if(m>>j&1)z^=(s+64)<<(7*j);return z};
 let certificates=[],xorOps=0;
 for(let g=1;g<64;g++){let found=null;for(let b=0;b<2&&!found;b++){let basis=Array(28).fill(null);for(let i=0;i<F.length;i++){let [m,s,y]=F[i];if(p(g&s)!==b)continue;let v=row(m,s),z=y,T=new Set([i]);for(let j=27;j>=0;j--)if(v>>j&1){if(!basis[j]){basis[j]=[v,z,T];break}let [u,w,S]=basis[j];v^=u;z^=w;xorOps++;for(let a of S){if(T.has(a))T.delete(a);else T.add(a)}}if(v===0&&z===1){found={g,b,rows:[...T].map(i=>F[i]).sort((x,y)=>x[0]-y[0]||x[1]-y[1])};break}}}if(!found)throw Error("selector survives");certificates.push(found)}
 // Independent checker: direct enumeration of each listed target and response over original legal words, then coefficient-wise parity.
 for(let c of certificates){let z=0,v=Array(28).fill(0);for(let [m,s,y] of c.rows){if(p(c.g&s)!==c.b||!f[s].length||!f[s].every(x=>p(m&x)===y))throw Error("bad forced row");z^=y;for(let j=0;j<4;j++)if(m>>j&1){for(let k=0;k<6;k++)v[7*j+k]^=s>>k&1;v[7*j+6]^=1}}if(z!==1||v.some(Boolean))throw Error("bad certificate")}
 return{planes,certificates,xorOps,forcedRows:F.length,checkedWords:f.flat().length};
}
console.log(JSON.stringify(certify(),null,2));
