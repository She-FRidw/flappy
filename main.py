import pygame
import random
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((829, 818))
pygame.display.set_caption('flappy bird')#название игры
icon = pygame.image.load('images/bird1.png')#иконка игры
pygame.display.set_icon(icon)

background = pygame.image.load('images/bg.png')
ground = pygame.image.load("images/ground.png")
#создаем игровые переменные
ground_scroll = 0 #для движения земли
scroll_speed = 4  #скорость движения земли
flying = False #для начала игры не сразу
game_over = False #для завершения игры
pipe_gap = 170 #для расстояния между верхней и нижней трубами
pipe_frequency = 1500 #милисекунды
last_pipe = pygame.time.get_ticks() - pipe_frequency#время генерации последней трубы
score = 0  # счетчик препятствий
font_res = pygame.font.Font("font/Minecraft Rus NEW.otf", 35)  # тип и размер шрифта
font_score = pygame.font.Font(None, 30)  # тип и размер шрифта
restart_button = pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 3 - 20, 200, 80)  # X, Y, Ширина, Высота
restart_button_white = pygame.Rect(screen.get_width() / 2 - 55, screen.get_height() / 3 - 25, 210, 90)  # X, Y, Ширина, Высота
restart_button_brown = pygame.Rect(screen.get_width() / 2 - 60, screen.get_height() / 3 - 30, 220, 105)  # X, Y, Ширина, Высота

#создаем класс игрока
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):#создание картинки
        pygame.sprite.Sprite.__init__(self)
        self.images = [] #создаем массив картинок для анимации
        self.counter = 0 #подсчет времени иттерации
        self.bird_anim_count = 0 #контроль номера картинки
        for num in range(1, 4): #цикл, заполняющий массив картинками
            img = pygame.image.load(f'images/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.bird_anim_count] #картинка, котторую будем выводить
        self.rect = self.image.get_rect() #выводим картинку
        self.rect.center = [x,y] #местоположение выводимой картинки
        self.vel = 0 #контроль увеличения координаты y
        self.clicked = False # \для контроля, чтобы птица не поднималась выше при удержании мышки

    def jump(self):
        self.vel = -10  # Устанавливаем скорость прыжка в отрицательное значение для движения вверх
        self.clicked = True
    def update(self):#обновляем картинку
        if flying == True:#когда игра начата
            #создание гравитации
            self.vel += 0.5
            if self.vel > 7:# чтобы более плавно падала
                self.vel = 7
            if self.rect.bottom < 683:
                self.rect.y += int(self.vel)
        if game_over == False:#если игра не окончена
            #создание прыжка по нажатию мыши
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False : #если нажата правая кнопка мыши
                self.jump()
            if pygame.mouse.get_pressed()[0] == 0: #если правая кнопка мыши разжата
                self.clicked = False
            #анимация полета
            self.counter += 1
            flap_cooldown = 5#контроль времени переключения картинок
            if self.counter > flap_cooldown:# делаем смену картинки на следующий номер
                self.counter = 0
                self.bird_anim_count += 1
                if self.bird_anim_count == 3:#если предыдущая картинка была третьей, то начинаем сначала
                    self.bird_anim_count = 0
            self.image = self.images[self.bird_anim_count]

            #поворот птицы при прыжке и падении
            self.image = pygame.transform.rotate(self.images[self.bird_anim_count], self.vel * (-2))#умнижили на -, чтобы при падении смотрела вниз, а при прыжке вверх, и на 2, чтобы поворот был больше
        else:#если игра окончена
            self.image = pygame.transform.rotate(self.images[self.bird_anim_count], -90)

#создаем класс препятствий
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):#создание картинки
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/pipe.png')
        self.rect = self.image.get_rect()
        #позиция 1, если труба сверху и 2, если снизу
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)#если трубф сверху, переворачиваем картинку
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]#координаты снизу
        if position == 2:
            self.rect.topleft = [x,y +  int(pipe_gap / 2)]#координаты сверху
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()  # Удаляем трубу, когда она выходит за экран
            global score
            score += 0.5  # Увеличиваем счетчик


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(150,309)
bird_group.add(flappy)

running = True
while running:
    clock.tick(60)
    screen.blit(background, (0,0))#вывод заднего фона

    bird_group.draw(screen)#вывод птички
    bird_group.update()  #обновляем картинку

    pipe_group.draw(screen)  #вывод трубы

    screen.blit(ground, (ground_scroll, 683))  #вывод земли

    #если птица ударяется об стенку или потолок, игра окончена
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom >= 683: #если птица ударяется о землю, игра окончена
        game_over = True
        flying = False

    if game_over:
        if game_over:
            pygame.draw.rect(screen, [65, 25, 0], restart_button_brown)  # Рисуем кнопку (коричневый)
            pygame.draw.rect(screen, [255, 255, 255], restart_button_white)  # Рисуем кнопку (белый)
            pygame.draw.rect(screen, [255, 79, 0], restart_button)  # Рисуем кнопку (ораньжевый)
            restart_text = font_res.render('RESTART', True, (255, 255, 255))
            restart_text_rect = restart_text.get_rect(center=restart_button.center)  # Выровнять текст по центру кнопки
            screen.blit(restart_text, restart_text_rect)  # Позиционируем текст на кнопке

        # Проверка нажатия на кнопку
        if event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
            # Сброс игровых переменных
            score = 0
            game_over = False
            # Перезапуск игры (например, создание новой птицы и очистка группы труб)
            bird_group.empty()
            pipe_group.empty()
            flappy = Bird(150, 309)
            bird_group.add(flappy)

    if game_over == False and flying == True: #если игра не окончена, продолжаем движение

        # создание новых препятствий
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:  # если с момента создания прошлой трубы прошло нужное кл-во времени, создаем новую
            pipe_hieght = random.randint(-150, 150) #рандомное изменение высоты трубы
            top_pipe = Pipe(829, 309 + pipe_hieght, 1)  # ввод верхней трубы
            bottom_pipe = Pipe(829, 309 + pipe_hieght, 2)  # ввод нижней трубы
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed#создание движения земли
        if ground_scroll < -35:#взяли картинку с запасом, чтобы она оюновлялась незаметно
            ground_scroll = 0
        pipe_group.update()  # обновляем картинку труб
    score_text = font_score.render(f'Score: {int(score)}', True, (255, 255, 255))  # Белый цвет
    screen.blit(score_text, (10, 10))  # Отображаем в верхнем левом углу
    pygame.display.update()

    for event in pygame.event.get():#закрытие по нажатию кнопки, а не автоматически
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:#начало игры посла нажатия мыши
            flying = True
        if event.type == pygame.KEYDOWN:  # Проверка нажатия клавиш
            if event.key == pygame.K_SPACE:  # Если нажат пробел
                if game_over:
                    # Сброс игровых переменных и перезапуск игры
                    score = 0
                    game_over = False
                    bird_group.empty()
                    pipe_group.empty()
                    flappy = Bird(150, 309)
                    bird_group.add(flappy)
                else:
                    # Здесь код для прыжка птицы, если игра не окончена
                    flappy.jump()
pygame.quit()
