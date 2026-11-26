function audit(){
 const check=(b)=>{if(!b)throw Error("assertion");stats.assertions++},stats={assertions:0,properSubsets:0,periodProbes:0,referenceWords:0,dpTransitions:0,closureProbes:0,yes:0,no:0,unknownC:0,jobs:[]};
 const pop=x=>{let z=0;while(x){z^=1;x&=x-1}return z};
 const build=(m,d,z)=>({m,d,z,rows:Array.from({length:6*m},(_,j)=>{let i=j%6,k=j-i;return [k+(i+5)%6,j,k+(i+1)%6]}),guards:[...Array.from({length:m},(_,i)=>({ids:[6*i,6*i+1,6*((i+m-1)%m)+1],rhs:d[i]})),{ids:Array.from({length:m},(_,i)=>6*i+1),rhs:z}]});
 const lift=(a,b)=>a.flatMap((v,i)=>[v,b[i],1-v-b[i],v,b[i],1-v-b[i]]);
 const verify=(F,x)=>x&&x.every(v=>v===0||v===1)&&F.rows.every(r=>r.reduce((s,i)=>s+x[i],0)===1)&&F.guards.every(g=>g.ids.reduce((s,i)=>s^x[i],0)===g.rhs);
 function A(F){let {m,d,z}=F,a=d.slice(),b=Array(m).fill(0);if(z){let i=d.indexOf(1);if(i<0){if(m%2===0)return null;b.fill(1);a.fill(0)}else{b[i]=1;a[i]=0;a[(i+1)%m]^=1}}return lift(a,b)}
 function B(F){let {m,d,z}=F;for(let start=0;start<2;start++){let cur=new Map([[2*start,{b:[],a:[]}]]);for(let i=0;i<m;i++){let next=new Map();for(let [key,p] of cur)for(let b=0;b<2;b++){stats.dpTransitions++;let a=d[i]^b^(key>>1);if(a+b>1||i===m-1&&b!==start)continue;let k=2*b+((key&1)^b);if(!next.has(k))next.set(k,{a:[...p.a,a],b:[...p.b,b]})}cur=next}for(let [k,p] of cur)if((k&1)===z)return lift(p.a,p.b)}return null}
 function C(F,cap){let m=F.m,total=3**m;for(let w=0;w<Math.min(cap,total);w++){stats.referenceWords++;let q=w,x=[];for(let i=0;i<m;i++){let k=q%3;q=Math.floor(q/3);x.push(+(k===0),+(k===1),+(k===2),+(k===0),+(k===1),+(k===2))}if(verify(F,x))return true}return total<=cap?false:"UNKNOWN"}
 // Exact local affine hull row test: setting a_i,b_i fixes b_i,b_prev;
 // a third free bit supplies the parity, then all a_j follow.
 function close(F){let {m,d,z}=F;for(let i=0;i<m;i++)for(let [a,b] of [[0,0],[1,0],[0,1]]){let w=Array(m).fill(0);w[i]=b;w[(i+m-1)%m]=a^b^d[i];let k=(i+1)%m;w[k]=w.reduce((s,v)=>s^v,0)^z;let aa=w.map((v,j)=>d[j]^v^w[(j+m-1)%m]);check(aa[i]===a&&w[i]===b&&w.reduce((s,v)=>s^v,0)===z);stats.closureProbes++}return 0}
 function integrated(F){if(F.d.every(v=>!v)){// source-certified implications b_i=>b_prev; SCC all b equal
  let b=F.z?1:0;if((b*(F.m%2))!==F.z)return null;return lift(Array(F.m).fill(0),Array(F.m).fill(b))
 }return B(F)}
 // exact support for all small subsets, including proper period test and full missing target
 for(let m=3;m<=9;m++){let ss=Array.from({length:m},(_,i)=>[0,1<<i,(1<<i)^(1<<((i+1)%m))^(1<<m)]);
 for(let mask=1;mask<(1<<m);mask++){let S=new Set([0]);for(let i=0;i<m;i++)if(mask>>i&1)S=new Set([...S].flatMap(s=>ss[i].map(v=>s^v)));if(mask===(1<<m)-1){check(S.size===(1<<(m+1))-(m%2?0:1));check(S.has(1<<m)===(m%2===1))}else{stats.properSubsets++;for(let t of S)if(t){stats.periodProbes++;check(![...S].every(s=>S.has(s^t)))}}}}
 // source prism atom verified against all 64 assignments
 let atom=build(3,[0,0,0],0).rows.slice(0,6),words=[];for(let x=0;x<64;x++)if(atom.every(r=>r.reduce((s,i)=>s+((x>>i)&1),0)===1))words.push(x);check(JSON.stringify(words)==="[9,18,36]");
 let seed=6112608;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>31};
 for(let m of [3,4,5,6,7,8,9,16,31,32,63,64,127,128]){let ds=m<=5?Array.from({length:1<<m},(_,k)=>Array.from({length:m},(_,i)=>(k>>i)&1)):[Array(m).fill(0),Array.from({length:m},(_,i)=>+(i===0)),...Array.from({length:4},()=>Array.from({length:m},rnd))];for(let d of ds)for(let z=0;z<2;z++){
 let F=build(m,d,z),N=JSON.stringify(F).length,cap=Math.min(4096,N*N),cl=close(F),a=A(F),b=B(F),c=C(F,cap),v=integrated(F);check(Boolean(a)===Boolean(b)&&Boolean(a)===Boolean(v));if(c!=="UNKNOWN")check(c===Boolean(a));else stats.unknownC++;for(let x of [a,b,v])if(x)check(verify(F,x));if(a)stats.yes++;else stats.no++;stats.jobs.push({m,d:d.join(""),z,N,cap,closure:cl,A:!!a,B:!!b,C:c,integrated:!!v,witness:a});}}
 return stats;
}
console.log(JSON.stringify(audit(),null,2));
