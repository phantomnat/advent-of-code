package util

import (
	"strconv"
)

func ParseInt64(input string) int64 {
	out, err := strconv.ParseInt(input, 10, 64)
	Must(err, input+"is not a valid number")
	return out
}

func ParseInt(input string) int {
	out, err := strconv.Atoi(input)
	Must(err, input+"is not a valid number")
	return out
}

func Sum(input ...int64) int64 {
	var out int64
	for _, i := range input {
		out += i
	}
	return out
}

func Last[T any](input []T) T {
	return input[len(input)-1]
}

func First[T any](input []T) T {
	return input[0]
}

func IsTheSame(input []int64, target int64) bool {
	for _, i := range input {
		if i != target {
			return false
		}
	}
	return true
}

type Number interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
		~float32 | ~float64
}

func Abs[T Number](input T) T {
	if input < 0 {
		return -input
	}
	return input
}
