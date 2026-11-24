// RT07B: stronger saturation-aware projected support
function run(){
let seed=0xc0da7;const rnd=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;},bit=i=>1n<<BigInt(i),assert=(b,m)=>{if(!b)throw Error(m);};
function tag(n,x,y){return bit(x)^bit(n+(x+y)%n);}
function parity(a){let b=0;while(a){a&=a-1n;b^=1;}return b;}
function add(B,v,w=0n){while(v){let j=v.toString(2).length-1;if(B[j]){v^=B[j][0];w^=B[j][1];}else{B[j]=[v,w];return true;}}return false;}
function solve(B,v){let w=0n;while(v){let j=v.toString(2).length-1;assert(B[j],"not spanned");v^=B[j][0];w^=B[j][1];}return w;}
function rank(a){let B=[];for(let v of a)add(B,v);return B.filter(Boolean).length;}
function randmask(d){let v=0n;for(let j=0;j<d;j+=32)v|=BigInt(rnd())<<BigInt(j);return v&(bit(d)-1n);}
function project(v,m){let p=0n;for(let i=0;i<m.length;i++)if(parity(v&m[i]))p|=bit(i);return p;}
let pairRanks=0,projectedWitnesses=0,guardedWitnesses=0,exactOwnerSelections=0,exactMaps=0;
let scaling=[];
for(let n of [4,8,12,16,32,64]){
let target=bit(2*n)-1n,base=0n;for(let y=0;y<n;y++)base^=tag(n,0,y);
let D=[];for(let y of [0,1])for(let x=0;x<n;x++)D.push(tag(n,x,y)^tag(n,0,y));
assert(rank(D)===2*n-3,"D rank");assert(rank([...D,target^base])===2*n-3,"target in hull");
for(let y=0;y<n;y+=2){let v=[];for(let j of [y,y+1])for(let x=0;x<n;x++)v.push(tag(n,x,j)^tag(n,0,j));assert(rank(v)===2*n-3&&rank([...D,...v])===2*n-3,"pair equals D");pairRanks++;}
for(let p of [...new Set([0,1,Math.floor(n/4),n/2-1])])for(let trial=0;trial<4;trial++){
let k=n/2-p,m=Array.from({length:k},()=>randmask(2*n)),r=rank(D.map(v=>project(v,m)));
let touched=new Set(),pins=[],choice=Array(n).fill(0);
while(pins.length<p){let y=rnd()%n;if(touched.has(y))continue;touched.add(y);let x=rnd()%n,v=rnd()%2;pins.push([x,y,v]);choice[y]=v?x:(x===0?1:0);}
let base=0n;for(let y=0;y<n;y++)base^=tag(n,choice[y],y);
let B=[],moves=[];for(let y=0;y<n&&moves.length<r;y+=2){if(touched.has(y)||touched.has(y+1))continue;let found=false;
for(let j of [y,y+1]){for(let x=0;x<n;x++)if(add(B,project(tag(n,x,j)^tag(n,choice[j],j),m),bit(moves.length))){moves.push([x,j]);found=true;break;}if(found)break;}assert(found,"greedy");}
assert(moves.length===r,"rank");let w=solve(B,project(target^base,m));for(let i=0;i<moves.length;i++)if(w&bit(i)){let [x,y]=moves[i];choice[y]=x;}
let s=0n;for(let y=0;y<n;y++)s^=tag(n,choice[y],y);for(let [x,y,v] of pins)assert((choice[y]===x)===!!v,"pin");assert(project(s,m)===project(target,m),"saturated projected witness");projectedWitnesses++;if(p)guardedWitnesses++;
}
if(n===4){let S=new Set();function rec(y,s){if(y===n){S.add(s);exactOwnerSelections++;return;}for(let x=0;x<n;x++)rec(y+1,s^tag(n,x,y));}rec(0,0n);assert(!S.has(target),"saturated UNSAT");for(let k=1;k<=2;k++)for(let i=0;i<32;i++){let m=Array.from({length:k},()=>randmask(2*n));assert([...S].some(s=>project(s,m)===project(target,m)),"brute projected target");exactMaps++;}}
scaling.push({n,affineDimension:2*n-3,guaranteedRank:n/2});
}
return {seed:"0xc0da7",pairRanks,projectedWitnesses,guardedWitnesses,exactOwnerSelections,exactMaps,scaling,disagreements:0};}
if(typeof module!=="undefined")module.exports=run;
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
