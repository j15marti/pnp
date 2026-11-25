// node replay.js DR18.json GD24.json BS17.json S23.json
const fs=require('fs');
function solve(groups,bits,A,D,cap=1000){
 let nodes=0,checks=0,scans=0,limited=false;
 const members=(g,mask)=>g.filter(r=>(mask&bits[r])!==0n);
 function visit(dom){
 if(nodes>=cap){limited=true;return null;}nodes++;
 let changed=true;
 while(changed){changed=false;scans++;for(let i=0;i<groups.length;i++){if(dom[i]===0n)return null;for(let r of members(groups[i],dom[i]))for(let j=0;j<groups.length;j++)if(i!==j){checks++;if((A[r]&dom[j])===0n){dom[i]&=~bits[r];changed=true;break;}}if(dom[i]===0n)return null;}}
 let lists=groups.map((g,i)=>members(g,dom[i]));let pick=-1;for(let i=0;i<lists.length;i++)if(lists[i].length>1&&(pick<0||lists[i].length<lists[pick].length))pick=i;
 if(pick<0)return lists.map(g=>g[0]);
 for(let r of lists[pick]){let ch=dom.slice();ch[pick]=bits[r];let ans=visit(ch);if(ans)return ans;if(limited)return null;}
 return null;
 }
 const ans=visit(D.slice());return{status:ans?"SAT":limited?"UNKNOWN":"UNSAT",nodes,checks,scans,ans};
}
function run(tables,guard=[],witness=null,cap=25000000){
 const rows=[],groups=[],m=tables.length;
 for(let i=0;i<m;i++){let g=[];for(let w of tables[i].a){if(guard.some(([v,b])=>tables[i].v.includes(v)&&+w[tables[i].v.indexOf(v)]!==b))continue;g.push(rows.length);rows.push({i,w,v:tables[i].v});}groups.push(g);}
 const R=rows.length,bits=rows.map((_,i)=>1n<<BigInt(i)), masks=groups.map(g=>g.reduce((a,r)=>a|bits[r],0n)),adj=rows.map(()=>0n),active=rows.map(()=>true);
 let initial=0,overlapTests=0,unary=0,pair=0,checks=0,passes=0,stopped=false,unsat=masks.some(x=>x===0n),changed=true;
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){const ix=tables[i].v.map((v,k)=>[k,tables[j].v.indexOf(v)]).filter(x=>x[1]>=0);for(let r of groups[i])for(let s of groups[j]){overlapTests++;if(ix.every(([a,b])=>rows[r].w[a]===rows[s].w[b])){adj[r]|=bits[s];adj[s]|=bits[r];initial++;}}}
 const initialAdj=adj.slice(),initialMasks=masks.slice();
 const alive=()=>groups.map(g=>g.filter(r=>active[r]).length);
 while(changed&&!unsat&&!stopped){changed=false;passes++;
 // Unconditional closure (within actual input guard), repeated after every batch of accepted pair deletions.
 let u=true;while(u&&!unsat){u=false;for(let r=0;r<R;r++)if(active[r]){for(let k=0;k<m;k++)if(k!==rows[r].i&&(adj[r]&masks[k])===0n){active[r]=false;masks[rows[r].i]&=~bits[r];for(let s=0;s<R;s++)adj[s]&=~bits[r];adj[r]=0n;unary++;u=changed=true;if(masks[rows[r].i]===0n)unsat=true;break;}}}
 if(unsat)break;
 outer:for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let r of groups[i])if(active[r])for(let s of groups[j])if(active[s]&&(adj[r]&bits[s])!==0n){
 const both=adj[r]&adj[s];for(let k=0;k<m;k++)if(k!==i&&k!==j){if(checks>=cap){stopped=true;break outer;}checks++;if((both&masks[k])===0n){adj[r]&=~bits[s];adj[s]&=~bits[r];pair++;changed=true;break;}}
 }
 }
 // Complete unary closure even if the triangle probe cap interrupted a sweep.
 let u=true;while(u&&!unsat){u=false;for(let r=0;r<R;r++)if(active[r]){for(let k=0;k<m;k++)if(k!==rows[r].i&&(adj[r]&masks[k])===0n){active[r]=false;masks[rows[r].i]&=~bits[r];for(let s=0;s<R;s++)adj[s]&=~bits[r];adj[r]=0n;unary++;u=true;if(masks[rows[r].i]===0n)unsat=true;break;}}}
 let valid=null;if(witness){let chosen=tables.map((t,i)=>groups[i].find(r=>rows[r].w===t.v.map(v=>witness[v]).join("")));valid=chosen.every(r=>r!==undefined&&active[r])&&chosen.every((r,i)=>chosen.every((s,j)=>i===j||(adj[r]&bits[s])!==0n));if(!valid)throw Error("lost supplied witness");}
 const remaining=alive();let edges=0;for(let r=0;r<R;r++)if(active[r])for(let s=r+1;s<R;s++)if((adj[r]&bits[s])!==0n)edges++;
 const direct=solve(groups,bits,initialAdj,initialMasks),combined=solve(groups,bits,adj,masks);
 const unpack=ans=>ans?Object.fromEntries(ans.flatMap(r=>rows[r].v.map((v,i)=>[v,+rows[r].w[i]]))):null;
 direct.assignment=unpack(direct.ans);combined.assignment=unpack(combined.ans);
 return {direct,combined,rowMap:rows.map(r=>[r.i,r.w]),pairHex:adj.map(x=>x.toString(16)),live:active,rows:R,owners:m,initialEdges:initial,finalEdges:edges,overlapTests,unaryDeleted:unary,pairDeleted:pair,checks,passes,stopped,unsat,remaining,valid};
}
function lift(a,g,b,s){
 if(!a)return null;let w=Array(b.n).fill(0);for(let i=0;i<b.n;i++)if(g.p[i]>=0)w[i]=g.p[i];for(let [i,v] of Object.entries(a))w[+i]=v;
 for(let x of g.merges.slice().reverse()){let key=x.scope.map(i=>w[i]).join("");let row=x.rows.find(z=>z[0]===key);if(!row)throw Error("missing GD lift");x.private.forEach((i,j)=>w[i]=+row[1][j]);}
 for(let x of b.eliminations.slice().reverse()){let key=x.u.reduce((q,v,i)=>q+w[v]*2**i,0);let row=x.lift.find(z=>z[0]===key);if(!row)throw Error("missing BS lift");w[x.v]=row[1];}
 if(!s.O.every(o=>new Set(o.t.map(i=>w[i])).size===2)||!b.guard.every(([i,v])=>w[i]===v))throw Error("bad source lift");
 return w.join("");
}
const [D0,G0,B0,S]=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p)));const D=D0.results.filter(x=>x.mode==='joint'),G=G0.jobs,B=B0.snapshots;const results=D.map(x=>{const z=run(x.finalTables,x.guard,x.witness);const gg=G.find(y=>y.id===x.id&&JSON.stringify(y.guard)===JSON.stringify(x.guard)),bb=B.find(y=>y.id===x.id&&JSON.stringify(y.guard)===JSON.stringify(x.guard)),ss=S.find(y=>y.id===x.id);z.direct.lift=lift(z.direct.assignment,gg,bb,ss);z.combined.lift=lift(z.combined.assignment,gg,bb,ss);return {id:x.id,guard:x.guard,...z};});console.log(JSON.stringify(results,null,2));
