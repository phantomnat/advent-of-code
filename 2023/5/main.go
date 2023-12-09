package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"slices"
	"sort"
	"strings"

	"aoc/util"
)

type Pair struct {
	Start     int64
	End       int64
	Diff      int64
	DestStart int64
	DestEnd   int64
}

func (p Pair) String() string {
	if p.Diff == 0 && p.DestStart == 0 && p.DestEnd == 0 {
		return fmt.Sprintf("[%d, %d],", p.Start, p.End)
	}
	return fmt.Sprintf("[%d, %d]--(%d)-->[%d, %d],", p.Start, p.End, p.Diff, p.DestStart, p.DestEnd)
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
	var almanacMaps [][]Pair = make([][]Pair, 7)
	// seedsToSoils := make(map[int]int)
	// soilsToFertilizers := make(map[int]int)
	// fertilizersToWaters := make(map[int]int)
	// for i := 0; i < 7; i++ {
	// 	almanacMaps = append(almanacMaps, make(map[int]int))
	// }

	var seeds []int64
	var inputType int

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			inputType = 0
			continue
		}
		switch {
		case strings.HasPrefix(line, "seeds: "):
			for _, txt := range strings.Split(line[7:], " ") {
				num := util.ParseInt64(txt)
				seeds = append(seeds, num)
			}
			continue
		case strings.HasPrefix(line, "seed-to-soil"):
			inputType = 1
			continue
		case strings.HasPrefix(line, "soil-to-fertilizer"):
			inputType = 2
			continue
		case strings.HasPrefix(line, "fertilizer-to-water"):
			inputType = 3
			continue
		case strings.HasPrefix(line, "water-to-light"):
			inputType = 4
			continue
		case strings.HasPrefix(line, "light-to-temperature"):
			inputType = 5
			continue
		case strings.HasPrefix(line, "temperature-to-humidity"):
			inputType = 6
			continue
		case strings.HasPrefix(line, "humidity-to-location"):
			inputType = 7
			continue
		}
		items := strings.Split(line, " ")
		if len(items) != 3 {
			util.Must(fmt.Errorf("invalid input: %s, expecting 3 numbers", line))
		}
		dest := util.ParseInt64(items[0])
		src := util.ParseInt64(items[1])
		length := util.ParseInt64(items[2])
		// fmt.Println("dest:", dest, "src:", src, "length:", length)
		// var targetMap map[int]int
		switch {
		case inputType >= 1 && inputType <= 7:
			// targetMap = almanacMaps[inputType-1]
			almanacMaps[inputType-1] = append(almanacMaps[inputType-1], Pair{
				Start:     src,
				End:       src + length - 1,
				Diff:      dest - src,
				DestStart: dest,
				DestEnd:   length - 1 + dest,
			})
		default:
			continue
		}
	}
	// fmt.Printf("seeds: %#v\n", seeds)
	// fmt.Printf("seed to soil: %v\n", almanacMaps[0])
	// fmt.Printf("soil to fertilizer: %#v\n", almanacMaps[1])

	getDestFromPairs := func(pairs []Pair, srcIdx int64) int64 {
		for i := range pairs {
			if pairs[i].Start <= srcIdx && srcIdx <= pairs[i].End {
				return srcIdx + pairs[i].Diff
			}
		}
		return srcIdx
	}
	getSeedLocation := func(almanacPairs [][]Pair, seed int64) int64 {
		srcIdx := seed
		for i := int64(0); i < int64(len(almanacPairs)); i++ {
			srcIdx = getDestFromPairs(almanacPairs[i], srcIdx)
		}
		return srcIdx
	}
	minLocation := int64(-1)
	// minSeed := -1
	for _, seed := range seeds {
		l := getSeedLocation(almanacMaps, seed)
		if minLocation == -1 || minLocation > l {
			minLocation = l
		}
		// fmt.Println("seed:", seed, "location:", l)
		// resultPart1 += getSeedLocation(seed)
	}
	resultPart1 = minLocation
	fmt.Println("part 1:", resultPart1)
	var seedPairs []Pair
	for i := 0; i+1 < len(seeds); i += 2 {
		seedPairs = append(seedPairs, Pair{Start: seeds[i], End: seeds[i+1] + seeds[i]})
	}
	fmt.Printf("seed pairs: %v\n", seedPairs)
	for i := 0; i < len(almanacMaps); i++ {
		sort.Slice(almanacMaps[i], func(j, k int) bool {
			return almanacMaps[i][j].Start < almanacMaps[i][k].Start
		})
		// fill the gap
		if almanacMaps[i][0].Start != 0 {
			p := Pair{Start: 0, End: almanacMaps[i][0].Start - 1, Diff: 0, DestStart: 0, DestEnd: almanacMaps[i][0].Start - 1}
			almanacMaps[i] = append([]Pair{p}, almanacMaps[i]...)
		}
		lastEnd := almanacMaps[i][0].End
		for j := 1; j < len(almanacMaps[i]); j++ {
			if almanacMaps[i][j].Start != lastEnd+1 {
				// fill the gap
				p := Pair{
					Start:     lastEnd + 1,
					End:       almanacMaps[i][j].Start - 1,
					Diff:      0,
					DestStart: lastEnd + 1,
					DestEnd:   almanacMaps[i][j].Start - 1,
				}
				// insert array into j position
				almanacMaps[i] = slices.Insert(almanacMaps[i], j, p)
			}
			lastEnd = almanacMaps[i][j].End
		}
		// fmt.Printf("%v\n", almanacMaps[i])
	}

	for i := int64(0); i < math.MaxInt64; i++ {
		idx := getSeedIndex(almanacMaps, i)
		if checkSeedExist(seedPairs, idx) {
			resultPart2 = i
			break
		}
	}
	fmt.Println("part 2:", resultPart2)
}

func checkSeedExist(seeds []Pair, seed int64) bool {
	for i := range seeds {
		if seeds[i].Start <= seed && seed <= seeds[i].End {
			return true
		}
	}
	return false
}

func getSeedIndex(almanacPairs [][]Pair, location int64) int64 {
	idx := location
	for i := len(almanacPairs) - 1; i >= 0; i-- {
		for j := range almanacPairs[i] {
			pair := almanacPairs[i][j]
			if pair.DestStart <= idx && idx <= pair.DestEnd {
				idx -= pair.Diff
				break
			}
		}
	}
	return idx
}
