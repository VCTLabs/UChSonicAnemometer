LDFLAGS=-lmpsse

all: adc_read

adc_read: adc_read.c
	$(CC) $(CFLAGS) adc_read.c -o adc_read $(LDFLAGS)

clean:
	rm -f *.dSYM
	rm -f  adc_read

distclean: clean
