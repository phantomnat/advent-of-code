package main

import (
	"aoc/util"
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
	var spaces [][]byte
	var galaxies []util.Pos

	// ---
	inputCount := 0
	for scanner.Scan() {
		inputCount++
		line := scanner.Text()
		// fmt.Println(line)
		if line == "" {
			continue
		}
		items := []byte(line)
		spaces = append(spaces, items)
	}

	emptySpaceX := findEmptyX(spaces)
	emptySpaceY := findEmptyY(spaces)

	for y := 0; y < len(spaces); y++ {
		for x := 0; x < len(spaces[0]); x++ {
			if spaces[y][x] == '#' {
				galaxies = append(galaxies, util.Pos{X: x, Y: y})
			}
		}
	}

	resultPart1 = findDistance(spaces, galaxies, emptySpaceX, emptySpaceY, 1)

	fmt.Println("part 1:", resultPart1)

	// part 2 code
	resultPart2 = findDistance(spaces, galaxies, emptySpaceX, emptySpaceY, 999_999)

	fmt.Println("part 2:", resultPart2)
}

func findDistance(spaces [][]byte, galaxies []util.Pos, emptySpaceX, emptySpaceY map[util.Pos]bool, emptyDistance int) int64 {
	totalDistance := int64(0)

	for i := 0; i < len(galaxies); i++ {
		for j := i + 1; j < len(galaxies); j++ {
			dist := util.Abs(galaxies[i].X-galaxies[j].X) + util.Abs(galaxies[i].Y-galaxies[j].Y)

			x1, x2 := min(galaxies[i].X, galaxies[j].X), max(galaxies[i].X, galaxies[j].X)
			for x := x1 + 1; x < x2; x++ {
				if emptySpaceX[util.Pos{X: x, Y: 0}] {
					dist += emptyDistance
				}
			}
			y1, y2 := min(galaxies[i].Y, galaxies[j].Y), max(galaxies[i].Y, galaxies[j].Y)
			for y := y1 + 1; y < y2; y++ {
				if emptySpaceY[util.Pos{X: 0, Y: y}] {
					dist += emptyDistance
				}
			}

			totalDistance += int64(dist)
		}
	}
	return totalDistance
}

func findEmptyY(spaces [][]byte) map[util.Pos]bool {
	var emptySpaces = make(map[util.Pos]bool)
	for y := len(spaces) - 1; y >= 0; y-- {
		galaxyCount := 0
		for x := 0; x < len(spaces[0]); x++ {
			if spaces[y][x] == '#' {
				galaxyCount++
			}
		}
		if galaxyCount == 0 {
			emptySpaces[util.Pos{X: 0, Y: y}] = true
		}
	}
	return emptySpaces
}

func findEmptyX(spaces [][]byte) map[util.Pos]bool {
	var emptySpaces = make(map[util.Pos]bool)
	for x := len(spaces[0]) - 1; x >= 0; x-- {
		galaxyCount := 0
		for y := 0; y < len(spaces); y++ {
			if spaces[y][x] == '#' {
				galaxyCount++
				break
			}
		}
		if galaxyCount == 0 {
			emptySpaces[util.Pos{X: x, Y: 0}] = true
		}
	}
	return emptySpaces
}
