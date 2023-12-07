package main

import (
	"aoc/utils"
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

type CardSetStrength int64

const (
	HighCard CardSetStrength = 1 << iota
	OnePair
	TwoPairs
	ThreeOfAKind
	FullHouse
	FourOfAKind
	FiveOfAKind
)

var (
	Part1CardStrengths = map[rune]int64{
		'2': 1 << 1,
		'3': 1 << 2,
		'4': 1 << 3,
		'5': 1 << 4,
		'6': 1 << 5,
		'7': 1 << 6,
		'8': 1 << 7,
		'9': 1 << 8,
		'T': 1 << 9,
		'J': 1 << 10,
		'Q': 1 << 11,
		'K': 1 << 12,
		'A': 1 << 13,
	}
	Part2CardStrengths = map[rune]int64{
		'J': 1 << 1,
		'2': 1 << 2,
		'3': 1 << 3,
		'4': 1 << 4,
		'5': 1 << 5,
		'6': 1 << 6,
		'7': 1 << 7,
		'8': 1 << 8,
		'9': 1 << 9,
		'T': 1 << 10,
		'Q': 1 << 11,
		'K': 1 << 12,
		'A': 1 << 13,
	}
)

type PlayerHand struct {
	Card        string
	CardCounts  map[rune]int64
	SetStrength CardSetStrength
	Bid         int64
}

func (p PlayerHand) String() string {
	return fmt.Sprintf("{%s, %d, bid: %d}", p.Card, p.SetStrength, p.Bid)
}

func isLess(cardI, cardJ string, cardStrengths map[rune]int64) bool {
	for k := 0; k < len(cardI); k++ {
		ic := rune(cardI[k])
		jc := rune(cardJ[k])
		is := cardStrengths[ic]
		js := cardStrengths[jc]
		if is < js {
			return true
		} else if is > js {
			return false
		}
	}
	return cardI < cardJ
}

func GetCardSetStrength(counts map[rune]int64) CardSetStrength {
	pairCount := 0
	for _, v := range counts {
		switch v {
		case 5:
			return FiveOfAKind
		case 4:
			return FourOfAKind
		case 3:
			if len(counts) == 2 {
				return FullHouse
			}
			return ThreeOfAKind
		case 2:
			pairCount++
		}

	}
	// one pair or two pairs
	if pairCount == 2 {
		return TwoPairs
	} else if pairCount == 1 {
		return OnePair
	}
	return HighCard
}

func GetCardSetStrengthForPart2(counts map[rune]int64) CardSetStrength {
	jokerCounts := counts['J']
	if jokerCounts == 5 {
		return FiveOfAKind
	}

	pairCount := int64(0)

	type pair struct {
		c rune
		v int64
	}
	var sortedCounts []pair
	for c, v := range counts {
		if c == 'J' {
			continue
		}
		sortedCounts = append(sortedCounts, pair{c, v})
	}
	sort.Slice(sortedCounts, func(i, j int) bool {
		return sortedCounts[i].v >= sortedCounts[j].v
	})

	for _, p := range sortedCounts {
		v := p.v

		switch v + jokerCounts {
		case 5:
			// ooooo
			// oooo + j
			// ooo + jj
			// oo + jjj
			// o + jjjj
			return FiveOfAKind
		case 4:
			// oooo   , a
			// ooo + j, a
			// oo + jj, a
			// o + jjj, a
			return FourOfAKind
		case 3:

			// ooo   , aa, len() = 2
			// oo + j, aa, len() = 3
			if len(counts) == 2 || (jokerCounts > 0 && len(counts) == 3) {
				return FullHouse
			}

			// oo + j, a b, len() = 4
			// o + jj, a b, len() = 5
			return ThreeOfAKind
		}
		if v == 2 {
			pairCount++
		}
	}

	if jokerCounts == 1 && pairCount == 0 {
		return OnePair
	}

	if pairCount == 2 {
		return TwoPairs
	} else if pairCount == 1 {
		return OnePair
	}
	return HighCard
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
	inputCount := 0
	var players []*PlayerHand
	for scanner.Scan() {
		inputCount++
		line := scanner.Text()
		// fmt.Println(line)

		fields := strings.Fields(line)
		utils.MustTrue(len(fields) == 2, "expect 2 fields from '%s'", line)
		cards := fields[0]
		bid, err := strconv.ParseInt(fields[1], 10, 64)
		utils.Must(err)

		player := PlayerHand{
			Card: cards,
			Bid:  bid,
		}

		cardCounts := make(map[rune]int64)
		for _, c := range cards {
			cardCounts[c]++
			// player.CardStrength += CardStrengths[c]
			// player.CardStrengths = append(player.CardStrengths, CardStrengths[c])
		}
		player.CardCounts = cardCounts
		player.SetStrength = GetCardSetStrength(cardCounts)

		// fmt.Println(cards)
		// fmt.Println(bid)
		players = append(players, &player)
	}

	// fmt.Println(Part1CardStrengths)
	sort.Slice(players, func(i, j int) bool {
		if players[i].SetStrength < players[j].SetStrength {
			return true
		} else if players[i].SetStrength > players[j].SetStrength {
			return false
		}
		return isLess(players[i].Card, players[j].Card, Part1CardStrengths)
	})
	// fmt.Println("players", players)
	for i := int64(0); i < int64(len(players)); i++ {
		resultPart1 += ((i + 1) * players[i].Bid)
	}

	fmt.Println("part 1:", resultPart1)

	// assign new set strength
	for i := 0; i < len(players); i++ {
		players[i].SetStrength = GetCardSetStrengthForPart2(players[i].CardCounts)
		// for _, c := range players[i].Card {
		// 	players[i].CardStrength += string(Part2CardStrengths[c])
		// }
	}

	sort.Slice(players, func(i, j int) bool {
		if players[i].SetStrength < players[j].SetStrength {
			return true
		} else if players[i].SetStrength > players[j].SetStrength {
			return false
		}
		return isLess(players[i].Card, players[j].Card, Part2CardStrengths)
		// return players[i].CardStrength < players[j].CardStrength
	})

	// fmt.Println("players", players)

	for i := int64(0); i < int64(len(players)); i++ {
		resultPart2 += ((i + 1) * players[i].Bid)
	}
	fmt.Println("part 2:", resultPart2)
}
