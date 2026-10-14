#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
mt19937_64 rng;
uint64_t bounded(uint64_t n){uint64_t x,t=-n%n;do{x=rng();}while(x<t);return x%n;}
double uniform01(){return (rng()>>11)*0x1.0p-53;}
void shuffle_v(vector<int>&v){for(int i=(int)v.size()-1;i>0;--i)swap(v[i],v[bounded(i+1)]);}
double P[3][19][19];int region[19];uint32_t met[19];long long waivers=0;
int game(int a,int b,int bo){return uniform01()<P[bo][a][b]?a:b;}
// Draw a uniformly shuffled team order, then place each drawn team in the
// earliest empty slot that permits completion. Backtracking supplies lookahead.
bool place(const vector<int>&order,vector<int>&slots,int k,bool initial){
 if(k==(int)order.size())return true;
 int t=order[k];
 for(int s=0;s<(int)slots.size();++s)if(slots[s]<0){
  int other=slots[s^1];
  if(other>=0 && (initial?region[t]==region[other]:(met[t]&(1u<<other))))continue;
  slots[s]=t;if(place(order,slots,k+1,initial))return true;slots[s]=-1;
 }
 return false;
}
vector<int> draw(vector<int> group){
 shuffle_v(group);vector<int> slots(group.size(),-1);
 if(!place(group,slots,0,false)){++waivers;return group;}
 return slots;
}
vector<int> first_draw(vector<int> high, vector<int> low){
 shuffle_v(high);shuffle_v(low);vector<int> slots(8,-1);
 for(int i=0;i<4;++i)slots[2*i]=high[i];
 bool ok=place(low,slots,0,true);assert(ok);return slots;
}
int main(int argc,char**argv){
 long long N=argc>1?stoll(argv[1]):14000605;uint64_t seed=argc>2?stoull(argv[2]):2026;
 bool fair=argc>3; rng.seed(seed);
 for(int&i:region)cin>>i;
 for(auto&m:P)for(auto&r:m)for(double&p:r){cin>>p;if(fair)p=.5;}
 long long champion[19]={},qualified[19]={},quarters[19]={},semis[19]={},finals[19]={};
 auto start=chrono::steady_clock::now();
 for(long long sim=0;sim<N;++sim){
  int a=game(13,10,2),b=game(18,16,2),la=a==13?10:13,lb=b==18?16:18;
  int u=game(a,b,2),lu=u==a?b:a,l=game(la,lb,2),f=game(lu,l,2),pi=game(u,f,2);++qualified[pi];
  vector<int> active;for(int i=0;i<19;++i)if(i!=10&&i!=13&&i!=16&&i!=18){active.push_back(i);++qualified[i];}active.push_back(pi);
  int w[19]={},loss[19]={};fill(begin(met),end(met),0);
  auto play=[&](const vector<int>&v,int bo){for(int j=0;j<(int)v.size();j+=2){int x=v[j],y=v[j+1];assert(w[x]==w[y]&&loss[x]==loss[y]);int winner=game(x,y,bo),loser=winner==x?y:x;++w[winner];++loss[loser];met[x]|=1u<<y;met[y]|=1u<<x;}};
  play(first_draw({4,0,11,8},{15,3,7,pi}),0);
  play(first_draw({14,17,5,1},{12,9,6,2}),0);
  for(int round=2;round<=5;++round){
   vector<vector<int>> groups(9);
   for(int t:active)if(w[t]<3&&loss[t]<3)groups[3*w[t]+loss[t]].push_back(t);
   for(auto&g:groups)if(!g.empty()){assert(g.size()%2==0);int bo=(w[g[0]]==2||loss[g[0]]==2)?1:0;play(draw(g),bo);}
  }
  vector<int> q0,q1,q2;
  for(int t:active){assert(w[t]==3||loss[t]==3);if(w[t]==3){++quarters[t];(loss[t]==0?q0:loss[t]==1?q1:q2).push_back(t);}}
  assert(q0.size()==2&&q1.size()==3&&q2.size()==3);
  shuffle_v(q0);shuffle_v(q2);q1.push_back(q2[2]);shuffle_v(q1);
  vector<int> bracket={q0[0],q2[0],q1[0],q1[1],q0[1],q2[1],q1[2],q1[3]};
  vector<int> ss;for(int i=0;i<8;i+=2){int t=game(bracket[i],bracket[i+1],2);ss.push_back(t);++semis[t];}
  int x=game(ss[0],ss[1],2),y=game(ss[2],ss[3],2);++finals[x];++finals[y];++champion[game(x,y,2)];
  if((sim+1)%1000000==0)cerr<<sim+1<<" / "<<N<<" elapsed "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<" s\n";
 }
 cout<<"{\"simulations\":"<<N<<",\"seed\":"<<seed<<",\"waived_draw_groups\":"<<waivers<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"counts\":[";
 for(int i=0;i<19;++i){if(i)cout<<',';cout<<"["<<champion[i]<<','<<qualified[i]<<','<<quarters[i]<<','<<semis[i]<<','<<finals[i]<<"]";}cout<<"]}\n";
 return 0;
}
