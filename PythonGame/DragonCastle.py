import random
import os


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage
    
    def attack(self):
        return random.randint(self.damage//2, self.damage)
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.enemy = []
        self.exits = {}
    
    def set_exit(self, direction, room):
        self.exits[direction] = room
    
    def add_item(self, item):
        self.items.append(item)
    
    def set_enemy(self, enemy):
        self.enemy.append(enemy)

class Player:
    ORIGINAL_HEALTH = 100
    def __init__(self, name):
        self.name = name
        self.health = Player.ORIGINAL_HEALTH
        self.attack_power = random.randint(5, 15)
        self.inventory = []
        self.potions = []
        self.current_room = None
        self.path = []
    
    def move(self, direction):
        if direction == 'backward':
            if len(self.path):
                self.current_room = self.path.pop()
                self.set_room(direction)
            else:
                print("No more backward moves left!!!")
        elif direction in self.current_room.exits:
            self.path.append(self.current_room)
            self.current_room = self.current_room.exits[direction]
            self.set_room(direction)
        else:
            print("You can't go that way.")
    
    def set_room(self,direction):
        refresh(self)
        self.set_enemy(self.current_room)
        print(self.current_room.description)
        print(f"You move {direction} and arrive at {self.current_room.name}.")
        
        while len(self.current_room.enemy):
            if(self.battle_mode()==-555555):
                return

    def set_enemy(self,room):
        enemy_names = ['Minion','Goblin','Bandit','Giant','Dragon']
        put_enemy = random.randint(0,1)
        enemy_number,enemy_hp,enemy_attack = 0,0,0
        enemy_name = ''
        if(put_enemy):
            enemy_number = random.randint(0,5)
            for i in range(enemy_number):
                enemy_name = enemy_names[random.randint(0,4)]
                for j in range(5):
                    if(enemy_name==enemy_names[j]):
                        enemy_hp = (j+1)*random.randint(10,20)
                        enemy_attack = (j+1)*random.randint(1,5)
                room.set_enemy(Enemy(enemy_name,enemy_hp,enemy_attack))

    def battle_mode(self):
        while self.health > 0:
            enemy = self.current_room.enemy[-1]
            print(f"\n\t{enemy.name} appeared!!!!!")
            action = input("\tConfront GoBack\n> ").strip().lower()
            if action == "goback":
                print("You retreat to the previous room.")
                return self.move('backward')
            elif action == "confront":
                while True:
                    print(f"\n         You : [HP : {self.health}]  [Attack : {self.attack_power}]     Enemy : [HP : {enemy.health}]  [Attack : {enemy.damage}]")
                    action = input("         Attack RunAway\n> ").strip().lower()
                    if action == "runaway":
                        print("You escaped the battle!")
                        return self.move('backward')
                    elif action == "attack":
                        enemy.take_damage(self.attack_power)
                        print(f"        Enemy -{self.attack_power}!!!")
                        enemy_damage = enemy.attack()
                        self.health -= enemy_damage
                        if self.health <= 0:
                            print("Game Over! You have been defeated.")
                            return -555555
                        if enemy.health <= 0:
                            print(f"        You defeated {enemy.name}!")
                            self.current_room.enemy.pop()
                            return
                        print(f"        You -{enemy_damage}!!!")
                    else:
                        print("Invalid action.")
            else:
                print("Invalid action.")
    
    def heal(self):
        if self.current_room.name == "First-Aid Room":
            if self.health < Player.ORIGINAL_HEALTH :
                self.health = Player.ORIGINAL_HEALTH
                print("Your wounds are healed now!!")
                print(f"New health: {self.health}!")
            else:
                print("You are fit already!!!")
        else:
            print("You need to get some medicine first!!! HINT: Medicines are available in First-Aid Room")

    def find(self):
        if self.current_room.items:
            found_item = random.choice(self.current_room.items)
            print(f"\tYou found a {found_item.name}!")
            while True:
                action = input("\tTake Discard\n\t> ").strip().lower()
                if action == "take":
                    self.take_item(found_item)
                    break
                elif action == "discard":
                    print(f"You discarded the {found_item.name}.")
                    break
                else:
                    print("Invalid action.")
        else:
            print("There is nothing to find.")
    
    def take_item(self, item):
        self.current_room.items.remove(item)
        print(f"You picked up {item.name}.")
        if "Sword" in item.name:
            attack_increase = random.randint(3, 7)
            self.attack_power += attack_increase
            print(f"Your attack power increased by {attack_increase}! New attack: {self.attack_power}")
        elif "Shield" in item.name:
            hp_increase = random.randint(10, 30)
            self.health += hp_increase
            print(f"Your health increased by {hp_increase}! New health: {self.health}")
        elif "Potion" in item.name:
            self.potions.append(item)
            return
        self.inventory.append(item)

    def show_inventory(self):
        if(len(self.inventory)+len(self.potions)==0):
            print("\t\tInventory is currently empty!!!")
            return
        print("\t\t=============== Inventory ===============\n\n")
        for item in self.inventory:
            print(f"\t\t- {item.name}: {item.description}")
        print("\n\t\tPotions:")
        for potion in self.potions:
            print(f"\t\t- {potion.name}: {potion.description}")
        print("\n\n\t\t=========================================")
        
    
    def show_potion(self):
        if(len(self.potions)==0):
            print("\t\tYou have currently no potions in your inventory!!!")
            return
        print("\t\t=============== Potions ===============\n\n")
        for potion in self.potions:
            print(f"\t\t- {potion.name}: {potion.description}")
        print("\n\n\t\t=======================================")
        
        potion_name = input("\n\t\tWhich potion do you want to use?\n\t\t> ").strip().lower()
        self.use_potion(potion_name)

    def use_potion(self, potion_name):
        potion = next((potion for potion in self.potions if potion.name.lower() == potion_name.lower()), None)
        if potion:
            if potion.name == "Health Potion":
                health_increase = random.randint(15, 30)
                self.health += health_increase
                print(f"\nYour health increased by {health_increase}! New health: {self.health}")
            elif potion.name == "Power Potion":
                attack_increase = random.randint(5, 10)
                self.attack_power += attack_increase
                print(f"\nYour attack power increased by {attack_increase}! New attack: {self.attack_power}")
            elif potion.name == "Mysterious Potion":
                effect = random.choice(["increase_attack", "increase_health", "poison"])
                if effect == "increase_attack":
                    attack_increase = random.randint(3, 7)
                    self.attack_power += attack_increase
                    print(f"\nYour attack power increased by {attack_increase}! New attack: {self.attack_power}")
                elif effect == "increase_health":
                    health_increase = random.randint(10, 20)
                    self.health += health_increase
                    print(f"\nYour health increased by {health_increase}! New health: {self.health}")
                elif effect == "poison":
                    poison_damage = random.randint(5, 10)
                    self.health -= poison_damage
                    print(f"\nYou've been poisoned! You lost {poison_damage} health. New health: {self.health}")
            self.potions.remove(potion)
        else:
            print("Potion not found.")


def refresh(player):
    os.system('cls')
    print("============================ Adventure Game ============================")
    world = world = f'''        
                        [ First-Aid Room {'∇ ' if player.current_room.name=='First-Aid Room' else ''}]
                                │
                                │
            [ Storage {'∇ ' if player.current_room.name=='Storage' else ''}] ─── [ Kitchen {'∇ ' if player.current_room.name=='Kitchen' else ''}] ─── [ Dungeon {'∇ ' if player.current_room.name=='Dungeon' else ''}]
                                │
                                │
                            [ Hall {'∇ ' if player.current_room.name=='Hall' else ''}]          
'''
    print('\n',world)
    print("\n\n")
    
def create_world():
    room1 = Room("Hall", "A grand entrance hall with a chandelier.")
    room2 = Room("Kitchen", "A kitchen with a strange smell.")
    room3 = Room("Dungeon", "A dark, damp dungeon with chains on the walls.")
    room4 = Room("First-Aid Room", "A small room with medical supplies to heal your wounds.")
    room5 = Room("Storage", "A cluttered storage room filled with old crates and cobwebs.")

    room1.set_exit("north", room2)
    room2.set_exit("south", room1)
    room2.set_exit("east", room3)
    room2.set_exit("north", room4)
    room2.set_exit("west", room5)
    room3.set_exit("west", room2)
    room4.set_exit("south", room2)
    room5.set_exit("east", room2)
    
    sword = Item("Sword", "A sharp blade, useful for battle.")
    shield = Item("Shield", "A sturdy shield that increases your health.")
    health_potion = Item("Health Potion", "Increases your HP.")
    power_potion = Item("Power Potion", "Increases your Attack Power.")
    mysterious_potion = Item("Mysterious Potion", "Could increase HP or attack or poison.")
    
    room2.add_item(sword)
    room3.add_item(shield)
    room2.add_item(health_potion)
    room3.add_item(power_potion)
    room1.add_item(mysterious_potion)
    room5.add_item(mysterious_potion)
    room5.add_item(power_potion)
    return room1

def main():
    player = Player("Hero")
    player.current_room = create_world()
    refresh(player)
    print("\t\tWelcome to the Adventure Game!")
    while player.health > 0:
        command = input("\nWhat do you want to do? (go [direction], find, potion, inventory, heal, exit)\n> ").strip().lower()
        refresh(player)
        if command.startswith("go "):
            direction = command.split(" ")[1]
            player.move(direction)
        elif command == "find":
            player.find()
        elif command == "potion":
            player.show_potion()
        elif command == "inventory":
            player.show_inventory()
        elif command == "heal":
            player.heal()
        elif command == "exit":
            os.system('cls')
            print("Thanks for playing!")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()