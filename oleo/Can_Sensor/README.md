main_sensor.c
Código que deve ser inserido na ESP-32 WROOM que contém o sensor para a medida do nível de óleo do tambor


Funcionalidades
* Interrupção para iniciar a medida do óleo.
* interrupção para indicar que houve a troca do tambor de óleo.
* Fazer a conversão da medida em distância para volume e subtrair o volume retirado do volume atual de óleo no tambor.
* Esperar a ESP-32 WROOM com acesso ao site pedir o nível atual do óleo pela interface CAN.
* Ao receber um pedido pela interface CAN enviar pela interface o nivel de oleo