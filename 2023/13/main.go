package main

import (
	"aoc/util"
	"bufio"
	"bytes"
	"fmt"
	"log"
	"os"
)

type MisMatchPoint struct {
	x     *int
	y     *int
	c     int
	count int
	diff  int
}

func (m MisMatchPoint) String() string {
	if m.x != nil {
		return fmt.Sprintf("{x: %d, c: %d}", *m.x, m.c)
	}
	return fmt.Sprintf("{y: %d, c: %d}", *m.y, m.c)
}
func diff(a, b []byte) int {
	if len(a) != len(b) {
		panic("len(a) != len(b)")
	}
	var diff int
	for i := 0; i < len(a); i++ {
		if a[i] != b[i] {
			diff++
		}
	}
	return diff
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

	// ---
	// put code here
	var rows [][][]byte
	var cols [][][]byte
	rows = append(rows, nil)
	verticalIdx := 0

	buildHorizon := func(v [][]byte) [][]byte {
		h := make([][]byte, len(v[0]))
		for i := 0; i < len(v[0]); i++ {
			for j := 0; j < len(v); j++ {
				h[i] = append(h[i], v[j][i])
			}
		}
		return h
	}

	// ---

	inputCount := 0
	for scanner.Scan() {
		inputCount++
		line := scanner.Text()
		// fmt.Println(line)
		if line == "" {
			cols = append(cols, buildHorizon(rows[verticalIdx]))
			verticalIdx++
			rows = append(rows, nil)
			continue
		}
		rows[verticalIdx] = append(rows[verticalIdx], []byte(line))
	}
	cols = append(cols, buildHorizon(rows[verticalIdx]))

	for i := 0; i < len(rows); i++ {
		var mismatches []MisMatchPoint

		for y := 0; y < len(rows[i]); y++ {
			var matchCount int
			var mmp MisMatchPoint
			isMatch := true
			for c := 0; y+c+1 < len(rows[i]) && y-c >= 0; c++ {
				if bytes.Equal(rows[i][y-c], rows[i][y+c+1]) {
					matchCount++
					continue
				}
				isMatch = false
				mmp.count++
				mmp.c = c
				mmp.diff = diff(rows[i][y-c], rows[i][y+c+1])
			}
			if isMatch && matchCount > 0 {
				// fmt.Println("col (y):", y)
				resultPart1 += int64(y+1) * 100
			} else if mmp.count == 1 && mmp.diff == 1 {
				mmp.y = util.Pointer(y)
				mismatches = append(mismatches, mmp)
			}
		}

		for x := 0; x < len(cols[i]); x++ {
			var matchCount int
			isMatch := true
			var mmp MisMatchPoint
			for c := 0; x+c+1 < len(cols[i]) && x-c >= 0; c++ {
				if bytes.Equal(cols[i][x-c], cols[i][x+c+1]) {
					matchCount++
					continue
				}
				isMatch = false
				mmp.count++
				mmp.c = c
				mmp.diff = diff(cols[i][x-c], cols[i][x+c+1])
			}
			if isMatch && matchCount > 0 {
				// fmt.Println("row (x):", x)
				resultPart1 += int64(x + 1)
			} else if mmp.count == 1 && mmp.diff == 1 {
				mmp.x = util.Pointer(x)
				mismatches = append(mismatches, mmp)
			}
		}
		// fmt.Println()
		if len(mismatches) > 1 {
			panic("len(mismatches) > 1")
		}
		for _, mmp := range mismatches {
			if mmp.x != nil {
				resultPart2 += int64(*mmp.x + 1)
			}
			if mmp.y != nil {
				resultPart2 += int64((*mmp.y + 1) * 100)
			}
			// fmt.Println("mis match:", mmp)
		}

		// fmt.Println("------")
	}

	fmt.Println("part 1:", resultPart1)

	fmt.Println("part 2:", resultPart2)
}
