#define main simulation_main
#include "simulate.cpp"
#undef main
bool independent_matching(vector<int> v){if(v.empty())return true;int a=v.back();v.pop_back();for(int i=0;i<(int)v.size();++i)if(!(met[a]&(1u<<v[i]))){auto rest=v;rest.erase(rest.begin()+i);if(independent_matching(rest))return true;}return false;}
int main(){rng.seed(87);
 for(int test=0;test<20000;++test){fill(begin(met),end(met),0);for(int a=0;a<8;++a)for(int b=a+1;b<8;++b)if(bounded(2)){met[a]|=1u<<b;met[b]|=1u<<a;}vector<int> v={0,1,2,3,4,5,6,7};bool expected=independent_matching(v);shuffle_v(v);vector<int> slots(8,-1);bool actual=place(v,slots,0,false);assert(expected==actual);if(actual){auto copy=slots;sort(copy.begin(),copy.end());assert(copy==vector<int>({0,1,2,3,4,5,6,7}));for(int i=0;i<8;i+=2)assert(!(met[slots[i]]&(1u<<slots[i+1])));}}
 cout<<"PASS 20000 random forbidden-opponent graphs versus independent matching search\n";
}
