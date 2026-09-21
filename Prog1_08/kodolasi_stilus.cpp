#include <iostream>
#include <utility>

struct DataPair {
    int primary;
    int secondary;
};

void printDoubleLine() {
    std::cout << "===\n";
}

void printSingleLine() {
    std::cout << "---\n";
}

void printHeader() {
    std::cout << "Output:\n";
}

void bubbleSortByPrimary(DataPair* data, int length) {
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < length - 1; j++) {
            if (data[j].primary > data[j + 1].primary) {
                std::swap(data[j], data[j + 1]);
            }
        }
    }
}

void processAndPrintData(DataPair* data, int length) {
    for (int i = 0; i < length; i++) {
        int p = data[i].primary;
        int s = data[i].secondary;
        int result = 0;

        if (p % 2 == 0) {
            if (s % 2 == 0) {
                result = p * s;
            } else {
                result = p + s;
            }
        } else {
            if (s % 2 == 0) {
                result = p - s;
            } else {
                result = p;
            }
        }
        
        std::cout << result << "\n";
    }
}

void executePipeline(DataPair* data, int length) {
    bubbleSortByPrimary(data, length);
    printDoubleLine();
    printHeader();
    printSingleLine();
    processAndPrintData(data, length);
}

int main() {
    DataPair dataset[5] = {
        {5, 1},
        {2, 4},
        {3, 7},
        {1, 6},
        {4, 5}
    };

    executePipeline(dataset, 5);

    return 0;
}
