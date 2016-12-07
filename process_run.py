#!/usr/bin/python
import io
import ctypes
import struct
import binascii
import array
import numpy
from collections import namedtuple
import glob
import os
import csv
import math
import matplotlib.pyplot as plt
from matplotlib import cm

class TestEntry:

    def __init__(self, entry1, entry2, entry3, array1, array2):
        self.entry1 = entry1
        self.entry2 = entry2
        self.entry3 = entry3
        self.array1 = array1
        self.array2 = array2
        #print self.entry1.ENERGY_LVL
        self.starts_hist_entry = numpy.array([entry2.starts_00, entry2.starts_01, entry2.starts_02, entry2.starts_03, entry2.starts_04, entry2.starts_05, entry2.starts_06, entry2.starts_07, entry2.starts_08, entry2.starts_09, entry2.starts_10, entry2.starts_11, entry2.starts_12, entry2.starts_13, entry2.starts_14, entry2.starts_15])
class TestRun:
    EntryList = []
    energy_elevation_start1 = [[[] for i in range(360)] for i in range(64)]
    energy_elevation_start2 = [[[] for i in range(360)] for i in range(64)]
    energy_elevation_stop1 = [[[] for i in range(360)] for i in range(64)]
    energy_elevation_stop2 = [[[] for i in range(360)] for i in range(64)]
    mean_energy_elevation_start1 = numpy.empty([64, 360], dtype=float)
    mean_energy_elevation_start2 = numpy.empty([64, 360], dtype=float)
    mean_energy_elevation_stop1 = numpy.empty([64, 360], dtype=float)
    mean_energy_elevation_stop2 = numpy.empty([64, 360], dtype=float)
    stable_count = 0
    starts_hist = numpy.zeros(16)
    def __init__(self, dir_name):
        print "Building new run from: " + dir_name
        self.root = dir_name

    def GetBinFile(self, directory):
        return glob.glob(self.root + directory + '/*.bin')[0]

    def CalculateCurrentDensity(self, directory):
        current_values = []
        filename = self.GetCurrentFile(directory)[0]
        with open(filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['acr13.moving'] != 'nan' and float(row['acr13.moving']) == 0:
                    val =  float(row['pam11.imon'])
                    if not math.isnan(val):
                        current_values.append(float(val))

            J = numpy.mean(current_values)*1e-12/(1.602e-19*3.14159)
            print J
            return J
    def GetCurrentFile(self, directory):
        filename = glob.glob(self.root + directory + "/char_beam_current*.csv")
        print filename
        return filename
    def ProcessRun(self):
        for directory in os.listdir(self.root):
            print directory
            file = open(self.GetBinFile(directory), 'rb')
            J = self.CalculateCurrentDensity(directory)
            self.ProcessEntry(file, J)
            self.GeneratePlots()
    def GeneratePlots(self):
        fig, ax = plt.subplots()
        cax = ax.imshow(self.mean_energy_elevation_start1, interpolation='nearest', cmap=cm.coolwarm)
        ax.set_title("Start1/J at Energy vs Elevation")
        cbar = fig.colorbar(cax, ticks=[numpy.min(self.mean_energy_elevation_start1), numpy.max(self.mean_energy_elevation_start1)/2, numpy.max(self.mean_energy_elevation_start1)])
        cbar.ax.set_yticklabels(['< 0', str(numpy.max(self.mean_energy_elevation_start1/2)), '>'+ str(numpy.max(self.mean_energy_elevation_start1))])  # vertically oriented colorbar

        fig, ax = plt.subplots()
        cax = ax.imshow(self.mean_energy_elevation_start2, interpolation='nearest', cmap=cm.coolwarm)
        ax.set_title("Start2/J at Energy vs Elevation")
        cbar = fig.colorbar(cax, ticks=[numpy.min(self.mean_energy_elevation_start2), numpy.max(self.mean_energy_elevation_start2)/2, numpy.max(self.mean_energy_elevation_start2)])
        cbar.ax.set_yticklabels(['< 0', str(numpy.max(self.mean_energy_elevation_start2/2)), '>'+ str(numpy.max(self.mean_energy_elevation_start2))])  # vertically oriented colorbar

        fig, ax = plt.subplots()
        cax = ax.imshow(self.mean_energy_elevation_start1, interpolation='nearest', cmap=cm.coolwarm)
        ax.set_title("Stop1/J at Energy vs Elevation")
        cbar = fig.colorbar(cax, ticks=[numpy.min(self.mean_energy_elevation_stop1), numpy.max(self.mean_energy_elevation_stop1)/2, numpy.max(self.mean_energy_elevation_stop1)])
        cbar.ax.set_yticklabels(['< 0', str(numpy.max(self.mean_energy_elevation_stop1/2)), '>'+ str(numpy.max(self.mean_energy_elevation_stop1))])  # vertically oriented colorbar

        fig, ax = plt.subplots()
        cax = ax.imshow(self.mean_energy_elevation_start1, interpolation='nearest', cmap=cm.coolwarm)
        ax.set_title("Stop2/J at Energy vs Elevation")
        cbar = fig.colorbar(cax, ticks=[numpy.min(self.mean_energy_elevation_stop2), numpy.max(self.mean_energy_elevation_stop2)/2, numpy.max(self.mean_energy_elevation_stop2)])
        cbar.ax.set_yticklabels(['< 0', str(numpy.max(self.mean_energy_elevation_stop2/2)), '>'+ str(numpy.max(self.mean_energy_elevation_stop2))])  # vertically oriented colorbar




        plt.show()

    def ProcessEntry(self, file, J):
        s1 = struct.Struct('>' + '26s I I I I I I I I I I I I f f f f f f f f 4s H H I I H I HHHHH I HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH III')
        array1 = struct.Struct('>' + '8192H')
        s2 = struct.Struct('>' + 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
        array2 = struct.Struct('>' + '1024I')
        s3 = struct.Struct('>' + 'BBBBBBBBB H BBBBB I')
        b = array.array('c', '\0' * (s1.size + s2.size + s3.size + array1.size + array2.size))
        current_index = 0
        first_entry = namedtuple('first_entry', 'Timestamp ENERGY_LVL MCP_PGM TOF_PGM TOF_TBL_ESA_RNG TOF_TBL_ESA_DAC TOF_TBL_RFVPSDAC TOF_TBL_RF_FREQ TOF_TBL_RFGENDAC TOF_TBL_SAMPLE TOF_DAC MCP_DAC GRID_DAC acr13_moving xacr13_prog acr13_xmon acr13_aprog acr13_amon acr13_bprog acr13_bmon vgc7_ig1pmon sync version energy fine_time coarse_time tof_reg_0 tof_reg_1 tof_reg_2_dwell tof_reg_2_sample dac_tof_dwellstart dac_mcp_dwellstart dac_grid_dwellstart scratchpad ESA_low_gain_voltage_monitor ESA_high_gain_voltage_monitor ESA_supply_voltage_monitor Grid_voltage_monitor MCP_voltage_monitor MCP_current_monitor TOF_voltage_monitor TOF_current_monitor CPU_temperature pos_3_3V_monitor RF_generator_board_temperature RF_LVPS_board_temperature pos_12V_monitor pos_1_8V_monitor RF_load_averaging_supply_voltage_monitor RF_generator_voltage_monitor FPGA_temperature pos_5V_monitor RF_Generator_frequency_monitor RF_Generator_program_voltage pos_1_5V_FPGA_core_voltage_monitor RF_variable_power_supply_program_voltage RF_variable_power_supply_current_monitor RF_variable_power_supply_voltage_monitor MCP_program_voltage_monitor TOF_program_voltage_monitor ESA_program_voltage_monitor Grid_program_voltage_monitor LVPS_board_temperature HVPS_board_temperature second_TOF_board_temperature TOF_board_temperature neg_5V_monitor neg_12V_monitor neg_5V_reference_monitor SPARE__jumper_to_analog_ground1 SPARE__jumper_to_analog_ground2 SPARE__jumper_to_analog_ground3 SPARE__jumper_to_analog_ground4 SPARE__jumper_to_analog_ground5 spare_0 spare_1 spare_2')
        second_entry = namedtuple('second_entry', 'starts_00 starts_01 starts_02 starts_03 starts_04 starts_05 starts_06 starts_07 starts_08 starts_09 starts_10 starts_11 starts_12 starts_13 starts_14 starts_15 valevttof1 valevttof2 valevttof3 starttof1 stoptof1 starttof2 stoptof2 overflow stops_00 stops_01 stops_02 stops_03 stops_04 stops_05 stops_06 stops_07')
        third_entry = namedtuple('third_entry', 'dac_00 dac_01 dac_02 dac_03 start_scaling stop_scaling tof_mode time_to_ve_ck hk_spare_1 counter hk_spare_2 bias_00 bias_01 bias_02 bias_03 crc32'  )
        while True:
            b = file.read(s1.size + s2.size + s3.size + array1.size + array2.size)
            if len(b) < s1.size + s2.size + s3.size + array1.size + array2.size:
                break
            entry1 = first_entry._make(s1.unpack_from(b, 0))
            first_array = [array1.unpack_from(b, 234)]
            numpy.reshape(first_array, (16, 512))
            entry2 = second_entry._make(s2.unpack_from(b, 16618))
            second_array = [array2.unpack_from(b, 16746)]
            entry3 = third_entry._make(s3.unpack_from(b, 20842))
            entry = TestEntry(entry1, entry2, entry3, first_array, second_array)
            if entry.entry1.acr13_moving == 0:
                self.energy_elevation_start1[entry.entry1.ENERGY_LVL][int(entry.entry1.acr13_bprog)+180].append(entry.entry2.starttof1)
                self.energy_elevation_start2[entry.entry1.ENERGY_LVL][int(entry.entry1.acr13_bprog)+180].append(entry.entry2.starttof2)
                self.energy_elevation_stop1[entry.entry1.ENERGY_LVL][int(entry.entry1.acr13_bprog)+180].append(entry.entry2.stoptof1)
                self.energy_elevation_stop2[entry.entry1.ENERGY_LVL][int(entry.entry1.acr13_bprog)+180].append(entry.entry2.stoptof2)
                self.stable_count += 1
        print "Collapsing to means"
        energy_index = 0
        elevation_index = -180
        for row in self.energy_elevation_start1:
            elevation_index = -180
            for column in row:
                for entry in column:
                    self.mean_energy_elevation_start1[energy_index][elevation_index+180] = numpy.mean(entry)/J
                elevation_index += 1
            energy_index +=1
        energy_index = 0
        elevation_index = -180
        for row in self.energy_elevation_start2:
            elevation_index = -180
            for column in row:
                for entry in column:
                    self.mean_energy_elevation_start2[energy_index][elevation_index+180] = numpy.mean(entry)/J
                elevation_index += 1
            energy_index +=1
        energy_index = 0
        elevation_index = -180
        for row in self.energy_elevation_stop1:
            elevation_index = -180
            for column in row:
                for entry in column:
                    self.mean_energy_elevation_stop1[energy_index][elevation_index+180] = numpy.mean(entry)/J
                elevation_index += 1
            energy_index +=1
        energy_index = 0
        elevation_index = -180
        for row in self.energy_elevation_stop2:
            elevation_index = -180
            for column in row:
                for entry in column:
                    self.mean_energy_elevation_stop2[energy_index][elevation_index+180] = numpy.mean(entry)/J
                elevation_index += 1
            energy_index +=1
        print "Run length: " + str(len(self.EntryList))
        print "Stable count: " + str(self.stable_count)
        print self.starts_hist
        del entry

if __name__ == "__main__":
    run = TestRun("./data/")
    run.ProcessRun()
