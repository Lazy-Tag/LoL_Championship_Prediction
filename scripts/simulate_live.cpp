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

// Conditional Swiss forecast: preserve completed games and published pairings.
// Input: old probability layout, active list, initial records/history, fixed games.
int main(int argc,char**argv){
 long long N=argc>1?stoll(argv[1]):14000605; rng.seed(argc>2?stoull(argv[2]):2026);
 for(int&i:region)cin>>i;
 for(auto&m:P)for(auto&r:m)for(double&p:r){cin>>p;assert(p>=0&&p<=1);}
 int n;cin>>n;assert(n==16);vector<int> active(n);for(int&i:active)cin>>i;
 int iw[19],il[19];uint32_t im[19];for(int i=0;i<19;i++)cin>>iw[i]>>il[i]>>im[i];
 struct Fixed {int round,a,b,bo;};int nf;cin>>nf;vector<Fixed> fixed(nf);
 for(auto&f:fixed)cin>>f.round>>f.a>>f.b>>f.bo;assert(cin.good());
 long long counts[19][4]={},joint[5][5]={};auto start=chrono::steady_clock::now();
 for(long long sim=0;sim<N;sim++){
  int w[19],loss[19];copy(iw,iw+19,w);copy(il,il+19,loss);copy(im,im+19,met);
  auto play=[&](int x,int y,int bo){assert(w[x]==w[y]&&loss[x]==loss[y]);assert(!(met[x]&(1u<<y)));int win=game(x,y,bo),lose=win==x?y:x;++w[win];++loss[lose];met[x]|=1u<<y;met[y]|=1u<<x;};
  for(int round=1;round<=5;round++){
   for(auto f:fixed)if(f.round==round){assert(w[f.a]+loss[f.a]==round-1);play(f.a,f.b,f.bo);}
   vector<vector<int>> groups(9);
   for(int t:active)if(w[t]<3&&loss[t]<3&&w[t]+loss[t]==round-1)groups[3*w[t]+loss[t]].push_back(t);
   for(auto&g:groups)if(!g.empty()){assert(g.size()%2==0);int bo=(w[g[0]]==2||loss[g[0]]==2)?1:0;auto v=draw(g);for(int j=0;j<(int)v.size();j+=2)play(v[j],v[j+1],bo);}
  }
  vector<int> q0,q1,q2;int cn=0,kr=0;
  for(int t:active){assert(w[t]==3||loss[t]==3);if(w[t]==3){counts[t][1]++;cn+=region[t]==5;kr+=region[t]==1;(loss[t]==0?q0:loss[t]==1?q1:q2).push_back(t);}}
  joint[cn][kr]++;assert(q0.size()==2&&q1.size()==3&&q2.size()==3);
  shuffle_v(q0);shuffle_v(q2);q1.push_back(q2[2]);shuffle_v(q1);
  vector<int> bracket={q0[0],q2[0],q1[0],q1[1],q0[1],q2[1],q1[2],q1[3]},ss;
  for(int i=0;i<8;i+=2){int t=game(bracket[i],bracket[i+1],2);ss.push_back(t);counts[t][2]++;}
  int x=game(ss[0],ss[1],2),y=game(ss[2],ss[3],2);counts[x][3]++;counts[y][3]++;counts[game(x,y,2)][0]++;
  if((sim+1)%1000000==0)cerr<<sim+1<<" / "<<N<<"\n";
 }
 cout<<"{\"simulations\":"<<N<<",\"seed\":2026,\"waived_draw_groups\":"<<waivers<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"counts\":[";
 for(int i=0;i<19;i++){if(i)cout<<',';cout<<'[';for(int j=0;j<4;j++){if(j)cout<<',';cout<<counts[i][j];}cout<<']';}cout<<"],\"joint\":[";
 for(int i=0;i<5;i++){if(i)cout<<',';cout<<'[';for(int j=0;j<5;j++){if(j)cout<<',';cout<<joint[i][j];}cout<<']';}cout<<"]}\n";
}
