#!/usr/bin/python
import io
import ctypes
import struct
import binascii
import array
import numpy
from collections import namedtuple
s1 = struct.Struct('>' + '26s I I I I I I I I I I I I f f f f f f f f 4s H H I I H I HHHHH I HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH III')
array1 = struct.Struct('>' + '8192H')
s2 = struct.Struct('>' + 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
array2 = struct.Struct('>' + '1024I')
s3 = struct.Struct('>' + 'BBBBBBBBB H BBBBB I')

#tof_hist = struct.Struct('>' + '8192I')
b = array.array('c', '\0' * (s1.size + s2.size + s3.size + array1.size + array2.size))
file = open("./data.bin", 'rb')
current_index = 0
first_entry = namedtuple('first_entry', 'Timestamp ENERGY_LVL MCP_PGM TOF_PGM TOF_TBL_ESA_RNG TOF_TBL_ESA_DAC TOF_TBL_RFVPSDAC TOF_TBL_RF_FREQ TOF_TBL_RFGENDAC TOF_TBL_SAMPLE TOF_DAC MCP_DAC GRID_DAC acr13_moving xacr13_prog acr13_xmon acr13_aprog acr13_amon acr13_bprog acr13_bmon vgc7_ig1pmon sync version energy fine_time coarse_time tof_reg_0 tof_reg_1 tof_reg_2_dwell tof_reg_2_sample dac_tof_dwellstart dac_mcp_dwellstart dac_grid_dwellstart scratchpad ESA_low_gain_voltage_monitor ESA_high_gain_voltage_monitor ESA_supply_voltage_monitor Grid_voltage_monitor MCP_voltage_monitor MCP_current_monitor TOF_voltage_monitor TOF_current_monitor CPU_temperature pos_3_3V_monitor RF_generator_board_temperature RF_LVPS_board_temperature pos_12V_monitor pos_1_8V_monitor RF_load_averaging_supply_voltage_monitor RF_generator_voltage_monitor FPGA_temperature pos_5V_monitor RF_Generator_frequency_monitor RF_Generator_program_voltage pos_1_5V_FPGA_core_voltage_monitor RF_variable_power_supply_program_voltage RF_variable_power_supply_current_monitor RF_variable_power_supply_voltage_monitor MCP_program_voltage_monitor TOF_program_voltage_monitor ESA_program_voltage_monitor Grid_program_voltage_monitor LVPS_board_temperature HVPS_board_temperature second_TOF_board_temperature TOF_board_temperature neg_5V_monitor neg_12V_monitor neg_5V_reference_monitor SPARE__jumper_to_analog_ground1 SPARE__jumper_to_analog_ground2 SPARE__jumper_to_analog_ground3 SPARE__jumper_to_analog_ground4 SPARE__jumper_to_analog_ground5 spare_0 spare_1 spare_2')

#tof_hist_16_512_
second_entry = namedtuple('second_entry', 'starts_00 starts_01 starts_02 starts_03 starts_04 starts_05 starts_06 starts_07 starts_08 starts_09 starts_10 starts_11 starts_12 starts_13 starts_14 starts_15 valevttof1 valevttof2 valevttof3 starttof1 stoptof1 starttof2 stoptof2 overflow stops_00 stops_01 stops_02 stops_03 stops_04 stops_05 stops_06 stops_07')

#direct_event

third_entry = namedtuple('third_entry', 'dac_00 dac_01 dac_02 dac_03 start_scaling stop_scaling tof_mode time_to_ve_ck hk_spare_1 counter hk_spare_2 bias_00 bias_01 bias_02 bias_03 crc32'  )
while True:
  b = file.read(s1.size + s2.size + s3.size + array1.size + array2.size)
  if len(b) < s1.size + s2.size + s3.size + array1.size + array2.size:
	break
  print first_entry._make(s1.unpack_from(b, 0))
  first_array = [array1.unpack_from(b, 234)]
  numpy.reshape(first_array, (16, 512))
  print first_array
  print second_entry._make(s2.unpack_from(b, 16618))
  second_array = [array2.unpack_from(b, 16746)]
  print second_array
  print third_entry._make(s3.unpack_from(b, 20842))



