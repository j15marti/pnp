function interfaceAudit(){
 let state=39174139,stats={seed:39174139,checks:0,localSystems:0,chains:0,chainSAT:0,chainUNSAT:0,interpolations:0,relaxations:0,large:[]};
 const rnd=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return (state>>>8)%n};
 const ok=(p,m)=>{stats.checks++;if(!p)throw Error(m)};
 const B=2;
 // An atom [v,a,c,b,d] means h[v] <= max(h[a]+c,h[b]+d) in a plus bag,
 // or -h[v] <= max(-h[a]+c,-h[b]+d) in a minus bag.
 const evalAtoms=(h,atoms,sign)=>atoms.every(([v,a,c,b,d])=>sign*h[v]<=Math.max(sign*h[a]+c,sign*h[b]+d));
 function normalize(h){return h.map(v=>v-h[0])}
 function localBound(h){return h[0]===0&&h.slice(1).every(v=>Math.abs(v)<=B)}
 function solve(atoms,sign,d,child){let A=atoms.slice();
  const diff=(v,a,c)=>A.push(sign===1?[v,a,c,a,c]:[a,v,c,v,c]);
  if(d!==null){diff(1,0,d);diff(0,1,-d)}
  if(child){diff(2,1,child.hi);diff(1,2,-child.lo)}
  let h=[0,B,B];for(;;){let changed=false;for(const [v,a,c,b,e] of A){stats.relaxations++;let z=Math.max(h[a]+c,h[b]+e);if(h[v]>z){if(v===0||z< -B)return null;h[v]=z;changed=true}}if(!changed)return h.map(v=>sign*v)}
 }
 function summary(atoms,sign,child){let list=[];for(let d=-B;d<=B;d++){let h=solve(atoms,sign,d,child);if(h)list.push({d,h})}
  if(!list.length)return null;let lo=list[0],hi=list[list.length-1];ok(list.length===hi.d-lo.d+1,"interval gap");return {lo:lo.d,hi:hi.d,L:lo.h,H:hi.h,sign};
 }
 function interpolate(S,d){ok(S.lo<=d&&d<=S.hi,"interface out of bounds");
  let h=S.sign===1?S.L.map((v,i)=>Math.max(v,S.H[i]+d-S.hi)):S.H.map((v,i)=>Math.min(v,S.L[i]+d-S.lo));
  ok(localBound(h)&&h[1]===d,"interpolation");stats.interpolations++;return h;
 }
 function bruteLocal(atoms,sign,child){let out=[];for(let a=-B;a<=B;a++)for(let b=-B;b<=B;b++){let h=[0,a,b];if(evalAtoms(h,atoms,sign)&&(!child||child.lo<=b-a&&b-a<=child.hi))out.push(h)}return out}
 function randomBag(){let sign=rnd(2)?1:-1,A=[];for(let i=0,k=rnd(8);i<k;i++)A.push([rnd(3),rnd(3),rnd(3)-1,rnd(3),rnd(3)-1]);return {sign,A}}
 function localCheck(bag,child){let S=summary(bag.A,bag.sign,child),br=bruteLocal(bag.A,bag.sign,child);stats.localSystems++;
  ok(!!S===!!br.length,"local existence");if(S){let ds=[...new Set(br.map(h=>h[1]))].sort((a,b)=>a-b);ok(ds.length===S.hi-S.lo+1&&ds[0]===S.lo&&ds[ds.length-1]===S.hi,"brute interval");
   for(let d=S.lo;d<=S.hi;d++){let h=interpolate(S,d);ok(evalAtoms(h,bag.A,bag.sign)&&(!child||child.lo<=h[2]-h[1]&&h[2]-h[1]<=child.hi),"lift local");}}
  return S;
 }
 function chain(bags,audit=true){let S=Array(bags.length),C=null;for(let i=bags.length-1;i>=0;i--){let b=bags[i];C=audit?localCheck(b,C):summary(b.A,b.sign,C);if(!C)return null;S[i]=C}
   let h=interpolate(S[0],S[0].lo),H=h.slice();
   for(let i=1;i<bags.length;i++){let d=H[i+1]-H[i],w=interpolate(S[i],d);H.push(H[i]+w[2]);}
   bags.forEach((b,i)=>{let h=normalize(H.slice(i,i+3));ok(localBound(h)&&evalAtoms(h,b.A,b.sign),"global lift")});return H;
 }
 // Independent exhaustive joins on actual local words, no intervals.
 function bruteChain(bags){const states=bags.map(b=>bruteLocal(b.A,b.sign,null));function rec(i,d){if(i===states.length)return true;for(const h of states[i])if((d===null||h[1]===d)&&rec(i+1,h[2]-h[1]))return true;return false}return rec(0,null)}
 for(let i=0;i<500;i++){let l=rnd(5)-2,h=l+rnd(3);localCheck(randomBag(),{lo:l,hi:h})}
 for(let i=0;i<450;i++){let bags=Array.from({length:2+rnd(5)},randomBag);let w=chain(bags);ok(!!w===bruteChain(bags),"chain decision");stats.chains++;stats[w?"chainSAT":"chainUNSAT"]++}
 // Alternating genuine nontrivial max and min atoms; explicit all-zero witness.
 for(let n of [16,64,256,1024]){let bags=Array.from({length:n},(_,i)=>({sign:i%2?1:-1,A:[[0,1,0,2,0],[2,0,1,1,0],[1,0,0,2,1]]}));let w=chain(bags,false);ok(!!w,"large SAT");stats.large.push({bags:n,faces:n+2,oppositePolarityBags:n/2,status:"YES"})}
 return stats;
}
console.log(JSON.stringify(interfaceAudit(),null,2));
