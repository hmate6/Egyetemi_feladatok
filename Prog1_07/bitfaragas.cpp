#include<bits/stdc++.h>
using namespace std;int main(){string s,r;cin>>s;for(char c:s)if(isalpha(c))r+=tolower(c);string t=r;reverse(t.begin(),t.end());cout<<((r==t&&r!="")?1:0);int n;cin>>n;vector<int>v(n);for(int&i:v)cin>>i;sort(v.begin(),v.end());for(int x:v)cout<<x<<" ";}
