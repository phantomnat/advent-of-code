package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
	"sync"
)

func max(in ...uint16) uint16 {
	if len(in) == 0 {
		return 0
	}
	v := in[0]
	for i := 1; i < len(in); i++ {
		if in[i] > v {
			v = in[i]
		}
	}
	return v
}

func search(minute, costRo, costRc, costRobOre, costRobClay, costRgOre, costRgOb uint16) int {
	visits := make(map[[9]uint16]struct{})

	// minute, ore, clay, ob, g, ro, rc, rob, rg
	nodes := [][9]uint16{{0, 0, 0, 0, 0, 1, 0, 0, 0}}
	maxRO := max(costRc, costRobOre, costRgOre)
	maxRC := costRobClay
	maxRob := costRgOb
	maxG := 0
	var node [9]uint16

	for len(nodes) > 0 {
		node, nodes = nodes[0], nodes[1:]
		min, o, c, ob, g, ro, rc, rob, rg := node[0], node[1], node[2], node[3], node[4], node[5], node[6], node[7], node[8]
		if int(g) > maxG {
			maxG = int(g)
		}
		if min >= minute {
			continue
		}
		if ro > maxRO {
			ro = maxRO
		}
		if rc > maxRC {
			rc = maxRC
		}
		if rob > maxRob {
			rob = maxRob
		}

		maxOPM := maxRO*min - ro*(min-1)
		maxCPM := maxRC*min - rc*(min-1)
		maxObPM := maxRob*min - rob*(min-1)

		if o > maxOPM {
			o = maxOPM
		}
		if c > maxCPM {
			c = maxCPM
		}
		if ob > maxObPM {
			ob = maxOPM
		}
		state := [9]uint16{min, o, c, ob, g, ro, rc, rob, rg}
		if _, ok := visits[state]; ok {
			continue
		}

		visits[state] = struct{}{}

		if minute > 24 && len(visits)%1000000 == 0 {
			log.Printf("%d - max g %d  (%d)", min, maxG, len(visits))
		}

		ns := [9]uint16{min + 1, o + ro, c + rc, ob + rob, g + rg, ro, rc, rob, rg}
		if _, ok := visits[ns]; !ok {
			nodes = append(nodes, ns)
		}

		if o >= costRgOre && ob >= costRgOb {
			ns := [9]uint16{min + 1, o + ro - costRgOre, c + rc, ob + rob - costRgOb, g + rg, ro, rc, rob, rg + 1}
			if _, ok := visits[ns]; !ok {
				nodes = append(nodes, ns)
			}
		}
		if ro+1 <= maxRO && o >= costRo {
			ns := [9]uint16{min + 1, o + ro - costRo, c + rc, ob + rob, g + rg, ro + 1, rc, rob, rg}
			if _, ok := visits[ns]; !ok {
				nodes = append(nodes, ns)
			}
		}
		if rc+1 <= maxRC && o >= costRc {
			ns := [9]uint16{min + 1, o + ro - costRc, c + rc, ob + rob, g + rg, ro, rc + 1, rob, rg}
			if _, ok := visits[ns]; !ok {
				nodes = append(nodes, ns)
			}
		}
		if rob+1 <= maxRob && o >= costRobOre && c >= costRobClay {
			ns := [9]uint16{min + 1, o + ro - costRobOre, c + rc - costRobClay, ob + rob, g + rg, ro, rc, rob + 1, rg}
			if _, ok := visits[ns]; !ok {
				nodes = append(nodes, ns)
			}
		}
	}

	if minute > 24 {
		log.Printf("max g: %d, total states: %d", maxG, len(visits))
	}

	visits = nil

	return int(maxG)
}

func main() {
	inputFile := "2022/input/example"
	inputFile = "2022/input/actual"

	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	output1 := make(chan int)
	output2 := make(chan int)
	done := make(chan struct{})
	wg := new(sync.WaitGroup)

	for scanner.Scan() {
		txts := strings.Split(scanner.Text(), " ")
		id, _ := strconv.Atoi(strings.Trim(txts[1], ":"))
		costRo, _ := strconv.Atoi(txts[6])
		costRc, _ := strconv.Atoi(txts[12])
		costRobOre, _ := strconv.Atoi(txts[18])
		costRobClay, _ := strconv.Atoi(txts[21])
		costRgOre, _ := strconv.Atoi(txts[27])
		costRgOb, _ := strconv.Atoi(txts[30])

		// result := search(24, uint16(costRo), uint16(costRc), uint16(costRobOre), uint16(costRobClay), uint16(costRgOre), uint16(costRgOb))
		// log.Printf("id: %d => %d", id, result*id)
		// total += result * id

		wg.Add(1)
		go func() {
			defer wg.Done()

			result := search(24, uint16(costRo), uint16(costRc), uint16(costRobOre), uint16(costRobClay), uint16(costRgOre), uint16(costRgOb))
			output1 <- result * id
		}()

        if id <= 3 {
            wg.Add(1)
            go func() {
                defer wg.Done()
    
                r2 := search(32, uint16(costRo), uint16(costRc), uint16(costRobOre), uint16(costRobClay), uint16(costRgOre), uint16(costRgOb))
                output2 <- r2
            }()
        }
	}

	wg2 := new(sync.WaitGroup)
	wg2.Add(1)
	go func() {
		total := 0
		total2 := 1
		for {
			select {
			case <-done:
				log.Printf("19.1: %d", total)
				log.Printf("19.2: %d", total2)
				wg2.Done()
				return
			case v := <-output1:
				total += v
			case v2 := <-output2:
				total2 *= v2
			}
		}
	}()

	log.Printf("wait")
	wg.Wait()
	close(done)
	wg2.Wait()

	// 35_069_789
	// 117_064_285
	// 9_888_286
}
