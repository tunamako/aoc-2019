#include <cassert>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

#include <gmpxx.h>


void part_one(std::vector<int> input) {}

void part_two(std::vector<int> input) {}

int main() {
	std::ifstream raw_input("input");
	auto input = std::vector<int>();

	std::string value;
	while (std::getline(raw_input, value, ',')) {
		input.push_back(std::stoi(value));
	}

	std::cout << part_one(input) << std::endl;
	std::cout << part_two(input) << std::endl;
}