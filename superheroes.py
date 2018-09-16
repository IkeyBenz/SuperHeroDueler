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
            hero.take_damage(damage)
            if hero.health <= 0:
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

class Arena:
    def __init__(self):
        self.team_one = self.build_team_one()
        self.team_two = self.build_team_two()
    
    def build_team(self):
        teamName = input('Enter the name for this team: ')
        teamHeros = []
        keepAddingHeroes = True
        while keepAddingHeroes:
            print('Adding a hero to your team...')
            newHero = Hero(input('What is the name of this hero? '))
            newHero.abilities.append(self.getAdditionsForHero('ability', newHero.name))
            newHero.abilities.append(self.getAdditionsForHero('weapon', newHero.name))
            newHero.armors.append(self.getAdditionsForHero('armor', newHero.name))
            teamHeros.append(newHero)
            keepAddingHeroes = self.yesOrNo('Do you want to add another hero to ' + teamName + '? ')
        newTeam = Team(teamName)
        newTeam.heroes = teamHeros
        return newTeam

    def getAdditionsForHero(self, additionType, heroName):
        additions = []
        if self.yesOrNo('Do you want to add ' + additionType + ' to ' + heroName + '? (y/n) '):
            keepAsking = True
            addition = Ability if additionType == 'ability' else Weapon if additionType == 'weapon' else Armor
            while keepAsking:
                name = input('What is this ' + additionType + ' called? ')
                attackStrength = int(input('What is ' + name + "'s attack strength? "))
                additions.append(addition(name, attackStrength))
                keepAsking = self.yesOrNo('Do you want to add another ' + additionType + ' to this team? (y/n) ')
        return additions

    def yesOrNo(self, prompt):
        res = input(prompt)
        if res in ['Y', 'y', 'N', 'n']:
            if res in 'Yy':
                return True
            return False
        print('Response not recognized.')
        return self.yesOrNo(prompt)

    def build_team_one(self):
        print('Building Team One...')
        return self.build_team()

    def build_team_two(self):
        print('Building Team Two...')
        return self.build_team()

    def team_battle(self):
        """
        This method should continue to battle teams until 
        one or both teams are dead.
        """

    def show_stats(self):
        """
        This method should print out the battle statistics 
        including each heroes kill/death ratio.
        """

arena = Arena()