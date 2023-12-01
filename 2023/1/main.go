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

	total := int64(0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		var nums = make([]int64, 0, 2)
		for _, c := range scanner.Text() {
			if c >= '0' && c <= '9' {
				num := int64(c - '0')
				if len(nums) == 2 {
					nums[1] = num
				} else {
					nums = append(nums, num)
				}
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
