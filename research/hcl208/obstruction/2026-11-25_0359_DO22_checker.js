// DO22 exact finite checker. Inputs are immutable S27/RT26/DA21 data embedded verbatim.
// Run node file.js; finite reference enumeration is not a polynomial SAT solver.
const inputs={
  "dense": [
    {
      "n": 7,
      "root": [
        {
          "t": [
            0,
            1,
            2
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            0,
            3,
            4
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            0,
            5,
            6
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            1,
            3,
            5
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            1,
            4,
            6
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            2,
            3,
            6
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            2,
            4,
            5
          ],
          "bad": [
            0,
            7
          ]
        }
      ],
      "sat": [
        {
          "t": [
            0,
            1,
            2
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            0,
            3,
            4
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            0,
            5,
            6
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            1,
            3,
            5
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            1,
            4,
            6
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            2,
            3,
            6
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "t": [
            2,
            4,
            5
          ],
          "bad": [
            0,
            7
          ]
        }
      ]
    },
    {
      "n": 15,
      "root": [
        {
          "t": [
            0,
            1,
            2
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            0,
            3,
            4
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            0,
            5,
            6
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            0,
            7,
            8
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            0,
            9,
            10
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            0,
            11,
            12
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            0,
            13,
            14
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            1,
            3,
            5
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            1,
            4,
            6
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            1,
            7,
            9
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            1,
            8,
            10
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            1,
            11,
            13
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            1,
            12,
            14
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            2,
            3,
            6
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            2,
            4,
            5
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            2,
            7,
            10
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            2,
            8,
            9
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            2,
            11,
            14
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            2,
            12,
            13
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            3,
            7,
            11
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            3,
            8,
            12
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            3,
            9,
            13
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            3,
            10,
            14
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            4,
            7,
            12
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            4,
            8,
            11
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            4,
            9,
            14
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            4,
            10,
            13
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            5,
            7,
            13
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            5,
            8,
            14
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            5,
            9,
            11
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            5,
            10,
            12
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            6,
            7,
            14
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            6,
            8,
            13
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            6,
            9,
            12
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            6,
            10,
            11
          ],
          "bad": [
            0,
            7
          ]
        }
      ],
      "sat": [
        {
          "t": [
            0,
            1,
            2
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            0,
            3,
            4
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            0,
            5,
            6
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            0,
            7,
            8
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            0,
            9,
            10
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            0,
            11,
            12
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            0,
            13,
            14
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            1,
            3,
            5
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            1,
            4,
            6
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            1,
            7,
            9
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            1,
            8,
            10
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            1,
            11,
            13
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            1,
            12,
            14
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            2,
            3,
            6
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            2,
            4,
            5
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            2,
            7,
            10
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            2,
            8,
            9
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            2,
            11,
            14
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            2,
            12,
            13
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            3,
            7,
            11
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            3,
            8,
            12
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            3,
            9,
            13
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            3,
            10,
            14
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            4,
            7,
            12
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            4,
            8,
            11
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            4,
            9,
            14
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            4,
            10,
            13
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            5,
            7,
            13
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "t": [
            5,
            8,
            14
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            5,
            9,
            11
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            5,
            10,
            12
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            6,
            7,
            14
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "t": [
            6,
            8,
            13
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            6,
            9,
            12
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "t": [
            6,
            10,
            11
          ],
          "bad": [
            2,
            5
          ]
        }
      ]
    }
  ],
  "rt": [
    {
      "n": 9,
      "root": [
        {
          "p": 0,
          "t": [
            7,
            8,
            5
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "p": 0,
          "t": [
            4,
            0,
            2
          ],
          "bad": [
            7,
            0
          ]
        },
        {
          "p": 1,
          "t": [
            8,
            2,
            1
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "p": 1,
          "t": [
            3,
            6,
            7
          ],
          "bad": [
            5,
            2
          ]
        },
        {
          "p": 2,
          "t": [
            5,
            2,
            0
          ],
          "bad": [
            4,
            3
          ]
        },
        {
          "p": 2,
          "t": [
            1,
            8,
            3
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "p": 3,
          "t": [
            6,
            2,
            7
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "p": 4,
          "t": [
            5,
            4,
            8
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "p": 4,
          "t": [
            3,
            2,
            1
          ],
          "bad": [
            5,
            2
          ]
        }
      ],
      "rootCuts": [
        [
          "c",
          0
        ],
        [
          "108",
          0
        ]
      ],
      "satCuts": [
        [
          "c",
          0
        ],
        [
          "108",
          0
        ],
        [
          "120",
          1
        ],
        [
          "180",
          1
        ]
      ]
    },
    {
      "n": 12,
      "root": [
        {
          "p": 1,
          "t": [
            0,
            7,
            6
          ],
          "bad": [
            7,
            0
          ]
        },
        {
          "p": 1,
          "t": [
            8,
            9,
            11
          ],
          "bad": [
            5,
            2
          ]
        },
        {
          "p": 2,
          "t": [
            7,
            5,
            8
          ],
          "bad": [
            5,
            2
          ]
        },
        {
          "p": 3,
          "t": [
            11,
            4,
            9
          ],
          "bad": [
            5,
            2
          ]
        },
        {
          "p": 4,
          "t": [
            5,
            7,
            11
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "p": 4,
          "t": [
            2,
            9,
            6
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "p": 5,
          "t": [
            6,
            7,
            0
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "p": 5,
          "t": [
            2,
            11,
            4
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "p": 6,
          "t": [
            2,
            4,
            9
          ],
          "bad": [
            0,
            7
          ]
        }
      ],
      "rootCuts": [
        [
          "44",
          0
        ],
        [
          "c0",
          1
        ],
        [
          "180",
          0
        ],
        [
          "300",
          0
        ],
        [
          "a00",
          1
        ]
      ],
      "satCuts": [
        [
          "44",
          0
        ],
        [
          "140",
          1
        ],
        [
          "300",
          0
        ],
        [
          "a00",
          1
        ],
        [
          "801",
          0
        ],
        [
          "880",
          0
        ]
      ]
    },
    {
      "n": 15,
      "root": [
        {
          "p": 0,
          "t": [
            6,
            5,
            3
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "p": 0,
          "t": [
            11,
            4,
            1
          ],
          "bad": [
            4,
            3
          ]
        },
        {
          "p": 0,
          "t": [
            14,
            2,
            13
          ],
          "bad": [
            5,
            2
          ]
        },
        {
          "p": 1,
          "t": [
            9,
            5,
            13
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "p": 1,
          "t": [
            1,
            10,
            11
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "p": 1,
          "t": [
            0,
            12,
            2
          ],
          "bad": [
            1,
            6
          ]
        },
        {
          "p": 1,
          "t": [
            6,
            14,
            3
          ],
          "bad": [
            4,
            3
          ]
        },
        {
          "p": 2,
          "t": [
            9,
            13,
            4
          ],
          "bad": [
            4,
            3
          ]
        },
        {
          "p": 2,
          "t": [
            1,
            5,
            6
          ],
          "bad": [
            7,
            0
          ]
        },
        {
          "p": 3,
          "t": [
            8,
            0,
            14
          ],
          "bad": [
            3,
            4
          ]
        },
        {
          "p": 3,
          "t": [
            9,
            13,
            5
          ],
          "bad": [
            4,
            3
          ]
        },
        {
          "p": 3,
          "t": [
            2,
            3,
            1
          ],
          "bad": [
            0,
            7
          ]
        },
        {
          "p": 4,
          "t": [
            8,
            4,
            10
          ],
          "bad": [
            6,
            1
          ]
        },
        {
          "p": 4,
          "t": [
            1,
            6,
            12
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "p": 4,
          "t": [
            5,
            9,
            13
          ],
          "bad": [
            2,
            5
          ]
        },
        {
          "p": 6,
          "t": [
            3,
            9,
            1
          ],
          "bad": [
            3,
            4
          ]
        }
      ],
      "rootCuts": [
        [
          "6",
          1
        ],
        [
          "c",
          1
        ],
        [
          "30",
          0
        ],
        [
          "48",
          1
        ],
        [
          "220",
          0
        ],
        [
          "2200",
          0
        ],
        [
          "41",
          0
        ],
        [
          "2040",
          0
        ],
        [
          "2800",
          1
        ],
        [
          "3000",
          0
        ],
        [
          "6000",
          1
        ]
      ],
      "satCuts": [
        [
          "30",
          0
        ],
        [
          "60",
          1
        ],
        [
          "240",
          1
        ],
        [
          "2200",
          0
        ],
        [
          "2008",
          1
        ]
      ]
    }
  ]
};
function run(inputs){
let checks=0,scans=0,sourceVisits=0,fwhtOps=0;
function ck(b,msg){checks++;if(!b)throw Error(msg)}
function parity(x){x^=x>>>16;x^=x>>>8;x^=x>>>4;return (0x6996>>>(x&15))&1}
function insert(B,m,b){while(m){let p=31-Math.clz32(m);if(!B[p]){B[p]=[m,b];return 1}m^=B[p][0];b^=B[p][1]}return b?-1:0}
function close(reg,initial){let B=[];for(let [m,b] of initial)if(insert(B,m,b)<0)return null;outer:while(true){for(let {t,bad} of reg){scans++;let good=[];for(let w=0;w<8;w++)if(!bad.includes(w)){let C=B.slice(),ok=true;for(let i=0;i<3;i++)if(insert(C,1<<t[i],(w>>i)&1)<0){ok=false;break}if(ok)good.push(w)}if(!good.length)return null;for(let a=1;a<8;a++){let v=parity(good[0]&a);if(good.every(w=>parity(w&a)===v)){let m=t.reduce((z,i,j)=>z^(((a>>j)&1)<<i),0),d=insert(B,m,v);ck(d>=0,"owner consequence");if(d>0)continue outer}}}return B.filter(Boolean)}}
function energy(reg,x){let e=0;for(let {t,bad} of reg){let w=t.reduce((z,i,j)=>z+(((x>>i)&1)<<j),0);if(bad.includes(w))e+=4}return e}
function support(a){let f=a.slice();for(let h=1;h<f.length;h*=2)for(let i=0;i<f.length;i+=2*h)for(let j=i;j<i+h;j++){let x=f[j],y=f[j+h];f[j]=x+y;f[j+h]=x-y;fwhtOps+=2}return f.reduce((s,x)=>s+(x!==0),0)}
function chart(n,reg,rows,E){
if(rows===null)return {status:"UNSAT-closure"};
// Reference affine parameterization; fix actual x0 only if global complement preserves every row.
let gauge=rows.every(([m])=>parity(m)===0),W=[];for(let x=0;x<2**n;x++)if((!gauge||!(x&1))&&rows.every(([m,b])=>parity(m&x)===b))W.push(x);
if(!W.length)return {status:"UNSAT-guard"};
let a=W[0],B=[],basis=[];for(let x of W)if(insert(B,x^a,0)>0)basis.push(x^a);
let d=basis.length,words=[a];for(let b of basis)words=words.concat(words.map(x=>x^b));ck(words.length===W.length&&new Set(words).size===W.length,"chart");ck(words.every(x=>rows.every(([m,b])=>parity(m&x)===b)),"guard chart");
let e=words.map(x=>E[x]),min=Math.min(...e),out={status:min===0?"SAT":"UNSAT",rank:rows.length,d,gauge,min,witness:words[e.indexOf(min)],directions:0,minAbsSupport:null,minQuotientSupport:null,maxQuotientSupport:0};
let dirs=new Set();if(d<=7){for(let q=1;q<2**d;q++)dirs.add(q)}else{for(let i=0;i<d;i++)dirs.add(1<<i);let s=20261125;for(let i=0;i<24;i++){s=(Math.imul(s,1664525)+1013904223)>>>0;dirs.add(1+s%(2**d-1))}}
for(let q of dirs){let A=[],B=[],M=[],lift=[];let bit=q&-q;for(let x=0;x<e.length;x++)if(!(x&bit)){let u=e[x],v=e[x^q];ck((u+v)%2===0&&(u-v)%2===0,"integer half");A.push((u+v)/2);B.push(Math.abs((u-v)/2));M.push(Math.min(u,v));lift.push(u<=v?words[x]:words[x^q]);}
let sa=support(B),sm=support(M),sA=support(A);ck(sm>=sa-sA,"support cancellation");let mm=Math.min(...M),i=M.indexOf(mm);ck(mm===min&&energy(reg,lift[i])===min&&rows.every(([m,b])=>parity(m&lift[i])===b),"exact lift");
out.directions++;out.minAbsSupport=out.minAbsSupport===null?sa:Math.min(sa,out.minAbsSupport);out.minQuotientSupport=out.minQuotientSupport===null?sm:Math.min(sm,out.minQuotientSupport);out.maxQuotientSupport=Math.max(sm,out.maxQuotientSupport);}
return out}
function one(n,reg,cuts=[]){let E=[];for(let x=0;x<2**n;x++){sourceVisits++;E.push(energy(reg,x))}let models=E.filter(x=>x===0).length,rows=close(reg,[]),raw=chart(n,reg,rows,E);ck((raw.status==="SAT")===(models>0),"raw label");
let used=0;for(let [m,b] of cuts){if(rows===null)break;let p=parseInt(m,16);ck(E.every((v,x)=>v!==0||parity(p&x)===b),"finite reference validity of imported cut");rows=close(reg,[...rows,[p,b]]);used++}
let combined=cuts.length?chart(n,reg,rows,E):null;if(combined){ck((combined.status==="SAT")===(models>0),"combined label");if(rows)ck(E.every((v,x)=>v!==0||rows.every(([m,b])=>parity(m&x)===b)),"no source model lost");}return{n,models,raw,combined,used}}
let dense=[],rt=[];for(let c of inputs.dense){for(let label of ["root","sat"])dense.push({label,...one(c.n,c[label])})}
for(let c of inputs.rt){for(let label of ["root","sat"]){let reg=JSON.parse(JSON.stringify(c.root));if(label==="sat")reg[0].bad=reg[0].bad.map(x=>x^1);rt.push({label,...one(c.n,reg,label==="sat"?c.satCuts:c.rootCuts)})}}
let symmetric=[];for(let l of [3,5,7,9,11,13,15])for(let shift of [-1,0,1]){let a=Array.from({length:2**l},(_,x)=>Math.abs(l-2*x.toString(2).replace(/0/g,"").length+shift));let b=a.map((v,x)=>(v+a[(2**l-1)^x])/2);let z=support(b);ck(z===2**(l-1),"odd absolute symmetric full even support");symmetric.push({l,shift,support:z})}
return {checks,scans,sourceVisits,fwhtOps,dense,rt,symmetric};
}
console.log(JSON.stringify(run(inputs),null,2));
