import pygame                                                                                                                       # Importowanie biblioteki PYGAME
from os.path import join
from random import randint, uniform
from pygame.sprite import Group

class Player(pygame.sprite.Sprite):                                                                                                 # Tworzymy klase GRACZ
    def __init__(self, groups):                                                                                                     # Konstruktor klasy
        super().__init__(groups)                                                                                                    # Wywołanie konstruktora klasy bazowej
        self.image = pygame.image.load(join("STARSHIP", "IMAGE", "player.png")).convert_alpha()                                     # Tworzymy gracza i importujemy zdjecie wykorzystując ściezkę i optymalizujemy obraz z przeźroczytsością (ucinamy niepotrzebne rzeczy z obrazu)
        self.rect = self.image.get_frect(center = (window_width / 2, window_hight / 2))                                             # Ustalamy środek gracza i wysylamy go na wskazane współrzędne, Mozna zmienic np na topleft, bottomright i tez jest git
        self.direction = pygame.math.Vector2()                                                                                      # Zmienna kierunkowa gracza działająca na zasadzie vektora
        self.speed = 300                                                                                                            # Ustalamy szybkość gracza

        # Shoots Cooldown
        self.can_shoot = True                                                                                                       # Ustawiamy ze zawsze POTRAFISZ/MOZESZ strzelasz
        self.laser_shoot_time = 0                                                                                                   # Ustawiamy czas strzału laserem na 0                                                                                     
        self.cooldown_duration = 400                                                                                                # Ustawiamy czas cooldawn na strzał 0.4s

    def laser_timer(self):                                                                                                          # Funkcja słuząca do zarządzania czasem oczekiwania 
        if not self.can_shoot:                                                                                                      # Jeśli nie masz mozliwości strzału:
            current_time = pygame.time.get_ticks()                                                                                  # Zliczanie czasu, który upłynął od odpalenia gry
            #  print(current_time)                                                                                                  # Wypisywanie obecnego czasu
            if current_time - self.laser_shoot_time >= self.cooldown_duration:                                                      # Warunek czasowy na strzał
                self.can_shoot = True                                                                                               # Mozna oddać strzał

    def update(self, dt):                                                                                                           # Wprowadzanie zmian w sprite (aktualizacja gracza)
        keys = pygame.key.get_pressed()                                                                                             # Wartośc wciśniętego klaswisza jest przypisywana do zmiennej keys tyle razy ile trzymay klawisz
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])                                                     # Zmianna X kierunkowa zmienia znak na 1 lub -1 (w prawo to 1, w lewo to -1)
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])                                                        # Zmienna Y kierunkowa zmienia znak na 1 lub -1 (w doł to 1, w góre to -1)
        self.direction = self.direction.normalize() if self.direction else self.direction                                           # Normaluzujemy długośc zmiennej kierunkowej czyli wektora, bo w momencie chodzenia po skosie gracz mial wiekszosc predkosc bo nie zmienial polozenia o jeden pixel tylko o przekatna z jednego pixela w prawo i jednego w gore, obecnie jest zawsze taka sama predkość
        self.rect.center += self.direction * self.speed * dt                                                                        # RUCH GRACZA to Pozycja gracza, która się zmienia zaleznie od zmiennej kierunkowej, szybkości i czasu
    
        recent_keys = pygame.key.get_just_pressed()                                                                                 # Naciśniety klawisz przekazuje raz wartość do zmiennej recent_keys
        if recent_keys[pygame.K_SPACE] and self.can_shoot:                                                                          # Jeśli naciśnięty klawisz to SPACJA to:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))                                                       # Rysujemy na oknie gry laser 
            self.can_shoot = False                                                                                                  # Nie mozna strzelać
            self.laser_shoot_time = pygame.time.get_ticks()                                                                         # Przypisujemy do zmiannej czas
            laser_sound.play()                                                                                                      # Deklarujemy moment dźwięku lasera

        self.laser_timer()                                                                                                          # Sprawdzanie czy gracz moze strzelać

class Star(pygame.sprite.Sprite):                                                                                                   # Tworzymy klase GWIAZDA
    def __init__(self, groups, surf):                                                                                               # Konstruktor klasy
        super().__init__(groups)                                                                                                    # Wywołanie kontruktora klasy bazowej
        self.image = surf                                                                                                           # Tworzymy gwiazde na powierzchni
        self.rect = self.image.get_frect(center = (randint(0, window_width), randint(0, window_hight)))                             # Tworzymy gwaizde o losowych współrzędnych

class Laser(pygame.sprite.Sprite):                                                                                                  # Tworzymy klase LASER
    def __init__(self, surf, pos, groups):                                                                                          # Konstruktor klasy
        super().__init__(groups)                                                                                                    # Wywoływanie konstruktora klasy bazowej
        self.image = surf                                                                                                           # Tworzymy laser
        self.rect = self.image.get_frect(midbottom = pos)                                                                           # Tworzymy laser gdzie punkt odniesienia to środek dolnej krawędzi

    def update(self, dt):                                                                                                           # Funkcja aktualizacji
        self.rect.centery -= 400 * dt                                                                                               # Aktualizacaja pozycji Lasera
        if self.rect.bottom < 0:                                                                                                    # Jeśli dolna krawędz lasera będzie mniejsza niz 0 to:
            self.kill()                                                                                                             # Laser znika (zabija się)

class Meteor(pygame.sprite.Sprite):                                                                                                 # Tworzymy klasę METEOR
    def __init__(self, surf, pos, groups):                                                                                          # Kontruktor klasy
        super(). __init__(groups)                                                                                                   # Wywołanie konstruktora klasy
        self.original_surf = surf                                                                                                   # Tworzymy oryginalną przestrzeń meteora
        self.image = surf                                                                                                           # Tworzymy meteor na przestrzeni
        self.rect = self.image.get_frect(center = pos)                                                                              # Tworzymy meteor gdzie punkt odnieśienia to środek
        self.start_time = pygame.time.get_ticks()                                                                                   # Zliczanie czasu który upłynął od startu gry
        self.lifetime = 4000                                                                                                        # Czas zycia meteoru zanim zniknie
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)                                                                      # Dodanie współrzędnej X zeby meteor nie poruszał się tylko po Y, ale tez po X
        self.speed = randint(300, 500)                                                                                              # Prędkość mateora
        self.rotation_speed = randint(40, 80)                                                                                       # Prędkość obracania się meteora
        self.rotation_angle = 0                                                                                                     # Kąt początkowy o jaki się obraca meteor

    def update(self, dt):                                                                                                           # Funkcja aktualizacji
        self.rect.center += self.direction * self.speed * dt                                                                        # Równanie ruchu meteora
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:                                                              # Jeśli po powstaniu meteora minie 4s to:
            self.kill()                                                                                                             # Meteor znika (zabija się)
        self.rotation_angle += self.rotation_speed * dt                                                                             # Deklarujemy prawdziwy kąt obrotu meteora, który zwiększa się o 1 i mnozony jest o dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation_angle, 1)                                          # Realny obrót meteora
        self.rect = self.image.get_frect(center = self.rect.center)                                                                 # Usuwamy dziwne zachowanie się meteora

class AnimatedExplosion(pygame.sprite.Sprite):                                                                                      # Tworzymy klasę ANIMACJA EKSPOZJI
    def __init__(self, frames, pos, groups):                                                                                        # Kontruktor klasy
        super(). __init__(groups)                                                                                                   # Wywołanie konstruktora klasy
        self.frames = frames                                                                                                        
        self.frame_index = 0                                                                                                        # Tworzymy pierwszy element listy
        self.image = self.frames[self.frame_index]                                                                                  # Tworzymy listę zdjęć eksplozji
        self.rect = self.image.get_frect(center = pos)                                                                              # Tworzymy eksplozje gdzie punkt odniesienia to środek
        explosion_sound.play()                                                                                                      # Deklarujemy moment dźwięku eksplozji

    def update(self, dt):                                                                                                           # Funkcja aktualizacji
        self.frame_index += 40 * dt                                                                                                 # Deklarujemy prędkość zmian zdjęć
        if self.frame_index < len(self.frames):                                                                                     # Jeśli index jest mniejszy od ilości zdjęć ekspolzji to:
            self.image = self.frames[int(self.frame_index)]                                                                         # Pokaz animacje zdjeć
        else:                                                                                                                       # W innym przypadku:
            self.kill()                                                                                                             # Zabij animacje

def collision():                                                                                                                    # Tworzymy funkcję COLLISION
    global running                                                                                                                  # Odwołujemy się do zmiennej globalnej
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)                       # Tworzymy listę zderzeń meteora z playerem i definiujemy maske (zabicie jest dopiero jak obiekt, nie obramówka dotknie obiektu)
    if collision_sprites:                                                                                                           # Jeśli jest kolizja pomiędzy graczem a meteorem to:
        running = False                                                                                                             # Wyłącz gre

    for laser in laser_sprites:                                                                                                     # Dla laser w grupie laserów:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)                     # Tworzymy listę kolizji pomiędzy laserem a meteorem i Usuwamy dotknięty meteor przez laser
        if collided_sprites:                                                                                                        # Jeśli jest kolizja pomiędzy laserem a meteorem
            laser.kill()                                                                                                            # Usuń z ekranu laser
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)                                                     # Deklarujemy wykoanie się eksplozji w punkcie dotyku lasera z meteorem

def display_score():                                                                                                                # Tworzymy funkcję WYNIK
    current_time = pygame.time.get_ticks() // 1000                                                                                  # Przypisujemy do zmiennej czas od odpalenia gry
    text_surf = font.render(str(current_time), True, (240, 240, 240))                                                               # Tworzymy powierzchnię napisu, który będzie pokazywać czas od odpalenia gry i kolorze
    text_rect = text_surf.get_frect(midbottom = (window_width / 2, window_hight - 50))                                              # Miejsce wypisu textu
    screen.blit(text_surf, text_rect)                                                                                               # Zaimportowanie odpowiedniego textu i miejsca wypisu textu
    pygame.draw.rect(screen, (240, 240, 240), text_rect.inflate(20, 10).move(0, -7), 5, 10)                                         # Rysujemy obramówke tekstu

# General Setup
pygame.init()                                                                                                                       # Inicjacja wszystkich modułów PYGAME
window_width, window_hight = 1280, 720                                                                                              # Tworzymy zmienne ekranu: szerokość okna = 1280px i wysokość = 720px
screen = pygame.display.set_mode((window_width, window_hight))                                                                      # Zadeklarowanie okna gry
pygame.display.set_caption("STARSHIP THE GAME")                                                                                     # Nazwanie okna gry
running = True                                                                                                                      # Kontrola głównej pętli gry
clock = pygame.time.Clock()                                                                                                         # Timer który kontroluje klatki na sekundę gry

# Import Surface
star_surf = pygame.image.load(join("STARSHIP", "IMAGE", "star.png")).convert_alpha()                                                # Tworzymy gwiazde i importujemy zdjecie wykorzystując ściezkę i optymalizujemy obraz z przeźroczytsością (ucinamy niepotrzebne rzeczy z obrazu)
meteor_surf = pygame.image.load(join("STARSHIP", "IMAGE", "meteor.png")).convert_alpha()                                            # Tworzymy meteor i importujemy zdjecie wykorzystując ściezkę i optymalizujemy obraz z przeźroczytsością (ucinamy niepotrzebne rzeczy z obrazu)
laser_surf = pygame.image.load(join("STARSHIP", "IMAGE", "laser.png")).convert_alpha()                                              # Tworzymy laser i importujemy zdjecie wykorzystując ściezkę i optymalizujemy obraz z przeźroczytsością (ucinamy niepotrzebne rzeczy z obrazu)
font = pygame.font.Font(join("STARSHIP", "IMAGE", "Oxanium-Bold.ttf"), 40)                                                          # Tworzymy font i rozmiar dla napisui i importujemy zdjecie wykorzystując ściezkę
explosion_frames = [pygame.image.load(join("STARSHIP", "IMAGE", "EXPLOSION", f"{i}.png")).convert_alpha() for i in range (21)]      # Tworzymy ekspolzje i importujemy zdjęcia wykorzystując ściezkę i optymalizujemy obraz z przeźroczytsością (ucinamy niepotrzebne rzeczy z obrazu)

# Import Sound
laser_sound = pygame.mixer.Sound(join("STARSHIP", "AUDIO", "laser.wav"))                                                            # Tworzymy dźwięk lasera
laser_sound.set_volume(0.1)                                                                                                         # Usatwianie głośności dźwięku lasera
explosion_sound = pygame.mixer.Sound(join("STARSHIP", "AUDIO", "explosion.wav"))                                                    # Tworzymy dźwięk eksplozji
explosion_sound.set_volume(0.1)                                                                                                     # Usatwianiee głośności dźwięku lasera
game_music = pygame.mixer.Sound(join("STARSHIP", "AUDIO", "game_music.wav"))                                                        # Tworzymy muzyke gry
game_music.set_volume(0.05)                                                                                                         # Ustawianie głośności muzyki
game_music.play(loops = -1)                                                                                                         # Deklarujemy moment muzyki gry

# Sprities
all_sprites = pygame.sprite.Group()                                                                                                 # Tworzymy grupę aby wszystkie Sprites do niej trafiły 
meteor_sprites = pygame.sprite.Group()                                                                                              # Tworzymy kolejną grupe aby łatwiej było ogarnąc kolizje miedzy playerem a meteorem
laser_sprites = pygame.sprite.Group()
for i in range(20):                                                                                                                 # Tworzymy 20 gwiazd
    Star(all_sprites, star_surf)                                                                                                    # Dodajemy Gwiazde do all_sprites i star_surf
player = Player(all_sprites)                                                                                                        # Przypisujemy klase Player do zmiennej player i dodajemy ją do SPRITES

# custom event -> meteor event
meteor_event = pygame.event.custom_type()                                                                                           # Deklarujemy uniklany, własny custom event dla meteorów
pygame.time.set_timer(meteor_event, 500)                                                                                            # Ustawiamy Timer, który co czas 0.5s automatycznie dodaje zdarzenie do kolejki

while running:                                                                                                                      # Pętla główna gry
    dt = clock.tick() / 1000                                                                                                        # Ustawiliśmy klatki na sekundę gry

    # Event Loop
    for event in pygame.event.get():                                                                                                # Obsługa zdarzeń, Pozwala na odczytywanie i reagowanie na akcje gracza
        if event.type == pygame.QUIT:                                                                                               # Obsługa zdarzenia: Zamknięcie okna gry
            running = False                                                                                                         # Zakończenie głównej pętli gry
        if event.type == meteor_event:                                                                                              # Obsługa zdarzenia: jeśli zdarzenie to meteor_event
            x, y = randint(0, window_width), randint(-200, -100)                                                                    # Przypisujemy randomowe wartości wpółrzędnym na których meteory mają sie spawnować
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))                                                              # Rysujemy meteor na powyzszych współrzędnych i dodajemy do grup

    # Update
    all_sprites.update(dt)                                                                                                          # Aktualizacja SPRITÓW i ich pozycji
    collision()                                                                                                                     # Wywołujemy funkcje kolizji

    # Draw the game
    screen.fill("#3B1D58")                                                                                                          # Kolorowanie okna gry w formacie HEX
    display_score()                                                                                                                 # Wypisanie funkcji Wynik
    all_sprites.draw(screen)                                                                                                        # Rysowanie SPRITÓW na ekarnie

    pygame.display.update()                                                                                                         # Odświezanie ekranu gry i pokazywanie kazdej zmiany (zamiast UPDATE mozna uzyć FLIP)

pygame.quit()                                                                                                                       # Zakończenie działania PYGAME i zwolnienie zasobów