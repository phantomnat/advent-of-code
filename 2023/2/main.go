package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func must(err error, msg string, args ...any) {
	if err != nil {
		panic(fmt.Sprintf(msg, args...))
	}
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func main() {
	inputFile := "input.txt"

	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	MaxR := 12
	MaxG := 13
	MaxB := 14
	result := 0
	result2 := 0

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// fmt.Println(line)
		items := strings.Split(line, " ")
		gameID, err := strconv.Atoi(items[1][:len(items[1])-1])
		must(err, "invalid gameID '%v'", items[1])
		possible := true
		r, g, b := 0, 0, 0

		// fmt.Println("game id", gameID)
		for i := 2; i+1 < len(items); i += 2 {
			no, err := strconv.Atoi(items[i])
			must(err, "invalid number '%v'", items[i])

			color := strings.TrimRightFunc(items[i+1], func(r rune) bool {
				switch r {
				case ',', ';':
					return true
				}
				return false
			})

			switch color {
			case "red":
				possible = possible && no <= MaxR
				r = max(r, no)
			case "green":
				possible = possible && no <= MaxG
				g = max(g, no)
			case "blue":
				possible = possible && no <= MaxB
				b = max(b, no)
			default:
			}
			// if !possible {
			// 	break
			// }
			// fmt.Println("no", no, "color", color)
		}
		if possible {
			result += gameID
		}
		// game 2
		fmt.Println("game id", gameID, "rgb", (r * g * b))
		result2 += (r * g * b)
	}
	fmt.Println("result:", result)
	fmt.Println("result2:", result2)
}
