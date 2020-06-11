/**
 * top file
 */

#include "top.h"

void Hough_Module(GRAY_IMAGE &edge_mat_src, int lines_thr, int gap_size, int min_length,
		float *out_rho, float *out_theta, int lines_segments[MAX_SEGMENTS][4],
		int *num_of_lines, int *num_of_segments)
{
#pragma HLS INLINE OFF

	hwv::Polar<float, float, MAX_LINES, int> lines;
	hwv::Cartesian<int, MAX_SEGMENTS, int> segments;

	hwv::HoughLines<1,2>(edge_mat_src, lines, segments, lines_thr, gap_size, min_length);
	// Zedboard doesn't support thetastep = 1

	// Stores the lines [rho, theta] in out_rho and out_theta
	// and the segments [x1,y1,x2,y2] in lines_segments.

	for (int i = 0; i < MAX_LINES; i++)
	{
		out_rho[i] = lines.rho[i];
		out_theta[i] = lines.theta[i];
	}

	for (int i = 0; i < MAX_SEGMENTS; i++)
	{
		lines_segments[i][0] = segments.x_begin[i];
		lines_segments[i][1] = segments.y_begin[i];
		lines_segments[i][2] = segments.x_end[i];
		lines_segments[i][3] = segments.y_end[i];
	}

	// After all the computations, store the number of detected lines and
	// segments on memory. On PYNQ, initialize num_of_segments with -1
	// (or any negative number) and stop the computation when it's not -1.
	num_of_lines[0] = lines.size;
	num_of_segments[0] = segments.size;
}

void hough_accel(RGB_STREAM *image_in, RGB_STREAM *edges,
				float out_rho[MAX_LINES], float out_theta[MAX_LINES], int num_of_lines[1],
				int lines_segments[MAX_SEGMENTS][4], int num_of_segments[1],
				int edges_lthr, int edges_hthr, int lines_thr,
				int gap_size, int min_length)
{
#pragma HLS INTERFACE axis depth=307200 port=image_in bundle=NEW_FRAME
#pragma HLS INTERFACE axis depth=307200 port=edges bundle=EDGES

#pragma HLS INTERFACE m_axi port=out_rho offset=slave bundle=LINES
#pragma HLS INTERFACE m_axi port=out_theta offset=slave bundle=LINES
#pragma HLS INTERFACE m_axi port=num_of_lines offset=slave bundle=LINES
#pragma HLS INTERFACE m_axi port=lines_segments offset=slave bundle=LINES
#pragma HLS INTERFACE m_axi port=num_of_segments offset=slave bundle=LINES

#pragma HLS INTERFACE s_axilite port=edges_lthr bundle=CTRL
#pragma HLS INTERFACE s_axilite port=edges_hthr bundle=CTRL
#pragma HLS INTERFACE s_axilite port=lines_thr bundle=CTRL
#pragma HLS INTERFACE s_axilite port=gap_size bundle=CTRL
#pragma HLS INTERFACE s_axilite port=min_length bundle=CTRL
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

	//Runs the Line and Segment Extraction Module
	Hough_Module(edge_mat_src, lines_thr, gap_size, min_length,
			out_rho, out_theta, lines_segments, num_of_lines, num_of_segments);

	hwv::Gray2Color(edge_mat_write, edge_rgb);
	hwv::Mat2stream(edge_rgb, edges);
}
