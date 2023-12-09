package main

import (
	"aoc/utils"
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

type Node struct {
	Left  string
	Right string
}

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

	inputCount := 0

	nodes := make(map[string]Node)
	var startNodes []string
	var instruction string
	for scanner.Scan() {
		inputCount++
		line := scanner.Text()
		// fmt.Println(line)
		if line == "" {
			continue
		}
		if inputCount == 1 {
			instruction = line
			continue
		}
		items := strings.Fields(strings.Replace(strings.Replace(strings.Replace(line, " = (", " ", -1), ", ", " ", -1), ")", "", -1))
		nodes[items[0]] = Node{Left: items[1], Right: items[2]}
		if items[0][2] == 'A' {
			startNodes = append(startNodes, items[0])
		}
	}
	stepCount := 0
	currentNode := startNodes[0]
	for {
		c := instruction[stepCount%len(instruction)]
		if currentNode[2] == 'Z' {
			break
		}

		if c == 'L' {
			currentNode = nodes[currentNode].Left
		} else if c == 'R' {
			currentNode = nodes[currentNode].Right
		} else {
			utils.MustTrue(1 == 0, "unknown instruction: %c", c)
		}
		stepCount++
	}

	// fmt.Println("nodes", nodes)
	resultPart1 = int64(stepCount)
	fmt.Println("part 1:", resultPart1)

	stepCount = 0
	fmt.Println("start nodes:", startNodes)

	stepCounts := make([]int64, len(startNodes))

	for i := range startNodes {
		currentNode := startNodes[i]
		stepCount = 0
		for {
			if currentNode[2] == 'Z' {
				break
			}
			c := instruction[stepCount%len(instruction)]
			if c == 'L' {
				currentNode = nodes[currentNode].Left
			} else if c == 'R' {
				currentNode = nodes[currentNode].Right
			} else {
				utils.MustTrue(1 == 0, "unknown instruction: %c", c)
			}

			stepCount++
		}
		stepCounts[i] = int64(stepCount)
		fmt.Println("node:", startNodes[i], "step count:", stepCount)
	}

	fmt.Println("step counts:", stepCounts)

	resultPart2 = lcmOfSlices(stepCounts, 0)

	fmt.Println("part 2:", resultPart2)
}

func gcd(a, b int64) int64 {
	if a == 0 {
		return b
	}
	return gcd(b%a, a)
}

func lcmOfSlices(slices []int64, idx int) int64 {
	if idx == len(slices)-1 {
		return slices[idx]
	}
	a := slices[idx]
	b := lcmOfSlices(slices, idx+1)
	return a * b / gcd(a, b)
}
