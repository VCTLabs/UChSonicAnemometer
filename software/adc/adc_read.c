/*
 * Program to read the data from ADC converter.
 * 
 * Input format from ADC122S706 is 16 bits: 4 zero bits + 12 data bits (2's
 * complement). Output to stdout format is signed 16 integer little endian.
 */
#include <stdio.h>
#include <stdlib.h>
#include <mpsse.h>

#define SAMPLES	10000
#define SIZE	2*SAMPLES			// Size of SPI flash device: 1MB
#define SPI_CLOCK 15000000

int main(void)
{
  char *data = (char *) malloc(SIZE);
  int retval = EXIT_FAILURE;
  struct mpsse_context *flash = NULL;

  if((flash = MPSSE(SPI0, SPI_CLOCK, MSB)) != NULL && flash->open)
  {
    fprintf(stderr, "OK %d\n", GetClock(flash));

    Start(flash);
    FastRead(flash, data, SIZE);
    Stop(flash);

    int i;
    for (i=0; i<SAMPLES; i++) {
      char left = data[2*i]; // first 8 bits from adc
      char right = data[2*i+1]; // last 8 bits from adc
      //signed extension
      if (left & (1<<3)) {
        left |= 0xf0;
      }
      //swap bytes
      data[2*i] = right;
      data[2*i+1] = left;
    }

    if(stdout)
    {
      fwrite(data, 1, SIZE, stdout);
      retval = EXIT_SUCCESS;
    } else {
      fprintf(stderr, "FAIL: Failed to open file\n");
    }
  }	else	{
    fprintf(stderr, "FAIL: Failed to initialize MPSSE: %s\n",
            ErrorString(flash));
  }

  free(data);
  Close(flash);

  return retval;
}
