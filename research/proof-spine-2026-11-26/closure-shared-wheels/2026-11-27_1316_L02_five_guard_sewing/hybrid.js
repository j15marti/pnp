const fs=require('fs');const hybrid=function hybrid(z){
 const F=z.nativeChart.clauses,n=z.nativeRes.n,G=z.nativeRes.guards,abs=Math.abs,uniq=x=>[...new Set(x)],cheap=G.filter((_,i)=>z.nativeRes.rows[i][0].conflict&&z.nativeRes.rows[i][4].conflict);
 let events=0;function count(guards,extra=[]){let total=0n;for(let mask=0;mask<2**guards.length;mask++){let p=new Map(),k=0,ok=true;for(let l of extra){if(p.has(abs(l))&&p.get(abs(l))!==Math.sign(l))ok=false;p.set(abs(l),Math.sign(l))}for(let i=0;i<guards.length;i++)if(mask&(1<<i)){k++;for(let l of guards[i]){if(p.has(abs(l))&&p.get(abs(l))!==Math.sign(l))ok=false;p.set(abs(l),Math.sign(l))}}events++;if(ok)total+=(k%2?-1n:1n)*(1n<<BigInt(n-p.size))}return total}
 // exact survivor hull in the relevant guard-coordinate subspace, with all non-guard coordinates free.
 let vars=uniq(cheap.flat().map(abs)).sort((a,b)=>a-b),allowed=[];for(let mask=0;mask<2**vars.length;mask++){let p=vars.map((v,i)=>(mask&(1<<i))?v:-v);if(count(cheap,p)>0n)allowed.push(mask)}
 let equations=[];const parity=x=>{let v=0;while(x){v^=1;x&=x-1}return v};
 if(allowed.length){let base=allowed[0];for(let m=1;m<2**vars.length;m++){let rhs=parity(m&base);if(allowed.every(x=>parity(x&m)===rhs))equations.push({vars:vars.filter((_,i)=>m&(1<<i)),rhs})}}
 let fixed=equations.filter(e=>e.vars.length===1).map(e=>e.rhs?e.vars[0]:-e.vars[0]),learned=cheap.map(g=>g.map(l=>-l));
 function up(g,clauses){let v=new Map(g.map(l=>[abs(l),Math.sign(l)])),work=0,used=[];while(true){let change=false;for(let i=0;i<clauses.length;i++){work++;let a=clauses[i];if(a.some(l=>v.get(abs(l))===Math.sign(l)))continue;let u=a.filter(l=>!v.has(abs(l)));if(!u.length)return {conflict:true,work,used:uniq(used.concat(i)),fixed:[...v].map(([x,t])=>t*x)};if(u.length===1){v.set(abs(u[0]),Math.sign(u[0]));used.push(i);change=true}}if(!change)return {conflict:false,work,used:uniq(used),fixed:[...v].map(([x,t])=>t*x)}}}
 // seeded candidate discovery at partial coverage plateau; each positive independently replayed by reverse-order UP
 let seed=20261127,random=[];function rand(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
 for(let i=0;i<20;i++){let a=rand()%n+1,b=rand()%n+1,g=[(rand()&1)?a:-a,(rand()&1)?b:-b];if(a===b){random.push({g,status:"duplicate"});continue}let p=up(g,F);let q=p.conflict?up(g,[...F].reverse()):null;random.push({g,work:p.work,check:q?.work||0,status:p.conflict&&q.conflict?"verified": "UNKNOWN"})}
 // stronger hybrid on same carrier: replay partial guard refutations, derive exact affine hull pins, add to clauses, reclose.
 const root=up(fixed,F.concat(learned));
 // resolution proof for disjoint five-guard cover, check each resolvent exactly.
 let C=G.map(g=>g.map(l=>-l)),steps=[];while(!C.some(a=>a.length===0)){let found=false;for(let i=0;i<C.length&&!found;i++)for(let j=i+1;j<C.length&&!found;j++)for(let l of C[i])if(C[j].includes(-l)){let a=uniq(C[i].filter(x=>x!==l).concat(C[j].filter(x=>x!==-l))).sort((x,y)=>x-y);if(a.some(x=>a.includes(-x))||a.length>=Math.max(C[i].length,C[j].length)||C.some(x=>x.length===a.length&&x.every(y=>a.includes(y))))continue;steps.push({i,j,pivot:l,result:a});C.push(a);found=true;break}if(!found)throw Error("guard merge");}
 let sizes=z.nativeCore.map(x=>x.length),overlap=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)overlap.push([i,j,z.nativeCore[i].filter(v=>z.nativeCore[j].includes(v)).length]);
 let total=z.nativeRes.rows.flat().reduce((s,x)=>s+x.events+(x.check||0),0),cnfTotal=z.cnf.rows.flat().reduce((s,x)=>s+x.events+(x.check||0),0);
 return {cheapCount:cheap.length,remaining:count(cheap).toString(),guardCoordinates:vars,allowed,equations,fixed,root,random,guardCountEvents:events,resolution:steps,coreSizes:sizes,coreUnion:uniq(z.nativeCore.flat()).length,overlap,total,cnfTotal}
};
console.log(JSON.stringify(JSON.parse(fs.readFileSync(process.argv[2],'utf8')).map(z=>({alias:z.alias,hybrid:hybrid(z)})),null,2));
