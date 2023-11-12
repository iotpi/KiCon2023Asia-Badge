#include "sk6812.h"

#define SEQUENCE 1

uint8_t sk6812_rgbs[SK_COUNT][SEQLEN][3] =
    {
#if (SEQUENCE == 0)
        {
            // SAO1 GPIO1
            {255, 255, 0},
            {0, 255, 0},
            {0, 0, 255},
            {255, 0, 0},
            {255, 255, 0},
            {0, 255, 0},
            {0, 0, 255},
            {255, 0, 0},
            {0, 0, 255},
            {255, 0, 0},
        },
        {
            // SAO2 GPIO1
            {255, 255, 0},
            {0, 255, 0},
            {0, 0, 255},
            {255, 0, 0},
            {255, 255, 0},
            {0, 255, 0},
            {0, 0, 255},
            {255, 0, 0},
            {0, 0, 255},
            {255, 0, 0},
        },
#elif (SEQUENCE == 1)
        {
            // SAO1 GPIO1
            {255, 0, 255},
            {255, 0, 200},
            {255, 0, 155},
            {255, 0, 100},
            {255, 0, 55},
            {255, 0, 35},
            {255, 0, 25},
            {255, 0, 15},
            {255, 0, 10},
            {255, 0, 5},
        },
        {
            // SAO2 GPIO1
            {255, 255, 255},
            {255, 255, 255},
            {255, 255, 255},
            {255, 255, 255},
            {255, 255, 255},
            {255, 255, 255},
            {255, 255, 255},
            {255, 255, 255},
            {255, 255, 255},
            {255, 255, 255},
        },
#endif
    };

#ifdef LED_SAO_USE_DMA
uint16_t sk6812_data[PATTERN_LEN][COUNT] = {};
#endif