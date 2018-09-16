from random import randint

class Hero:
    def __init__(self, name, health=100):
        self.name = name
        self.abilities = []
        self.armors = []
        self.start_health = health
        self.health = health
        self.deaths = 0
        self.kills = 0

    def add_ability(self, ability):
        self.abilities.append(ability)

    def attack(self):
        if len(self.abilities) == 0:
            return 0
        return sum([ability.attack() for ability in self.abilities])

    def __repr__(self):
        string = 'Hero Name: ' + self.name
        string += '\nAbilities:\n\t'
        string += '\n\t'.join(['{}: {}'.format(a.name, a.attackStrength) for a in self.abilities])
        return string

    def defend(self):
        if self.health == 0:
            return self.health
        return sum([a.defend() for a in self.armors])

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.deaths += 1
            return 'Died'

    def add_kill(self, numberOfKills):
        self.kills += numberOfKills

    def add_armor(self, armor):
        self.armors.append(armor)

class Ability:
    def __init__(self, name, attackStrength):
        self.name = name
        self.attackStrength = attackStrength

    def attack(self):
        return randint(self.attackStrength // 2, self.attackStrength)

    def update_attack_strength(self, newStrength):
        self.attack_strength = newStrength
    
class Weapon(Ability):
    def attack(self):
        return randint(0, self.attackStrength)

class Team:
    def __init__(self, team_name):
        self.name = team_name
        self.heroes = []

    def add_hero(self, hero):
        self.heroes.append(hero)

    def remove_hero(self, name):
        index = self.find_hero(name)
        if index == -1:
            return 0
        self.heroes.pop(index)

    def find_hero(self, name):
        indexOfHero = -1
        for index, hero in enumerate(self.heroes):
            if hero.name == name:
                indexOfHero = index
        return indexOfHero
    
    def attack(self, other_team):
        attackStrength = sum([hero.attack() for hero in self.heroes])
        enemiesKilled = other_team.defend(attackStrength)
        self.update_kills(enemiesKilled)

    def defend(self, damage_amt):
        defenseStrength = sum([hero.defend() for hero in self.heroes])
        exessDamage = damage_amt - defenseStrength
        if exessDamage > 0:
            return self.deal_damage(exessDamage)
        return 0

    def deal_damage(self, damage):
        damage = damage / len(self.heroes)
        deadHeros = 0
        for hero in self.heroes:
            if hero.take_damage(damage) == 'Died':
                deadHeros += 1
        return deadHeros

    def revive_heroes(self, health=100):
        for hero in self.heroes:
            hero.health = hero.start_health

    def stats(self):
        print(self.name, 'Stats:')
        for hero in self.heroes:
            ratio = hero.kills/hero.deaths if hero.deaths > 0 else hero.kills
            print(hero.name, 'kill/death ratio:', ratio)

    def update_kills(self, kills):
        for hero in self.heroes:
            hero.add_kill(kills)

    def viewAllHeroes(self):
        for hero in self.heroes:
            print(hero)

class Armor:
    def __init__(self, name, defenseStrength):
        self.name = name
        self.defenseStrength = defenseStrength

    def defend(self):
        return randint(0, self.defenseStrength)