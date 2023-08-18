#ifndef MD5_H
#define MD5_H

#include <stddef.h>
#include <stdint.h>

uint8_t *md5(const char *message, size_t length);

#endif
