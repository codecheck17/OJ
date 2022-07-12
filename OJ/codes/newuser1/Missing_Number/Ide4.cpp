#include <bits/stdc++.h>
#define ll long long int
const int M=1e9+7;
using namespace std;
int getAll(vector<int>& a,int x,int curr,vector<vector<int>>& dp){
    if(curr==a.size())
        return (x==0)?1:0;
    if(x<=0)
        return (x==0)?1:0;
    if(dp[curr][x]!=-1)
        return dp[curr][x];
    if(a[curr]>x)
        return dp[curr][x]=getAll(a,x,curr+1,dp);
    
    int smallAns1=getAll(a,x-a[curr],curr,dp);
    int smallAns2=getAll(a,x,curr+1,dp);
    return dp[curr][x]=(smallAns1+smallAns2)%M;
}
void solve()
{
    int n,x;
    cin>>n>>x;
    vector<int> a(n,0);
    vector<vector<int>> dp(n,vector<int>(x+1,-1));
    for(int i=0;i<n;i++){
        cin>>a[i];
    }
    sort(a.begin(),a.end());
    int ans=getAll(a,x,0,dp);
    cout<<ans<<"\n";
}
int main() 
{
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);
	int t=1;
	//cin>>t;
	while(t--)
	{
	   solve();
	}
	return 0;
}