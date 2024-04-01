#ifndef PI_H
#define PI_H

#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>

//use key 'I' when accessing shared memory
typedef struct PI_t;
void initialize_PI(PI_t *pi);
void destroy_PI(PI_t *pi);
double calculateOutput(PI_t *pi, double y, double yref);
void updateState(PI_t *pi, double u);
long getHMillis(PI_t *pi);
void setParameters(PI_t *pi, double K, double Ti, double Tr, double Beta, double H, bool integratorOn);
void reset(PI_t *pi);

#endif