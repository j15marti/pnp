const experiment = function experiment(){
  let seed=171124, st={systems:0,referenceMatchings:0,targets:0,sat:0,unsat:0,assertions:0,closureQueries:0,forced:0,absent:0,witnesses:0,initialForced:0,initialAbsent:0,strictRank:0,maxRawLocal:0,maxLocal:0,maxRawShared:0,maxShared:0,localMatchings:0,skeletonMatchings:0,convolutions:0,scaling:[]};
  function ck(x){st.assertions++;if(!x)throw Error("assert "+st.assertions);}
  function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n);}
  const bit=i=>1n<<BigInt(i);
  const key=(t,h)=>t.toString()+":"+h;
  function basis(xs){let a=[];for(let x of xs){for(let b of a)if((x^b)<x)x^=b;if(x){a.push(x);a.sort((a,b)=>a>b?-1:a<b?1:0);}}return a;}
  function rem(x,b){for(let y of b)if((x^y)<x)x^=y;return x;}
  function xor(a){return a.reduce((x,y)=>x^y,0n);}
  function deps(A,B){let piv=[],out=[];for(let i=0;i<A.length+B.length;i++){let x=i<A.length?A[i]:B[i-A.length],c=bit(i);for(let [v,w] of piv)if((x^v)<x){x^=v;c^=w;}if(x){piv.push([x,c]);piv.sort((a,b)=>a[0]>b[0]?-1:1);}else out.push(xor(A.filter((v,j)=>(c&bit(j))!==0n)));}return basis(out);}
  function coordinates(x,bs){let piv=[];for(let i=0;i<bs.length;i++){let v=bs[i],c=bit(i);for(let [y,z] of piv)if((v^y)<v){v^=y;c^=z;}ck(v!==0n);piv.push([v,c]);piv.sort((a,b)=>a[0]>b[0]?-1:1);}let c=0n;for(let [v,z] of piv)if((x^v)<x){x^=v;c^=z;}return x?null:c;}
  function enumerate(vertices,edges){if(!vertices.length)return [[]];let v=vertices[0],out=[];for(let e of edges){let w=e.a===v?e.b:e.b===v?e.a:-1;if(w>=0&&vertices.includes(w))for(let M of enumerate(vertices.filter(x=>x!==v&&x!==w),edges))out.push([e,...M]);}return out;}
  function total(M){return [xor(M.map(e=>e.t)),M.reduce((a,e)=>a+e.h,0)];}
  function add(map,t,h,n,w){let k=key(t,h),v=map.get(k);if(v)v.n+=n;else map.set(k,{t,h,n,w});}
  function shared(U){return basis([...U[0],...U.slice(1).flatMap((u,j)=>deps(u,basis(U.filter((v,i)=>i!==j+1).flat())))]);}
  function normalize(E,V,shore,ref){
    let used=new Set(ref.flatMap(M=>M.map(e=>e.id)));
    let forced=E.filter(e=>ref.every(M=>M.includes(e)));st.initialForced+=forced.length;st.initialAbsent+=E.length-used.size;
    E=E.filter(e=>used.has(e.id));
    let s=shore.length,owner=v=>Math.floor(v/5);
    let local=Array.from({length:s},()=>new Map()),internal=shore.map((S,i)=>E.filter(e=>owner(e.a)===i&&owner(e.b)===i));
    let cut=E.filter(e=>owner(e.a)!==owner(e.b));
    let K=[];
    for(let e of cut){let a=owner(e.a),b=owner(e.b);
      for(let [i,p] of [[a,e.a],[b,e.b]]){
        let ms=enumerate(shore[i].filter(v=>v!==p),internal[i]);ck(ms.length>0);st.localMatchings+=ms.length;
        let b0=total(ms[0])[0],U=basis(ms.map(M=>total(M)[0]^b0));
        let ms2=ms.map(M=>{let [t,h]=total(M);let t2=xor(M.map(e=>e.t^rem(e.t,U)))^(b0^rem(b0,U));ck(t2===(t^b0));return {t:t2,h,ids:M.map(e=>e.id)};});
        local[i].set(e.id,{b0,U,ms:ms2});
      }
      K.push({...e,a,b,t:e.t^local[a].get(e.id).b0^local[b].get(e.id).b0});
    }
    let km=enumerate(Array.from({length:s},(_,i)=>i),K);st.skeletonMatchings+=km.length;ck(km.length>0);
    let base=total(km[0])[0],U0=basis(km.map(M=>total(M)[0]^base)),U=[U0,...local.map(L=>basis([...L.values()].flatMap(v=>v.U)))];
    let W=shared(U),B=[...W],groups=[];
    for(let i=1;i<U.length;i++){let start=B.length;for(let x of U[i])if(rem(x,basis(B)))B.push(x);groups.push([start,B.length]);}
    ck(B.length===basis(U.flat()).length);
    let raw=[basis(cut.map(e=>e.t)),...internal.map(es=>basis(es.map(e=>e.t)))],rawC=Math.max(...raw.slice(1).map(u=>u.length)),c=Math.max(...local.flatMap(L=>[...L.values()].map(v=>v.U.length))),rawR=shared(raw).length,r=W.length;
    st.maxRawLocal=Math.max(st.maxRawLocal,rawC);st.maxLocal=Math.max(st.maxLocal,c);st.maxRawShared=Math.max(st.maxRawShared,rawR);st.maxShared=Math.max(st.maxShared,r);if(rawC>c||rawR>r)st.strictRank++;
    let wm=bit(r)-1n,pm=groups.map(([a,b])=>(bit(b)-1n)^(bit(a)-1n));
    for(let i=0;i<s;i++)for(let v of local[i].values())for(let m of v.ms){m.coord=coordinates(m.t,B);ck(m.coord!==null);ck((m.coord&~(wm|pm[i]))===0n);}
    let ks=km.map(M=>{let [t,h]=total(M),t2=xor(M.map(e=>e.t^rem(e.t,U0)))^(base^rem(base,U0));ck(t2===(t^base));let z=coordinates(t2,B);ck(z!==null&&(z&~wm)===0n);return {M,z,h};});
    function query(t,h,ban=new Set()){
      let target=coordinates(t^base,B);if(target===null)return {n:0,w:[]};
      let n=0,w=[];
      for(let k of ks){if(k.M.some(e=>ban.has(e.id)))continue;
        let D=new Map();add(D,k.z,k.h,1,k.M.map(e=>e.id));
        for(let i=0;i<s;i++){let edge=k.M.find(e=>e.a===i||e.b===i),L=local[i].get(edge.id),C=new Map();
          for(let m of L.ms)if((m.coord&pm[i])===(target&pm[i])&&!m.ids.some(id=>ban.has(id)))add(C,m.coord&wm,m.h,1,m.ids);
          let D2=new Map();for(let a of D.values())for(let b of C.values()){st.convolutions++;add(D2,a.t^b.t,a.h+b.h,a.n*b.n,a.w.concat(b.w));}D=D2;
        }
        let a=D.get(key(target&wm,h));if(a){n+=a.n;w=a.w;}
      }return {n,w};
    }
    return {query,c,r,rawC,rawR};
  }
  for(let test=0;test<60;test++){
    let s=test%3===0?6:4,V=Array.from({length:5*s},(_,i)=>i),shore=Array.from({length:s},(_,i)=>V.slice(5*i,5*i+5)),E=[];
    let gauge=V.map((v)=>bit(12+v%5)^bit(20+v)),addE=(a,b,t,h)=>E.push({a,b,t:t^gauge[a]^gauge[b],h,id:E.length});
    for(let i=0;i<s;i++){let [r,a,b,c,d]=shore[i];addE(r,a,BigInt(rnd(16)),rnd(5)-2);for(let [u,v] of [[a,b],[a,c],[a,d],[b,c],[b,d],[c,d]])addE(u,v,BigInt(rnd(16))^ (rnd(2)?bit(5+i):0n),rnd(5)-2);}
    for(let i=0;i<s;i++){let j=(i+1)%s;addE(shore[i][rnd(2)?0:2],shore[j][rnd(2)?0:2],BigInt(rnd(16)),rnd(5)-2);}
    let ref=enumerate(V,E);ck(ref.length>0);st.systems++;st.referenceMatchings+=ref.length;
    for(let M of ref)for(let i=0;i<s;i++)ck(M.filter(e=>(shore[i].includes(e.a))!==shore[i].includes(e.b)).length===1);
    let z=normalize(E,V,shore,ref),lookup=new Map();for(let M of ref){let [t,h]=total(M);add(lookup,t,h,1,M.map(e=>e.id));}
    let vals=[...lookup.values()];
    for(let k=0;k<12;k++){let a=vals[rnd(vals.length)],t=a.t,h=a.h;if(k%3===1)t^=bit(rnd(12));if(k%3===2)h+=1+rnd(3);
      let expect=lookup.get(key(t,h))?.n??0,got=z.query(t,h);ck(expect===got.n);st.targets++;if(got.n){st.sat++;let M=got.w.map(id=>E[id]);ck(new Set(M.flatMap(e=>[e.a,e.b])).size===V.length&&M.length*2===V.length);let [u,v]=total(M);ck(u===t&&v===h);st.witnesses++;}else st.unsat++;
    }
    let a=vals[rnd(vals.length)],fiber=ref.filter(M=>{let[t,h]=total(M);return t===a.t&&h===a.h;});
    let ban=new Set(),pins=new Map(),changed=true;while(changed){changed=false;for(let e of E){if(pins.has(e.id))continue;let no=new Set([...ban,e.id]),yes=new Set([...ban,...E.filter(f=>f.id!==e.id&&[f.a,f.b].some(v=>v===e.a||v===e.b)).map(f=>f.id)]);let n=z.query(a.t,a.h,no).n,y=z.query(a.t,a.h,yes).n;st.closureQueries+=2;
      ck(n===fiber.filter(M=>!M.includes(e)).length);ck(y===fiber.filter(M=>M.includes(e)).length);
      if(!n){pins.set(e.id,1);st.forced++;ban=yes;changed=true;break;}if(!y){pins.set(e.id,0);st.absent++;ban=no;changed=true;break;}
    }}ck(z.query(a.t,a.h,ban).n===fiber.length);
  }
  // Gauge-inflated exact analytic controls: two shores, k K4 blocks per shore,
  // one crossing selector, every block has three matchings. Only first block
  // carries two private bits, others have gauge-only tags. Calculate local
  // three-match supports by actual K4 enumeration and compose their counts.
  for(let k of [1,4,16,64]){
    let raw=[],U=[],base=0n,counts=new Map();add(counts,0n,0,1n,[]);
    for(let j=0;j<k;j++){let E=[],g=Array.from({length:4},(_,v)=>bit(8+4*j+v));
      for(let [a,b] of [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])E.push({a,b,t:g[a]^g[b]^(j===0&&a===0?(b===1?1n:b===2?2n:0n):0n),h:0});
      raw.push(...E.map(e=>e.t));let ms=enumerate([0,1,2,3],E).map(M=>total(M)[0]),b0=ms[0];base^=b0;U.push(...ms.map(t=>t^b0));
      let D=new Map();for(let a of counts.values())for(let t of ms)add(D,a.t^t,0,a.n,[]);counts=D;
    }
    ck(counts.size===3);let n=[...counts.values()].reduce((a,b)=>a+b.n,0n);ck(n===3n**BigInt(k));
    let tags=[...counts.values()].map(v=>v.t),missing=tags[0]^tags[1]^tags[2];ck(!counts.has(key(missing,0)));
    st.scaling.push({blocksPerShore:k,rawLocalRank:basis(raw).length,localVariationRank:basis(U).length,localMatchings:n.toString(),satControl:true,unsatControl:true});
  }
  return st;
};
console.log(JSON.stringify(experiment(), null, 2));
