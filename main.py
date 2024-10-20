import random
import json
import pygame as pg

# Инициализация pg
pg.init()

# Размеры окна
SCREEN_SIZE = (900, 550)
ICON_SIZE = (80, 80)
PADDING = 5
BUTTON_SIZE = (200, 60)
DOG_SIZE = (310, 500)
MENU_NAV = (90, 130)
FOOD_SIZE = 200
TOY_SIZE = 100
FPS = 60

font = pg.font.Font(None, 40)
mini_font = pg.font.Font(None, 15)
maxi_font = pg.font.Font(None, 200)


def load_image(file, size):
    image = pg.transform.scale(pg.image.load(file).convert_alpha(), size)
    return image


def text_render(text, font=font, color='black'):
    return font.render(str(text), True, color)

class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        picture_name = random.choice(("red bone.png", 'blue bone.png', 'ball.png'))
        self.image = load_image(f'images/toys/{picture_name}', (TOY_SIZE, TOY_SIZE))
        self.rect = self.image.get_rect(center=(random.randint(int(SCREEN_SIZE[0]*0.2), int(SCREEN_SIZE[0]*0.8)), SCREEN_SIZE[1] * 0.15))

    def update(self):
        self.rect.y += 5
        if self.rect.top > SCREEN_SIZE[1] * 0.75:
            self.kill()

class Dog(pg.sprite.Sprite):
    def __init__(self,):
        pg.sprite.Sprite.__init__(self)

        self.image = load_image('images/dog.png', (DOG_SIZE[0] // 2, DOG_SIZE[1] // 2))
        self.rect = self.image.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] * 0.74))

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.x -= 5
        elif keys[pg.K_d]:
            self.rect.x += 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class MiniGame:
    def __init__(self, game):
        self.game = game

        self.background = load_image('images/game_background.png', SCREEN_SIZE)


    def new_game(self):
        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 20

    def update(self):
        self.dog.update()
        self.toys.update()
        if random.randint(0, 50) == 0:
            self.toys.add(Toy())
            hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.8))
            self.score += len(hits)
        if pg.time.get_ticks() - self.start_time > self.interval:
            self.game.happiness += int(self.score // 2)
            self.game.mode = "Main"
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(text_render(self.score), (MENU_NAV[0] + 20, 80))
        self.toys.draw(screen)
        self.dog.draw(screen)
class Food:
    def __init__(self, name, price, file, satiety, medicine_power=0):
        self.name = name
        self.satiety = satiety
        self.price = price
        self.medicine_power = medicine_power
        self.image = load_image(file, (FOOD_SIZE, FOOD_SIZE))

class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image('images/menu/menu_page.png', SCREEN_SIZE)

        self.bottom_label_off = load_image('images/menu/bottom_label_off.png', SCREEN_SIZE)
        self.bottom_label_on = load_image('images/menu/bottom_label_on.png', SCREEN_SIZE)
        self.top_label_off = load_image('images/menu/top_label_off.png', SCREEN_SIZE)
        self.top_label_on = load_image('images/menu/top_label_on.png', SCREEN_SIZE)

        self.items = [Food('Мясо', 30, 'images/food/meat.png', 10),
                      Food('Корм', 40, 'images/food/dog food.png', 15),
                      Food('Элитный корм', 100, 'images/food/dog food elite.png', 25, medicine_power=2),
                      Food('Лекарство', 200, 'images/food/medicine.png', 0, medicine_power=10)]

        self.curent_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

        self.next_button = Button('Вперед', SCREEN_SIZE[0] - MENU_NAV[0] - BUTTON_SIZE[0], SCREEN_SIZE[1] - MENU_NAV[1],
                                  button_size=tuple((x//1.2 for x in BUTTON_SIZE)),
                                  func=self.to_next)
        self.prev_button = Button('Назад', SCREEN_SIZE[0]*0.12, SCREEN_SIZE[1] - MENU_NAV[1],
                                  button_size=tuple((x // 1.2 for x in BUTTON_SIZE)),
                                  func=self.to_prev)
        self.buy_button = Button('Съесть', SCREEN_SIZE[0] * 0.41, SCREEN_SIZE[1]*0.65,
                                  button_size=tuple((x // 1.2 for x in BUTTON_SIZE)),
                                  func=self.buy)

        self.buttons = self.next_button, self.prev_button, self.buy_button

        self.update()



    def to_next(self):
        if self.curent_item != len(self.items) - 1:
            self.curent_item += 1
    def to_prev(self):
        if self.curent_item != 0:
            self.curent_item -= 1

    def buy(self):
        if self.game.money >= self.items[self.curent_item].price:
            self.game.money -= self.items[self.curent_item].price
            self.game.satiety += self.items[self.curent_item].satiety
            if self.game.satiety > 100:
                self.game.satiety = 100

            self.game.health += self.items[self.curent_item].medicine_power
            if self.game.health > 100:
                self.game.health = 100

    def update(self):
        self.price_text = text_render(self.items[self.curent_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_SIZE[0] // 2, 180)
        self.name_text = text_render(self.items[self.curent_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_SIZE[0] // 2, 120)


        for button in self.buttons:
            button.update()

    def draw(self, screen):

        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.items[self.curent_item].image, self.item_rect)

        for button in self.buttons:
            button.draw(screen)

        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)


class Item:
    def __init__(self, name, price, file, is_put_on, is_bought):
        self.name = name
        self.price = price
        self.is_put_on = is_put_on
        self.is_bought = is_bought
        self._file = file
        self.image = load_image(file, (DOG_SIZE[0] // 1.7, DOG_SIZE[1] // 1.7))
        self.full_image = load_image(file, DOG_SIZE)


class ClothesMenu:
    def __init__(self, game, data):
        self.game = game
        self.menu_page = load_image('images/menu/menu_page.png', SCREEN_SIZE)

        self.bottom_label_off = load_image('images/menu/bottom_label_off.png', SCREEN_SIZE)
        self.bottom_label_on = load_image('images/menu/bottom_label_on.png', SCREEN_SIZE)
        self.top_label_off = load_image('images/menu/top_label_off.png', SCREEN_SIZE)
        self.top_label_on = load_image('images/menu/top_label_on.png', SCREEN_SIZE)


        self.items = [Item(*item.values()) for item in data]

        self.curent_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

        self.next_button = Button('Вперед', SCREEN_SIZE[0] - MENU_NAV[0] - BUTTON_SIZE[0], SCREEN_SIZE[1] - MENU_NAV[1],
                                  button_size=tuple((x//1.2 for x in BUTTON_SIZE)),
                                  func=self.to_next)
        self.prev_button = Button('Назад', SCREEN_SIZE[0]*0.12, SCREEN_SIZE[1] - MENU_NAV[1],
                                  button_size=tuple((x // 1.2 for x in BUTTON_SIZE)),
                                  func=self.to_prev)
        self.buy_button = Button('Купить', SCREEN_SIZE[0] * 0.41, SCREEN_SIZE[1]*0.65,
                                  button_size=tuple((x // 1.2 for x in BUTTON_SIZE)),
                                  func=self.buy)
        self.put_on_button = Button('Надеть', SCREEN_SIZE[0]*0.12, SCREEN_SIZE[1] - MENU_NAV[1] - BUTTON_SIZE[1],
                                    button_size=tuple((x // 1.2 for x in BUTTON_SIZE)),
                                    func=self.use_item)
        self.buttons = self.next_button, self.prev_button, self.buy_button, self.put_on_button

        self.update()

    def to_next(self):
        if self.curent_item != len(self.items) - 1:
            self.curent_item += 1
    def to_prev(self):
        if self.curent_item != 0:
            self.curent_item -= 1

    def buy(self):
        if self.game.money > self.items[self.curent_item].price and not self.items[self.curent_item].is_bought:
            self.items[self.curent_item].is_bought = True
            self.game.money -= self.items[self.curent_item].price



    def use_item(self):
        if self.items[self.curent_item].is_bought:
            self.items[self.curent_item].is_put_on = not self.items[self.curent_item].is_put_on
    def update(self):
        self.price_text = text_render(self.items[self.curent_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_SIZE[0] // 2, 180)
        self.name_text = text_render(self.items[self.curent_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_SIZE[0] // 2, 120)
        self.use_text = text_render("Надето")
        self.use_text_rect = self.use_text.get_rect()
        self.use_text_rect.midright = (SCREEN_SIZE[0] - 150, 125)
        self.buy_text = text_render("Куплено")
        self.buy_text_rect = self.buy_text.get_rect()
        self.buy_text_rect.midright = (SCREEN_SIZE[0] - 140, 195)

        for button in self.buttons:
            button.update()

    def draw(self, screen):

        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.items[self.curent_item].image, self.item_rect)

        if self.items[self.curent_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))

        if self.items[self.curent_item].is_put_on:
            screen.blit(self.top_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))

        for button in self.buttons:
            button.draw(screen)
        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.use_text, self.use_text_rect)
        screen.blit(self.buy_text, self.buy_text_rect)
class Button:
    def __init__(self, text, x, y, button_size=BUTTON_SIZE, text_font=font, func=None):
        self.idle_image = load_image("images/button.png", button_size)
        self.pressed_image = load_image('images/button_clicked.png', button_size)
        self.image = self.idle_image
        self.rect = self.image.get_rect(x=x, y=y)
        self.text_font = text_font
        self.text = self.text_font.render(str(text), True, 'black')
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center
        self.is_pressed = False
        self.func = func

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):

        if pg.mouse.get_pressed()[0] and self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.is_pressed:
                self.is_pressed = True
                self.image = self.pressed_image
                self.func()
        else:
            self.is_pressed = False
            self.image = self.idle_image



class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        pg.display.set_caption("Виртуальный питомец")

        with open('save.json', encoding='utf-8') as f:
            data = json.load(f)

        self.happiness = data["hapiness"]
        self.satiety = data["satiety"] 
        self.health = data["health"]
        self.money = data["money"]
        self.coins_per_second = data["coins_per_second"]
        self.costs_of_upgrade = {}
        print(data)

        for i in data["cost_of_upgrade"]:
            self.costs_of_upgrade[int(i)] = data["cost_of_upgrade"][i]

        self.clock = pg.time.Clock()

        self.mode = 'Main'

        self.background = load_image("images/background.png", SCREEN_SIZE)
        self.happiness_image = load_image("images/happiness.png", ICON_SIZE)
        self.satiety_image = load_image("images/satiety.png", ICON_SIZE)
        self.health_image = load_image("images/health.png", ICON_SIZE)
        self.money_image = load_image("images/money.png", ICON_SIZE)
        self.dog_image = load_image('images/dog.png', DOG_SIZE)

        self.eat_button = Button('Еда', SCREEN_SIZE[0] - BUTTON_SIZE[0] - PADDING, ICON_SIZE[0] + PADDING, func=self.food_menu_on)
        self.clothes_button = Button('Одежда', SCREEN_SIZE[0] - BUTTON_SIZE[0] - PADDING,
                                     ICON_SIZE[0] + PADDING * 2 + BUTTON_SIZE[1],
                                     func=self.clothes_menu_on)
        self.play_button = Button('Игры', SCREEN_SIZE[0] - BUTTON_SIZE[0] - PADDING,
                                  ICON_SIZE[0] + PADDING * 3 + BUTTON_SIZE[1] * 2,
                                  func=self.mini_game_on)
        self.upgrade_button = Button('Улучшить', SCREEN_SIZE[0] - ICON_SIZE[1], 0,
                                     button_size=[i // 3 for i in BUTTON_SIZE],
                                     text_font=mini_font,
                                     func=self.increase_money)

        self.buttons = [self.eat_button, self.clothes_button, self.play_button, self.upgrade_button]

        self.clothes_menu = ClothesMenu(self, data["items"])
        self.food_menu = FoodMenu(self)
        self.mini_game = MiniGame(self)

        self.DICREASE = pg.USEREVENT + 2
        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)
        pg.time.set_timer(self.DICREASE, 1000)

        self.run()

    def clothes_menu_on(self):
        self.mode = "Clothes menu"
    def food_menu_on(self):
        self.mode = "Food menu"

    def mini_game_on(self):
        self.mode = 'Mini game'
        self.mini_game.new_game()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def increase_money(self):
        for cost in self.costs_of_upgrade:
            if not self.costs_of_upgrade[cost] and self.money >= cost:
                self.money -= cost
                self.coins_per_second += 1
                self.costs_of_upgrade[cost] = True

    def dicrease(self):
        chance = random.randint(0, 10)

        if chance <= 5:
            self.satiety -= 1
        elif 5 < chance <= 9:
            self.happiness -= 1
        else:
            self.health -= 1

    def save(self):
        with open("save.json", 'w', encoding='utf-8') as f:
            items = []
            for item in self.clothes_menu.items:
                items.append({
                    "name": item.name,
                    "price": item.price,
                    "image": item._file,
                    "is_put_on": item.is_put_on,
                    "is_bought": item.is_bought
                })
            data = {
                "hapiness": self.happiness,
                "satiety": self.satiety,
                "health": self.health,
                "money": self.money,
                "coins_per_second": self.coins_per_second,
                "cost_of_upgrade": self.costs_of_upgrade,
                "items": items
            }
            json.dump(data, f, ensure_ascii=False)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.mode == "Game over":
                    data = {
                        "hapiness": 100,
                        "satiety": 100,
                        "health": 100,
                        "money": 0,
                        "coins_per_second": 1,
                        "cost_of_upgrade": {
                            "100": False,
                            "1000": False,
                            "5000": False,
                            "10000": False
                        },
                        "items": [
                            {
                                "name": "Синяя футболка",
                                "price": 10,
                                "image": "images/items/blue t-shirt.png",
                                "is_put_on": False,
                                "is_bought": False
                            },
                            {
                                "name": "Ботинки",
                                "price": 50,
                                "image": "images/items/boots.png",
                                "is_put_on": False,
                                "is_bought": False
                            },
                            {
                                "name": "Шляпа",
                                "price": 50,
                                "image": "images/items/hat.png",
                                "is_put_on": False,
                                "is_bought": False
                            }
                        ]
                    }
                    with open("save.json", 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False)
                else:
                    self.save()
                pg.quit()
                exit()

            if self.mode != "Game over" and event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += self.coins_per_second

            elif self.mode != "Game over" and event.type == self.DICREASE:
                self.dicrease()

            if event.type == pg.KEYDOWN:
                if event.key ==  pg.K_ESCAPE:
                    self.mode = 'Main'

    def update(self):
        if self.mode == 'Main':
            for button in self.buttons:
                button.update()
        elif self.mode == 'Clothes menu':
            self.clothes_menu.update()
        elif self.mode == 'Food menu':
            self.food_menu.update()
        elif self.mode == 'Mini game':
            self.mini_game.update()

        if self.happiness <= 0 or self.satiety <= 0 or self.health <= 0:
            self.mode = 'Game over'




    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(self.satiety_image, (PADDING, PADDING + ICON_SIZE[0]))
        self.screen.blit(self.health_image, (PADDING, PADDING + ICON_SIZE[0] * 2))
        self.screen.blit(self.money_image, (SCREEN_SIZE[0] - PADDING - ICON_SIZE[1], PADDING))
        self.screen.blit(self.dog_image, (280, 130))
        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE[1], PADDING * 6))
        self.screen.blit(text_render(self.satiety), (PADDING + ICON_SIZE[1], PADDING * 6 + ICON_SIZE[1]))
        self.screen.blit(text_render(self.health), (PADDING + ICON_SIZE[1], PADDING * 6 + ICON_SIZE[1] * 2))
        self.screen.blit(text_render(self.money), (SCREEN_SIZE[0] - PADDING * 10 - ICON_SIZE[1], PADDING * 7))

        for button in self.buttons:
            button.draw(self.screen)

        for item in self.clothes_menu.items:
            if item.is_put_on:
                self.screen.blit(item.full_image, (SCREEN_SIZE[0]*0.31, SCREEN_SIZE[1]*0.24))
        if self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)

        elif self.mode == "Food menu":
            self.food_menu.draw(self.screen)

        elif self.mode == "Mini game":
            self.mini_game.draw(self.screen)
        elif self.mode == "Game over":
            text = text_render("Проигрыш", maxi_font, 'red')
            text_rect = text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
            self.screen.blit(text, text_rect)

        pg.display.flip()

if __name__ == "__main__":
    Game()
