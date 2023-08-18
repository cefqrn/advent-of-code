from __future__ import annotations

from sys import stdin, argv
from os import isatty

if len(argv) == 2:
    with open(argv[1]) as f:
        s = f.read()
elif not isatty(0):  # check if stdin is a file
    s = stdin.read()
else:
    print("input not given")
    exit(1)

s = s.strip()  # s is the input as a string

from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Effect:
    name: str
    duration: int
    damage: int = 0
    heal: int = 0
    armor: int = 0
    mana: int = 0

    def __eq__(self, other: Effect):
        return self.name == other.name

    __str__ = __repr__ = lambda self: f"{self.name}({self.duration})"

@dataclass(frozen=True)
class Spell:
    name: str
    cost: int
    base_duration: int
    damage: int = 0
    heal: int = 0
    armor: int = 0
    mana: int = 0

    @property
    def effect(self):
        return Effect(self.name, self.base_duration, self.damage, self.heal, self.armor, self.mana)
    
    __str__ = __repr__ = lambda self: f"{self.name}"

spells = [
    Spell("Magic Missile", 53,  1, damage=4),
    Spell("Drain",         73,  1, damage=2,  heal=2),
    Spell("Shield",        113, 6, armor=7),
    Spell("Poison",        173, 6, damage=3),
    Spell("Recharge",      229, 5, mana=101)
]

base_player_hp = 50
base_player_mana = 500

base_boss_hp, boss_damage = map(int, map(lambda x: x.split(': ')[1], s.splitlines()))

@dataclass
class Game:
    player_hp: int
    boss_hp: int
    mana: int
    effects: list[Effect]
    armor: int = 0
    mana_spent: int = 0

    def apply_effects(self):
        new_effects = []

        self.armor = 0
        for effect in self.effects:
            effect.duration -= 1
            self.armor += effect.armor
            self.mana += effect.mana
            self.boss_hp -= effect.damage
            self.player_hp += effect.heal

            if effect.duration > 0:
                new_effects.append(effect)
        
        self.effects = new_effects

current_min = 99999999999
def play(game: Game, hard=False):
    # player turn
    global current_min

    if hard:
        game.player_hp -= 1
        if game.player_hp <= 0:
            return -1

    game.apply_effects()
    if game.boss_hp <= 0:
        return game.mana_spent

    values = []
    for spell in spells:
        if spell.effect in game.effects or game.mana - spell.cost < 0 or game.mana_spent + spell.cost >= current_min:
            continue
        
        new_game = Game(game.player_hp, game.boss_hp, game.mana - spell.cost, [*deepcopy(game.effects), spell.effect], mana_spent=game.mana_spent + spell.cost)
        # boss turn
        new_game.apply_effects()
        if new_game.boss_hp <= 0:
            values.append(new_game.mana_spent)
            continue

        new_game.player_hp -= boss_damage - new_game.armor
        if new_game.player_hp <= 0:
            continue

        if (value:=play(new_game, hard)) != -1:
            values.append(value)

    if values:
        if (min_val:=min(values)) < current_min:
            current_min = min_val
        return min_val
    else:
        return -1

def p1():
    game = Game(base_player_hp, base_boss_hp, base_player_mana, [])
    print(f"p1: {play(game)}")

def p2():
    game = Game(base_player_hp, base_boss_hp, base_player_mana, [])
    print(f"p2: {play(game, hard=True)}")

p1()
current_min = 99999999999
p2()