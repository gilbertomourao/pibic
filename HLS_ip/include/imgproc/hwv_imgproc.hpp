/**
 *
 */

#ifndef HWV_IMG_PROC_HPP
#define HWV_IMG_PROC_HPP

#include "common/hwv_class.h"

#include <hls_video.h>

namespace hwv
{
	
// Converts rgb Matrix to gray Matrix
template<class SRC_T, int HEIGHT, int WIDTH, class DST_T>
void Color2Gray(Matrix<SRC_T, HEIGHT, WIDTH> &src, Matrix<DST_T, HEIGHT, WIDTH> &dst)
{
#pragma HLS INLINE OFF

	for (int y = 0; y < HEIGHT; y++)
	{
		for (int x = 0; x < WIDTH; x++)
		{
#pragma HLS PIPELINE II=1
#pragma HLS LOOP_FLATTEN OFF

			int pix_gray;
			ap_uint<24> dat = src.read(y, x);

			#pragma HLS RESOURCE variable=pix_gray core=AddSub

			// Y = B*0.144 + G*0.587 + R*0.299
			pix_gray = 9437 * (dat & 0x0000ff)
					 + 38469 * ( (dat & 0x00ff00) >> 8 )
					 + 19595 * ( (dat & 0xff0000) >> 16 );

			pix_gray >>= 16;
			
			// to consider saturation
			if (pix_gray > 255)
				pix_gray = 255;
			else if (pix_gray < 0)
				pix_gray = 0;
		
			// output
			dst.write(y, x, pix_gray);
		}
	}
}

// Converts gray Matrix to rgb Matrix
template<class SRC_T, int HEIGHT, int WIDTH, class DST_T>
void Gray2Color(Matrix<SRC_T, HEIGHT, WIDTH> &src, Matrix<DST_T, HEIGHT, WIDTH> &dst)
{
#pragma HLS INLINE OFF

	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
#pragma HLS PIPELINE II=1
#pragma HLS LOOP_FLATTEN OFF

			ap_uint<24> pix_gray = src.read(i,j);
			ap_uint<24> rgb_pix;

			// Gray --> (R, G, B)
			rgb_pix =   (pix_gray << 16) + 
						(pix_gray << 8) +
						(pix_gray);			

			// output			
			dst.write(i,j,rgb_pix);
		}
	}
}

template<class SRC_T, int HEIGHT, int WIDTH>
void Duplicate(Matrix<SRC_T, HEIGHT, WIDTH> &src, Matrix<SRC_T, HEIGHT, WIDTH> &dst1, Matrix<SRC_T, HEIGHT, WIDTH> &dst2)
{
	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
#pragma HLS PIPELINE II=1
#pragma HLS LOOP_FLATTEN OFF

			SRC_T dat = src.read(i,j);
			dst1.write(i,j,dat);
			dst2.write(i,j,dat);
		}
	}
}

template<class SRC_T, int HEIGHT, int WIDTH, int DST_T>
void hwv2hlsMat(Matrix<SRC_T, HEIGHT, WIDTH> &src, hls::Mat<HEIGHT, WIDTH, DST_T> &dst)
{
	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
			dst.write(hls::Scalar<1, unsigned char>(src.read(i,j)));
		}
	}
}

template<class SRC_T, int HEIGHT, int WIDTH, int DST_T>
void hls2hwvMat(hls::Mat<HEIGHT, WIDTH, DST_T> &src, Matrix<SRC_T, HEIGHT, WIDTH> &dst)
{
	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
			dst.write(i, j, src.read().val[0]);
		}
	}
}

} // namespace hwv

#endif // HWV_IMG_PROC_HPP
