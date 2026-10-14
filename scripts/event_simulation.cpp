// Complete-event replay. All ratings are frozen before the event.
// Duration-seeded ties use exchangeable random duration seeds (explicit model
// assumption). Complex >=4-way ties use a documented elimination scenario.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
using namespace std;using V=vector<int>;using VV=vector<V>;
mt19937_64 rng;int n,year,kind,region[32],exception_team=-1,exception_trigger=-1;double P[3][32][32];uint32_t met[32];
V direct,byes;VV groups,main_groups,opening,tiers;V bye_group;
long long N;long long counts[32][33][33]={};int ranklo[32],rankhi[32];
long long duration_ties=0,complex_ties=0,waivers=0;bool fair=false;
uint64_t bounded(uint64_t n){uint64_t x,t=-n%n;do{x=rng();}while(x<t);return x%n;}
double unif(){return (rng()>>11)*0x1.0p-53;}
void shuf(V&v){for(int i=int(v.size())-1;i>0;--i)swap(v[i],v[bounded(i+1)]);}
int game(int a,int b,int bo){assert(a>=0&&a<n&&b>=0&&b<n&&a!=b);return unif()<P[bo][a][b]?a:b;}
int lose(int a,int b,int win){return a==win?b:a;}
void put(int t,int lo,int hi){assert(ranklo[t]==0);assert(lo>=1&&hi<=n&&lo<=hi);ranklo[t]=lo;rankhi[t]=hi;}
void tied(V v,int lo,int hi){for(int t:v)put(t,lo,hi);}

V tie_break(V v,int h[32][32],int reps,int offset,int qualify,bool choose){
 if(v.size()<2)return v;
 if(v.size()==2){
  if(h[v[0]][v[1]]!=h[v[1]][v[0]]){if(h[v[0]][v[1]]<h[v[1]][v[0]])swap(v[0],v[1]);return v;}
  // For MSI's selectable 3rd/4th opponents, time breaks a tied seed.
  if(choose&&offset==2&&qualify==4){++duration_ties;shuf(v);return v;}
  int w=game(v[0],v[1],0);if(w==v[1])swap(v[0],v[1]);return v;
 }
 int hs[32]={};for(int a:v)for(int b:v)hs[a]+=h[a][b];
 // A team beating every tied opponent, or losing to every tied opponent,
 // is separated before the remaining tied subset is resolved.
 V top,bottom,middle;
 for(int t:v){if(hs[t]==reps*(int(v.size())-1))top.push_back(t);else if(hs[t]==0)bottom.push_back(t);else middle.push_back(t);}
 if(!top.empty()||!bottom.empty()){
  V out=top;V mid=tie_break(middle,h,reps,offset+top.size(),qualify,choose);out.insert(out.end(),mid.begin(),mid.end());out.insert(out.end(),bottom.begin(),bottom.end());return out;
 }
 ++duration_ties;shuf(v);stable_sort(v.begin(),v.end(),[&](int a,int b){return hs[a]>hs[b];});
 if(v.size()==3){int w=game(v[1],v[2],0),l=lose(v[1],v[2],w),ww=game(v[0],w,0);return {ww,lose(v[0],w,ww),l};}
 ++complex_ties;
 // Fully order >=4-way ties using seeded BO1 elimination plus classification
 // games. A sensitivity scenario, not an assertion about every vintage rule.
 V out;
 while(v.size()>1){V alive=v;while(alive.size()>1){V next;for(int i=0;i<int(alive.size());i+=2)next.push_back(i+1<int(alive.size())?game(alive[i],alive[i+1],0):alive[i]);alive=next;}int w=alive[0];out.push_back(w);v.erase(find(v.begin(),v.end(),w));}
 out.insert(out.end(),v.begin(),v.end());return out;
}
V rr(V v,int reps,int qualify,bool choose=false){
 int wins[32]={},h[32][32]={};
 for(int k=0;k<reps;++k)for(int i=0;i<int(v.size());++i)for(int j=i+1;j<int(v.size());++j){int a=v[i],b=v[j],w=game(a,b,0);++wins[w];++h[w][lose(a,b,w)];}
 stable_sort(v.begin(),v.end(),[&](int a,int b){return wins[a]>wins[b];});V out;
 for(int i=0;i<int(v.size());){int j=i+1;while(j<int(v.size())&&wins[v[i]]==wins[v[j]])++j;V sub(v.begin()+i,v.begin()+j);sub=tie_break(sub,h,reps,i,qualify,choose);out.insert(out.end(),sub.begin(),sub.end());i=j;}
 return out;
}
void single(V v,int qbo=2){int size=v.size();while(v.size()>1){V next;int bo=size==8&&v.size()==8?qbo:2;for(int i=0;i<int(v.size());i+=2){int w=game(v[i],v[i+1],bo);put(lose(v[i],v[i+1],w),v.size()/2+1,v.size());next.push_back(w);}v=next;}put(v[0],1,1);}
void msi_final(V order,bool choose){
 put(order[4],5,5);put(order[5],6,6);
 int opp=3;
 if(choose){double p3=P[2][order[0]][order[2]],p4=P[2][order[0]][order[3]];opp=p3>p4?2:3;if(p3==p4)opp=2+bounded(2);}
 single({order[0],order[opp],order[1],order[opp==2?3:2]});
}
// 4-team GSL: return upper qualifier, lower qualifier, 1-2, 0-2.
V gsl(V v,int bo,bool complete=true){assert(v.size()==4);int a=game(v[0],v[1],bo),b=game(v[2],v[3],bo),la=lose(v[0],v[1],a),lb=lose(v[2],v[3],b);int u=game(a,b,bo),lu=lose(a,b,u),l=game(la,lb,bo),ll=lose(la,lb,l);if(!complete)return {u,lu,l,ll};int q=game(lu,l,bo);return {u,q,lose(lu,l,q),ll};}
void double8(V v){
 assert(v.size()==8);V w,l;
 for(int i=0;i<8;i+=2){int x=game(v[i],v[i+1],2);w.push_back(x);l.push_back(lose(v[i],v[i+1],x));}
 int a=game(w[0],w[1],2),b=game(w[2],w[3],2),la=lose(w[0],w[1],a),lb=lose(w[2],w[3],b);
 int c=game(l[0],l[1],2),d=game(l[2],l[3],2);put(lose(l[0],l[1],c),7,8);put(lose(l[2],l[3],d),7,8);
 // Cross-drop upper-round losers into opposite lower sides.
 int e=game(c,lb,2),f=game(d,la,2);put(lose(c,lb,e),5,6);put(lose(d,la,f),5,6);
 int u=game(a,b,2),lu=lose(a,b,u),g=game(e,f,2);put(lose(e,f,g),4,4);
 int h=game(g,lu,2);put(lose(g,lu,h),3,3);int ch=game(u,h,2);put(lose(u,h,ch),2,2);put(ch,1,1);
}
bool slot_place(const V&order,V&slots,int k,int mode){
 if(k==int(order.size()))return true;int t=order[k];
 for(int s=0;s<int(slots.size());++s)if(slots[s]<0){int o=slots[s^1];if(o>=0&&(mode==1?region[t]==region[o]:(met[t]&(1u<<o))))continue;slots[s]=t;if(slot_place(order,slots,k+1,mode))return true;slots[s]=-1;}
 return false;
}
V pair_groups(V high,V low,int mode=1){assert(high.size()==low.size());shuf(high);shuf(low);V slots(2*high.size(),-1);for(int i=0;i<int(high.size());++i)slots[2*i]=high[i];bool ok=slot_place(low,slots,0,mode);if(!ok){++waivers;for(int i=0;i<int(low.size());++i)slots[2*i+1]=low[i];}return slots;}
V pair_same(V g,int mode){shuf(g);V slots(g.size(),-1);if(mode<0)return g;if(!slot_place(g,slots,0,mode)){++waivers;return g;}return slots;}
// Insert play-in qualifiers into pre-drawn main groups, respecting regions.
bool insert_group(const V&order,VV&gs,int k){if(k==int(order.size()))return true;int t=order[k];for(auto&g:gs)if(g.size()==3&&none_of(g.begin(),g.end(),[&](int x){return region[x]==region[t];})){g.push_back(t);if(insert_group(order,gs,k+1))return true;g.pop_back();}return false;}
V world_group_bracket(V first,V second){
 // Group winners are shuffled; their group's runner-up must be in the other half.
 V order={0,1,2,3};shuf(order);V runners={0,1,2,3};shuf(runners);V selected;
 // Enumerate remaining placements in draw order using first feasible assignment.
 auto dfs=[&](auto&&self,int k,V&used)->bool{if(k==4)return true;for(int idx:runners)if(find(used.begin(),used.end(),idx)==used.end()){int pos=find(order.begin(),order.end(),idx)-order.begin();if(pos/2==k/2)continue;used.push_back(idx);if(self(self,k+1,used))return true;used.pop_back();}return false;};
 bool ok=dfs(dfs,0,selected);assert(ok);V v;for(int i=0;i<4;++i){v.push_back(first[order[i]]);v.push_back(second[selected[i]]);}return v;
}

void worlds_groups(){
 VV gs=main_groups;V qual;
 if(!groups.empty()){
  VV ranks;for(auto&g:groups)ranks.push_back(rr(g,year<=2019?2:1,year<=2019?2:4));
  if(year<=2019){V first,second;for(auto&v:ranks){first.push_back(v[0]);second.push_back(v[1]);put(v[2],21,24);}V order={0,1,2,3};shuf(order);V perm=order;while(true){bool ok=true;for(int i=0;i<4;++i)if(perm[i]==i)ok=false;if(ok)break;shuf(perm);}for(int i=0;i<4;++i){int w=game(first[i],second[perm[i]],2);put(lose(first[i],second[perm[i]],w),17,20);qual.push_back(w);}}
  else{for(auto&v:ranks){qual.push_back(v[0]);for(int pos=4;pos<int(v.size());++pos)put(v[pos],21+2*(pos-4),22+2*(pos-4));}for(int i=0;i<2;++i){auto&v=ranks[i];int w=game(v[2],v[3],2);put(lose(v[2],v[3],w),19,20);int q=game(w,ranks[1-i][1],2);put(lose(w,ranks[1-i][1],q),17,18);qual.push_back(q);}}
  shuf(qual);int saved=-1;if(year==2022 && find(qual.begin(),qual.end(),exception_team)!=qual.end() && find(qual.begin(),qual.end(),exception_trigger)!=qual.end()){saved=region[exception_team];region[exception_team]=99;}bool ok=insert_group(qual,gs,0);if(saved>=0)region[exception_team]=saved;assert(ok);
 }
 V first,second;
 for(auto&g:gs){V o=rr(g,2,2);first.push_back(o[0]);second.push_back(o[1]);for(int pos=2;pos<int(g.size());++pos)put(o[pos],year==2013?9+2*(pos-2):9+4*(pos-2),year==2013?10+2*(pos-2):12+4*(pos-2));}
 if(year==2013){V bye=byes;shuf(bye);V q={first[0],first[1],second[0],second[1]};shuf(q);V v;for(int i=0;i<4;++i){v.push_back(bye[i]);v.push_back(q[i]);}single(v,1);}
 else single(world_group_bracket(first,second));
}
void swiss(V active,V qual){
 int wins[32]={},loss[32]={};fill(begin(met),end(met),0);
 auto play=[&](V v,int bo){for(int i=0;i<int(v.size());i+=2){int a=v[i],b=v[i+1];assert(wins[a]==wins[b]&&loss[a]==loss[b]);int w=game(a,b,bo),l=lose(a,b,w);++wins[w];++loss[l];met[a]|=1u<<b;met[b]|=1u<<a;}};
 if(year<2025){V low=tiers[3];low.insert(low.end(),qual.begin(),qual.end());play(pair_groups(tiers[0],low),0);play(pair_groups(tiers[1],tiers[2]),0);}
 else{V one=tiers[0],two=tiers[1],three=tiers[2];int q=qual[0];auto it=find_if(three.begin(),three.end(),[&](int t){return region[t]==region[q];});assert(it!=three.end());two.push_back(*it);three.erase(it);three.push_back(q);play(pair_groups(one,three),0);play(pair_same(two,1),0);}
 for(int round=2;round<=5;++round){VV buckets(9);for(int t:active)if(wins[t]<3&&loss[t]<3)buckets[3*wins[t]+loss[t]].push_back(t);for(auto&g:buckets)if(!g.empty()){int bo=(wins[g[0]]==2||loss[g[0]]==2)?1:0;play(pair_same(g,year==2023?-1:0),bo);}}
 V a,b,c;
 for(int t:active)if(wins[t]==3)(loss[t]==0?a:loss[t]==1?b:c).push_back(t);else{assert(loss[t]==3);if(wins[t]==0)put(t,15,16);else if(wins[t]==1)put(t,12,14);else put(t,9,11);}
 assert(a.size()==2&&b.size()==3&&c.size()==3);shuf(a);shuf(c);b.push_back(c[2]);shuf(b);single({a[0],c[0],b[0],b[1],a[1],c[1],b[2],b[3]});
}
void worlds_swiss(){V qual;
 if(year==2025){int w=game(opening[0][0],opening[0][1],2);qual={w};put(lose(opening[0][0],opening[0][1],w),17,17);}
 else if(year==2023){V a=gsl(opening[0],1),b=gsl(opening[1],1);put(a[3],21,22);put(b[3],21,22);put(a[2],19,20);put(b[2],19,20);int x=game(a[0],b[1],2),y=game(b[0],a[1],2);put(lose(a[0],b[1],x),17,18);put(lose(b[0],a[1],y),17,18);qual={x,y};}
 else{V a=gsl(opening[0],1,false),b=gsl(opening[1],1,false);put(a[3],19,20);put(b[3],19,20);int x=game(a[1],b[2],1),y=game(b[1],a[2],1);put(lose(a[1],b[2],x),17,18);put(lose(b[1],a[2],y),17,18);qual={a[0],b[0],x,y};}
 V active=direct;active.insert(active.end(),qual.begin(),qual.end());swiss(active,qual);
}
void msi_old(){V main=direct;
 if(!groups.empty()){
  V q,el;for(auto&g:groups){V o=rr(g,2,1);q.push_back(o[0]);el.insert(el.end(),o.begin()+1,o.end());}
  // Coarse stage bands: no arbitrary order among eliminated first-stage teams.
  tied(el,year==2018?9:8,n);
  V bb=byes;if(year!=2019)shuf(bb);else if(bye_group[0]==1)swap(bb[0],bb[1]);
  V losers;for(int i=0;i<2;++i){int w=game(q[i],bb[i],2);main.push_back(w);losers.push_back(lose(q[i],bb[i],w));}
  if(year==2018)tied(losers,7,8);else{int w=game(losers[0],losers[1],2);main.push_back(w);put(lose(losers[0],losers[1],w),7,7);}
 }
 assert(main.size()==6);msi_final(rr(main,year==2015?1:2,4,year>=2017),year>=2017);
}
void msi_rumble(){V rum;for(auto&g:groups){V o=rr(g,g.size()==3?4:2,2);rum.push_back(o[0]);rum.push_back(o[1]);put(o[2],7,9);if(o.size()==4)put(o[3],10,11);}msi_final(rr(rum,2,4,true),true);}
// Cached legal seeded brackets: a pure function of qualifiers, not outcomes.
struct CacheEntry{uint32_t mask;VV brackets;};vector<CacheEntry> bracket_cache;
V main_draw(V qual){
 uint32_t mask=0;for(int t:qual)mask|=1u<<t;
 for(auto&e:bracket_cache)if(e.mask==mask)return e.brackets[bounded(e.brackets.size())];
 VV legal;
 if(year==2023){V hi=tiers[0],mid=tiers[1],low=tiers[2];low.insert(low.end(),qual.begin(),qual.end());sort(low.begin(),low.end());do{V v={hi[0],low[0],mid[0],low[1],hi[1],low[2],mid[1],low[3]};for(int sw=0;sw<2;++sw){if(sw)swap(v[2],v[6]);bool ok=true;for(int i=0;i<8;i+=2)if(region[v[i]]==region[v[i+1]])ok=false;if(ok)legal.push_back(v);}}while(next_permutation(low.begin(),low.end()));}
 else if(year==2024){V hi=tiers[0],mid=tiers[1];V upper,lower; // pool 3 = 2-0 qualifiers, pool 4 = 2-1 qualifiers
  upper={qual[0],qual[2]};lower={qual[1],qual[3]};
  for(int x=0;x<2;++x)for(int y=0;y<2;++y)for(int z=0;z<2;++z){V v={hi[0],lower[x],mid[y],upper[z],hi[1],lower[1-x],mid[1-y],upper[1-z]};bool ok=true;for(int start:{0,4})for(int i=start;i<start+4;++i)for(int j=i+1;j<start+4;++j)if(region[v[i]]==region[v[j]])ok=false;if(ok)legal.push_back(v);}
 }
 else {V hi=tiers[0],mid=tiers[1],third=tiers[2];for(int x=0;x<2;++x)for(int y=0;y<2;++y){V v={hi[0],qual[x],mid[y],third[0],hi[1],qual[1-x],mid[1-y],third[1]};bool ok=true;for(int start:{0,4})for(int i=start;i<start+4;++i)for(int j=i+1;j<start+4;++j)if(region[v[i]]==region[v[j]])ok=false;if(ok)legal.push_back(v);}}
 assert(!legal.empty());
 // 2024 seeding depends on qualifier upper/lower status, not just set.
 if(year!=2024)bracket_cache.push_back({mask,legal});return legal[bounded(legal.size())];
}
void msi_double(){V qual;
 if(year==2025){V a=gsl(opening[0],2);qual={a[0],a[1]};put(a[2],9,9);put(a[3],10,10);}
 else{V a=gsl(opening[0],1),b=gsl(opening[1],1);int base=year==2023?12:11;put(a[3],base,base+1);put(b[3],base,base+1);put(a[2],base-2,base-1);put(b[2],base-2,base-1);if(year==2023){int w=game(a[1],b[1],2);put(lose(a[1],b[1],w),9,9);qual={a[0],b[0],w};}else qual={a[0],a[1],b[0],b[1]};}
 double8(main_draw(qual));
}
V readv(){int k;cin>>k;V v(k);for(int&i:v)cin>>i;return v;}
VV readvv(){int k;cin>>k;VV v;while(k--)v.push_back(readv());return v;}
int main(int argc,char**argv){cin>>year>>kind>>n;N=argc>1?stoll(argv[1]):14000605;fair=argc>2;rng.seed(year);for(int i=0;i<n;++i)cin>>region[i];for(int i=0;i<n;++i)for(int j=0;j<n;++j){double p;cin>>p;if(fair)p=.5;P[0][i][j]=p;P[1][i][j]=p*p*(3-2*p);P[2][i][j]=p*p*p*(10-15*p+6*p*p);}groups=readvv();main_groups=readvv();opening=readvv();tiers=readvv();direct=readv();byes=readv();cin>>exception_team>>exception_trigger;bye_group=readv();auto start=chrono::steady_clock::now();
 for(long long sim=0;sim<N;++sim){fill(begin(ranklo),end(ranklo),0);fill(begin(rankhi),end(rankhi),0);
  if(kind==0)worlds_groups();else if(kind==1)worlds_swiss();else if(kind==2)msi_old();else if(kind==3)msi_rumble();else if(kind==4)msi_double();else{V a=rr(groups[0],1,2),b=rr(groups[1],1,2);put(a[2],5,6);put(b[2],5,6);put(a[3],7,8);put(b[3],7,8);single({a[0],b[1],b[0],a[1]});}
  double sum=0;int ch=0;for(int i=0;i<n;++i){assert(ranklo[i]>0&&rankhi[i]>=ranklo[i]);sum+=(ranklo[i]+rankhi[i])*.5;if(ranklo[i]==1&&rankhi[i]==1)++ch;++counts[i][ranklo[i]][rankhi[i]];}assert(ch==1);assert(abs(sum-n*(n+1)*.5)<1e-8);
  if((sim+1)%1000000==0)cerr<<year<<" kind "<<kind<<" "<<sim+1<<"/"<<N<<" "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"s\n";
 }
 cout<<"{\"samples\":"<<N<<",\"seed\":"<<year<<",\"duration_seeded_ties\":"<<duration_ties<<",\"complex_tie_scenarios\":"<<complex_ties<<",\"draw_waivers\":"<<waivers<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"counts\":[";
 for(int i=0;i<n;++i){if(i)cout<<',';cout<<'[';bool first=true;for(int lo=1;lo<=n;++lo)for(int hi=lo;hi<=n;++hi)if(counts[i][lo][hi]){if(!first)cout<<',';first=false;cout<<'['<<lo<<','<<hi<<','<<counts[i][lo][hi]<<']';}cout<<']';}cout<<"]}\n";return 0;
}
