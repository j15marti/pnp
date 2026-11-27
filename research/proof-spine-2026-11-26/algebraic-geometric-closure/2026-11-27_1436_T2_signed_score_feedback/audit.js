
function run(compiler,corpus,registry,helper,prior,peerJ,peerR){
const compile=Function(compiler.slice(compiler.indexOf("function compile"),compiler.indexOf("function auditLocal"))+";return compile")();
const H=Function(helper.slice(0,helper.indexOf("function runCase"))+";return {sha,normalize,independentNormalize,eliminate,verifyTrace}")();
const P=Function(prior.slice(0,prior.indexOf('if(typeof module')).replace('const cap=200000;','const cap=1000000;').replace('const B=JSON.parse(corpus),R=JSON.parse(registry),result=[];', 'return {vars,restrict,budget,gac,alg,binary,bucket,dag,order,makeGuards,cnfTables,portMap,replayPeer,test}; const B=JSON.parse(corpus),R=JSON.parse(registry),result=[];')+";return engine")()(compiler,corpus,registry,helper);
const budget=(max=1000000)=>({n:0,add(k=1){this.n+=k;if(this.n>max)throw Error("cap")}});
const top=x=>x.toString(2).length-1,bit=(x,i)=>Number(x>>BigInt(i)&1n),hash=x=>H.sha(JSON.stringify(x)+"\n");
function space(F){
 const V=P.vars(F),n=V.length,I=[[],...V.map(v=>[v])],M=new Map([["",0],...V.map((v,i)=>[String(v),i+1])]);
 for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){M.set(V[i]+","+V[j],I.length);I.push([V[i],V[j]])}
 const mon=a=>1n<<BigInt(M.get([...new Set(a)].sort((x,y)=>x-y).join(",")));
 const loc=f=>[[],...f.vs.map(v=>[v]),...f.vs.flatMap((v,i)=>f.vs.slice(i+1).map(w=>[v,w]))];
 const value=(f,w,a)=>a.every(v=>w>>f.vs.indexOf(v)&1);
 return{V,n,I,mon,loc,value}
}
function discovery(F0,guard,B,feedback=true){
 const F=P.restrict(F0,new Map(guard)),{V,n,I,mon,loc,value}=space(F);
 const R=new Map(),done=new Set(),trace=[];let round=0,del=0,lifts=0,eqs=0,checks=0;
 function reduce(x,S){while(x){let p=top(x);B.add();if(!S.has(p))break;x^=S.get(p)}return x}
 function add(x){x=reduce(x,R);if(x)R.set(top(x),x)}
 function local(f){if(!f.ok.length){add(1n);return}const M=loc(f),E=new Map();
  for(let i=0;i<M.length;i++){let e=0n,q=1n<<BigInt(i);for(let j=0;j<f.ok.length;j++){B.add();if(value(f,f.ok[j],M[i]))e|=1n<<BigInt(j)}
   while(e){let k=top(e);B.add();if(!E.has(k)){E.set(k,[e,q]);break}e^=E.get(k)[0];q^=E.get(k)[1]}
   if(!e){let row=0n;for(let k=0;k<M.length;k++)if(bit(q,k))row^=mon(M[k]);add(row);eqs++}
  }
 }
 function consistent(f,w){let T=new Map();for(let a of loc(f).slice(1)){let y=reduce(mon(a)^(value(f,w,a)?1n:0n),R);y=reduce(y,T);if(y===1n)return false;if(y)T.set(top(y),y)}return true}
 const out=no=>({no,rank:R.size,round,del,lifts,eqs,checks,trace,remaining:F.reduce((s,f)=>s+f.ok.length,0)});
 for(;;){round++;for(let f of F)local(f);if(R.has(0))return out(true);
  for(;;){let ch=false;for(let[p,row]of [...R])if(p>0&&p<=n&&!done.has(String(row))){done.add(String(row));ch=true;
    for(let v of V){let prod=0n;for(let i=0;i<=n;i++)if(bit(row,i)){prod^=mon([...I[i],v]);B.add()}add(prod);lifts++}}
   if(R.has(0))return out(true);if(!ch)break}
  if(!feedback)return out(false);
  let ch=false;for(let f of F){let keep=[];for(let w of f.ok){checks++;if(consistent(f,w))keep.push(w);else{ch=true;del++;trace.push([round,f.id,w])}}f.ok=keep;if(!keep.length)return out(true)}if(!ch)return out(false);
 }
}
// independent checker: local row kernel, fresh span per round, full augmented elimination
function replay(F0,guard,rec,B){
 const pins=new Map(guard);
 const F=F0.map(f=>{const vs=f.vs.filter(v=>!pins.has(v)),ok=[];for(const w of f.ok){B.add();if(f.vs.some((v,i)=>pins.has(v)&&pins.get(v)!==(w>>i&1)))continue;let z=0;vs.forEach((v,i)=>z|=(w>>f.vs.indexOf(v)&1)<<i);if(!ok.includes(z))ok.push(z)}return{...f,vs,ok}});
 const {V,n,I,mon,loc,value}=space(F);
 const add=(R,x)=>{while(x){const p=top(x);B.add();if(!R.has(p)){R.set(p,x);return true}x^=R.get(p)}return false};
 const current=()=>{const R=new Map(),done=new Set();
   for(const f of F){if(!f.ok.length){add(R,1n);continue}const M=loc(f),L=new Map();
    for(const w of f.ok){let row=0n;for(let i=0;i<M.length;i++){B.add();if(value(f,w,M[i]))row|=1n<<BigInt(i)}add(L,row)}
    for(let i=0;i<M.length;i++)if(!L.has(i)){let q=1n<<BigInt(i);for(const p of [...L.keys()].sort((a,b)=>a-b)){let z=q&L.get(p),par=0;while(z){z&=z-1n;par^=1;B.add()}if(par)q|=1n<<BigInt(p)}
      let poly=0n;for(let j=0;j<M.length;j++)if(bit(q,j))poly^=mon(M[j]);for(const w of f.ok){let p=0;for(let j=0;j<M.length;j++)if(bit(q,j)&&value(f,w,M[j]))p^=1;B.add();if(p)throw Error("local kernel")};add(R,poly)}
   }
   for(;;){let change=false;for(const [p,row] of [...R])if(p>0&&p<=n&&!done.has(String(row))){done.add(String(row));change=true;
     for(const v of V){let prod=0n;for(let i=0;i<=n;i++)if(bit(row,i)){prod^=mon([...I[i],v]);B.add()}add(R,prod)}}
    if(!change||R.has(0))break}
   return R
 };
 let verified=0;
 for(let round=1;round<=rec.round;round++){
  const R=current();if(R.has(0)){if(!rec.no)throw Error("replay stronger contradiction");return{no:true,verified,F}}
  for(const [,id,w] of rec.trace.filter(z=>z[0]===round)){
   const f=F.find(g=>g.id===id);if(!f||!f.ok.includes(w))throw Error("row not present");
   const T=new Map(R);for(const a of loc(f).slice(1))add(T,mon(a)^(value(f,w,a)?1n:0n));
   if(!T.has(0))throw Error("not a verified row deletion");
   f.ok=f.ok.filter(z=>z!==w);verified++;
  }
  if(F.some(f=>!f.ok.length)){if(!rec.no)throw Error("unreported contradiction");return{no:true,verified,F}}
 }
 if(rec.no){const R=current();if(!R.has(0))throw Error("missing final contradiction")}
 return{no:rec.no,verified,F}
}
function execute(F,guards,hybrid=false){
 let B=budget(),S=budget(3000000),out=[];
 for(const g of guards){let rec,stat;try{rec=discovery(F,g,B,true)}catch(e){out.push({guard:g,status:"UNKNOWN "+e,events:B.n});continue}
  try{stat=replay(F,g,rec,S)}catch(e){out.push({guard:g,rec,check_error:String(e)});continue}
  const q={guard:g,rec,check:{verified:stat.verified,events:S.n,no:stat.no}};
  if(hybrid&&!rec.no){const o=P.budget(),cl=P.gac(stat.F,new Map(),o);q.reclosure={no:cl.no,events:o.n,pins:[...cl.A]};q.post=P.test(stat.F,[[]]).map(l=>({method:l.method,events:l.events,no:l.out[0]?.no===true}))}
  out.push(q)
 }return{out,events:B.n,checkEvents:S.n}
}
const C=JSON.parse(corpus),Reg=JSON.parse(registry),result=[];
if(H.sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||H.sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("sha");
let controls=0;
for(let signs=0;signs<16;signs++)for(let w=0;w<16;w++){let b=[],q=0;for(let i=0;i<4;i++){let x=w>>i&1,v=(signs>>i&1)?x-1:x;b.push(v*v);q+=v*v}let e1=b.reduce((s,x)=>s^x,0),e2=0;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)e2^=b[i]*b[j];if((q===2)!==(e1===0&&e2===1))throw Error("score");controls++}
for(let signs=0;signs<8;signs++)for(let w=0;w<8;w++){let b=Array.from({length:3},(_,i)=>{let x=w>>i&1,v=signs>>i&1?x-1:x;return v*v}),q=b.reduce((a,c)=>a+c,0),p=b[0]^b[1]^b[2],t=b[0]*b[1]^b[0]*b[2]^b[1]*b[2];if((q>0)!==Boolean(p||t))throw Error("clause");controls++}
const hostile=Array.from({length:8},(_,i)=>({id:i,vs:[1,2,3],ok:Array.from({length:8},(_,w)=>w).filter(w=>w!==i)}));
const hostileRec=discovery(hostile,[],budget(),true);if(hostileRec.no||hostileRec.del!==0)throw Error("hostile");
for(const name of ["JOINT-24","RANDOM-3CNF-40"]){
 const x=C.instances.find(i=>i.id===name),e=Reg.instances.find(i=>i.alias==="EB-"+name),G=compile(x),s=JSON.stringify(G.network)+"\n",m=JSON.stringify(G.source_map)+"\n";
 if(H.sha(s)!==e.sha256||s.length*8!==e.N_bits||H.sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits||H.sha(m)!==e.source_map_sha256)throw Error("identity "+name);
 const D=H.normalize(G.network),I=H.independentNormalize(G.network);if(JSON.stringify(D.fs)!==JSON.stringify(I.fs))throw Error("normalize");
 let pre=P.budget(),init=P.gac(D.fs,new Map(),pre),E=H.eliminate(D.fs,true),Z=H.verifyTrace(I.fs,E.trace);if(JSON.stringify(E.fs)!==JSON.stringify(Z.fs))throw Error("projection");
 const F=Z.fs,g=P.makeGuards(F),clB=P.budget(),cl=P.gac(F,new Map(),clB);
 const baseline=P.test(F,g),source=execute(F,g,true),cnfF=P.cnfTables(x),cnf=execute(cnfF,P.makeGuards(cnfF),false);
 const peers=[{name:"JOINT-24",hash:"45253de6765bc5584ef313e95dc0328f9fa805314dbfb730936f5d95135df655",bytes:peerJ},{name:"RANDOM-3CNF-40",hash:"69c62f8bcf0da083649520a0ff8f3f643f66b4e4867a7ccc261f5b73e7c9ff9a",bytes:peerR}];
 let imported=P.replayPeer(G.network,I.fs,peers.find(p=>p.name===name),e),V=new Set(P.vars(F)),Q=F.slice(),imports=[];
 for(const f of imported.imports.filter(f=>f.vs.every(v=>V.has(v)))){Q.push(f);let b=P.budget(),z=P.gac(Q,new Map(),b);imports.push({f,closureEvents:b.n,closureNo:z.no,pins:[...z.A]})}
 const cooperative=execute(Q,g,true);
 const {R,D:phase}=P.portMap(G.network);
 const guards=g.map(a=>{const ports=a.map(([v,b])=>[v-1,b]);for(const [v,b]of ports)if(R[v]!==v||phase[v]!==0)throw Error("representative");return{ports,guard_id:"GUARD-v1:sha256:"+hash(["PNP-GUARD-v1",e.instance_id,"EB-PORT-PINS-v1",hash(ports)])}});
 const map={schema:"PORT-REP-PHASE-PROJECTION-v1",R:Array.from(R),phase:Array.from(phase),trace:E.trace};
 const mapHash=hash(map),tableHash=hash(F);
 for(let i=0;i<guards.length;i++){const r=P.restrict(F,new Map(g[i]));guards[i].tableHash=hash(r);guards[i].residual_id="RESIDUAL-v1:sha256:"+hash(["PNP-RESIDUAL-v1",e.instance_id,guards[i].guard_id,"T2-SCORE-TABLE-v1",hash(r),mapHash])}
 result.push({name,problem_id:"STRICT-EB4-v1",instance:e.short_id,instance_id:e.instance_id,N:e.N_bits,cnf:e.source_cnf,source_pin:"registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c; corpus e315349cd6c1fe3fa696504859f28312f6aab69a; compiler 21b9d53fb8166c819b24e708656c742cd3c24f10",guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1]},rootFactors:D.fs.length,normalizedCarriers:D.roots,projection:{count:E.trace.length,checks:E.checks,scans:E.scans,verify:Z.tests,verifyScans:Z.scans,mapHash,tableHash},remainingCarriers:P.vars(F).length,initial:{events:pre.n,no:init.no,pins:[...init.A]},closure:{events:clB.n,no:cl.no,pins:[...cl.A]},guards,baseline,source,cnf,peer:{hash:imported.hash,checks:imported.results,imports},cooperative})
}
return{controls,hostile:{no:hostileRec.no,del:hostileRec.del,rank:hostileRec.rank},result}
}
if(typeof module!=="undefined"){module.exports=run;if(require.main===module){const fs=require("fs");const a=process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"));console.log(JSON.stringify(run(...a),null,2))}}
