function audit(){
 const P=[[15n,32n],[13n,17n],[14n,36n],[11n,53n],[10n,39n]], words=[];let checks=0;const req=x=>{checks++;if(!x)throw Error("audit")};
 function rec(a){if(a.length===5){words.push(a);return}for(let z=1;z<4;z++)rec([...a,z])}rec([]);
 const sum=(p,a)=>p.reduce((s,[u,v],i)=>s^((a[i]&1)?u:0n)^((a[i]&2)?v:0n),0n);
 const hist=Array(64).fill(0);for(const a of words)hist[Number(sum(P,a))]++;
 let dp=Array(64).fill(0);dp[0]=1;for(const [u,v] of P){dp=dp.map((_,i)=>[u,v,u^v].reduce((s,j)=>s+dp[i^Number(j)],0))}req(JSON.stringify(dp)===JSON.stringify(hist));req(hist[29]===0&&hist.filter(x=>x===0).length===1);
 const mask=a=>a.reduce((s,z,i)=>s|(z<<(2*i)),0);let fiber=words.filter(a=>sum(P,a)===0n).map(mask);let diffs=new Set(fiber.flatMap(x=>fiber.map(y=>x^y)));req(diffs.size===16);
 let p=P,d=6,aa=words,levels=[];const swap=z=>((z&1)<<1)|((z&2)>>1);for(let l=0;l<=5;l++){
  let bits=2*p.length*d+d;for(let i=0;i<words.length;i++){req(sum(p,aa[i])===sum(P,words[i]));req(aa[i].every(z=>z>0));}
  let rowMasks=[];for(let j=0;j<2*p.length;j++){let s=0;for(let i=0;i<10;i++){let b=Array(5).fill(0);b[i>>1]=1<<(i&1);for(let k=0;k<l;k++)b=b.flatMap(z=>[swap(z),z]);if((b[j>>1]>>(j&1))&1)s|=1<<i;}rowMasks.push(s);}
  const parity=x=>{let y=0;while(x){y^=1;x&=x-1}return y};
  for(let i=0;i<words.length;i++){let z=mask(words[i]);for(let j=0;j<rowMasks.length;j++)req(parity(z&rowMasks[j])===((aa[i][j>>1]>>(j&1))&1));}
  // All single coordinate pins plus one cross-owner equality checked against root guard pullback.
  let guardTests=0;for(let j=0;j<rowMasks.length;j++){for(let b=0;b<2;b++){let actual=0,pulled=0;for(let i=0;i<words.length;i++){if(((aa[i][j>>1]>>(j&1))&1)===b)actual++;if(parity(mask(words[i])&rowMasks[j])===b)pulled++;}req(actual===pulled);guardTests++;}}
  levels.push({level:l,owners:p.length,dimension:d,payloadBits:bits,rootWords:words.length,coordinateGuardTests:guardTests,distinctPulledCoordinateRows:new Set(rowMasks).size});
  if(l===5)break;let next=[];for(let i=0;i<p.length;i++){let [u,v]=p[i],a=1n<<BigInt(d+2*i),b=a<<1n;next.push([a,b^u],[b,a^v]);}d+=2*p.length;p=next;aa=aa.map(a=>a.flatMap(z=>[swap(z),z]));
 }
 function encode(L,R){let r=L.length,n0=3*r-2,y=n0+1,u=y+1,v=u+1,n=8*r-1,w=n.toString(2).length;let p=2*r+1,src=[];for(let i=0;i<r;i++)src.push([-i-1,r+L[i],p],[-i-1,r+L[i],-p]);let t=Array.from({length:r-3},(_,i)=>2*r+2+i);if(r===3)src.push([1,2,3]);else{src.push([1,2,t[0]]);for(let j=0;j<r-4;j++)src.push([-t[j],j+3,t[j+1]]);src.push([-t.at(-1),r-1,r]);}for(let i=0;i<r;i++)src.push([-i-1,-r-R[i],p],[-i-1,-r-R[i],-p]);let clauses=[[y,u,v],[y,u,-v],[y,-u,v],[y,-u,-v]];src.forEach(([a,b,c],j)=>clauses.push([-y,a,v+1+j],[-v-1-j,b,c]));const bin=x=>x.toString(2).padStart(w,"0"),g=(clauses.length+1).toString(2);return "1".repeat(n)+"0"+"0".repeat(g.length-1)+g+clauses.flat().map(x=>(x<0?"1":"0")+bin(Math.abs(x))).join("")+Array.from({length:2*n},(_,i)=>i%n+1===u||(i>=n&&i%n+1===v)?"1":"0").join("")+bin(y);}
 function decode(s){let n=s.indexOf("0"),r=(n+1)/8;if(!Number.isInteger(r)||r<3)return null;let k=n+1,z=0;while(s[k]==="0"){z++;k++;}let m=parseInt(s.slice(k,k+z+1),2)-1;k+=z+1;let w=n.toString(2).length;if(m!==10*r)return null;const lit=(c,j)=>{let i=k+(3*c+j)*(w+1);return (s[i]==="1"?-1:1)*parseInt(s.slice(i+1,i+w+1),2)};let L=[],R=[];for(let i=0;i<r;i++){L.push(lit(5+4*i,1)-r);R.push(-lit(6*r+1+4*i,1)-r);}if([...L,...R].some(x=>!Number.isInteger(x)||x<1||x>r)||encode(L,R)!==s)return null;return {L,R,eq:L.every((x,i)=>x===R[i])};}
 function perms(a){return a.length===0?[[]]:a.flatMap((v,i)=>perms(a.filter((_,j)=>j!==i)).map(z=>[v,...z]));}
 let transport=[];for(let r of [3,4]){let ps=perms(Array.from({length:r},(_,i)=>i+1)),no=0,yes=0;for(const L of ps)for(const R of ps){let s=encode(L,R),q=decode(s);req(q!==null);req(q.eq===(L.join()===R.join()));req(s.length===3*(8*r-1)+2+2*Math.floor(Math.log2(10*r+1))+30*r*((8*r-1).toString(2).length+1)+(8*r-1).toString(2).length);if(q.eq)no++;else yes++;}transport.push({r,no,yes,bits:encode(ps[0],ps[0]).length});}
 for(let r of [8,32,128,512]){let L=Array.from({length:r},(_,i)=>i+1),s=encode(L,L);req(decode(s)?.eq);let bad=s.slice(0,-1)+(s.at(-1)==="1"?"0":"1");req(decode(bad)===null);transport.push({r,no:1,yes:0,bits:s.length});}
 return {checks,hist,fiber,levels,transport};
}
console.log(JSON.stringify(audit(),null,2));
