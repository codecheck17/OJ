#include <bits/stdc++.h>
#define ll long long int
#define ld long double
const int MAXN=1e5+10;
using namespace std;
void solve()
{
    int n;
    cin>>n;
    vector<int> a(n-1);
    for(auto &i:a) cin>>i;
    sort(a.begin(),a.end());
    for(int i=0;i<n-1;i++){
        if(a[i]!=i+1){
            cout<<i+1<<"\n";
            return;
        }
    }
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
