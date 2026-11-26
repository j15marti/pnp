function audit(){
 let seed=26112606, checks=0, cases=0;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};const ok=x=>{checks++;if(!x)throw Error("check "+checks)};
 const A=[0,3,6,9,12,15],bit=(w,p)=>(w>>[3,2,1,0][p])&1;
 // Relation along a row/column; split at crossing edges, count attainable seam words once.
 function count(k,S,D,d){
 let total=1n;for(let l=0;l<k;l++){
 let weights=[1n,0n],R=[[true,false],[false,true]];
 for(let j=0;j<k;j++){
 let i=d===0?l*k+j:j*k+l,local=[[false,false],[false,false]];for(let w of D[i])local[bit(w,d===0?3:0)][bit(w,d===0?1:2)]=true;
 R=R.map(row=>[0,1].map(b=>[0,1].some(a=>row[a]&&local[a][b])));
 let next=d===0?i+1:i+k;
 if(j===k-1||S[i]!==S[next]){
 weights=[0,1].map(b=>weights.reduce((v,w,a)=>v+(R[a][b]?w:0n),0n));
 R=[[true,false],[false,true]];
 }
 }
 total*=weights[0]
 }
 return total
 }
 function brute(k,S,D,d){
 let total=1n;for(let l=0;l<k;l++){let sig=new Set;for(let x=0;x<1<<(k-1);x++){let bits=[0,...Array.from({length:k-1},(_,j)=>(x>>j)&1),0],good=true,key="";for(let j=0;j<k;j++){let i=d===0?l*k+j:j*k+l;good=good&&D[i].some(w=>bit(w,d===0?3:0)===bits[j]&&bit(w,d===0?1:2)===bits[j+1]);if(j<k-1&&S[i]!==S[d===0?i+1:i+k])key+=bits[j+1]}if(good)sig.add(key)}total*=BigInt(sig.size)}return total
 }
 let rows=[];
 for(let k of [2,3,4,6,8,16,64,128]){
 let maxExponent=0;for(let t=0;t<30;t++){let S=Array.from({length:k*k},()=>rnd()<.5),D=Array.from({length:k*k},()=>t%2===0?A:A.filter(()=>rnd()<.65));for(let d of [0,1]){
 let r=count(k,S,D,d);if(k<=8){ok(r===brute(k,S,D,d));cases++}
 if(t%2===0){let q=0;for(let i=0;i<k*k;i++)if((d===0?i%k<k-1:i<k*(k-1))&&S[i]!==S[d===0?i+1:i+k])q++;ok(r===(1n<<BigInt(q)));maxExponent=Math.max(maxExponent,q)}
 }}rows.push({k,maxExponent})
 }
 return {checks,bruteComparisons:cases,rows,seed:26112606};
}
console.log(JSON.stringify(audit(),null,2));
