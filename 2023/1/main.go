package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {
	// fmt.Printf("hello")

	inputFile := "input.txt"

	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	wordToNumbers := []string{
		"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
	}

	total := int64(0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		var nums = make([]int64, 0, 2)
		var num *int64

		line := scanner.Text()
		for i, c := range line {
			for j, word := range wordToNumbers {
				if len(word)+i <= len(line) && line[i:i+len(word)] == word {
					n := int64(j)
					num = &n
					break
				}
			}
			if c >= '0' && c <= '9' {
				n := int64(c - '0')
				num = &n
			}
			if num != nil {
				if len(nums) == 2 {
					nums[1] = *num
				} else {
					nums = append(nums, *num)
				}
				num = nil
			}
		}
		if len(nums) == 0 {
			panic("found no numbers")
		}
		if len(nums) == 1 {
			nums = append(nums, nums[0])
		}
		total += (nums[0] * 10) + nums[1]
		// fmt.Println()
	}
	fmt.Println(total)
}
