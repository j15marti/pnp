"use strict";
/* TMR-1/004 finite indexed-input E_n parser and charged seek-distance audit.
 * Structural/asymptotic TM simulation is proved in the accompanying report.
 * Finite JS Number indexes are deliberately capped at n<=96.
 * No Node dependencies; run with: node experiments/tmr/tmr1_indexed_sequential_bridge004.cjs
 */
function width(n){return Math.max(1,Math.ceil(Math.log2(n)));}
function bits(x,w){return x.toString(2).padStart(w,"0");}
function encode(n,a,b){
  if(n<1||n>96||a.length!==n||b.length!==n)throw Error("unsupported finite test");
  const w=width(5*n); let s="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0";
  for(let side=0;side<2;side++){
    const arr=side===0?a:b;
    for(let i=0;i<n;i++){
      const v=(side===0?n:3*n)+2*i;
      for(const [u,t] of [[0,0],[0,1],[1,0],[1,1]]){
        s+=String(1-arr[i])+bits(i,w)+String(u)+bits(v,w)+String(t)+bits(v+1,w);
      }
    }
  }
  return s;
}
function indexedCheck(x){
  const L=x.length, aw=width(L+2);
  let last=0, reads=0, moves=L, out=false;
  function at(j){
    if(j<0||j>L){out=true;return "#";}
    const dest=Math.min(j,L);
    moves+=Math.abs(dest-last)+1;last=dest;reads++;
    return j===L?"#":x[j];
  }
  function reject(){return {member:false,sat:null,reads,moves,L,addressWidth:aw,indexCostProxy:(L+reads)*(aw+1),sequentialSeekProxy:(moves+L)*(aw+1)};}
  let p=0,N=0;
  while(p<L&&at(p)==="1"){N++;p++;if(N>5*96) return reject();}
  if(N===0||N%5!==0||at(p)!=="0")return reject();
  p++;const n=N/5, M=8*n, w=width(N);
  for(let i=0;i<M;i++){if(at(p++)!=="1")return reject();}
  if(at(p++)!=="0")return reject();
  const bank0=p;let same=true;
  function checkID(v){for(let k=w-1;k>=0;k--){const expected=((v>>k)&1)?"1":"0";if(at(p++)!==expected)return false;}return true;}
  for(let side=0;side<2;side++){
    for(let i=0;i<n;i++){
      const v=(side===0?n:3*n)+2*i;
      let lead=null;
      for(const [u,t] of [[0,0],[0,1],[1,0],[1,1]]){
        const sign=at(p++);
        if(sign!=="0"&&sign!=="1")return reject();
        if(lead===null)lead=sign;
        if(sign!==lead||!checkID(i))return reject();
        if(at(p++)!==String(u)||!checkID(v))return reject();
        if(at(p++)!==String(t)||!checkID(v+1))return reject();
      }
      if(side===1){
        const firstBankSignAddr=bank0+i*12*(1+w);
        if(lead!==at(firstBankSignAddr))same=false;
      }
    }
  }
  if(p!==L||at(p)!=="#")return reject();
  return {member:true,sat:same,reads,moves,L,n,w,addressWidth:aw,
    indexCostProxy:(L+reads)*(aw+1),sequentialSeekProxy:(moves+L)*(aw+1)};
}
function audit(){
  const st={id:"TMR1-IB4",status:"COMPUTATIONAL",model:"finite exact source/index-address emulator, NOT physical TM",allPairs:0,sat:0,unsat:0,malformedRejected:0,encodedBitsChecked:0,indexQueries:0,paidSeekDistance:0,failures:0,maxN:0,samples:[],asymptoticRatios:[]};
  function ok(b,msg){if(!b){st.failures++;throw Error(msg);}}
  for(let n=1;n<=5;n++){
    const z=(1<<n);
    for(let a=0;a<z;a++)for(let b=0;b<z;b++){
      const aa=Array.from({length:n},(_,j)=>(a>>j)&1),bb=Array.from({length:n},(_,j)=>(b>>j)&1);
      const x=encode(n,aa,bb),q=indexedCheck(x);
      ok(q.member&&q.sat===(a===b),"exact indexed SAT/EQ n="+n+" a="+a+" b="+b);
      ok(q.reads<=2*x.length+n+1,"index query count");
      ok(q.moves<=(q.reads+1)*(x.length+1),"seek distance upper");
      ok(q.sequentialSeekProxy<=4*(x.length+2)*(q.addressWidth+1)*(q.indexCostProxy+1),"simulation accounting");
      st.allPairs++;st[q.sat?"sat":"unsat"]++;st.encodedBitsChecked+=x.length;st.indexQueries+=q.reads;st.paidSeekDistance+=q.moves;st.maxN=n;
      if(a===0&&b===0)st.samples.push({n,L:x.length,idx:q.indexCostProxy,seq:q.sequentialSeekProxy,reads:q.reads,seek_moves:q.moves});
    }
    const valid=encode(n,Array(n).fill(0),Array(n).fill(0));
    const mutations=[valid.slice(0,-1),valid+"1","",valid.slice(1),"0",valid.slice(0,valid.indexOf("0")+1)+"0"+valid.slice(valid.indexOf("0")+2)];
    const hd=13*n+2, w=width(5*n);
    const fixedIdBit=hd+1; // first X-variable ID, expected all zero
    mutations.push(valid.slice(0,fixedIdBit)+"1"+valid.slice(fixedIdBit+1));
    const auxSign=hd+(1+w); // first auxiliary sign, expected 0
    mutations.push(valid.slice(0,auxSign)+"1"+valid.slice(auxSign+1));
    for(const y of mutations){ok(!indexedCheck(y).member,"malformed accepted n="+n);st.malformedRejected++;}
  }
  // Deterministic LCG seeded finite controls beyond exhaustive small pairs.
  let state=0x2eab391;
  function randomBit(){state=(Math.imul(state,1664525)+1013904223)>>>0;return(state>>>19)&1;}
  for(const n of [6,8,16,32,64,96])for(let r=0;r<18;r++){
    const a=Array.from({length:n},randomBit),b=r%3===0?a.slice():Array.from({length:n},randomBit);
    const x=encode(n,a,b),q=indexedCheck(x),eq=a.every((v,i)=>v===b[i]);
    ok(q.member&&q.sat===eq,"seeded case "+n+"/"+r);
    st.allPairs++;st[q.sat?"sat":"unsat"]++;st.encodedBitsChecked+=x.length;st.indexQueries+=q.reads;st.paidSeekDistance+=q.moves;st.maxN=n;
    if(r===0)st.samples.push({n,L:x.length,idx:q.indexCostProxy,seq:q.sequentialSeekProxy,reads:q.reads,seek_moves:q.moves});
  }
  // Growth comparison for symbolic O(L log^3 L) indexed product versus Omega(L*n).
  for(let e of [8,12,16,20,24,28,32]){
    const n=2**e,w=width(5*n),L=13*n+2+24*n*(1+w);
    const ell=Math.log2(L+2);
    st.asymptoticRatios.push({n,L,log2L:+ell.toFixed(3),log3OverN:+((ell**3)/n).toPrecision(5)});
  }
  return st;
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
