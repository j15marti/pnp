"use strict";
function audit(){
  let seed=26112604, assertions=0;
  const rnd=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)/4294967296};
  const ck=(x,msg)=>{assertions++;if(!x)throw Error(msg)};
  const bits=[8,4,2,1], all=Array.from({length:16},(_,i)=>i);
  function div(w,p){let a=!!(w&4)+!!(w&1),b=!!(w&8)+!!(w&2);return p?b-a:a-b}
  const dummy=[0,1].map(p=>all.filter(w=>div(w,p)>0).slice(0,3));
  const active=[0,1].map(p=>all.filter(w=>div(w,p)===0));
  ck(active.every(a=>a.length===6)&&dummy.every(a=>a.length===3),"catalogue");
  function generate(k,random=true){
    let w=new Uint8Array(k*k), f=[];
    for(let i=0;i<k-1;i++)for(let j=0;j<k-1;j++)if((i+j)%2===0){
      let b=random?+(rnd()<.5):0; f.push({i,j,b});
      if(b){w[i*k+j]|=6;w[i*k+j+1]|=3;w[(i+1)*k+j]|=12;w[(i+1)*k+j+1]|=9}
    }
    return {w,f};
  }
  function grid(k,w){
    let h=k+2,R=[];
    for(let i=0;i<h;i++)for(let j=0;j<h;j++){
      let mask;
      if(i>0&&i<h-1&&j>0&&j<h-1){
        let p=(i+j)%2,a=w[(i-1)*k+j-1];ck(active[p].includes(a),"balanced active");
        mask=[a,...dummy[p]]
      }else if(i===0&&j===0)mask=all.filter(x=>(x&9)===0);
      else if(i===0&&j===h-1)mask=all.filter(x=>(x&12)===0);
      else if(i===h-1&&j===0)mask=all.filter(x=>(x&3)===2);
      else if(i===h-1&&j===h-1)mask=all.filter(x=>(x&6)===2);
      else if(i===0)mask=all.filter(x=>(x&10)===0);
      else if(i===h-1)mask=all.filter(x=>(x&10)===2);
      else mask=all.filter(x=>(x&5)===0);
      ck(mask.length===4&&new Set(mask).size===4,"exact-four");
      R.push(mask)
    }
    return {h,k,R};
  }
  // Edges have stable IDs: horizontal grid interfaces H(i,j), vertical V(i,j).
  function geometry(h){
    let e=[],pin=new Map;
    const H=(i,j)=>i*(h+1)+j,V=(i,j)=>h*(h+1)+i*h+j;
    for(let i=0;i<h;i++)for(let j=0;j<h;j++)e.push([V(i,j),H(i,j+1),V(i+1,j),H(i,j)]);
    for(let j=0;j<h;j++){pin.set(V(0,j),0);pin.set(V(h,j),1)}
    return {e,pin,m:2*h*(h+1)};
  }
  function close(g,guards=[],charge=false){
    const {e,pin,m}=geometry(g.h),D=new Uint8Array(m).fill(3);
    for(const [i,b] of [...pin,...guards]){D[i]&=1<<b;if(!D[i])return {sat:false,forced:0}}
    let R=g.R.map(a=>a.slice()), changed=true,rounds=0;
    if(charge)for(let i=1;i<g.h-1;i++)for(let j=1;j<g.h-1;j++){
      let z=i*g.h+j;R[z]=R[z].filter(w=>div(w,(i+j)%2)===0)
    }
    while(changed){changed=false;rounds++;
      for(let v=0;v<R.length;v++){
        const t=R[v].filter(w=>e[v].every((q,i)=>D[q]&(1<<+(!!(w&bits[i])))));
        if(!t.length)return {sat:false,forced:D.filter(x=>x!==3).length,rounds};
        if(t.length!==R[v].length){R[v]=t;changed=true}
        for(let i=0;i<4;i++){
          let m=0;for(const w of t)m|=1<<+(!!(w&bits[i]));let q=e[v][i],a=D[q]&m;
          if(!a)return {sat:false,forced:0,rounds};if(a!==D[q]){D[q]=a;changed=true}
        }
      }
    }
    let values=Array.from(D,d=>d===2?1:0);
    let witness=e.map(a=>a.reduce((s,q,i)=>s+(values[q]?bits[i]:0),0));
    let valid=witness.every((w,i)=>g.R[i].includes(w))&&[...pin,...guards].every(([q,b])=>values[q]===b);
    if(charge)ck(valid,"charge lift");
    return {sat:true,forced:D.filter(x=>x!==3).length,rounds,valid};
  }
  // Independent native row-frontier feasibility, no conservation assumption.
  function frontier(g){
    let states=new Set([0]), h=g.h;
    for(let i=0;i<h;i++){
      let next=new Set;
      for(const n of states){
        let a=new Set([0,1]); // code: partial S bit mask *2 + west bit
        for(let j=0;j<h;j++){
          let b=new Set;
          for(const p of a)for(const w of g.R[i*h+j]){
            if(+(!!(w&8))!==((n>>j)&1)||+(!!(w&1))!==(p&1))continue;
            b.add(((p>>1)|((+(!!(w&2)))<<j))*2+(+(!!(w&4))))
          }
          a=b;
        }
        for(const p of a)next.add(p>>1)
      }
      states=next;
    }
    return states.has((1<<h)-1);
  }
  function mutate(k,w){let u=w.slice(),i=Math.floor(rnd()*k),j=Math.floor(rnd()*k),p=(i+j)%2;u[i*k+j]=active[p].find(a=>a!==u[i*k+j]);return u}
  let small=0,rows=[],negativeStagnant=0;
  for(let k of [2,3,4,8,16,36,64,128]){
    let stats={k,core:k*k,source:(k+2)**2,pairs:0,negativeLocalSurvivors:0,maxInitialPins:0,maxFinalPins:0,guarded:0};
    let reps=k<=4?24:k<=16?8:3;
    for(let t=0;t<reps;t++){
      let {w}=generate(k), a=grid(k,w),b=grid(k,mutate(k,w));
      let ia=close(a),ib=close(b),fa=close(a,[],true),fb=close(b,[],true);
      ck(ia.sat&&fa.sat&&fa.valid&&!fb.sat,"neighbor exact");
      if(ib.sat){stats.negativeLocalSurvivors++;negativeStagnant++}
      stats.maxInitialPins=Math.max(stats.maxInitialPins,ia.forced);
      stats.maxFinalPins=Math.max(stats.maxFinalPins,fa.forced);
      if(k<=4){ck(frontier(a)&&!frontier(b),"independent DP");small+=2}
      let {e}=geometry(a.h),v=a.h+1,q=e[v][0],x=+(!!(w[0]&8));
      ck(close(a,[[q,x]],true).sat&&!close(a,[[q,1-x]],true).sat,"physical guard neighbors");
      stats.guarded+=2;stats.pairs++;
    }
    rows.push(stats)
  }
  function cut(k,S){
    let r=k-2,inside=0,ec=0,faces=new Set;
    for(let i=1;i<k-1;i++)for(let j=1;j<k-1;j++){
      inside+=S[i*k+j];
      if(j<k-2&&S[i*k+j]!==S[i*k+j+1]){
        ec++;let a=(i+j)%2===0?i:i-1;faces.add(a*k+j)
      }
      if(i<k-2&&S[i*k+j]!==S[(i+1)*k+j]){
        ec++;let b=(i+j)%2===0?j:j-1;faces.add(i*k+b)
      }
    }
    ck(inside>=r*r/4&&r*r-inside>=r*r/4,"inner balanced");
    ck(ec>=r/4&&faces.size>=Math.ceil(r/16)&&ec<=4*faces.size,"cut certificate");
    for(let z of faces){let i=Math.floor(z/k),j=z%k;ck(i>=0&&i<k-1&&j>=0&&j<k-1&&(i+j)%2===0,"selected face")}
    return {ec,faces:faces.size};
  }
  let cuts=[];
  for(let k of [36,48,64,128]){
    let minFaces=Infinity,minEdges=Infinity,cases=0;
    for(let t=0;t<64;t++){
      let S=new Uint8Array(k*k),ids=Array.from({length:k*k},(_,i)=>i);
      if(t===0)for(let i=0;i<k;i++)for(let j=0;j<k;j++)S[i*k+j]=+(i<Math.floor(k/2));
      else if(t===1)for(let i=0;i<k;i++)for(let j=0;j<k;j++)S[i*k+j]=+(j<Math.floor(k/2));
      else {for(let i=ids.length-1;i>0;i--){let j=Math.floor(rnd()*(i+1));[ids[i],ids[j]]=[ids[j],ids[i]]}let size=Math.ceil(k*k/3)+Math.floor(rnd()*(Math.floor(2*k*k/3)-Math.ceil(k*k/3)+1));for(let i=0;i<size;i++)S[ids[i]]=1}
      let a=cut(k,S);minFaces=Math.min(minFaces,a.faces);minEdges=Math.min(minEdges,a.ec);cases++;
    }
    cuts.push({k,cases,minFaces,minEdges,theorem:Math.ceil((k-2)/16)})
  }
  // Check exact projection obstruction on small forced-coordinate controls.
  let certificateTrials=0;
  for(let n of [14,32,64,128])for(let t=0;t<100;t++){
    let z=new Set;while(z.size<n-1)z.add(Math.floor(rnd()*n*n));
    let usedShift=new Set,usedRow=new Set;
    for(let q of z){let i=Math.floor(q/n),j=q%n;usedShift.add((j-i+n)%n);usedRow.add(i)}
    let s=Array.from({length:n},(_,i)=>i).find(i=>!usedShift.has(i));
    let r=Array.from({length:n},(_,i)=>i).find(i=>!usedRow.has(i));
    ck(s!==undefined&&r!==undefined,"certificate extremes");
    for(let q of z){let i=Math.floor(q/n),j=q%n;ck(j!==(i+s)%n&&i!==r,"actual YES/NO completion")}
    certificateTrials++;
  }
  return {seed:26112604,assertions,smallNativeDPComparisons:small,negativeStagnant,rows,cuts,certificateTrials,dummy,active};
}
console.log(JSON.stringify(audit(),null,2));
