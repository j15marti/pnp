function audit(){
  let checks=0;const ok=(b)=>{checks++;if(!b)throw Error("assertion "+checks)};
  const pop=x=>{let n=0;while(x){n+=x&1;x>>>=1}return n};
  let seed=0x731cab09;const rnd=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0};
  function source(k,b){
    const V=k*k,ports=Array.from({length:V},()=>[]),edges=[],map=new Map();
    for(let r=0;r<k;r++)for(let c=0;c<k;c++){
      const v=r*k+c;for(let p=0;p<4;p++){
        const [dr,dc]=[[-1,0],[0,1],[1,0],[0,-1]][p],rr=r+dr,cc=c+dc;
        const w=rr>=0&&rr<k&&cc>=0&&cc<k?rr*k+cc:-1;
        const key=w<0?`b:${v}:${p}`:`${Math.min(v,w)}:${Math.max(v,w)}`;
        if(!map.has(key)){
          const a=w>=0&&(dr===0||c===0||c===k-1||((Math.min(r,rr)+c)%2===0));
          map.set(key,edges.length);edges.push({ends:[],a,bound:w<0&&(p===0||p===2)?(p===2?1:0):null,base:w<0&&p===2?1:0});
        }
        const e=map.get(key);ports[v][p]=e;edges[e].ends.push([v,p]);
      }
    }
    let masks=[],fixed=[];
    for(let v=0;v<V;v++){
      const f=ports[v].findIndex(e=>!edges[e].a);fixed.push(f);ok(f>=0);
      let m=0;for(let w=0;w<16;w++){
        let parity=0;for(let p=0;p<4;p++)if(edges[ports[v][p]].a)parity^=(w>>(3-p))&1;
        if(parity===b[v]&&((w>>(3-f))&1)===edges[ports[v][f]].base)m|=1<<w;
      }
      ok(pop(m)===4);masks.push(m);
    }
    let hash=2166136261;for(const m of masks){hash=Math.imul(hash^(m&255),16777619);hash=Math.imul(hash^(m>>>8),16777619)}
    return {k,V,ports,edges,masks,fixed,hash:(hash>>>0).toString(16).padStart(8,"0")};
  }
  function tree(s,b){
    const {V,edges,ports}=s,pa=new Int32Array(V).fill(-1),pe=new Int32Array(V).fill(-1),order=[0];pa[0]=0;
    for(let j=0;j<order.length;j++){let v=order[j];for(const e of ports[v])if(edges[e].a){let w=edges[e].ends.find(t=>t[0]!==v)[0];if(pa[w]<0){pa[w]=v;pe[w]=e;order.push(w)}}}
    ok(order.length===V);const a=edges.map(e=>e.base),res=b.slice();
    for(let j=V-1;j>0;j--){const v=order[j];a[pe[v]]=res[v];res[pa[v]]^=res[v]}
    if(res[0])return null;
    for(let v=0;v<V;v++){let w=0;for(const e of ports[v])w=(w<<1)|a[e];ok((s.masks[v]&(1<<w))!==0)}
    for(let e=0;e<edges.length;e++)if(edges[e].bound!==null)ok(a[e]===edges[e].bound);
    return a;
  }
  function closure(s){
    const {edges,ports,V}=s,m=s.masks.slice(),d=edges.map(e=>e.bound===null?3:1<<e.bound);
    let changed=true,rounds=0,scans=0;
    while(changed){changed=false;rounds++;for(let v=0;v<V;v++){
      scans++;let keep=0,poss=[0,0,0,0];
      for(let w=0;w<16;w++)if(m[v]&(1<<w)){let yes=true;for(let p=0;p<4;p++)if(!(d[ports[v][p]]&(1<<((w>>(3-p))&1))))yes=false;
        if(yes){keep|=1<<w;for(let p=0;p<4;p++)poss[p]|=1<<((w>>(3-p))&1)}}
      if(!keep)return {sat:false,rounds,scans};
      if(keep!==m[v]){m[v]=keep;changed=true}
      for(let p=0;p<4;p++){let e=ports[v][p],z=d[e]&poss[p];if(z!==d[e]){d[e]=z;changed=true}}
    }}
    let full=0;for(let e=0;e<edges.length;e++)if(edges[e].a){ok(d[e]===3);full++}
    return {sat:true,rounds,scans,full};
  }
  function global(s){
    // Decode sign from membership only, not supplied charge vector.
    let even=1,odd=0;
    for(let v=0;v<s.V;v++){
      const f=s.fixed[v],w=s.edges[s.ports[v][f]].base<<(3-f),e=(s.masks[v]>>w)&1;
      // alternate rail is any one active bit flipped
      const p=s.ports[v].findIndex(i=>s.edges[i].a),o=(s.masks[v]>>(w^(1<<(3-p))))&1;
      ok(e+o===1);[even,odd]=[(even&e)|(odd&o),(even&o)|(odd&e)];
    }return even===1;
  }
  function frontier(s,cap){
    const k=s.k; if(k>8)return {value:null,steps:0};
    let states=new Set([0]),steps=0;
    for(let r=0;r<k;r++)for(let c=0;c<k;c++){
      const next=new Set(),m=s.masks[r*k+c];
      for(const st of states)for(let w=0;w<16;w++)if(m&(1<<w)){
        if(++steps>cap)return {value:null,steps};
        const n=(w>>3)&1,e=(w>>2)&1,b=(w>>1)&1,l=w&1,mask=st>>1,prev=st&1;
        if(n!==((mask>>c)&1)||(c>0&&l!==prev)||(r===k-1&&b!==1))continue;
        const nm=(mask&~(1<<c))|(b<<c);next.add((nm<<1)|(c===k-1?0:e));
      }states=next;if(!states.size)return {value:false,steps};
    }return {value:states.size>0,steps};
  }
  let rows=[],exhaustive=0,marginalChecks=0,frontierChecks=0,witnesses=0,closureNeg=0;
  function job(k,b){
    const original=source(k,b),a=JSON.stringify(original.masks),s1=source(k,b),s2=source(k,b);
    ok(a===JSON.stringify(s1.masks)&&a===JSON.stringify(s2.masks));
    const c=closure(original),ta=tree(s1,b),tb=global(s2),tc=frontier(original,(16*k*k)**3);
    const yes=!!ta;ok(yes===tb);ok(c.sat);if(!yes)closureNeg++;if(yes)witnesses++;
    if(tc.value!==null){ok(tc.value===yes);frontierChecks++}
    ok(yes===(b.reduce((x,y)=>x^y,0)===0));
    return {k,N:16*k*k,active:c.full,yes,hash:original.hash,closureRounds:c.rounds,closureScans:c.scans,frontier:tc};
  }
  for(let x=0;x<16;x++){let b=Array.from({length:4},(_,i)=>(x>>i)&1);job(2,b);exhaustive++}
  for(let mask=0;mask<15;mask++){const ev=new Map(),od=new Map();for(let x=0;x<16;x++){let m=pop(x)%2?od:ev;const key=x&mask;m.set(key,(m.get(key)||0)+1)}
    for(const [key,count] of ev){ok(od.get(key)===count);marginalChecks++}}
  for(const k of [4,6,8,16,32,64,128]){
    const b=Array.from({length:k*k},()=>rnd()&1);b[0]^=b.reduce((a,x)=>a^x,0);
    rows.push(job(k,b));const c=b.slice();c[Math.floor(c.length/2)]^=1;rows.push(job(k,c));
  }
  return {checks,exhaustive,marginalChecks,frontierChecks,witnesses,closureNeg,rows,seed:"0x731cab09",note:"Interleaved, cap N^3 frontier transitions for k<=8; larger frontier deliberately not run. FNV-1a over row-major 16-bit masks, not cryptographic. No machine/circuit/proof synthesis."};
}
console.log(JSON.stringify(audit(),null,2));
