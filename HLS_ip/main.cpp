/**
 * testbench
 */

#include "top.h"
#include <hls_opencv.h>

#define IMAGE_PATH "C:/Users/chico/Documents/HLS/Zedboard/test_hough/data/usar/star.png"

void draw_lines(float *outrho, float *outtheta, int *num_of_lines, cv::Mat &edge_img, cv::Mat &orig_img)
{
	int wdtby2 = IMG_WIDTH/2;
	int heiby2 = IMG_HEIGHT/2;

	for (int i = 0; i < num_of_lines[0]; i++)
	{
		float rho = outrho[i], theta = outtheta[i];
		//printf("[%f][%f]\n", rho, theta);
		cv::Point pt1xi, pt2xi;
		double a = cos(theta), b = sin(theta);
		double x0 = a*rho, y0 = b*rho;
		pt1xi.x = cvRound(x0 + 1500*(-b) + (wdtby2));
		pt1xi.y = cvRound(y0 + 1500*(a) + (heiby2));
		pt2xi.x = cvRound(x0 - 1500*(-b) + (wdtby2));
		pt2xi.y = cvRound(y0 - 1500*(a) + (heiby2));
		cv::line(edge_img, pt1xi, pt2xi, cv::Scalar(0,0,255), 1, CV_AA);
		cv::line(orig_img, pt1xi, pt2xi, cv::Scalar(0,0,255), 1, CV_AA);
	}
}

void draw_segments(int segments[][4], int *num_of_segments, cv::Mat &img)
{
	for (int i = 0; i < *num_of_segments; i++)
	{
		cv::Point pt1xi, pt2xi;
		pt1xi.x = segments[i][0];
		pt1xi.y = segments[i][1];
		pt2xi.x = segments[i][2];
		pt2xi.y = segments[i][3];
		cv::line(img, pt1xi, pt2xi, cv::Scalar(0,255,0), 2, CV_AA);
		//cv::line(orig_img, pt1xi, pt2xi, cv::Scalar(0,0,255), 1, CV_AA);
	}
}

int main()
{
	cv::Mat src_img = cv::imread(IMAGE_PATH);

	hwv::Stream<HWV_RGB_MODE, IMG_HEIGHT, IMG_WIDTH> img_in;
	hwv::Stream<HWV_RGB_MODE, IMG_HEIGHT, IMG_WIDTH> img_edges;

	img_in.cv2axis(src_img.data);

	float outrho[MAX_LINES], outtheta[MAX_LINES];
	int num_of_lines[1];

	int segments[MAX_SEGMENTS][4];
	int num_of_segments[1];

	int edges_lthr = 20;
	int edges_hthr = 30;
	int lines_thr = 80;
	int gap_size = 5;
	int min_length = 50;

	hough_accel(img_in.data, img_edges.data,
			outrho, outtheta, num_of_lines,
			segments, num_of_segments,
			edges_lthr, edges_hthr, lines_thr,
			gap_size, min_length);

	/*
	for (int r = 0; r < MAX_LINES; r++)
	{
		printf("[%f, %f]\n", outrho[r], outtheta[r]);
	}
	*/

	printf("Number of detected lines: %d\n", num_of_lines[0]);
	printf("Number of detected segments: %d\n", num_of_segments[0]);

	// Edge image
	cv::Mat edges_img(IMG_HEIGHT, IMG_WIDTH, CV_8UC3);
	cv::Mat src_img2(IMG_HEIGHT, IMG_WIDTH, CV_8UC3);

	img_edges.axis2cv(edges_img.data);
	img_in.axis2cv(src_img2.data);

	cv::imwrite("Edges.jpg", edges_img);

	// Draw the lines
	draw_lines(outrho, outtheta, num_of_lines, edges_img, src_img);

	draw_segments(segments, num_of_segments, src_img2);

	cv::imwrite("Lines_Edges.jpg", edges_img);
	cv::imwrite("Lines_Original.jpg", src_img);
	cv::imwrite("segments.jpg", src_img2);

	return 0;
}
