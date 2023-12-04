package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
)

type Pos struct {
	X int
	Y int
}
type Number struct {
	Pos
	Length int
	// Text   string
	Value int
}
type Gear struct {
	Numbers map[Pos]bool
}

func main() {
	inputFile := "input.txt"

	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	resultPart1 := 0
	resultPart2 := 0

	scanner := bufio.NewScanner(file)
	cardToWinCounts := make(map[int]int)
	cardCounts := make(map[int]int)
	cardCount := 0

	for scanner.Scan() {
		line := scanner.Text()
		// fmt.Println(line)
		numbers := strings.Split(line, "|")
		if len(numbers) != 2 {
			panic(fmt.Sprintf("invalid numbers: %d", len(numbers)))
		}
		winnerNumbers := strings.Split(strings.Trim(numbers[0], " "), " ")[2:]
		myNumbers := strings.Split(strings.Trim(numbers[1], " "), " ")
		// fmt.Println("winner: ", winnerNumbers)
		// fmt.Println("my: ", myNumbers)
		winnerNumbersSet := make(map[string]bool)
		winCount := 0
		point := 0
		for _, n := range winnerNumbers {
			if n == "" {
				continue
			}
			winnerNumbersSet[n] = true
		}
		for _, n := range myNumbers {
			if n == "" {
				continue
			}
			if winnerNumbersSet[n] {
				// fmt.Println("  win", n)
				winCount++
				if point == 0 {
					point = 1
				} else {
					point *= 2
				}
			}
		}
		// fmt.Println("card", "point", point)
		resultPart1 += point

		cardCounts[cardCount] = 1
		cardToWinCounts[cardCount] = winCount
		cardCount++
	}

	fmt.Println("part 1:", resultPart1)

	// fmt.Println("card to win count:", cardToWinCounts)
	// fmt.Println("card count:", cardCounts)

	cardIDs := make([]int, 0, len(cardToWinCounts))
	for cid := range cardToWinCounts {
		cardIDs = append(cardIDs, cid)
	}
	sort.Ints(cardIDs)
	for _, cid := range cardIDs {
		winCount := cardToWinCounts[cid]
		for i := 1; i <= winCount; i++ {
			cardCounts[cid+i] += cardCounts[cid]
		}
	}

	// fmt.Println("card to win count:", cardToWinCounts)
	// fmt.Println("card count:", cardCounts)

	for _, cardCount := range cardCounts {
		resultPart2 += cardCount
	}

	fmt.Println("part 2:", resultPart2)
}
