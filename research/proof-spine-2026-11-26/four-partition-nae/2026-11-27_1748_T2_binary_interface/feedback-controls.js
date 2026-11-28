// Node 22; export feedbackStudy or run node feedback-controls.js clauses.json
function feedbackStudy(C,cap=10000000){
const unique=x=>[...new Set(x)].sort((a,b)=>a-b),key=x=>unique(x).join(","),vars=unique(C.flat().map(Math.abs));
function run(width,arm){
 let start=Date.now(),work=0,peakBytes=0,counts={pair:0,pivot:0,truth:0,lit:0,search:0,check:0,residue:0,serialize:0};
 const charge=(k,n=1)=>{counts[k]+=n;work+=n;if(work>cap)throw Error("CAP")};
 let F=C.map(c=>c.slice()),proof=[],flips=[],changed=0,tree=null,verified=false,scoreInitial=null,scoreEnd=null,verdict="UNKNOWN",peakLogical=0;
 const sample=()=>{let n=JSON.stringify([F,proof,flips,tree]).length;peakLogical=Math.max(peakLogical,n);charge("serialize",n)};
 function propagate(F,pins,reverse=false,kind="search"){let a=new Map(pins);while(true){let change=false;for(let t=0;t<F.length;t++){let i=reverse?F.length-1-t:t,c=F[i],missing=[],sat=false;for(let l of c){charge(kind);if(a.get(Math.abs(l))===+(l>0)){sat=true;break}if(!a.has(Math.abs(l)))missing.push(l)}if(sat)continue;if(!missing.length)return {bad:true,a};if(missing.length===1){a.set(Math.abs(missing[0]),+(missing[0]>0));change=true}}if(!change)return {bad:false,a}}}
 const table=(F,a,extra,kind="lit")=>{let bad=0,zero=0;const rows=[];for(let c of F){let k=0,s=0;for(let l of c){charge(kind);if(a.get(Math.abs(l))===+(l>0)){k++;s+=Math.sign(l)}}if(!k)bad++;if(extra){charge("residue",2);let kr=k%3,sr=(s%3+3)%3;if(k>0&&!sr)zero++;rows.push([k,kr,sr])}else rows.push([k])}return {bad,zero,rows}};
 function search(pins){let nodes=0;function walk(p){nodes++;let a=propagate(F,p);if(a.bad)return ["X"];let w=new Map();for(let c of F){let sat=false;for(let l of c){charge("search");if(a.a.get(Math.abs(l))===+(l>0)){sat=true;break}}if(sat)continue;for(let l of c){charge("search");if(!a.a.has(Math.abs(l)))w.set(Math.abs(l),(w.get(Math.abs(l))||0)+1)}}if(!w.size)return ["S",[...a.a]];let x=[...w].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let l=walk(new Map([...a.a,[x,0]]));if(l[0]==="S")return l;let r=walk(new Map([...a.a,[x,1]]));if(r[0]==="S")return r;return ["B",x,l,r]}let tree=walk(pins);return {tree,nodes}}
 function check(t,p){let a=propagate(F,p,true,"check");if(a.bad)return true;if(t[0]!=="B")return false;let x=t[1];if(a.a.has(x))return check(t[2+a.a.get(x)],a.a);return check(t[2],new Map([...a.a,[x,0]]))&&check(t[3],new Map([...a.a,[x,1]]))}
 let resultNodes=null,early=null,initialFields=null,learnedFields=null,stage="first root UP stall";
 try{
 early=propagate(C,[]);if(early.bad){verdict="UNSAT";verified=propagate(C,[],true,"check").bad;stage="stage unreachable: early closure";return {width,arm,verdict,verified,work,counts,stage}}
 // Source all-false/all-true scoring fields. Same charge in all paired arms.
 const all0=new Map(vars.map(x=>[x,0])),all1=new Map(vars.map(x=>[x,1]));
 initialFields={allFalse:table(C,all0,true).rows,allTrue:table(C,all1,true).rows};
 if(["deductions","table","residue"].includes(arm)){
 let seen=new Set(F.map(key));for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){charge("pair");let a=C[i],b=C[j];for(let l of a){charge("pivot");if(!b.includes(-l))continue;let c=unique([...a.filter(x=>x!==l),...b.filter(x=>x!==-l)]);if(c.length>width||c.some(x=>c.includes(-x))||seen.has(key(c)))continue;let u=unique([...a,...b].map(Math.abs));for(let m=0;m<2**u.length;m++){charge("truth");let as=new Map(u.map((x,h)=>[x,m>>h&1]));let sat=c=>c.some(l=>{charge("lit");return as.get(Math.abs(l))===+(l>0)});if(sat(a)&&sat(b)&&!sat(c))throw Error("invalid resolution")}seen.add(key(c));F.push(c);proof.push({parents:[i+1,j+1],pivot:l,c})}}
 learnedFields={allFalse:table(F,all0,true).rows,allTrue:table(F,all1,true).rows};
 }
 if(["flips","table","residue"].includes(arm)){
 let a=new Map(all1),extra=arm==="residue",s=table(F,a,extra);scoreInitial=[s.bad,s.zero];while(s.bad){let candidates=[];for(let x of vars){a.set(x,1-a.get(x));let t=table(F,a,extra);a.set(x,1-a.get(x));if(t.bad<s.bad)candidates.push([x,t.bad,t.zero])}if(!candidates.length)break;candidates.sort((a,b)=>a[1]-b[1]||a[0]-b[0]);let base=candidates[0][0];if(extra)candidates.sort((a,b)=>a[1]-b[1]||a[2]-b[2]||a[0]-b[0]);let [x,b,z]=candidates[0];if(x!==base)changed++;a.set(x,1-a.get(x));s=table(F,a,extra);if(s.bad!==b)throw Error("score");flips.push({variable:x,bad:b,residueZero:z,plainChoice:base})}scoreEnd=[s.bad,s.zero];if(!s.bad){let exact=table(C,a,true,"check");if(exact.bad)throw Error("false SAT");verdict="SAT";verified=true;tree=["S",[...a]];}
 }
 sample();
 if(verdict!=="SAT"){let s=search([]);tree=s.tree;resultNodes=s.nodes;if(tree[0]==="S"){let a=new Map(tree[1]);verified=table(C,a,true,"check").bad===0;verdict=verified?"SAT":"UNKNOWN"}else{verified=check(tree,[]);verdict=verified?"UNSAT":"UNKNOWN"}}
 sample();
 }catch(e){if(e.message!=="CAP")throw e;verdict="UNKNOWN";verified=false;stage="cap reached"}
 return {width,arm,stage,verdict,verified,work,counts,nodes:resultNodes,elapsed_ms:Date.now()-start,peak_serialized_sample_bytes:peakLogical,earlyForced:early?.a.size??null,learned:proof.length,proof,tree,flips,changed,scoreInitial,scoreEnd,initialFields,learnedFields};
 }
 return [2,4].flatMap(w=>["baseline","flips","deductions","table","residue"].map(a=>run(w,a)))
}
if(require.main===module)console.log(JSON.stringify(feedbackStudy(JSON.parse(require('node:fs').readFileSync(process.argv[2],'utf8')))));module.exports={feedbackStudy};
