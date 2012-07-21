'''
beaglebone GPIO manipulation utility.

   copyright Kouji Yatou <kouji.yatou@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

'''

import os

debugmode=0

#gpio database.
#[No of gpio, name in omap_mux dir, SIGNAL_Name]
Bone_GPIO =\
[\
[38,'gpmc_ad6','GPIO1_6'],\
[39,'gpmc_ad7','GPIO1_7'],\
[34,'gpmc_ad2','GPIO1_2'],\
#[35,'gpmc_ad3','GPIO1_3'],\ #this gpio pin did not work my BeagleBone.
[66,'gpmc_advn_ale','TIMER4'],\
[67,'gpmc_oen_ren','TIMER7'],\
[69,'gpmc_ben0_cle','TIMER5'],\
[68,'gpmc_wen','TIMER6'],\
[45,'gpmc_ad13','GPIO1_13'],\
[44,'gpmc_ad12','GPIO1_12'],\
[23,'gpmc_ad9','EHRPWM2B'],\
[26,'gpmc_ad10','GPIO0_26'],\
[47,'gpmc_ad15','GPIO1_15'],\
[46,'gpmc_ad14','GPIO1_14'],\
[27,'gpmc_ad11','GPIO0_27'],\
[65,'gpmc_clk','GPIO2_1'],\
[22,'gpmc_ad8','EHRPWM2A'],\
[63,'gpmc_csn2','GPIO1_31'],\
[62,'gpmc_csn1','GPIO1_30'],\
[37,'gpmc_ad5','GPIO1_5'],\
[36,'gpmc_ad4','GPIO1_4'],\
[33,'gpmc_ad1','GPIO1_1'],\
[32,'gpmc_ad0','GPIO1_0'],\
[61,'gpmc_csn0','GPIO1_29'],\
[86,'lcd_vsync','GPIO2_22'],\
[88,'lcd_pclk','GPIO2_24'],\
[87,'lcd_hsync','GPIO2_23'],\
[89,'lcd_ac_bias_en','GPIO2_25'],\
[10,'lcd_data14','UART5_CTSN'],\
[11,'lcd_data15','UART5_RTSN'],\
[9,'lcd_data13','UART4_RTSN'],\
[81,'lcd_data11','UART3_RTSN'],\
[8,'lcd_data12','UART4_CTSN'],\
[80,'lcd_data10','UART3_CTSN'],\
[78,'lcd_data8','UART5_TXD'],\
[79,'lcd_data9','UART5_RXD'],\
[76,'lcd_data6','GPIO2_12'],\
[77,'lcd_data7','GPIO2_13'],\
[74,'lcd_data4','GPIO2_10'],\
[75,'lcd_data5','GPIO2_11'],\
[72,'lcd_data2','GPIO2_8'],\
[73,'lcd_data3','GPIO2_9'],\
[70,'lcd_data0','GPIO2_6'],\
[71,'lcd_data1','GPIO2_7'],\
[30,'gpmc_wait0','UART4_RXD'],\
[60,'gpmc_ben1','GPIO1_28'],\
[31,'gpmc_wpn','UART4_TXD'],\
[50,'gpmc_a2','EHRPWM1A'],\
[48,'gpmc_a0','GPIO1_16'],\
[51,'gpmc_a3','EHRPWM1B'],\
[5,'spi0_cs0','I2C1_SCL'],\
[4,'spi0_d1','I2C1_SDA'],\
[13,'uart1_rtsn','I2C2_SCL'],\
[12,'uart1_ctsn','I2C2_SDA'],\
[3,'spi0_d0','UART2_TXD'],\
[2,'spi0_sclk','UART2_RXD'],\
[49,'gpmc_a1','GPIO1_17'],\
[15,'uart1_txd','UART1_TXD'],\
[117,'mcasp0_ahclkx','GPIO3_21'],\
[14,'uart1_rxd','UART1_RXD'],\
[115,'mcasp0_fsr','GPIO3_19'],\
[113,'mcasp0_ahclkr','SPI1_CS0'],\
[111,'mcasp0_fsx','SPI1_D0'],\
[112,'mcasp0_axr0','SPI1_D1'],\
[110,'mcasp0_aclkx','SPI1_SCLK'],\
[20,'xdma_event_intr1','CLKOUT2']
]



def getMuxName(gpiono):
	"""find omap_mux name from GPIO database."""
	muxname='no_muxName'
	for rec in Bone_GPIO:
		if rec[0]==gpiono:
			muxname=rec[1]
	return muxname


def getPinName(gpiono):
	"""find PIN name(in P8 or P9) from GPIO database."""
	pinname='NONE'
	for rec in Bone_GPIO:
		if rec[0]==gpiono:
			pinname=rec[2]
	return pinname

def exportPin(gpiono):
	"""exportPin(gpiono) exports to sysfs."""
	
	pinno=int(gpiono)
	dirname='/sys/class/gpio/gpio%d' % pinno
	if not os.path.isdir(dirname):
		cmd= 'echo '+str(gpiono)+' > /sys/class/gpio/export'
		#print cmd
		os.system(cmd)
		

def unexportPin(gpiono):
	"""unexportPin(gpiono) unexports from sysfs."""
	dirname='/sys/class/gpio/gpio%d' % gpiono
	if os.path.isdir(dirname):
		pinno=int(gpiono)
		cmd= 'echo '+str(gpiono)+' > /sys/class/gpio/unexport'
		#print cmd
		os.system(cmd)


def setGPIOWriteMode(gpiono):
	"""set multiplex to gpio mode"""
	cmd= 'echo 7 > /sys/kernel/debug/omap_mux/'+getMuxName(gpiono)
	if debugmode:print cmd
	os.system(cmd)
	cmd= 'echo out > /sys/class/gpio/gpio'+str(gpiono)+'/direction'
	if debugmode:print cmd
	os.system(cmd)


def setGPIOReadMode(gpiono):
	"""set multiplex to gpio mode (readable)"""
	cmd= 'echo 27 > /sys/kernel/debug/omap_mux/'+getMuxName(gpiono)
	if debugmode:print cmd
	os.system(cmd)

def gpioOn(gpiono):
	cmd = 'echo 1 > '+getGPIOPath(gpiono)+'/value'
	if debugmode:print cmd
	os.system(cmd)

def gpioOff(gpiono):
	cmd = 'echo 0 > '+getGPIOPath(gpiono)+'/value'
	if debugmode:print cmd
	os.system(cmd)

def getGPIOPath(gpiono):
	return '/sys/class/gpio/gpio'+str(gpiono)



"""
for n in range(0,128):
	print str(n)+'>'+getMuxName(n),
	print '>'+getPinName(n)
"""

def exportAllGPIO():
	"""Export ALL GPIO pin. you need admin parminssion. """
	for rec in Bone_GPIO:
		unexportPin(rec[0])
		exportPin(rec[0])
		setGPIOWriteMode(rec[0])


def unexportAllGPIO():
	"""UnExport ALL GPIO pin """
	for rec in Bone_GPIO:
		unexportPin(rec[0])




#test
if __name__ == '__main__':
	#test
	exportAllGPIO()

        unexportAllGPIO()

