import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Nenhum controle detectado!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Controle detectado: {joystick.get_name()}")
print(f"Botões: {joystick.get_numbuttons()}")
print(f"Eixos: {joystick.get_numaxes()}")
print(f"Hats: {joystick.get_numhats()}")

# Guardar último valor dos eixos p/ comparar
last_axis = [0.0] * joystick.get_numaxes()
deadzone = 0.2  # limite mínimo para ignorar ruído

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.JOYBUTTONDOWN:
            print(f"[PRESS] Botão {event.button}")

        if event.type == pygame.JOYBUTTONUP:
            print(f"[RELEASE] Botão {event.button}")

        if event.type == pygame.JOYHATMOTION:
            print(f"[HAT] {event.value}")

        if event.type == pygame.JOYAXISMOTION:
            axis = event.axis
            value = round(event.value, 2)
            if abs(value - last_axis[axis]) > deadzone:
                print(f"[AXIS {axis}] = {value}")
                last_axis[axis] = value