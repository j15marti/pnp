// node redteam.js -- C08-17 guarded closure obstruction and autarky check
function redteam(){
let checks=0,seed=20261127,wordScans=0;function ok(v,m){checks++;if(!v)throw Error(m||"check "+checks)}
function rnd(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
function parity(x){x^=x>>>16;x^=x>>>8;x^=x>>>4;return(0x6996>>>(x&15))&1}
function mult(a,b){let c=0;while(b){if(b&1)c^=a;b>>>=1;a<<=1;if(a&64)a^=67}return c}
for(let a=1;a<64;a++){let inv=false;for(let b=1;b<64;b++)if(mult(a,b)===1)inv=true;ok(inv)}
let col=Array.from({length:64},(_,t)=>1|(t<<1)|(mult(mult(t,t),t)<<7)),pairSums=new Set;
ok(new Set(col).size===64&&col.every(c=>c&1));for(let a=0;a<64;a++)for(let b=a+1;b<64;b++){let t=col[a]^col[b];ok(!pairSums.has(t)&&t!==0);pairSums.add(t)}
function rank(V){let P=new Uint32Array(13),r=0;for(let a of V){for(let i=12;i>=0&&a;i--)if((a>>>i)&1){if(P[i])a^=P[i];else{P[i]=a;r++;break}}}return r}
ok(rank(col)===13);
let words=[];for(let z=0;z<8192;z++){let a=0,b=0;for(let i=0;i<32;i++){a|=parity(col[i]&z)<<i;b|=parity(col[i+32]&z)<<i}words.push([a>>>0,b>>>0])}
function accepts(a,b){return (((a|(a>>>1))&0x55555555)===0x55555555)&&(((b|(b>>>1))&0x55555555)===0x55555555)}
let offsets=[],target=null;
for(let j=0;j<128;j++){let a=rnd(),b=rnd(),num=0;for(let [u,v] of words){wordScans++;if(accepts(u^a,v^b))num++}offsets.push({a,b,models:num});if(!num){target=[a,b];break}}ok(target!==null);
const value=(word,i)=>(word[i>>5]>>>(i&31))&1;
let guardedProfiles=0;for(let i=0;i<64;i++)for(let bit of [0,1]){let pins=[[i,bit]];if(!bit)pins.push([i^1,1]);let selected=words.filter(w=>pins.every(([j,b])=>(value(w,j)^value(target,j))===b));ok(selected.length===2**(13-pins.length));guardedProfiles+=selected.length; // independent coordinate projections of affine space after each branch
for(let j=0;j<64;j++)if(!pins.some(p=>p[0]===j)){let a=selected[0],v=value(a,j);ok(selected.some(w=>value(w,j)!==v))}
for(let j=0;j<64;j++)for(let k=j+1;k<64;k++)if(!pins.some(p=>p[0]===j||p[0]===k)){ok(rank(pins.map(([i])=>col[i]).concat([col[j],col[k]]))===pins.length+2)}}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
let C=AG.flat().filter(c=>c.join(",")!=="0,1,2"&&c.join(",")!=="3,4,5"),capAut=0;
function partial(c,x){let has=false,z=0;for(let [v,s] of c){if(x[v]<0)continue;has=true;z|=1<<(x[v]^s)}return !has||z===3}
let L=C.map(c=>c.map(v=>[v,0]));for(let w=0;w<3**9;w++){let q=w,x=[];for(let i=0;i<9;i++){x.push(q%3-1);q=Math.floor(q/3)}if(L.every(c=>partial(c,x))){capAut++;ok(x.slice(0,6).every(v=>v<0)||x.slice(0,6).every(v=>v>=0));if(x.slice(0,6).every(v=>v<0))ok(x.every(v=>v<0))}}
let cycles=[];for(let n of [6,8,10,12])for(let no of [true,false]){let w=Array(n).fill(0);w[0]=+no;let C=Array.from({length:n},(_,i)=>[[i,0],[(i+n-1)%n,w[(i+n-1)%n]],[(i+1)%n,1^w[i]]]),aut=0,full=0;
for(let a=0;a<3**n;a++){let v=a,x=[];for(let i=0;i<n;i++){x.push(v%3-1);v=Math.floor(v/3)}if(C.every(c=>partial(c,x))){aut++;if(x.every(v=>v>=0))full++;ok(x.every(v=>v<0)||x.every(v=>v>=0))}}ok(aut===(no?1:5)&&full===(no?0:4));cycles.push({n,label:no?"UNSAT":"SAT",partialWords:3**n,autarkies:aut,full})}
return{seed:20261127,checks,wordScans,fieldPolynomial:"x^6+x+1",columnRank:13,columnCount:64,pairSums:pairSums.size,offsetTrials:offsets,target,guardedProfiles,all128SingletonBranchesConsistentInBothRelaxations:true,capAutarkies:capAut,cycles};
}
console.log(JSON.stringify(redteam(),null,2));
