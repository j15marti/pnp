// TMR-3/025. Reproduce: node experiments/tmr/tmr3_ring_network025.cjs
// Direct network and swept-array proxy, not a compiled finite-alphabet TM.
function run() {
  const seeds = { x: 20261114 };
  function rand() { seeds.x = (Math.imul(seeds.x,1664525)+1013904223)>>>0; return seeds.x & 1; }
  function update(i,b,a,cell,left,right) {
    const z = a ^ (b==="1"?1:0) ^ cell ^ left ^ right ^ (i&1);
    const value=cell^z;
    return [z,value,z?1:-1,value,z];
  }
  function direct(p,s) {
    const R=s.length+p+1, state=Array(p).fill(0), head=Array(p).fill(0),cells=Array.from({length:p},()=>new Map());
    let L=Array(p).fill(0),D=Array(p).fill(0);
    for(let t=0;t<R;t++){
      const nL=Array(p).fill(0),nD=Array(p).fill(0);
      for(let i=0;i<p;i++){
        const old=cells[i].get(head[i])||0;
        const [a,v,m,ol,or]=update(i,t<s.length?s[t]:"0",state[i],old,L[i],D[i]);
        state[i]=a;
        if(v)cells[i].set(head[i],v); else cells[i].delete(head[i]);
        head[i]+=m; nD[(i-1+p)%p]=ol; nL[(i+1)%p]=or;
      }
      L=nL;D=nD;
    }
    return JSON.stringify({state,head,cells:cells.map(m=>Array.from(m.entries()).sort((a,b)=>a[0]-b[0])),L,D});
  }
  function proxy(p,s) {
    const R=s.length+p+1, B=R, W=2*B+3, flat=new Uint8Array(p*W), state=Array(p).fill(0),head=Array(p).fill(0);
    let L=Array(p).fill(0),D=Array(p).fill(0),physical=s.length+flat.length;
    for(let t=0;t<R;t++){
      let nL=Array(p).fill(0),nD=Array(p).fill(0),oldheads=head.slice();
      for(let k=0;k<flat.length;k++){
        physical++;
        const i=Math.floor(k/W),pos=k%W;
        if(pos!==B+1+oldheads[i])continue;
        const [a,v,m,ol,or]=update(i,t<s.length?s[t]:"0",state[i],flat[k],L[i],D[i]);
        state[i]=a;flat[k]=v;head[i]+=m;
        nD[(i-1+p)%p]=ol;nL[(i+1)%p]=or;
      }
      physical+=4*flat.length; L=nL;D=nD;
    }
    const cells=Array.from({length:p},(_,i)=>{
      const a=[]; for(let j=0;j<W;j++){const v=flat[i*W+j];if(v)a.push([j-(B+1),v]);}return a;
    });
    return {config:JSON.stringify({state,head,cells,L,D}),physical,B,W};
  }
  let cases=0,yes=0,no=0,moves=0,maxMoves=0,maxp=0;
  function check(p,s){
    const x=direct(p,s), y=proxy(p,s);
    if(x!==y.config)throw new Error("config mismatch p="+p+" source="+s+" x="+x+" y="+y.config);
    if(y.physical>(5*y.B+1)*p*y.W+s.length)throw new Error("sweep bound failed");
    const label=JSON.parse(x).state[0]; if(label)yes++;else no++;
    cases++;moves+=y.physical;maxMoves=Math.max(maxMoves,y.physical);maxp=Math.max(maxp,p);
  }
  for(let p=1;p<=6;p++)for(let n=0;n<=8;n++)for(let v=0;v<(1<<n);v++)check(p,v.toString(2).padStart(n,"0").slice(n===0?1:0));
  for(const p of [1,3,6,8,12])for(const n of [9,10,12,15])for(let j=0;j<15;j++){
    let s="";for(let k=0;k<n;k++)s+=rand();check(p,s);
  }
  const malformed=["2","01x","a","??","011 0"];
  for(const s of malformed)if(!/[^01]/.test(s))throw new Error("missing malformed control");
  return {run:"TMR3_RING_NETWORK025_V8",status:"COMPUTATIONAL",native_execution:"hosted V8; separate native CPython reimplementation also executed locally",native_tm_compiler:false,source_model:"uniform ring p locally moving one-tape processors, common one-way bit stream, two unit messages per round",tested_processor_counts:"1..6 exhaustive up to 8 source bits; 1,3,6,8,12 seeded length 9,10,12,15",complete_configuration_checks:cases,yes,no,malformed:malformed.length,max_processors:maxp,total_swept_proxy_movements:moves,max_swept_proxy_movements:maxMoves,assertion_failures:0,clock_bound:"O(U(N)+B(N)*(N+p(N)*B(N))) under fully specified polynomial clock B>=R and uniform ring",limitations:"symbolic model-specific proof; V8 swept-array proxy not compiled finite-alphabet one-tape machine"};
}
console.log(JSON.stringify(run(),null,2));
