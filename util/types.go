package util

func Pointer[A any](a A) *A {
	return &a
}

type Pos struct {
	X int
	Y int
}

func (p Pos) Add(other Pos) Pos {
	return Pos{X: p.X + other.X, Y: p.Y + other.Y}
}

func (p Pos) AddX(x int) Pos {
	return Pos{X: p.X + x, Y: p.Y}
}

func (p Pos) AddY(y int) Pos {
	return Pos{X: p.X, Y: p.Y + y}
}

func (p Pos) Expand4Directions() []Pos {
	return []Pos{p.AddX(1), p.AddX(-1), p.AddY(1), p.AddY(-1)}
}
