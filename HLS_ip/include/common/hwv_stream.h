/**
 *	Stream class of Hardware Vision project
 */

#ifndef HWV_STREAM_H
#define HWV_STREAM_H

#include <ap_int.h>
#include "hwv_class.h"

// to csim
#define HWV_RGB_MODE 24
#define HWV_GRAY_MODE 8
// end to csim

namespace hwv
{
template <int bits>
struct axi_dma_stream
{
	ap_uint<bits> data;
	ap_uint<1> user;
	ap_uint<1> last;
};

// Saves stream data to Matrix
template<int bits, class SRC_T, int HEIGHT, int WIDTH>
void stream2Mat(axi_dma_stream<bits> *src, Matrix<SRC_T, HEIGHT, WIDTH> &dst)
{
#pragma HLS INLINE OFF

	for (int y = 0; y < HEIGHT; y++)
	{
		for (int x = 0; x < WIDTH; x++)
		{
//#pragma HLS PIPELINE II=1
//#pragma HLS LOOP_FLATTEN OFF

			dst.write(y, x, src[x + y*WIDTH].data);
		}
	}
}

// Converts Matrix to stream
template<class SRC_T, int HEIGHT, int WIDTH, int bits>
void Mat2stream(Matrix<SRC_T, HEIGHT, WIDTH> &src, axi_dma_stream<bits> *dst)
{
#pragma HLS INLINE OFF

	for (int y = 0; y < HEIGHT; y++)
	{
		for (int x = 0; x < WIDTH; x++)
		{
#pragma HLS PIPELINE II=1
#pragma HLS LOOP_FLATTEN off
			dst[x + y*WIDTH].data = src.read(y,x);
			dst[x + y*WIDTH].user = (y == 0 && x == 0) ? 1:0;
			dst[x + y*WIDTH].last = (y == HEIGHT-1 && x == WIDTH-1) ? 1:0;
		}
	}
}

// use the stream class on the testbench
template<int TYPE, int HEIGHT, int WIDTH>
class Stream
{
private:
	int CHANNELS;

public:

	// variables
#ifndef __SYNTHESIS__
	axi_dma_stream<TYPE> *data;
#else 
	axi_dma_stream<TYPE> data[HEIGHT * WIDTH];
#endif
// methods
Stream()
{
#ifndef __SYNTHESIS__
	// memory allocation
	data = (axi_dma_stream<TYPE> *)malloc(HEIGHT * WIDTH * sizeof(axi_dma_stream<TYPE>));
#endif
	CHANNELS = TYPE >> 3;
}

~Stream()
{
#ifndef __SYNTHESIS__
	free(data);
#endif
}

void cv2axis(void *_src)
{
	ap_uint<8> *src = (ap_uint<8> *)_src;

	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
			ap_uint<8> *color = &src[CHANNELS*(i*WIDTH + j)];

			int dat = 0;

			for (int k = 0; k < CHANNELS; k++)
			{
				int intensity = color[k];
				dat += intensity << (k << 3);
			}

			data[i*WIDTH + j].data = dat;
		}
	}
}

void axis2cv(void *_dst)
{
	ap_uint<8> *dst = (ap_uint<8> *)_dst;

	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
			int dat = data[i*WIDTH + j].data;

			for (int k = 0; k < CHANNELS; k++)
			{
				int conversor = 0x0000ff << (k << 3);
				dst[CHANNELS*(i*WIDTH + j) + k] = (dat & conversor) >> (k << 3);
			}
		}
	}
} 	

};

} // namespace hwv

#endif // HWV_STREAM_H
