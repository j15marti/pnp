function affineAudit(inputs){
 const bit=i=>1n<<BigInt(i),parity=x=>{let p=0;while(x){p^=1;x&=x-1n;}return p};
 let out=[];
 for(const j of inputs){
 let n=Math.max(...j.scopes.flat(),...j.guard.map(a=>a[0]))+1,counts={xor:0,rowTests:0},basis=Array(n).fill(0n);
 function add(B,row,k){for(let i=k-1;i>=0;i--)if(row&bit(i)){if(B[i]){row^=B[i];counts.xor++;}else{B[i]=row;return true;}}return row===0n;}
 const local=j.rows.map((R,i)=>R.filter((a,k)=>!!(BigInt("0x"+j.domainMasks[i])&bit(k))));
 for(let i=0;i<local.length;i++){
  let rows=local[i],v=j.scopes[i],k=v.length,encode=w=>[...w].reduce((a,b,l)=>a+(b==="1"?bit(l):0n),0n),ref=encode(rows[0]),L=Array(k).fill(0n);
  for(const w of rows)add(L,encode(w)^ref,k);
  for(let f=0;f<k;f++)if(!L[f]){
   let z=bit(f);for(let p=0;p<k;p++)if(L[p]&&parity(L[p]&z))z^=bit(p);
   let g=v.reduce((a,x,l)=>a+((z&bit(l))?bit(x):0n),0n);if(parity(z&ref))g|=bit(n);if(!add(basis,g,n))throw Error("inconsistent actual chart");
  }
 }
 for(const [v,b] of j.guard)if(!add(basis,bit(v)|(b?bit(n):0n),n))throw Error("inconsistent guard");
 let deletions=[],forced=[];
 for(let i=0;i<local.length;i++)for(const w of local[i]){
  counts.rowTests++;let B=basis.slice(),ok=true;for(let k=0;k<w.length;k++)if(!add(B,bit(j.scopes[i][k])|(w[k]==="1"?bit(n):0n),n)){ok=false;break;}if(!ok)deletions.push([j.ownerIds[i],w]);
 }
 for(let i=0;i<n;i++){let a=add(basis.slice(),bit(i),n),b=add(basis.slice(),bit(i)|bit(n),n);if(!a||!b)forced.push([i,+!a]);}
 out.push({id:j.id,guard:j.guard,rank:basis.filter(Boolean).length,forced,deletions,counts});
 }
 return out;
}
const fs=require('fs'); console.log(JSON.stringify(affineAudit(process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2));
