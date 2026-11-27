function assert(x,m){if(!x)throw Error(m)}

function cycles(p){let seen=new Set(),c=0;for(let i=0;i<p.length;i++)if(!seen.has(i)){c++;let j=i;while(!seen.has(j)){seen.add(j);j=p[j]}}return c}

function sign(p){return (p.length-cycles(p))%2?-1:1}

function family(r){assert(r%6===0,"r");let n=3*r,a=Array.from({length:n},()=>[]),neg=[];for(let i=0;i<n;i++){let q=i%3===0?i+2:i-1;a[i].push((i+2)%n,(q+2)%n);if(i%3===0)a[i].push((i+5)%n)}neg.push([0,5]);return {a,neg}}

function det(a,neg=[]){let n=a.length,b=Array.from({length:n},()=>Array(n).fill(0n));for(let i=0;i<n;i++)for(let j of a[i])b[i][j]=1n;for(let [i,j] of neg)if(b[i][j])b[i][j]=-1n;let d=1n,s=1n;for(let k=0;k<n-1;k++){let i=k;while(i<n&&!b[i][k])i++;if(i===n)return 0n;if(i!==k){[b[i],b[k]]=[b[k],b[i]];s=-s}let p=b[k][k];for(let i=k+1;i<n;i++){for(let j=k+1;j<n;j++)b[i][j]=(b[i][j]*p-b[i][k]*b[k][j])/d;b[i][k]=0n}d=p}return s*b[n-1][n-1]}

function count(a,neg){let c=det(a,neg);if(c<0n)c=-c;let d=det(a),z=c+(a.length%2?d:-d);assert(z>=0n&&z%2n===0n,"parity count");return {total:c,target:z/2n}}

function matching(a){let n=a.length,inv=Array(n).fill(-1);function aug(i,seen){for(let j of a[i])if(!seen.has(j)){seen.add(j);if(inv[j]===-1||aug(inv[j],seen)){inv[j]=i;return true}}return false}for(let i=0;i<n;i++)if(!aug(i,new Set()))return null;let p=Array(n);for(let j=0;j<n;j++)p[inv[j]]=j;return p}

function reach(a,i){let s=new Set([i]),q=[i];for(let k=0;k<q.length;k++)for(let j of a[q[k]])if(!s.has(j)){s.add(j);q.push(j)}return s}

function closure(a){let p=matching(a);if(!p)return {a:null};let n=a.length,inv=Array(n);p.forEach((j,i)=>inv[j]=i);let b=a.map((row,i)=>row.map(j=>inv[j]).filter(j=>j!==i));let rr=b.map((_,i)=>reach(b,i));let out=a.map((row,i)=>row.filter(j=>rr[inv[j]].has(i)));return {a:out,p,removed:a.reduce((s,r,i)=>s+r.length-out[i].length,0),forced:out.filter(r=>r.length===1).length,strong:out.every((_,i)=>reach(out,i).size===n)}}

function enumerate(a,cap){let p=Array(a.length),used=new Set(),total=0,targets=0,hc=0,visits=0,overflow=false;function go(i){if(++visits>cap){overflow=true;return}if(i===a.length){total++;let c=cycles(p);if(c%2)targets++;if(c===1)hc++;return}for(let j of a[i])if(!used.has(j)){used.add(j);p[i]=j;go(i+1);used.delete(j);if(overflow)return}}go(0);return {total,targets,hc,visits,overflow}}

function filter(a,neg,cap){let z=count(a,neg),calls=1,closed=0,leaves=0,hc=0;if(z.target>BigInt(cap))return {status:"UNKNOWN",calls,closed,leaves,hc};function go(a,i){if(i===a.length){leaves++;if(cycles(a.map(r=>r[0]))===1)hc++;return}for(let j of a[i]){let b=a.map((row,k)=>k===i?[j]:row.filter(x=>x!==j));if(i>0)b=a.map((row,k)=>k<i?row:k===i?[j]:row.filter(x=>x!==j));let q=closure(b);closed++;if(q.a===null)continue;let z=count(q.a,neg);calls++;if(z.target)go(q.a,i+1)}}if(z.target)go(a,0);return {status:hc?"NOT_NO":"NO",calls,closed,leaves,hc}}

function blowup(a,neg){let n=a.length,b=Array.from({length:4*n},()=>[]);for(let i=0;i<n;i++){let k=4*i;b[k]=[k+1,k+2];b[k+1]=[k+2,k+3];b[k+2]=[k+1,k+3];b[k+3]=a[i].map(j=>4*j)}return {a:b,neg:neg.map(([i,j])=>[4*i+3,4*j])}}

function quotient(a,neg){let n=a.length,ins=Array.from({length:n},()=>[]);a.forEach((row,i)=>row.forEach(j=>ins[j].push(i)));let blocks=[],used=new Set();const eq=(a,b)=>a.length===b.length&&a.every(x=>b.includes(x));for(let i=0;i<n;i++)if(!used.has(i)&&a[i].length===2){let [j,k]=a[i];if(a[j].length!==2||a[k].length!==2)continue;let d=a[j].find(x=>x!==k);if(d===undefined||new Set([i,j,k,d]).size!==4||[i,j,k,d].some(x=>used.has(x)))continue;if(!eq(a[j],[k,d])||!eq(a[k],[j,d])||!eq(ins[j],[i,k])||!eq(ins[k],[i,j])||!eq(ins[d],[j,k])||ins[i].some(x=>[i,j,k,d].includes(x))||a[d].some(x=>[i,j,k,d].includes(x)))continue;blocks.push([i,j,k,d]);[i,j,k,d].forEach(x=>used.add(x))}if(used.size!==n)return null;let map=new Map(blocks.map((b,i)=>[b[0],i])),end=new Map(blocks.map((b,i)=>[b[3],i]));assert(blocks.every(b=>a[b[3]].every(x=>map.has(x))),"cross");if(neg.some(([i,j])=>!end.has(i)||!map.has(j)))return null;return {a:blocks.map(b=>a[b[3]].map(x=>map.get(x))),neg:neg.map(([i,j])=>[end.get(i),map.get(j)]),blocks}}

function run(){let out=[];for(let r of [6,12,24,48]){let {a,neg}=family(r),q=closure(a),z=count(a,neg);assert(q.strong&&q.removed===0&&q.forced===0,"closure");assert(z.total===(1n<<BigInt(r))+1n&&z.target===1n,"counts");let ref=r<=12?enumerate(a,2000000):null;if(ref)assert(!ref.overflow&&ref.total===Number(z.total)&&ref.targets===1&&ref.hc===0,"reference");let f=r<=24?filter(a,neg,1):null;if(f)assert(f.status==="NO"&&f.leaves===1,"filter");out.push({r,n:a.length,total:String(z.total),target:String(z.target),closure:{removed:q.removed,forced:q.forced,strong:q.strong},ref,filter:f})}let {a,neg}=family(6),b=blowup(a,neg),q=closure(b.a),z=count(b.a,b.neg);assert(q.strong&&q.removed===0&&q.forced===0,"blow closure");assert(z.target===1n<<BigInt(a.length),"blow target");let f=filter(b.a,b.neg,1),k=quotient(b.a,b.neg);assert(k&&k.a.length===a.length,"quotient");let ff=filter(k.a,k.neg,1);assert(f.status==="UNKNOWN"&&ff.status==="NO","hybrid");let ctrl=family(6); // minimal soundness control: one 6-vertex Hamilton cycle
let ca=Array.from({length:6},(_,i)=>[(i+1)%6]);assert(filter(ca,[],1).status==="NOT_NO","soundness");return {family:out,hostile:{n:b.a.length,total:String(z.total),target:String(z.target),closure:{removed:q.removed,forced:q.forced,strong:q.strong},before:f,after:ff,quotient_n:k.a.length},control:"single cycle not refuted"}}
console.log(JSON.stringify(run(),null,2));
