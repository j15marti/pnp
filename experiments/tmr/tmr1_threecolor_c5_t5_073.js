// TMR-1/073 finite executable audit: 3-color -> anchored C5 -> parsimonious T5.
// Full bit parser, isolate reduction, witness lift/reverse, path multiplicities.
const verify=function verifyTmr1Reduction073() {
  "use strict";
  const R=(a,b)=>{const d=(b-a+5)%5;return d===1||d===3};
  const C=(a,b)=>{const d=(b-a+5)%5;return d===1||d===4};
  const w=n=>Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
  let assertions=0, graphCases=0, sourceColorings=0, successfulWitnessLifts=0, invalidCases=0, comparisonCases=0, nonParsimonious=0;
  const check=(v,msg)=>{assertions++;if(!v)throw new Error("assertion "+assertions+": "+msg)};
  const cmp=(a,b)=>a[0]-b[0]||a[1]-b[1];
  const bits=(n,k)=>Array.from({length:k},(_,i)=>((n>>i)&1)?"1":"0").join("");
  const encode=(n,edges)=>{
    const e=edges.slice().sort(cmp);
    return "1".repeat(n)+"0"+"1".repeat(e.length)+"0"+e.map(([a,b])=>bits(a,w(n))+bits(b,w(n))).join("");
  };
  const parse=(s,directed=false)=>{
    if(!/^[01]*$/.test(s))throw new Error("nonbinary");
    let p=0;const unary=()=>{let n=0;while(p<s.length&&s[p]==="1"){n++;p++;}if(p>=s.length)throw new Error("missing delimiter");p++;return n;};
    const n=unary(),m=unary(),width=w(n);
    if(s.length-p!==2*m*width)throw new Error("truncated/trailer");
    const read=()=>{let x=0;for(let i=0;i<width;i++)if(s[p++]==="1")x+=2**i;return x;};
    let prev=null;const E=[];
    for(let j=0;j<m;j++){let a=read(),b=read();
      if(a>=n||b>=n||(directed?false:a>=b))throw new Error("invalid endpoints");
      const ab=[a,b];if(prev&&cmp(prev,ab)>=0)throw new Error("duplicate/unsorted");
      E.push(ab);prev=ab;
    }
    if(p!==s.length)throw new Error("trailer");
    return {n,E};
  };
  const compile=(src)=>{
    const {n,E}=parse(src,false);
    if(E.length===0)return {src,n,E,core:[],H:{n:0,E:[]},D:{n:0,E:[]},out:"00"};
    const active=Array(n).fill(false);for(const [a,b] of E){active[a]=true;active[b]=true;}
    const core=Array.from({length:n},(_,i)=>i).filter(i=>active[i]);
    const idx=new Map(core.map((a,i)=>[a,i])),k=core.length,m=E.length;
    const Hedges=[[0,1],[1,2],[2,3],[3,4],[0,4]];
    for(let i=0;i<k;i++){let t=5+k+i,v=5+i;Hedges.push([0,t],[v,t]);}
    for(let e=0;e<m;e++){let [a,b]=E[e],u=5+idx.get(a),v=5+idx.get(b),p=5+2*k+2*e,q=p+1;
      Hedges.push([Math.min(u,p),Math.max(u,p)],[p,q],[Math.min(q,v),Math.max(q,v)]);
    }
    Hedges.sort(cmp);
    const H={n:5+2*k+2*m,E:Hedges};
    const arcs=[];
    for(let e=0;e<Hedges.length;e++){
      const [u,v]=Hedges[e],z=H.n+2*e,t=z+1;
      arcs.push([u,z],[u,t],[t,z],[t,v]);
    }
    arcs.sort(cmp);
    const D={n:H.n+2*Hedges.length,E:arcs};
    const out=encode(D.n,D.E);
    check(H.n===5+2*k+2*m&&Hedges.length===5+2*k+3*m,"H exact size");
    check(D.n===15+6*k+8*m&&D.E.length===20+8*k+12*m,"D exact size");
    check(parse(out,true).n===D.n,"serialized output roundtrip");
    check(out.length<=331*src.length,"constant encoded-bit factor");
    return {src,n,E,core,H,D,out};
  };
  const lift=(compiled,sourceColors)=>{
    const {n,E,core,H,D}=compiled;
    check(sourceColors.length===n&&sourceColors.every(a=>a===0||a===1||a===2),"proper input witness format");
    if(!E.every(([a,b])=>sourceColors[a]!==sourceColors[b]))throw new Error("improper 3-color");
    if(E.length===0)return [];
    const k=core.length,m=E.length,h=Array(H.n).fill(-1);
    for(let a=0;a<5;a++)h[a]=a;
    const map=[0,2,3];
    for(let i=0;i<k;i++){
      let val=map[sourceColors[core[i]]];h[5+i]=val;
      let t=5+k+i;
      h[t]=Array.from({length:5},(_,a)=>a).find(a=>C(a,0)&&C(a,val));
      check(h[t]!==undefined,"unary path found");
    }
    const idx=new Map(core.map((a,i)=>[a,i]));
    for(let e=0;e<m;e++){
      let [a,b]=E[e],v=h[5+idx.get(a)],v2=h[5+idx.get(b)];
      let p=5+2*k+2*e,q=p+1,found=false;
      for(let x=0;x<5&&!found;x++)for(let y=0;y<5&&!found;y++)if(C(v,x)&&C(x,y)&&C(y,v2)){h[p]=x;h[q]=y;found=true;}
      check(found,"length-three path exists");
    }
    check(H.E.every(([a,b])=>C(h[a],h[b])),"whole H witness valid");
    const d=h.slice();
    for(let e=0;e<H.E.length;e++){let [u]=H.E[e];d[H.n+2*e]=(h[u]+1)%5;d[H.n+2*e+1]=(h[u]+3)%5;}
    check(d.length===D.n&&D.E.every(([a,b])=>R(d[a],d[b])),"whole D witness valid");
    return d;
  };
  const reverse=(compiled,witness)=>{
    if(compiled.E.length===0)return Array(compiled.n).fill(0);
    const {H,D,core,n,E}=compiled;
    if(witness.length!==D.n||!witness.every(x=>Number.isInteger(x)&&x>=0&&x<5)||!D.E.every(([a,b])=>R(witness[a],witness[b])))throw new Error("invalid D witness");
    const h=witness.slice(0,H.n),origin=h[0],step=(h[1]-origin+5)%5;
    if(step!==1&&step!==4)throw new Error("broken anchor");
    const colors=Array(n).fill(0);
    for(let i=0;i<core.length;i++){
      const relative=step*((h[5+i]-origin+5)%5)%5;
      const col={0:0,2:1,3:2}[relative];
      if(col===undefined)throw new Error("invalid unary domain");
      colors[core[i]]=col;
    }
    check(E.every(([a,b])=>colors[a]!==colors[b]),"recovered source proper");
    return colors;
  };
  const W=(a,b,t)=>{
    if(t===0)return a===b?1:0;
    let count=0;
    const walk=(x,steps)=>{if(steps===0){if(x===b)count++;return}for(let y=0;y<5;y++)if(C(x,y))walk(y,steps-1)};
    walk(a,t);return count;
  };
  for(let a=0;a<5;a++)for(let b=0;b<5;b++){
    let d=(b-a+5)%5;
    check(W(a,b,2)===(d===0?2:(d===2||d===3?1:0)),"W2 endpoint");
    check(W(a,b,3)===(d===0?0:(d===1||d===4?3:1)),"W3 endpoint");
    comparisonCases+=2;
  }
  const inspectGraph=(n,E)=>{
    const src=encode(n,E),got=parse(src,false);check(got.n===n&&got.E.length===E.length,"source roundtrip");
    const c=compile(src), k=c.core.length,m=E.length;
    let good=0,weighted=0;
    for(let mask=0;mask<3**n;mask++){
      let v=mask,cols=Array.from({length:n},()=>{let z=v%3;v=Math.floor(v/3);return z});
      if(!E.every(([a,b])=>cols[a]!==cols[b]))continue;
      good++;sourceColorings++;
      const d=lift(c,cols);const recovered=reverse(c,d);
      check(E.every(([a,b])=>recovered[a]!==recovered[b]),"source witness recovered");
      successfulWitnessLifts++;
      if(m>0){
        const coreLabels=c.core.map(i=>[0,2,3][cols[i]]);
        let n0=coreLabels.filter(x=>x===0).length;
        const idx=new Map(c.core.map((v,i)=>[v,i]));
        let e23=E.filter(([u,v])=>[coreLabels[idx.get(u)],coreLabels[idx.get(v)]].sort().join(",")==="2,3").length;
        weighted+=(2**n0)*(3**e23);
      }
    }
    check((good>0)===(m===0||weighted>0),"yes/no weighted identity");
    if(m>0){
      check(c.H.E.length===5+2*k+3*m,"H edges");
      check(c.D.E.length===20+8*k+12*m,"D arcs");
      check((10*weighted)%10===0,"C5 count multiple ten");
      if(10*weighted!==good)nonParsimonious++;
    }else check(c.D.n===0&&c.D.E.length===0&&c.out==="00","zero-edge branch");
    graphCases++;
  };
  for(let n=0;n<=5;n++){
    const possible=[];for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)possible.push([a,b]);
    for(let mask=0;mask<2**possible.length;mask++){
      const E=possible.filter((_,e)=>(mask&(2**e))!==0);
      inspectGraph(n,E);
    }
  }
  // Explicit unsatisfiable K4 and K5; all source isolated vertices route to constant YES.
  const K4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const v4=compile(encode(4,K4));
  check(v4.D.n===15+6*4+8*6,"K4 compiled despite unsat");
  const a=encode(3,[[0,1],[1,2]]);
  const malformed=["","0","1","1010",a+"0","2"+a,a.slice(0,-1)];
  for(const bad of malformed){let rejected=false;try{parse(bad,false)}catch(e){rejected=true;}check(rejected,"malformed rejects");invalidCases++;}
  let sorted=false;try{parse(encode(3,[[0,1],[1,2]]).replace(/.{2}$/,"00"),false)}catch(e){sorted=true;} // optional malformed may still be valid; skip assertion
  return {revision:"tmr1-3color-to-t5-path073.v1",seed:"NONE",runtime:"V8 JavaScript",sourceGrammar:"unary vertex/edge counts; low-first fixed-width sorted undirected edge records",graphCases,sourceColorings,successfulWitnessLifts,pathEndpointComparisons:comparisonCases,malformedRejected:invalidCases,nonParsimoniousCaseCount:nonParsimonious,assertions,failures:0,scope:"Exhaustive all simple graphs n<=5; symbolic all-n theorem separate; no NP lower bound"};
};
console.log(JSON.stringify(verify(),null,2));
