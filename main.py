import pygame, sys, random
pygame.init ()


# ngegambar jalan
def draw_jalan():
  SCREEN.blit(jalan, (0, jalan_y))
  SCREEN.blit(jalan, (0, jalan_y - 650))

# posisi coin
coin_random_x1 = [i for i in range(250, 650, 17)]
coin_random_x2 = [i for i in range(250, 650, 17)]
coin_y = -650

# membuat coin
def create_coin():
  coin_pos1 = random.choice(coin_random_x1)
  coin_pos2 = random.choice(coin_random_x2)
  coin_left = coin.get_rect(center = (coin_pos1, coin_y))
  coin_right = coin.get_rect(center = (coin_pos2, coin_y -900))
  return coin_left, coin_right

# menggambar coin
def draw_coin(coins):
  for coinn in coins:
    SCREEN.blit(coin,coinn)

# menggerakkan coin
def move_coins(coins):
  for coinn in coins:
    coinn.centery += 5
  visible_coins = [coinn for coinn in coins]
  return visible_coins

# posisi mobil musuh
enemy1_x = [i for i in range(130, 325, 10)]
enemy2_x = [i for i in range(325, 551, 10)]
enemy_y = -650

# membuat mobil musuh
def create_enemy():
  random_enemy_pos1 = random.choice(enemy1_x)
  random_enemy_pos2 = random.choice(enemy2_x)
  enemy_left = enemy.get_rect(midleft = (random_enemy_pos1, enemy_y))
  enemy_right = enemy.get_rect(midright = (random_enemy_pos2, enemy_y -900))
  return enemy_left,enemy_right

# menggambar mobil musuh
def draw_enemy(enemies):
	for enemyy in enemies:
		SCREEN.blit(enemy,enemyy)

# menggerakkan mobil musuh
def move_enemy(enemies):
	for enemyy in enemies:
		enemyy.centery += 7
	visible_enemies = [enemyy for enemyy in enemies]
	return visible_enemies

# score bertambah ketika player mengenai coin (scoring)
can_score = True
def coin_score(coins):
  global score, can_score, coin_list
  for coinn in coins:
    if player_rect.colliderect(coinn) and can_score:
      score += 1
      coin_sound.play()
      coin_list = [] #reset coin
      can_score = True

# cek tabrakan dengan mobil musuh
def check_collision(enemies):
    global can_score
    for enemyy in enemies:
      if player_rect.colliderect(enemyy):
        crash_sound.play()
        can_score = True
        return False
    return True

# menampilkan score dan main screen
def main_screen():
    if start:
        score_surface = game_font1.render(str(int(score)),True,(0,0,0))
        score_rect = score_surface.get_rect(center = (100,30))
        SCREEN.blit(score_surface,score_rect)
    else:
        SCREEN.blit(jalan,(0,0))
        text_title = game_font1.render(f'Vroom Vroom Car Dash' ,True,(0,0,0))
        SCREEN.blit(text_title, [230, 225])
        text_ins = game_font1.render(f'Press SPACE to Play' ,True,(0,0,0))
        SCREEN.blit(text_ins, [255, 285])
        score_surface = game_font2.render(f'Score: {int(score)}' ,True,(0,0,0))
        score_rect = score_surface.get_rect(center = (420,355))
        SCREEN.blit(score_surface,score_rect)
        high_score_surface = game_font2.render(f'High score: {int(high_score)}',True,(0,0,0))
        high_score_rect = high_score_surface.get_rect(center = (420,405))
        SCREEN.blit(high_score_surface,high_score_rect)

        pygame.display.flip()


SCREEN = pygame.display.set_mode((840, 650))
pygame.display.set_caption("Vroom Vroom Car Dash")
icon = pygame.image.load('assets/GreenStrip.png') 
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 130

# aset gambar
# pemain
player = pygame.image.load('assets/BlackOut.png').convert_alpha()
player_rect = player.get_rect(center= (420,500))

# jalan
jalan = pygame.image.load('assets/background-1.png')
jalan_y = 0

# koin
coin = pygame.image.load('assets/coin_01.png').convert_alpha()
coin_list = create_coin()

# mobil musuh
enemy = pygame.image.load('assets/GreenCar.png').convert_alpha()
enemy_list = create_enemy()

# sfx
player_sound = pygame.mixer.Sound('assets/sound/car.wav')
coin_sound = pygame.mixer.Sound('assets/sound/coin.wav')
enemy_sound = pygame.mixer.Sound('assets/sound/beep.wav')
crash_sound = pygame.mixer.Sound('assets/sound/tabrakan.wav')

# memanggil mobil musuh
SPAWNENEMY = pygame.USEREVENT
pygame.time.set_timer(SPAWNENEMY,2000)
enemy_list = []

# memanggil coin
SPAWNCOIN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNCOIN,3000)
coin_list = []

# score dan high score
score = 0
high_score = 0
game_font1 = pygame.font.SysFont('monaco', 50)
game_font2 = pygame.font.SysFont('monaco', 35)

start = False
player_movement = 0

# logika game
while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      # jika keyboard ditekan, mobil player bergerak
      if event.type == pygame.KEYDOWN:
        # game dimulai dengan tekan SPACE
        if event.key == pygame.K_SPACE and not start:
          enemy_list = []
          coin_list = []
          score = 0
          start = True
        if event.key == pygame.K_RIGHT and start:
          player_movement = 5 #kanan
        if event.key == pygame.K_LEFT and start:
          player_movement = -5 #kiri

      # jika keyboard dilepas, mobil player berhenti 
      if event.type == pygame.KEYUP:
          if event.key == pygame.K_RIGHT and start:
            player_sound.play()
            player_movement = 0 #berhenti
          if event.key == pygame.K_LEFT and start:
            player_sound.play()
            player_movement = 0 #berhenti

      # event memanggil mobil musuh
      if event.type == SPAWNENEMY:
        enemy_list.extend(create_enemy())
        enemy_sound.play()

      # event memanggil koin
      if event.type == SPAWNCOIN:
        coin_list.extend(create_coin())
  

    SCREEN.fill((255,255,255))

# jika game dimulai
    if start:
      # menggerakkan jalan
      jalan_y += 5
      draw_jalan() 
      if jalan_y >= 650:
        jalan_y = 0 
      
      # menggerakkan player
      if player_rect.x > 130:  
        player_rect.x += player_movement
        SCREEN.blit(player,player_rect)
      elif player_rect.left <= 130:
        player_rect.x = 131 #supaya mobil tidak melewati batas kiri
        SCREEN.blit(player,player_rect)
      if player_rect.x < 650: 
        player_rect.x += player_movement
        SCREEN.blit(player,player_rect)
      elif player_rect.left >= 650:
        player_rect.x = 649 #supaya mobil tidak melewati batas kanan
        SCREEN.blit(player,player_rect)

      # memulai mengecek adanya tabrakan antara player dengan musuh
      start = check_collision(enemy_list)
      enemy_list = move_enemy(enemy_list)
      draw_enemy(enemy_list)

      # mengecek apakah mobil menyentuh koin, kemudian menambahkan skor
      coin_score(coin_list)
      coin_list = move_coins(coin_list)
      draw_coin(coin_list)


    else:
      # penyimpanan high score
      if high_score < score:
        high_score = score
      enemy_sound.stop()


    # menampilkan score, high score, dan main screen
    main_screen()
    pygame.display.update()
