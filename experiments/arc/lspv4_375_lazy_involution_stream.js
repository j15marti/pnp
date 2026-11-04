// LSPV-4/375: logspace streaming PHP/contradictory-unit involution.
// Dependency-free ES2020 reference; all input bytes are read-only.
// Host test materialization is NOT a measurement of Turing-machine workspace.
"use strict";
function vh(h){return h*(h+1);}
function mh(h){return (h+1)+h*h*(h+1)/2;}
function* php(h){
  const v=vh(h),m=mh(h); yield "p cnf "+v+" "+m+"\n";
  for(let i=1;i<=h+1;i++){for(let j=1;j<=h;j++)yield ((i-1)*h+j)+" ";yield "0\n";}
  for(let j=1;j<=h;j++)for(let i=1;i<=h+1;i++)for(let k=i+1;k<=h+1;k++)
    yield "-"+((i-1)*h+j)+" -"+((k-1)*h+j)+" 0\n";
}
function* easy(h){
  const v=vh(h),m=mh(h);yield "p cnf "+v+" "+m+"\n";yield "1 0\n";yield "-1 0\n";
  let used=0;for(let i=1;i<=v&&used<m-2;i++)for(let j=i+1;j<=v&&used<m-2;j++){
    yield i+" "+j+" 0\n";used++;
  }
  if(used!==m-2)throw Error("insufficient decoy clause count");
}
function boundedLength(h,cap,stats){
  let n=8; for(const generator of [php(h),easy(h)]){
    for(const chunk of generator){n+=chunk.length;if(stats)stats.generated+=chunk.length;
      if(n>cap)return cap+1;
    }
  }
  return n;
}
function locateH(N,stats){
  if(N<1)return null;let low=1, high=N;
  while(low<=high){
    const mid=Math.floor((low+high)/2),size=boundedLength(mid,N,stats);
    if(size===N)return mid;
    if(size<N)low=mid+1; else high=mid-1;
  }
  return null;
}
function* presented(h,which,a,b){
  const target=a+b+8,baseLength=(which==="X"?a:b),padding=target-baseLength-4;
  if(padding<0)throw Error("negative padding");
  yield which==="X"?"c X":"c Y";
  for(let j=0;j<padding;j++)yield " ";
  yield "\n";
  yield* (which==="X"?php(h):easy(h));
}
function countBase(generator){
  let n=0;for(const chunk of generator)n+=chunk.length;return n;
}
function matches(input,generator,stats){
  let off=0;
  for(const chunk of generator)for(let i=0;i<chunk.length;i++){
    if(stats)stats.sourceQueries++;
    if(off>=input.length||input[off]!==chunk.charCodeAt(i))return false;
    off++;
  }
  return off===input.length;
}
function analyze(input,stats){
  const h=locateH(input.length,stats);
  if(h===null)return {h:null,which:null};
  const a=countBase(php(h)),b=countBase(easy(h));
  const X=matches(input,presented(h,"X",a,b),stats);
  if(X)return {h,which:"X",a,b};
  if(matches(input,presented(h,"Y",a,b),stats))return {h,which:"Y",a,b};
  return {h:null,which:null};
}
function streamMap(input,sink,stats){
  const t=analyze(input,stats);
  if(t.h===null){for(let i=0;i<input.length;i++){sink(input[i]);if(stats)stats.outputBits+=8;}
    return "IDENTITY";}
  const dest=t.which==="X"?"Y":"X";
  for(const chunk of presented(t.h,dest,t.a,t.b))for(let i=0;i<chunk.length;i++){
    sink(chunk.charCodeAt(i));if(stats)stats.outputBits+=8;
  }
  return dest;
}
function map(input,stats){let a=[];const mode=streamMap(input,b=>a.push(b),stats);return {bytes:Uint8Array.from(a),mode};}
function lazyByte(input,i,stats){
  if(!Number.isInteger(i)||i<0||i>=input.length)throw Error("out-of-range output index");
  const t=analyze(input,stats);if(t.h===null)return input[i];
  let off=0;const dest=t.which==="X"?"Y":"X";
  for(const chunk of presented(t.h,dest,t.a,t.b)){
    if(i<off+chunk.length){if(stats)stats.virtualOutputReads++;return chunk.charCodeAt(i-off);}
    off+=chunk.length;if(stats)stats.virtualOutputReads+=chunk.length;
  }throw Error("output not found");
}
function asciiBytes(s){let a=new Uint8Array(s.length);for(let i=0;i<s.length;i++)a[i]=s.charCodeAt(i);return a;}
function render(gen){let a="";for(const s of gen)a+=s;return a;}
function equal(a,b){if(a.length!==b.length)return false;for(let i=0;i<a.length;i++)if(a[i]!==b[i])return false;return true;}
function parseAsciiCNF(data){
  const s=String.fromCharCode(...data),lines=s.split("\n");let hdr=null,cls=[];
  for(const line of lines){if(!line.trim())continue;if(line.startsWith("c "))continue;
    const w=line.trim().split(/\s+/);
    if(w[0]==="p"){if(hdr||w.length!==4||w[1]!=="cnf")throw Error("bad header");hdr=[+w[2],+w[3]];continue;}
    if(!hdr||w.at(-1)!=="0")throw Error("bad clause");
    let c=w.slice(0,-1).map(Number);if(!c.length||c.some(z=>!Number.isInteger(z)||z===0||Math.abs(z)>hdr[0]))throw Error("bad literal");
    if(new Set(c).size!==c.length||c.some(z=>c.includes(-z)))throw Error("not proper");
    cls.push(c);
  }
  if(!hdr||hdr[1]!==cls.length)throw Error("bad clause count");
  if(new Set(cls.map(c=>c.join(","))).size!==cls.length)throw Error("duplicate clause");
  return {v:hdr[0],m:hdr[1],clauses:cls};
}
function models(obj){
  if(obj.v>16)throw Error("brute bound");
  let ans=0;for(let a=0;a<(1<<obj.v);a++){
    if(obj.clauses.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))ans++;
  }return ans;
}
function k4Models(charge){
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],rows=[];
  for(let v=0;v<4;v++){const es=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
    for(let a=0;a<8;a++){let bits=[a&1,(a>>1)&1,(a>>2)&1];
      if((bits[0]^bits[1]^bits[2])!==charge[v])rows.push(es.map((e,i)=>bits[i]?-e-1:e+1));
    }
  }
  return models({v:6,m:16,clauses:rows});
}
function runTests(){
  let tests=0,totalBytes=0,originals=0,malformed=0,visits=0,roundtrip=0,maxN=0,lazy=0;
  function check(x,why){tests++;if(!x)throw Error("failed: "+why);}
  for(let h=1;h<=8;h++){
    const a=countBase(php(h)),b=countBase(easy(h));const N=a+b+8;
    check(N>maxN,"increasing lengths");maxN=N;
    const X=asciiBytes(render(presented(h,"X",a,b))),Y=asciiBytes(render(presented(h,"Y",a,b)));
    check(X.length===N&&Y.length===N,"length");
    const x=parseAsciiCNF(X),y=parseAsciiCNF(Y);
    check(x.v===vh(h)&&y.v===vh(h)&&x.m===mh(h)&&y.m===mh(h),"shape");
    if(h<=3){check(models(x)===0,"PHP unsat");check(models(y)===0,"unit unsat");}
    const stat={generated:0,sourceQueries:0,outputBits:0,virtualOutputReads:0};
    const xy=map(X,stat).bytes,yx=map(Y,stat).bytes;
    check(equal(xy,Y)&&equal(yx,X),"forward inverse");
    check(equal(map(xy).bytes,X),"twice involution");
    totalBytes+=N*4;originals+=2;visits+=stat.sourceQueries;roundtrip++;
    for(let pos of [0,1,Math.floor(N/2),N-1]){
      check(lazyByte(X,pos,stat)===Y[pos],"lazy X");
      check(lazyByte(Y,pos,stat)===X[pos],"lazy Y");lazy+=2;
    }
    const tampered=X.slice();tampered[Math.floor(N/2)]^=1;
    check(equal(map(tampered).bytes,tampered),"unrelated modified input identity");
  }
  const misc=["","p cnf 1 1\n1 0\n","p cnf 1 2\n1 0\n","p cnf 1 2\n1 0\n-1 0\n",
    "p cnf 2 1\n1 -2 0\n","c Z\np cnf 2 2\n1 0\n-1 0\n","junk","p cnf 0 0\n"];
  for(const s of misc){const a=asciiBytes(s);check(equal(map(a).bytes,a),"identity other");malformed++;}
  for(const a of [Uint8Array.from([0xff,0x00,1]),Uint8Array.from([0,255,12,10])]){
    check(equal(map(a).bytes,a),"binary identity");malformed++;
  }
  check(k4Models([1,0,0,0])===0,"odd K4");check(k4Models([0,0,0,0])===8,"even K4");
  return {tests,originals,roundtrip,lazy,malformed,parityOdd:0,parityEven:8,totalBytes,
    maxN,sourceComparisons:visits,algorithm:"logspace generated CNF involution",status:"FINITE COMPUTATIONAL"};
}

// For standalone Node: node -e "const fs=require('fs');const src=fs.readFileSync(process.argv[1],'utf8');console.log(JSON.stringify((new Function(src+'\\nreturn runTests;'))(),null,2));" experiments/arc/lspv4_375_lazy_involution_stream.js
