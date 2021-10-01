main_wifi.c
Codigo que deve ser inserido na ESP-32 WROOM que se comunica com o site


Funcionalidades
* Enviar dado remoto pela interface CAN para pedir o dado do sensor.
* Receber o dado pedido pela interface CAN.
* Enviar o dado para o site.


Configurações
* Incluir e-mail e senha nos campos username e password respectivamente, na função static void http_rest_with_url(void) em esp_http_client_config_t config.
* No arquivo sdkconfig nos campos CONFIG_EXAMPLE_WIFI_SSID e CONFIG_EXAMPLE_WIFI_PASSWORD colocar nome e senha do wi-fi local respectivamente.