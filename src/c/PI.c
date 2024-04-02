#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>
#include "../../include/PI.h"

void initialize_PI(PI_t *pi)
{
    pi->K = 2.2;
    pi->Ti = 0.0;
    pi->Tr = 10.0;
    pi->Beta = 1.0;
    pi->H = 0.1;
    pi->integratorOn = false;
    pi->I = 0.0;
    pi->v = 0.0;
    pi->e = 0.0;
    pthread_mutex_init(&(pi->mutex), NULL); // free this memory!
}

void destroy_PI(PI_t *pi)
{
    pthread_mutex_destroy(&(pi->mutex));
}

double calculateOutput(PI_t *pi, double y, double yref)
{
    pthread_mutex_lock(&(pi->mutex));
    pi->e = yref - y;
    pi->v = pi->K * (pi->Beta * yref - y) + pi->I;
    double v = pi->v;
    pthread_mutex_unlock(&(pi->mutex));
    return v;
}

void updateState(PI_t *pi, double u)
{
    pthread_mutex_lock(&(pi->mutex));
    if (pi->integratorOn)
    {
        pi->I = pi->I + pi->K * pi->H / pi->Ti * pi->e + pi->H / pi->Tr * (u - pi->v);
    }
    else
    {
        pi->I = 0.0;
    }
    pthread_mutex_unlock(&(pi->mutex));
}

long getHMillis(PI_t *pi)
{
    pthread_mutex_lock(&(pi->mutex));
    long h = (long)(pi->H * 1000.0);
    pthread_mutex_unlock(&(pi->mutex));
    return h;
}

void setParameters(PI_t *pi, double K, double Ti, double Tr, double Beta, double H, bool integratorOn)
{
    pthread_mutex_lock(&(pi->mutex));
    pi->K = K;
    pi->Ti = Ti;
    pi->Tr = Tr;
    pi->Beta = Beta;
    pi->H = H;
    pi->integratorOn = integratorOn;
    if (!pi->integratorOn)
    {
        pi->I = 0.0;
    }
    pthread_mutex_unlock(&(pi->mutex));
}

void reset(PI_t *pi)
{
    pthread_mutex_lock(&(pi->mutex));
    pi->I = 0.0;
    pthread_mutex_unlock(&(pi->mutex));
}

// Is getParameters() needed here?