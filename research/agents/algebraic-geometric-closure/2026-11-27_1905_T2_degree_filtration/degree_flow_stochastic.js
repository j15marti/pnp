/* Supplemental scoped filtration/flow/probe experiment. Requires pinned checker.js, corpus/compiler/registry. */
function filtration(F){let vs=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),idx=new Map(vs.map((v,i)=>[v,i])),masks=vs.map((_,i)=>1n<<BigInt(i));const deg=x=>{let d=0;for(;x;x&=x-1n)d++;return d};const xor=(set,k)=>set.has(k)?set.delete(k):set.add(k);let rows=F.map(c=>{let p=new Set([0n]);for(let l of c){let m=masks[idx.get(Math.abs(l))],q=new Set;for(let t of p){if(l>0)xor(q,t);xor(q,t|m)}p=q}return {p:[...p],scope:c.map(Math.abs).sort((a,b)=>a-b).join(","),v:c.map(l=>idx.get(Math.abs(l)))}});let same=[],cross=[],neighbors=vs.map(()=>new Set);for(let q of rows)for(let i of q.v)for(let j of q.v)if(i!==j)neighbors[i].add(j);for(let q of rows)if(q.v.length<=2){const inside=[...new Set(q.v)];for(let i of inside){let p=new Set;for(let m of q.p)xor(p,m|masks[i]);same.push({p:[...p],scope:q.scope})}const outs=[...new Set(inside.flatMap(i=>[...neighbors[i]]))].filter(i=>!inside.includes(i)).sort((a,b)=>a-b).slice(0,2);for(let i of outs){let p=new Set;for(let m of q.p)xor(p,m|masks[i]);cross.push({p:[...p],scope:q.scope+"+"+vs[i]})}}
let mons=[...new Set([...rows,...same,...cross].flatMap(q=>q.p.map(String)))].map(BigInt).sort((a,b)=>deg(a)-deg(b)||(a<b?-1:1));let mi=new Map(mons.map((m,i)=>[m,i]));const enc=q=>q.p.reduce((x,m)=>x^(1n<<BigInt(mi.get(m))),0n);let ops=0;function basis(xs){let B=new Map;for(let x of xs)while(x){let j=x.toString(2).length-1;if(B.has(j)){x^=B.get(j);ops++}else{B.set(j,x);break}}return B}const low=B=>[...B].filter(([j])=>deg(mons[j])<=2).map(x=>x[1]);const summary=B=>({rank:B.size,low:low(B).length,constant:B.has(mi.get(0n))});let groups=new Map;for(let q of rows){if(!groups.has(q.scope))groups.set(q.scope,[]);groups.get(q.scope).push(enc(q))}let blocks=[...groups.values()].map(basis);let local=basis(blocks.flatMap(low));let levels=[blocks.length];while(blocks.length>1){let next=[];for(let i=0;i<blocks.length;i+=2)next.push(i+1===blocks.length?blocks[i]:basis([...blocks[i].values(),...blocks[i+1].values()]));blocks=next;levels.push(blocks.length)}let flat=basis(rows.map(enc)),hier=blocks[0];if(flat.size!==hier.size||low(flat).length!==low(hier).length||basis([...flat.values(),...hier.values()]).size!==flat.size)throw Error("hierarchy");let S=basis([...rows,...same].map(enc)),X=basis([...rows,...same,...cross].map(enc));return {vars:vs.length,features:mons.length,raw:rows.length,rawLow:rows.filter(q=>q.p.every(m=>deg(m)<=2)).length,localLow:local.size,flat:summary(flat),hierarchy:summary(hier),levels,insideMultiples:same.length,adjacentMultiples:cross.length,same:summary(S),cross:summary(X),xorOps:ops}}
function affineFlow(G,z){let bs=[],ids=[...new Set(z.map.map(t=>t[0]))].filter(x=>x!==z.anchor),idx=new Map(ids.map((x,i)=>[x,i])),P=ids.map(()=>[0,0]),B=new Map,ops=0,visits=0;G.types.forEach((t,v)=>{if(t!=="B")return;let row=z.map.slice(4*v,4*v+4);bs.push(row);let p=0n;for(const [x,s] of row){if(s)p^=1n;if(x!==z.anchor){p^=1n<<BigInt(idx.get(x)+1);P[idx.get(x)][s]++}}while(p){let j=p.toString(2).length-1;if(B.has(j)){p^=B.get(j);ops++}else{B.set(j,p);break}}});let A=B.size,contradiction=B.has(0);let keys=[...B.keys()].sort((a,b)=>a-b);for(let j of keys)for(let k of keys)if(k>j&&(B.get(k)&(1n<<BigInt(j)))){B.set(k,B.get(k)^B.get(j));ops++}let pins=[...B].filter(([j,p])=>j>0&&(p>>1n)===(1n<<BigInt(j-1))).length;
let n=bs.length+ids.length+3,src=n-2,sink=n-1,adj=Array.from({length:n},()=>[]),anchor=bs.length+ids.length;function edge(u,v,c){let a={v,c,rev:adj[v].length},b={v:u,c:0,rev:adj[u].length};adj[u].push(a);adj[v].push(b)}let ac=0;bs.forEach((row,i)=>{edge(src,i,2);for(let [x,s] of row){if(x===z.anchor){if(s){edge(i,anchor,1);ac++}}else edge(i,bs.length+idx.get(x),1)}});P.forEach((p,i)=>edge(bs.length+i,sink,Math.max(...p)));edge(anchor,sink,ac);let flow=0,rounds=0;while(true){let L=new Int32Array(n).fill(-1),Q=[src];L[src]=0;for(let i=0;i<Q.length;i++)for(let e of adj[Q[i]]){visits++;if(e.c>0&&L[e.v]<0){L[e.v]=L[Q[i]]+1;Q.push(e.v)}}if(L[sink]<0)break;rounds++;let it=new Int32Array(n);function dfs(u,f){if(u===sink)return f;for(;it[u]<adj[u].length;it[u]++){let e=adj[u][it[u]];visits++;if(e.c>0&&L[e.v]===L[u]+1){let a=dfs(e.v,Math.min(f,e.c));if(a){e.c-=a;adj[e.v][e.rev].c+=a;return a}}}return 0}let a;while(a=dfs(src,1e9))flow+=a}return {affineRank:A,affineContradiction:contradiction,affineUnary:pins,affineXors:ops,relaxedFlow:flow,demand:2*bs.length,flowRounds:rounds,flowArcVisits:visits}}
function randomProbe(F,seed=20261127,adaptive=false){let vs=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),counts=new Map,st={scans:0},hits=0,guards=[];let rng=seed>>>0;const next=()=>{rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return rng>>>0};for(let i=0;i<16;i++){let pick=()=>vs[next()%vs.length],x=pick(),y=pick();if(adaptive&&i>0){let q=[...counts].sort((a,b)=>b[1]-a[1]||a[0]-b[0]);if(q.length)x=q[0][0]}if(y===x)y=vs[(vs.indexOf(x)+1)%vs.length];let a=[[x,next()%2],[y,next()%2]],b=propagate(F,new Map(a),st);if(!b){hits++;guards.push(a);counts.set(x,(counts.get(x)||0)+1);counts.set(y,(counts.get(y)||0)+1)}}return {seed,adaptive,hits,guards,scans:st.scans,distribution:"xorshift32 modulo dictionary (modulo bias); adaptive prefers past successful x"}}
// Recorded outputs below (no unrestricted conclusion).
const recorded=[
  {
    "name": "JOINT-24",
    "algebraNative": {
      "vars": 642,
      "features": 4241,
      "raw": 2364,
      "rawLow": 591,
      "localLow": 1379,
      "flat": {
        "rank": 2364,
        "low": 1379,
        "constant": false
      },
      "hierarchy": {
        "rank": 2364,
        "low": 1379,
        "constant": false
      },
      "levels": [
        1576,
        788,
        394,
        197,
        99,
        50,
        25,
        13,
        7,
        4,
        2,
        1
      ],
      "insideMultiples": 1182,
      "adjacentMultiples": 1182,
      "same": {
        "rank": 2364,
        "low": 1379,
        "constant": false
      },
      "cross": {
        "rank": 3538,
        "low": 1613,
        "constant": false
      },
      "xorOps": 12239
    },
    "algebraCNF": {
      "vars": 24,
      "features": 884,
      "raw": 170,
      "rawLow": 155,
      "localLow": 129,
      "flat": {
        "rank": 144,
        "low": 129,
        "constant": false
      },
      "hierarchy": {
        "rank": 144,
        "low": 129,
        "constant": false
      },
      "levels": [
        144,
        72,
        36,
        18,
        9,
        5,
        3,
        2,
        1
      ],
      "insideMultiples": 310,
      "adjacentMultiples": 310,
      "same": {
        "rank": 144,
        "low": 129,
        "constant": false
      },
      "cross": {
        "rank": 386,
        "low": 131,
        "constant": false
      },
      "xorOps": 944
    },
    "flow": {
      "affineRank": 394,
      "affineContradiction": false,
      "affineUnary": 0,
      "affineXors": 394,
      "relaxedFlow": 1576,
      "demand": 1576,
      "flowRounds": 2,
      "flowArcVisits": 29471
    },
    "random": [
      {
        "seed": 20261127,
        "adaptive": false,
        "hits": 2,
        "guards": [
          [
            [
              1724,
              0
            ],
            [
              594,
              1
            ]
          ],
          [
            [
              620,
              0
            ],
            [
              627,
              1
            ]
          ]
        ],
        "scans": 107102,
        "distribution": "xorshift32 modulo dictionary (modulo bias); adaptive prefers past successful x"
      },
      {
        "seed": 20261127,
        "adaptive": true,
        "hits": 6,
        "guards": [
          [
            [
              1724,
              0
            ],
            [
              594,
              1
            ]
          ],
          [
            [
              594,
              1
            ],
            [
              2868,
              1
            ]
          ],
          [
            [
              594,
              1
            ],
            [
              2483,
              1
            ]
          ],
          [
            [
              594,
              1
            ],
            [
              2956,
              1
            ]
          ],
          [
            [
              594,
              1
            ],
            [
              1108,
              1
            ]
          ],
          [
            [
              594,
              1
            ],
            [
              2547,
              0
            ]
          ]
        ],
        "scans": 223859,
        "distribution": "xorshift32 modulo dictionary (modulo bias); adaptive prefers past successful x"
      },
      {
        "seed": 20261127,
        "adaptive": false,
        "hits": 8,
        "guards": [
          [
            [
              1,
              1
            ],
            [
              8,
              1
            ]
          ],
          [
            [
              16,
              1
            ],
            [
              7,
              1
            ]
          ],
          [
            [
              6,
              0
            ],
            [
              14,
              1
            ]
          ],
          [
            [
              1,
              0
            ],
            [
              18,
              1
            ]
          ],
          [
            [
              6,
              1
            ],
            [
              24,
              1
            ]
          ],
          [
            [
              21,
              0
            ],
            [
              15,
              1
            ]
          ],
          [
            [
              7,
              1
            ],
            [
              15,
              1
            ]
          ],
          [
            [
              17,
              1
            ],
            [
              20,
              0
            ]
          ]
        ],
        "scans": 4680,
        "distribution": "xorshift32 modulo dictionary (modulo bias); adaptive prefers past successful x"
      },
      {
        "seed": 20261127,
        "adaptive": true,
        "hits": 8,
        "guards": [
          [
            [
              1,
              1
            ],
            [
              8,
              1
            ]
          ],
          [
            [
              1,
              1
            ],
            [
              7,
              1
            ]
          ],
          [
            [
              1,
              0
            ],
            [
              24,
              1
            ]
          ],
          [
            [
              1,
              0
            ],
            [
              14,
              1
            ]
          ],
          [
            [
              1,
              0
            ],
            [
              21,
              1
            ]
          ],
          [
            [
              1,
              0
            ],
            [
              18,
              1
            ]
          ],
          [
            [
              1,
              0
            ],
            [
              15,
              1
            ]
          ],
          [
            [
              1,
              1
            ],
            [
              15,
              1
            ]
          ]
        ],
        "scans": 4202,
        "distribution": "xorshift32 modulo dictionary (modulo bias); adaptive prefers past successful x"
      }
    ],
    "elapsedMs": 407
  },
  {
    "name": "RANDOM-3CNF-40",
    "algebraNative": {
      "vars": 592,
      "features": 4405,
      "raw": 2208,
      "rawLow": 552,
      "localLow": 1288,
      "flat": {
        "rank": 2208,
        "low": 1288,
        "constant": false
      },
      "hierarchy": {
        "rank": 2208,
        "low": 1288,
        "constant": false
      },
      "levels": [
        1472,
        736,
        368,
        184,
        92,
        46,
        23,
        12,
        6,
        3,
        2,
        1
      ],
      "insideMultiples": 1104,
      "adjacentMultiples": 1104,
      "same": {
        "rank": 2208,
        "low": 1288,
        "constant": false
      },
      "cross": {
        "rank": 3310,
        "low": 1419,
        "constant": false
      },
      "xorOps": 9503
    },
    "algebraCNF": {
      "vars": 40,
      "features": 451,
      "raw": 184,
      "rawLow": 0,
      "localLow": 1,
      "flat": {
        "rank": 184,
        "low": 1,
        "constant": false
      },
      "hierarchy": {
        "rank": 184,
        "low": 1,
        "constant": false
      },
      "levels": [
        183,
        92,
        46,
        23,
        12,
        6,
        3,
        2,
        1
      ],
      "insideMultiples": 0,
      "adjacentMultiples": 0,
      "same": {
        "rank": 184,
        "low": 1,
        "constant": false
      },
      "cross": {
        "rank": 184,
        "low": 1,
        "constant": false
      },
      "xorOps": 188
    },
    "flow": {
      "affineRank": 368,
      "affineContradiction": false,
      "affineUnary": 0,
      "affineXors": 368,
      "relaxedFlow": 1472,
      "demand": 1472,
      "flowRounds": 3,
      "flowArcVisits": 39313
    },
    "random": [
      {
        "seed": 20261127,
        "adaptive": false,
        "hits": 0,
        "guards": [],
        "scans": 72864,
        "distribution": "xorshift32 modulo dictionary (modulo bias); adaptive prefers past successful x"
      },
      {
        "seed": 20261127,
        "adaptive": true,
        "hits": 0,
        "guards": [],
        "scans": 72864,
        "distribution": "xorshift32 modulo dictionary (modulo bias); adaptive prefers past successful x"
      },
      {
        "seed": 20261127,
        "adaptive": false,
        "hits": 0,
        "guards": [],
        "scans": 3496,
        "distribution": "xorshift32 modulo dictionary (modulo bias); adaptive prefers past successful x"
      },
      {
        "seed": 20261127,
        "adaptive": true,
        "hits": 0,
        "guards": [],
        "scans": 3496,
        "distribution": "xorshift32 modulo dictionary (modulo bias); adaptive prefers past successful x"
      }
    ],
    "elapsedMs": 307
  }
];
module.exports={filtration,affineFlow,randomProbe,recorded};
