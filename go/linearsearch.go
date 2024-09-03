package main

import (
	"fmt"
	"math"
	"slices"
)

func linearSearch(arr []int, st int) bool {
	for i := 0; i < len(arr); i++ {
		fmt.Println(arr[i], "==>", i)
		if arr[i] == st {
			return true
		}
	}
	return false
}

func binarySearch(arr []int, st int) bool {
	slices.Sort(arr)
	lo := 0
	hi := len(arr)

	for lo < hi {
		m := (lo + (hi-lo)/2)
		fmt.Println("array ==> ", arr[lo:hi])
		fmt.Println("[mid] ==> ", arr[m])
		fmt.Println("mi ind ==>", m)
		fmt.Println("lo ind ==>", lo)
		fmt.Println("hi ind ==>", hi)
		if arr[m] == st {
			return true
		} else if st > arr[m] {
			lo = m + 1
		} else {
			hi = m
		}

	}

	return false
}

func twoCrystalBalls(arr []bool) int {
	// jumpAmt := int(math.Sqrt(math.Ceil(float64(len(arr)))))
	n := len(arr)
	jumpAmt := int(math.Sqrt(float64(n)))
	fmt.Println(jumpAmt)

	i := jumpAmt
	for ; i < len(arr); i += jumpAmt {
		fmt.Println("xb == >", arr[i])
		if arr[i] {
			break
		}
	}
	i -= jumpAmt
	fmt.Println("check linear ", i)
	for j := 0; j < jumpAmt && i < len(arr); j++ {
		if arr[i] {

			fmt.Println("xl == >", arr[i])
			return i
		}
		i++
	}
	return -1
}

// twoCrystalBalls function to find the critical floor
func twoCrystalBallsgpt(breaker []bool) int {
	n := len(breaker)
	jumpAmt := int(math.Ceil(math.Sqrt(float64(n))))

	// First crystal ball
	i := 0
	for i < n && !breaker[i] {
		i += jumpAmt
	}

	// Step back to the last safe point
	i -= jumpAmt

	// Second crystal ball
	for j := 0; j < jumpAmt && i < n; j++ {
		if breaker[i] {
			return i
		}
		i++
	}

	return -1 // Return -1 if no breaking point is found
}

func main() {
	// fmt.Print("this is cool")
	// arr := []int{3, 4, 5, 6, 1, 2, 90, 91}
	// var output bool
	// fmt.Println(len(arr))
	// output = linearSearch(arr, 90)
	// fmt.Print(output)
	// output = binarySearch(arr, 90)
	// fmt.Print(output)

	breaker := []bool{false, false, false, false, false, false, true, true}
	solution := twoCrystalBallsgpt(breaker)
	fmt.Println(solution)

}
