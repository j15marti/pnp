// Run: node gauge_wup_audit.js
const audit=function audit(){
const check=(b,s)=>{if(!b)throw Error(s)};
const parity=t=>{let q=-1;for(let i=0;i<t.length;i++)if(t[i]){let p=i.toString(2).replace(/0/g,"").length%2;if(q<0)q=p;else if(q!==p)return false}return q>=0};
let B=[];for(let a of [-1,0,1])for(let b of [-1,0,1])for(let c of [-1,0,1])for(let d of [-1,0,1])if(a*d-b*c)B.push([[a,b],[c,d]]);
const diag=M=>M[0][1]===0&&M[1][0]===0,anti=M=>M[0][0]===0&&M[1][1]===0;
function q(M){let [[a,b],[c,d]]=M;return [[a*d+b*c,2*b*d],[-2*a*c,-a*d-b*c]]} // det(M)*M^-1 Z M
// Correct formula for offdiagonal from adj(M) Z M: (2bd,-2ac).
function dual(M){let [[a,b],[c,d]]=M;return [[d,-c],[-b,a]]} // det(M) M^-T
function transform(M,words){
 let out=[];for(let j=0;j<(1<<M.length);j++){let sum=0;for(let w of words){let z=1;for(let i=0;i<M.length;i++)z*=M[i][j>>i&1][w>>i&1];sum+=z}out.push(sum)}return out;
}
let tests=0,eqGood=0,wGood=0,conflicts=0;
for(let a of B)for(let b of B)for(let c of B){
 let M=[a,b,c],Q=M.map(q),e=parity(transform(M,[0,7])),w=parity(transform(M.map(dual),[1,2,4]));tests++;
 if(e){eqGood++;check(Q.every(anti),"EQ3 parity not anti");}
 if(w){wGood++;check(Q.every(x=>x[1][0]===0||x[0][1]===0),"W3 triangular necessary");check(Q.every(x=>!anti(x)),"W3 anti");}
 if(e&&w)conflicts++;
}
check(conflicts===0,"gauge collision");
let local=Array.from({length:16},()=>[0,0]);for(let w=0;w<16;w++)for(let s=0;s<256;s++){
 if((s&3)!==(w&3))continue;
 let row=[((w>>2)&1)+((w>>3)&1),0,0,0,0,0];
 for(let i=0;i<8;i++)if(s>>i&1){if(i>=2)row[i>>2]++;row[2+(i>>1&1)]++;row[4+(i&1)]++}
 if(row.every(x=>x===1)){local[w][0]++;if(!(s&(1<<2|1<<5)))local[w][1]++}
}
function pm(mask,edges){if(!mask)return 1;let i=0;while(!(mask>>i&1))i++;let z=0;for(let [a,b] of edges){if(a===i&&mask>>b&1)z+=pm(mask^(1<<a)^(1<<b),edges);if(b===i&&mask>>a&1)z+=pm(mask^(1<<a)^(1<<b),edges)}return z}
let cycle=[[0,4],[4,1],[1,2],[2,5],[5,3],[3,0]],path=cycle.slice(0,-1);
for(let w=0;w<16;w++){check(pm(63^w,cycle)===local[w][0],"cycle");check(pm(63^w,path)===local[w][1],"path")}
function grid(l){
 let k=l*l,id=(i,j)=>i+l*j,T=[],E=[],O=[],I=[];
 for(let a=0;a<k;a++)for(let i=0;i<8;i++)T.push([2*a+(i>>2),2*a+(i>>1&1),2*a+(i&1)]);
 for(let i=0;i<l;i++)for(let j=0;j<l;j++){if(i+1<l)E.push([id(i,j),0,id(i+1,j),0]);if(j+1<l)E.push([id(i,j),1,id(i,j+1),1]);}
 for(let i=0;i<l;i++)O.push([id(i,l-1),1]);for(let j=l-1;j>=0;j--)O.push([id(l-1,j),0]);
 for(let i=l-1;i>=0;i--)I.push([id(i,0),1]);for(let j=0;j<l;j++)I.push([id(0,j),0]);
 I.reverse();O.forEach((x,i)=>E.push([...x,...I[i]]));for(let [a,p,b,q] of E)T[8*a+p][0]=2*b;
 return {k,T,E}
}
function countNative(F,prune){let n=2*F.k,T=F.T.filter((_,i)=>!prune||![2,5].includes(i%8)),R=Array.from({length:n},()=>[]);for(let [x,y,z] of T)R[x].push([y,z]);
 function f(i,Y,Z){if(i===n)return 1n;let s=0n;for(let[y,z]of R[i]){let a=1n<<BigInt(y),b=1n<<BigInt(z);if(!(Y&a)&&!(Z&b))s+=f(i+1,Y|a,Z|b)}return s}
 return f(0,0n,0n)
}
function permanent(F,w){let n=F.k,A=Array.from({length:n},(_,i)=>new Map([[i,BigInt(w)]]));for(let [a,p,b,q] of F.E)A[a].set(b,(A[a].get(b)||0n)+1n);
 let dp=new Map([[0,1n]]);for(let row of A){let next=new Map();for(let [s,v] of dp)for(let [j,x] of row)if(!(s>>j&1)){let t=s|1<<j;next.set(t,(next.get(t)||0n)+v*x)}dp=next}return dp.get((1<<n)-1)||0n
}
let scales=[];for(let l of [1,2,3,4,8,12]){
 let F=grid(l),n=2*F.k,T=F.T.filter((_,i)=>![2,5].includes(i%8)),deg=Array(3*n).fill(0);
 for(let t of T)t.forEach((x,c)=>deg[c*n+x]++);
 check(deg.every(x=>x===3)&&T.length===deg.length,"not cubic after WUP");
 let out=Array.from({length:F.k},()=>[]);F.E.forEach((e,i)=>out[e[0]].push(i));
 let yes=new Set(),no=new Set(),lifts=0;
 function lift(cyc){let W=Array(F.k).fill(0);for(let i of cyc){let[a,p,b,q]=F.E[i];W[a]|=1<<p;W[b]|=1<<(2+q)}
  let sel=new Set;for(let i=0;i<F.k;i++){let w=W[i],ids=w===0?[3,4]:(w&1)?[0,7]:[1,6];check(local[w][1]===1,"missing response");for(let j of ids)sel.add(8*i+j)}
  let occ=Array(3*n).fill(0);for(let i of sel){check(![2,5].includes(i%8),"pruned tuple");F.T[i].forEach((x,c)=>occ[c*n+x]++)}check(occ.every(x=>x===1),"lift");
  for(let i=0;i<F.T.length;i++)if(![2,5].includes(i%8)){(sel.has(i)?yes:no).add(i)}lifts++;
 }
 lift([]);
 for(let i=0;i<F.E.length;i++){
  let[a,p,b,q]=F.E[i],P=new Map([[b,-1]]),Q=[b];for(let v of Q){if(P.has(a))break;for(let j of out[v]){let z=F.E[j][2];if(!P.has(z)){P.set(z,j);Q.push(z)}}}
  check(P.has(a),"no cycle");let C=[i],v=a;while(v!==b){let j=P.get(v);C.push(j);v=F.E[j][0]}lift(C);
 }
 check(yes.size===T.length&&no.size===T.length,"unary");
 let cnt=null;if(l<=4){cnt=[permanent(F,2).toString(),permanent(F,1).toString()];if(l<=3)check(cnt[0]===countNative(F,false).toString()&&cnt[1]===countNative(F,true).toString(),"count mismatch")}
 scales.push({l,original:F.T.length,pruned:T.length,minimum_defects:T.length,lifts,counts_original_pruned:cnt})
}
return {bases:B.length,basis_triples:tests,eq3_parity_cases:eqGood,w3_parity_cases:wGood,shared_parity_cases:conflicts,local_count_pairs:local,scales};
};
console.log(JSON.stringify(audit(),null,2));
