use std::fs;
use std::io::BufRead;
use std::io::BufReader;
use std::collections::HashMap;

fn main() {
    let mut left: Vec<i32> = Vec::new();
    let mut right: Vec<i32> = Vec::new();
    let mut freq: HashMap<i32, i32> = HashMap::new();

    let reader = BufReader::new(fs::File::open("2024/1/input.txt").expect("Cannot open file"));

    for line in reader.lines() {
        let line = line.unwrap();
        let words: Vec<&str> = line.split_whitespace().collect();

        let rv = words[1].parse().expect("found non-number: {words}");
        left.push(words[0].parse().expect("found non-number: {words}"));
        right.push(rv);
        *freq.entry(rv).or_insert(0) += 1
    }
    left.sort();
    right.sort();

    // println!("{:?}", left);
    // println!("{:?}", right);

    let mut part1 = 0;
    for idx in (0..left.len()) {
        let result = left[idx] - right[idx];
        part1 += result.abs()
    }
    println!("part 1: {part1}");

    let mut part2 = 0;
    for l in left {
        part2 += l * *freq.entry(l).or_insert(0)
    }
    println!("part 2: {part2}")
}