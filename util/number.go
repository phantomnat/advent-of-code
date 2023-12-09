package util

import "strconv"

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
