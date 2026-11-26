// C02-05. Independent exact signed quotient / guard / padding checks. Run node.
const audit = () => {
  const seeds = [
    {name:"C01-alternating",n:3,T:[[0,0,1],[2,1,1],[1,0,1],[2,1,0],[0,2,2],[0,2,0],[1,2,2],[1,0,2]]},
    {name:"C01-adjacent",n:4,T:[[1,0,1],[2,1,0],[2,1,1],[0,1,1],[2,0,0],[1,2,3],[3,0,0],[3,3,2],[3,2,3],[0,3,2]]},
    {name:"MF-U",n:3,T:["000","002","010","011","021","022","100","101","111","201","202","221"].map(s=>[...s].map(Number))}
  ]; seeds.push({name:"MF-V",n:3,T:[...seeds[2].T,[1,1,0]]});
  let checks=0;function ok(b){checks++;if(!b)throw Error("assertion "+checks);}
  const rowList=(T,n)=>{let r=Array.from({length:3*n},()=>[]);T.forEach((t,i)=>t.forEach((v,c)=>r[c*n+v].push(i)));return r;};
  const good=(r,w)=>r.every(s=>s.reduce((a,i)=>a+w[i],0)===1);
  const brute=(T,n)=>{let r=rowList(T,n),A=[];for(let b=0;b<2**T.length;b++){let w=T.map((_,i)=>(b>>i)&1);if(good(r,w))A.push(w);}return A;};
  function inflate(T,n,d){for(let j=0;j<d;j++){let old=T;T=[];old.forEach(([a,b,c],i)=>{let z=n+i;T.push([z,z,z],[a,z,z],[z,b,c]);});n+=old.length;}return {T,n};}
  function lift(w,d){for(let j=0;j<d;j++)w=w.flatMap(b=>[1-b,b,b]);return w;}
  function quotient(T,n){
    let rows=rowList(T,n),adj=T.map(()=>[]);
    for(let r of rows)if(r.length===2){adj[r[0]].push(r[1]);adj[r[1]].push(r[0]);}
    let c=T.map(()=>-1),s=T.map(()=>0),k=0;
    for(let i=0;i<T.length;i++)if(c[i]<0){c[i]=k;let Q=[i];while(Q.length){let u=Q.pop();for(let v of adj[u]){if(c[v]<0){c[v]=k;s[v]=1-s[u];Q.push(v);}else ok(s[v]!==s[u]);}}k++;}
    let E=new Map();for(let r of rows){let a=new Map(),b=1;for(let i of r){a.set(c[i],(a.get(c[i])||0)+(s[i]?-1:1));b-=s[i];}let R=[...a.entries()].filter(x=>x[1]).sort((a,b)=>a[0]-b[0]);if(!R.length)ok(b===0);else E.set(JSON.stringify([R,b]),[R,b]);}
    let W=[];for(let m=0;m<2**k;m++){if([...E.values()].every(([r,b])=>r.reduce((a,[i,w])=>a+w*((m>>i)&1),0)===b)){let w=c.map((i,j)=>((m>>i)&1)^s[j]);ok(good(rows,w));W.push(w);}}
    return {c,s,k,W};
  }
  // Complete local response, including arbitrary literal restrictions.
  for(let mask=0;mask<27;mask++){let a=mask,p=[];for(let i=0;i<3;i++){p.push(a%3-1);a=Math.floor(a/3);}
    let actual=[];for(let w=0;w<8;w++){let x=[w&1,(w>>1)&1,(w>>2)&1];if(x[0]+x[1]===1&&x[0]+x[2]===1&&p.every((b,i)=>b<0||x[i]===b))actual.push(x[1]);}
    let pred=[0,1].filter(b=>p.every((v,i)=>v<0||v===[1-b,b,b][i]));ok(JSON.stringify(actual.sort())===JSON.stringify(pred));}
  const scales=[];
  for(let base of seeds){let words=brute(base.T,base.n);for(let d of [0,1,2,3,4,5,6,7]){
    if(base.name.startsWith("MF")&&d===7)continue;
    let {T,n}=inflate(base.T,base.n,d),q=quotient(T,n),expected=words.map(w=>lift(w,d));
    ok(new Set(T.map(t=>t.join(","))).size===T.length);ok(q.k<=base.T.length);
    ok(q.W.length===expected.length);let actualSet=new Set(q.W.map(w=>w.join("")));
    for(let w of expected){ok(actualSet.has(w.join("")));ok(good(rowList(T,n),w));}
    let guardChecks=0;for(let j=0;j<Math.min(24,T.length);j++){
      let i=(37*j+11)%T.length,l=(53*j+5)%T.length,b=j%2,b2=(j>>1)&1;
      let want=expected.some(w=>w[i]===b&&w[l]===b2),got=q.W.some(w=>w[i]===b&&w[l]===b2);
      ok(want===got);guardChecks++;
    }
    scales.push({source:base.name,d,triples:T.length,classes:q.k,covers:q.W.length,guardChecks});
  }}
  // Exact integer checks of the padding exponent bound for the whole parameter range.
  for(let m=1;m<=100;m++){let p=1;while(p<m)p*=3;for(let h=1;h<=6;h++){let M=BigInt(m)*BigInt(p)**BigInt(h);ok(BigInt(m)**BigInt(h+1)<=M);ok(M<=3n**BigInt(h)*BigInt(m)**BigInt(h+1));}}
  return {checks,scales};
};
console.log(JSON.stringify(audit(),null,2));
