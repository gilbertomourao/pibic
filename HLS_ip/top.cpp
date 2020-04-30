/**
 * top file
 */

#include "top.h"

void hough_accel(RGB_STREAM *image_in, RGB_STREAM *edges,
				float *out_rho, float *out_theta,
				int edges_lthr, int edges_hthr, int lines_thr)
{
#pragma HLS INTERFACE axis depth=307200 port=image_in bundle=NEW_FRAME
#pragma HLS INTERFACE axis depth=307200 port=edges bundle=EDGES
#pragma HLS INTERFACE m_axi depth=30 port=out_rho offset=slave bundle=LINES
#pragma HLS INTERFACE m_axi depth=30 port=out_theta offset=slave bundle=LINES
#pragma HLS INTERFACE s_axilite port=edges_lthr bundle=CTRL
#pragma HLS INTERFACE s_axilite port=edges_hthr bundle=CTRL
#pragma HLS INTERFACE s_axilite port=lines_thr bundle=CTRL
#pragma HLS INTERFACE s_axilite port=return bundle=CTRL

	RGB_IMAGE rgb_src_mat;
	GRAY_IMAGE gray_src_mat;
	GRAY_IMAGE edge_mat;
	GRAY_IMAGE edge_mat_src;
	GRAY_IMAGE edge_mat_write;
	RGB_IMAGE edge_rgb;

#pragma HLS DATAFLOW

	hwv::stream2Mat(image_in, rgb_src_mat);
	hwv::Color2Gray(rgb_src_mat, gray_src_mat);
	hwv::CannyEdge(gray_src_mat, edge_mat, edges_lthr, edges_hthr);
	hwv::Duplicate(edge_mat, edge_mat_src, edge_mat_write);

	hwv::Polar<float, float> lines[MAX_LINES];

	hwv::HoughLines<1,2>(edge_mat_src, lines, lines_thr);
	// Zedboard doesn't support thetastep = 1

	for (int i = 0; i < MAX_LINES; i++)
	{
#pragma HLS UNROLL
		out_rho[i] = lines[i].rho;
		out_theta[i] = lines[i].theta;
	}

	hwv::Gray2Color(edge_mat_write, edge_rgb);
	hwv::Mat2stream(edge_rgb, edges);
}
