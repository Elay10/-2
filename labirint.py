from pygame import *



class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        #каждый спрайт дожен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    #метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        #вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed


    def update(self):
        '''пермещает персонажа, применяя текущую горизантальную и вертикальную скорость'''
        #сначала движения по горизантальной
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        #если защли за стену, то втанет вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:    
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed > 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) 
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
            #если зашли за стенку, то встает вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                #проверяем какая из платформ снизу самая высокая, выравниваемся по ней
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)
    #метод "выстрел" (используя место игрока, чтобы создать пулю)
    def fire(self):
        bullet = Bullet('mario.block.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)


#класс спрайта - врага
class Enemy(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed


    #движения врага
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


#класс спрайта - пули
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    #движения врага
    def update(self):
        self.rect.x += self.speed
        #исчезает, если дойдет до края экрна
        if self.rect.x > win_width + 10:
            self.kill()
    

#Создание окна
win_width = 700
win_height = 500 
display.set_caption('Лабиринт')
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)#задаем цвет согласно цветовой схеме RGB

mixer.init()
mixer.music.load('mario.mp3')
mixer.music.play()

#создаем группу для стен
barriers = sprite.Group()


#создаем группу для пуль
bullets = sprite.Group()


#создаем группу для монстров
monsters = sprite.Group()


#создаем стены картинки
w1 = GameSprite('mario_wall.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('wall2.jpg', 370, 100, 50, 400)


#добавление стены в группу
barriers.add(w1)
barriers.add(w2)


#создаем спрайты
packman = Player('mario3.jpg', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('mystery_box.png', win_width - 85, win_height - 100, 80, 80)


monster1 = Enemy('villian.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('villian.png', win_width - 80, 230, 80, 80, 5)
#добавляем монстра в группу
monsters.add(monster1)
monsters.add(monster2)


#переменная, отвечающая за то, как кончилосась игра
finish = False
#игоровой цикл
run = True
while run:
    #цикл срабатывает каждую 0.05 секунд
    time.delay(50)
    #перебираем все события, которые моги произойти
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()    
        
        
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    
    
    #проверка, что игра еще не заврешена
    if not finish:
        #обновляем фон каждую интерацию
        window.fill(back)#закрашиваем окно цветом

        #запускаем движения спрайтов
        packman.update()
        bullets.update()


        #обновляем их в новом местоположении при каждой интерации цикла
        packman.reset()
        #рисуем стены 2
        #
        #
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()


        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)


        #Проверка столкновения героя с врагом и стенами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            #вычисляем отношение
            img = image.load('background2.jpg')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))


        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('background2.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update()    