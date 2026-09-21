#include <iostream>
#include <windows.h>

using namespace std;

void gotoxy(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

void hideCursor() {
    HANDLE consoleHandle = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_CURSOR_INFO info;
    info.dwSize = 100;
    info.bVisible = FALSE;
    SetConsoleCursorInfo(consoleHandle, &info);
}

int main() {
    const int WIDTH = 40;
    const int HEIGHT = 15;
    
    int x = 5, y = 5;
    int dx = 1, dy = 1;

    hideCursor();
    system("cls");

    for (int i = 0; i <= WIDTH; i++) {
        gotoxy(i, 0); cout << "#";   
        gotoxy(i, HEIGHT); cout << "#";  
    }
    for (int i = 0; i <= HEIGHT; i++) {
        gotoxy(0, i); cout << "#";   
        gotoxy(WIDTH, i); cout << "#";  
    }

    while (true) {
        gotoxy(x, y);
        cout << " ";
        x += dx;
        y += dy;
        
        if (x <= 1 || x >= WIDTH - 1) dx *= -1;
        if (y <= 1 || y >= HEIGHT - 1) dy *= -1;

        gotoxy(x, y);
        cout << "O";

        Sleep(45); 
    }

    return 0;
}
