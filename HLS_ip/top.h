/**
 * configuration file
 */

#include <hwv_library.h>

#define IMG_HEIGHT 480
#define IMG_WIDTH 640

#define MAX_LINES 100
#define MAX_SEGMENTS 200

// stream
typedef hwv::axi_dma_stream<24> RGB_STREAM;
//typedef hwv::axi_dma_stream<8> GRAY_STREAM;

// matrix
typedef hwv::Matrix<ap_uint<24>, IMG_HEIGHT, IMG_WIDTH> RGB_IMAGE;
typedef hwv::Matrix<ap_uint<8>, IMG_HEIGHT, IMG_WIDTH> GRAY_IMAGE;

void hough_accel(RGB_STREAM *image_in, RGB_STREAM *edges,
				float out_rho[MAX_LINES], float out_theta[MAX_LINES], int num_of_lines[1],
				int lines_segments[MAX_SEGMENTS][4], int num_of_segments[1],
				int edges_lthr, int edges_hthr, int lines_thr,
				int gap_size, int min_length);
