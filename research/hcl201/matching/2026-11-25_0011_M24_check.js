// node M24_check.js GD24_deductions.json > results.json
const fs=require('fs');
function run(input){
  const controls=[];
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const plane=[]; for(let s=0;s<3;s++)for(let b=0;b<3;b++)plane.push([0,1,2].map(a=>3*a+(s*a+b)%3));for(let a=0;a<3;a++)plane.push([3*a,3*a+1,3*a+2]);
  for(const [id,clauses,flip] of [["Fano",fano,false],["Fano sign neighbor",fano,true],["Affine plane",plane,false],["Affine plane sign neighbor",plane,true]]){
    const final=clauses.map((v,i)=>({id:i,v,a:Array.from({length:8},(_,j)=>j.toString(2).padStart(3,"0")).filter(w=>{let q=w;if(flip&&i===0)q=(1-Number(w[0]))+w.slice(1);return q!=="000"&&q!=="111"})}));
    const n=1+Math.max(...clauses.flat());let count=0;for(let z=0;z<2**n;z++)if(final.every(t=>t.a.includes(t.v.map(v=>(z>>v)&1).join(""))))count++;
    controls.push({id,guard:[],final,referenceCount:count});
  }
  // Inconsistent pair cycle, all pairwise semijoins initially survive.
  const tri=[{id:0,v:[0,1],a:["00","11"]},{id:1,v:[1,2],a:["00","11"]},{id:2,v:[0,2],a:["01","10"]}];
  controls.push({id:"Parity triangle",guard:[],final:tri,referenceCount:0});
  controls.push({id:"Parity triangle SAT",guard:[],final:tri.map((t,i)=>i===2?{...t,a:["00","11"]}:t),referenceCount:2});
  function solve(job, mode){
    const T=job.final,n=T.length, masks=T.map(t=>t.a.map((_,i)=>1n<<BigInt(i)));
    const full=masks.map(a=>a.reduce((u,v)=>u|v,0n));
    const adj=Array.from({length:n},()=>[]);let groupBuildRows=0;
    const cost={probes:0,arcRevisions:0,groupTests:0,strictBatches:0,closureCalls:0,rootDeleted:0,conditionalConflicts:0,peakRetainedProbeDomains:0};
    const events=[];
    for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
      const common=T[i].v.filter(v=>T[j].v.includes(v));if(!common.length)continue;
      const groups=k=>{const ids=common.map(v=>T[k].v.indexOf(v)),g=new Map();T[k].a.forEach((w,a)=>{groupBuildRows++;const key=ids.map(b=>w[b]).join("");g.set(key,(g.get(key)||0n)|masks[k][a])});return g};
      const a=groups(i),b=groups(j),pairs=[...a].map(([k,v])=>[v,b.get(k)||0n]);adj[i].push({j,pairs});adj[j].push({j:i,pairs:pairs.map(([u,v])=>[v,u])});
    }
    function close(D){cost.closureCalls++;const q=Array.from({length:n},(_,i)=>i),inQ=Array(n).fill(true);if(D.some(a=>!a))return false;
      for(let h=0;h<q.length;h++){const i=q[h];inQ[i]=false;
        for(const {j,pairs} of adj[i]){cost.arcRevisions++;let keep=0n;
          for(const [u,v] of pairs){cost.groupTests++;if(D[i]&u)keep|=v}
          const z=D[j]&keep;if(z===D[j])continue;D[j]=z;if(!z)return false;if(!inQ[j]){q.push(j);inQ[j]=true}}
      }return true;
    }
    const count=D=>D.reduce((s,d,i)=>s+masks[i].filter(b=>d&b).length,0);
    let D=full.map((d,i)=>{for(const [v,b] of job.guard||[]){const k=T[i].v.indexOf(v);if(k>=0)T[i].a.forEach((w,a)=>{if(+w[k]!==b)d&=~masks[i][a]})}return d});
    const initial=count(D); let ok=close(D);cost.rootDeleted=initial-count(D);
    if(ok&&mode!=="AC"){
      // Every accepted global deletion batch is followed immediately by ordinary certified closure.
      let change=true;while(change&&ok){change=false;
        for(let i=0;i<n&&ok;i++){
          const prior=D.slice(), union=Array(n).fill(0n);let surviving=0n;
          for(const b of masks[i])if(prior[i]&b){cost.probes++;let d=prior.slice();d[i]=b;cost.peakRetainedProbeDomains=Math.max(cost.peakRetainedProbeDomains,3*n);
            if(close(d)){surviving|=b;for(let j=0;j<n;j++)union[j]|=d[j]}else cost.conditionalConflicts++;
          }
          const next=mode==="SAC"?prior.map((d,j)=>j===i?surviving:d):prior.map((d,j)=>d&union[j]);
          if(next.some((d,j)=>d!==prior[j])){
            const deleted=prior.map((d,j)=>({id:T[j].id,words:T[j].a.filter((_,a)=>(d&masks[j][a])&&!(next[j]&masks[j][a]))})).filter(o=>o.words.length);
            events.push({pivot:T[i].id,deleted});cost.strictBatches++;change=true;D=next;ok=close(D);
          }
        }
      }
    }
    const final=count(D), pins={};if(ok)for(let i=0;i<n;i++)for(let k=0;k<T[i].v.length;k++){const vals=new Set(T[i].a.filter((_,a)=>D[i]&masks[i][a]).map(w=>w[k]));if(vals.size===1){let v=T[i].v[k],b=+Array.from(vals)[0];if(v in pins&&pins[v]!==b)throw Error("inconsistent pin");pins[v]=b}}
    const assignment={};let compatible=ok;
    if(ok)for(let i=0;i<n;i++){let a=masks[i].findIndex(b=>D[i]&b);T[i].v.forEach((v,k)=>{let b=+T[i].a[a][k];if(v in assignment&&assignment[v]!==b)compatible=false;assignment[v]=b})}
    if(compatible&&!T.every(t=>t.a.includes(t.v.map(v=>assignment[v]).join(""))))throw Error("witness");
    return {mode,initial,final,decision:!ok?"UNSAT":compatible?"SAT":"UNKNOWN",pins,witness:compatible?assignment:null,cost,groupBuildRows,events};
  }
  return {inputRef:"a06b25dad6c0d06f689a201825e2d267269cf181",jobs:[...input.jobs,...controls].map(j=>{
    const runs=["AC","SAC","UNION"].map(m=>solve(j,m));
    if(j.referenceCount!==undefined)for(const r of runs){if(r.decision==="SAT"&&!j.referenceCount||r.decision==="UNSAT"&&j.referenceCount)throw Error("bad control");}
    return {id:j.id,guard:j.guard,referenceCount:j.referenceCount,runs};
  })};
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
