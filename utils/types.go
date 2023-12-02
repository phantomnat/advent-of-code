package utils

func Pointer[A any](a A) *A {
	return &a
}