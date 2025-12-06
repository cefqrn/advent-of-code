use std::cmp::max;
use std::fs;

const HI: usize = 12;

fn get_outputs(bank: impl Iterator<Item = u64>) -> Vec<u64> {
    bank.fold(vec![], |best: Vec<u64>, joltage: u64| {
        if best.is_empty() {
            return vec![joltage];
        }

        let mut out = Vec::with_capacity(best.len() + 1);
        let curr = best[0];
        out.push(max(curr, joltage));
        let curr = best[1..]
            .iter()
            .take(HI-1)
            .fold(curr, |curr, best_of_next| {
                out.push(max(*best_of_next, curr * 10 + joltage));
                *best_of_next
            });
        out.push(curr * 10 + joltage);

        out
    })
}

fn main() {
    let (p1, p2) = fs::read_to_string("../input")
        .expect("couldn't read input")
        .trim()
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| c.to_digit(10).expect("invalid input").into())
        })
        .map(get_outputs)
        .fold((0, 0), |(p1, p2), outputs| {
            (p1 + outputs[2 - 1], p2 + outputs[12 - 1])
        });

    println!("{p1} {p2}");
}
