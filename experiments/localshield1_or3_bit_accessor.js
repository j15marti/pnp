
// LOCALSHIELD1 record-local four-leaf OR3 reference implementation
function bits(n){return Math.max(1,Math.floor(Math.log2(Math.max(1,n)))+1);}
function gamma(n){const b=n.toString(2);return "0".repeat(b.length-1)+b;}
function enc(n,clauses){let s=gamma(n+1)+gamma(clauses.length+1),w=bits(n);for(const c of clauses)for(const v of c)s+=(v<0?"1":"0")+Math.abs(v).toString(2).padStart(w,"0");return s;}
function source(raw){let probes=0;const probe=(i)=>{if(i<0||i>=raw.length)throw Error("bad source position");probes++;return raw[i];};
  function parse(at){let z=0;while(probe(at+z)==="0")z++;return [parseInt(Array.from({length:z+1},(_,i)=>probe(at+z+i)).join(""),2),at+2*z+1];}
  let [np,pos]=parse(0),[mp,h]=parse(pos),n=np-1,m=mp-1,w=bits(n);
  if(h+3*m*(w+1)!==raw.length)throw Error("bad source length");
  if(m && (n<3||n>3*m))throw Error("bad source dimension");
  if(!m&&n!==0)throw Error("bad empty source");
  return {n,m,w,h,probes:()=>probes,validate(){for(let i=0;i<m;i++)this.record(i);},
   record(i){if(i<0||i>=m)throw Error("record range");const c=[];for(let k=0;k<3;k++){
     const a=h+(i*3+k)*(w+1);const neg=probe(a)==="1";let v=0;
     for(let j=0;j<w;j++)v=2*v+Number(probe(a+1+j));
     if(v<1||v>n)throw Error("bad id");c.push(neg?-v:v);}
     if(new Set(c.map(Math.abs)).size!==3)throw Error("repeated variable");return c;}};}
function leaf(n,m,gen,name){return {n,m,gen,name,offset:0,record(i){if(i<0||i>=m)throw Error("leaf range");return gen(i).map(v=>Math.sign(v)*(Math.abs(v)+this.offset));}};}
function cube(b,name){return leaf(3*b,8*b,j=>{const t=Math.floor(j/8),mask=j%8;return [0,1,2].map(i=>(mask&(1<<i))?-(3*t+i+1):3*t+i+1);},name);}
function prism(r,name){return leaf(3*r,8*r,j=>{const v=Math.floor(j/4),side=Math.floor(v/r),at=v%r,charge=Number(v===0);
  const edge=[side*r+1+(at+r-1)%r,side*r+1+at,2*r+1+at];let seen=0,mask=0;
  for(let x=0;x<8;x++)if((popcount(x)%2)!==charge){if(seen++===j%4){mask=x;break;}}
  return edge.map((id,k)=>(mask&(1<<k))?-id:id);},name);}
function popcount(x){let n=0;while(x){n+=x&1;x>>=1;}return n;}
function node(left,right,name){return {left,right,name,m:2*(left.m+right.m),aux:1+left.m+right.m,selector:0,base:0,
  record(j){if(j<0||j>=this.m)throw Error("node range");if(j<2*left.m){const i=Math.floor(j/2),c=left.record(i),y=this.base+i;
    return j%2===0?[this.selector,c[0],y]:[-y,c[1],c[2]];}
  const jj=j-2*left.m,i=Math.floor(jj/2),c=right.record(i),z=this.base+left.m+i;
  return jj%2===0?[-this.selector,c[0],z]:[-z,c[1],c[2]];}};}
function shield(leaves){if(leaves.length!==4)throw Error("four leaves required");let next=0;
  for(const l of leaves){l.offset=next;next+=l.n;}
  let ll=node(leaves[0],leaves[1],"ll"),rr=node(leaves[2],leaves[3],"rr"),root=node(ll,rr,"root");
  for(const u of [ll,rr,root]){u.selector=next+1;u.base=next+2;next+=u.aux;}
  const V=next,M=root.m,w=bits(V),head=gamma(V+1)+gamma(M+1),length=head.length+3*M*(w+1);
  if(V!==leaves.reduce((s,l)=>s+l.n,0)+3*leaves.reduce((s,l)=>s+l.m,0)+3)throw Error("V identity");
  if(M!==4*leaves.reduce((s,l)=>s+l.m,0))throw Error("M identity");
  return {V,M,w,length,head,root,record(i){return root.record(i);},
    bit(i){if(i<0||i>=length)throw Error("shield bit range");if(i<head.length)return head[i];
      const p=i-head.length,cl=Math.floor(p/(3*(w+1))),off=p%(3*(w+1)),j=Math.floor(off/(w+1)),k=off%(w+1);
      const a=root.record(cl)[j];return k===0?(a<0?"1":"0"):(Math.floor(Math.abs(a)/(2**(w-k)))%2).toString();},
    materialize(){let s=head;for(let j=0;j<M;j++)for(let a of root.record(j))s+=(a<0?"1":"0")+Math.abs(a).toString(2).padStart(w,"0");return s;}};}
function sat(n,C){for(let mask=0;mask<2**n;mask++){let ok=true;for(const c of C){let cOK=false;for(const lit of c){const val=Math.floor(mask/2**(Math.abs(lit)-1))%2;if((lit>0&&val===1)||(lit<0&&val===0)){cOK=true;break;}}if(!cOK){ok=false;break;}}if(ok)return true;}return false;}
function rng(seed){let v=seed>>>0;return ()=>{v=(Math.imul(v,1664525)+1013904223)>>>0;return v/4294967296;};}
function randInt(R,n){return Math.floor(R()*n);}
function tests(){const R=rng(58301),t0=Date.now();let semantics=0,bitTests=0,maxSourceReads=0;let examples=[];
  for(let t=0;t<55;t++){let A=[],B=[],ma=1+randInt(R,3),mb=1+randInt(R,3);
    for(let i=0;i<ma;i++)A.push([1,2,3].map(x=>R()<.5?-x:x));
    for(let i=0;i<mb;i++)B.push([1,2,3].map(x=>R()<.5?-x:x));
    const la=leaf(3,ma,i=>A[i],"A"),lb=leaf(3,mb,i=>B[i],"B");la.offset=0;lb.offset=3;
    const z=node(la,lb,"binary");z.selector=7;z.base=8;
    const cnf=Array.from({length:z.m},(_,i)=>z.record(i));
    if(sat(7+ma+mb,cnf)!==(sat(3,A)||sat(3,B)))throw Error("OR3 semantics failed");
    semantics++;
  }
  for(let t=0;t<45;t++){const n=3+randInt(R,13),m=Math.ceil(n/3)+randInt(R,16);
    let c=[];for(let j=0;j<m;j++){let seen=new Set(),vs=[];while(vs.length<3){let a=1+randInt(R,n);if(!seen.has(a)){seen.add(a);vs.push(R()<.5?-a:a);}}c.push(vs);}
    const packedInput=enc(n,c),src=source(packedInput),meta=src.probes();src.validate();
    const L=leaf(src.n,src.m,i=>src.record(i),"H");
    const F=shield([L,prism(3,"prism-test"),cube(1,"cp-test"),cube(2,"pc-test")]);
    const packedOutput=F.materialize();
    if(packedOutput.length!==F.length)throw Error("length");
    for(let i=0;i<packedOutput.length;i++){if(F.bit(i)!==packedOutput[i])throw Error("bit mismatch at "+i);bitTests++;}
    for(let k=0;k<50;k++){const p=randInt(R,F.length),old=src.probes();F.bit(p);
      const used=src.probes()-old;maxSourceReads=Math.max(maxSourceReads,used);
      if(used>3*(src.w+1))throw Error("full reread");}
    if(t<3)examples.push({H_bits:packedInput.length,shield_bits:F.length,H_m:m,shield_m:F.M,shield_v:F.V,header_probes:meta});
  }
  const big=100003,bigLeaf=leaf(50002,big,i=>{const a=1+(17*i)%50000,b=1+(a+11)%50000,c=1+(b+19)%50000;return [a,-b,c];},"virtual-H");
  const F=shield([bigLeaf,prism(5,"prism-test"),cube(15,"cp-test"),cube(10,"pc-test")]);
  for(let i=0;i<10000;i++){const p=randInt(R,F.length);if(!/[01]/.test(F.bit(p)))throw Error("bad output");}
  return {status:"PASS",binary_OR3_full_truth_cases:semantics,shield_cases:45,exhaustive_compared_output_bits:bitTests,max_source_reads_one_output_bit:maxSourceReads,
    large_virtual_input_clauses:big,large_virtual_output_clauses:F.M,large_virtual_output_variables:F.V,large_virtual_output_bits:F.length,
    large_virtual_random_bit_queries:10000,large_virtual_output_materialized:false,seconds:(Date.now()-t0)/1000,
    tests_only_not_hard_cores:true,examples};}

console.log(JSON.stringify(tests(),null,2));
