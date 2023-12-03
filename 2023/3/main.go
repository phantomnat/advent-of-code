package main

import (
	"aoc/utils"
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
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

	var symbols = make(map[Pos]bool)
	var gears = make(map[Pos]*Gear)
	var numbers = make(map[Pos]Number)

	scanner := bufio.NewScanner(file)
	y := 0
	for scanner.Scan() {
		line := scanner.Text()
		var num *Number
		for x := 0; x < len(line); x++ {
			switch {
			case line[x] == '.':
				// ignore
			case line[x] >= '0' && line[x] <= '9':
				// number
				if num == nil {
					num = &Number{Pos: Pos{X: x, Y: y}, Length: 1}
				} else {
					num.Length++
				}
				continue
			default:
				if line[x] == '*' {
					gears[Pos{X: x, Y: y}] = &Gear{
						Numbers: make(map[Pos]bool),
					}
				}

				// symbols
				symbols[Pos{X: x, Y: y}] = true
			}
			// process number
			if num != nil {
				text := line[num.X : num.X+num.Length]
				value, err := strconv.Atoi(text)
				utils.Must(err)
				num.Value = value
				numbers[Pos{X: num.X, Y: num.Y}] = *num
				// numbers = append(numbers, *num)
			}
			num = nil
		}
		// process number
		if num != nil {
			text := line[num.X : num.X+num.Length]
			value, err := strconv.Atoi(text)
			utils.Must(err)
			num.Value = value
			numbers[Pos{X: num.X, Y: num.Y}] = *num
			// numbers = append(numbers, *num)
		}
		y++
	}

	// fmt.Println("symbols:", len(symbols))
	// fmt.Println("numbers:", len(numbers))

	for _, num := range numbers {
		isPart := false
		// scan for symbols
		// NEXT_NUMBER:
		for y := num.Y - 1; y <= num.Y+1; y++ {
			for x := num.X - 1; x <= num.X+num.Length; x++ {
				gear, isGear := gears[Pos{X: x, Y: y}]
				if isGear {
					gear.Numbers[Pos{X: num.X, Y: num.Y}] = true
				}
				if symbols[Pos{X: x, Y: y}] && !isPart {
					resultPart1 += num.Value
					isPart = true
					// break NEXT_NUMBER
				}
			}
		}
	}

	fmt.Println("part 1:", resultPart1)
	for _, gear := range gears {
		if len(gear.Numbers) == 2 {
			v := 1
			for pos := range gear.Numbers {
				v *= numbers[pos].Value
			}
			resultPart2 += v
		}
	}
	fmt.Println("part 2:", resultPart2)
}
