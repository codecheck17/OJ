#include <bits/stdc++.h>
#define ll long long int
#define ld long double
const int MAXN=1e5+10;
using namespace std;
void solve(){
   ll n;
   cin>>n;
   while(n!=1){
       cout<<n<<" ";
       if(n&1){
           n*=3;
           n++;
       }else{
           n/=2;  
       } 
   }
   cout<<n<<"\n";
}   
int main() 
{
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);
	int t=1;
	//cin>>t;
    for(int i=1;i<=t;i++){
        solve();
    }
	return 0;
}
