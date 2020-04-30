from pynq import Overlay, GPIO, Register, Xlnk
import os
import inspect
import numpy as np
import time

class houghOverlay(Overlay):
    """
    This overlay constains the inferface to the PL
    image processing filter. It extracts the edges
    of the image and the lines polar parameters as
    well. The image size is 640x480. 
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

    # S_AXILITE offset
    __EDGES_LTHR_ADDR = 0x20
    __EDGES_HTHR_ADDR = 0x28
    __LINES_THR_ADDR = 0x30

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

        # DMA transfer engine
        self.__xlnk = Xlnk()

        # Memory pre-allocation
        self.__cma_rho = self.__xlnk.cma_array(self.__LINES, np.single)
        self.__cma_theta = self.__xlnk.cma_array(self.__LINES, np.single)
        self.__cmabuf_dest = self.__xlnk.cma_array((self.__HEIGHT, self.__WIDTH, 3), np.uint8)
        # public
        self.frame = self.__xlnk.cma_array((self.__HEIGHT, self.__WIDTH, 3), np.uint8)

        # Numpy arrays
        self.__rho = np.zeros(self.__LINES, dtype = np.single)
        self.__theta = np.zeros(self.__LINES, dtype = np.single)

        # Write address of _rho and _theta to HLS core
        self.__outrho_offset[31:0] = self.__xlnk.cma_get_phy_addr(self.__cma_rho.pointer)
        self.__outtheta_offset[31:0] = self.__xlnk.cma_get_phy_addr(self.__cma_theta.pointer)

    def __del__(self):
        self.__cmabuf_dest.freebuffer()
        self.__cma_rho.freebuffer()
        self.__cma_theta.freebuffer()
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

        self.__hough.write(self.__EDGES_LTHR_ADDR, edges_lthr)
        self.__hough.write(self.__EDGES_HTHR_ADDR, edges_hthr)
        self.__hough.write(self.__LINES_THR_ADDR, lines_thr)

    def HoughLines(self, canny = None):
        """
        Launch computation on the HLS core
        """
        # To check when the computation will finish
        self.__cma_rho[self.__LINES-1] = -1 # impossible to have rho < 0

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
        #time.sleep(1e-3)
        while(self.__cma_rho[self.__LINES-1] == -1):
            continue

        # Lower the AP_START bit of the AP_CTRL to terminate computation
        self.__stop()

        self.__rho[:] = self.__cma_rho[:]
        self.__theta[:] = self.__cma_theta[:]
        if (type(canny) is np.ndarray and canny.shape == (self.__HEIGHT, self.__WIDTH, 3) and canny.dtype == np.uint8):
            canny[:] = self.__cmabuf_dest[:]

        return [self.__rho, self.__theta]

# end of HoughDrive    