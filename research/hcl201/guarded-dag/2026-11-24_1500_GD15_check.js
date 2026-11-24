const run = function run(){
 const stats={gauss:0,joins:0,closure:0,pins:0,assertions:0,referenceWords:0,peakStates:0};
 const chk=(v)=>{stats.assertions++;if(!v)throw Error("assertion "+stats.assertions)};
 const lead=x=>x.toString(2).length-1;
 function count(d,eq){stats.gauss++;let B=new Map;for(let [x,b] of eq){while(x){let p=lead(x),t=B.get(p);if(!t){B.set(p,[x,b]);break}x^=t[0];b^=t[1]}if(!x&&b)return 0n}return 1n<<BigInt(d-B.size)}
 function basis(rows){let B=new Map;for(let x of rows){while(x){let p=lead(x);if(!B.has(p)){B.set(p,x);break}x^=B.get(p)}}return [...B.values()]}
 function intersect(A,B){let T=new Map(basis(A).map(x=>[lead(x),[x,0n]])),out=[];for(let orig of basis(B)){let x=orig,y=orig;while(x){let p=lead(x),t=T.get(p);if(!t){T.set(p,[x,y]);break}x^=t[0];y^=t[1]}if(!x&&y)out.push(y)}return basis(out)}
 function prepare(g){let rows=g.layers.map(l=>l.flatMap(e=>e.g.map(x=>x[0]))),I=[];for(let i=0;i<=rows.length;i++)I.push(intersect(rows.slice(0,i).flat(),rows.slice(i).flat()));return {...g,I,width:Math.max(...I.map(x=>x.length))}}
 const eqs=(I,a)=>I.map((x,i)=>[x,(a>>i)&1]);
 function reachable(g,accept){let S=new Set([0]);for(let l of g.layers){let T=new Set;for(let e of l)if(S.has(e.u)&&accept(e))T.add(e.v);S=T}return S.has(0)}
 function close(g,pins){pins=pins.slice();while(true){stats.closure++;let L=count(g.d,pins);if(!L)return {pins,ans:"UNSAT"};let C=new Map;for(let l of g.layers)for(let e of l)C.set(e,count(g.d,pins.concat(e.g)));if(reachable(g,e=>C.get(e)===L))return {pins,ans:"UNSAT"};if(!reachable(g,e=>C.get(e)>0n))return {pins,ans:"SAT"};let pin=null;outer:for(let l of g.layers)for(let e of l)if(C.get(e)*2n===L&&reachable(g,f=>f===e||C.get(f)===L)){for(let [x,b] of e.g)if(count(g.d,pins.concat([[x,b]]))*2n===L){pin=[x,b^1];break outer}}if(!pin)return {pins,ans:null};pins.push(pin);stats.pins++}}
 function moments(g,pins,max){let total=count(g.d,pins),out=[total];for(let q=1;q<=max;q++){let init=Array(q).fill(0),D=new Map([[init.join(",")+"|0",{vs:init,a:0,n:total}]]);for(let i=0;i<g.layers.length;i++){let E=new Map;for(let e of g.layers[i]){if(!E.has(e.u))E.set(e.u,[]);E.get(e.u).push(e)}let T=new Map;for(let {vs,a,n} of D.values()){let p=pins.concat(eqs(g.I[i],a)),den=count(g.d,p);if(!den)continue;function extend(j,next,guard){if(j<q){for(let e of E.get(vs[j])??[])extend(j+1,next.concat(e.v),guard.concat(e.g));return}if(!count(g.d,p.concat(guard)))return;for(let b=0;b<2**g.I[i+1].length;b++){stats.joins++;let c=count(g.d,p.concat(guard,eqs(g.I[i+1],b)));if(!c)continue;let num=n*c;chk(num%den===0n);let k=next.join(",")+"|"+b,t=T.get(k);if(t)t.n+=num/den;else T.set(k,{vs:next,a:b,n:num/den})}}extend(0,[],[])}D=T;stats.peakStates=Math.max(stats.peakStates,D.size)}out.push(D.get(init.join(",")+"|0")?.n??0n)}return out}
 function binMom(M){let poly=[1n],out=[M[0]],fac=1n;for(let j=1;j<M.length;j++){let p=Array(poly.length+1).fill(0n);for(let i=0;i<poly.length;i++){p[i]-=BigInt(j-1)*poly[i];p[i+1]+=poly[i]}poly=p;fac*=BigInt(j);let v=poly.reduce((s,c,i)=>s+c*M[i],0n);chk(v%fac===0n&&v>=0n);out.push(v/fac)}return out}
 function credit(g,pins,b){let c=close(g,pins);if(c.ans==="UNSAT")return {...c,value:0n,exact:true};if(c.ans==="SAT")return {...c,value:count(g.d,c.pins),exact:true};let S=binMom(moments(g,c.pins,b+1)),exact=S[b+1]===0n;let value=S[0];for(let i=1;i<=b;i++)value+=(i%2?-1n:1n)*S[i];if(exact)return {...c,value,exact};if(b%2&&value>0n)return {...c,value,exact:false};return {...c,value:null,exact:false}}
 function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
 function lift(g,pins){let z=0n;for(let j=0;j<g.d;j++){let x=1n<<BigInt(j);if(count(g.d,pins.concat([[x,0]])))pins=pins.concat([[x,0]]);else{pins=pins.concat([[x,1]]);z|=x}}return z}
 function pathcount(g,z){let D=new Map([[0,1n]]);for(let l of g.layers){let T=new Map;for(let e of l)if(e.g.every(([x,b])=>parity(x&z)===b))T.set(e.v,(T.get(e.v)??0n)+(D.get(e.u)??0n));D=T}return D.get(0)??0n}
 function solve(g,b){let c=credit(g,[],b);if(c.value===null)return {label:"UNKNOWN"};if(c.value===0n)return {label:"UNSAT",exact:c.exact,value:"0"};let start=c.value,exact=c.exact;for(let x of basis(g.layers.flatMap(l=>l.flatMap(e=>e.g.map(a=>a[0]))))){ // use actual rows, not a Gaussian combination basis: replace below by raw rows
 }for(let x of g.layers.flatMap(l=>l.flatMap(e=>e.g.map(a=>a[0])))){if(c.ans==="SAT")break;let L=count(g.d,c.pins);if(count(g.d,c.pins.concat([[x,0]]))===0n||count(g.d,c.pins.concat([[x,1]]))===0n)continue;let a=credit(g,c.pins.concat([[x,0]]),b);if(a.value!==null&&a.value>0n)c=a;else{let a1=credit(g,c.pins.concat([[x,1]]),b);chk(a1.value!==null&&a1.value>0n);c=a1}}let z=lift(g,c.pins);chk(pathcount(g,z)===0n);return {label:"SAT",exact,value:String(start),witness:String(z)}}
 function ref(g,b){let M=Array(b+2).fill(0n),safe=0n;for(let z=0n;z<(1n<<BigInt(g.d));z++){stats.referenceWords++;let p=pathcount(g,z);if(!p)safe++;for(let i=0;i<M.length;i++)M[i]+=p**BigInt(i)}return {M,safe}}
 function clauses(d,C){let L=[[],[],[]];C.forEach((c,i)=>{for(let j=0;j<3;j++)L[j].push({u:j?i+1:0,v:j===2?0:i+1,g:[c[j]]})});return prepare({d,layers:L})}
 let rows=[],summary={SAT:0,UNSAT:0,UNKNOWN:0},seed=171913;
 function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 function test(name,g,b,reference=true,expected=null,raw=false){let R=reference?ref(g,b):null;if(R&&raw){let M=moments(g,[],b+1);chk(M.every((v,i)=>v===R.M[i]))}let s=solve(g,b);if(R&&s.label!=="UNKNOWN"){chk((s.label==="SAT")===(R.safe>0n));if(s.exact)chk(BigInt(s.value)===R.safe)}if(expected)chk(s.label===expected);summary[s.label]++;rows.push({name,width:g.width,...s,referenceSafe:R?String(R.safe):null})}
 // cube all subsets, each word enables at most one clause path
 for(let m=0;m<256;m++){let C=[];for(let a=0;a<8;a++)if((m>>a)&1)C.push([0,1,2].map(j=>[1n<<BigInt(j),(a>>j)&1]));test("cube-"+m,clauses(3,C),1,true,m===255?"UNSAT":"SAT",m%17===0)}
 // random affine layered DAGs, including non-coordinate overlapping rows
 for(let t=0;t<50;t++){let L=[];for(let i=0;i<3;i++){let E=[];for(let u=0;u<(i===0?1:2);u++)for(let v=0;v<(i===2?1:2);v++)for(let j=0;j<1+rand(2);j++){let G=[];for(let h=0;h<1+rand(2);h++)G.push([BigInt(1+rand(15)),rand(2)]);E.push({u,v,g:G})}L.push(E)}test("random-"+t,prepare({d:4,layers:L}),2,true,null,true)}
 // 2 copies of deterministic parity automaton, no shared rank across layers
 function parityGraph(d,all){let layers=[];for(let i=0;i<d;i++){let E=[];for(let c=0;c<2;c++)for(let p=0;p<2;p++){if(i===0&&p)continue;for(let x=0;x<2;x++){let np=p^x;if(i===d-1&&!all&&np===0)continue;E.push({u:i===0?0:1+2*c+p,v:i===d-1?0:1+2*c+np,g:[[1n<<BigInt(i),x]]})}}layers.push(E)}return prepare({d,layers})}
 for(let d of [4,8,16,32,64])for(let all of [false,true])test("parity-"+d+"-"+all,parityGraph(d,all),2,d===4,all?"UNSAT":"SAT");
 // unbounded multiplicity, first and third Bonferroni differ; four paths iff x=y=0
 let odd=prepare({d:2,layers:[[...Array.from({length:4},()=>({u:0,v:0,g:[[1n,0],[2n,0]]}))]]});test("odd-credit",odd,3,true,"SAT",true);
 // many paths on every word: duplicate complementary guard transitions, cap must not lie
 let high=prepare({d:8,layers:Array.from({length:8},(_,i)=>Array.from({length:4},(_,j)=>({u:0,v:0,g:[[1n<<BigInt(i),j%2]]})))});
 test("high-multiplicity",high,2,true,"UNKNOWN",true);
 // Fano reference and bounded terminal: use b=1 (can abstain); genuine monotone clauses with two orientations
 let triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],F=triples.flatMap(t=>[0,1].map(b=>t.map(i=>[1n<<BigInt(i),b])));
 for(let i=-1;i<14;i++)test("fano-"+i,clauses(7,F.filter((_,j)=>i!==j)),1,true);
 return {summary,stats,rows}
};
console.log(JSON.stringify(run(),null,2));
