// Usage: node hostile42.js certificate.json [exact source chart clauses JSON]
// For native charts authenticate/regenerate using the certificate's pinned compiler,
// registry and chart reproducer, then export its ordered clauses as JSON + LF.
const fs=require('node:fs'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const enc=x=>JSON.stringify(x)+'\n';const c=JSON.parse(fs.readFileSync(process.argv[2]));
const canon=r=>[...new Set(r)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b), key=r=>canon(r).join(','), vs=r=>[...new Set(r.flat().map(Math.abs))].sort((a,b)=>a-b);
const bit=(m,i)=>Math.floor(m/2**i)%2;
const sat=(r,word)=>r.some(l=>word.get(Math.abs(l))===Number(l>0));
function words(s){return Array.from({length:2**s.length},(_,m)=>new Map(s.map((v,i)=>[v,bit(m,s.length-1-i)])));}
function models(F,n){return Array.from({length:2**n},(_,m)=>m).filter(m=>F.every(r=>r.some(l=>bit(m,Math.abs(l)-1)===Number(l>0))));}
function graph(F){const E=new Map();const add=(u,v)=>{if(!E.has(u))E.set(u,new Set());E.get(u).add(v);};for(const r of F){if(r.length===1)add(-r[0],r[0]);if(r.length===2){add(-r[0],r[1]);add(-r[1],r[0]);}}return E;}
function reach(E,u){const S=new Set([u]),Q=[u];for(const v of Q)for(const w of E.get(v)||[])if(!S.has(w)){S.add(w);Q.push(w);}return S;}
function count(F,V){const E=graph(F);let n=0;for(const v of V)for(const u of [-v,v])n+=reach(E,u).size-1;return n;}
function checkParity(s,rows,p){assert(s.length===3);const W=words(s).filter(w=>[...w.values()].reduce((a,b)=>a+b,0)%2===p);assert(W.length===4);for(const w of W)assert(rows.every(r=>sat(r,w)));for(let i=0;i<3;i++){assert(W.filter(w=>w.get(s[i])===1).length===2);for(let j=i+1;j<3;j++){const h=new Set(W.map(w=>2*w.get(s[i])+w.get(s[j])));assert(h.size===4);}}}
if(c.format==='UNIQUE-SCOPE-3CNF-PAIR-REFUSAL-v1'){
 const U=c.gadget,T=U.filter(r=>JSON.stringify(r)!==JSON.stringify(c.removed));assert.deepEqual(models(U,8),[]);const M=models(T,8);assert.deepEqual(M,c.gadget_models);assert(M.length&&M.every(m=>bit(m,c.pin-1)===c.pinbit));assert.deepEqual(models(c.source,3),c.source_models);
 let next=4,F=[],copies=[],maps=[];function pin(){let offset=next-1;next+=8;F.push(...T.map(r=>r.map(l=>Math.sign(l)*(Math.abs(l)+offset))));maps.push(offset);return (c.pin+offset)*(c.pinbit===0?1:-1);}
 for(const r of c.source){const out=[];for(const l of r){let v=Math.abs(l),q=next++;copies.push([q,v]);out.push(Math.sign(l)*q);let p=pin(),t=pin();F.push([-v,q,p],[v,-q,t]);}F.push(out);}
 assert.equal(next-1,c.nvars);assert.equal(F.length,c.nclauses);assert.equal(new Set(F.map(r=>vs([r]).join(','))).size,F.length);
 const dimacs='p cnf '+c.nvars+' '+F.length+'\n'+F.map(r=>r.join(' ')+' 0\n').join('');assert.equal('DIMACS-CNF-v1:sha256:'+sha(dimacs),c.instance_id);assert.equal(Buffer.byteLength(dimacs)*8,c.original_N_bits);
 for(const r of F){const s=vs([r]);checkParity(s,[r],1-r.filter(l=>l<0).length%2);}
 for(const m of c.source_models){const W=new Map([1,2,3].map(v=>[v,bit(m,v-1)]));for(const [q,v] of copies)W.set(q,W.get(v));for(const off of maps)for(let i=1;i<=8;i++)W.set(off+i,bit(M[0],i-1));assert.equal(W.size,c.nvars);assert(F.every(r=>sat(r,W)));}
 console.log('PASS',c.instance,c.nclauses,'scopes',c.source_models.length?'YES':'NO','pair LP feasible');
}else{
 const F=JSON.parse(fs.readFileSync(process.argv[3]));assert.equal(sha(enc(F)),c.source_chart_clauses_sha256||c.projection.source_chart_clauses_sha256);
 if(c.format==='PAIR-PARITY-LP-REFUSAL-v1'){
  const groups=new Map();for(const r of F){const s=vs([r]),k=s.join(',');if(!groups.has(k))groups.set(k,[s,[]]);groups.get(k)[1].push(r);}
  const arr=[...groups.values()].sort((a,b)=>{for(let i=0;i<Math.min(a[0].length,b[0].length);i++)if(a[0][i]!==b[0][i])return a[0][i]-b[0][i];return a[0].length-b[0].length;});assert.equal(arr.length,c.group_count);assert.equal(c.parities.length,arr.length);assert.equal(F.length,c.clause_count);assert.equal(c.denominator,4);
  arr.forEach(([s,rs],i)=>checkParity(s,rs,Number(c.parities[i])));console.log('PASS',c.instance,arr.length,'exact local factors');
 }else if(c.format==='ROOT-PAIR-TRANSPORT-v1'){
  const D=F.map(canon),p=c.projection,v=p.v,B=D.filter(r=>r.includes(v)||r.includes(-v)),E=D.filter(r=>!r.includes(v)&&!r.includes(-v)),R=p.resolvents;assert.deepEqual(B,p.bucket);assert.deepEqual(vs(B).filter(u=>u!==v),p.boundary);
  const H=E.concat(R);assert.equal(sha(enc(H)),p.projected_clauses_sha256);
  const W=words(p.boundary);assert.equal(W.length,p.witness_table.length);W.forEach((w,i)=>{let ok0=B.every(r=>sat(r,new Map([...w,[v,0]]))),ok1=B.every(r=>sat(r,new Map([...w,[v,1]])));assert.equal(R.every(r=>sat(r,w)),ok0||ok1);assert.equal(p.witness_table[i],ok0?0:ok1?1:-1);});
  const db=H.slice();for(const t of c.trace){const r=t.c;if(t.kind==='table'){assert(t.parents.every(i=>i>=0&&i<db.length));const rs=t.parents.map(i=>db[i]);for(const w of words(vs(rs.concat([r]))))assert(sat(r,w)||!rs.every(s=>sat(s,w)));}else{const [u,z]=t.parents;assert.equal(key(r),key([-u,z]));assert(reach(graph(db),u).has(z));}db.push(r);}
  const root=D.filter(r=>r.length<=2),incoming=db.filter(r=>r.length<=2);const unique=F=>new Set(F.map(key)).size;assert.deepEqual([unique(root),unique(root.concat(incoming))],c.counts.root_clauses);assert.deepEqual([count(root,vs(D)),count(root.concat(incoming),vs(D))],c.counts.root_graph_pairs);assert.equal(unique(incoming),c.counts.consumer_distinct);console.log('PASS',c.instance,c.counts);
 }else throw Error('unsupported certificate');
}
console.log('CERT-v1:sha256:'+sha(fs.readFileSync(process.argv[2])));
