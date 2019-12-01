#include <cassert>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

#include <gmpxx.h>


mpz_class part_one(std::vector<mpz_class> input) {
	mpz_class total = 0;
	for (auto mass : input)
		total += mass/3 - 2;

	return total;
}

mpz_class part_two(std::vector<mpz_class> input) {
	mpz_class total = 0;
	for (auto mass : input) {
		while ((mass = mass/3 - 2) > 0)
			total += mass;
	}
	return total;
}

int main() {
	std::ifstream raw_input("input");
	auto input = std::vector<mpz_class>();

	std::string line;
	while (std::getline(raw_input, line)) {
		mpz_class tmp;
		tmp.set_str(line, 10);
		input.push_back(tmp);
	}

	//std::cout << part_one(input) << std::endl;
	std::cout << part_two(input) << std::endl;
}