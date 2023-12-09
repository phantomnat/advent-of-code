package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"

	"aoc/util"
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
	resultPart2 := int64(0)

	scanner := bufio.NewScanner(file)
	var times []int
	var distances []int
	var part2Time string
	var part2Distance string
	inputCount := 0
	for scanner.Scan() {
		inputCount++
		line := scanner.Text()
		fields := strings.Fields(line)
		// fmt.Println("fields:", fields)
		if inputCount == 1 {
			for _, txt := range fields[1:] {
				part2Time += txt
				num := util.ParseInt(txt)
				times = append(times, num)
			}
		} else if inputCount == 2 {
			for _, txt := range fields[1:] {
				part2Distance += txt
				num := util.ParseInt(txt)
				distances = append(distances, num)
			}
		}
	}

	// fmt.Println("times:", times)
	// fmt.Println("distance:", distances)
	resultPart1 = 1
	for i := 0; i < len(times); i++ {
		timeLimit := times[i]
		distance := distances[i]
		winCount := 0
		for j := 1; j < distance; j++ {
			currentSpeed := j
			finalDistance := currentSpeed * (timeLimit - j)
			if finalDistance > distance {
				winCount++
			}
		}
		resultPart1 *= winCount
		// fmt.Println("win count:", winCount)
	}
	fmt.Println("part 1:", resultPart1)

	time2 := util.ParseInt64(part2Time)
	distance2 := util.ParseInt64(part2Distance)
	firstWinIndex := int64(0)
	for i := int64(1); i < time2; i++ {
		minSpeed := distance2 / (time2 - i)
		if i > minSpeed {
			firstWinIndex = i
			// fmt.Println(i*(time2-i), ">", distance2)
			break
		}
	}
	lastWinIndex := int64(0)
	for i := time2 - 1; i > 0; i-- {
		minSpeed := distance2 / (time2 - i)
		if i > minSpeed {
			lastWinIndex = i
			// fmt.Println("i:", i, ", dist:", i*(time2-i), ">", distance2)
			break
		}
	}

	// fmt.Println("time 2:", time2, "distance 2:", distance2)
	// fmt.Println("first win index:", firstWinIndex)
	// fmt.Println("last win index:", lastWinIndex)
	resultPart2 = lastWinIndex - firstWinIndex + 1
	fmt.Println("part 2:", resultPart2)
}
