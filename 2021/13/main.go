package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"aoc/utils"
)

type Coor struct {
	X int
	Y int
}
type Fold struct {
	PosX *int
	PosY *int
}

func main() {
	inputFile := "input.txt"

	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	minX, minY := 0, 0
	maxX, maxY := 0, 0
	dots := make(map[Coor]bool)
	var folds []Fold

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// fmt.Println(line)
		if line == "" {
			continue
		}
		if strings.Contains(line, "fold along ") {
			fold := strings.Split(line[len("fold along "):], "=")
			pos, err := strconv.Atoi(fold[1])
			utils.Must(err)

			f := Fold{}
			switch fold[0] {
			case "x":
				f.PosX = utils.Pointer(pos)
			case "y":
				f.PosY = utils.Pointer(pos)
			}
			folds = append(folds, f)
			continue
		}
		coor := strings.Split(line, ",")
		x, _ := strconv.Atoi(coor[0])
		y, _ := strconv.Atoi(coor[1])
		// fmt.Println("coor", x, y)
		dots[Coor{x, y}] = true

		maxX = max(maxX, x)
		maxY = max(maxY, y)
	}
	// print(dots, minX, minY, maxX, maxY)

	for _, fold := range folds {
		if fold.PosX != nil {
			// TODO: check not equal fold
			fmt.Println("fold x", *fold.PosX, "maxX", maxX)
			for x := 1; *fold.PosX-x >= minX && *fold.PosX+x <= maxX; x++ {
				for y := minY; y <= maxY; y++ {
					if dots[Coor{*fold.PosX + x, y}] {
						dots[Coor{*fold.PosX - x, y}] = true
					}
				}
			}
			maxX = *fold.PosX - 1

		} else if fold.PosY != nil {

			// TODO: check not equal fold
			fmt.Println("fold y", *fold.PosY, "maxY", maxY)
			for y := 1; *fold.PosY-y >= minY && *fold.PosY+y <= maxY; y++ {
				for x := minX; x <= maxX; x++ {
					if dots[Coor{x, *fold.PosY + y}] {
						dots[Coor{x, *fold.PosY - y}] = true
					}
				}
			}

			maxY = *fold.PosY - 1
		}
		// print(dots, minX, minY, maxX, maxY)
	}
	print(dots, minX, minY, maxX, maxY)
}

func print(dots map[Coor]bool, minX, minY, maxX, maxY int) {
	count := 0
	for y := minY; y <= maxY; y++ {
		for x := minX; x <= maxX; x++ {
			if dots[Coor{x, y}] {
				fmt.Print("#")
				count++
				continue
			}
			fmt.Print(".")
		}
		fmt.Println()
	}
	fmt.Println("dots:", count, "\n")
}
