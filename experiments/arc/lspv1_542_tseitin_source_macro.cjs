const mkGraph = function(kind, k=4) {
 let h,edges=[];
 if(kind==="K4"){h=4;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);}
 else if(kind==="K33"){h=6;for(let i=0;i<3;i++)for(let j=3;j<6;j++)edges.push([i,j]);}
 else if(kind==="cube"){h=8;for(let i=0;i<8;i++)for(let b=0;b<3;b++){let j=i^(1<<b);if(i<j)edges.push([i,j]);}}
 else if(kind==="petersen"){h=10;for(let i=0;i<5;i++){let add=(a,b)=>edges.push(a<b?[a,b]:[b,a]);add(i,(i+1)%5);add(5+i,5+(i+2)%5);add(i,5+i);}}
 else if(kind==="prism"){h=2*k;for(let i=0;i<k;i++){let add=(a,b)=>edges.push(a<b?[a,b]:[b,a]);add(i,(i+1)%k);add(k+i,k+(i+1)%k);add(i,k+i);}}
 else throw Error("bad graph");
 edges.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 return {h,edges};
};

const gen = function(g,charges){
 const n=g.edges.length, inc=Array.from({length:g.h},()=>[]);
 g.edges.forEach(([a,b],j)=>{inc[a].push(j+1);inc[b].push(j+1)});
 const clauses=[];
 for(let v=0;v<g.h;v++)for(let mask=0;mask<8;mask++)if(((mask.toString(2).split("1").length-1)&1)!==charges[v]){
  const t=inc[v].slice().sort((a,b)=>a-b);
  clauses.push(t.map((x,i)=>(mask>>i&1)?-x:x));
 }
 return {src:`p cnf ${n} ${clauses.length}\n`+clauses.map(c=>c.join(" ")+" 0").join("\n")+"\n",witness:{edges:g.edges,charges,source_ids:Array.from({length:clauses.length},(_,i)=>i+1)},n,m:clauses.length};
};

const parse = function(src){
 const lines=src.trim().split(/\r?\n/);
 const header=lines.shift().trim().split(/\s+/);
 if(header.length!==4||header[0]!=="p"||header[1]!=="cnf"||!(/^\d+$/.test(header[2]))||!(/^\d+$/.test(header[3])))throw Error("header");
 const n=Number(header[2]),m=Number(header[3]);
 if(!Number.isSafeInteger(n)||!Number.isSafeInteger(m)||lines.length!==m)throw Error("count");
 const clauses=lines.map(l=>{const ts=l.trim().split(/\s+/);if(ts.length!==4||ts[3]!=="0")throw Error("termination");const c=ts.slice(0,3).map(x=>Number(x));if(c.some(x=>!Number.isSafeInteger(x)||x===0||Math.abs(x)>n)||new Set(c.map(x=>Math.abs(x))).size!==3)throw Error("literal");return c;});
 return {n,m,clauses};
};

const certify = function(src,w){
 const p=parse(src),h=w.charges.length,n=w.edges.length;
 if(h<4||h%2!==0||n*2!==h*3||p.n!==n||p.m!==4*h)throw Error("shape");
 if(w.source_ids.length!==p.m||w.source_ids.some((x,i)=>x!==i+1))throw Error("source IDs");
 const inc=Array.from({length:h},()=>[]);
 let names=new Set(), pairs=new Set();
 for(let i=0;i<n;i++){const e=w.edges[i];if(!Array.isArray(e)||e.length!==2)throw Error("edge");let [a,b]=e;if(!Number.isInteger(a)||!Number.isInteger(b)||a<0||b>=h||a>=b)throw Error("edge endpoints");let key=a+","+b;if(pairs.has(key))throw Error("parallel edge");pairs.add(key);inc[a].push(i+1);inc[b].push(i+1);}
 if(inc.some(x=>x.length!==3)||w.charges.some(x=>x!==0&&x!==1))throw Error("degree or charge");
 const seen=new Set([0]),work=[0];
 while(work.length){let v=work.pop();for(let [a,b] of w.edges){let u=a===v?b:(b===v?a:-1);if(u!==-1&&!seen.has(u)){seen.add(u);work.push(u)}}}
 if(seen.size!==h)throw Error("disconnected");
 const norm=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
 const actual=p.clauses.map(norm).sort();
 const expected=[];
 for(let v=0;v<h;v++){
  const t=inc[v].slice().sort((a,b)=>a-b);
  for(let mask=0;mask<8;mask++) {
   const parity=((mask>>0)&1)^((mask>>1)&1)^((mask>>2)&1);
   if(parity!==w.charges[v])expected.push(norm(t.map((x,i)=>((mask>>i)&1)?-x:x)));
  }
 }
 expected.sort();
 if(expected.length!==actual.length||expected.some((x,i)=>x!==actual[i]))throw Error("source mismatch");
 const charge=w.charges.reduce((a,b)=>a^b,0);
 if(charge!==1)throw Error("even charge; no contradiction");
 return {ok:true,p:n,h,m:p.m,reason:"sum of all vertex GF(2) equations gives 0=1",paid_nodes:1,logical_weight:1,source_footprint:p.m};
};

const models = function(src){
 const {n,clauses}=parse(src);
 if(n>15)return null;
 let count=0;
 for(let a=0;a<1<<n;a++){
  if(clauses.every(c=>c.some(l=>{let v=(a>>(Math.abs(l)-1))&1;return l>0?v:!v})))count++;
 }
 return count;
};

const tests = function(){
 let checks=0,err=0,samples=[];
 function check(x,msg){checks++;if(!x){err++;throw Error(msg)}}
 function rejected(f,msg){let rejected=false;try{f()}catch(e){rejected=true;}check(rejected,msg)}
 const cases=[["K4"],["K33"],["cube"],["petersen"],["prism",6],["prism",8]];
 for(const [kind,k] of cases){
  let g=mkGraph(kind,k),charges=Array(g.h).fill(0);charges[0]=1;
  let a=gen(g,charges),v=certify(a.src,a.witness);
  check(v.ok&&v.p===g.edges.length&&v.m===4*g.h,"odd valid "+kind);
  check(models(a.src)===0||models(a.src)===null,"unsat odd "+kind);
  let even=gen(g,Array(g.h).fill(0));rejected(()=>certify(even.src,even.witness),"even rejected");
  if(models(even.src)!==null)check(models(even.src)===2**(g.edges.length-g.h+1),"even model count");
  let bad={...a.witness,charges:[...a.witness.charges]};bad.charges[0]=0;
  rejected(()=>certify(a.src,bad),"charge forgery");
  let badIds={...a.witness,source_ids:a.witness.source_ids.slice(1)};
  rejected(()=>certify(a.src,badIds),"provenance forgery");
  let lines=a.src.trim().split("\n");lines[1]=lines[1].replace(/^(-?\d+)/, x=>String(-Number(x)));
  rejected(()=>certify(lines.join("\n")+"\n",a.witness),"changed source literal");
  let lineDelete=a.src.trim().split("\n");lineDelete.pop();
  rejected(()=>certify(lineDelete.join("\n")+"\n",a.witness),"source omitted");
  let parallel={...a.witness,edges:a.witness.edges.map(x=>x.slice())};parallel.edges[0]=parallel.edges[1];
  rejected(()=>certify(a.src,parallel),"bad graph edge");
  samples.push({kind,h:g.h,n:a.n,m:a.m,input_bytes:a.src.length,witness_bytes:JSON.stringify(a.witness).length,odd_models:models(a.src),even_models:models(even.src),accepted_cert:v.ok});
 }
 const loop=mkGraph("K4"),w=gen(loop,[1,0,0,0]);
 rejected(()=>certify("p cnf 6 16\nbad\n",w.witness),"malformed");
 return {tag:"LSPV1-542-TSEITIN-SOURCE-MACRO",status:err?"FAIL":"PASS",checks,failures:err,samples,model:"separate proposed R_T = unit-cost RES plus one unit-cost source-exact TSEITIN-CLOSE; NOT historical R_mix341",interpretation:"This is an explicit accepted polynomial-source macro and an abstract-rule coverage falsifier, not a full mixed lower bound."};
};

console.log(JSON.stringify(tests(),null,2));
