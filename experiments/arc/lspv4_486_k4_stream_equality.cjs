"use strict";
// LSPV-4/486. Pure-JavaScript independent replay of original strict signed 3-CNF sources.
// Run with node experiments/arc/lspv4_486_k4_stream_equality.cjs
const run486 = function run486(){
  let checks=0, negative=0, rows=[];
  function ok(b,msg){if(!b)throw Error("FAIL "+msg);checks++;}
  function bits(n,w){return Array.from({length:w},(_,i)=>(n>>i)&1);}
  function g(w){const b=w.toString(2);return "0".repeat(b.length-1)+b;}
  const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  function eid(j,u,v){const a=Math.min(u,v),b=Math.max(u,v);return 6*j+E.findIndex(z=>z[0]===a&&z[1]===b)+1;}
  function make(w,a,b){
    const clauses=[], groups=[];
    for(let v=0;v<4;v++) for(let j=0;j<w;j++){
      const ids=Array.from({length:4},(_,k)=>k).filter(k=>k!==v).map(k=>eid(j,v,k));
      const cs=[];
      for(let z=0;z<8;z++){let pat=[(z>>2)&1,(z>>1)&1,z&1];
        const bad=(v<2 ? pat[0] !== (v===0?a[j]:b[j]) : (pat[0]^pat[1]^pat[2])!==0);
        if(bad)cs.push(ids.map((id,k)=>pat[k]===1?-id:id));
      }
      if(cs.length!==4)throw Error("not 4");
      groups.push(cs);clauses.push(...cs);
    }
    const L=(6*w).toString(2).length;
    const source=g(w)+clauses.flat().map(x=>(x<0?"1":"0")+Math.abs(x).toString(2).padStart(L,"0")).join("");
    return {source,clauses,groups,L};
  }
  function decode(s){
    if(typeof s!=="string"||!/^[01]+$/.test(s))throw Error("alphabet");
    let z=0;while(z<s.length&&s[z]==="0")z++;
    if(z>=s.length||z>20)throw Error("gamma");
    const b=z+1;
    if(s.length<z+b)throw Error("truncated gamma");
    const w=parseInt(s.slice(z,z+b),2);
    if(w<1||w>1024)throw Error("w");
    const L=(6*w).toString(2).length;
    if(s.length!==(2*b-1)+48*w*(L+1))throw Error("length");
    let cursor=2*b-1;const clauses=[];
    for(let k=0;k<16*w;k++){
      const c=[];
      for(let j=0;j<3;j++){
        let neg=s[cursor]==="1";cursor++;
        let id=parseInt(s.slice(cursor,cursor+L),2);cursor+=L;
        if(id<1||id>6*w)throw Error("id");
        c.push(neg?-id:id);
      }
      if(new Set(c.map(Math.abs)).size!==3)throw Error("repeat");
      clauses.push(c);
    }
    const aa=[],bb=[];
    for(let j=0;j<w;j++){
      aa.push(clauses[4*j][0]>0?1:0);
      bb.push(clauses[4*(w+j)][0]>0?1:0);
    }
    if(make(w,aa,bb).source!==s)throw Error("out-of-family");
    return {w,aa,bb,clauses};
  }
  function satcount(clauses,m){let n=0;for(let mask=0;mask<(1<<m);mask++){
    let yes=true;for(const c of clauses){let holds=false;
      for(const l of c){let bit=(mask>> (Math.abs(l)-1))&1;if(bit===(l>0?1:0)){holds=true;break;}}
      if(!holds){yes=false;break;}
    }if(yes)n++;
  }return n;}
  for(let w=1;w<=2;w++){
    const sources=new Set();
    for(let x=0;x<(1<<w);x++) for(let y=0;y<(1<<w);y++){
      const a=bits(x,w),b=bits(y,w),m=make(w,a,b),r=decode(m.source);
      ok(m.clauses.length===16*w,"clause count");ok(m.source.length===(2*w.toString(2).length-1)+48*w*(m.L+1),"source length");
      ok(m.clauses.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"proper signed triples");
      ok(r.aa.join("")===a.join("")&&r.bb.join("")===b.join(""),"recover A,B");
      const cnt=satcount(r.clauses,6*w),expected=(x===y)?8**w:0;
      ok(cnt===expected,"model count "+w+"/"+x+"/"+y);ok(!sources.has(m.source),"collision");
      sources.add(m.source);rows.push({w,a:a.join(""),b:b.join(""),N:m.source.length,models:cnt,source_bits:m.source});
    }
    ok(sources.size===(1<<(2*w)),"distinct sources");
    const truth=Array.from({length:1<<w},(_,x)=>Array.from({length:1<<w},(_,y)=>+(x===y)).join(""));
    ok(new Set(truth).size===(1<<w),"distinct communication rows");
  }
  for(const w of [3,4,8,16]){
    const cases=[[0,0],[0,1],[(1<<w)-1,(1<<w)-1],[(1<<w)-1,0]];
    for(const [x,y]of cases){
      const a=bits(x,w),b=bits(y,w),m=make(w,a,b),r=decode(m.source);
      ok(r.w===w&&r.aa.join("")===a.join(""),"larger decode");
      ok(m.source.length===(2*w.toString(2).length-1)+48*w*(m.L+1),"larger N");
      rows.push({w,a:a.join(""),b:b.join(""),N:m.source.length,models:x===y?"8^w by proved product":"0 by proved product"});
    }
  }
  const canonical=make(2,[0,1],[0,1]);let tests=[
    canonical.source.slice(0,-1),
    canonical.source.slice(0,1)+("0"===canonical.source[1]?"1":"0")+canonical.source.slice(2),
    canonical.source.slice(0,8)+"2"+canonical.source.slice(9),
    "0".repeat(50)
  ];
  for(let i=0;i<tests.length;i++){let rejected=false;try{decode(tests[i]);}catch(e){rejected=true;}ok(rejected,"negative "+i);negative++;}
  // A sign-bit mutation inside parity packet retains valid literal shape but must fail family authentication.
  let t=canonical.source.split("");const z=2*2-1,L=canonical.L,offset=z+4*(2*2)*(3*(L+1));t[offset]=t[offset]==="0"?"1":"0";
  let rejected=false;try{decode(t.join(""));}catch(e){rejected=true;}
  ok(rejected,"valid triple wrong packet");negative++;
  return {status:"PASS",checks,negative_controls:negative,exhaustive_original_sources:20,larger_structural_sources:16,rows,scope:"exact finite original signed strict 3CNF controls; not FLMV native timing",theorem:"Deterministic p full-scan, state S: (2p-1)(S+O(log N)) >= w"};
};
const result=run486();
if (typeof console !== "undefined") console.log(JSON.stringify(result, null, 2));
