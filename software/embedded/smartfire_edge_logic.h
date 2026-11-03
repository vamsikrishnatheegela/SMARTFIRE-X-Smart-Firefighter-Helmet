#ifndef SMARTFIRE_EDGE_LOGIC_H
#define SMARTFIRE_EDGE_LOGIC_H
#include <stdint.h>
typedef struct {
    float object_temp_c;
    float ambient_temp_c;
    uint16_t co2_ppm;
    uint16_t mq2_raw;
    uint8_t object_temp_valid;
    uint8_t ambient_temp_valid;
    uint8_t co2_valid;
    uint8_t mq2_valid;
} SmartfireEdgeInput;
typedef struct {
    uint8_t risk_level;       /* 0 normal, 1 watch, 2 high, 3 critical */
    uint8_t event_changed;    /* 1 when state changes or event is triggered */
    uint8_t evidence_count;   /* number of valid channels, 0..4 */
    uint16_t score;           /* prototype score, capped at 100 */
} SmartfireEdgeOutput;
void SmartfireEdge_Init(void);
SmartfireEdgeOutput SmartfireEdge_Evaluate(const SmartfireEdgeInput *in);
#endif


/*
 * INTERFACE NOTES
 * ---------------
 * Validity flags indicate whether each sensor channel contains a usable
 * reading. A numeric zero is therefore not used to represent missing data.
 * risk_level encoding: 0 = NORMAL, 1 = GUARDED, 2 = HIGH, 3 = CRITICAL.
 * score is a prototype rule score, not a probability or calibrated confidence.
 * Keep this header synchronized with smartfire_edge_logic.c.
 */
