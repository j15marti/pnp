// NAE4A3 deterministic audit, Node.js. Independent exhaustive reference only on small inputs.
const sources=[
  {
    "name": "affine_plane",
    "n": 9,
    "clauses": [
      [
        [
          0,
          1,
          2
        ],
        [
          3,
          4,
          5
        ],
        [
          6,
          7,
          8
        ]
      ],
      [
        [
          0,
          3,
          6
        ],
        [
          1,
          4,
          7
        ],
        [
          2,
          5,
          8
        ]
      ],
      [
        [
          0,
          4,
          8
        ],
        [
          1,
          5,
          6
        ],
        [
          2,
          3,
          7
        ]
      ],
      [
        [
          0,
          5,
          7
        ],
        [
          1,
          3,
          8
        ],
        [
          2,
          4,
          6
        ]
      ]
    ]
  },
  {
    "name": "layered_5",
    "n": 15,
    "clauses": [
      [
        [
          0,
          5,
          10
        ],
        [
          1,
          6,
          11
        ],
        [
          2,
          7,
          12
        ],
        [
          3,
          8,
          13
        ],
        [
          4,
          9,
          14
        ]
      ],
      [
        [
          0,
          6,
          12
        ],
        [
          1,
          7,
          13
        ],
        [
          2,
          8,
          14
        ],
        [
          3,
          9,
          10
        ],
        [
          4,
          5,
          11
        ]
      ],
      [
        [
          0,
          7,
          14
        ],
        [
          1,
          8,
          10
        ],
        [
          2,
          9,
          11
        ],
        [
          3,
          5,
          12
        ],
        [
          4,
          6,
          13
        ]
      ],
      [
        [
          0,
          8,
          11
        ],
        [
          1,
          9,
          12
        ],
        [
          2,
          5,
          13
        ],
        [
          3,
          6,
          14
        ],
        [
          4,
          7,
          10
        ]
      ]
    ]
  },
  {
    "name": "random_0",
    "n": 15,
    "clauses": [
      [
        [
          12,
          6,
          4
        ],
        [
          1,
          0,
          3
        ],
        [
          13,
          10,
          8
        ],
        [
          9,
          14,
          5
        ],
        [
          2,
          7,
          11
        ]
      ],
      [
        [
          0,
          2,
          9
        ],
        [
          12,
          3,
          10
        ],
        [
          8,
          11,
          4
        ],
        [
          1,
          14,
          13
        ],
        [
          6,
          7,
          5
        ]
      ],
      [
        [
          6,
          2,
          8
        ],
        [
          4,
          10,
          1
        ],
        [
          0,
          5,
          13
        ],
        [
          3,
          7,
          9
        ],
        [
          14,
          11,
          12
        ]
      ],
      [
        [
          6,
          11,
          0
        ],
        [
          4,
          14,
          3
        ],
        [
          2,
          5,
          10
        ],
        [
          12,
          13,
          9
        ],
        [
          7,
          1,
          8
        ]
      ]
    ]
  },
  {
    "name": "random_5",
    "n": 15,
    "clauses": [
      [
        [
          12,
          14,
          13
        ],
        [
          4,
          10,
          3
        ],
        [
          0,
          8,
          11
        ],
        [
          1,
          5,
          7
        ],
        [
          6,
          9,
          2
        ]
      ],
      [
        [
          10,
          9,
          0
        ],
        [
          12,
          11,
          1
        ],
        [
          6,
          3,
          14
        ],
        [
          5,
          2,
          13
        ],
        [
          4,
          7,
          8
        ]
      ],
      [
        [
          0,
          2,
          14
        ],
        [
          6,
          4,
          12
        ],
        [
          9,
          11,
          5
        ],
        [
          10,
          7,
          13
        ],
        [
          8,
          3,
          1
        ]
      ],
      [
        [
          10,
          1,
          6
        ],
        [
          3,
          0,
          5
        ],
        [
          12,
          7,
          2
        ],
        [
          13,
          4,
          11
        ],
        [
          14,
          9,
          8
        ]
      ]
    ]
  },
  {
    "name": "random_8",
    "n": 15,
    "clauses": [
      [
        [
          0,
          2,
          4
        ],
        [
          6,
          5,
          10
        ],
        [
          9,
          3,
          8
        ],
        [
          11,
          14,
          7
        ],
        [
          1,
          13,
          12
        ]
      ],
      [
        [
          14,
          12,
          8
        ],
        [
          13,
          0,
          10
        ],
        [
          2,
          11,
          1
        ],
        [
          9,
          5,
          7
        ],
        [
          6,
          3,
          4
        ]
      ],
      [
        [
          0,
          6,
          7
        ],
        [
          14,
          2,
          10
        ],
        [
          12,
          11,
          3
        ],
        [
          1,
          8,
          5
        ],
        [
          4,
          9,
          13
        ]
      ],
      [
        [
          12,
          6,
          2
        ],
        [
          4,
          14,
          1
        ],
        [
          10,
          7,
          8
        ],
        [
          3,
          5,
          13
        ],
        [
          0,
          11,
          9
        ]
      ]
    ]
  }
];
function audit(sources) {
  let checks=0,guardJobs=0,sideCharts=0,exchangeJobs=0,exchangeInsertions=0,anchorJobs=0,targetTests=0,canonicalSuccess=0,acyclicTargetSuccess=0,forcedCycleTargetTests=0,firstAnchorFailure=null,firstForcedCounter=null;
  const A=(b,m)=>{checks++;if(!b)throw Error(m)};
  const rng=(()=>{let s=20261125;return n=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return s%n}})();
  const sat=(cs,w)=>cs.every(([a,b,c])=>((w>>a&1)!==(w>>b&1))||((w>>b&1)!==(w>>c&1)));
  const pairs=c=>{const [a,b,d]=[...c].sort((x,y)=>x-y);return [[a,b],[a,d],[b,d]]};
  const legal=(cs,...ws)=>cs.map(c=>pairs(c).filter(([a,b])=>ws.every(w=>(w>>a&1)!==(w>>b&1))));
  const path=(n,sel,a,b,skip=-1)=>{
    const adj=Array.from({length:n},()=>[]);
    sel.forEach((e,i)=>{if(e&&i!==skip){adj[e[0]].push([e[1],i]);adj[e[1]].push([e[0],i])}});
    let q=[a],prev=Array(n).fill(-1),pe=Array(n).fill(-1);prev[a]=a;
    for(let k=0;k<q.length;k++)for(const [v,i] of adj[q[k]])if(prev[v]<0){prev[v]=q[k];pe[v]=i;q.push(v)}
    if(prev[b]<0)return null;
    let out=[];for(let v=b;v!==a;v=prev[v])out.push(pe[v]);return out;
  };
  const cycles=(n,sel)=>{
    const seen=new Set(),out=[];
    for(let i=0;i<sel.length;i++)if(sel[i]&&!seen.has(i)){
      const p=path(n,sel,...sel[i],i);
      if(p!==null){let c=[i,...p];c.forEach(j=>seen.add(j));out.push(c)}
    }return out;
  };
  const chart=(n,options,random=false)=>{
    const sel=options.map(o=>o[random?rng(o.length):0]);let it=0;
    while(true){
      let cy=cycles(n,sel).find(c=>c.some(i=>options[i].length>1));
      if(!cy)break;
      let i=cy.find(i=>options[i].length>1);
      let old=sel[i],next=options[i].find(e=>String(e)!==String(old));
      sel[i]=next;A(++it<=options.length,"cycle-breaking cap");
    }
    const cc=cycles(n,sel);
    A(cc.every(c=>c.every(i=>options[i].length===1)),"nonmandatory cycle remains");
    A(cc.length===cycles(n,options.map(o=>o.length===1?o[0]:null)).length,"forced cycle count");
    sideCharts++;return sel;
  };
  const parity=(n,sel)=>{
    let adj=Array.from({length:n},()=>[]);
    for(const e of sel)if(e){adj[e[0]].push(e[1]);adj[e[1]].push(e[0])}
    let p=Array(n).fill(-1),comp=Array(n).fill(-1),k=0;
    for(let r=0;r<n;r++)if(p[r]<0){
      p[r]=0;comp[r]=k++;let q=[r];
      for(let i=0;i<q.length;i++)for(const v of adj[q[i]]){let u=q[i];if(p[v]<0){p[v]=p[u]^1;comp[v]=comp[u];q.push(v)}else if(p[v]===p[u])return null;}
    }
    let w=p.reduce((s,v,i)=>s|(v<<i),0);return {w,comp,k};
  };
  const up=(n,cs,pins)=>{
    let p=[...pins],changed=true;
    while(changed){changed=false;for(let c of cs){
      let v=c.map(i=>p[i]),z=v.filter(x=>x===0).length,o=v.filter(x=>x===1).length;
      if(z===3||o===3)return null;
      if((z===2||o===2)&&v.includes(-1)){p[c[v.indexOf(-1)]]=z===2?1:0;changed=true}
    }}return p;
  };
  const guardedChart=(n,cs,p)=>{
    let sel=[];
    for(let c of cs){let v=c.map(i=>p[i]);if(v.includes(0)&&v.includes(1))continue;
      let f=c.filter(i=>p[i]===-1);A(f.length>=2,"unclosed owner");
      sel.push([f[0],f[1]]);
    }
    let h=parity(n,sel);A(h!==null,"guarded chart bipartite");
    let w=0,w2=0;for(let i=0;i<n;i++){let b=p[i]===-1?(h.w>>i&1):p[i];w|=b<<i;w2|=(p[i]===-1?b^1:b)<<i;}
    return [w,w2];
  };
  const reconfigure=(n,start,end)=>{
    let s=start.slice(),steps=0,holes=0,m=s.length;
    while(s.some((e,i)=>String(e)!==String(end[i]))){
      let h=s.findIndex((e,i)=>String(e)!==String(end[i]));
      s[h]=null;holes++;
      while(h>=0){
        let e=end[h],p=path(n,s,...e);
        if(p===null){s[h]=e;h=-1}
        else{let j=p.find(i=>String(s[i])!==String(end[i]));A(j!==undefined,"target cycle");s[h]=e;s[j]=null;h=j;}
        A(cycles(n,s).length===0,"puncture state cycle");
        A(s.filter(e=>e===null).length<=1,"two holes");
        A(++steps<=m,"nonmonotone reconfiguration");
      }
    }exchangeJobs++;exchangeInsertions+=steps;return {steps,holes};
  };
  const validSource=({n,clauses})=>{
    let used=new Set();
    for(let part of clauses){A(part.flat().length===n&&new Set(part.flat()).size===n,"not perfect partition");for(let c of part)for(let [a,b] of pairs(c)){let k=a+","+b;A(!used.has(k),"not linear");used.add(k)}}
  };
  const bridge=(n,pa,pb,d)=>{
    let a=parity(n,pa),b=parity(n,pb);A(a&&b,"side parity");
    let es=Array.from({length:n},(_,i)=>[a.comp[i],a.k+b.comp[i]]);
    return path(a.k+b.k,es,...es[d],d)===null;
  };
  const rec=[];
  for(let src of sources){
    validSource(src);
    let {n,clauses,name}=src,all=clauses.flat(),models=[];
    for(let w=0;w<1<<n;w++)if(sat(all,w))models.push(w);
    let stats={name,n,models:models.length,guardJobs:0,anchorJobs:0,canonicalSuccess:0,acyclicTargetSuccess:0,minForcedHistogram:{},canonicalPairTrackSuccess:0};
    let sideMap=new Map();
    for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
      let cs=[...clauses[i],...clauses[j]],words=[];
      for(let w=0;w<1<<n;w++)if(sat(cs,w))words.push(w);
      sideMap.set(i+","+j,{cs,words});
      let opts=legal(cs),s=chart(n,opts),t=chart(n,opts,true),p=parity(n,s);
      A(p.k===n/3,"wrong phase dimension");A(sat(cs,p.w),"chart witness");
      reconfigure(n,s,t);
      // Exact reference for a fixed chart, not a polynomial full-source solver.
      let track=false;
      for(let b=0;b<1<<p.k;b++){let w=p.w;for(let v=0;v<n;v++)if(b>>p.comp[v]&1)w^=1<<v;if(sat(all,w))track=true}
      stats.canonicalPairTrackSuccess+=Number(track);
      for(let r=0;r<24;r++){
        let pins=Array(n).fill(-1);for(let k=0;k<r%8;k++)pins[rng(n)]=rng(2);
        let ref=words.filter(w=>pins.every((b,v)=>b<0||b===(w>>v&1))),cl=up(n,cs,pins);
        A(!!cl===(ref.length>0),"UP decision mismatch");
        if(cl){let [w,w2]=guardedChart(n,cs,cl);A(sat(cs,w)&&sat(cs,w2),"guard witness invalid");
          for(let v=0;v<n;v++){A(ref.every(a=>(a>>v&1)===(ref[0]>>v&1))===(cl[v]>=0),"missed forced coordinate");A(cl[v]<0?((w^w2)>>v&1)===1:(w>>v&1)===cl[v]&&(w2>>v&1)===cl[v],"two witness guard");}
        }guardJobs++;stats.guardJobs++;
      }
      for(let r=0;r<8;r++){
        let x=words[rng(words.length)],o=legal(cs,x),a=chart(n,o),b=chart(n,o,true);
        A(parity(n,a).k===n/3,"anchor phase count");
        reconfigure(n,a,b);
        for(let k=0;k<3;k++){let z=words[rng(words.length)],oo=legal(cs,x,z),c=chart(n,oo);A(c.every(([u,v])=>((x^x>>0)===0)&&((x>>u&1)!==(x>>v&1))&&((z>>u&1)!==(z>>v&1))),"two-word chart");}
      }
    }
    for(let [l,r] of [["0,1","2,3"],["0,2","1,3"],["0,3","1,2"]]){
      let L=sideMap.get(l),R=sideMap.get(r),right=new Set(R.words), candidates=[];
      for(let x of L.words){if(right.has(x))continue;for(let d=0;d<n;d++){let y=x^(1<<d);if(!right.has(y)||sat(L.cs,y))continue;
        const blocker=(cs,w)=>cs.filter(c=>c.includes(d)&&c.filter(v=>v!==d).every(v=>(w>>v&1)!==(w>>d&1))).length;
        if(blocker(L.cs,x)===1&&blocker(R.cs,y)===1)candidates.push([x,y,d]);
      }}
      // deterministic samples spread across candidate set
      for(let k=0;k<Math.min(16,candidates.length);k++){
        let [x,y,d]=candidates[Math.floor(k*candidates.length/Math.min(16,candidates.length))];
        let ac=chart(n,legal(L.cs,x)),bc=chart(n,legal(R.cs,y)),canon=bridge(n,ac,bc,d);
        let direct=parity(n,[...ac,...bc]);
        A(canon===!!direct,"bridge/parity mismatch");if(direct)A(sat(all,direct.w),"bridge witness invalid");
        anchorJobs++;stats.anchorJobs++;canonicalSuccess+=Number(canon);stats.canonicalSuccess+=Number(canon);
        let min=Infinity,chosen=null;
        for(let z of models){
          let ao=legal(L.cs,x,z),bo=legal(R.cs,y,z);
          let ca=cycles(n,ao.map(o=>o.length===1?o[0]:null)).length,cb=cycles(n,bo.map(o=>o.length===1?o[0]:null)).length;
          targetTests++;if(ca+cb)forcedCycleTargetTests++;
          if(ca+cb<min){min=ca+cb;chosen=z}
        }
        let good=min===0;acyclicTargetSuccess+=Number(good);stats.acyclicTargetSuccess+=Number(good);stats.minForcedHistogram[String(min)]=(stats.minForcedHistogram[String(min)]||0)+1;
        if(chosen!==null){let a=chart(n,legal(L.cs,x,chosen)),b=chart(n,legal(R.cs,y,chosen));A(bridge(n,a,b,d),"target charts not bridge");A(cycles(n,a).length+cycles(n,b).length===min,"minimum mandatory cycles");}
        if(!canon&&models.length&&!firstAnchorFailure)firstAnchorFailure={name,l,r,x,y,d,common:models[0],min};
        if(models.length&&!good&&!firstForcedCounter)firstForcedCounter={name,l,r,x,y,d,min,models};
      }
    }
    rec.push(stats);
  }
  return {seed:20261125,checks,guardJobs,sideCharts,exchangeJobs,exchangeInsertions,anchorJobs,targetTests,canonicalSuccess,acyclicTargetSuccess,forcedCycleTargetTests,firstAnchorFailure,firstForcedCounter,records:rec,sources};
}
console.log(JSON.stringify(audit(sources),null,2));
