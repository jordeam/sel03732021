/* Can para o ESP32 do sensor
    Esse codigo instala e inicializa o driver can para a ESP32 central
    espera o pedido de leitura via interfase 
     e realiza a leitura e manda a resposta
*/
#include <stdio.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_err.h"
#include "esp_log.h"
#include "driver/can.h"
#include "driver/gpio.h"
#include "sdkconfig.h"
#include "driver/timer.h"
#include "soc/timer_group_struct.h"
#include "driver/periph_ctrl.h"
#include "driver/timer.h"
#include <inttypes.h>

#define MSG_ID                 0x000
#define TIMER_DIVIDER         (16)  
#define TIMER_SCALE           (TIMER_BASE_CLK / TIMER_DIVIDER) 
#define PIN_TRIGGER           GPIO_NUM_19
#define PIN_ECHO              GPIO_NUM_18
#define PIN_ATIVO             GPIO_NUM_26
#define PIN_TROCA_TAMBOR      GPIO_NUM_25

static double volume_tambor = 200.00000;
static double area_superficial = 222;
static double altura = 30.4;
static xQueueHandle gpio_evt_queue = NULL;
static int medir=0;



void interrupcao_troca_tambor(void);

static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    uint32_t gpio_num = (uint32_t) arg;
    xQueueSendFromISR(gpio_evt_queue, &gpio_num, NULL);
    vTaskDelay(0.5);
}

static void gpio_task_example(void* arg)
{
    uint32_t io_num;
    
    for(;;) {
        if(xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY)) {
            if (io_num == 26)
            {
                medir = 1;
                
            }if(io_num == 25){
                interrupcao_troca_tambor();
            }
                        
        }
    }
}

static void driver_install(void)
{
    //configuração de inicialização da interfase can
    can_general_config_t g_config = CAN_GENERAL_CONFIG_DEFAULT(GPIO_NUM_21, GPIO_NUM_22, CAN_MODE_NORMAL);
    can_timing_config_t t_config = CAN_TIMING_CONFIG_500KBITS();
    can_filter_config_t f_config = CAN_FILTER_CONFIG_ACCEPT_ALL();

    //instalação do driver can driver foi corretamente instalado
    //instala e ferica se o
    if (can_driver_install(&g_config, &t_config, &f_config) == ESP_OK) {
        printf("Driver instalado\n");
    } else {
        printf("falha na instalação do driver\n");
        return;
    }

    //inicializa o driver
    if (can_start() == ESP_OK) {
        printf("driver inicializado\n");
    } else {
        printf("falha na inicialização do driver\n");
        return;
    }

    //configuração de alertas de erro
    uint32_t alerts_to_enable = CAN_ALERT_ERR_PASS | CAN_ALERT_BUS_OFF;
    if (can_reconfigure_alerts(alerts_to_enable, NULL) == ESP_OK) {
        printf("Alertas reconfigurados\n");
    } else {
     printf("falha na reconfiguração dos alertas");
    }
}

static void reciveremote_transmite(void)
{
    can_message_t message;
    if (can_receive(&message, pdMS_TO_TICKS(1000)) == ESP_OK) {
        //mandar mensagem
        can_message_t message1;
        message1.identifier = 0x0000;
        message1.flags = CAN_MSG_FLAG_EXTD;
        message1.data_length_code = sizeof(1);
        message1.data[0] = volume_tambor;

        //COloca a mensagem na fila de transmição 
        if (can_transmit(&message1, pdMS_TO_TICKS(1000)) == ESP_OK) {
            printf("Message queued for transmission\n");
        } else {
            printf("Failed to queue message for transmission\n");
        }
    } 
    else {
        printf("Failed to receive message\n");
        return;
    }
}

double mesure(void)
{
    
    timer_config_t config = {
        .divider = TIMER_DIVIDER,
        .counter_dir = TIMER_COUNT_UP,
        .counter_en = TIMER_PAUSE,
        .auto_reload = 0,
    }; 
    timer_init(TIMER_GROUP_0, 0, &config);
    //valor de iniciação do timer
    timer_set_counter_value(TIMER_GROUP_0, 0, 0x00000000ULL);

    double a = 0;
    double *b = &a;
    double saida = 0;

    //colocar trigger em 1 por 10us
    gpio_set_level(PIN_TRIGGER, 1);
    vTaskDelay(0.01);
    gpio_set_level(PIN_TRIGGER, 0);
    while (gpio_get_level(PIN_ECHO) == 0)
    {}
    timer_start(TIMER_GROUP_0, 0);
    int d = gpio_get_level(PIN_ECHO);
    //printf("Level: %d \n", d);
     while(d == 1)
     {
         timer_get_counter_time_sec(TIMER_GROUP_0, 0, b); 
         d = gpio_get_level(PIN_ECHO);
     }
    timer_pause(TIMER_GROUP_0, 0);
    saida = (a*340*100)/2;
    printf("saida = %2.5lf"    "\n", saida);
    return saida;
}



double ajuste_tambor(double a)
{
    volume_tambor = volume_tambor - ((altura-a)*area_superficial)/1000;
    printf("Volume: %2.5lf \n", volume_tambor);
    return volume_tambor;
}

void interrupcao_troca_tambor(void)
{
    printf("Tambor Novo\n");
    volume_tambor = 200.0000;
}


void  inicia_pinos(void)
{
    gpio_config_t i_conf;
    i_conf.intr_type = GPIO_PIN_INTR_POSEDGE;
    i_conf.mode = GPIO_MODE_INPUT;
    i_conf.pin_bit_mask = (1ULL<<PIN_TROCA_TAMBOR);
    i_conf.pull_down_en = 0;
    i_conf.pull_up_en = 1;
    gpio_config(&i_conf);

    gpio_config_t i_conf1;
    i_conf1.intr_type = GPIO_PIN_INTR_POSEDGE;
    i_conf1.mode = GPIO_MODE_INPUT;
    i_conf1.pin_bit_mask = (1ULL<<PIN_ATIVO);
    i_conf1.pull_down_en = 0;
    i_conf1.pull_up_en = 1;
    gpio_config(&i_conf1);

    gpio_set_intr_type(PIN_ATIVO, GPIO_INTR_ANYEDGE);
    gpio_set_intr_type(PIN_TROCA_TAMBOR, GPIO_INTR_ANYEDGE);
    gpio_evt_queue = xQueueCreate(10, sizeof(uint32_t));
    xTaskCreate(gpio_task_example, "gpio_task_example", 2048, NULL, 10, NULL);

    gpio_install_isr_service(0);
    gpio_isr_handler_add(PIN_ATIVO, gpio_isr_handler, (void*) PIN_ATIVO);
    gpio_isr_handler_add(PIN_TROCA_TAMBOR, gpio_isr_handler, (void*) PIN_TROCA_TAMBOR);

    gpio_config_t o_conf;
    o_conf.intr_type = GPIO_PIN_INTR_DISABLE;
    o_conf.mode = GPIO_MODE_OUTPUT;
    o_conf.pin_bit_mask = (1ULL<<19);
    o_conf.pull_down_en = 0;
    o_conf.pull_up_en = 0;
    gpio_config(&o_conf);

    gpio_config_t i_conf2;
    i_conf2.intr_type = GPIO_PIN_INTR_DISABLE;
    i_conf2.mode = GPIO_MODE_INPUT;
    i_conf2.pin_bit_mask = (1ULL<<21);
    i_conf2.pull_down_en = 0;
    i_conf2.pull_up_en = 0;
    gpio_config(&i_conf2);
}


void app_main(void)
{
    static double a=0;
    inicia_pinos();
    driver_install();
    while (1)
    {
        reciveremote_transmite();
        if (medir == 1)
        {
            while(gpio_get_level(PIN_ATIVO) == 1)
            {}
            a = mesure();
            ajuste_tambor(a);
            medir=0;
            driver_install();
        }
        
    }  
}