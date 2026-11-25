function pairHull(inputs){
 const bit=i=>1n<<BigInt(i),parity=x=>{let p=0;while(x){p^=1;x&=x-1n;}return p};
 let results=[];
 for(const j of inputs){
  const n=Math.max(...j.scopes.flat(),...j.guard.map(a=>a[0]))+1,basis=Array(n).fill(0n);let counts={pairWords:0,rankXors:0,localHulls:0,rowTests:0};
  const add=(B,row,k)=>{for(let p=k-1;p>=0;p--)if(row&bit(p)){if(B[p]){row^=B[p];counts.rankXors++;}else{B[p]=row;return true;}}return row===0n;};
  const masks=j.domainMasks.map(x=>BigInt("0x"+x)), words=j.rows.map((R,i)=>R.map(w=>j.scopes[i].reduce((a,v,k)=>a|(w[k]==="1"?bit(v):0n),0n)));
  function acquire(v,seq){
   const L=Array(n).fill(0n);let ref=null,rank=0;let support=v.reduce((a,z)=>a|bit(z),0n);
   for(const w of seq){counts.pairWords++;if(ref===null){ref=w;continue;}if(rank===v.length)break;let z=w^ref;for(let p=n-1;p>=0;p--)if(z&bit(p)){if(L[p]){z^=L[p];counts.rankXors++;}else{L[p]=z;rank++;break;}}}
   if(ref===null)throw Error("empty pair");counts.localHulls++;
   for(let f=0;f<n;f++)if((support&bit(f))&&!L[f]){let z=bit(f);for(let p=0;p<n;p++)if(L[p]&&parity(L[p]&z))z^=bit(p);if(!add(basis,z|(parity(z&ref)?bit(n):0n),n))throw Error("contradiction");}
  }
  for(const [i,k,R] of j.relations){const v=[...new Set([...j.scopes[i],...j.scopes[k]])];function* seq(){for(let a=0;a<words[i].length;a++)if(masks[i]&bit(a)){let s=BigInt("0x"+R[a])&masks[k];for(let b=0;b<words[k].length;b++)if(s&bit(b))yield words[i][a]|words[k][b];}}acquire(v,seq());}
  for(const [v,b] of j.guard)if(!add(basis,bit(v)|(b?bit(n):0n),n))throw Error("guard");
  let deletions=[],forced=[];for(let i=0;i<words.length;i++)for(let a=0;a<words[i].length;a++)if(masks[i]&bit(a)){counts.rowTests++;let B=basis.slice(),ok=true;for(const v of j.scopes[i])if(!add(B,bit(v)|(words[i][a]&bit(v)?bit(n):0n),n)){ok=false;break;}if(!ok)deletions.push([j.ownerIds[i],j.rows[i][a]]);}
  for(let i=0;i<n;i++){let a=add(basis.slice(),bit(i),n),b=add(basis.slice(),bit(i)|bit(n),n);if(!a||!b)forced.push([i,+!a]);}
  results.push({id:j.id,guard:j.guard,rank:basis.filter(Boolean).length,forced,deletions,counts});
 }return results;
}
const fs=require('fs'); console.log(JSON.stringify(pairHull(process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2));
