/**
 *	Header to prevent SIGSEGV when doing C simulation
 */

#ifndef HWV_CLASS_H
#define HWV_CLASS_H

namespace hwv
{
	template<class SRC_T, int HEIGHT, int WIDTH>
	class Matrix
	{
	public:
		Matrix() // constructor
		{
			#ifndef __SYNTHESIS__
				data = (SRC_T *)malloc(HEIGHT * WIDTH * sizeof(SRC_T));
			#endif
			#pragma HLS STREAM variable=data depth=2 dim=1
		}

		SRC_T read(int i, int j)
		{
			return data[i*WIDTH + j];
		}

		void write(int i, int j, SRC_T value)
		{
			data[i*WIDTH + j] = value;
		}

		~Matrix() // destructor
		{
			#ifndef __SYNTHESIS__
				free(data);
			#endif
		}

	//private:
		#ifndef __SYNTHESIS__
			SRC_T *data;
		#else
			SRC_T data[HEIGHT * WIDTH];
		#endif
	};

}

#endif // HWV_CLASS_H