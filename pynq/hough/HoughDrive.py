from pynq import Overlay, GPIO, Register, Xlnk
import os
import inspect
import numpy as np
import time

class houghOverlay(Overlay):
    """
    This overlay constains the inferface to the PL
    image processing filter. It extracts the edges
    of the image, the lines polar parameters and the
    lines segments as well. The image size is 640x480. 
    """

    __HEIGHT = 480
    __WIDTH = 640
    __LINES = 100

    __RESET_VALUE = 0
    __NRESET_VALUE = 1

    # Registers offset
    __HOUGH_AP_CTRL_OFF = 0x00
    __HOUGH_AP_CTRL_START_IDX = 0
    __HOUGH_AP_CTRL_DONE_IDX = 1
    __HOUGH_AP_CTRL_IDLE_IDX = 2
    __HOUGH_AP_CTRL_READY_IDX = 3

    __HOUGH_GIE_OFF = 0x04
    __HOUGH_IER_OFF = 0x08
    __HOUGH_ISR_OFF = 0x0C

    # M_AXI offset
    __OUTRHO_ADDR = 0x10
    __OUTTHETA_ADDR = 0x18
    __NUM_OF_LINES_ADDR = 0x20
    __LINES_SEGMENTS_ADDR = 0x28
    __NUM_OF_SEGMENTS_ADDR = 0x30

    # S_AXILITE offset
    __EDGES_LTHR_ADDR = 0x38
    __EDGES_HTHR_ADDR = 0x40
    __LINES_THR_ADDR = 0x48
    __GAP_SIZE_ADDR = 0x50
    __MIN_LENGTH_ADDR = 0x58

    def __init__(self, bitfile, **kwargs):
        """
        Constructor (load the bit file)
        """
        file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
        dir_path = os.path.dirname(file_path)
        bitfile = os.path.join(dir_path, bitfile)
        super().__init__(bitfile, **kwargs)

        # Manually define the GPIO pin that drives reset
        self.__resetPin = GPIO(GPIO.get_gpio_pin(0), "out")
        self.nreset()

        # For convenience
        self.__hough = self.image_processing.hough_accel_0
        self.__dma = self.image_processing.axi_dma_0

        # Define a Register object at address 0x00 of the overlay address space
        base_addr = self.__hough.mmio.base_addr
        self.__ap_ctrl = Register(base_addr, 32)
        self.__outrho_offset = Register(base_addr + self.__OUTRHO_ADDR, 32)
        self.__outtheta_offset = Register(base_addr + self.__OUTTHETA_ADDR, 32)
        self.__num_of_lines_offset = Register(base_addr + self.__NUM_OF_LINES_ADDR, 32)
        self.__segments_offset = Register(base_addr + self.__LINES_SEGMENTS_ADDR, 32)
        self.__num_of_segments_offset = Register(base_addr + self.__NUM_OF_SEGMENTS_ADDR, 32)

        # DMA transfer engine
        self.__xlnk = Xlnk()

        # Memory pre-allocation
        self.__cma_rho = self.__xlnk.cma_array(self.__LINES, np.single)
        self.__cma_theta = self.__xlnk.cma_array(self.__LINES, np.single)
        self.__cma_numoflines = self.__xlnk.cma_array(1, np.int)
        self.__cma_segments = self.__xlnk.cma_array((self.__LINES, 4), np.int)
        self.__cma_numofsegments = self.__xlnk.cma_array(1, np.int)

        self.__cmabuf_dest = self.__xlnk.cma_array((self.__HEIGHT, self.__WIDTH, 3), np.uint8)
        
        # public
        self.frame = self.__xlnk.cma_array((self.__HEIGHT, self.__WIDTH, 3), np.uint8)

        # Write address of M_AXI to HLS core
        self.__outrho_offset[31:0] = self.__xlnk.cma_get_phy_addr(self.__cma_rho.pointer)
        self.__outtheta_offset[31:0] = self.__xlnk.cma_get_phy_addr(self.__cma_theta.pointer)
        self.__num_of_lines_offset[31:0] = self.__xlnk.cma_get_phy_addr(self.__cma_numoflines.pointer)
        self.__segments_offset[31:0] = self.__xlnk.cma_get_phy_addr(self.__cma_segments.pointer)
        self.__num_of_segments_offset[31:0] = self.__xlnk.cma_get_phy_addr(self.__cma_numofsegments.pointer)

    def __del__(self):
        self.__cmabuf_dest.freebuffer()
        self.__cma_rho.freebuffer()
        self.__cma_theta.freebuffer()
        self.__cma_numoflines.freebuffer()
        self.__cma_segments.freebuffer()
        self.__cma_numofsegments.freebuffer()
        self.frame.freebuffer()

    def __start(self):
        """
        Raise AP_START and enable the HLS core
        """
        self.__ap_ctrl[self.__HOUGH_AP_CTRL_START_IDX] = 1
        pass

    def __stop(self):
        """
        Lower AP_START and disable the HLS core
        """
        self.__ap_ctrl[self.__HOUGH_AP_CTRL_START_IDX] = 0
        pass

    def nreset(self):
        """
        Set the reset pin to self.__NRESET_VALUE to place the core into
        not-reset (usually run)
        """
        self.__resetPin.write(self.__NRESET_VALUE)

    def reset(self):
        """
        Set the reset pin to self.__RESET_VALUE to place the core into
        reset
        """
        self.__resetPin.write(self.__RESET_VALUE)

    def loadParameters(self, **kwargs):
        """
        Load the Hough overlay coefficients into the HLS core
        """
        edges_lthr = kwargs.get('edges_lthr')
        edges_hthr = kwargs.get('edges_hthr')
       
        lines_thr = kwargs.get('lines_thr')
        gap_size = kwargs.get('gap_size')
        min_length = kwargs.get('min_length')

        self.__hough.write(self.__EDGES_LTHR_ADDR, edges_lthr)
        self.__hough.write(self.__EDGES_HTHR_ADDR, edges_hthr)
        
        self.__hough.write(self.__LINES_THR_ADDR, lines_thr)
        self.__hough.write(self.__GAP_SIZE_ADDR, gap_size)
        self.__hough.write(self.__MIN_LENGTH_ADDR, min_length)

    def HoughLines(self, canny = None):
        """
        Launch computation on the HLS core
        """
        # To check when the computation will finish
        self.__cma_numofsegments[0] = -1 # impossible to have numofsegments < 0

        # FPGA --> ARM
        self.__dma.recvchannel.transfer(self.__cmabuf_dest)
        
        # ARM --> FPGA
        self.__dma.sendchannel.transfer(self.frame)

        # Raise the AP_START bit of the AP_CTRL to initiate computation
        self.__start()

        # Wait for the DMA engines to finish
        self.__dma.sendchannel.wait()
        self.__dma.recvchannel.wait()
        
        # delay to wait for the m_axi output
        #time.sleep(3e-3)
        while(self.__cma_numofsegments[0] == -1):
            continue

        # Lower the AP_START bit of the AP_CTRL to terminate computation
        self.__stop()

        # Return the values as numpy arrays
        n_lines = self.__cma_numoflines[0]
        n_segments = self.__cma_numofsegments[0]

        lines = np.zeros((n_lines,2), dtype = np.single)
        segments = np.zeros((n_segments,4), dtype = np.int)

        lines[:,0] = self.__cma_rho[0:n_lines]
        lines[:,1] = self.__cma_theta[0:n_lines]

        segments = self.__cma_segments[0:n_segments][:]

        if (type(canny) is np.ndarray and canny.shape == (self.__HEIGHT, self.__WIDTH, 3) and canny.dtype == np.uint8):
            canny[:] = self.__cmabuf_dest[:]

        return [lines, segments]

# end of HoughDrive    
