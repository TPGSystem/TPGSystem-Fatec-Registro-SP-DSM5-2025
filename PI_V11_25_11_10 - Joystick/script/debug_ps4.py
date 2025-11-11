import pygame
import time

# =======================
# Configurações de Debug
# =======================
DEADZONE = 0.15       # variação mínima para logar movimento de eixo
THROTTLE = 0.05       # seg. mínimos entre logs do MESMO eixo
PRINT_RAW_ANALOG = False  # True para sempre imprimir axis (mesmo com deadzone/limite)

pygame.init()
pygame.joystick.init()
pygame.display.set_caption("Debug Joystick (ESC para sair)")
screen = pygame.display.set_mode((540, 180))  # janela simples só p/ receber QUIT/ESC
font = pygame.font.SysFont(None, 22)

last_axis_log_time = {}
last_axis_value = {}

def textline(surface, txt, y, color=(220,220,220)):
    img = font.render(txt, True, color)
    surface.blit(img, (10, y))

def attach(index):
    try:
        js = pygame.joystick.Joystick(index)
        js.init()
        name = js.get_name()
        print(f"\n[ATTACH] idx={index} name={name}")
        print(f"  instance_id={js.get_instance_id()} buttons={js.get_numbuttons()} axes={js.get_numaxes()} hats={js.get_numhats()}")
        return js
    except Exception as e:
        print(f"[ATTACH] Falha ao inicializar joystick {index}: {e}")
        return None

def detach(js):
    if not js:
        return
    try:
        print(f"[DETACH] name={js.get_name()} instance_id={js.get_instance_id()}")
        js.quit()
    except Exception:
        pass

# Conecta o primeiro disponível (se existir)
joystick = attach(0) if pygame.joystick.get_count() > 0 else None
if not joystick:
    print("[INFO] Nenhum controle detectado no início. Conecte um controle...")

running = True
clock = pygame.time.Clock()

while running:
    # UI: desenha cabeçalho
    screen.fill((30, 30, 30))
    textline(screen, "Debug Joystick — ESC: sair | Conecte/desconecte p/ testar hotplug", 10)
    if joystick:
        textline(screen, f"Conectado: {joystick.get_name()} | id={joystick.get_instance_id()} | "
                         f"btns={joystick.get_numbuttons()} axes={joystick.get_numaxes()} hats={joystick.get_numhats()}", 40, (180,255,180))
    else:
        textline(screen, "Nenhum controle conectado.", 40, (255,180,180))
    pygame.display.flip()

    now = time.time()

    for event in pygame.event.get():
        # Fechar janela ou ESC
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # Hotplug
        if event.type == pygame.JOYDEVICEADDED:
            # Se não há joystick atual, conecta o que chegou
            if joystick is None:
                joystick = attach(event.device_index)
            else:
                # Apenas informa (multi-joysticks). Você pode trocar a lógica se quiser.
                print(f"[HOTPLUG] Outro device adicionado: idx={event.device_index}")
            continue

        if event.type == pygame.JOYDEVICEREMOVED:
            # Se o removido é o atual, detach
            if joystick and event.instance_id == joystick.get_instance_id():
                detach(joystick)
                joystick = None
            else:
                print(f"[HOTPLUG] Device removido (não era o atual): instance_id={event.instance_id}")
            continue

        # Se não há joystick, ignore o resto
        if joystick is None:
            continue

        # Botões
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"[PRESS]  button={event.button}")
        elif event.type == pygame.JOYBUTTONUP:
            print(f"[RELEASE] button={event.button}")

        # D-Pad (HAT)
        elif event.type == pygame.JOYHATMOTION:
            x, y = event.value  # (-1,0,1)
            dir_txt = []
            if y == 1:  dir_txt.append("UP")
            if y == -1: dir_txt.append("DOWN")
            if x == -1: dir_txt.append("LEFT")
            if x == 1:  dir_txt.append("RIGHT")
            if not dir_txt: dir_txt = ["CENTER"]
            print(f"[HAT] {event.value} -> {'+'.join(dir_txt)}")

        # Analógicos
        elif event.type == pygame.JOYAXISMOTION:
            axis = event.axis
            val = float(event.value)
            if PRINT_RAW_ANALOG:
                print(f"[AXIS {axis}] = {val:.3f}")
            else:
                # Só imprime quando passa da deadzone e com ‘throttle’ por eixo
                if abs(val) >= DEADZONE:
                    t_last = last_axis_log_time.get(axis, 0.0)
                    if now - t_last >= THROTTLE:
                        print(f"[AXIS {axis}] = {val:+.3f}")
                        last_axis_log_time[axis] = now
                else:
                    # Se saiu da zona, imprime retorno ao centro apenas uma vez
                    prev = last_axis_value.get(axis, 0.0)
                    if abs(prev) >= DEADZONE and abs(val) < DEADZONE:
                        print(f"[AXIS {axis}] -> CENTER")
            last_axis_value[event.axis] = val

    clock.tick(120)

# Encerramento
detach(joystick)
pygame.quit()
