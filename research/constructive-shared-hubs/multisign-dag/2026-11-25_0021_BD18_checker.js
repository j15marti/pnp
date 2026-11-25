// Node.js: node checker.js DR18_M24_reclosed.json
const fs=require('fs');
function run(tables,guard=[],witness=null,cap=25000000){
 const rows=[],groups=[],m=tables.length;
 for(let i=0;i<m;i++){let g=[];for(let w of tables[i].a){if(guard.some(([v,b])=>tables[i].v.includes(v)&&+w[tables[i].v.indexOf(v)]!==b))continue;g.push(rows.length);rows.push({i,w,v:tables[i].v});}groups.push(g);}
 const R=rows.length,bits=rows.map((_,i)=>1n<<BigInt(i)), masks=groups.map(g=>g.reduce((a,r)=>a|bits[r],0n)),adj=rows.map(()=>0n),active=rows.map(()=>true);
 let initial=0,overlapTests=0,unary=0,pair=0,checks=0,passes=0,stopped=false,unsat=masks.some(x=>x===0n),changed=true;
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){const ix=tables[i].v.map((v,k)=>[k,tables[j].v.indexOf(v)]).filter(x=>x[1]>=0);for(let r of groups[i])for(let s of groups[j]){overlapTests++;if(ix.every(([a,b])=>rows[r].w[a]===rows[s].w[b])){adj[r]|=bits[s];adj[s]|=bits[r];initial++;}}}
 const alive=()=>groups.map(g=>g.filter(r=>active[r]).length);
 while(changed&&!unsat&&!stopped){changed=false;passes++;
 // Unconditional closure (within actual input guard), repeated after every batch of accepted pair deletions.
 let u=true;while(u&&!unsat){u=false;for(let r=0;r<R;r++)if(active[r]){for(let k=0;k<m;k++)if(k!==rows[r].i&&(adj[r]&masks[k])===0n){active[r]=false;masks[rows[r].i]&=~bits[r];for(let s=0;s<R;s++)adj[s]&=~bits[r];adj[r]=0n;unary++;u=changed=true;if(masks[rows[r].i]===0n)unsat=true;break;}}}
 if(unsat)break;
 outer:for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let r of groups[i])if(active[r])for(let s of groups[j])if(active[s]&&(adj[r]&bits[s])!==0n){
 const both=adj[r]&adj[s];for(let k=0;k<m;k++)if(k!==i&&k!==j){if(checks>=cap){stopped=true;break outer;}checks++;if((both&masks[k])===0n){adj[r]&=~bits[s];adj[s]&=~bits[r];pair++;changed=true;break;}}
 }
 }
 let valid=null;if(witness){let chosen=tables.map((t,i)=>groups[i].find(r=>rows[r].w===t.v.map(v=>witness[v]).join("")));valid=chosen.every(r=>r!==undefined&&active[r])&&chosen.every((r,i)=>chosen.every((s,j)=>i===j||(adj[r]&bits[s])!==0n));if(!valid)throw Error("lost supplied witness");}
 const remaining=alive();let edges=0;for(let r=0;r<R;r++)if(active[r])for(let s=r+1;s<R;s++)if((adj[r]&bits[s])!==0n)edges++;
 return {rows:R,owners:m,initialEdges:initial,finalEdges:edges,overlapTests,unaryDeleted:unary,pairDeleted:pair,checks,passes,stopped,unsat,remaining,valid};
}
const d=JSON.parse(fs.readFileSync(process.argv[2])).results.filter(x=>x.mode==='joint');
const nae=(v,sign=0)=>({v,a:Array.from({length:8},(_,i)=>i.toString(2).padStart(3,"0")).filter(w=>w!==((sign).toString(2).padStart(3,"0"))&&w!==((sign^7).toString(2).padStart(3,"0")))}); const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
console.log(JSON.stringify({results:d.map(x=>({id:x.id,guard:x.guard,...run(x.finalTables,x.guard,x.witness)})),controls:[{id:"Fano",...run(fano.map(v=>nae(v)))},{id:"Fano-deletion",...run(fano.slice(1).map(v=>nae(v)))},{id:"parity-triangle",...run([{v:[0,1],a:["00","11"]},{v:[1,2],a:["00","11"]},{v:[0,2],a:["01","10"]}])},{id:"parity-triangle-SAT",...run([{v:[0,1],a:["00","11"]},{v:[1,2],a:["00","11"]},{v:[0,2],a:["00","11"]}],[],[0,0,0])}]},null,2));
