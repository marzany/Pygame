import pygame
import random

class Pelaaja:
  def __init__(self):
    self.kuva = pygame.image.load("robo.png")
    self.x = 0
    self.y = 480-self.kuva.get_height()
    self.robo_oikealle = False
    self.robo_vasemmalle = False
    self.robo_ylos = False
    self.robo_alas = False

# Pelaajan liikkuminen + nopeus
  def liiku(self):
    if self.robo_oikealle and self.x < 640-self.kuva.get_width():
      self.x += 4
    if self.robo_vasemmalle and self.x > 0:
      self.x -= 4
    if self.robo_ylos and self.y > 0:
      self.y -= 4
    if self.robo_alas and self.y < 480-self.kuva.get_height():
      self.y += 4

  def get_position_x(self):
    return self.x

  def get_position_y(self):
    return self.y

class Monster:
  def __init__(self, nopeus: float):
    self.nopeus = nopeus
    self.kuva = pygame.image.load("hirvio.png")
    self.x = random.randint(0, 640-self.kuva.get_width())
    self.y = random.randint(0, 480-self.kuva.get_height())

#Liikuttaa monsteria kohti pelaajaa
  def liiku(self, Pelaaja):
    nopeus = self.nopeus
    if self.x > Pelaaja.get_position_x():
      self.x -= nopeus
    if self.x < Pelaaja.get_position_x():
      self.x += nopeus
    if self.y > Pelaaja.get_position_y():
      self.y -= nopeus
    if self.y < Pelaaja.get_position_y():
      self.y += nopeus

# tarkastaa osuuko monsteri pelaajaan
  def osuuko(self, Pelaaja):
    return ((self.x in range(Pelaaja.get_position_x(), Pelaaja.get_position_x() + 40) and self.y in range(Pelaaja.get_position_y(), Pelaaja.get_position_y() + 40)) or
    ((self.x + 40) in range(Pelaaja.get_position_x(), Pelaaja.get_position_x() + Pelaaja.kuva.get_width()) and (self.y + 60) in range(Pelaaja.get_position_y(), Pelaaja.get_position_y() + Pelaaja.kuva.get_height())))


#Pelin luokka
class Collector:
  def __init__(self):
    pygame.init()
    self.peli = True
    self.monsterit = []
    self.robo = Pelaaja()
    self.keratyt_kolikot = 0
    self.kolikko_x = random.randint(1, 640-self.robo.kuva.get_width())
    self.kolikko_y = random.randint(1, 480-self.robo.kuva.get_height())
    self.naytto = pygame.display.set_mode((640, 480))
    self.fontti = pygame.font.SysFont("Arial", 24)
    self.paattyi = pygame.font.SysFont("Arial", 50)

    self.kello = pygame.time.Clock()

    self.lataa_kuvat()
    self.uusi_peli()
    self.silmukka()

  def lataa_kuvat(self):
    self.kolikko = pygame.image.load("kolikko.png")

  def uusi_peli(self):
    self.robo.x = 0
    self.robo.y = 480-self.robo.kuva.get_height()
    self.keratyt_kolikot = 0

    self.kolikko_x = random.randint(1, 640-self.robo.kuva.get_width())
    self.kolikko_y = random.randint(1, 480-self.robo.kuva.get_height())

    self.monsterit.clear()
    self.monsterit.append(Monster(1))

  def nollaa(self):
    self.robo.robo_oikealle = False
    self.robo.robo_vasemmalle = False
    self.robo.robo_alas = False
    self.robo.robo_ylos = False
    self.peli = True
    self.lataa_kuvat()
    self.uusi_peli()
    self.silmukka()

#Jos osut monsteriin
  def peli_paattyi(self):
    self.naytto.fill((155, 0, 0))
    loppu = self.paattyi.render(f"Game Over", True, (0, 0, 0))
    self.naytto.blit(loppu, (200, 200))
    score = self.fontti.render(f"Kerätyt kolikot: {self.keratyt_kolikot}/12", True, (0, 0, 0))
    self.naytto.blit(score, (400, 0))
    uusipeli = self.fontti.render("F2 - Uusi Peli", True, (0, 0, 0))
    self.naytto.blit(uusipeli, (50, 450))
    suljepeli = self.fontti.render("ESC - Lopeta peli", True, (0, 0, 0))
    self.naytto.blit(suljepeli, (200, 450))
    pygame.display.flip()
    for tapahtuma in pygame.event.get():
      if tapahtuma.type == pygame.KEYUP:
        if tapahtuma.key == pygame.K_F2:
          self.nollaa()
        if tapahtuma.key == pygame.K_ESCAPE:
          exit()
  
  def peli_lapi(self):
    self.naytto.fill((155, 0, 0))
    loppu = self.paattyi.render(f"Yay! Voitit pelin!", True, (0, 0, 0))
    self.naytto.blit(loppu, (200, 200))
    score = self.fontti.render(f"Kerätyt kolikot: {self.keratyt_kolikot}/12", True, (0, 0, 0))
    self.naytto.blit(score, (400, 0))
    uusipeli = self.fontti.render("F2 - Uusi Peli", True, (0, 0, 0))
    self.naytto.blit(uusipeli, (50, 450))
    suljepeli = self.fontti.render("ESC - Lopeta peli", True, (0, 0, 0))
    self.naytto.blit(suljepeli, (200, 450))
    pygame.display.flip()
    for tapahtuma in pygame.event.get():
      if tapahtuma.type == pygame.KEYUP:
        if tapahtuma.key == pygame.K_F2:
          self.nollaa()
        if tapahtuma.key == pygame.K_ESCAPE:
          exit()

#Pääsilmukka
  def silmukka(self):
    while self.peli == True:
      if self.keratyt_kolikot < 12:
        self.tutki_tapahtumat()
        self.piirra_naytto()
        self.kello.tick(60)
      elif self.keratyt_kolikot == 12:
        self.peli_lapi()
    while self.peli == False:
      self.peli_paattyi()

  def tutki_tapahtumat(self):
    #Robotin liikkuminen näppäimillä
    for tapahtuma in pygame.event.get():
      if tapahtuma.type == pygame.KEYDOWN:
        if tapahtuma.key == pygame.K_LEFT:
          self.robo.robo_vasemmalle = True
        if tapahtuma.key == pygame.K_RIGHT:
          self.robo.robo_oikealle = True
        if tapahtuma.key == pygame.K_UP:
          self.robo.robo_ylos = True
        if tapahtuma.key == pygame.K_DOWN:
          self.robo.robo_alas = True 
      if tapahtuma.type == pygame.KEYUP:
        if tapahtuma.key == pygame.K_LEFT:
          self.robo.robo_vasemmalle = False
        if tapahtuma.key == pygame.K_RIGHT:
          self.robo.robo_oikealle = False
        if tapahtuma.key == pygame.K_UP:
          self.robo.robo_ylos = False
        if tapahtuma.key == pygame.K_DOWN:
          self.robo.robo_alas = False
        if tapahtuma.key == pygame.K_F2:
          self.nollaa()
        if tapahtuma.key == pygame.K_ESCAPE:
          exit()

    self.robo.liiku()
    for monsteri in self.monsterit:
      monsteri.liiku(self.robo)
      if monsteri.osuuko(self.robo):
        self.peli = False

  #Tarkistus kolikon osumasta ja siirto uuteen paikkaan
    if (self.kolikko_x in range(self.robo.x, self.robo.x + 50) and self.kolikko_y in range(self.robo.y, self.robo.y + 50)) or (self.kolikko_x in range(self.robo.x, self.robo.x + self.kolikko.get_width()) and self.kolikko_y in range(self.robo.y, self.robo.y + self.kolikko.get_height())):
      self.keratyt_kolikot = self.keratyt_kolikot + 1
      self.kolikko_x = random.randint(1, 600-self.robo.kuva.get_width())
      self.kolikko_y = random.randint(1, 400-self.robo.kuva.get_height())
    #Kun tietyn verran kolikoita kerätty, tulee lisää monstereita = peli vaikeutuu:
    if self.keratyt_kolikot == 4 and len(self.monsterit) == 1:
      self.monsterit.append(Monster(1.5))
    if self.keratyt_kolikot == 7 and len(self.monsterit) == 2:
      self.monsterit.append(Monster(2))



  def piirra_naytto(self):
    #Lisää näytön tekstit, pisteet ja kuvat näkyviin
    self.naytto.fill((155, 0, 0))
    score = self.fontti.render(f"Kerätyt kolikot: {self.keratyt_kolikot}/12", True, (0, 0, 0))
    self.naytto.blit(score, (400, 0))
    uusipeli = self.fontti.render("F2 - Uusi Peli", True, (0, 0, 0))
    self.naytto.blit(uusipeli, (50, 450))
    suljepeli = self.fontti.render("ESC - Lopeta peli", True, (0, 0, 0))
    self.naytto.blit(suljepeli, (200, 450))
    self.naytto.blit(self.robo.kuva, (self.robo.x, self.robo.y))
    self.naytto.blit(self.kolikko, (self.kolikko_x, self.kolikko_y))
    for monster in self.monsterit:
      self.naytto.blit(monster.kuva, (monster.x, monster.y))
    pygame.display.flip()


if __name__ == "__main__":
  Collector()
