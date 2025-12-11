use std::cmp;
use std::fs;
use std::str::FromStr;
use std::sync::{Arc, Mutex};
use std::time::Instant;

use rayon::prelude::*;

#[derive(Debug)]
struct Machine {
    diagram: Vec<bool>,
    buttons: Vec<Vec<bool>>,
    joltages: Vec<u32>,
}

fn strip_around(s: &str, prefix: char, suffix: char) -> Option<&str> {
    let s = s.strip_prefix(prefix)?;
    let s = s.strip_suffix(suffix)?;
    Some(s)
}

fn parse_comma_separated_ints(s: &str) -> Option<Vec<u32>> {
    s.split(',')
        .map(str::parse::<u32>)
        .map(std::result::Result::ok)
        .collect()
}

impl FromStr for Machine {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut it = s.split(' ');

        let diagram = it.next().ok_or_else(|| s.to_string())?;
        let diagram = strip_around(diagram, '[', ']').ok_or_else(|| s.to_string())?;
        let diagram = diagram.chars().map(|x| x == '#').collect();

        let joltages = it.next_back().ok_or_else(|| s.to_string())?;
        let joltages = strip_around(joltages, '{', '}').ok_or_else(|| s.to_string())?;
        let joltages = parse_comma_separated_ints(joltages).ok_or_else(|| s.to_string())?;

        let buttons = it
            .map(|x| {
                let button = strip_around(x, '(', ')')?;
                let button = parse_comma_separated_ints(button)?;

                Some(
                    (0..joltages.len().try_into().ok()?)
                        .map(|i| button.contains(&i))
                        .collect(),
                )
            })
            .collect::<Option<Vec<Vec<bool>>>>()
            .ok_or_else(|| s.to_string())?;

        Ok(Self {
            diagram,
            buttons,
            joltages,
        })
    }
}

fn light_configuration_cost(diagram: &[bool], buttons: &[Vec<bool>]) -> Option<u32> {
    if diagram.iter().all(|x| !x) {
        return Some(0);
    }

    if buttons.is_empty() {
        return None;
    }

    let best_without = light_configuration_cost(diagram, &buttons[1..]);

    let modified_diagram = &diagram
        .iter()
        .zip(&buttons[0])
        .map(|(state, should_toggle)| state ^ should_toggle)
        .collect::<Vec<bool>>();
    let best_with = light_configuration_cost(modified_diagram, &buttons[1..]).map(|x| x + 1);

    match (best_without, best_with) {
        (Some(a), Some(b)) => Some(cmp::min(a, b)),
        (Some(a), _) => Some(a),
        (_, Some(b)) => Some(b),
        _ => None,
    }
}

fn joltage_configuration_cost(joltages: &[u32], buttons: &[Vec<bool>]) -> Option<u32> {
    let avoided: Vec<bool> = joltages.iter().map(|required| *required == 0).collect();
    if avoided.iter().all(|x| *x) {
        return Some(0);
    }

    let allowed: Vec<&Vec<bool>> = buttons
        .iter()
        .filter(|button| {
            button
                .iter()
                .zip(&avoided)
                .all(|(x, should_avoid)| !*should_avoid || !*x)
        })
        .collect();

    if allowed.is_empty() {
        return None;
    }

    // get joltages with least conflicts first
    let (current_joltage, relevant_buttons) = (0..joltages.len())
        .filter(|i| joltages[*i] > 0)
        .map(|i| {
            (
                i,
                allowed
                    .iter()
                    .filter(|button| button[i])
                    .copied()
                    .collect::<Vec<&Vec<bool>>>(),
            )
        })
        .min_by_key(|(_, buttons)| buttons.len())?;

    let mut left = vec![(0, 0, joltages.to_vec())];
    let mut best = None;
    while let Some((cost, button_index, amounts)) = left.pop() {
        if cost > best.unwrap_or(u32::MAX) {
            continue;
        }

        if amounts[current_joltage] == 0 {
            if let Some(rest) = joltage_configuration_cost(&amounts, buttons) {
                let curr = cost + rest;
                best = Some(best.map_or(curr, |b| cmp::min(b, curr)));
            }

            continue;
        }

        if button_index >= relevant_buttons.len() {
            continue;
        }

        let button = relevant_buttons[button_index];
        let mut new_joltages = amounts;
        let mut new_cost = cost;
        loop {
            left.push((new_cost, button_index + 1, new_joltages.clone()));

            new_joltages = match new_joltages
                .into_iter()
                .zip(button)
                .map(|(joltage, added)| joltage.checked_sub(u32::from(*added)))
                .collect::<Option<Vec<u32>>>()
            {
                Some(joltages) => joltages,
                None => break,
            };
            new_cost += 1;
        }
    }

    best
}

fn main() {
    let machines = match fs::read_to_string("../input")
        .expect("couldn't read input")
        .trim()
        .lines()
        .map(str::parse::<Machine>)
        .collect::<Result<Vec<Machine>, String>>()
    {
        Ok(machines) => machines,
        Err(s) => panic!("couldn't parse '{s}'"),
    };

    let p1 = machines
        .iter()
        .map(|m| light_configuration_cost(&m.diagram, &m.buttons))
        .sum::<Option<u32>>()
        .expect("input contained unsatisfiable diagram");

    let left = Arc::new(Mutex::new(machines.len()));
    let p2 = machines
        .par_iter()
        .map(|m| {
            let now = Instant::now();
            let result = joltage_configuration_cost(&m.joltages, &m.buttons);
            let mut left = left.lock().unwrap();
            *left -= 1;
            println!(
                "{result:?} - found in {:?} ({left} left): {m:?}",
                now.elapsed()
            );
            println!();

            result
        })
        .sum::<Option<u32>>()
        .expect("input contained unsatisfiable joltages");

    println!("{p1} {p2}");
}
