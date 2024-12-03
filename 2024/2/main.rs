use core::num;
use std::collections::HashMap;
use std::fs;
use std::io::BufRead;
use std::io::BufReader;

fn main() {
    let filename = file!().replace("main.rs", "input.txt");
    print!("{filename}");

    let reader = BufReader::new(fs::File::open(filename).expect("Cannot open file"));
    let mut part1 = 0;
    let mut part2 = 0;

    for line in reader.lines() {
        let line = line.unwrap();
        let nums: Vec<i32> = line
            .split_whitespace()
            .map(|x| x.parse::<i32>().unwrap())
            .collect();

        if check_nums(&nums) {
            part1 += 1
        } else {
            let n: usize = (&nums).len();
            for ignore in 0..n {
                let mut new_nums: Vec<i32> = Vec::new();
                for (idx, v) in nums.iter().enumerate() {
                    if idx == ignore {
                        continue;
                    }
                    new_nums.push(*v);
                }
                if check_nums(&new_nums) {
                    part2 += 1;
                    break
                }
            }
        }
    }
    part2 += part1;
    println!("part 1: {part1}");
    println!("part 2: {part2}");
}

fn check_nums(nums: &Vec<i32>) -> bool {
    let mut diff: Vec<i32> = Vec::new();
    for idx in 1..nums.len() {
        diff.push(nums[idx] - nums[idx - 1]);
    }

    let neg_count = diff.iter().filter(|&&x| x < 0).count();
    let pos_count = diff.iter().filter(|&&x| x > 0).count();
    let within_limit_count = diff
        .iter()
        .filter(|&&x| {
            let v = x.abs();
            v >= 1 && v <= 3
        })
        .count();

    let is_neg = neg_count == diff.len() && within_limit_count == diff.len();
    let is_pos = pos_count == diff.len() && within_limit_count == diff.len();

    is_neg || is_pos
}
