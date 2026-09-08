# ControlCaídas

Prototipo visual de una app de detección de caídas y desmayos para personas mayores
que viven solas, pensada para que hijos/cuidadores monitoreen la casa desde el móvil.

El hardware objetivo es un ESP32 + sensor mmWave LD2450 (aún no disponible), así que
este prototipo trabaja con **datos simulados** para poder diseñar y validar toda la
experiencia de usuario antes de integrar el hardware real.

## Concepto

- Cada **familia** tiene una cuenta con su **casa**, sus **sensores** (uno por
  habitación) y sus **cuidadores**, al estilo Life360.
- El sensor solo importa si detecta o no una posible caída — no identifica a la
  persona.
- Cuando se detecta una posible caída, todos los cuidadores reciben una alerta a
  pantalla completa con opción de confirmar, descartar o pedir ayuda, con un
  escalado automático al siguiente contacto si nadie responde a tiempo.

## Stack

- React + TypeScript + Vite
- Tailwind CSS v4 (tema de marca azul + estados de seguridad: verde/ámbar/rojo)
- React Router
- Estado en memoria (Context) con datos mock — sin backend todavía

## Desarrollo

```bash
npm install
npm run dev
```

Hay un botón flotante "modo demo" en la esquina inferior derecha para simular una
caída en cualquier habitación sin necesidad del hardware.

## Pantallas

- **Inicio**: estado general de la casa y de cada habitación/sensor.
- **Alerta**: pantalla completa roja al detectarse una posible caída, con
  cuenta regresiva de escalado.
- **Historial**: eventos pasados (caídas confirmadas, falsas alarmas, etc.).
- **Sensores**: gestión de dispositivos ESP32 + LD2450 por habitación.
- **Familia**: círculo de cuidadores y orden de aviso ante una alerta.
- **Ajustes**: sensibilidad de detección, notificaciones, modo no molestar.
