#include <iostream>
using namespace std;

struct het
{
    string nap;
    int ora;
    int perc;
};

int main(){
    het tomb[7] =
    {
        {"Hetfo",8,00},
        {"Kedd",8,10},
        {"Szerda",7,40},
        {"Csutortok",6,20},
        {"Pentek",8,30},
        {"Szombat",9,45},
        {"Szombat",9,20},
    };

    for(int i = 0; i < 7; i++){
        cout << tomb[i].nap << " " << tomb[i].ora << ":" << tomb[i].perc << "\n";
    }
    return 0;
}
