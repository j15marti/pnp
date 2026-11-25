function runGD22(){
  let checks=0,closureScans=0,branchCalls=0,transitionCalls=0;
  const ck=(x)=>{checks++;if(!x)throw Error("assertion "+checks)};
  const words=["100001011010100001010100101001010110","100001010100001011010100011100011110","100001010110001011010100011100011110","100011110001110001010100101001010110","100011100011100011010100101001010110","100001110100001011010100011100011110"];
  const W=words.map(s=>[...s].map(Number));
  const tmpl=[[[0,2,5],[1,3,8],[4,7,10],[6,9,11]],[[0,2,5],[1,3,8],[4,7,10],[6,9,11]],[[0,2,5],[1,3,10],[4,7,9],[6,8,11]]];
  const special=[[0,4,8],[1,3,6],[2,9,11],[5,7,10]];
  const base=Array.from({length:36},(_,v)=>(Math.floor(v/3)%2)^Number(v%3===Math.floor(v/3)%3));
  const good=(w,e)=>!(w[e[0]]===w[e[1]]&&w[e[1]]===w[e[2]]);
  const valid=(w,E)=>E.every(e=>good(w,e));
  function clauses(q){let P=Array.from({length:4},()=>[]),L=12*q;for(let i=0;i<L;i++)for(let j=0;j<3;j++)P[(i+j)%3].push([3*i+j,3*((i+1)%L)+j,3*((i+1)%L)+(j+1)%3]);for(let b=0;b<q;b++)for(let j=0;j<3;j++)for(const e of b===0&&j===0?special:tmpl[j])P[3].push(e.map(i=>36*b+3*i+j));return P}
  function checkPartitions(P,n){let pairs=new Set;for(const p of P){let c=Array(n).fill(0);for(const e of p){ck(new Set(e).size===3);for(const i of e)c[i]++;for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let k=[e[a],e[b]].sort((a,b)=>a-b).join(",");ck(!pairs.has(k));pairs.add(k)}}ck(c.every(v=>v===1))}}
  function propagate(w,E){while(true){closureScans++;let changed=false;for(const e of E){let a=e.map(i=>w[i]),v=a.filter(b=>b>=0);if(v.includes(0)&&v.includes(1))continue;if(v.length===3)return false;if(v.length===2){w[e[a.indexOf(-1)]]=1-v[0];changed=true}}if(!changed)return true}}
  function solve(w,E){branchCalls++;if(!propagate(w,E))return null;let i=w.indexOf(-1);if(i<0)return w;for(let b=0;b<2;b++){let v=w.slice();v[i]=b;let z=solve(v,E);if(z)return z}return null}
  function localTable(isSpecial,seed){let E=[];for(let i=0;i<12;i++)for(let j=0;j<3;j++)E.push([3*i+j,3*(i+1)+j,3*(i+1)+(j+1)%3]);for(let j=0;j<3;j++)for(const e of isSpecial&&j===0?special:tmpl[j])E.push(e.map(i=>3*i+j));let T=Array.from({length:8},()=>Array(8).fill(null));for(let a=0;a<8;a++)for(let b=0;b<8;b++){transitionCalls++;let w=Array(39).fill(-1);for(let j=0;j<3;j++){w[j]=(a>>j)&1;w[36+j]=(b>>j)&1}if(isSpecial&&seed!==null&&w[0]!==seed)continue;let z=solve(w,E);if(z){ck(valid(z,E));T[a][b]=z.slice(0,36)}}return T}
  function ringDP(q,T0,T){for(let start=0;start<8;start++){let states=new Map([[start,[]]]);for(let b=0;b<q;b++){let next=new Map;for(let [a,path] of states)for(let c=0;c<8;c++)if((b===0?T0:T)[a][c]&&!next.has(c))next.set(c,path.concat([(b===0?T0:T)[a][c]]));states=next}if(states.has(start))return states.get(start).flat()}return null}
  let maxs=[];for(let s=0;s<8;s++){let D=Array.from({length:8},(_,i)=>i).filter(i=>i!==s&&i!==(s^7)),max=0;for(let m=0;m<64;m++){let L=D.filter((_,i)=>(m>>i)&1),A=new Set(L);if(L.every(a=>L.every(b=>A.has(a&b)&&A.has(a|b))))max=Math.max(max,L.length)}ck(max<=4);maxs.push(max)}
  ck(new Set(W.map(w=>[w[6],w[9],w[10]].join(""))).size===6);for(const w of W){ck(w.length===36);ck([0,1,2,33,34,35].every(i=>w[i]===base[i]))}
  let T=localTable(false,null), T0=[localTable(true,0),localTable(true,1)], scales=[];
  for(let q of [2,3,4,8,16,32]){
    let P=clauses(q),E=P.flat(),n=36*q,x=Array.from({length:n},(_,i)=>Math.floor(i/3)%2),y=x.slice();y[0]^=1;checkPartitions(P,n);ck(valid(x,P[0].concat(P[1])));ck(valid(y,P[2].concat(P[3])));ck(!valid(x,E)&&!valid(y,E));ck(x.filter((v,i)=>v!==y[i]).length===1);
    for(let s=0;s<2;s++){let pin=Array(n).fill(-1);pin[0]=s;ck(propagate(pin,E));ck(pin.filter(v=>v>=0).length===1);let z=ringDP(q,T0[s],T);ck(z&&z[0]===s&&valid(z,E))}
    let count=q<=4?6**(q-1):32;
    for(let k=0;k<count;k++){let z=base.slice(),a=k;for(let b=1;b<q;b++){let j=q<=4?a%6:(k+3*b)%6;a=Math.floor(a/6);z.push(...W[j])}ck(valid(z,E));ck(z[0]===1);ck(valid(z.map(v=>1-v),E))}
    scales.push({q,n,witnessChoicesChecked:count*2,log2FlatCoverLowerBound:(q-1)*Math.log2(1.5),bothSeedFibersDP:true})
  }
  let P=[Array.from({length:3},(_,r)=>[3*r,3*r+1,3*r+2]),Array.from({length:3},(_,c)=>[c,3+c,6+c]),... [1,-1].map(d=>Array.from({length:3},(_,b)=>Array.from({length:3},(_,r)=>3*r+(d*r+b+3)%3)))];checkPartitions(P,9);
  let x=[0,0,1,0,0,1,1,1,0],y=x.slice();y[8]=1;ck(valid(x,P[0].concat(P[1]))&&valid(y,P[2].concat(P[3])));let modelCount=0;for(let i=0;i<512;i++){let w=Array.from({length:9},(_,j)=>(i>>j)&1);if(valid(w,P.flat()))modelCount++}ck(modelCount===0);for(let b=0;b<2;b++){let pin=Array(9).fill(-1);pin[8]=b;ck(propagate(pin,P.flat()));ck(pin.filter(v=>v>=0).length===1);ck(solve(pin,P.flat())===null)}
  return {checks,closureScans,branchCalls,transitionCalls,ordinaryTransitionCount:T.flat().filter(Boolean).length,specialTransitionCounts:T0.map(t=>t.flat().filter(Boolean).length),maxLatticeSizes:maxs,localWitnesses:words,scales,unsatAffinePlane:{words:512,models:modelCount,oneMismatch:true,bothPinDpllUnsat:true},limits:"No general polynomial repair search, actual residual cycle extraction, formal kernel, or physical CM. Constant-size local DPLL and ring DP only."}
}
console.log(JSON.stringify(runGD22(),null,2));
