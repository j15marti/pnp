'use strict';
function coalitionAudit(){
  let checks=0,seed=20261125;
  const assert=(x,m="assert")=>{checks++;if(!x)throw Error(m)};
  function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
  const xor=a=>a.reduce((x,y)=>x^y,0n);
  function red(x,B){for(const [p,v] of B)if(x&p)x^=v;return x}
  function add(B,x){x=red(x,B);if(!x)return false;B.push([1n<<BigInt(x.toString(2).length-1),x]);B.sort((a,b)=>a[0]>b[0]?-1:a[0]<b[0]?1:0);return true}
  function subsets(n,k){let out=[];function rec(i,s){if(s.length)out.push(s.slice());if(s.length===k)return;for(let j=i;j<n;j++){s.push(j);rec(j+1,s);s.pop()}}rec(0,[]);return out}
  function table(A,I,B=[]){let S=new Map([[0n,[]]]);for(const i of I){const T=new Map();for(const [s,w] of S)for(const a of A[i]){let v=s^red(a,B);if(!T.has(v))T.set(v,[...w,a])}S=T}return S}
  function periods(S){let a=S.keys().next().value;return [...S.keys()].map(x=>x^a).filter(p=>p&&[...S.keys()].every(y=>S.has(y^p)))}
  function saturate(A,k,reverse=false){let H=[],log=[],I=subsets(A.length,k);if(reverse)I.reverse();
    while(true){let step=null;for(const group of I){const P=periods(table(A,group,H));if(P.length){step={group,before:H.slice(),p:reverse?P[P.length-1]:P[0]};break}}
      if(!step)break;assert(add(H,step.p));log.push(step);
    }return {H,log}
  }
  function lift(A,t,H,log){const I=A.map((_,i)=>i),Q=table(A,I,H),w=Q.get(red(t,H));if(!w)return null;let d=t^xor(w);
    for(let j=log.length-1;j>=0;j--){const {group,before,p}=log[j],r=red(d,before);assert(r===0n||r===p);
      if(r){const old=xor(group.map(i=>w[i])),need=red(old,before)^r,v=table(A,group,before).get(need);assert(v!==undefined);
        d^=old^xor(v);for(let q=0;q<group.length;q++)w[group[q]]=v[q];
      }
    }assert(d===0n&&xor(w)===t&&w.every((x,i)=>A[i].includes(x)));return w
  }
  let targets=0,orders=0;
  for(let run=0;run<240;run++){
    const d=1+rng(6),n=1+rng(5),A=Array.from({length:n},()=>[...new Set(Array.from({length:1+rng(5)},()=>BigInt(rng(1<<d))))]),k=Math.min(2,n);
    const a=saturate(A,k),b=saturate(A,k,true);assert(a.H.length===b.H.length&&a.H.every(([,v])=>red(v,b.H)===0n),"canonical closure");orders++;
    const actual=table(A,A.map((_,i)=>i));
    for(let t=0;t<(1<<d);t++){assert(!!lift(A,BigInt(t),a.H,a.log)===actual.has(BigInt(t)),"coalition lift");targets++}
  }
  const pair=[[0n,1n,2n],[0n,1n,2n]],a=saturate(pair,1),b=saturate(pair,2);
  assert(a.H.length===0&&b.H.length===2);for(let t=0;t<4;t++)assert(!!lift(pair,BigInt(t),b.H,b.log));
  const cycle=[];let properSubsets=0;
  for(let n=3;n<=10;n++){const E=i=>1n<<BigInt(i),A=Array.from({length:n},(_,i)=>[0n,E(i),E(i)^E((i+1)%n)]);
    for(const I of subsets(n,n-1)){assert(periods(table(A,I)).length===0,"proper coalition aperiodic");properSubsets++}
    const full=table(A,A.map((_,i)=>i));assert(full.size===2**n,"full cycle");cycle.push({n,properSubsets:2**n-2,full:full.size})
  }
  return {seed:20261125,checks,randomCoalitionOrderComparisons:orders,targets,properSubsets,cycle,pair:{singleRank:a.H.length,pairRank:b.H.length},scope:"abstract support tables, exhaustive small controls; mathematical cycle proof general"};
}
console.log(JSON.stringify(coalitionAudit(),null,2));
