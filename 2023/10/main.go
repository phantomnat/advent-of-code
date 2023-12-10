package main

import (
	"bufio"
	"bytes"
	"fmt"
	"log"
	"os"
)

type Pos struct {
	X int
	Y int
}

type OuterPosSide int

const (
	OuterPosSideDownRight = 1 << iota
	OuterPosSideDown
	OuterPosSideDownLeft
	OuterPosSideRight
	OuterPosSideCenter
	OuterPosSideLeft
	OuterPosSideUpRight
	OuterPosSideUp
	OuterPosSideUpLeft
)

const (
	OuterPosSideAll = OuterPosSideLeft | OuterPosSideRight | OuterPosSideUp | OuterPosSideDown | OuterPosSideUpLeft | OuterPosSideUpRight | OuterPosSideDownLeft | OuterPosSideDownRight

	// return "║"
	OuterPosSide_Left_UD  = OuterPosSideLeft | OuterPosSideUpLeft | OuterPosSideDownLeft
	OuterPosSide_Right_UD = OuterPosSideRight | OuterPosSideUpRight | OuterPosSideDownRight

	// return "═"
	OuterPosSide_Up_LR   = OuterPosSideUp | OuterPosSideUpLeft | OuterPosSideUpRight
	OuterPosSide_Down_LR = OuterPosSideDown | OuterPosSideDownLeft | OuterPosSideDownRight

	// return "╚"
	OuterPosSide_Lower_Left = OuterPosSide_Down_LR | OuterPosSide_Left_UD

	// return "╝"
	OuterPosSide_Lower_Right = OuterPosSide_Down_LR | OuterPosSide_Right_UD

	// return "╗"
	OuterPosSide_Upper_Right = OuterPosSide_Up_LR | OuterPosSide_Right_UD

	// return "╔"
	OuterPosSide_Upper_Left = OuterPosSide_Up_LR | OuterPosSide_Left_UD
)

type OuterPos struct {
	Pos
	Side OuterPosSide
}

// func (p OuterPos) Add(x, y int, side OuterPosSide) OuterPos {
// 	return OuterPos{p.Pos.Add(x, y), side}
// }

func newOuterPos(p Pos, addX, addY int, side OuterPosSide) OuterPos {
	return OuterPos{p.Add(addX, addY), side}
}

func (p Pos) Add(x, y int) Pos {
	return Pos{p.X + x, p.Y + y}
}

type Pipe struct {
	Pos
	Type string
}

func (p Pipe) Allow(in Pos) bool {
	isSameX, isSameY := p.X == in.X, p.Y == in.Y
	isUpper := in.Y == p.Y-1
	isLower := in.Y == p.Y+1
	isLeft := in.X == p.X-1
	isRight := in.X == p.X+1
	switch p.Type {
	case "|":
		return isSameX && (isUpper || isLower)
	case "-":
		return isSameY && (isLeft || isRight)
	case "L":
		return (isSameX && isUpper) || (isSameY && isRight)
	case "J":
		return (isSameX && isUpper) || (isSameY && isLeft)
	case "7":
		return (isSameX && isLower) || (isSameY && isLeft)
	case "F":
		return (isSameX && isLower) || (isSameY && isRight)
	}
	return false
}

func (p Pipe) String() string {
	switch p.Type {
	case "-":
		return "═"
	case "|":
		return "║"
	case "L":
		return "╚"
	case "J":
		return "╝"
	case "7":
		return "╗"
	case "F":
		return "╔"
	}
	panic("pipe type not found" + p.Type)
}

func (p Pipe) Nexts() []Pos {
	switch p.Type {
	case "|":
		return []Pos{p.Add(0, 1), p.Add(0, -1)}
	case "-":
		return []Pos{p.Add(1, 0), p.Add(-1, 0)}
	case "L":
		return []Pos{p.Add(1, 0), p.Add(0, -1)}
	case "J":
		return []Pos{p.Add(-1, 0), p.Add(0, -1)}
	case "7":
		return []Pos{p.Add(0, 1), p.Add(-1, 0)}
	case "F":
		return []Pos{p.Add(0, 1), p.Add(1, 0)}
	}
	panic("pipe type not found" + p.Type)
}

func (p Pipe) NextOuter(in OuterPos) OuterPos {
	isSameX := p.X == in.X
	isSameY := p.Y == in.Y
	isUpper := in.Y == p.Y-1
	isLower := in.Y == p.Y+1
	isLeft := in.X == p.X-1
	isRight := in.X == p.X+1
	var side OuterPosSide
	switch p.Type {
	case "|":
		if isSameY {
			// right
			if isRight {
				return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSide_Right_UD)
			}
			// left
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSide_Left_UD)
		}

		// up or down
		if isLower {
			if in.Side&OuterPosSideUpRight > 0 {
				side = OuterPosSide_Right_UD
			}
			if in.Side&OuterPosSideUpLeft > 0 {
				side = OuterPosSide_Left_UD
			}
		}
		if isUpper {
			if in.Side&OuterPosSideDownRight > 0 {
				side = OuterPosSide_Right_UD
			}
			if in.Side&OuterPosSideDownLeft > 0 {
				side = OuterPosSide_Left_UD
			}
		}
	case "-":
		if isSameX {
			if isUpper {
				return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSide_Up_LR)
			}

			// down
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSide_Down_LR)
		}
		if isLeft {
			if in.Side&OuterPosSideUpRight > 0 {
				side = OuterPosSide_Up_LR
			}
			if in.Side&OuterPosSideDownRight > 0 {
				side = OuterPosSide_Down_LR
			}
		}
		if isRight {
			if in.Side&OuterPosSideUpLeft > 0 {
				side = OuterPosSide_Up_LR
			}
			if in.Side&OuterPosSideDownLeft > 0 {
				side = OuterPosSide_Down_LR
			}
		}
	case "L":
		if isLower || isLeft {
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSide_Lower_Left)
		}
		if isUpper && isRight {
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSideUpRight)
		}
		if isRight && isSameY {
			if in.Side&OuterPosSideUpLeft > 0 {
				side = OuterPosSideUpRight
			}
			if in.Side&OuterPosSideDownLeft > 0 {
				side = OuterPosSide_Lower_Left
			}
		}
		if isUpper && isSameX {
			if in.Side&OuterPosSideDownRight > 0 {
				side = OuterPosSideUpRight
			}
			if in.Side&OuterPosSideDownLeft > 0 {
				side = OuterPosSide_Lower_Left
			}
		}
	case "J":
		if isLower || isRight {
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSide_Lower_Right)
		}
		// top left
		if isUpper && isLeft {
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSideUpLeft)
		}
		if isLeft && isSameY {
			if in.Side&OuterPosSideDownRight > 0 {
				side = OuterPosSide_Lower_Right
			}
			if in.Side&OuterPosSideUpRight > 0 {
				side = OuterPosSideUpLeft
			}
		}
		if isUpper && isSameX {
			if in.Side&OuterPosSideDownRight > 0 {
				side = OuterPosSide_Lower_Right
			}
			if in.Side&OuterPosSideDownLeft > 0 {
				side = OuterPosSideUpLeft
			}
		}
	case "7":
		if isUpper || isRight {
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSide_Upper_Right)
		}
		if isLower && isLeft {
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSideDownLeft)
		}
		if isLeft && isSameY {
			if in.Side&OuterPosSideUpRight > 0 {
				side = OuterPosSide_Upper_Right
			}
			if in.Side&OuterPosSideDownRight > 0 {
				side = OuterPosSideDownLeft
			}
		}
		if isLower && isSameX {
			if in.Side&OuterPosSideUpRight > 0 {
				side = OuterPosSide_Upper_Right
			}
			if in.Side&OuterPosSideUpLeft > 0 {
				side = OuterPosSideDownLeft
			}
		}
	case "F":
		if isUpper || isLeft {
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSide_Upper_Left)
		}
		if isLower && isRight {
			return newOuterPos(p.Pos, 0, 0, in.Side&OuterPosSideDownRight)
		}
		if isRight && isSameY {
			if in.Side&OuterPosSideUpLeft > 0 {
				side = OuterPosSide_Upper_Left
			}
			if in.Side&OuterPosSideDownLeft > 0 {
				side = OuterPosSideDownRight
			}
		}
		if isLower && isSameX {
			if in.Side&OuterPosSideUpRight > 0 {
				side = OuterPosSideDownRight
			}
			if in.Side&OuterPosSideUpLeft > 0 {
				side = OuterPosSide_Upper_Left
			}
		}
	}
	if side == 0 {
		panic(fmt.Sprintln("unexpected side", "in", in, "pipe", p))
	}
	return newOuterPos(p.Pos, 0, 0, side)
}

func (p Pipe) Next(x, y int) (int, int) {
	addX, addY := 0, 0
	isUpper := y == p.Y-1
	isLower := y == p.Y+1
	isLeft := x == p.X-1
	isRight := x == p.X+1
	switch p.Type {
	case "|":
		addY = 1
		if isLower {
			addY = -1
		}
	case "-":
		addX = 1
		if isRight {
			addX = -1
		}
	case "L":
		if isUpper {
			addX = 1
		} else if isRight {
			addY = -1
		}
	case "J":
		if isUpper {
			addX = -1
		} else if isLeft {
			addY = -1
		}
	case "7":
		if isLower {
			addX = -1
		} else if isLeft {
			addY = 1
		}
	case "F":
		if isLower {
			addX = 1
		} else if isRight {
			addY = 1
		}
	}
	return p.X + addX, p.Y + addY
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
	var start Pos
	var maxX, maxY int
	pipes := make(map[Pos]Pipe)
	// ---

	inputCount := 0
	for scanner.Scan() {
		inputCount++
		line := scanner.Text()
		fmt.Println(line)
		if line == "" {
			continue
		}
		for i, c := range line {
			if c == '.' {
				continue
			}
			if c == 'S' {
				start = Pos{i, inputCount - 1}
				continue
			}
			p := Pipe{Pos{i, inputCount - 1}, string(c)}
			pipes[Pos{i, inputCount - 1}] = p

		}
		maxX = len(line)
	}

	// another code
	fmt.Println()
	fmt.Println("start", start)
	fmt.Println("maxX", maxX)
	fmt.Println("maxY", maxY)
	maxY = inputCount

	positions := []Pos{start}
	nextPositions := make(map[Pos]struct{})
	pipeDistances := make(map[Pos]int)
	var pos Pos
	pipeDistance := 0
	pipeDistances[start] = 0

	for len(positions) > 0 {
		pos, positions = positions[0], positions[1:]
		if pos == start {
			for _, nextP := range []Pos{pos.Add(0, 1), pos.Add(1, 0), pos.Add(0, -1), pos.Add(-1, 0)} {
				if _, ok := pipes[nextP]; ok && pipes[nextP].Allow(pos) {
					nextPositions[nextP] = struct{}{}
					// nextPositions = append(nextPositions, nextP)
					// pipeDistances[nextP] = pipeDistance + 1
				}
			}
		}
		if _, ok := pipes[pos]; ok {
			pipeDistances[pos] = pipeDistance
			for _, nextPipe := range pipes[pos].Nexts() {
				if _, exist := pipes[nextPipe]; !exist {
					continue
				}
				if _, exist := pipeDistances[nextPipe]; exist {
					continue
				}
				nextPositions[nextPipe] = struct{}{}
				// nextPositions = append(nextPositions, nextPipe)
			}
		}
		if len(positions) == 0 {
			pipeDistance++
			positions = make([]Pos, 0, len(nextPositions))
			for p := range nextPositions {
				positions = append(positions, p)
			}
			nextPositions = make(map[Pos]struct{})
			// positions = nextPositions
			// nextPositions = nil
		}
	}

	resultPart1 = int64(pipeDistance) - 1

	fmt.Println("part 1:", resultPart1)

	// part 2 code
	var outerPos OuterPos
	outerLoopVisits := make(map[Pos]struct{})
	var outerLoops []OuterPos
	nextOuterLoops := make(map[OuterPos]struct{})

	for y := 0; y < maxY; y++ {
		p1 := OuterPos{Pos{0, y}, OuterPosSideAll}
		if _, exist := pipeDistances[p1.Pos]; exist {
			continue
		}
		p2 := OuterPos{Pos{maxX - 1, y}, OuterPosSideAll}
		outerLoops = append(outerLoops, p1, p2)
		outerLoopVisits[p1.Pos] = struct{}{}
		outerLoopVisits[p2.Pos] = struct{}{}
	}
	for x := 0; x < maxX; x++ {
		p1 := OuterPos{Pos{x, 0}, OuterPosSideAll}
		p2 := OuterPos{Pos{x, maxY - 1}, OuterPosSideAll}
		outerLoops = append(outerLoops, p1, p2)
		outerLoopVisits[p1.Pos] = struct{}{}
		outerLoopVisits[p2.Pos] = struct{}{}
	}

	for len(outerLoops) > 0 {
		outerPos, outerLoops = outerLoops[0], outerLoops[1:]

		outerLoopVisits[outerPos.Pos] = struct{}{}
		// nextLeft := outerPos.Add(-1, 0)
		// nextRight := outerPos.Add(1, 0)
		// nextUp := outerPos.Add(0, -1)
		// nextDown := outerPos.Add(0, 1)

		for _, nextP := range []Pos{outerPos.Add(0, 1), outerPos.Add(1, 0), outerPos.Add(0, -1), outerPos.Add(-1, 0)} {
			if _, exist := outerLoopVisits[nextP]; exist {
				continue
			}
			if nextP == start {
				continue
			}
			isLeft := nextP.X == outerPos.X-1
			canGoLeft := outerPos.Side&OuterPosSideLeft > 0 || outerPos.Side&OuterPosSideDownLeft > 0 || outerPos.Side&OuterPosSideUpLeft > 0
			isRight := nextP.X == outerPos.X+1
			canGoRight := outerPos.Side&OuterPosSideRight > 0 || outerPos.Side&OuterPosSideDownRight > 0 || outerPos.Side&OuterPosSideUpRight > 0
			isUp := nextP.Y == outerPos.Y-1
			canGoUp := outerPos.Side&OuterPosSideUp > 0 || outerPos.Side&OuterPosSideUpLeft > 0 || outerPos.Side&OuterPosSideUpRight > 0
			isDown := nextP.Y == outerPos.Y+1
			canGoDown := outerPos.Side&OuterPosSideDown > 0 || outerPos.Side&OuterPosSideDownLeft > 0 || outerPos.Side&OuterPosSideDownRight > 0
			if (isLeft && !canGoLeft) || // left
				(isRight && !canGoRight) || // right
				(isUp && !canGoUp) || // up
				(isDown && !canGoDown) { // down
				continue
			}

			if _, exist := pipeDistances[nextP]; exist {
				pipe := pipes[nextP]
				nextOuterLoops[pipe.NextOuter(outerPos)] = struct{}{}
				// for _, nextOuter := range pipe.NextOuters(outerPos) {
				// 	if _, exist := outerLoopVisits[nextOuter.Pos]; exist {
				// 		continue
				// 	}
				// 	nextOuterLoops[OuterPos{nextP, nextOuter.Side}] = struct{}{}
				// }
				// pipe.NextOuters()
				continue
			}
			if nextP.X < 0 || nextP.X >= maxX || nextP.Y < 0 || nextP.Y >= maxY {
				continue
			}
			nextOuterLoops[OuterPos{nextP, OuterPosSideAll}] = struct{}{}
		}

		if len(outerLoops) == 0 && len(nextOuterLoops) > 0 {
			outerLoops = make([]OuterPos, 0, len(nextOuterLoops))
			for nextP := range nextOuterLoops {
				outerLoops = append(outerLoops, nextP)
			}
			nextOuterLoops = make(map[OuterPos]struct{})
			// printMap(maxX, maxY, start, pipeDistances, pipes, outerLoopVisits)
		}
	}
	printMap(maxX, maxY, start, pipeDistances, pipes, outerLoopVisits)

	buf := &bytes.Buffer{}
	for y := 0; y < maxY; y++ {
		for x := 0; x < maxX; x++ {
			if x == start.X && y == start.Y {
				fmt.Print("S")
				fmt.Fprint(buf, "S")
				continue
			}
			if _, ok := pipeDistances[Pos{x, y}]; ok {
				fmt.Print(pipes[Pos{x, y}])
				fmt.Fprint(buf, pipes[Pos{x, y}])
				continue
			}
			if _, ok := outerLoopVisits[Pos{x, y}]; ok {
				fmt.Print(" ")
				fmt.Fprint(buf, " ")
				continue
			}
			fmt.Fprint(buf, "?")
			fmt.Print("?")
			resultPart2++
		}
		fmt.Println()
		fmt.Fprintln(buf)
	}

	os.WriteFile("output.txt", buf.Bytes(), 0o644)

	fmt.Println("part 2:", resultPart2)
}

func printMap(maxX, maxY int, start Pos, pipeDistances map[Pos]int, pipes map[Pos]Pipe, outerLoopVisits map[Pos]struct{}) {
	fmt.Println()
	for y := 0; y < maxY; y++ {
		for x := 0; x < maxX; x++ {
			if x == start.X && y == start.Y {
				fmt.Print("S")
				continue
			}
			if _, ok := pipeDistances[Pos{x, y}]; ok {
				if _, ok := outerLoopVisits[Pos{x, y}]; ok {
					fmt.Print("+")
					continue
				}
				fmt.Print(pipes[Pos{x, y}])
				continue
			}
			if _, ok := outerLoopVisits[Pos{x, y}]; ok {
				fmt.Print("■")
				continue
			}

			fmt.Print("?")
		}
		fmt.Println()
	}
	fmt.Println()
}
