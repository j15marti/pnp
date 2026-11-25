const result = (function () {
  const out={checks:0,rank:[],guardedWords:0,pinCases:0,pinSAT:0,pinUNSAT:0,closureScans:0,forcedPins:0,referenceWords:0,fano:[]};
  function check(x){out.checks++;if(!x)throw Error("assert "+out.checks);}
  function pop(x){let n=0;while(x){x&=x-1;n++;}return n;}
  function gf2(rows){const basis=new Map();for(let x of rows){while(x){const p=x.toString(2).length-1;if(basis.has(p))x^=basis.get(p);else{basis.set(p,x);break;}}}return basis.size;}
  // Each half of a group has a different private bit, with two opposite rows
  // guarded by its exterior bit. Check existence of a private assignment directly.
  function compatible(a,b){for(let p=0;p<4;p++){const u=p&1,v=(p>>1)&1;let ok=true;for(const [g,x] of [[a,u],[b,v]])if(g&&(x!==0||x!==1))ok=false;if(ok)return true;}return false;}
  function closure(clauses,initial){const pins=initial.slice();for(;;){out.closureScans++;let changed=false;for(const c of clauses){let sat=false,free=[];for(const l of c){const i=Math.abs(l)-1,need=l>0?1:0;if(pins[i]===need)sat=true;else if(pins[i]===-1)free.push(l);}if(sat)continue;if(!free.length)return null;if(free.length===1){const l=free[0];pins[Math.abs(l)-1]=l>0?1:0;out.forcedPins++;changed=true;break;}}if(!changed)return pins;}}
  function satisfies(clauses,w){return clauses.every(c=>c.some(l=>((w>>(Math.abs(l)-1))&1)===(l>0?1:0)));}
  function respects(p,w){return p.every((v,i)=>v===-1||v===((w>>i)&1));}
  function refs(clauses,p){let models=[];for(let w=0;w<2**p.length;w++)if(respects(p,w)){out.referenceWords++;if(satisfies(clauses,w))models.push(w);}return models;}
  for(let k=1;k<=8;k++){
    const n=2**k,all=n-1,rows=[];
    for(let a=0;a<n;a++){let row=0n;for(let c=0;c<n;c++){const b=all^c;let actual=true;for(let i=0;i<k;i++)actual=actual&&!compatible((a>>i)&1,(b>>i)&1);const expected=(a|b)===all;check(actual===expected);out.guardedWords++;check(!actual||c<=a);if(actual)row|=1n<<BigInt(c);}check((row&(1n<<BigInt(a)))!==0n);rows.push(row);}
    const rank=gf2(rows);check(rank===n);
    // Exact deterministic residual-key enumeration over all possible prefixes.
    function peak(order){let states=new Set([0]),seenA=0,seenB=0,both=0,max=1;for(const [i,h] of order){const bit=1<<i,next=new Set();let other=h?seenA:seenB;for(const x of states){for(let v=0;v<2;v++){if(other&bit){if(!(x&bit)&&!v)continue;next.add(x&~bit);}else next.add(v?x|bit:x&~bit);}}if(h)seenB|=bit;else seenA|=bit;both=seenA&seenB;for(const x of next)check((x&both)===0);states=next;max=Math.max(max,states.size);}check(states.size===1&&states.has(0));return max;}
    const left=Array.from({length:k},(_,i)=>[i,0]),right=Array.from({length:k},(_,i)=>[i,1]);const grouped=peak([...left,...right]),interleaved=peak(left.flatMap((x,i)=>[x,right[i]]));check(grouped===n&&interleaved===2);out.rank.push({k,rank,grouped,interleaved});
  }
  for(let k=1;k<=4;k++){
    const clauses=Array.from({length:k},(_,i)=>[i+1,k+i+1]);
    for(let t=0;t<3**(2*k);t++){let q=t,p=[];for(let i=0;i<2*k;i++){p.push(q%3-1);q=Math.floor(q/3);}let orig=refs(clauses,p),closed=closure(clauses,p);out.pinCases++;if(orig.length)out.pinSAT++;else out.pinUNSAT++;check((closed!==null)===(orig.length>0));if(closed){check(orig.every(w=>respects(closed,w)));const witness=closed.reduce((w,v,i)=>w|((v===-1?1:v)<<i),0);check(respects(p,witness)&&satisfies(clauses,witness));}}
  }
  const triples=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
  function fano(owners,label){const clauses=owners.flatMap(c=>[c,c.map(x=>-x)]),p=Array(7).fill(-1),closed=closure(clauses,p),m=refs(clauses,p);const independent=[];for(let w=0;w<128;w++)if(owners.every(c=>{const vals=c.map(l=>(((w>>(Math.abs(l)-1))&1)^(l<0?1:0)));return vals.some(v=>v===0)&&vals.some(v=>v===1);})){independent.push(w);}check(JSON.stringify(m)===JSON.stringify(independent));check(closed!==null&&m.every(w=>respects(closed,w)));out.fano.push({label,models:m.length});}
  fano(triples,"root");for(let i=0;i<7;i++)for(let j=0;j<3;j++)fano(triples.map((c,a)=>c.map((l,b)=>a===i&&b===j?-l:l)),`flip-${i}-${j}`);
  check(out.fano[0].models===0&&out.fano.slice(1).every(x=>x.models===10));
  return out;
})();
console.log(JSON.stringify(result,null,2));
