use std::fs;
use std::io::BufRead;
use std::io::BufReader;
use std::ops::Mul;
use std::str::FromStr;

fn main() {
    let filename = file!().replace("main.rs", "input.txt");

    let reader: BufReader<fs::File> =
        BufReader::new(fs::File::open(filename).expect("Cannot open file"));
    let mut part1: i64 = 0;
    let mut part2: i64 = 0;
    let mut adding = true;

    for line in reader.lines().filter_map(Result::ok) {
        let mut idx = 0;
        while idx + 9 < line.len() {
            let four = &line[idx..idx+4];
            let seven = &line[idx..idx+7];
            if seven == "don't()" {
                adding = false;
                idx += seven.len();
            } else if four == "do()" {
                adding = true;
                idx += four.len();
            } else if four == "mul(" {
                // let num = get_num(&line[idx+4..]);
                match get_num2::<i64>(&line[idx+4..]) {
                    Some(v) => {
                        part1 += v;
                        if adding { part2 += v }
                    },
                    _ => {}
                }
                idx += four.len()
            } else {
                idx += 1;
            }
        }
    }

    println!("part 1: {part1}");
    println!("part 2: {part2}");
}

fn get_num2<T>(item: &str) -> Option<T::Output> where T: FromStr + Mul<Output = T> {
    let (nums, _) = item.split_once(')')?;
    let (left, right) = nums.split_once(',')?;

    let left_num = left.parse::<T>().ok()?;
    let right_num = right.parse::<T>().ok()?;

    Some(left_num * right_num)
}

fn get_num(item: &str) -> Option<i64> {
    let comma_idx = match item.find(',') {
        Some(v) => v,
        _ => return None,
    };
    let close_bracket = match item.find(')') {
        Some(v) => v,
        _ => return None,
    };
    let is_valid_pos = comma_idx < close_bracket;
    if !is_valid_pos {
        return None;
    }
    let nums = &item[..close_bracket].split(',').collect::<Vec<_>>();
    if nums.len() != 2 {
        return None;
    }
    let is_left_num = nums[0].chars().all(|x| char::is_ascii_digit(&x));
    let is_right_num = nums[1].chars().all(|x| char::is_ascii_digit(&x));
    let left = match nums[0].parse::<i64>() {
        Ok(v) => v,
        _ => return None,
    };
    let right = match nums[1].parse::<i64>() {
        Ok(v) => v,
        _ => return None,
    };
    let is_valid_number = is_left_num && is_right_num;
    if !is_valid_number {
        return None;
    }
    Some(left * right)
}
