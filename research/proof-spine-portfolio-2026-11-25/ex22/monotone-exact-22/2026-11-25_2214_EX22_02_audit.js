// Run: node audit.js
function audit(){
  let seed=202611252214, checks=0;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}function ok(x){checks++;if(!x)throw Error("assert "+checks)}const pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
  const rows=(t,d)=>t==="C"?[3,5,6,9,10,12]:[0,(1<<d)-1];
  let treeStats={branch:0,nonbranch:0,words:0,exchangeChecks:0,examples:[]};
  for(let z=0;z<120;z++){
    let nodes=[{t:z%3===0?"C":"E",d:z%3===0?4:2+rand(3),ports:[]}],edges=0;
    for(let j=0;j<nodes[0].d;j++)nodes[0].ports.push(edges++);
    let used=new Set, k=1+rand(4);
    while(nodes.length<k){let opts=nodes.flatMap((u,i)=>u.ports.filter(e=>!used.has(e)).map(e=>[i,e]));let [i,e]=opts[rand(opts.length)],t=nodes[i].t==="C"?"E":"C",d=t==="C"?4:2+rand(3);used.add(e);let p=[e];while(p.length<d)p.push(edges++);nodes.push({t,d,ports:p})}
    let boundary=Array.from({length:edges},(_,i)=>i).filter(i=>!used.has(i));let root=nodes.findIndex(u=>u.t==="E"&&u.d>=3), support=new Map(),v=Array(edges).fill(-1);
    function walk(i,tag){if(i===nodes.length){let b=boundary.reduce((s,e,j)=>s+(v[e]<<j),0);support.set(b,(support.get(b)||0)|(1<<tag));return}let u=nodes[i];for(let w of rows(u.t,u.d)){let a=u.ports.map(e=>v[e]);if(a.some((x,j)=>x>=0&&x!==((w>>j)&1)))continue;u.ports.forEach((e,j)=>v[e]=(w>>j)&1);walk(i+1,i===root?(w&1):tag);u.ports.forEach((e,j)=>v[e]=a[j])}}walk(0,0);
    let words=[...support.keys()];treeStats.words+=words.length;
    if(root>=0){treeStats.branch++;let best=Infinity,A=0,B=0;for(let a of words.filter(w=>support.get(w)&1))for(let b of words.filter(w=>support.get(w)&2)){let p=pop(a^b);if(p<best){best=p;A=a;B=b}}ok(best>=3&&best<Infinity);let diff=A^B;for(let i=0;i<boundary.length;i++)if(diff>>i&1){ok(!support.has(A^(1<<i)));for(let j=0;j<boundary.length;j++)if(j!==i&&(diff>>j&1)){treeStats.exchangeChecks++;ok(!support.has(A^(1<<i)^(1<<j)))}}if(treeStats.examples.length<3)treeStats.examples.push({nodes,boundary,A,B,distance:best,words:words.length});
    }else{treeStats.nonbranch++;for(let l=0;l<100;l++){let a=words[rand(words.length)],b=words[rand(words.length)],d=a^b;for(let i=0;i<boundary.length;i++)if(d>>i&1){treeStats.exchangeChecks++;ok(Array.from({length:boundary.length},(_,j)=>j).some(j=>j!==i&&(d>>j&1)&&support.has(a^(1<<i)^(1<<j))))}}}
  }
  let scans=0,probes=0;function prop(F,n,pin=[]){let a=Array(n).fill(-1);for(let [v,b] of pin){if(a[v]>=0&&a[v]!==b)return null;a[v]=b}let change=true;while(change){change=false;for(let c of F){scans++;let s=c.reduce((s,x)=>s+(a[x]===1),0),u=c.filter(x=>a[x]<0);if(s>2||s+u.length<2)return null;if(s===2||s+u.length===2){let b=s===2?0:1;for(let x of u){a[x]=b;change=true}}}}return a}
  function closure(F,n){let pins=[],a;while(true){a=prop(F,n,pins);if(!a)return {status:"NO",pins};let next=null;for(let i=0;i<n;i++)if(a[i]<0){probes+=2;let l=prop(F,n,[...pins,[i,0]]),r=prop(F,n,[...pins,[i,1]]);if(!l&&!r)return {status:"NO",pins};if(!l||!r){next=[i,l?0:1];break}}if(!next)return {status:"OPEN",pins,free:a.filter(x=>x<0).length};pins.push(next)}}
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const valid=(F,a)=>F.every(c=>c.reduce((s,x)=>s+a[x],0)===2);
  function reference(F,n){let c=0;for(let a=0;a<2**n;a++)if(F.every(r=>r.reduce((s,x)=>s+((a>>x)&1),0)===2))c++;return c}
  let controls=[],chartStats={pairs:0,branches:0,yes:0,imperfectRescues:0,relaxedModelsSampled:0};
  function chartTest(F,n){
    let occ=Array.from({length:n},()=>[]);F.forEach((c,i)=>c.forEach((v,j)=>occ[v].push(4*i+j)));
    let groups=[],owners=Array.from({length:n},()=>[]),of=[];
    occ.forEach((o,i)=>{for(let j=0;j<o.length;j+=2){let g=o.slice(j,j+2),k=groups.length;groups.push(g);owners[i].push(k);g.forEach(e=>of[e]=k)}});
    let Q=F.map((c,i)=>c.map((_,j)=>of[4*i+j])),models=[]; // exhaustive reference on small split source
    function dfs(pins){if(models.length>=512)return;let a=prop(Q,groups.length,pins);if(!a)return;let v=a.indexOf(-1);if(v<0){models.push(a);return}dfs([...pins,[v,0]]);dfs([...pins,[v,1]])}dfs([]);
    chartStats.relaxedModelsSampled+=models.length;
    const m=F.length,base=6*m,dummy=new Map;let D=[];groups.forEach((g,i)=>{if(g.length===1){dummy.set(i,base+D.length);D.push(base+D.length)}});if(D.length%2)D.push(base+D.length);
    let size=base+D.length;let ports=e=>6*Math.floor(e/4)+e%4;
    let links=groups.map((g,i)=>[ports(g[0]),g.length===2?ports(g[1]):dummy.get(i)]);
    const make=a=>{let mt=Array(size).fill(-1);function link(u,v){ok(mt[u]<0&&mt[v]<0);mt[u]=v;mt[v]=u}a.forEach((b,i)=>{if(b)link(...links[i])});for(let i=0;i<m;i++){let free=[0,1,2,3].filter(j=>mt[6*i+j]<0);ok(free.length===2);free.forEach((j,k)=>link(6*i+j,6*i+4+k))}let free=D.filter(v=>mt[v]<0);ok(free.length%2===0);for(let j=0;j<free.length;j+=2)link(free[j],free[j+1]);ok(mt.every((v,i)=>v>=0&&mt[v]===i));return mt};
    const bits=mt=>links.map(([u,v])=>+(mt[u]===v)),good=a=>owners.every(o=>o.every(i=>a[i]===a[o[0]])), lift=a=>owners.map(o=>o.length?a[o[0]]:0);
    let matchings=models.map(make);let local={sampled:models.length,pairs:0,yes:0,rescues:0};
    for(let p=0;p<160&&models.length;p++){let i=rand(models.length),j=rand(models.length),A=matchings[i],B=matchings[j],cycle=Array(size).fill(-1),parts=[];for(let u=0;u<size;u++)if(A[u]!==B[u]&&cycle[u]<0){let v=u,part=[];do{cycle[v]=parts.length;part.push(v);let w=A[v];cycle[w]=parts.length;part.push(w);v=B[w]}while(v!==u);parts.push(part)}
      let a=bits(A),b=bits(B),q=parts.length;ok(q<20);let eq=[];for(let o of owners)for(let t=1;t<o.length;t++){let x=o[0],y=o[t],mask=0;if(a[x]!==b[x])mask^=1<<cycle[links[x][0]];if(a[y]!==b[y])mask^=1<<cycle[links[y][0]];eq.push([mask,a[x]^a[y]])}
      // independent Gaussian elimination, then construct actual combined matching
      let basis=Array(q).fill(null),pass=true;for(let [mask,r] of eq){for(let t=q-1;t>=0;t--)if(mask>>t&1){if(basis[t]){mask^=basis[t][0];r^=basis[t][1]}else{basis[t]=[mask,r];mask=0;r=0;break}}if(!mask&&r){pass=false;break}}
      let sol=0;if(pass)for(let t=0;t<q;t++)if(basis[t]){let [mask,r]=basis[t];if((pop(mask&sol)&1)!==r)sol|=1<<t}
      let brute=false;for(let s=0;s<2**q;s++){chartStats.branches++;let M=A.map((v,u)=>cycle[u]>=0&&(s>>cycle[u]&1)?B[u]:v);let w=bits(M);if(good(w)){ok(valid(F,lift(w)));brute=true}}
      ok(pass===brute);if(pass){let M=A.map((v,u)=>cycle[u]>=0&&(sol>>cycle[u]&1)?B[u]:v),w=bits(M);ok(good(w)&&valid(F,lift(w)));local.yes++;chartStats.yes++;if(!good(a)&&!good(b)){local.rescues++;chartStats.imperfectRescues++}}
      local.pairs++;chartStats.pairs++;
    }return local
  }
  for(let sat of [false,true]){let F=fano.slice(sat?1:0).map((c,i)=>[...c,7+i]),n=7+F.length,models=reference(F,n);ok((models>0)===sat);let C=closure(F,n);ok(C.status!=="NO"||!sat);controls.push({name:sat?"Fano-minus-line":"Fano",n,m:F.length,models,closure:C,chart:chartTest(F,n)})}
  let lifts=[];for(let p of [5,11,23,47,97]){let F=[];for(let i=0;i<4;i++)for(let t=0;t<p;t++)F.push(Array.from({length:4},(_,j)=>j*p+(t+i*j)%p));let n=4*p,deg=Array(n).fill(0),pairs=new Set;for(let c of F){ok(new Set(c).size===4);c.forEach(x=>deg[x]++);for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){let k=c[i]+","+c[j];ok(!pairs.has(k));pairs.add(k)}}ok(deg.every(x=>x===4));let a=Array.from({length:n},(_,i)=>+(i<2*p));ok(valid(F,a)&&valid(F,a.map(x=>1-x)));let C=closure(F,n);ok(C.status==="OPEN"&&C.free===n);lifts.push({p,n,m:F.length,girthLower:6,closure:C})}
  return {seed:202611252214,checks,treeStats,controls,chartStats,lifts,scans,probes}
}
console.log(JSON.stringify(audit(),null,2));
