// LSPV-1/531. Standalone V8/Node finite verifier. No nonstandard dependencies.

// Model: original two one-hot q-state indicator groups, no auxiliary variables; conditional on exact onehot.

// Does not check native R_mix341 or establish P vs NP.

function comb(n,r){let z=1;for(let j=1;j<=r;j++)z=z*(n-j+1)/j;return Math.round(z)}

function km(q){let k=0;while(comb(k,Math.floor(k/2))<q)k++;return k}

function make(q,c=0,sign=1){
 const k=km(q),w=Math.floor(k/2),code=[];for(let x=0;x<(1<<k)&&code.length<q;x++)if(x.toString(2).replace(/0/g,"").length===w)code.push(x);
 const p=Array.from({length:q},(_,i)=>(sign*(c-i)%q+q)%q),clauses=[];
 for(let j=0;j<k;j++){const S=code.map((m,i)=>[m,i]).filter(a=>(a[0]>>j)&1).map(a=>a[1]),T=code.map((m,i)=>[m,i]).filter(a=>!((a[0]>>j)&1)).map(a=>p[a[1]]);
 const C=[];for(let i=0;i<q;i++)if(!S.includes(i))C.push(i+1);for(let i=0;i<q;i++)if(!T.includes(i))C.push(q+i+1);if(C.length!==q)throw Error("WIDTH");clauses.push(C)}
 let truth=0;
 for(let x=0;x<q;x++)for(let y=0;y<q;y++){let actual=clauses.every(C=>C.some(a=>a<=q?x===a-1:y===a-q-1)),want=y===p[x];if(actual!==want)throw Error(`TRUTH q${q} c${c} x${x} y${y}`);truth++}
 return {q,c,sign,k,widths:clauses.map(a=>a.length),tested:truth,codes:code,clauses,permutation:p};
}

function brute(q){
 const p=Array.from({length:q},(_,i)=>(q-i)%q),good=new Set(),full=[];let target=0;for(let x=0;x<q;x++)for(let y=0;y<q;y++)if(y!==p[x])target|=(1<<(x*q+y));
 for(let z=0;z<3**(2*q);z++){let a=z,pattern=[];for(let i=0;i<2*q;i++){pattern.push(a%3-1);a=Math.floor(a/3)}let m=0,sound=true;
 for(let x=0;x<q&&sound;x++)for(let y=0;y<q;y++){let sat=false;for(let i=0;i<2*q;i++){const t=pattern[i];if(!t)continue;const v=i<q?x===i:y===i-q;if((t===1&&v)||(t===-1&&!v)){sat=true;break}}if(!sat){if(y===p[x]){sound=false;break}m|=1<<(x*q+y)}}
 if(sound&&m)good.add(m)}
 let reached=new Set([0]),levels=[];for(let t=1;t<=km(q);t++){let next=new Set();for(let a of reached)for(let b of good)next.add(a|b);reached=next;levels.push(reached.size);if(reached.has(target))return {q,firstCover:t,uniqueSoundFalsityMasks:good.size,reachableSizes:levels}}
 throw Error("no cover");
}

function run(){
 let cases=0,pairs=0;for(let q=2;q<=11;q++)for(let c of [0,1,q-1])for(let s of [1,-1]){const r=make(q,c,s);cases++;pairs+=r.tested}
 let exact=[2,3,4].map(brute);for(const e of exact)if(e.firstCover!==km(e.q))throw Error("OPT");
 const samples=[make(3),make(5)],seq=Array.from({length:10},(_,i)=>({q:i+2,k:km(i+2),binomial:comb(km(i+2),Math.floor(km(i+2)/2))}));
 return {status:"PASS",run:"LSPV1_531_PERMUTATION_ONEHOT_CROWN",model:"no auxiliary, original onehot indicators, unrestricted CNF clause width",cases,pairs,exact,samples,seq,checks:{wrong_valid_pairs:0,exact_small_q:true,positive_literal_construction:true},historical_rmix_checker_executed:false};
}

const result=run();

if (typeof console !== 'undefined') console.log(JSON.stringify(result,null,2));
