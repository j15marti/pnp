"use strict";
function BW09() {
  "use strict";
  const out={seed:1509,assertions:0,states:0,composition_checks:0,random_fibers:0,random_sat:0,random_unsat:0,cube:{sat:0,unsat:0},fano:{sat:0,unsat:0,counts:[]},graph_controls:[],gaussian_calls:0,gaussian_xors:0,event_probes:0,closure_sweeps:0,forced_pins:0,search_nodes:0,dp_calls:0,dp_checks:0,witnesses:0};
  const chk=(v,m)=>{out.assertions++;if(!v)throw Error(m)};
  let seed=out.seed;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
  const vals=[0,1,2,3], bits=m=>vals.filter(x=>m&(1<<x));
  const list=(a,b)=>15&~((1<<a)|(1<<b));
  // Independent reachability and actual lift.
  function dp(sites,p,q,end=0){
    out.dp_calls++;let R=new Map([[p,[]]]);
    for(const [a,b,s] of sites){const T=new Map();
      for(const [x,history] of R)for(const y of bits(list(a,b))){out.dp_checks++;if((x^y)!==s&&!T.has(y))T.set(y,history.concat(y));}
      R=T;
    }
    for(const [x,history] of R)if((x^q)!==end){let prev=p;for(let i=0;i<sites.length;i++){const [a,b,s]=sites[i],y=history[i];chk(y!==a&&y!==b&&(prev^y)!==s,"lift");prev=y;}chk((prev^q)!==end,"last");return history;}
    return null;
  }
  const leaf=([a,b,s])=>{if(a===b)return [0,0];let D=0;for(const x of vals)if(bits(list(a,b)).includes(x^s))D|=1<<x;return [D,s^a^b]};
  const compose=([D,t],[E,u])=>{let mask=0;for(const x of bits(D))if(E&(1<<(x^t)))mask|=1<<x;return [mask,mask?(t^u):0]};
  const key=s=>s.join(",");
  const reps=new Map();for(const a of vals)for(const b of vals)for(const s of vals){const path=[[a,b,s]],v=leaf(path[0]);reps.set(key(v),{v,path});}
  const initial=[...reps.values()];for(const x of initial)for(const y of initial){const v=compose(x.v,y.v);reps.set(key(v),{v,path:x.path.concat(y.path)});}
  out.states=reps.size;chk(out.states===41,"41 states");
  for(const a of reps.values())for(const b of reps.values()){const v=compose(a.v,b.v);const sites=a.path.concat(b.path);for(const p of vals)for(const q of vals){const bad=Boolean(v[0]&(1<<p))&&((p^v[1])===q);chk((dp(sites,p,q)===null)===bad,"composition");out.composition_checks++;}}
  for(const a of reps.values())for(const b of reps.values())if(key(a.v)!==key(b.v)){chk(vals.some(p=>vals.some(q=>(Boolean(a.v[0]&(1<<p))&&(p^a.v[1])===q)!==(Boolean(b.v[0]&(1<<p))&&(p^b.v[1])===q))),"distinguish");}
  // Affine bit expressions: bit 0 constant; bit i+1 coefficient of x_i.
  const bit=i=>1n<<BigInt(i+1), con=x=>[BigInt(x&1),BigInt((x>>1)&1)], add=(a,b)=>[a[0]^b[0],a[1]^b[1]];
  function parity(x){let p=0;while(x){x&=x-1n;p^=1;}return p;}
  const ev=(f,z)=>parity(f&(1n|(z<<1n))), word=(w,z)=>ev(w[0],z)+2*ev(w[1],z);
  function solve(rows,n){out.gaussian_calls++;const piv=new Map();for(let f of rows){while(f>1n){let j=f.toString(2).length-1;if(piv.has(j)){f^=piv.get(j);out.gaussian_xors++;}else{piv.set(j,f);break;}}if(f===1n)return null;}
    let z=0n;for(const j of [...piv.keys()].sort((a,b)=>a-b)){if(ev(piv.get(j),z))z|=1n<<BigInt(j-1);}return z;
  }
  function events(path){let c=path.p;const E=[];for(const [a,b,s] of path.sites){let d=add(a,b),f=add(c,s);E.push(d,add(f,a),add(f,b));c=add(f,d);}
    let last=add(add(c,path.end),path.q);E.push([last[0]^1n],[last[1]^1n]);return E;
  }
  function oracle(path,G,n){for(const e of path.E){out.event_probes++;let z=solve(G.concat(e),n);if(z!==null)return z;}return null;}
  function lift(path,z){const ss=path.sites.map(site=>site.map(w=>word(w,z)));return dp(ss,word(path.p,z),word(path.q,z),word(path.end,z));}
  function mk(sites,p=con(0),q=con(0),end=con(0)){let o={sites,p,q,end};o.E=events(o);return o;}
  for(let t=0;t<240;t++){const n=5,randbit=()=>BigInt(rnd(1<<(n+1))),rw=()=>[randbit(),randbit()],m=1+rnd(6),path=mk(Array.from({length:m},()=>[rw(),rw(),rw()]),rw(),rw(),rw()),G=Array.from({length:rnd(5)},randbit);
    let count=0;for(let i=0;i<(1<<n);i++){let z=BigInt(i);if(G.some(f=>ev(f,z)))continue;let yes=lift(path,z)!==null;chk(yes===path.E.some(e=>e.every(f=>!ev(f,z))),"affine events");count+=Number(yes);}
    let w=oracle(path,G,n);chk((w!==null)===(count>0),"fiber");if(w!==null){chk(G.every(f=>!ev(f,w))&&lift(path,w)!==null,"oracle lift");out.witnesses++;out.random_sat++;}else out.random_unsat++;out.random_fibers++;
  }
  // Every literal is a false-event bit. Duplicate sites restore forced color 0.
  function clause(lits){let sites=[];for(const [i,neg] of lits){const f=bit(i)^BigInt(neg?0:1);sites.push([ [0n,f],[1n,f],con(0) ],[ [1n,f],[0n,f],con(0) ]);}return mk(sites);}
  function close(paths,G,n){G=G.slice();restart:while(true){out.closure_sweeps++;if(solve(G,n)===null)return null;
    for(const p of paths)if(oracle(p,G,n)===null)return null;
    for(let i=0;i<n;i++){let h=bit(i);if(solve(G.concat(h),n)===null||solve(G.concat(h^1n),n)===null)continue;
      for(const p of paths){const a=oracle(p,G.concat(h),n),b=oracle(p,G.concat(h^1n),n);if(a===null||b===null){if(a===null&&b===null)return null;G.push(a===null?h^1n:h);out.forced_pins++;continue restart;}}
    }return G;
  }}
  function count(paths,G,n){out.search_nodes++;G=close(paths,G,n);if(G===null)return {count:0,w:null};let z=solve(G,n);
    for(let i=0;i<n;i++){let h=bit(i);if(solve(G.concat(h),n)!==null&&solve(G.concat(h^1n),n)!==null){let a=count(paths,G.concat(h),n),b=count(paths,G.concat(h^1n),n);return {count:a.count+b.count,w:a.w??b.w};}}
    chk(paths.every(p=>lift(p,z)!==null),"source leaf");return {count:1,w:z};
  }
  function bench(lits,n){const paths=lits.map(clause);const r=count(paths,[],n);let ref=0;for(let j=0;j<1<<n;j++){const z=BigInt(j);const legal=lits.every(c=>c.some(([i,neg])=>Boolean((j>>i)&1)!==Boolean(neg)));chk(legal===paths.every(p=>p.E.some(e=>e.every(f=>!ev(f,z)))),"clause compiler");ref+=Number(legal);}
    chk(r.count===ref,"count");if(r.w!==null){chk(paths.every(p=>lift(p,r.w)!==null),"combined witness");out.witnesses++;}return ref;}
  const cube=Array.from({length:8},(_,j)=>Array.from({length:3},(_,i)=>[i,(j>>i)&1]));
  for(let m=0;m<256;m++){const c=bench(cube.filter((_,i)=>m&(1<<i)),3);out.cube[c?"sat":"unsat"]++;}
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].flatMap(t=>[t.map(i=>[i,0]),t.map(i=>[i,1])]);
  for(let k=-1;k<14;k++){const c=bench(fano.filter((_,i)=>i!==k),7);chk(c===(k<0?0:5),"Fano reference");out.fano[c?"sat":"unsat"]++;out.fano.counts.push(c);}
  // Graph 4-coloring reduction to non-universal extension of a single pinned odd rim.
  // T(d0,d1)=(d1,d0+d1), order 3; det(d,Td)=1 iff d nonzero.
  for(const [n,omit] of [[4,false],[5,false],[5,true]]){let edges=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(!(omit&&u===0&&v===1))edges.push([u,v]);
    const sites=[];for(const [u,v] of edges){const d=[bit(2*u)^bit(2*v),bit(2*u+1)^bit(2*v+1)],td=[d[1],d[0]^d[1]];for(const f of [con(0),d]){let a=add(f,td);sites.push([a,add(a,d),con(0)]);}}
    const path=mk(sites);let bad=0;for(let j=0;j<(1<<(2*n));j++){const z=BigInt(j),proper=edges.every(([u,v])=>((j>>(2*u))&3)!==((j>>(2*v))&3));const fails=lift(path,z)===null;chk(fails===proper,"graph reduction");chk(fails===!path.E.some(e=>e.every(f=>!ev(f,z))),"graph event");bad+=Number(fails);}
    out.graph_controls.push({n,omit,edges:edges.length,rim:sites.length+1,assignments:1<<(2*n),bad,universal_safe:bad===0});
  }
  return out;
}
console.log(JSON.stringify(BW09(),null,2));
