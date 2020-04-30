/**
 * configuration file
 */

#include <hwv_library.h>

#define IMG_HEIGHT 480
#define IMG_WIDTH 640

#define MAX_LINES 100

// stream
typedef hwv::axi_dma_stream<24> RGB_STREAM;
//typedef hwv::axi_dma_stream<8> GRAY_STREAM;

// matrix
typedef hwv::Matrix<ap_uint<24>, IMG_HEIGHT, IMG_WIDTH> RGB_IMAGE;
typedef hwv::Matrix<ap_uint<8>, IMG_HEIGHT, IMG_WIDTH> GRAY_IMAGE;

void hough_accel(RGB_STREAM *image_in, RGB_STREAM *edges,
				float *out_rho, float *out_theta,
				int edges_lthr, int edges_hthr, int lines_thr);
