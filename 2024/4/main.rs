use std::fs;
use std::io::BufRead;
use std::io::BufReader;

fn main() {
    let filename = file!().replace("main.rs", "input.txt");

    let reader: BufReader<fs::File> =
        BufReader::new(fs::File::open(filename).expect("Cannot open file"));
    let mut part1: i64 = 0;
    let mut part2: i64 = 0;
    let mut cares: Vec<Vec<char>> = Vec::new();
    for line in reader.lines().filter_map(Result::ok) {
        // println!("{line}");
        cares.push(line.chars().collect());
    }
    let w = cares[0].len();
    let h = cares.len();

    // println!("w: {w}, h: {h}");
    // for line in cares {
    //     println!("{:?}", line);
    // }
    for y in 0..h {
        for x in 0..w {
            part1 += look_for_xmas(&cares, w, h, x, y);
            part2 += look_for_x_mas(&cares, w, h, x, y);
        }
    }

    println!("part 1: {part1}");
    println!("part 2: {part2}");
}

fn look_for_x_mas(cares: &Vec<Vec<char>>, w: usize, h: usize, x: usize, y: usize) -> i64 {
    if cares[y][x] != 'A' {
        return 0;
    }
    let mut count: usize = 0;

    let is_within_bound = (x as i32) - 1 >= 0 && x + 1 < w && (y as i32) - 1 >= 0 && y + 1 < h;
    if !is_within_bound {
        return 0;
    }

    let first = (cares[y-1][x-1] == 'M' && cares[y+1][x+1] == 'S') || (cares[y-1][x-1] == 'S' && cares[y+1][x+1] == 'M');
    let second = (cares[y-1][x+1] == 'M' && cares[y+1][x-1] == 'S') || (cares[y-1][x+1] == 'S' && cares[y+1][x-1] == 'M');
    if first && second {
        count += 1;
    }
    count as i64
}

fn look_for_xmas(cares: &Vec<Vec<char>>, w: usize, h: usize, x: usize, y: usize) -> i64 {
    if cares[y][x] != 'X' {
        return 0;
    }
    let xmas: Vec<_> = "XMAS".chars().collect();
    let mut count: usize = 0;
    let directions: Vec<(i32, i32)> = vec![
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
    ];

    for (dy, dx) in directions {
        let mut found = true;
        for mul in 0..4 {
            let new_y = (y as i32) + (dy * mul);
            let new_x = (x as i32) + (dx * mul);
            let is_within_bound = new_x >= 0 && new_x < w as i32 && new_y >= 0 && new_y < h as i32;
            if !is_within_bound || cares[new_y as usize][new_x as usize] != xmas[mul as usize] {
                found = false;
                break;
            }
        }
        if found {
            count += 1;
        }
    }
    count as i64
}
