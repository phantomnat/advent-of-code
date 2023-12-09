package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {
	inputFile := "input.txt"

	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	resultPart1 := int64(0)
	resultPart2 := int64(0)

	scanner := bufio.NewScanner(file)

	// ---
	// put code here

	// ---
	inputCount := 0
	for scanner.Scan() {
		inputCount++
		line := scanner.Text()
		fmt.Println(line)
		if line == "" {
			continue
		}

	}

	// another code

	fmt.Println("part 1:", resultPart1)

	// part 2 code

	fmt.Println("part 2:", resultPart2)
}
