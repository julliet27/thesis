#include<bits/stdc++.h>
#define ll long long
#define endline "\n"
using namespace std;
void boundary(vector<string>&text){
    stack<int>stk;
    stk.push(-1); // to find end of the stack
    unordered_map<int,int>mp;
    for(int i=0;i<text.size();i++){
        if(text[i]=="gap") continue;
        size_t found_while=text[i].find("while"); // searching is there any for loop of while in line
        size_t found_for=text[i].find("for");
        if(found_while!=string::npos || found_for!=string::npos){
            int temp=i+1;
            if((text[i][text[i].size()-1]=='{') || (text[i+1][0]=='{')){ //text[i][text[i].size()-1]=='{' ---for (int i = 0; i < 8; ++i){
                if(text[i+1][0]=='{') i++;                               //text[i+1][0]=='{'  ---  {cout<<"lamia"<<endline;
                stk.push(i+1);   // to get the position of '{'
                mp[i+1]=temp;
            }
            else cout<<"loop in :"<<i+1<<" where start from: "<<i+1<<" and end: "<<i+1<<endline;

        };
        for(char chr:text[i]){
            if(chr=='}'){
                int first=stk.top(),last=i+1;
                if(first!=-1){
                    cout<<"loop in :"<<mp[first]<<" where start from: "<<first<<" and end: "<<last<<endline;
                    stk.pop();
                }
            }
        }
    }
}

int main(){
    ifstream my_file("input1.txt");
    string my_text;
    vector<string>vec;
    while(getline(my_file,my_text)){
        my_text.erase(remove(my_text.begin(),my_text.end(),' '),my_text.end()); // remove all whitespace
        if(my_text.size()){
            if(my_text[0]=='/') vec.push_back("gap");
            else vec.push_back(my_text);     // store all line in vector
        }
        else(vec.push_back("gap")); // remove all gaps between line
    }
    boundary(vec);
    my_file.close();
    return 0;
}
