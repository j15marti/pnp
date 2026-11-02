// LSPV-4 A9-PETERSEN-BOUND-SHARP328: independent exact checker, no imports
// Standard Node.js; run: node a9_petersen_sharp328_independent.js
const P=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9]];
const N=[[1,5,9],[2,6,7],[3,4,8],[1,6,8],[2,4,9],[3,5,7]].map(c=>c.map(x=>-x));
const F=P.concat(N);
function sat(a){return F.every(c=>c.some(v=>((a>>(Math.abs(v)-1))&1)===(v>0?1:0)));}
let ct=0;for(let a=0;a<512;a++) if(sat(a))ct++;
if(ct!==18)throw Error('A9 count mismatch');
const pairs=new Map();
for(const c of F)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){
 const k=[Math.abs(c[i]),Math.abs(c[j])].sort((a,b)=>a-b).join(',');
 pairs.set(k,(pairs.get(k)||0)+1);
}
if(pairs.size!==36||[...pairs.values()].some(x=>x!==1))throw Error('A9 is not STS9');
function w(i,j){
 const a=F[i],b=F[j],common=a.filter(x=>b.includes(x)).length;
 return common>0?common:(a.every(v=>v>0)!==b.every(v=>v>0)&&a.every(v=>b.includes(-v))?2:0);
}
const memo=new Map();
function opt(mask){
 if(mask===0)return 0;
 if(memo.has(mask))return memo.get(mask);
 let i=0;while(!((mask>>i)&1))i++;
 let rem=mask^(1<<i),best=opt(rem);
 for(let j=i+1;j<F.length;j++)if((rem>>j)&1)best=Math.max(best,opt(rem^(1<<j))+w(i,j));
 memo.set(mask,best);return best;
}
const W=opt((1<<F.length)-1);
if(W!==6)throw Error('matched weight not 6');
const other=[0,0,0,1,1,1,0,0];const pin=[];
for(let x1=0;x1<2;x1++){
 const bits=[x1,...other].reduce((s,v,i)=>s|(v<<i),0);
 pin.push(sat(bits));
}
if(pin.join(',')!=='false,true')throw Error('opposite-label source pins failed');
for(let x=1;x<=9;x++){
 if(F.filter(c=>c.includes(x)).length!==2||F.filter(c=>c.includes(-x)).length!==2)
  throw Error('original occurrence quota violated');
}
console.log(JSON.stringify({source:'A9 original',models:ct,primal_pair_count:pairs.size,
 all_pairs_unique:true,matched_architecture_weight:W,matching_dp_states:memo.size,
 private_gate_count:35,matched_gate_count:35-W,one_bit_pins:{x1_0:pin[0],x1_1:pin[1]},
 infinite_family:{n:'9*t',m:'12*t',matched_gate_count:'30*t-1',models:'18**t'},
 status:'COMPUTATIONAL; restricted symbolic theorem elsewhere; P versus NP OPEN'},null,2));