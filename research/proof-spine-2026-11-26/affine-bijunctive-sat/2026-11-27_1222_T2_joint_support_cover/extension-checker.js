function extensionAudit(){
const base=[[15,32,47],[13,17,28],[14,36,42],[11,53,62],[10,39,45]],B=new Map();
for(let x=0;x<1024;x++){let s=0,ok=true;for(let i=0;i<5;i++){let c=x>>(2*i)&3;if(!c){ok=false;break}s^=base[i][c-1]}if(ok&&!B.has(s))B.set(s,x)}
if(B.size!==63||B.has(29))throw Error("base");
function verify(t){
let planes=base.concat(Array.from({length:t},(_,i)=>[1,2**(6+i),1+2**(6+i)])),n=6+t,count=0,hole=29^(t&1);
for(let s=0;s<2**n;s++){let hi=s>>>6,par=0;for(let i=0;i<t;i++)par^=(hi>>i&1)^1;let ell=(s&63)^par;
if(ell===29&&!hi){if(s!==hole)throw Error("hole");continue}
let j=ell===29?Math.log2(hi&-hi):-1,word=BigInt(B.get(ell^(j<0?0:1))),z=0;
for(let i=0;i<t;i++){let a=1^(hi>>i&1)^Number(i===j),b=hi>>i&1;word|=BigInt(a+2*b)<<BigInt(10+2*i)}
for(let i=0;i<planes.length;i++){let u=Number(word>>BigInt(2*i)&3n);if(!u)throw Error("illegal");z^=planes[i][u-1]}if(z!==s)throw Error("syndrome");count++}
return {t,dimension:n,planes,missing:hole,attained:count,fixed_selector_rank_lower_bound:n-2,fixed_selector_cell_lower_bound:2**(n-2),adaptive_charts:63+t}}
return Array.from({length:13},(_,t)=>verify(t))
}
if(typeof module!=="undefined"){module.exports={extensionAudit};if(require.main===module)console.log(JSON.stringify(extensionAudit()))}
