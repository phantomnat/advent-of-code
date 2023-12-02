package main

import (
	"aoc/utils"
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

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
		utils.Must(err, "invalid gameID")
		possible := true
		r, g, b := 0, 0, 0

		// fmt.Println("game id", gameID)
		for i := 2; i+1 < len(items); i += 2 {
			no, err := strconv.Atoi(items[i])
			utils.Must(err, "invalid number")

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
		}
		if possible {
			result += gameID
		}
		fmt.Println("game id", gameID, "rgb", (r * g * b))
		result2 += (r * g * b)
	}
	fmt.Println("result:", result)
	fmt.Println("result2:", result2)
}
