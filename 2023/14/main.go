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
	var platform [][]byte
	var platform2 [][]byte
	inputCount := 0
	for scanner.Scan() {
		inputCount++
		line := scanner.Text()
		// fmt.Println(line)
		if line == "" {
			continue
		}
		platform = append(platform, []byte(line))
		platform2 = append(platform2, []byte(line))
	}
	maxY := len(platform)
	maxX := len(platform[0])
	// fmt.Println("maxY:", maxY, ", maxX:", maxX)

	// var noMove bool

	// for !noMove {
	// 	noMove = true
	// 	for y := 0; y < maxY-1; y++ {
	// 		for x := 0; x < maxX; x++ {
	// 			isEmpty := platform[y][x] == '.'
	// 			isStoneBelow := platform[y+1][x] == 'O'
	// 			if isEmpty && isStoneBelow {
	// 				platform[y][x] = 'O'
	// 				platform[y+1][x] = '.'
	// 				noMove = false
	// 			}
	// 		}
	// 	}
	// }
	// // fmt.Println()
	// for y := 0; y < maxY; y++ {
	// 	// fmt.Println(string(platform[y]))
	// 	count := 0
	// 	for x := 0; x < maxX; x++ {
	// 		if platform[y][x] == 'O' {
	// 			count++
	// 		}
	// 	}
	// 	resultPart1 += int64(count) * (int64(maxY - y))
	// }
	// fmt.Println()
	resultPart1 = roll(maxX, maxY, platform, "n")

	fmt.Println("part 1:", resultPart1)

	round := int64(0)
	var results []int64
	maxRound := int64(1_000_000_000)
	for int64(round) < maxRound {

		result := int64(0)
		// fmt.Println("------")
		// for y := 0; y < maxY; y++ {
		// 	fmt.Println(string(platform[y]))
		// 	count := 0
		// 	for x := 0; x < maxX; x++ {
		// 		if platform[y][x] == 'O' {
		// 			count++
		// 		}
		// 	}
		// 	result += int64(count) * (int64(maxY - y))
		// }
		roll(maxX, maxY, platform2, "n")
		roll(maxX, maxY, platform2, "w")
		roll(maxX, maxY, platform2, "s")
		result = roll(maxX, maxY, platform2, "e")
		results = append(results, result)
		round++
		half := len(results) / 2
		last := len(results) - 1
		for n := 2; n < half; n++ {
			// for n := half; n > 1; n-- {
			match := true
			for j := 0; j < n; j++ {
				if results[last-j] != results[last-j-n] {
					match = false
					break
				}
			}
			if match {
				// fmt.Println("match:", results[last-n:last], " n:", n)
				resultPart2 = results[last-n : last][(maxRound-round)%int64(n)]
				fmt.Println("part 2:", resultPart2)
				return
			}
		}
		// detect loop
	}

	fmt.Println("part 2:", resultPart2)
}

func roll(maxX, maxY int, platform [][]byte, direction string) int64 {
	noMove := false

	for !noMove {
		noMove = true
		// var startX, startY, endX, endY int

		switch direction {
		case "n":
			// up
			// startX, endX = 0, maxX
			// startY, endY = 0, maxY-1

			for y := 0; y < maxY-1; y++ {
				for x := 0; x < maxX; x++ {
					isEmpty := platform[y][x] == '.'
					isStone := platform[y+1][x] == 'O'
					if isEmpty && isStone {
						platform[y][x] = 'O'
						platform[y+1][x] = '.'
						noMove = false
					}
				}
			}
		case "w":
			// left
			for x := 0; x < maxX-1; x++ {
				for y := 0; y < maxY; y++ {
					isEmpty := platform[y][x] == '.'
					isStone := platform[y][x+1] == 'O'
					if isStone && isEmpty {
						platform[y][x], platform[y][x+1] = 'O', '.'
						noMove = false
					}
				}
			}
		case "s":
			// down
			for y := maxY - 1; y > 0; y-- {
				for x := 0; x < maxX; x++ {
					isEmpty := platform[y][x] == '.'
					isStone := platform[y-1][x] == 'O'
					if isStone && isEmpty {
						platform[y][x], platform[y-1][x] = 'O', '.'
						noMove = false
					}
				}
			}
		case "e":
			// right
			for x := maxX - 1; x > 0; x-- {
				for y := 0; y < maxY; y++ {
					isEmpty := platform[y][x] == '.'
					isStone := platform[y][x-1] == 'O'
					if isStone && isEmpty {
						platform[y][x], platform[y][x-1] = 'O', '.'
						noMove = false
					}
				}
			}
		default:
			panic("invalid direction: " + direction)
		}
	}
	var result int64
	print := false
	if print {
		fmt.Println("------")
	}
	for y := 0; y < maxY; y++ {
		count := 0
		for x := 0; x < maxX; x++ {
			if platform[y][x] == 'O' {
				count++
			}
		}
		result += int64(count) * (int64(maxY - y))
		if print {
			fmt.Println(string(platform[y]))
		}
	}
	// fmt.Println()
	return result
}
