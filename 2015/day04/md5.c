#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// #define F(x,y,z) (z ^ (x & (y ^ z)))
// #define G(x,y,z) (y ^ (z & (y ^ x)))

#define F(X,Y,Z) ((X & Y) | (~X & Z))
#define G(X,Y,Z) ((X & Z) | (Y & ~Z))
#define H(X,Y,Z) (X ^ Y ^ Z)
#define I(X,Y,Z) (Y ^ (X | ~Z))

static const int S[64] = {
    7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
    5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
    4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
    6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
};

static const uint32_t K[64] = {
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
};

static const size_t W[64] = {
     0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
     1,  6, 11,  0,  5, 10, 15,  4,  9, 14,  3,  8, 13,  2,  7, 12,
     5,  8, 11, 14,  1,  4,  7, 10, 13,  0,  3,  6,  9, 12, 15,  2,
     0,  7, 14,  5, 12,  3, 10,  1,  8, 15,  6, 13,  4, 11,  2,  9
};

static inline uint32_t rotateLeft(uint32_t x, int n){
	return (x << n) | (x >> (32 - n));
}

unsigned char *md5(const char *message, size_t length) {
    uint32_t A = 0x67452301;
    uint32_t B = 0xefcdab89;
    uint32_t C = 0x98badcfe;
    uint32_t D = 0x10325476;

    uint32_t w[64] = {0};
    
    memcpy(w, message, length);

    ((uint8_t *)w)[length] = 0x80;

    // append length
    ((uint64_t *)w)[7] = (uint64_t)length * 8;

    {
        uint32_t a = A;
        uint32_t b = B;
        uint32_t c = C;
        uint32_t d = D;

        for (size_t i=0; i < 64; ++i) {
            uint32_t e = a + K[i] + w[W[i]];

            if (i < 16) {
                e += F(b, c, d);
            } else if (i < 32) {
                e += G(b, c, d);
            } else if (i < 48) {
                e += H(b, c, d);
            } else {
                e += I(b, c, d);
            }

            a = d;
            d = c;
            c = b;
            b += rotateLeft(e, S[i]);
        }

        A += a;
        B += b;
        C += c;
        D += d;
    }

    uint32_t *digest = malloc(4 * sizeof *digest);
    digest[0] = A;
    digest[1] = B;
    digest[2] = C;
    digest[3] = D;

    return (uint8_t *)digest;
}
