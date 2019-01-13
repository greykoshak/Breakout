import pygame
import sys

from collections import defaultdict


class Game:
    """
    Source: https://habr.com/post/347138/
    Класс Game — это ядро игры. Он выполняется в основном цикле.
    """

    def __init__(self,
                 caption,
                 width,
                 height,
                 back_image_filename,
                 frame_rate):
        self.background_image = \
            pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    # Методы update() и draw() очень просты. Они обходят все управляемые игровые объекты и
    # вызывают соответствующие им методы. Если два объекта накладываются друг на друга на экране,
    # то порядок списка объектов определяет, какой из них будет рендериться первым, а остальные
    # будут частично или полностью его перекрывать.
    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    # Метод handle_events() слушает события, генерируемые Pygame, такие как события клавиш и мыши.
    # Для каждого события он вызывает все функции-обработчики, которые должны обрабатывать события
    # соответствующих типов.
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    # run() выполняет основной цикл. Он выполняется до тех пор, пока элемент game_over не принимает
    # значение True. В каждой итерации он рендерит фоновое изображение и вызывает по порядку методы
    # handle_events(), update() и draw().
    # Затем он обновляет экран, то есть записывает на физический дисплей всё содержимое, которое было
    # отрендерено на текущей итерации. И последнее, но не менее важное — он вызывает метод clock.tick()
    # для управления тем, когда будет вызвана следующая итерация.
    def run(self):
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
