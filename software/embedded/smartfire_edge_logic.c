#include "smartfire_edge_logic.h"
static uint8_t previous_level;
void SmartfireEdge_Init(void) { previous_level = 0U; }
SmartfireEdgeOutput SmartfireEdge_Evaluate(const SmartfireEdgeInput *in)
{
    SmartfireEdgeOutput out = {0U, 0U, 0U, 0U};
    uint16_t score = 0U;
    if (in == 0) { out.risk_level = 3U; out.score = 100U; out.event_changed = 1U; return out; }
    if (in->object_temp_valid) {
        out.evidence_count++;
        if (in->object_temp_c >= 60.0f) score += 45U;
        else if (in->object_temp_c >= 50.0f) score += 30U;
        else if (in->object_temp_c >= 40.0f) score += 12U;
    }
    if (in->ambient_temp_valid) {
        out.evidence_count++;
        if (in->ambient_temp_c >= 60.0f) score += 40U;
        else if (in->ambient_temp_c >= 45.0f) score += 25U;
        else if (in->ambient_temp_c >= 38.0f) score += 10U;
    }
    if (in->co2_valid) {
        out.evidence_count++;
        if (in->co2_ppm >= 3000U) score += 35U;
        else if (in->co2_ppm >= 1500U) score += 22U;
        else if (in->co2_ppm >= 1000U) score += 8U;
    }
    if (in->mq2_valid) {
        out.evidence_count++;
        if (in->mq2_raw >= 1600U) score += 25U;
        else if (in->mq2_raw >= 1200U) score += 15U;
    }
    if (in->object_temp_valid && in->co2_valid &&
        in->object_temp_c >= 40.0f && in->co2_ppm >= 1000U) score += 15U;
    if (in->ambient_temp_valid && in->mq2_valid &&
        in->ambient_temp_c >= 38.0f && in->mq2_raw >= 1000U) score += 10U;
    if (score > 100U) score = 100U;
    out.score = score;
    out.risk_level = (score >= 70U) ? 3U : (score >= 45U) ? 2U : (score >= 20U) ? 1U : 0U;
    out.event_changed = (out.risk_level != previous_level) ? 1U : 0U;
    previous_level = out.risk_level;
    return out;
}
