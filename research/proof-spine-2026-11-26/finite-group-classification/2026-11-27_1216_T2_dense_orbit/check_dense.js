function check(R,out,four,verification){
 const n=R.free.length,C=1n<<BigInt(n),mask=C-1n,oldC=1n<<BigInt(R.original_root_positions.length),ob=R.free.map(s=>BigInt("0x"+s)),P=s=>BigInt("0x"+s),lo=x=>x&-x,hi=x=>1n<<BigInt(x.toString(2).length-1),par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 let ticks=0,checks=0,treeNodes=0,units=0;const norm=R=>{let a=R.slice(),k=0;for(let j=n-1;j>=0;j--){let p=1n<<BigInt(j),i=a.findIndex((r,i)=>i>=k&&Boolean(r&p));if(i<0)continue;[a[k],a[i]]=[a[i],a[k]];for(let l=0;l<a.length;l++)if(l!==k){ticks++;if(a[l]&p)a[l]^=a[k]}k++}if(a.slice(k).some(x=>x===C))return null;return a.slice(0,k)};
 const uniq=F=>[...new Map(F.filter(x=>x!==null).map(e=>[e.join(","),e])).values()], join=(A,B)=>A===null||B===null?null:norm([...A,...B]),count=(E,d)=>E===null?0n:1n<<BigInt(d-E.length),res=(e,b,v)=>norm(e.map(r=>r&b?r^b^(v?C:0n):r));
 function compress(s){let r=P(s),v=r&oldC?C:0n;ob.forEach((b,i)=>{if(r&b)v|=1n<<BigInt(i)});return v}
 let F=uniq(R.events.map(e=>norm(e.map(compress)))),active=mask;const size=()=>active.toString(2).replace(/0/g,"").length;
 const cond=(F,r,b)=>uniq(F.map(e=>norm(e.map(a=>a&b?a^r:a))));
 for(let s of out.trace){
  if(s.gauge){let G=s.gauge.map(P).reduce((a,b)=>a|b,0n);if((G&active)!==G||s.periods.length!==s.gauge.length)throw Error("bad gauge");s.periods.forEach((v,i)=>{let h=P(v);if((h&G)!==P(s.gauge[i])||(h&active)!==h||F.some(e=>e.some(r=>par((r&mask)&h))))throw Error("period")});F=uniq(F.map(e=>norm(e.map(r=>r&~G))));active&=~G}
  else if(s.unit){let r=P(s.unit),b=lo(r&mask);if(!F.some(e=>e.length===1&&e[0]===(r^C)))throw Error("unit");F=cond(F,r,b);active&=~b}
  else{let h=P(s.h),b=lo(h);if((h&active)!==h||!h)throw Error("direction");let S=F.map(e=>norm(e.map(r=>Boolean(r&b)!==Boolean(par((r&mask)&h))?r^b:r))),A=S.filter(e=>e.some(r=>r&b)),O=S.filter(e=>!e.some(r=>r&b));if(A.length!==s.t)throw Error("touch");
   for(let i=0;i<A.length;i++)for(let j=i+1;j<A.length;j++){
    let Q=norm([...A[i],...A[j].map(r=>r&b?r^C:r)]);if(Q!==null){let u=Q.find(r=>r&b);if(!u)throw Error("projection");Q=norm(Q.filter(r=>r!==u).map(r=>r&b?r^u:r))}
    let U=join(res(A[i],b,0),res(A[j],b,1)),V=join(res(A[i],b,1),res(A[j],b,0));for(let Z of [U,V])if(Z!==null&&(Q===null||Q.some(r=>norm([...Z,r^C])!==null)))throw Error("inclusion");let d=size()-1;if(count(Q,d)!==count(U,d)+count(V,d)-count(join(U,V),d))throw Error("coverage");checks++;if(Q!==null)O.push(Q)
   }F=uniq(O);active&=~b
  }
  if(size()!==s.d||F.length!==s.m)throw Error("size");
 }
 let A=new Set(F.map(e=>e.join(","))),B=new Set(uniq(out.events.map(e=>norm(e.map(P)))).map(e=>e.join(",")));if(A.size!==B.size||[...A].some(x=>!B.has(x)))throw Error("final");
 function ranks(o){let seen=new Set();return o.stop.groups.map(g=>{let B=new Map();for(let i of g){if(seen.has(i)||i<0||i>=o.events.length)throw Error("overlap");seen.add(i);for(let s of o.events[i]){let r=P(s)&((1n<<BigInt(o.n))-1n);while(r){let p=hi(r);if(B.has(p))r^=B.get(p);else{B.set(p,r);break}}}}if(B.size!==o.final.d)throw Error("rank");return B.size})}
 const ranks3=ranks(out),ranks4=ranks(four);
 // Verify four-stage reindexing itself, since refusal is in a different compact chart.
 let fb=out.free.map(P),c4=1n<<BigInt(fb.length), remap=x=>{let r=P(x),v=r&C?c4:0n;fb.forEach((p,i)=>{if(r&p)v|=1n<<BigInt(i)});return v};
 // Each row in remapped original is implied by a written four event, and vice versa.
 function span(rows){let m=new Map();for(let r of rows){while(r){let q=lo(r);if(m.has(q))r^=m.get(q);else{m.set(q,r);break}}}return m}
 const eq=(a,b)=>{let x=span(a),y=span(b);if(x.size!==y.size)return false;for(let r of a){while(r){let p=lo(r);if(!y.has(p))return false;r^=y.get(p)}}return true};
 if(four.trace.length!==0||out.events.length!==four.events.length||out.events.some((e,i)=>!eq(e.map(remap),four.events[i].map(P))))throw Error("four remapping");
 function walk(F,t,live){treeNodes++;for(let s of t.unit||[]){let r=P(s),b=hi(r&mask);if(!(b&live)||!F.some(e=>e.length===1&&e[0]===(r^C)))throw Error("tree unit");F=cond(F,r,b);live&=~b;units++}if(t.conflict){if(!F.some(e=>e.length===0))throw Error("tree conflict");return}let r=P(t.split),b=hi(r&mask);if(!(b&live)||r&C||!Array.isArray(t.children)||t.children.length!==2)throw Error("tree split");walk(cond(F,r,b),t.children[0],live&~b);walk(cond(F,r^C,b),t.children[1],live&~b)}
 walk(F,verification.branch.tree,active);
 return{ranks3,ranks4,orientationChecks:checks,treeNodes,units,ticks};
}
module.exports={check};
if(require.main===module){const fs=require('fs');const a=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));console.log(JSON.stringify(check(...a),null,2))}
