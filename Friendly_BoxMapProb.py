from tkinter import Tk, Label, Button, W, E, Entry, OptionMenu, StringVar, DoubleVar, IntVar, Canvas, Scrollbar, VERTICAL, Frame, messagebox
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import utm
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class MyFirstGUI:

    def __init__(self, master):
        self.master = master
        master.title("BoxMapProb")

        self.var_input = StringVar(master)
        self.var_input.set("Set manually")
        run_name = StringVar(master)
        run_name.set("Example")
        self.var_dem = StringVar(master)
        self.var_dem.set("STRM 30 m")
        lon1 = DoubleVar(master)
        lon1.set(-72.8)
        lon2 = DoubleVar(master)
        lon2.set(-72.5)
        lat1 = DoubleVar(master)
        lat1.set(-42.95)
        lat2 = DoubleVar(master)
        lat2.set(-42.75)
        conoid_levels = IntVar(master)
        conoid_levels.set(30)
        self.var_ds = StringVar(master)
        self.var_ds.set("Punctual")
        lon_cen = DoubleVar(master)
        lon_cen.set(-72.650)
        lat_cen = DoubleVar(master)
        lat_cen.set(-42.835)
        east_cen = DoubleVar(master)
        east_cen.set(501000.0)
        north_cen = DoubleVar(master)
        north_cen.set(4178000.0)
        azimuth_line = DoubleVar(master)
        azimuth_line.set(10.0)
        length_line = DoubleVar(master)
        length_line.set(1000.0)
        radius_rad = DoubleVar(master)
        radius_rad.set(1000.0)
        ang1_rad = DoubleVar(master)
        ang1_rad.set(10.0)
        ang2_rad = DoubleVar(master)
        ang2_rad.set(150.0)
        cen_var = DoubleVar(master)
        cen_var.set(300.0)
        volume = DoubleVar(master)
        volume.set(10000000.0)
        var_volume = DoubleVar(master)
        var_volume.set(1000000.0)
        ws = DoubleVar(master)
        ws.set(0.40)
        var_ws = DoubleVar(master)
        var_ws.set(0.05)
        phi0 = DoubleVar(master)
        phi0.set(0.010)
        var_phi0 = DoubleVar(master)
        var_phi0.set(0.005)
        Fr = DoubleVar(master)
        Fr.set(1.0)
        var_Fr = DoubleVar(master)
        var_Fr.set(0.1)
        rhop = DoubleVar(master)
        rhop.set(1000.0)
        var_rhop = DoubleVar(master)
        var_rhop.set(200.0)
        rhog = DoubleVar(master)
        rhog.set(1.10)
        var_rhog = DoubleVar(master)
        var_rhog.set(0.10)
        self.var_d_input = StringVar(master)
        self.var_d_input.set("Uniform")
        N = IntVar(master)
        N.set(30)
        var_save = StringVar(master)
        var_save.set("Yes")

        self.label1 = Label(master, text="Source input parameters")
        self.label1.grid(row=0, column=0, columnspan=2, sticky=W)

        self.label2 = Label(master, text="Run name")
        self.label2.grid(row=1, column=0, columnspan=2, sticky=W)

        self.label3 = Label(master, text="Source DEM")
        self.label3.grid(row=2, column=0, columnspan=2, sticky=W)

        self.label4 = Label(master, text="Longitude 1 [deg]")
        self.label4.grid(row=3, column=0, columnspan=2, sticky=W)

        self.label5 = Label(master, text="Longitude 2 [deg]")
        self.label5.grid(row=4, column=0, columnspan=2, sticky=W)

        self.label6 = Label(master, text="Latitude 1 [deg]")
        self.label6.grid(row=5, column=0, columnspan=2, sticky=W)

        self.label7 = Label(master, text="Latitude 2 [deg]")
        self.label7.grid(row=6, column=0, columnspan=2, sticky=W)

        self.label9 = Label(master, text="Geometry of expected vent position")
        self.label9.grid(row=11, column=0, columnspan=2, sticky=W)

        self.label10 = Label(master, text="Longitude Collapse [deg]")
        self.label10.grid(row=7, column=0, columnspan=2, sticky=W)

        self.label11 = Label(master, text="Latitude Collapse [deg]")
        self.label11.grid(row=8, column=0, columnspan=2, sticky=W)

        self.label12 = Label(master, text="East Coordinate Colapse [m]", state = 'disabled')
        self.label12.grid(row=9, column=0, columnspan=2, sticky=W)

        self.label13 = Label(master, text="North Coordinate Colapse [m]", state = 'disabled')
        self.label13.grid(row=10, column=0, columnspan=2, sticky=W)

        self.label14 = Label(master, text="Azimuth Line [deg]", state = 'disabled')
        self.label14.grid(row=12, column=0, columnspan=2, sticky=W)

        self.label15 = Label(master, text="Length Line [m]", state = 'disabled')
        self.label15.grid(row=13, column=0, columnspan=2, sticky=W)

        self.label16 = Label(master, text="Radius (Circumference arch) [m]", state = 'disabled')
        self.label16.grid(row=14, column=0, columnspan=2, sticky=W)

        self.label17 = Label(master, text="Initial angle (Circumference arch) [deg]", state = 'disabled')
        self.label17.grid(row=15, column=0, columnspan=2, sticky=W)

        self.label18 = Label(master, text="Final angle (Circumference arch) [deg]", state = 'disabled')
        self.label18.grid(row=16, column=0, columnspan=2, sticky=W)

        self.label19 = Label(master, text="Uncertainty of vent position [m]")
        self.label19.grid(row=17, column=0, columnspan=2, sticky=W)

        self.label20 = Label(master, text="Collapsing volume [m^3]")
        self.label20.grid(row=4, column=3, columnspan=2, sticky=W)

        self.label21 = Label(master, text="Uncertainty of collapsing volume [m^3]")
        self.label21.grid(row=5, column=3, columnspan=2, sticky=W)

        self.label22 = Label(master, text="Sedimentation velocity [m/s]")
        self.label22.grid(row=6, column=3, columnspan=2, sticky=W)

        self.label23 = Label(master, text="Uncertainty of sedimentation velocity [m/s]")
        self.label23.grid(row=7, column=3, columnspan=2, sticky=W)

        self.label23a = Label(master, text="Initial particle concentration")
        self.label23a.grid(row=8, column=3, columnspan=2, sticky=W)

        self.label23b = Label(master, text="Uncertainty of initial particle concentration")
        self.label23b.grid(row=9, column=3, columnspan=2, sticky=W)

        self.label23c = Label(master, text="Froude number")
        self.label23c.grid(row=10, column=3, columnspan=2, sticky=W)

        self.label23d = Label(master, text="Uncertainty of Froude number")
        self.label23d.grid(row=11, column=3, columnspan=2, sticky=W)

        self.label23e = Label(master, text="Solid particle density [kg/m^3]")
        self.label23e.grid(row=12, column=3, columnspan=2, sticky=W)

        self.label23f = Label(master, text="Uncertainty of solid particle density [kg/m^3]")
        self.label23f.grid(row=13, column=3, columnspan=2, sticky=W)

        self.label23g = Label(master, text="Gas density [kg/m^3]")
        self.label23g.grid(row=14, column=3, columnspan=2, sticky=W)

        self.label23h = Label(master, text="Uncertainty of gas density [kg/m^3]")
        self.label23h.grid(row=15, column=3, columnspan=2, sticky=W)

        self.label24 = Label(master, text="Probability distribution of input parameters")
        self.label24.grid(row=3, column=3, columnspan=2, sticky=W)

        self.label8 = Label(master, text="Maximum order of conoids")
        self.label8.grid(row=16, column=3, columnspan=2, sticky=W)

        self.label25 = Label(master, text="Number of simulations")
        self.label25.grid(row=17, column=3, columnspan=2, sticky=W)

        self.inputdata = OptionMenu(master, self.var_input, "Set manually", "Input File", command = self.opt_input)
        self.inputdata.grid(row=0, column=2, columnspan=4, sticky=W+E)

        self.runname = Entry(master, textvariable=run_name)
        self.runname.grid(row=1, column=2, columnspan=4, sticky=W+E)

        self.sourcedem = OptionMenu(master, self.var_dem, "STRM 30 m", "Input DEM (utm)", "Input DEM (lat,lon)", command = self.opt_dem)
        self.sourcedem.grid(row=2, column=2, columnspan=4, sticky=W+E)

        self.lon1 = Entry(master, textvariable=lon1)
        self.lon1.grid(row=3, column=2, sticky=W+E)

        self.lon2 = Entry(master, textvariable=lon2)
        self.lon2.grid(row=4, column=2, sticky=W+E)

        self.lat1 = Entry(master, textvariable=lat1)
        self.lat1.grid(row=5, column=2, sticky=W+E)

        self.lat2 = Entry(master, textvariable=lat2)
        self.lat2.grid(row=6, column=2, sticky=W+E)

        self.vent_dist = OptionMenu(master, self.var_ds, "Punctual", "Linear", "Circumference arch", command = self.opt_geom)
        self.vent_dist.grid(row=11, column=2, sticky=W+E)

        self.lon_cen = Entry(master, textvariable=lon_cen)
        self.lon_cen.grid(row=7, column=2, sticky=W+E)

        self.lat_cen = Entry(master, textvariable=lat_cen)
        self.lat_cen.grid(row=8, column=2, sticky=W+E)

        self.east_cen = Entry(master, textvariable=east_cen, state = 'disabled')
        self.east_cen.grid(row=9, column=2, sticky=W+E)

        self.north_cen = Entry(master, textvariable=north_cen, state = 'disabled')
        self.north_cen.grid(row=10, column=2, sticky=W+E)

        self.azimuth_line = Entry(master, textvariable=azimuth_line, state = 'disabled')
        self.azimuth_line.grid(row=12, column=2, sticky=W+E)

        self.length_line = Entry(master, textvariable=length_line, state = 'disabled')
        self.length_line.grid(row=13, column=2, sticky=W+E)

        self.radius_rad = Entry(master, textvariable=radius_rad, state = 'disabled')
        self.radius_rad.grid(row=14, column=2, sticky=W+E)

        self.ang1_rad = Entry(master, textvariable=ang1_rad, state = 'disabled')
        self.ang1_rad.grid(row=15, column=2, sticky=W+E)

        self.ang2_rad = Entry(master, textvariable=ang2_rad, state = 'disabled')
        self.ang2_rad.grid(row=16, column=2, sticky=W+E)

        self.cen_var = Entry(master, textvariable=cen_var)
        self.cen_var.grid(row=17, column=2, sticky=W+E)

        self.volume = Entry(master, textvariable=volume)
        self.volume.grid(row=4, column=5, sticky=W+E)

        self.var_volume = Entry(master, textvariable=var_volume)
        self.var_volume.grid(row=5, column=5, sticky=W+E)

        self.ws = Entry(master, textvariable=ws)
        self.ws.grid(row=6, column=5, sticky=W+E)

        self.var_ws = Entry(master, textvariable=var_ws)
        self.var_ws.grid(row=7, column=5, sticky=W+E)

        self.phi0 = Entry(master, textvariable=phi0)
        self.phi0.grid(row=8, column=5, sticky=W+E)

        self.var_phi0 = Entry(master, textvariable=var_phi0)
        self.var_phi0.grid(row=9, column=5, sticky=W+E)

        self.Fr = Entry(master, textvariable=Fr)
        self.Fr.grid(row=10, column=5, sticky=W+E)

        self.var_Fr = Entry(master, textvariable=var_Fr)
        self.var_Fr.grid(row=11, column=5, sticky=W+E)

        self.rhop = Entry(master, textvariable=rhop)
        self.rhop.grid(row=12, column=5, sticky=W+E)

        self.var_rhop = Entry(master, textvariable=var_rhop)
        self.var_rhop.grid(row=13, column=5, sticky=W+E)

        self.rhog = Entry(master, textvariable=rhog)
        self.rhog.grid(row=14, column=5, sticky=W+E)

        self.var_rhog = Entry(master, textvariable=var_rhog)
        self.var_rhog.grid(row=15, column=5, sticky=W+E)

        self.input_dist = OptionMenu(master, self.var_d_input, "Uniform", "Gaussian")
        self.input_dist.grid(row=3, column=5, sticky=W+E)

        self.Nsim = Entry(master, textvariable=N)
        self.Nsim.grid(row=17,column=5, sticky=W+E)

        self.conoid_levels = Entry(master, textvariable=conoid_levels)
        self.conoid_levels.grid(row=16, column=5, sticky=W+E)

        self.simulation = Button(master, text = "Run simulation", command = self.runcode)
        self.simulation.grid(row=18, column = 0, columnspan=6, sticky=W+E)

        self.plot1 = Button(master, text = "Plot Output Map", command = self.figure_1, state = 'disabled')
        self.plot1.grid(row=19, column = 0, columnspan=2 , sticky=W+E)

        self.plot2 = Button(master, text = "Histograms", command = self.figure_2, state = 'disabled')
        self.plot2.grid(row=19, column = 2, columnspan=2 , sticky=W+E)

        self.plot3 = Button(master, text = "Scatter Plots", command = self.figure_3, state = 'disabled')
        self.plot3.grid(row=19, column = 4, columnspan=2 , sticky=W+E)

    def opt_geom(self, opt):

        if(opt == "Punctual"):
            self.label14.configure(state = 'disabled')
            self.label15.configure(state = 'disabled')
            self.label16.configure(state = 'disabled')
            self.label17.configure(state = 'disabled')
            self.label18.configure(state = 'disabled')
            self.azimuth_line.configure(state = 'disabled')
            self.length_line.configure(state = 'disabled')
            self.radius_rad.configure(state = 'disabled')
            self.ang1_rad.configure(state = 'disabled')
            self.ang2_rad.configure(state = 'disabled')
        if(opt == "Linear"):
            self.label14.configure(state = 'normal')
            self.label15.configure(state = 'normal')
            self.label16.configure(state = 'disabled')
            self.label17.configure(state = 'disabled')
            self.label18.configure(state = 'disabled')
            self.azimuth_line.configure(state = 'normal')
            self.length_line.configure(state = 'normal')
            self.radius_rad.configure(state = 'disabled')
            self.ang1_rad.configure(state = 'disabled')
            self.ang2_rad.configure(state = 'disabled')
        if(opt == "Circumference arch"):
            self.label14.configure(state = 'disabled')
            self.label15.configure(state = 'disabled')
            self.label16.configure(state = 'normal')
            self.label17.configure(state = 'normal')
            self.label18.configure(state = 'normal')
            self.azimuth_line.configure(state = 'disabled')
            self.length_line.configure(state = 'disabled')
            self.radius_rad.configure(state = 'normal')
            self.ang1_rad.configure(state = 'normal')
            self.ang2_rad.configure(state = 'normal')

    def opt_input(self, opt):
        if(opt == "Set manually"):
            self.label2.configure(state = 'normal')
            self.label3.configure(state = 'normal')
            self.label4.configure(state = 'normal')
            self.label5.configure(state = 'normal')
            self.label6.configure(state = 'normal')
            self.label7.configure(state = 'normal')
            self.label8.configure(state = 'normal')
            self.label9.configure(state = 'normal')
            self.label10.configure(state = 'normal')
            self.label11.configure(state = 'normal')
            self.label12.configure(state = 'normal')
            self.label13.configure(state = 'normal')
            self.label14.configure(state = 'normal')
            self.label15.configure(state = 'normal')
            self.label16.configure(state = 'normal')
            self.label17.configure(state = 'normal')
            self.label18.configure(state = 'normal')
            self.label19.configure(state = 'normal')
            self.label20.configure(state = 'normal')
            self.label21.configure(state = 'normal')
            self.label22.configure(state = 'normal')
            self.label23.configure(state = 'normal')
            self.label23a.configure(state = 'normal')
            self.label23b.configure(state = 'normal')
            self.label23c.configure(state = 'normal')
            self.label23d.configure(state = 'normal')
            self.label23e.configure(state = 'normal')
            self.label23f.configure(state = 'normal')
            self.label23g.configure(state = 'normal')
            self.label23h.configure(state = 'normal')
            self.label24.configure(state = 'normal')
            self.label25.configure(state = 'normal')
            self.runname.configure(state = 'normal')
            self.sourcedem.configure(state = 'normal')
            self.lon1.configure(state = 'normal')
            self.lon2.configure(state = 'normal')
            self.lat1.configure(state = 'normal')
            self.lat2.configure(state = 'normal')
            self.conoid_levels.configure(state = 'normal')
            self.vent_dist.configure(state = 'normal')
            self.lon_cen.configure(state = 'normal')
            self.lat_cen.configure(state = 'normal')
            self.east_cen.configure(state = 'normal')
            self.north_cen.configure(state = 'normal')
            self.azimuth_line.configure(state = 'normal')
            self.length_line.configure(state = 'normal')
            self.radius_rad.configure(state = 'normal')
            self.ang1_rad.configure(state = 'normal')
            self.ang2_rad.configure(state = 'normal')
            self.cen_var.configure(state = 'normal')
            self.volume.configure(state = 'normal')
            self.var_volume.configure(state = 'normal')
            self.ws.configure(state = 'normal')
            self.var_ws.configure(state = 'normal')
            self.phi0.configure(state = 'normal')
            self.var_phi0.configure(state = 'normal')
            self.Fr.configure(state = 'normal')
            self.var_Fr.configure(state = 'normal')
            self.rhop.configure(state = 'normal')
            self.var_rhop.configure(state = 'normal')
            self.rhog.configure(state = 'normal')
            self.var_rhog.configure(state = 'normal')
            self.input_dist.configure(state = 'normal')
            self.Nsim.configure(state = 'normal')
            self.opt_dem(self.var_dem.get())
            self.opt_geom(self.var_ds.get())
        if(opt == "Input File"):
            self.label2.configure(state = 'disabled')
            self.label3.configure(state = 'disabled')
            self.label4.configure(state = 'disabled')
            self.label5.configure(state = 'disabled')
            self.label6.configure(state = 'disabled')
            self.label7.configure(state = 'disabled')
            self.label8.configure(state = 'disabled')
            self.label9.configure(state = 'disabled')
            self.label10.configure(state = 'disabled')
            self.label11.configure(state = 'disabled')
            self.label12.configure(state = 'disabled')
            self.label13.configure(state = 'disabled')
            self.label14.configure(state = 'disabled')
            self.label15.configure(state = 'disabled')
            self.label16.configure(state = 'disabled')
            self.label17.configure(state = 'disabled')
            self.label18.configure(state = 'disabled')
            self.label19.configure(state = 'disabled')
            self.label20.configure(state = 'disabled')
            self.label21.configure(state = 'disabled')
            self.label22.configure(state = 'disabled')
            self.label23.configure(state = 'disabled')
            self.label23a.configure(state = 'disabled')
            self.label23b.configure(state = 'disabled')
            self.label23c.configure(state = 'disabled')
            self.label23d.configure(state = 'disabled')
            self.label23e.configure(state = 'disabled')
            self.label23f.configure(state = 'disabled')
            self.label23g.configure(state = 'disabled')
            self.label23h.configure(state = 'disabled')
            self.label24.configure(state = 'disabled')
            self.label25.configure(state = 'disabled')
            self.runname.configure(state = 'disabled')
            self.sourcedem.configure(state = 'disabled')
            self.lon1.configure(state = 'disabled')
            self.lon2.configure(state = 'disabled')
            self.lat1.configure(state = 'disabled')
            self.lat2.configure(state = 'disabled')
            self.conoid_levels.configure(state = 'disabled')
            self.vent_dist.configure(state = 'disabled')
            self.lon_cen.configure(state = 'disabled')
            self.lat_cen.configure(state = 'disabled')
            self.east_cen.configure(state = 'disabled')
            self.north_cen.configure(state = 'disabled')
            self.azimuth_line.configure(state = 'disabled')
            self.length_line.configure(state = 'disabled')
            self.radius_rad.configure(state = 'disabled')
            self.ang1_rad.configure(state = 'disabled')
            self.ang2_rad.configure(state = 'disabled')
            self.cen_var.configure(state = 'disabled')
            self.volume.configure(state = 'disabled')
            self.var_volume.configure(state = 'disabled')
            self.ws.configure(state = 'disabled')
            self.var_ws.configure(state = 'disabled')
            self.phi0.configure(state = 'disabled')
            self.var_phi0.configure(state = 'disabled')
            self.Fr.configure(state = 'disabled')
            self.var_Fr.configure(state = 'disabled')
            self.rhop.configure(state = 'disabled')
            self.var_rhop.configure(state = 'disabled')
            self.rhog.configure(state = 'disabled')
            self.var_rhog.configure(state = 'disabled')
            self.input_dist.configure(state = 'disabled')
            self.Nsim.configure(state = 'disabled')

    def opt_dem(self, opt):
        if(opt == "STRM 30 m"):
            self.label4.configure(state = 'normal')
            self.label5.configure(state = 'normal')
            self.label6.configure(state = 'normal')
            self.label7.configure(state = 'normal')
            self.label10.configure(state = 'normal')
            self.label11.configure(state = 'normal')
            self.label12.configure(state = 'normal')
            self.label13.configure(state = 'normal')
            self.lon1.configure(state = 'normal')
            self.lon2.configure(state = 'normal')
            self.lat1.configure(state = 'normal')
            self.lat2.configure(state = 'normal')
            self.lon_cen.configure(state = 'normal')
            self.lat_cen.configure(state = 'normal')
            self.east_cen.configure(state = 'disabled')
            self.north_cen.configure(state = 'disabled')
        if(opt == "Input DEM (utm)"):
            self.label4.configure(state = 'disabled')
            self.label5.configure(state = 'disabled')
            self.label6.configure(state = 'disabled')
            self.label7.configure(state = 'disabled')
            self.label10.configure(state = 'disabled')
            self.label11.configure(state = 'disabled')
            self.label12.configure(state = 'normal')
            self.label13.configure(state = 'normal')
            self.lon1.configure(state = 'disabled')
            self.lon2.configure(state = 'disabled')
            self.lat1.configure(state = 'disabled')
            self.lat2.configure(state = 'disabled')
            self.lon_cen.configure(state = 'disabled')
            self.lat_cen.configure(state = 'disabled')
            self.east_cen.configure(state = 'normal')
            self.north_cen.configure(state = 'normal')
        if(opt == "Input DEM (lat,lon)"):
            self.label4.configure(state = 'disabled')
            self.label5.configure(state = 'disabled')
            self.label6.configure(state = 'disabled')
            self.label7.configure(state = 'disabled')
            self.label10.configure(state = 'normal')
            self.label11.configure(state = 'normal')
            self.label12.configure(state = 'disabled')
            self.label13.configure(state = 'disabled')
            self.lon1.configure(state = 'disabled')
            self.lon2.configure(state = 'disabled')
            self.lat1.configure(state = 'disabled')
            self.lat2.configure(state = 'disabled')
            self.lon_cen.configure(state = 'normal')
            self.lat_cen.configure(state = 'normal')
            self.east_cen.configure(state = 'disabled')
            self.north_cen.configure(state = 'disabled')

    def figure_1(self):

        fig1 = plt.figure()
        cmapg = plt.cm.get_cmap('Greys')
        cmapr = plt.cm.get_cmap('Reds')
        cmaps = plt.cm.get_cmap('Blues') 

        if( self.s_dem == 1 or self.s_dem == 3):
            if( self.N > 1 ):
                CS_Topo = plt.contourf(self.matrix_lon,self.matrix_lat,self.topography, 100, alpha = 1.0, cmap = cmapg ,antialiased=True)
                CS_Sea = plt.contourf(self.matrix_lon,self.matrix_lat,self.topography_sea, 100, alpha = 0.5, cmap = cmaps ,antialiased=True)
                CS = plt.contourf(self.matrix_lon, self.matrix_lat, self.N * self.data_cones, 100, vmin = 0.0, vmax = 1.0,  alpha= 0.3, interpolation='linear', cmap=cmapr, antialiased=True)
                fmt = '%.2f'
                plt.colorbar()
                CS_lines = plt.contour(self.matrix_lon,self.matrix_lat, self.N * self.data_cones, np.array([self.val_down, self.val_up]), colors='r', interpolation='linear', linewidths = 0.1)
                plt.clabel(CS_lines, inline=0.1, fontsize = 7, colors='k', fmt=fmt)

                plt.axes().set_aspect(self.step_lat_m/self.step_lon_m)
                plt.xlabel('Longitude $[^\circ]$')
                plt.ylabel('Latitude $[^\circ]$')
                plt.xlim(self.plot_lon1, self.plot_lon2 )
                plt.ylim(self.plot_lat1, self.plot_lat2 )
                plt.plot(self.lon_vector, self.lat_vector, 'b.')
            else:
                CS_Topo = plt.contourf(self.matrix_lon,self.matrix_lat,self.topography, 100, alpha = 1.0, cmap = cmapg ,antialiased=True)
                CS_Sea = plt.contourf(self.matrix_lon,self.matrix_lat,self.topography_sea, 100, alpha = 0.5, cmap = cmaps ,antialiased=True)
                CS = plt.contourf(self.matrix_lon, self.matrix_lat, self.data_cones, 100, alpha= 0.3, cmap=cmapr, antialiased=True)
                plt.axes().set_aspect(self.step_lat_m/self.step_lon_m)
                plt.xlabel('Longitude $[^\circ]$')
                plt.ylabel('Latitude $[^\circ]$')
                plt.xlim(self.plot_lon1, self.plot_lon2 )
                plt.ylim(self.plot_lat1, self.plot_lat2 )
                plt.plot(self.lon_vector, self.lat_vector, 'b.')

        else:
            if( self.N > 1 ):
                CS_Topo = plt.contourf(self.matrix_east,self.matrix_north,self.topography, 100, alpha = 1.0, cmap = cmapg ,antialiased=True)
                CS_Sea = plt.contourf(self.matrix_east,self.matrix_north,self.topography_sea, 100, alpha = 0.5, cmap = cmaps ,antialiased=True)
                CS = plt.contourf(self.matrix_east, self.matrix_north, self.N * self.data_cones, 100, vmin = 0.0, vmax = 1.0,  alpha= 0.3, interpolation='linear', cmap=cmapr, antialiased=True)	
                fmt = '%.2f'
                plt.colorbar()
                CS_lines = plt.contour(self.matrix_east,self.matrix_north, self.N * self.data_cones, np.array([self.val_down, self.val_up]), colors='r', interpolation='linear', linewidths = 0.1)
                plt.clabel(CS_lines, inline=0.1, fontsize = 7, colors='k', fmt=fmt)

                plt.axes().set_aspect(1.0)
                plt.xlabel('Longitude $[^\circ]$')
                plt.ylabel('Latitude $[^\circ]$')
                plt.xlim(self.plot_east1, self.plot_east2 )
                plt.ylim(self.plot_north1, self.plot_north2 )
                plt.plot(self.east_vector, self.north_vector, 'b.')
            else:
                CS_Topo = plt.contourf(self.matrix_east,self.matrix_north,self.topography, 100, alpha = 1.0, cmap = cmapg ,antialiased=True)
                CS_Sea = plt.contourf(self.matrix_east,self.matrix_north,self.topography_sea, 100, alpha = 0.5, cmap = cmaps ,antialiased=True)
                CS = plt.contourf(self.matrix_east, self.matrix_north, self.data_cones, 100, alpha= 0.3, cmap=cmapr, antialiased=True)
                plt.axes().set_aspect(1.0)
                plt.xlabel('Longitude $[^\circ]$')
                plt.ylabel('Latitude $[^\circ]$')
                plt.xlim(self.plot_east1, self.plot_east2 )
                plt.ylim(self.plot_north1, self.plot_north2 )
                plt.plot(self.east_vector, self.north_vector, 'b.')

        plt.show(fig1)

    def figure_2(self):

        fig2 = plt.figure()
        plt.subplot(231)
        plt.hist(self.volume_vector)
        plt.xlabel('Collapsing volume $[m^3]$')
        plt.subplot(232)
        plt.hist(self.ws_vector)
        plt.xlabel('Sedimentation velocity $[m/s]$')
        plt.subplot(233)
        plt.hist(self.phi_0_vector)
        plt.xlabel('Initial particle concentration')
        plt.subplot(234)
        plt.hist(self.Fr_vector)
        plt.xlabel('Froude number')
        plt.subplot(235)
        plt.hist(self.rho_p_vector)
        plt.xlabel('Solid particle density $[kg/m^3]$')
        plt.subplot(236)
        plt.hist(self.rho_gas_vector)
        plt.xlabel('Gas density $[kg/m^3]$')
        plt.show(fig2)

    def figure_3(self):

        fig3 = plt.figure()
        plt.plot(self.distance_vector, self.inundation_vector, 'b.')
        plt.xlabel('Runout distance $[km]$')
        plt.ylabel('Inundation area $[km^2]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 * np.max(self.inundation_vector)+1))
        plt.xlim(xmin=0)
        plt.xlim(xmax=np.floor(1.1 *np.max(self.distance_vector)+1))

        fig4 = plt.figure()
        plt.subplot(231)
        plt.plot(self.volume_vector, self.distance_vector, 'b.')
        plt.xlabel('Collapsing volume $[m^3]$')
        plt.ylabel('Runout distance $[km]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.distance_vector)+1))
        plt.subplot(232)
        plt.plot(self.ws_vector, self.distance_vector, 'b.')
        plt.xlabel('Sedimentation velocity $[m/s]$')
        plt.ylabel('Runout distance $[km]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.distance_vector)+1))
        plt.subplot(233)
        plt.plot(self.phi_0_vector, self.distance_vector, 'b.')
        plt.xlabel('Initial particle concentration')
        plt.ylabel('Runout distance $[km]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.distance_vector)+1))
        plt.subplot(234)
        plt.plot(self.Fr_vector, self.distance_vector, 'b.')
        plt.xlabel('Froude number')
        plt.ylabel('Runout distance $[km]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.distance_vector)+1))
        plt.subplot(235)
        plt.plot(self.rho_p_vector, self.distance_vector, 'b.')
        plt.xlabel('Solid particle density $[kg/m^3]$')
        plt.ylabel('Runout distance $[km]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.distance_vector)+1))
        plt.subplot(236)
        plt.plot(self.rho_gas_vector, self.distance_vector, 'b.')
        plt.xlabel('Gas density $[kg/m^3]$')
        plt.ylabel('Runout distance $[km]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.distance_vector)+1))

        fig5 = plt.figure()
        plt.subplot(231)
        plt.plot(self.volume_vector, self.inundation_vector, 'b.')
        plt.xlabel('Collapsing volume $[m^3]$')
        plt.ylabel('Inundation area $[km^2]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.inundation_vector)+1))
        plt.subplot(232)
        plt.plot(self.ws_vector, self.inundation_vector, 'b.')
        plt.xlabel('Sedimentation velocity $[m/s]$')
        plt.ylabel('Inundation area $[km^2]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.inundation_vector)+1))
        plt.subplot(233)
        plt.plot(self.phi_0_vector, self.inundation_vector, 'b.')
        plt.xlabel('Initial particle concentration')
        plt.ylabel('Inundation area $[km^2]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.inundation_vector)+1))
        plt.subplot(234)
        plt.plot(self.Fr_vector, self.inundation_vector, 'b.')
        plt.xlabel('Froude number')
        plt.ylabel('Inundation area $[km^2]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.inundation_vector)+1))
        plt.subplot(235)
        plt.plot(self.rho_p_vector, self.inundation_vector, 'b.')
        plt.xlabel('Solid particle density $[kg/m^3]$')
        plt.ylabel('Inundation area $[km^2]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.inundation_vector)+1))
        plt.subplot(236)
        plt.plot(self.rho_gas_vector, self.inundation_vector, 'b.')
        plt.xlabel('Gas density $[kg/m^3]$')
        plt.ylabel('Inundation area $[km^2]$')
        plt.ylim(ymin=0)
        plt.ylim(ymax=np.floor(1.1 *np.max(self.inundation_vector)+1))

        plt.show([fig3,fig4,fig5])

    def runcode(self):

        print('\n Run simulation \n')

        self.current_path = os.getcwd()
        if(self.var_input.get() == 'Input File'):
                try:
                        file_txt = open('input_data.py')
                        file_txt.close()
                except: 
                        messagebox.showerror("Error", 'input_data.py not found in ' + str(self.current_path))
                        return
                self.modify_input()
                os.system('python BoxMapProb.py')
        else:
                if(self.var_dem.get() == "Input DEM (utm)"):
                        try:
                                file_txt = open('input_DEM.asc')
                                file_txt.close()
                        except: 
                                messagebox.showerror("Error", 'input_DEM.asc not found in ' + str(self.current_path))
                                return
                if(self.var_dem.get() == "Input DEM (lat,lon)"):
                        try:
                                file_txt = open('Topography_3.asc')
                                file_txt.close()
                        except: 
                                messagebox.showerror("Error", 'Topography_3.asc not found in ' + str(self.current_path))
                                return
                self.create_input()
                os.system('python BoxMapProb.py')

        file_txt = open('input_data.py')
        line = file_txt.readlines()
        file_txt.close()

        self.run_name = 'run_default'
        self.N = 1
        self.s_dem = 1
        for i in range(0,len(line)):
                line[i] = line[i].replace('=',' ')
                aux = line[i].split()
                if(len(aux) > 0):
                    if( aux[0][0] != '#'):
                        if( aux[0] == 'run_name'):
                            self.run_name = aux[1]
                        if( aux[0] == 'N'):
                            self.N = int(aux[1])
                        if( aux[0] == 'source_dem'):
                            self.s_dem = int(aux[1])

        try:
                file_txt = open('Results/' + self.run_name + '/log.txt')
                line = file_txt.readlines()
                file_txt.close()
        except:
                self.plot1.configure(state = 'disabled')
                self.plot2.configure(state = 'disabled')
                self.plot3.configure(state = 'disabled')
                messagebox.showerror("Error", 'Simulations were not performed. Problems with input parameters')
                return

        if( float(line[0]) == 0):
            self.plot1.configure(state = 'disabled')
            self.plot2.configure(state = 'disabled')
            self.plot3.configure(state = 'disabled')
            messagebox.showerror("Error", 'Simulations were not performed. Problems with input parameters')
            return

        if( self.s_dem == 1 or self.s_dem == 3):
            self.matrix_lat = np.loadtxt(self.current_path + "/Results/" + self.run_name + "/matrix_lat.txt")
            self.matrix_lon = np.loadtxt(self.current_path + "/Results/" + self.run_name + "/matrix_lon.txt")
        else:
            self.matrix_east = np.loadtxt(self.current_path + "/Results/" + self.run_name + "/matrix_east.txt")
            self.matrix_north = np.loadtxt(self.current_path + "/Results/" + self.run_name + "/matrix_north.txt")

        self.data_cones = np.loadtxt(self.current_path + "/Results/" + self.run_name + "/data_cones.txt")
        self.topography = np.loadtxt(self.current_path + "/Results/" + self.run_name + "/topography.txt")
        summary = np.loadtxt(self.current_path + "/Results/" + self.run_name + "/summary.txt")

        if( self.s_dem == 1 or self.s_dem == 3):
            self.plot_lon1 = np.amin(self.matrix_lon)
            self.plot_lon2 = np.amax(self.matrix_lon)
            self.plot_lat1 = np.amin(self.matrix_lat)
            self.plot_lat2 = np.amax(self.matrix_lat)
            cells_lon = len(self.matrix_lon[1,:])
            cells_lat = len(self.matrix_lon[:,1])

            utm1 = utm.from_latlon(self.plot_lat1,self.plot_lon1)
            utm2 = utm.from_latlon(self.plot_lat2,self.plot_lon2)

            if( utm1[2] == utm2[2] and utm1[3] == utm2[3] ):
                distance_lon = abs(utm2[0] - utm1[0])
                distance_lat = abs(utm2[1] - utm1[1])
            else:
                distance_lon = distance_two_points(lat1,lat1,lon1,lon2)
                distance_lat = distance_two_points(lat1,lat2,lon1,lon1)

            self.step_lon_m = distance_lon / (cells_lon-1)
            self.step_lat_m = distance_lat / (cells_lat-1)
            if( self.N > 1 ):
                self.lon_vector = summary[0:self.N,6]
                self.lat_vector = summary[0:self.N,7]
            else:
                self.lon_vector = summary[6]
                self.lat_vector = summary[7]
        else:
            self.plot_east1 = np.amin(self.matrix_east)
            self.plot_east2 = np.amax(self.matrix_east)
            self.plot_north1  = np.amin(self.matrix_north)
            self.plot_north2 = np.amax(self.matrix_north)
            if( self.N > 1 ):
                self.east_vector = summary[0:self.N,6]
                self.north_vector = summary[0:self.N,7]
            else:
                self.east_vector = summary[6]
                self.north_vector = summary[7]

        self.topography_sea = np.loadtxt(self.current_path + "/Results/" + self.run_name + "/topography_sea.txt")
	
        self.data_cones = self.data_cones[ range(len(self.data_cones[:,0]) -1 , -1 , -1 ) , : ] / self.N
        self.line_val = self.data_cones.max()
        self.data_cones[self.data_cones[:,:] == 0] =  np.nan
        self.val_up = np.floor((self.line_val + 0.1 - 1.0 / self.N ) * 10.0) / 20.0
        if( self.val_up > 0.05 ):
            self.val_down = np.maximum( self.val_up / 10.0 , 0.05 )
        else:
            self.val_down = self.val_up / 2.0

        if( self.N > 1 ):
            self.volume_vector = summary[0:self.N,0]
            self.ws_vector = summary[0:self.N,1]
            self.phi_0_vector = summary[0:self.N,2]
            self.Fr_vector = summary[0:self.N,3]
            self.rho_p_vector = summary[0:self.N,4]
            self.rho_gas_vector = summary[0:self.N,5]
            self.distance_vector = summary[0:self.N,9]
            self.inundation_vector = summary[0:self.N,8]
        self.plot1.configure(state = 'normal')
        if( self.N == 1):
            self.plot2.configure(state = 'disabled')
            self.plot3.configure(state = 'disabled')
        else:
            self.plot2.configure(state = 'normal')
            self.plot3.configure(state = 'normal')

    def create_input(self):
        f = open('input_data.py','w')
        f.write('# Name of the run (used to save the parameters and the output)'+ '\n')
        f.write('run_name = ' + self.runname.get() + '\n')
        f.write('\n')
        f.write('# Source of DEM' + '\n')
        f.write('# source_dem = type of input data (1 => SRTM 30 m / 2 => Uploaded DEM (UTM) / 3 => Uploaded Data (lat,lon)).'+'\n')
        f.write('# topography_file = location of file containing topography (only used when source_dem = 2 or source_dem = 3).'+'\n')
        f.write('# (see examples of source_dem = 2 in EXAMPLES/Upload_DEM_UTM and of source_dem = 3 in EXAMPLES/Upload_DEM_deg).'+'\n')
        f.write('# (Simulations with source_dem = 1 and save_data = 1 create a compatible topography file for source_dem = 3 in Results' + '\n')
        f.write('# called Topography_3.txt).'+'\n')

        if( self.var_dem.get() == "STRM 30 m"):
            f.write('source_dem = 1' + '\n')
        elif( self.var_dem.get() =="Input DEM (utm)"):
            f.write('source_dem = 2' + '\n')
            f.write('topography_file = input_DEM.asc' + '\n')
        else:
            f.write('source_dem = 3' + '\n')
            f.write('topography_file = Topography_3.txt' + '\n')
        f.write('\n')
        f.write('# Map limits (only considered if source_dem = 1)' + '\n')
        f.write('# lon1 = longitude of the first limit of the map' + '\n')
        f.write('# lon2 = longitude of the second limit of the map ' + '\n')
        f.write('# lat1 = latitude of the first limit of the map' + '\n')
        f.write('# lat2 = latitude of the second limit of the map' + '\n')
        if( self.var_dem.get() == "STRM 30 m"):
            f.write('lon1 = ' +  self.lon1.get() + '\n')
            f.write('lon2 = ' +  self.lon2.get() + '\n')
            f.write('lat1 = ' +  self.lat1.get() + '\n')
            f.write('lat2 = ' +  self.lat2.get() + '\n')
        f.write('\n')
        f.write('# Maximum order of secondary collapses' + '\n')
        f.write('max_levels = ' +  self.conoid_levels.get() + '\n')
        f.write('\n')
        f.write('# Probability distribution of collapse location (1 => Punctual / 2 => Linear / 3 => Circumference arch)' + '\n')
        if( self.var_ds.get() == "Punctual"):
            f.write('dist_source = 1' + '\n')
        elif( self.var_ds.get() == "Linear"):
            f.write('dist_source = 2' + '\n')
        else:
            f.write('dist_source = 3' + '\n')
        f.write('\n')
        f.write('# Parameters of the collapse location' + '\n')
        f.write('# lon_cen = longitude of the collapse zone center (only considered if source_dem = 1 or 3)' + '\n')
        f.write('# lat_cen = latitude of the collapse zone center (only considered if source_dem = 1 or 3)' + '\n')
        f.write('# east_cen = east coordinate of collapse zone center (only considered if source_dem = 2)' + '\n')
        f.write('# north_cen = north coordinate of collapse zone center (only considered if source_dem = 2)' + '\n')
        f.write('# var_cen = uncertainty of collapse position (in meters)' + '\n')
        f.write('# azimuth_lin = azimuth of the line that define the collapse zone (in degrees, only considered if dist_source = 2)' + '\n')
        f.write('# length_lin = length of the line that define the collapse zone (in meters, only considered if dist_source = 2)' + '\n')
        f.write('# radius_rad = radius of the circumference arch that define the collapse zone (in meters, only considered if dist_source = 3)' + '\n')
        f.write('# ang1_rad = initial angle of the circumference arch that define the collapse zone (in degrees, only considered if dist_source = 3. Anticlockwise)' + '\n')
        f.write('# ang2_rad = initial angle of the circumference arch that define the collapse zone (in degrees, only considered if dist_source = 3. Anticlockwise)' + '\n')
        if( self.var_dem.get() == "Input DEM (utm)"):
            f.write('east_cen = ' + self.east_cen.get() + '\n')
            f.write('north_cen = ' + self.north_cen.get() + '\n')
        else:
            f.write('lon_cen = ' + self.lon_cen.get() + '\n')
            f.write('lat_cen = ' + self.lat_cen.get() + '\n')
        f.write('var_cen = ' + self.cen_var.get() + '\n')
        if( self.var_ds.get() == "Linear"):
            f.write('azimuth_lin = ' + self.azimuth_line.get() + '\n')
            f.write('length_lin = ' + self.length_line.get() + '\n')
        elif( self.var_ds.get() == "Circumference arch"):
            f.write('radius_rad = ' + self.radius_rad.get() + '\n')
            f.write('ang1_rad = ' + self.ang1_rad.get() + '\n')
            f.write('ang2_rad = ' + self.ang2_rad.get() + '\n')
        f.write('\n')
        f.write('# Other parameters of box model' + '\n')
        f.write('# volume = collapsing volume (in cubic meters)' + '\n')
        f.write('# ws = sedimentation velocity (m/s)' + '\n')
        f.write('# phi_0 = initial concentration of particles' + '\n')
        f.write('# Fr = Froude Number' + '\n')
        f.write('# rho_p = pyroclast density (in kg/m3) ' + '\n')
        f.write('# rho_gas = gas density in PDC (in kg/m3)' + '\n')
        f.write('# var_volume = uncertainty of collapsing volume (in cubic meters)' + '\n')
        f.write('# var_ws = uncertainty of sedimentation velocity (m/s)' + '\n')
        f.write('# var_phi_0 = uncertainty of initial concentration of particles ' + '\n')
        f.write('# var_Fr = uncertainty of Fr' + '\n')
        f.write('# var_rho_p = uncertainty of pyroclast density (in kg/m3)' + '\n')
        f.write('# var_rho_gas = uncertainty of gas density (in kg/m3)' + '\n')
        f.write('# dist_input = type of distribution for volume, ws, phi_0, Fr, rho_p and rho_gas (1 => Gaussian / 2 => Uniform)' + '\n')
        f.write('volume = ' + self.volume.get() + '\n')
        f.write('ws = ' + self.ws.get() + '\n')
        f.write('phi_0 = ' + self.phi0.get() + '\n')
        f.write('Fr = ' + self.Fr.get() + '\n')
        f.write('rho_p = ' + self.rhop.get() + '\n')
        f.write('rho_gas = ' + self.rhog.get() + '\n')
        f.write('var_volume = ' + self.var_volume.get() + '\n')
        f.write('var_ws = ' + self.var_ws.get() + '\n')
        f.write('var_phi_0 = ' + self.var_phi0.get() + '\n')
        f.write('var_Fr = ' + self.var_Fr.get() + '\n')
        f.write('var_rho_p = ' + self.var_rhop.get() + '\n')
        f.write('var_rho_gas = ' + self.var_rhog.get() + '\n')
        if( self.var_d_input.get() == "Gaussian"):
            f.write('dist_input = 1' + '\n')
        else:
            f.write('dist_input = 2' + '\n')
        f.write('\n')
        f.write('# Number of simulations computed by the code' + '\n')
        f.write('N = ' + self.Nsim.get() + '\n')
        f.write('\n')
        f.write('# Save results in files txt ( 1 => Yes / 0 => No )' + '\n')
        f.write('save_data = 1' + '\n')
        f.write('\n')
        f.write('# Assumption for redistributing pyroclastic material (1, 2, 3 or 4. Please use 4)' + '\n')
        f.write('redist_energy = 4' + '\n')
        f.write('\n')
        f.write('# Additional inputs (only for friendly version)' + '\n')
        f.write('plot_flag = 0' + '\n')
        f.write('sea_flag = 1' + '\n')
        f.close()

    def modify_input(self):
        current_path = os.getcwd()
        file_txt = open('input_data.py')
        line = file_txt.readlines()
        file_txt.close()

        plot_flag = 1
        sea_flag = 0
        save_data = 0
        for i in range(0,len(line)):
            line[i] = line[i].replace('=',' ')
            aux = line[i].split()
            if(len(aux) > 0):
                if( aux[0][0] != '#'):
                    if( aux[0] == 'plot_flag'):
                        plot_flag = int(aux[1])
                    if( aux[0] == 'sea_flag'):
                        sea_flag = int(aux[1])
                    if( aux[0] == 'save_data'):
                        save_data = int(aux[1])

        if( plot_flag == 1 or sea_flag == 0 or save_data == 0):
            f = open('input_data.py', 'a')
            f.write('\n')
            f.write('# Additional inputs (only for user-friendly version)' + '\n')
            if( plot_flag == 1 ):
                f.write('plot_flag = 0' + '\n')
            if( sea_flag == 0 ):
                f.write('sea_flag = 1' + '\n')
            if( save_data == 0 ):
                f.write('save_data = 1' + '\n')
            f.close()

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
sys.exit(0)
