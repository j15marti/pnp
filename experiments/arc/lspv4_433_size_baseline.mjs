#!/usr/bin/env node
// LSPV-4/433 independent exact-bit and size-normalization verifier.
// No claim of native FLMV-machine timing or P-versus-NP separation.
let checks=0;
function ok(value,why){checks++;if(!value)throw Error(why)}
function graph(name){
  if(name==="K4"){let E=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)E.push([u,v]);return [4,E]}
  if(name==="Cube"){let E=[];for(let u=0;u<8;u++)for(let b=0;b<3;b++){let v=u^(1<<b);if(u<v)E.push([u,v])}return [8,E]}
  if(name==="Petersen"){let E=[];for(let i=0;i<5;i++) E.push([i,(i+1)%5],[i,i+5],[i+5,(i+2)%5+5]);return [10,E.map(([a,b])=>a<b?[a,b]:[b,a])]}
  throw Error("unsupported");
}
function encode(name,charge){
 let [H,edges]=graph(name); edges.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 let M=edges.length,w=Math.floor(Math.log2(M))+1;
 let pad=x=>x.toString(2).padStart(w,"0");
 let bits="10100111"+"1".repeat(H)+"0"+"1".repeat(M)+"0";
 for(const [a,b] of edges)bits+=pad(a)+pad(b);
 for(let v=0;v<H;v++){
   let ids=edges.flatMap((e,i)=>e.includes(v)?[i+1]:[]).sort((a,b)=>a-b);
   ok(ids.length===3,"cubic");
   for(let p=0;p<2;p++)for(let r=0;r<2;r++)
     bits+=p+pad(ids[0])+r+pad(ids[1])+(p^r^1^charge[v])+pad(ids[2]);
 }
 bits+="00";
 ok(bits.length===8+(H+1)+(M+1)+2*M*w+12*H*(w+1)+2,"encoded bit length");
 return bits;
}
let records=[];
for(const name of ["K4","Cube","Petersen"]){
 let [H,edges]=graph(name),n=encode(name,Array(H).fill(0)).length;
 let set=new Set;
 for(let mask=0;mask<2**H;mask++){
   let charge=Array.from({length:H},(_,i)=>(mask>>i)&1),bits=encode(name,charge);
   ok(!set.has(bits),"independent charge encoding injection");set.add(bits);
   ok(charge.reduce((s,x)=>s^x,0)===(charge.reduce((s,x)=>s+x,0)%2),"parity");
 }
 ok(set.size===2**H,"all distinct charges");
 let even=encode(name,Array(H).fill(0)),odd=encode(name,[1,...Array(H-1).fill(0)]);
 let changes=0;for(let i=0;i<n;i++)if(even[i]!==odd[i])changes++;
 ok(changes===4,"exact four pivotal sign bits");
 let q=name==="K4"?3:5;
 let B=q*n,reads=q*H;
 ok(reads<=B,"cannot read more distinct positions than tuple holds");
 records.push({name,H,n,q,B,reads});
}
for(let k of [20,40,60,80,100,120,160,200,240,300]){
 let P=1n<<BigInt(k),q=1n<<BigInt(Math.floor(3*k/5));
 let L=1n<<BigInt(Math.floor(k/2)),H=L/BigInt(12*Math.floor(k/2));
 ok(q*H<=q*L,"raw read lb bounded by raw length");
 if(k>=100)ok(q*H>P,"exact independent charges exceed possible parent length");
}
for(let H=1;H<=5;H++)for(let q=1;q<=3;q++){
 let independent=1n<<BigInt(H*q),P=H*q-1;
 ok(independent>((1n<<BigInt(P+1))-1n),"length <=P cannot encode all independent charges");
}
ok((23*2-45)===1,"FLMV 1/90 gap arithmetic");
const answer={checks,records,status:"finite exact-bit controls only; restricted analytic normalization"};
process.stdout.write(JSON.stringify(answer,null,2)+"\n");