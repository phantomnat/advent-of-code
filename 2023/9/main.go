package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"

	"aoc/util"
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
	var seqs [][]int64
	// ---
	inputCount := 0
	for scanner.Scan() {
		inputCount++
		line := scanner.Text()
		// fmt.Println(line)
		if line == "" {
			continue
		}

		var seq []int64
		for _, f := range strings.Fields(line) {
			seq = append(seq, util.ParseInt64(f))
		}

		seqs = append(seqs, seq)
	}

	// another code

	// fmt.Println("seqs:", seqs)
	for i := range seqs {

		var diffMap [][]int64
		diffMap = append(diffMap, seqs[i])
		diffMapIdx := 0

		// fmt.Println("i", i)
		// fmt.Println("diffMap:", diffMapIdx, ", map:", diffMap[diffMapIdx])
		for !util.IsTheSame(diffMap[diffMapIdx], 0) {
			diffMap = append(diffMap, []int64{})
			for j := 1; j < len(diffMap[diffMapIdx]); j++ {
				diffMap[diffMapIdx+1] = append(diffMap[diffMapIdx+1], diffMap[diffMapIdx][j]-diffMap[diffMapIdx][j-1])
			}
			diffMapIdx++
			// fmt.Println("diffMap:", diffMapIdx, ", map:", diffMap[diffMapIdx])
		}

		diffVal := int64(0)
		for j := len(diffMap) - 1; j >= 0; j-- {
			diffVal = util.Last(diffMap[j]) + diffVal
		}
		resultPart1 += diffVal
		// a b
		//  c
		// b - a = c
		// a = b - c
		diffVal = 0
		for j := len(diffMap) - 1; j >= 0; j-- {
			diffVal = diffMap[j][0] - diffVal
		}
		resultPart2 += diffVal
	}

	fmt.Println("part 1:", resultPart1)

	// part 2 code

	fmt.Println("part 2:", resultPart2)
}
