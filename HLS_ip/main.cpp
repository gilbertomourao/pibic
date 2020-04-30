/**
 * testbench
 */

#include "top.h"
#include <hls_opencv.h>

#define IMAGE_PATH "C:/Users/chico/Documents/HLS/Zedboard/test_hough/data_casa/usar/canto.jpg"

int main()
{
	cv::Mat src_img = cv::imread(IMAGE_PATH);

	hwv::Stream<HWV_RGB_MODE, IMG_HEIGHT, IMG_WIDTH> img_in;
	hwv::Stream<HWV_RGB_MODE, IMG_HEIGHT, IMG_WIDTH> img_edges;

	img_in.cv2axis(src_img.data);

	float outrho[MAX_LINES], outtheta[MAX_LINES];

	hough_accel(img_in.data, img_edges.data, outrho, outtheta, 20, 50, 80);

	// Edge image
	cv::Mat edges_img(IMG_HEIGHT, IMG_WIDTH, CV_8UC3);

	img_edges.axis2cv(edges_img.data);

	cv::imwrite("Edges.jpg", edges_img);

	// Draws the lines
	int wdtby2 = IMG_WIDTH/2;
	int heiby2 = IMG_HEIGHT/2;

	for (int i = 0; i < MAX_LINES; i++)
	{
		float rho = outrho[i], theta = outtheta[i];
		cv::Point pt1xi, pt2xi;
		double a = cos(theta), b = sin(theta);
		double x0 = a*rho, y0 = b*rho;
		pt1xi.x = cvRound(x0 + 1500*(-b) + (wdtby2));
		pt1xi.y = cvRound(y0 + 1500*(a) + (heiby2));
		pt2xi.x = cvRound(x0 - 1500*(-b) + (wdtby2));
		pt2xi.y = cvRound(y0 - 1500*(a) + (heiby2));
		cv::line( edges_img, pt1xi, pt2xi, cv::Scalar(255,0,0), 1, CV_AA);
	}

	cv::imwrite("Lines.jpg", edges_img);

	return 0;
}
