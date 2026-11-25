const fs=require('fs');
const cert={
  "9": {
    "root": [
      [
        "c 44 48",
        6
      ],
      [
        "11 21 30",
        6
      ],
      [
        "14 104 110",
        6
      ],
      [
        "24 84 a0",
        6
      ],
      [
        "88 108 180",
        6
      ]
    ],
    "neighbor": [
      [
        "11 14 21 24",
        6
      ],
      [
        "30 a0 110 180",
        6
      ],
      [
        "44 48 84 88",
        6
      ]
    ]
  },
  "12": {
    "root": [
      [
        "120 820 900",
        6
      ],
      [
        "44 c0 804 880",
        6
      ],
      [
        "c0 180 240 300",
        6
      ]
    ],
    "neighbor": [
      [
        "41 81 c0",
        12
      ],
      [
        "120 180 820 880",
        6
      ]
    ]
  },
  "15": {
    "root": [
      [
        "5 1001 1004",
        2
      ],
      [
        "6 1002 1004",
        4
      ],
      [
        "c 4004 4008",
        3
      ],
      [
        "22 202 220",
        4
      ],
      [
        "28 208 220",
        2
      ],
      [
        "101 4001 4100",
        2
      ],
      [
        "410 810 c00",
        6
      ],
      [
        "2004 4004 6000",
        1
      ],
      [
        "5 101 4004 4100",
        2
      ],
      [
        "6 c 202 208",
        2
      ],
      [
        "c 28 2004 2020",
        1
      ],
      [
        "12 22 2010 2020",
        2
      ],
      [
        "12 110 402 500",
        4
      ],
      [
        "28 2020 4008 6000",
        3
      ],
      [
        "110 2010 4100 6000",
        2
      ],
      [
        "1001 1040 4001 4040",
        4
      ]
    ],
    "neighbor": [
      [
        "5 1001 1004",
        6
      ],
      [
        "28 48 60",
        6
      ],
      [
        "48 4008 4040",
        6
      ],
      [
        "101 4001 4100",
        6
      ],
      [
        "410 810 c00",
        6
      ],
      [
        "2004 4004 6000",
        6
      ],
      [
        "6 c 202 208",
        6
      ],
      [
        "12 110 402 500",
        6
      ],
      [
        "22 60 1002 1040",
        6
      ]
    ]
  }
};
function run(rt,da,cert){
 let checks=0;const assert=(x,m)=>{checks++;if(!x)throw Error(m)};
 function parity(x){let v=0;while(x){v^=1;x&=x-1}return v}
 function gauss(rows){let P=new Map();function red(a,b){for(let k of [...P.keys()].sort((a,b)=>b-a)){let [v,t]=P.get(k);if(a&(1<<k)){a^=v;b^=t}}return [a,b]}
 for(let [a,b]of rows){[a,b]=red(a,b);if(!a&&b)return null;if(a)P.set(31-Math.clz32(a),[a,b])}return {P,red}}
 function closure(reg,guard){let G=guard.slice(),added=[];for(;;){let s=gauss(G);if(!s)return {bad:true,added};let ch=false;for(let r of reg){let W=[];for(let w=0;w<8;w++)if(!r.bad.includes(w)&&gauss([...G,...r.t.map((v,i)=>[1<<v,w>>i&1])]))W.push(w);if(!W.length)return {bad:true,added};for(let k=1;k<8;k++){let b=parity(k&W[0]);if(W.every(w=>parity(k&w)===b)){let a=r.t.reduce((v,t,i)=>v^((k>>i&1)?1<<t:0),0);let [m,h]=gauss(G).red(a,b);if(m){G.push([a,b]);added.push([a.toString(16),b]);ch=true}else if(h)return {bad:true,added}}}}if(!ch)return {bad:false,G,added,s:gauss(G)}}}
 function energy(reg,s){let c=reg.length,M=new Map();for(let r of reg)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let [a,b]=s.red((1<<r.t[i])^(1<<r.t[j]),((r.bad[0]>>i)^(r.bad[0]>>j))&1);if(a)M.set(a,(M.get(a)||0)+(b?-1:1));else c+=b?-1:1}let T=[...M].filter(x=>x[1]).sort((a,b)=>a[0]-b[0]).map(([a,w])=>({a,p:+(w>0),w:2*Math.abs(w)}));return {T,B:c-T.reduce((s,t)=>s+t.w/2,0)}}
 function reference(n,reg,G){let models=[],min=1e6;for(let x=0;x<1<<n;x++){if(G.some(([a,b])=>parity(a&x)!==b))continue;let e=4*reg.filter(r=>r.bad.includes(r.t.reduce((v,t,i)=>v|((x>>t&1)<<i),0))).length;min=Math.min(min,e);if(!e)models.push(x)}return {models,min}}
 function verify(n,reg,guard,pack,denom,expected){let cl=closure(reg,guard),rr=reference(n,reg,guard);assert(rr.models.length===expected,"model count");
 if(cl.bad){assert(!expected,"closure sound");return {status:"UNSAT-local",models:expected,added:cl.added}}
 let {T,B}=energy(reg,cl.s),dict=new Map(T.map(t=>[t.a,t])),load=new Map(T.map(t=>[t.a,0])),sum=0,tight=[];
 for(let [ss,k]of pack){let a=ss.split(" ").map(x=>parseInt(x,16));assert(k>=0&&new Set(a).size===a.length&&a.every(v=>dict.has(v)),"pack terms "+n+" "+ss);assert(a.reduce((x,y)=>x^y,0)===0&&a.reduce((x,y)=>x^dict.get(y).p,0)===1,"odd check");for(let v of a)load.set(v,load.get(v)+k);sum+=k;if(k)tight.push(a)}
 for(let t of T)assert(load.get(t.a)<=denom*t.w,"capacity");
 let L=denom*B+sum;assert(L<=denom*rr.min,"lower bound");
 let forced=L===0?T.filter(t=>load.get(t.a)<denom*t.w).map(t=>[t.a,t.p]):[];
 for(let x of rr.models){assert(cl.G.every(([a,b])=>parity(a&x)===b),"closure preservation");for(let [a,b]of forced)assert(parity(a&x)===b,"forced preservation");if(L===0)for(let a of tight)assert(a.reduce((s,v)=>s+(parity(v&x)^dict.get(v).p),0)===1,"saturation")}
 let mods=[];if(L===0){let eq=tight.map(a=>[...T.map(t=>+a.includes(t.a)),1]);for(let [a]of forced)eq.push([...T.map(t=>+(t.a===a)),0]);for(let q of [2,3,5,7]){let P=new Map(),bad=false;for(let row of eq){let v=row.map(x=>x%q);for(let j=0;j<T.length;j++)if(v[j]){if(P.has(j)){let k=v[j];v=v.map((x,i)=>(x-k*P.get(j)[i]%q+q)%q)}else{let a=v[j],k=1;while(a*k%q!==1)k++;P.set(j,v.map(x=>x*k%q));break}}if(v.slice(0,-1).every(x=>!x)&&v.at(-1))bad=true}if(bad)mods.push(q)}}
 assert(!(L>0||mods.length)||!rr.models.length,"false rejection");
 let after=closure(reg,[...cl.G,...forced]);if(after.bad)assert(!expected,"post deduction closure");
 return {status:L>0||mods.length||after.bad?"UNSAT":"OPEN",models:expected,minimum:rr.min,B,terms:T.length,lowerNumerator:L,denom,pack,mods,forced:forced.map(([a,b])=>[a.toString(16),b]),postClosureAdded:after.added};
 }
 let out=[];
 for(let [i,r]of rt.controls.entries())for(let nb of [false,true]){let reg=r.registry.map(q=>({...q,bad:q.bad.slice()}));if(nb){let b=reg[0].bad[0]^1;reg[0].bad=[b,b^7]}let d=da.rt[i],exp=nb?d.models:0;out.push({n:r.n,neighbor:nb,mode:"raw",...verify(r.n,reg,[],cert[r.n][nb?"neighbor":"root"],3,exp)});
 let G=d[nb?"neighborAlternating":"alternating"].accepted.map(([a,b])=>[parseInt(a,16),b]);let cl=closure(reg,G),rr=reference(r.n,reg,[]);for(let x of rr.models)assert(G.every(([a,b])=>parity(a&x)===b),"peer cut source verification");if(cl.bad){assert(!exp,"peer closure");out.push({n:r.n,neighbor:nb,mode:"peer-closure",status:"UNSAT-local",models:exp,added:cl.added});continue}
 let {T,B}=energy(reg,cl.s);out.push({n:r.n,neighbor:nb,mode:"peer-closure",status:B>0?"UNSAT-offset":T.length===0&&B===0?"SAT-constant":"OPEN",models:exp,B,terms:T.length,added:cl.added});
 }
 let F=[];for(let a=1;a<8;a++)for(let b=a+1;b<8;b++)if((a^b)>b)F.push({t:[a-1,b-1,(a^b)-1],bad:[0,7]});let P=[];for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)for(let c=b+1;c<7;c++)P.push([[ (1<<a)^(1<<b),(1<<a)^(1<<c),(1<<b)^(1<<c)].map(x=>x.toString(16)).join(" "),2]);
 out.push({n:7,neighbor:false,mode:"Fano",...verify(7,F,[],P,5,0)});
 let N=F.map(r=>({...r,bad:r.bad.slice()}));N[0].bad=[1,6];out.push({n:7,neighbor:true,mode:"Fano",...verify(7,N,[],[],5,10)});
 return {checks,out};
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3])),cert),null,2));
