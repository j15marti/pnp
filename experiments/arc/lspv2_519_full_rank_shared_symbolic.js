/* LSPV-2/519 standalone independent JavaScript verifier.
   Source-authenticated finite controls only, NOT a native FLMV machine. */
function edges(h) {
  if (h===4) return [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  if (h<6 || h%2) throw Error("bad H");
  const r=h/2,S=new Set();
  for(let layer=0;layer<2;layer++) for(let i=0;i<r;i++) {
    const a=layer*r+i,b=layer*r+((i+1)%r);
    S.add([Math.min(a,b),Math.max(a,b)].join(","));
  }
  for(let i=0;i<r;i++) S.add(i+","+(i+r));
  return [...S].map(s=>s.split(",").map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
}
function make(h,d) {
  const E=edges(h),e=E.length,w=Math.floor(Math.log2(e))+1;
  let bits="10110110"+"1".repeat(e)+"0", clauses=[];
  for(let v=0;v<h;v++) {
    let ids=E.flatMap(([a,b],j)=>a===v||b===v?[j+1]:[]);
    if(ids.length!==3) throw Error("not cubic");
    const c=v===h-1?0:(d>>v)&1;
    for(let p=0;p<=1;p++) for(let q=0;q<=1;q++) {
      let neg=[p,q,1^c^p^q];
      clauses.push(ids.map((id,j)=>neg[j]?-id:id));
      ids.forEach((id,j)=>bits+=String(neg[j])+id.toString(2).padStart(w,"0"));
    }
  }
  return {bits:bits+"01",clauses,E};
}
function decode(bits,h) {
  const E=edges(h),e=E.length,w=Math.floor(Math.log2(e))+1;
  if(typeof bits!=="string" || !/^[01]+$/.test(bits)) return null;
  if(bits.length!==8+e+1+12*h*(w+1)+2) return null;
  if(bits.slice(0,8+e+1)!==("10110110"+"1".repeat(e)+"0")||bits.slice(-2)!=="01")return null;
  let at=8+e+1,d=0;
  for(let v=0;v<h;v++) {
    let ids=E.flatMap(([a,b],j)=>a===v||b===v?[j+1]:[]),charge=null;
    for(let p=0;p<2;p++) for(let q=0;q<2;q++) {
      let neg=[];
      for(let j=0;j<3;j++) {
        neg.push(Number(bits[at++]));
        const id=parseInt(bits.slice(at,at+w),2);at+=w;
        if(id!==ids[j])return null;
      }
      if(neg[0]!==p||neg[1]!==q)return null;
      const c=1^p^q^neg[2];
      if(charge!==null&&charge!==c)return null;
      charge=c;
    }
    if(v===h-1 && charge!==0)return null;
    if(v<h-1)d|=charge<<v;
  }
  return d;
}
function satBrute(C,e) {
  for(let a=0;a<(1<<e);a++) {
    let good=true;
    for(const clause of C) {
      if(!clause.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))){good=false;break;}
    }
    if(good)return true;
  }
  return false;
}
function satGF2(E,h,d) {
  const parent=Array.from({length:h},(_,i)=>i),height=new Array(h).fill(0);
  function root(i){while(parent[i]!==i)i=parent[i]=parent[parent[i]];return i;}
  for(let [a,b] of E){let x=root(a),y=root(b);if(x===y)continue;
    if(height[x]<height[y])[x,y]=[y,x];parent[y]=x;if(height[x]===height[y])height[x]++;
  }
  let syndrome=new Map();
  for(let i=0;i<h;i++){let p=root(i);syndrome.set(p,(syndrome.get(p)||0)^(i<h-1?(d>>i)&1:0));}
  return [...syndrome.values()].every(s=>s===0);
}
function run() {
  let assertions=0,originalCNFs=0,sat=0,unsat=0,bruteCases=0,grayUpdates=0,malformedRejections=0,byH={};
  function check(ok,msg){assertions++;if(!ok)throw Error("assertion: "+msg);}
  for(let h of [4,6,8,10,12]) {
    const k=h-1,q=1<<k,labels=[];
    for(let d=0;d<q;d++) {
      const F=make(h,d),truth=(()=>{let x=d,p=0;while(x){p^=x&1;x>>=1;}return p===0;})();
      check(decode(F.bits,h)===d,"decode "+h+"/"+d);
      check(satGF2(F.E,h,d)===truth,"GF2 "+h+"/"+d);
      if(h<=8){check(satBrute(F.clauses,F.E.length)===truth,"truth table");bruteCases++;}
      labels.push(truth);originalCNFs++;if(truth)sat++;else unsat++;
      if(d===0){
        const offsets=[0,8+F.E.length+1,8+F.E.length+1+2*(Math.floor(Math.log2(F.E.length))+2),F.bits.length-1];
        for(let at of offsets){
          let corrupted=F.bits.slice(0,at)+(F.bits[at]==="0"?"1":"0")+F.bits.slice(at+1);
          check(decode(corrupted,h)===null,"corrupt");malformedRejections++;
        }
        check(decode(F.bits.slice(0,-1),h)===null,"truncate");malformedRejections++;
      }
    }
    const origin=make(h,0).bits,groups=[];
    for(let i=0;i<k;i++){
      const other=make(h,1<<i).bits,changes=[];
      for(let pos=0;pos<origin.length;pos++)if(origin[pos]!==other[pos])changes.push(pos);
      check(changes.length===4,"sign positions");groups.push(changes);
    }
    check(new Set(groups.flat()).size===4*k,"disjoint charge positions");
    const sample=groups.map(g=>g[0]),traces=new Set();
    for(let d=0;d<q;d++){
      const bits=make(h,d).bits;traces.add(sample.map(pos=>bits[pos]).join(""));
    }
    check(traces.size===q,"rank transcript injection");
    const r=Math.min(k,8),stream=1<<r;let last=0,parity=0,graySAT=0;
    for(let i=0;i<stream;i++){
      const desc=i^(i>>1);
      if(i){
        const delta=desc^last;
        check(delta>0&&(delta&(delta-1))===0,"one flip");
        parity^=1;grayUpdates++;
      }
      check((parity===0)===labels[desc],"Gray output");
      graySAT+=(parity===0);last=desc;
    }
    byH[h]={sourceBits:origin.length,k,distinctTraces:traces.size,grayOutputs:stream,graySAT,grayUNSAT:stream-graySAT};
  }
  return {status:"PASS",assertions,originalCNFs,sat,unsat,bruteCases,grayUpdates,malformedRejections,byH,nativeFLMV:"NOT EXECUTED"};
}
if(typeof module!=="undefined")module.exports={run,make,decode};
if(typeof require!=="undefined" && require.main===module) process.stdout.write(JSON.stringify(run(),null,2)+"\n");