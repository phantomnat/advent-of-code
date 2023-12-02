package utils

import "fmt"

func Must(err error, msg ...string) {
	if err != nil {
		if len(msg) > 0 {
			panic(fmt.Sprintf("%s: %+v", msg[0], err))
		}
		panic(fmt.Sprintf("error: %+v", err))
	}
}