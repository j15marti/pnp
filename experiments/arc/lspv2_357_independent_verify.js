#!/usr/bin/env node
/** Independent no-import Resolution/DPLL port-branch certificate referee.
 * Does not call or reuse the Python producer; checks all source, residual and lifted steps.
 */
'use strict';
const fs=require('fs'),crypto=require('crypto'),path=require('path');
let checks=0;const chk=(p,m)=>{checks++;if(!p)throw Error(`assertion ${checks}: ${m}`);};
const norm=a=>[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
function parse(t){
 if(!t.endsWith('\n'))throw Error('newline');
 let l=t.split('\n').map(x=>x.trim()).filter(x=>x.length && !x.startsWith('c'));
 if(!l.length)throw Error('empty');let h=l.shift().split(/\s+/);
 if(h.length!==4||h[0]!=='p'||h[1]!=='cnf'||!/^\d+$/.test(h[2])||!/^\d+$/.test(h[3]))throw Error('header');
 let n=+h[2],m=+h[3];if(n<1||m<1||l.length!==m)throw Error('count');
 let out=[],seen=new Set();
 for(let line of l){let toks=line.split(/\s+/);if(toks.some(x=>!/^[-]?\d+$/.test(x)))throw Error('numeric');
  let a=toks.map(Number);if(a.at(-1)!==0||a.slice(0,-1).includes(0))throw Error('terminator');
  a.pop();if(a.some(x=>Math.abs(x)>n))throw Error('index');
  if(new Set(a).size!==a.length||a.some(x=>a.includes(-x)))throw Error('canonical');
  a.forEach(x=>seen.add(Math.abs(x)));out.push(norm(a));
 }
 if(seen.size!==n||[...seen].some(v=>v<1||v>n))throw Error('unused');
 return {n,clauses:out};
}
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const subset=(a,b)=>a.every(x=>b.includes(x));
function res(a,b,v){
 if(!a.includes(v)||!b.includes(-v))throw Error('not strict complementary pivot');
 let u=norm([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);
 if(u.some(x=>u.includes(-x)))throw Error('tautology');return u;
}
function rest(cl,env){
 if(cl.some(l=>env.has(Math.abs(l))&&env.get(Math.abs(l))===(l>0)))return null;
 return cl.filter(l=>!env.has(Math.abs(l)));
}
function valClause(c,bits){return c.some(l=>bits[Math.abs(l)-1]===(l>0));}
function exhaustive(n,cls){let sat=0,first=null;for(let mask=0;mask<2**n;mask++){
 let bits=Array.from({length:n},(_,i)=>!!(mask&(1<<i)));
 if(cls.every(c=>valClause(c,bits))){sat++;if(!first)first=bits;}
}return {sat,first};}
function checkOne(a){
 let {n,clauses:src}=parse(a.source),m=src.length,ports=a.ports;
 chk(n===a.n,'n');chk(new Set(ports).size===ports.length,'ports distinct');
 chk(ports.every(v=>Number.isInteger(v)&&v>=1&&v<=n),'ports in range');
 chk(exhaustive(n,src).sat===0,'unsat original');
 chk(a.nodes.length>=m,'global source count');
 for(let j=0;j<m;j++){chk(a.nodes[j].kind==='source','original source only');chk(eq(a.nodes[j].clause,src[j]),'source-auth');}
 for(let i=m;i<a.nodes.length;i++){
  let d=a.nodes[i];chk(d.kind==='res','no new axiom');chk(Number.isInteger(d.p)&&d.p<i&&d.p>=0,'p earlier');
  chk(Number.isInteger(d.q)&&d.q<i&&d.q>=0,'q earlier');chk(Number.isInteger(d.pivot)&&d.pivot>=1&&d.pivot<=n,'pivot');
  chk(eq(d.clause,res(a.nodes[d.p].clause,a.nodes[d.q].clause,d.pivot)), 'exact RES');
 }
 chk(eq(a.nodes[a.root].clause,[]),'final empty');
 let expected=m, retained=0, replayed=0, bypassed=0, leaves={};
 let keys=Object.keys(a.leaves).sort();chk(keys.length===2**ports.length,'complete port cube');
 for(let key of keys){
  let leaf=a.leaves[key],bits=key.split('').map(Number);chk(bits.length===ports.length&&bits.every(x=>x===0||x===1),'assignment');
  chk(eq(bits,leaf.partial),'partial record');let env=new Map(ports.map((x,j)=>[x,!!bits[j]]));
  let blocker=ports.map(x=>env.get(x)?-x:x);
  let local=[],translated=[];
  for(let d of leaf.residual){
   chk(eq(d.clause,norm(d.clause)),'residual normalized');
   if(d.kind==='source'){
    chk(d.source>=0&&d.source<m,'local source index');
    let r=rest(src[d.source],env);
    chk(r!==null&&eq(r,d.clause),'restricted exact authentic source');
    translated.push(d.source);
   }else{
    chk(d.kind==='res','residual kind');chk(d.p>=0&&d.p<local.length,'residual p');chk(d.q>=0&&d.q<local.length,'residual q');
    chk(eq(d.clause,res(local[d.p],local[d.q],d.pivot)),'residual pivot');
    let p=translated[d.p],q=translated[d.q],P=a.nodes[p].clause,Q=a.nodes[q].clause,idx;
    if(P.includes(d.pivot)&&Q.includes(-d.pivot)){
      chk(expected<a.nodes.length,'global replay exists');
      let got=a.nodes[expected];chk(eq(got.clause,res(P,Q,d.pivot)),'global lift exact');
      chk(got.p===p&&got.q===q&&got.pivot===d.pivot,'same parents/pivot');
      idx=expected++;replayed++;
    }else if(!P.includes(d.pivot)){idx=p;bypassed++;}else{chk(!Q.includes(-d.pivot),'legal bypass');idx=q;bypassed++;}
    translated.push(idx);retained++;
   }
   chk(subset(a.nodes[translated.at(-1)].clause,norm([...d.clause,...blocker])),'subsumption lifting invariant');
   local.push(d.clause);
  }
  chk(eq(local[leaf.root],[]),'restricted root contradictory');
  chk(translated[leaf.root]===leaf.lifted_root,'lifted root identity');
  chk(subset(a.nodes[leaf.lifted_root].clause,blocker),'blocking clause');
  leaves[key]=leaf.lifted_root;
 }
 let merges=0;
 function join(prefix,depth){
  if(depth===ports.length)return leaves[prefix];
  let x=ports[depth],p=join(prefix+'0',depth+1),q=join(prefix+'1',depth+1),P=a.nodes[p].clause,Q=a.nodes[q].clause;
  if(!P.includes(x))return p;
  if(!Q.includes(-x))return q;
  chk(expected<a.nodes.length,'missing merge line');
  let got=a.nodes[expected];chk(got.p===p&&got.q===q&&got.pivot===x,'merge parent');
  chk(eq(got.clause,res(P,Q,x)),'merge exact');
  merges++;return expected++;
 }
 let rt=join('',0);
 chk(rt===a.root,'root ID');chk(expected===a.nodes.length,'no uncertified steps');
 chk(a.stats.actual_paid===replayed+merges,'paid count');chk(a.stats.retained_residual_paid===retained,'branch cost');
 chk(a.stats.replayed_paid===replayed,'branch replay');chk(a.stats.merges===merges,'merge count');
 chk(a.stats.bypassed_restricted_steps===bypassed,'bypass count');
 chk(a.stats.limit===retained+2**ports.length-1,'bound exact');
 chk(a.stats.actual_paid<=a.stats.limit,'cost cap');
 return {name:a.name,paid:a.stats.actual_paid,limit:a.stats.limit,branch_cost:retained,merges,bypassed};
}
function mustReject(cb,label){let ok=false;try{cb();}catch(e){ok=true;}chk(ok,`accept corrupted ${label}`);}
function main(){let f=process.argv[2]||path.join(__dirname,'lspv2_357_port_split_proofs.json');
 let buf=fs.readFileSync(f),data=JSON.parse(buf);
 let cases=data.cases.map(checkOne);
 // Independent source-neighbor SAT witnesses where they exist, and positive/malformed fixtures.
 for(let x of data.sat_deletion_controls){let parent=data.cases.find(c=>c.name===x.base);
  let p=parse(parent.source),restsrc=p.clauses.filter((c,j)=>j!==x.remove);
  let ans=exhaustive(p.n,restsrc);chk((x.witness===null)===(ans.first===null),'neighbor class');
  if(x.witness!==null)chk(restsrc.every(c=>valClause(c,x.witness.map(Boolean))),'neighbor witness');
 }
 let sat=[['p cnf 2 2\n1 2 0\n-1 2 0\n',1],['p cnf 3 1\n1 2 3 0\n',1]];
 for(let [s] of sat)chk(exhaustive(parse(s).n,parse(s).clauses).sat>0,'positive SAT');
 let bad=['p cnf 2 1\n1 0\n2 0\n','p cnf 2 1\n3 0\n','p cnf 2 1\na 0\n','p cNF 2 1\n1 0\n','p cnf 2 1\n1 2\n','p cnf 2 1\n1 1 0\n','p cnf 2 1\n1 -1 0\n','p cnf 2 1\n1 0'];
 for(let [i,b] of bad.entries())mustReject(()=>parse(b),`malformed ${i}`);
 let corrupt=0;
 for(let x of data.cases){let first=x.nodes.findIndex((n,i)=>i>=parse(x.source).clauses.length&&n.kind==='res');
  if(first>=0){let z=JSON.parse(JSON.stringify(x));z.nodes[first].pivot=999;
   mustReject(()=>checkOne(z),`bad pivot ${x.name}`);corrupt++;
   z=JSON.parse(JSON.stringify(x));z.nodes[first].clause=[-999];
   mustReject(()=>checkOne(z),`bad resolvent ${x.name}`);corrupt++;
  }
  let z=JSON.parse(JSON.stringify(x));z.nodes[0].clause=[999];
  mustReject(()=>checkOne(z),`forged original source ${x.name}`);corrupt++;
  z=JSON.parse(JSON.stringify(x));z.leaves[Object.keys(z.leaves)[0]].root=999;
  mustReject(()=>checkOne(z),`forged leaf root ${x.name}`);corrupt++;
 }
 chk(data.malformed_rejected===bad.length,'producer bad controls');chk(data.sat_positive===4,'producer positive controls');
 let out={status:'PASS',cases,checks,corruptions_rejected:corrupt,malformed_rejected:bad.length,raw_sha256:crypto.createHash('sha256').update(buf).digest('hex')};
 fs.writeFileSync(path.join(__dirname,'lspv2_357_independent_record.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out,null,2));
}
main();
