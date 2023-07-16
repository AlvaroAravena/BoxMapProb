from tkinter import Tk , ttk , Label , Button , W , E , Entry , OptionMenu , StringVar , DoubleVar , IntVar , Canvas , Scrollbar , VERTICAL , Frame , messagebox , filedialog
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import utm
import warnings
warnings.filterwarnings( "ignore" )
import matplotlib
matplotlib.use( "TkAgg" )
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg , NavigationToolbar2Tk )
from matplotlib.figure import Figure
from BoxMapProb_Functions import import_map , read_map_utm , read_map_deg , matrix_deg , matrix_utm , create_inputs , create_vent_deg , create_vent_utm , read_comparison_polygon_deg , read_comparison_polygon_utm , initial_definitions , definitions_save_data_deg , definitions_save_data_utm , compute_box_model_deg , compute_box_model_utm , save_data_deg , save_data_utm , plot_deg , plot_only_topography_deg , plot_only_topography_utm , plot_utm, calibration , plot_only_vent_deg, plot_only_vent_utm , plot_only_properties , plot_only_comparison_polygon_deg , plot_only_comparison_polygon_utm , plot_only_map_deg , plot_only_map_utm , plot_only_calibration , plot_input_output

class MainFrame:

	def __init__(self , master):

		self.master = master
		master.title( "BoxMapProb" )
		tab_parent = ttk.Notebook( master )
		tab1 = ttk.Frame( tab_parent )
		tab2 = ttk.Frame( tab_parent )
		tab3 = ttk.Frame( tab_parent )
		tab4 = ttk.Frame( tab_parent )

		for i in range( 6 ):
			tab1.columnconfigure( i , weight = 2 )
			tab2.columnconfigure( i , weight = 2 )
			tab3.columnconfigure( i , weight = 2 )
			tab4.columnconfigure( i , weight = 2 )
		for i in range( 15 ):
			tab1.rowconfigure( i , minsize = 30 )
			tab2.rowconfigure( i , minsize = 30 )
			tab3.rowconfigure( i , minsize = 30 )
			tab4.rowconfigure( i , minsize = 30 )

		tab_parent.add( tab1 , text = "General inputs and topography" )
		tab_parent.add( tab2 , text = "Collapse position" )
		tab_parent.add( tab3 , text = "PDC properties" )
		tab_parent.add( tab4 , text = "Run simulations" )

		self.redist_volume = 4
		self.g = 9.8
		self.save_data = 1
		self.current_path = os.getcwd()
		self.type_sim = np.nan
		self.type_sim_choice = 1
		self.boolean_polygon = 0
		self.boolean_polygon_choice = 0
		self.max_levels = 1
		self.N = np.nan
		self.N_choice = np.nan
		self.source_dem = np.nan
		self.source_dem_choice = 1
		self.topography_availability = 0
		self.topography_inputs = ""
		self.vent_type = 1
		self.vent_type_choice = 1
		self.vent_dist = 1
		self.vent_dist_choice = 1
		self.sample_vent_availability = 0
		self.vent_inputs = ""
		self.sample_cal_availability = 0
		self.calib_inputs = ""
		self.type_input = 1
		self.type_input_choice = 1
		self.dist_volume = 1
		self.dist_volume_choice = 1
		self.dist_phi_0 = 1
		self.dist_phi_0_choice = 1
		self.dist_ws = 1
		self.dist_ws_choice = 1
		self.dist_Fr = 1
		self.dist_Fr_choice = 1
		self.dist_rho_p = 1
		self.dist_rho_p_choice = 1
		self.dist_rho_gas = 1
		self.dist_rho_gas_choice = 1
		self.calibration_type = 1
		self.calibration_type_choice = 1
		self.dist_distance = 1
		self.dist_distance_choice = 1
		self.dist_area = 1
		self.dist_area_choice = 1
		self.sample_properties_availability = 0
		self.properties_inputs = ""
		self.results_availability = 0
		self.run_inputs = ""

		typesim = StringVar( master )
		typesim.set( "Default mode: Construction of PDC inundation probability map" )
		max_levels = IntVar( master )
		max_levels.set( 1 )
		Nsim = IntVar( master )
		Nsim.set( 10 )
		var_dem = StringVar( master )
		var_dem.set( "STRM 30 m" )
		lon1 = DoubleVar( master )
		lon1.set( -72.8 )
		lon2 = DoubleVar( master )
		lon2.set( -72.5 )
		lat1 = DoubleVar( master )
		lat1.set( -42.95 )
		lat2 = DoubleVar( master )
		lat2.set( -42.75 )
		self.venttype = StringVar( master )
		self.venttype.set( "Pointwise" )
		loncen = DoubleVar( master )
		loncen.set( -72.650 )
		latcen = DoubleVar( master )
		latcen.set( -42.835 )
		eastcen = DoubleVar( master )
		eastcen.set( 501000.0 )
		northcen = DoubleVar( master )
		northcen.set( 4178000.0 )
		azimuthline = DoubleVar( master )
		azimuthline.set( 0.0 )
		lengthline = DoubleVar( master )
		lengthline.set( 1000.0 )
		radcir = DoubleVar( master )
		radcir.set( 1000.0 )
		ang1cir = DoubleVar( master )
		ang1cir.set( 0.0 )
		ang2cir = DoubleVar( master )
		ang2cir.set( 90.0 )
		self.varcen = DoubleVar( master )
		self.varcen.set( 300.0 )
		ventdist = StringVar( master )
		ventdist.set( "Gaussian" )
		self.typeinput = StringVar( master )
		self.typeinput.set( "Predefined distributions" )
		self.distvolume = StringVar( master )
		self.distvolume.set( "Gaussian" )
		volume = DoubleVar( master )
		volume.set( 10000000.0 )
		var_volume = DoubleVar( master )
		var_volume.set( 2000000.0 )
		volume_k = DoubleVar( master )
		volume_k.set( 10.0 )
		volume_theta = DoubleVar( master )
		volume_theta.set( 1000000.0 )
		self.distphi_0 = StringVar( master )
		self.distphi_0.set( "Gaussian" )
		phi_0 = DoubleVar( master )
		phi_0.set( 0.010 )
		var_phi_0 = DoubleVar( master )
		var_phi_0.set( 0.005 )
		phi_0_k = DoubleVar( master )
		phi_0_k.set( 5.0 )
		phi_0_theta = DoubleVar( master )
		phi_0_theta.set( 0.02 )
		self.distws = StringVar( master )
		self.distws.set( "Gaussian" )
		ws = DoubleVar( master )
		ws.set( 0.6 )
		self.varws = DoubleVar( master )
		self.varws.set( 0.4 )
		ws_k = DoubleVar( master )
		ws_k.set( 5.0 )
		ws_theta = DoubleVar( master )
		ws_theta.set( 0.1 )
		self.distFr = StringVar( master )
		self.distFr.set( "Gaussian" )
		Fr = DoubleVar( master )
		Fr.set( 1.1 )
		self.varFr = DoubleVar( master )
		self.varFr.set( 0.1 )
		Fr_k = DoubleVar( master )
		Fr_k.set( 20.0 )
		Fr_theta = DoubleVar( master )
		Fr_theta.set( 0.05 )
		self.distrho_p = StringVar( master )
		self.distrho_p.set( "Gaussian" )
		rho_p = DoubleVar( master )
		rho_p.set( 1500.0 )
		self.varrho_p = DoubleVar( master )
		self.varrho_p.set( 200.0 )
		rho_p_k = DoubleVar( master )
		rho_p_k.set( 10.0 )
		rho_p_theta = DoubleVar( master )
		rho_p_theta.set( 100.0 )
		self.distrho_gas = StringVar( master )
		self.distrho_gas.set( "Gaussian" )
		rho_gas = DoubleVar( master )
		rho_gas.set( 1.1 )
		self.varrho_gas = DoubleVar( master )
		self.varrho_gas.set( 0.1 )
		rho_gas_k = DoubleVar( master )
		rho_gas_k.set( 20.0 )
		rho_gas_theta = DoubleVar( master )
		rho_gas_theta.set( 0.05 )
		calibrationtype = StringVar( master )
		calibrationtype.set( "Jaccard index" )		
		distdistance = StringVar( master )
		distdistance.set( "Gaussian" )
		distance = DoubleVar( master )
		distance.set( 3000.0 )
		var_distance = DoubleVar( master )
		var_distance.set( 500.0 )
		distance_k = DoubleVar( master )
		distance_k.set( 1.0 )
		distance_theta = DoubleVar( master )
		distance_theta.set( 2000.0 )
		distarea = StringVar( master )
		distarea.set( "Gaussian" )
		area = DoubleVar( master )
		area.set( 5.0 )
		var_area = DoubleVar( master )
		var_area.set( 1.0 )
		area_k = DoubleVar( master )
		area_k.set( 1.0 )
		area_theta = DoubleVar( master )
		area_theta.set( 3.0 )
		runname = StringVar( master )
		runname.set( "Default_Name" )
		
		self.label_typesim = Label( tab1 , text = "Type of simulation" )
		self.label_typesim.grid( row = 0 , column = 0 , columnspan = 3 , sticky = W )
		self.typesim_entry = OptionMenu( tab1 , typesim , "Default mode: Construction of PDC inundation probability map" , "Calibration mode: Based on the distribution of PDC runout distance or inundation area" , "Calibration mode: Including reference PDC deposit polygon" , command = self.opt_typesim )
		self.typesim_entry.grid( row = 0 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_max_levels = Label( tab1 , text = "Number of generations" )
		self.label_max_levels.grid( row = 1 , column = 0 , columnspan = 3 , sticky = W )
		self.max_levels_entry = Entry( tab1 , textvariable = max_levels )
		self.max_levels_entry.grid( row = 1 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_Nsim = Label( tab1 , text = "Number of simulations (maximum)" )
		self.label_Nsim.grid( row = 2 , column = 0 , columnspan = 3 , sticky = W )
		self.Nsim_entry = Entry( tab1 , textvariable = Nsim )
		self.Nsim_entry.grid( row = 2 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_sourcedem = Label( tab1 , text = "Source DEM" )
		self.label_sourcedem.grid( row = 3 , column = 0 , columnspan = 3 , sticky = W )
		self.sourcedem_entry = OptionMenu( tab1 , var_dem , "STRM 30 m" , "Input DEM (utm)" , "Input DEM (lat, lon)" , command = self.opt_dem )
		self.sourcedem_entry.grid( row = 3 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_lon1 = Label( tab1 , text = "Longitude 1 [deg]" )
		self.label_lon1.grid( row = 4 , column = 0 , columnspan = 3 , sticky = W )
		self.lon1_entry = Entry( tab1 , textvariable = lon1 )
		self.lon1_entry.grid( row = 4 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_lon2 = Label( tab1 , text = "Longitude 2 [deg]" )
		self.label_lon2.grid( row = 5 , column = 0 , columnspan = 3 , sticky = W )
		self.lon2_entry = Entry( tab1 , textvariable = lon2 )
		self.lon2_entry.grid( row = 5 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_lat1 = Label( tab1 , text = "Latitude 1 [deg]" )
		self.label_lat1.grid( row = 6 , column = 0 , columnspan = 3 , sticky = W )
		self.lat1_entry = Entry( tab1 , textvariable = lat1 )
		self.lat1_entry.grid( row = 6 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_lat2 = Label( tab1 , text = "Latitude 2 [deg]" )
		self.label_lat2.grid( row = 7 , column = 0 , columnspan = 3 , sticky = W )
		self.lat2_entry = Entry( tab1 , textvariable = lat2 )
		self.lat2_entry.grid( row = 7 , column = 3 , columnspan = 3 , sticky = W + E )
		self.but_load_topography = Button( tab1 , text = "Load topography" , command = self.load_topography , state = 'normal' )
		self.but_load_topography.grid( row = 8 , column = 0 , columnspan = 6 , sticky = W + E )
		self.but_plot_topography = Button( tab1 , text = "Plot topography" , command = self.plot_topography , state = 'disabled' )
		self.but_plot_topography.grid( row = 9 , column = 0 , columnspan = 6 , sticky = W + E )
		self.label_venttype = Label( tab2 , text = "Vent type" , state = 'disabled' )
		self.label_venttype.grid( row = 0 , column = 0 , columnspan = 3 , sticky = W )
		self.venttype_entry = OptionMenu( tab2 , self.venttype , "Pointwise" , "Linear" , "Circumference arch" , "Input file" , command = self.opt_venttype )
		self.venttype_entry.grid( row = 0 , column = 3 , columnspan = 3 , sticky = W + E )
		self.venttype_entry.configure( state = 'disabled' )
		self.label_loncen = Label( tab2 , text = "Longitude Collapse [deg]" , state = 'disabled' )
		self.label_loncen.grid( row = 1 , column = 0 , columnspan = 3 , sticky = W )
		self.loncen_entry = Entry( tab2 , textvariable = loncen , state = 'disabled' )
		self.loncen_entry.grid( row = 1 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_latcen = Label( tab2 , text = "Latitude Collapse [deg]" , state = 'disabled' )
		self.label_latcen.grid( row = 2 , column = 0 , columnspan = 3 , sticky = W )
		self.latcen_entry = Entry( tab2 , textvariable = latcen , state = 'disabled' )
		self.latcen_entry.grid( row = 2 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_eastcen = Label( tab2 , text = "East Coordinate Colapse [m]" , state = 'disabled' )
		self.label_eastcen.grid( row = 3 , column = 0 , columnspan = 3 , sticky = W )
		self.eastcen_entry = Entry( tab2 , textvariable = eastcen , state = 'disabled' )
		self.eastcen_entry.grid( row = 3 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_northcen = Label( tab2 , text = "North Coordinate Colapse [m]" , state = 'disabled' )
		self.label_northcen.grid( row = 4 , column = 0 , columnspan = 3 , sticky = W )
		self.northcen_entry = Entry( tab2 , textvariable = northcen , state = 'disabled' )
		self.northcen_entry.grid( row = 4 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_azimuthline = Label( tab2 , text = "Azimuth Line [deg]" , state = 'disabled' )
		self.label_azimuthline.grid( row = 5 , column = 0 , columnspan = 3 , sticky = W )
		self.azimuthline_entry = Entry( tab2 , textvariable = azimuthline , state = 'disabled' )
		self.azimuthline_entry.grid( row = 5 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_lengthline = Label( tab2 , text = "Length Line [m]" , state = 'disabled' )
		self.label_lengthline.grid( row = 6 , column = 0 , columnspan = 3 , sticky = W )
		self.lengthline_entry = Entry( tab2 , textvariable = lengthline , state = 'disabled' )
		self.lengthline_entry.grid( row = 6 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_radcir = Label( tab2 , text = "Radius (Circumference arch) [m]" , state = 'disabled' )
		self.label_radcir.grid( row = 7 , column = 0 , columnspan = 3 , sticky = W )
		self.radcir_entry = Entry( tab2 , textvariable = radcir , state = 'disabled' )
		self.radcir_entry.grid( row = 7 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_ang1cir = Label( tab2 , text = "Initial angle (Circumference arch) [deg]" , state = 'disabled' )
		self.label_ang1cir.grid( row = 8 , column = 0 , columnspan = 3 , sticky = W )
		self.ang1cir_entry = Entry( tab2 , textvariable = ang1cir , state = 'disabled' )
		self.ang1cir_entry.grid( row = 8 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_ang2cir = Label( tab2 , text = "Final angle (Circumference arch) [deg]" , state = 'disabled' )
		self.label_ang2cir.grid( row = 9 , column = 0 , columnspan = 3 , sticky = W )
		self.ang2cir_entry = Entry( tab2 , textvariable = ang2cir , state = 'disabled' )
		self.ang2cir_entry.grid( row = 9 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_varcen = Label( tab2 , text = "Uncertainty of collapse position [m]" , state = 'disabled' )
		self.label_varcen.grid( row = 10 , column = 0 , columnspan = 3 , sticky = W )
		self.varcen_entry = Entry( tab2 , textvariable = self.varcen , state = 'disabled' )
		self.varcen_entry.grid( row = 10 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_ventdist = Label( tab2 , text = "Probability distribution for uncertainty of collapse position" , state = 'disabled' )
		self.label_ventdist.grid( row = 11 , column = 0 , columnspan = 3 , sticky = W )
		self.ventdist_entry = OptionMenu( tab2 , ventdist , "Gaussian" , "Uniform" , command = self.opt_ventdist )
		self.ventdist_entry.grid( row = 11 , column = 3 , columnspan = 3 , sticky = W + E )
		self.ventdist_entry.configure( state = 'disabled' )
		self.but_sample_vent = Button( tab2 , text = "Collapse position sampling" , command = self.sample_vent , state = 'disabled' )
		self.but_sample_vent.grid( row = 12 , column = 0 , columnspan = 6 , sticky = W + E )
		self.but_plot_vent = Button( tab2 , text = "Plot collapse positions" , command = self.plot_vent , state = 'disabled' )
		self.but_plot_vent.grid( row = 13 , column = 0 , columnspan = 6 , sticky = W + E )
		self.but_sample_calib = Button( tab2 , text = "Set parameters for calibration mode" , command = self.sample_calib , state = 'disabled' )
		self.but_sample_calib.grid( row = 14 , column = 0 , columnspan = 6 , sticky = W + E )
		self.but_plot_calib = Button( tab2 , text = "Plot reference polygon for calibration" , command = self.plot_calib , state = 'disabled' )
		self.but_plot_calib.grid( row = 15 , column = 0 , columnspan = 6 , sticky = W + E )
		self.label_type_input = Label( tab3 , text = "Input type for PDC properties" )
		self.label_type_input.grid( row = 0 , column = 0 , columnspan = 2 , sticky = W )
		self.type_input_entry = OptionMenu( tab3 , self.typeinput , "Predefined distributions" , "Input file" , "Calibration-based sampling" , command = self.opt_typeinput )
		self.type_input_entry.grid( row = 0 , column = 2 , columnspan = 4 , sticky = W + E )
		self.label_prescribed = Label( tab3 , text = "Predefined distributions" )
		self.label_prescribed.grid( row = 1 , column = 0 , columnspan = 6 , sticky = W + E )		
		self.label_dist_volume = Label( tab3 , text = "Predefined distribution for collapsing volume" )
		self.label_dist_volume.grid( row = 2 , column = 0 , columnspan = 2 , sticky = W )
		self.dist_volume_entry = OptionMenu( tab3 , self.distvolume , "Gaussian" , "Uniform" , "Gamma" , "Lognormal" , command = self.opt_distvolume )
		self.dist_volume_entry.grid( row = 2 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_volume = Label( tab3 , text = "Expected collapsing volume [m3]" )
		self.label_volume.grid( row = 3 , column = 0 , columnspan = 2 , sticky = W )
		self.volume_entry = Entry( tab3 , textvariable = volume )
		self.volume_entry.grid( row = 3 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_var_volume = Label( tab3 , text = "Uncertainty collapsing volume [m3]" )
		self.label_var_volume.grid( row = 4 , column = 0 , columnspan = 2 , sticky = W )
		self.var_volume_entry = Entry( tab3 , textvariable = var_volume )
		self.var_volume_entry.grid( row = 4 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_volume_k = Label( tab3 , text = "Parameter k in gamma distribution (collapsing volume [m3])" , state = 'disabled' )
		self.label_volume_k.grid( row = 5 , column = 0 , columnspan = 2 , sticky = W )
		self.volume_k_entry = Entry( tab3 , textvariable = volume_k , state = 'disabled' )
		self.volume_k_entry.grid( row = 5 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_volume_theta = Label( tab3 , text = "Parameter theta in gamma distribution (collapsing volume [m3])" , state = 'disabled' )
		self.label_volume_theta.grid( row = 6 , column = 0 , columnspan = 2 , sticky = W )
		self.volume_theta_entry = Entry( tab3 , textvariable = volume_theta , state = 'disabled' )
		self.volume_theta_entry.grid( row = 6 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_dist_phi_0 = Label( tab3 , text = "Predefined distribution for initial concentration" )
		self.label_dist_phi_0.grid( row = 2 , column = 3 , columnspan = 2 , sticky = W )
		self.dist_phi_0_entry = OptionMenu( tab3 , self.distphi_0 , "Gaussian" , "Uniform" , "Gamma" , "Lognormal" , command = self.opt_distphi_0 )
		self.dist_phi_0_entry.grid( row = 2 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_phi_0 = Label( tab3 , text = "Expected initial concentration" )
		self.label_phi_0.grid( row = 3 , column = 3 , columnspan = 2 , sticky = W )
		self.phi_0_entry = Entry( tab3 , textvariable = phi_0 )
		self.phi_0_entry.grid( row = 3 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_var_phi_0 = Label( tab3 , text = "Uncertainty initial concentration" )
		self.label_var_phi_0.grid( row = 4 , column = 3 , columnspan = 2 , sticky = W )
		self.var_phi_0_entry = Entry( tab3 , textvariable = var_phi_0 )
		self.var_phi_0_entry.grid( row = 4 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_phi_0_k = Label( tab3 , text = "Parameter k in gamma distribution (initial concentration)" , state = 'disabled' )
		self.label_phi_0_k.grid( row = 5 , column = 3 , columnspan = 2 , sticky = W )
		self.phi_0_k_entry = Entry( tab3 , textvariable = phi_0_k , state = 'disabled' )
		self.phi_0_k_entry.grid( row = 5 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_phi_0_theta = Label( tab3 , text = "Parameter theta in gamma distribution (initial concentration)" , state = 'disabled' )
		self.label_phi_0_theta.grid( row = 6 , column = 3 , columnspan = 2 , sticky = W )
		self.phi_0_theta_entry = Entry( tab3 , textvariable = phi_0_theta , state = 'disabled' )
		self.phi_0_theta_entry.grid( row = 6 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_dist_ws = Label( tab3 , text = "Predefined distribution for sedimentation velocity" )
		self.label_dist_ws.grid( row = 7 , column = 0 , columnspan = 2 , sticky = W )
		self.dist_ws_entry = OptionMenu( tab3 , self.distws , "Gaussian" , "Uniform" , "Gamma" , "Lognormal" , command = self.opt_distws )
		self.dist_ws_entry.grid( row = 7 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_ws = Label( tab3 , text = "Expected sedimentation velocity [m/s]" )
		self.label_ws.grid( row = 8 , column = 0 , columnspan = 2 , sticky = W )
		self.ws_entry = Entry( tab3 , textvariable = ws )
		self.ws_entry.grid( row = 8 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_var_ws = Label( tab3 , text = "Uncertainty sedimentation velocity [m/s]" )
		self.label_var_ws.grid( row = 9 , column = 0 , columnspan = 2 , sticky = W )
		self.var_ws_entry = Entry( tab3 , textvariable = self.varws )
		self.var_ws_entry.grid( row = 9 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_ws_k = Label( tab3 , text = "Parameter k in gamma distribution (sedimentation velocity [m/s])" , state = 'disabled' )
		self.label_ws_k.grid( row = 10 , column = 0 , columnspan = 2 , sticky = W )
		self.ws_k_entry = Entry( tab3 , textvariable = ws_k , state = 'disabled' )
		self.ws_k_entry.grid( row = 10 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_ws_theta = Label( tab3 , text = "Parameter theta in gamma distribution (sedimentation velocity [m/s])" , state = 'disabled' )
		self.label_ws_theta.grid( row = 11 , column = 0 , columnspan = 2 , sticky = W )
		self.ws_theta_entry = Entry( tab3 , textvariable = ws_theta , state = 'disabled' )
		self.ws_theta_entry.grid( row = 11 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_dist_Fr = Label( tab3 , text = "Predefined distribution for Froude number" )
		self.label_dist_Fr.grid( row = 7 , column = 3 , columnspan = 2 , sticky = W )
		self.dist_Fr_entry = OptionMenu( tab3 , self.distFr , "Gaussian" , "Uniform" , "Gamma" , "Lognormal" , command = self.opt_distFr )
		self.dist_Fr_entry.grid( row = 7 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_Fr = Label( tab3 , text = "Expected Froude number" )
		self.label_Fr.grid( row = 8 , column = 3 , columnspan = 2 , sticky = W )
		self.Fr_entry = Entry( tab3 , textvariable = Fr )
		self.Fr_entry.grid( row = 8 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_var_Fr = Label( tab3 , text = "Uncertainty Froude number" )
		self.label_var_Fr.grid( row = 9 , column = 3 , columnspan = 2 , sticky = W )
		self.var_Fr_entry = Entry( tab3 , textvariable = self.varFr )
		self.var_Fr_entry.grid( row = 9 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_Fr_k = Label( tab3 , text = "Parameter k in gamma distribution (Froude number)" , state = 'disabled' )
		self.label_Fr_k.grid( row = 10 , column = 3 , columnspan = 2 , sticky = W )
		self.Fr_k_entry = Entry( tab3 , textvariable = Fr_k , state = 'disabled' )
		self.Fr_k_entry.grid( row = 10 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_Fr_theta = Label( tab3 , text = "Parameter theta in gamma distribution (Froude number)" , state = 'disabled' )
		self.label_Fr_theta.grid( row = 11 , column = 3 , columnspan = 2 , sticky = W )
		self.Fr_theta_entry = Entry( tab3 , textvariable = Fr_theta , state = 'disabled' )
		self.Fr_theta_entry.grid( row = 11 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_dist_rho_p = Label( tab3 , text = "Predefined distribution for pyroclasts density" )
		self.label_dist_rho_p.grid( row = 12 , column = 0 , columnspan = 2 , sticky = W )
		self.dist_rho_p_entry = OptionMenu( tab3 , self.distrho_p , "Gaussian" , "Uniform" , "Gamma" , "Lognormal" , command = self.opt_distrho_p )
		self.dist_rho_p_entry.grid( row = 12 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_rho_p = Label( tab3 , text = "Expected pyroclasts density [kg/m3]" )
		self.label_rho_p.grid( row = 13 , column = 0 , columnspan = 2 , sticky = W )
		self.rho_p_entry = Entry( tab3 , textvariable = rho_p )
		self.rho_p_entry.grid( row = 13 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_var_rho_p = Label( tab3 , text = "Uncertainty pyroclasts density [kg/m3]" )
		self.label_var_rho_p.grid( row = 14 , column = 0 , columnspan = 2 , sticky = W )
		self.var_rho_p_entry = Entry( tab3 , textvariable = self.varrho_p )
		self.var_rho_p_entry.grid( row = 14 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_rho_p_k = Label( tab3 , text = "Parameter k in gamma distribution (pyroclasts density [kg/m3])" , state = 'disabled' )
		self.label_rho_p_k.grid( row = 15 , column = 0 , columnspan = 2 , sticky = W )
		self.rho_p_k_entry = Entry( tab3 , textvariable = rho_p_k , state = 'disabled' )
		self.rho_p_k_entry.grid( row = 15 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_rho_p_theta = Label( tab3 , text = "Parameter theta in gamma distribution (pyroclasts density [kg/m3])" , state = 'disabled' )
		self.label_rho_p_theta.grid( row = 16 , column = 0 , columnspan = 2 , sticky = W )
		self.rho_p_theta_entry = Entry( tab3 , textvariable = rho_p_theta , state = 'disabled' )
		self.rho_p_theta_entry.grid( row = 16 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_dist_rho_gas = Label( tab3 , text = "Predefined distribution for gas density" )
		self.label_dist_rho_gas.grid( row = 12 , column = 3 , columnspan = 2 , sticky = W )
		self.dist_rho_gas_entry = OptionMenu( tab3 , self.distrho_gas , "Gaussian" , "Uniform" , "Gamma" , "Lognormal" , command = self.opt_distrho_gas )
		self.dist_rho_gas_entry.grid( row = 12 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_rho_gas = Label( tab3 , text = "Expected gas density [kg/m3]" )
		self.label_rho_gas.grid( row = 13 , column = 3 , columnspan = 2 , sticky = W )
		self.rho_gas_entry = Entry( tab3 , textvariable = rho_gas )
		self.rho_gas_entry.grid( row = 13 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_var_rho_gas = Label( tab3 , text = "Uncertainty gas density [kg/m3]" )
		self.label_var_rho_gas.grid( row = 14 , column = 3 , columnspan = 2 , sticky = W )
		self.var_rho_gas_entry = Entry( tab3 , textvariable = self.varrho_gas )
		self.var_rho_gas_entry.grid( row = 14 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_rho_gas_k = Label( tab3 , text = "Parameter k in gamma distribution (gas density [kg/m3])" , state = 'disabled' )
		self.label_rho_gas_k.grid( row = 15 , column = 3 , columnspan = 2 , sticky = W )
		self.rho_gas_k_entry = Entry( tab3 , textvariable = rho_gas_k , state = 'disabled' )
		self.rho_gas_k_entry.grid( row = 15 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_rho_gas_theta = Label( tab3 , text = "Parameter theta in gamma distribution (gas density [kg/m3])" , state = 'disabled' )
		self.label_rho_gas_theta.grid( row = 16 , column = 3 , columnspan = 2 , sticky = W )
		self.rho_gas_theta_entry = Entry( tab3 , textvariable = rho_gas_theta , state = 'disabled' )
		self.rho_gas_theta_entry.grid( row = 16 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_calibrationbased = Label( tab3 , text = "Calibration-based sampling" , state = 'disabled' )
		self.label_calibrationbased.grid( row = 17 , column = 0 , columnspan = 6 , sticky = W + E )	
		self.label_calibration_type = Label( tab3 , text = "Type of calibration" , state = 'disabled' )
		self.label_calibration_type.grid( row = 18 , column = 0 , columnspan = 2 , sticky = W )
		self.calibration_type_entry = OptionMenu( tab3 , calibrationtype , "Jaccard index" , "Hausdorff distance" , "RMSD" , "Runout distance-based" , "Inundation area-based", command = self.opt_calibrationtype )
		self.calibration_type_entry.grid( row = 18 , column = 2 , columnspan = 4 , sticky = W + E )
		self.calibration_type_entry.configure( state = 'disabled' )
		self.label_dist_distance = Label( tab3 , text = "Distribution for runout distance" , state = 'disabled' )
		self.label_dist_distance.grid( row = 19 , column = 0 , columnspan = 2 , sticky = W )
		self.dist_distance_entry = OptionMenu( tab3 , distdistance , "Gaussian" , "Uniform" , "Gamma" , "Lognormal" , "Input cumulative distribution" , command = self.opt_distdistance )
		self.dist_distance_entry.grid( row = 19 , column = 2 , columnspan = 1 , sticky = W + E )
		self.dist_distance_entry.configure( state = 'disabled' )
		self.label_distance = Label( tab3 , text = "Expected runout distance [m]" , state = 'disabled' )
		self.label_distance.grid( row = 20 , column = 0 , columnspan = 2 , sticky = W )
		self.distance_entry = Entry( tab3 , textvariable = distance , state = 'disabled' )
		self.distance_entry.grid( row = 20 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_var_distance = Label( tab3 , text = "Uncertainty runout distance [m]" , state = 'disabled' )
		self.label_var_distance.grid( row = 21 , column = 0 , columnspan = 2 , sticky = W )
		self.var_distance_entry = Entry( tab3 , textvariable = var_distance , state = 'disabled' )
		self.var_distance_entry.grid( row = 21 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_distance_k = Label( tab3 , text = "Parameter k in gamma distribution (runout distance [m])" , state = 'disabled' )
		self.label_distance_k.grid( row = 22 , column = 0 , columnspan = 2 , sticky = W )
		self.distance_k_entry = Entry( tab3 , textvariable = distance_k , state = 'disabled' )
		self.distance_k_entry.grid( row = 22 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_distance_theta = Label( tab3 , text = "Parameter theta in gamma distribution (runout distance [m])" , state = 'disabled' )
		self.label_distance_theta.grid( row = 23 , column = 0 , columnspan = 2 , sticky = W )
		self.distance_theta_entry = Entry( tab3 , textvariable = distance_theta , state = 'disabled' )
		self.distance_theta_entry.grid( row = 23 , column = 2 , columnspan = 1 , sticky = W + E )
		self.label_dist_area = Label( tab3 , text = "Distribution for inundation area" , state = 'disabled' )
		self.label_dist_area.grid( row = 19 , column = 3 , columnspan = 2 , sticky = W )
		self.dist_area_entry = OptionMenu( tab3 , distarea , "Gaussian" , "Uniform" , "Gamma" , "Lognormal" , "Input cumulative distribution" , command = self.opt_distarea )
		self.dist_area_entry.grid( row = 19 , column = 5 , columnspan = 1 , sticky = W + E )
		self.dist_area_entry.configure( state = 'disabled' )
		self.label_area = Label( tab3 , text = "Expected inundation area [km2]" , state = 'disabled' )
		self.label_area.grid( row = 20 , column = 3 , columnspan = 2 , sticky = W )
		self.area_entry = Entry( tab3 , textvariable = area , state = 'disabled' )
		self.area_entry.grid( row = 20 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_var_area = Label( tab3 , text = "Uncertainty inundation area [km2]" , state = 'disabled' )
		self.label_var_area.grid( row = 21 , column = 3 , columnspan = 2 , sticky = W )
		self.var_area_entry = Entry( tab3 , textvariable = var_area , state = 'disabled' )
		self.var_area_entry.grid( row = 21 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_area_k = Label( tab3 , text = "Parameter k in gamma distribution (inundation area [km2])" , state = 'disabled' )
		self.label_area_k.grid( row = 22 , column = 3 , columnspan = 2 , sticky = W )
		self.area_k_entry = Entry( tab3 , textvariable = area_k , state = 'disabled' )
		self.area_k_entry.grid( row = 22 , column = 5 , columnspan = 1 , sticky = W + E )
		self.label_area_theta = Label( tab3 , text = "Parameter theta in gamma distribution (inundation area [km2])" , state = 'disabled' )
		self.label_area_theta.grid( row = 23 , column = 3 , columnspan = 2 , sticky = W )
		self.area_theta_entry = Entry( tab3 , textvariable = area_theta , state = 'disabled' )
		self.area_theta_entry.grid( row = 23 , column = 5 , columnspan = 1 , sticky = W + E )
		self.but_sample_properties = Button( tab3 , text = "Set PDC properties" , command = self.sample_properties )
		self.but_sample_properties.grid( row = 24 , column = 0 , columnspan = 6 , sticky = W + E )
		self.but_plot_properties = Button( tab3 , text = "Plot PDC properties" , command = self.plot_properties , state = 'disabled' )
		self.but_plot_properties.grid( row = 25 , column = 0 , columnspan = 6 , sticky = W + E )
		self.label_runname = Label( tab4 , text = "Run name" )
		self.label_runname.grid( row = 0 , column = 0 , columnspan = 3 , sticky = W )
		self.runname_entry = Entry( tab4 , textvariable = runname )
		self.runname_entry.grid( row = 0 , column = 3 , columnspan = 3 , sticky = W + E )
		self.label_typesimulation = Label( tab4 , text = "Type of simulation" )
		self.label_typesimulation.grid( row = 1 , column = 0 , columnspan = 3 , sticky = W )
		self.loaded_typesimulation = Label( tab4 , text = "Not defined" )
		self.loaded_typesimulation.grid( row = 1 , column = 3 , columnspan = 3 , sticky = W )
		self.label_loaded_topo = Label( tab4 , text = "Topography" )
		self.label_loaded_topo.grid( row = 2 , column = 0 , columnspan = 3 , sticky = W )
		self.loaded_topo = Label( tab4 , text = "Not loaded" )
		self.loaded_topo.grid( row = 2 , column = 3 , columnspan = 3 , sticky = W )
		self.label_coordinates = Label( tab4 , text = "Coordinate type" )
		self.label_coordinates.grid( row = 3 , column = 0 , columnspan = 3 , sticky = W )
		self.loaded_coordinates = Label( tab4 , text = "Not defined" )
		self.loaded_coordinates.grid( row = 3 , column = 3 , columnspan = 3 , sticky = W )
		self.label_loaded_vent = Label( tab4 , text = "Vent position" )
		self.label_loaded_vent.grid( row = 4 , column = 0 , columnspan = 3 , sticky = W )
		self.loaded_vent = Label( tab4 , text = "Not sampled" )
		self.loaded_vent.grid( row = 4 , column = 3 , columnspan = 3 , sticky = W )
		self.label_loaded_properties = Label( tab4 , text = "PDC properties" )
		self.label_loaded_properties.grid( row = 5 , column = 0 , columnspan = 3 , sticky = W )
		self.loaded_properties = Label( tab4 , text = "Not sampled" )
		self.loaded_properties.grid( row = 5 , column = 3 , columnspan = 3 , sticky = W )
		self.label_loaded_calib = Label( tab4 , text = "Calibration mode inputs" )
		self.label_loaded_calib.grid( row = 6 , column = 0 , columnspan = 3 , sticky = W )
		self.loaded_calib = Label( tab4 , text = "Not defined / Not needed" )
		self.loaded_calib.grid( row = 6 , column = 3 , columnspan = 3 , sticky = W )
		self.label_numbersim = Label( tab4 , text = "Number of simulations" )
		self.label_numbersim.grid( row = 7 , column = 0 , columnspan = 3 , sticky = W )
		self.loaded_numbersim = Label( tab4 , text = "Not defined" )
		self.loaded_numbersim.grid( row = 7 , column = 3 , columnspan = 3 , sticky = W )
		self.but_runsim = Button( tab4 , text = "Run simulations" , command = self.runsim , state = 'disabled' )
		self.but_runsim.grid( row = 8 , column = 0 , columnspan = 6 , sticky = W + E )
		self.but_plotres = Button( tab4 , text = "Plot results" , command = self.plotres , state = 'disabled' )
		self.but_plotres.grid( row = 10 , column = 0 , columnspan = 6 , sticky = W + E )
		self.but_saveres = Button( tab4 , text = "Save results" , command = self.saveres , state = 'disabled' )
		self.but_saveres.grid( row = 11 , column = 0 , columnspan = 6 , sticky = W + E )
		tab_parent.pack( expand = 1 , fill = 'both' )

	def opt_typesim( self , opt ):
		if( opt == "Default mode: Construction of PDC inundation probability map" ):
			self.type_sim_choice = 1
		else:
			self.type_sim_choice = 2
			if( opt == "Calibration mode: Based on the distribution of PDC runout distance or inundation area" ):
				self.boolean_polygon_choice = 0
			else:
				self.boolean_polygon_choice = 1
		self.enabled_disabled()

	def opt_dem( self , opt ):
		if( opt == "STRM 30 m" ):
			self.source_dem_choice = 1
		elif( opt == "Input DEM (utm)" ):
			self.source_dem_choice = 2
		else:
			self.source_dem_choice = 3
		self.enabled_disabled()

	def opt_venttype( self , opt ):
		if( opt == "Pointwise" ):
			self.vent_type_choice = 1
		elif( opt == "Linear" ):
			self.vent_type_choice = 2
		elif( opt == "Circumference arch" ):
			self.vent_type_choice = 3
		elif( opt == "Input file" ):
			self.vent_type_choice = 4
		self.enabled_disabled()

	def opt_ventdist( self , opt ):
		if( opt == "Gaussian" ):
			self.vent_dist_choice = 1
		elif( opt == "Uniform" ):
			self.vent_dist_choice = 2
		self.enabled_disabled()

	def opt_typeinput( self , opt ):
		if( opt == "Predefined distributions" ):
			self.type_input_choice = 1
		elif( opt == "Input file" ):
			self.type_input_choice = 2
		else:
			self.type_input_choice = 3
		self.enabled_disabled()

	def opt_distvolume( self , opt ):
		if( opt == "Gaussian" ):
			self.dist_volume_choice = 1
		elif( opt == "Uniform" ):
			self.dist_volume_choice = 2
		elif( opt == "Gamma" ):
			self.dist_volume_choice = 3
		elif( opt == "Lognormal" ):
			self.dist_volume_choice = 4
		self.enabled_disabled()

	def opt_distphi_0( self , opt ):
		if( opt == "Gaussian" ):
			self.dist_phi_0_choice = 1
		elif( opt == "Uniform" ):
			self.dist_phi_0_choice = 2
		elif( opt == "Gamma" ):
			self.dist_phi_0_choice = 3
		elif( opt == "Lognormal" ):
			self.dist_phi_0_choice = 4
		self.enabled_disabled()

	def opt_distws( self , opt ):
		if( opt == "Gaussian" ):
			self.dist_ws_choice = 1
		elif( opt == "Uniform" ):
			self.dist_ws_choice = 2
		elif( opt == "Gamma" ):
			self.dist_ws_choice = 3
		elif( opt == "Lognormal" ):
			self.dist_ws_choice = 4
		self.enabled_disabled()

	def opt_distFr( self , opt ):
		if( opt == "Gaussian" ):
			self.dist_Fr_choice = 1
		elif( opt == "Uniform" ):
			self.dist_Fr_choice = 2
		elif( opt == "Gamma" ):
			self.dist_Fr_choice = 3
		elif( opt == "Lognormal" ):
			self.dist_Fr_choice = 4
		self.enabled_disabled()

	def opt_distrho_p( self , opt ):
		if( opt == "Gaussian" ):
			self.dist_rho_p_choice = 1
		elif( opt == "Uniform" ):
			self.dist_rho_p_choice = 2
		elif( opt == "Gamma" ):
			self.dist_rho_p_choice = 3
		elif( opt == "Lognormal" ):
			self.dist_rho_p_choice = 4
		self.enabled_disabled()

	def opt_distrho_gas( self , opt ):
		if( opt == "Gaussian" ):
			self.dist_rho_gas_choice = 1
		elif( opt == "Uniform" ):
			self.dist_rho_gas_choice = 2
		elif( opt == "Gamma" ):
			self.dist_rho_gas_choice = 3
		elif( opt == "Lognormal" ):
			self.dist_rho_gas_choice = 4
		self.enabled_disabled()

	def opt_calibrationtype( self , opt ):
		if( opt == "Jaccard index" ):
			self.calibration_type_choice = 1
		elif( opt == "Hausdorff distance" ):
			self.calibration_type_choice = 3
		elif( opt == "RMSD" ):
			self.calibration_type_choice = 2
		elif( opt == "Runout distance-based" ):
			self.calibration_type_choice = 5
		else:
			self.calibration_type_choice = 7
		self.enabled_disabled()

	def opt_distdistance( self , opt ):
		if( opt == "Gaussian" ):
			self.dist_distance_choice = 1
		elif( opt == "Uniform" ):
			self.dist_distance_choice = 2
		elif( opt == "Gamma" ):
			self.dist_distance_choice = 3
		elif( opt == "Lognormal" ):
			self.dist_distance_choice = 4
		elif( opt == "Input cumulative distribution" ):
			self.dist_distance_choice = 5
		self.enabled_disabled()

	def opt_distarea( self , opt ):
		if( opt == "Gaussian" ):
			self.dist_area_choice = 1
		elif( opt == "Uniform" ):
			self.dist_area_choice = 2
		elif( opt == "Gamma" ):
			self.dist_area_choice = 3
		elif( opt == "Lognormal" ):
			self.dist_area_choice = 4
		elif( opt == "Input cumulative distribution" ):
			self.dist_area_choice = 5
		self.enabled_disabled()

	def load_topography( self ):
		if( self.topography_availability == 1 ):
			result = messagebox.askquestion( "Continue?" , "Topography information was loaded previously. If you continue, the code will discard all the information loaded previously, except PDC properties data. Do you want to continue?" , icon = 'warning' )
			if( result == 'no' ):
				return
			else:
				self.topography_availability == 0
				self.sample_vent_availability = 0
				self.sample_cal_availability = 0
				self.boolean_polygon = 0
				self.results_availability = 0
				self.source_dem = np.nan
				self.vent_type = 1
				self.vent_dist = 1
				self.topography_inputs = ""
				self.vent_inputs = ""
				self.calib_inputs = ""
				self.run_inputs = ""
		try:
			if( self.source_dem_choice == 1 ):
				self.lon1 = float( self.lon1_entry.get() )
				self.lon2 = float( self.lon2_entry.get() )
				self.lat1 = float( self.lat1_entry.get() )
				self.lat2 = float( self.lat2_entry.get() )
				[ self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.Cities , self.Topography , self.Topography_Sea , self.cells_lon , self.cells_lat ] = import_map( self.current_path , "DTopo" , self.lon1 , self.lon2 , self.lat1 , self.lat2 , 1 , 0 )
				[ self.matrix_lon , self.matrix_lat , self.step_lon_m , self.step_lat_m , self.step_lon_deg , self.step_lat_deg , self.utm_save ] = matrix_deg( self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.cells_lon , self.cells_lat )
				self.resolution_factor = np.sqrt( self.step_lon_m * self.step_lat_m )
				self.source_dem = 1
				self.topography_inputs = "Source DEM: SRTM 30 m" + "\n"
				self.topography_inputs = self.topography_inputs + "Longitude 1: " + str( self.lon1 ) + "\n"
				self.topography_inputs = self.topography_inputs + "Longitude 2: " + str( self.lon2 ) + "\n"
				self.topography_inputs = self.topography_inputs + "Latitude 1: " + str( self.lat1 ) + "\n"
				self.topography_inputs = self.topography_inputs + "Latitude 2: " + str( self.lat2 ) + "\n"
			else:
				file_path = filedialog.askopenfilename()
				if( len( file_path ) == 0 ):
					self.topography_availability == 0
					self.source_dem = np.nan
					self.topography_inputs = ""
					self.enabled_disabled()
					messagebox.showerror( title = None , message = "Topography was not loaded" )
					return
				if( self.source_dem_choice == 2 ):
					[ self.Topography , self.Topography_Sea , self.n_north , self.n_east , self.cellsize , self.east_cor , self.north_cor ] = read_map_utm( file_path , file_path , 1 , 0 )
					[ self.matrix_north , self.matrix_east , self.utm_save ] = matrix_utm( self.n_north , self.n_east , self.cellsize , self.east_cor , self.north_cor )
					self.resolution_factor = self.cellsize
					self.source_dem = 2
					self.topography_inputs = "Source DEM: Input DEM (utm)" + "\n"
				else:
					[ self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.Cities , self.Topography , self.Topography_Sea , self.cells_lon , self.cells_lat ] = read_map_deg( file_path , file_path , 1 , 0 )
					[ self.matrix_lon , self.matrix_lat , self.step_lon_m , self.step_lat_m , self.step_lon_deg , self.step_lat_deg , self.utm_save ] = matrix_deg( self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.cells_lon , self.cells_lat )
					self.resolution_factor = np.sqrt( self.step_lon_m * self.step_lat_m )
					self.source_dem = 3
					self.topography_inputs = "Source DEM: Input DEM (lon, lat)" + "\n"
				self.topography_inputs = self.topography_inputs + "Topography File: " + file_path + "\n"
			self.topography_availability = 1
			self.enabled_disabled()
			messagebox.showinfo( title = None , message = "Topography loaded successfully" )
		except:
			self.topography_availability == 0
			self.source_dem = np.nan
			self.topography_inputs = ""
			self.enabled_disabled()
			messagebox.showerror( title = None , message = "Topography was not loaded" )

	def plot_topography( self ):
		if( self.source_dem == 1 or self.source_dem == 3 ):
			plot_only_topography_deg( self.Cities , self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.step_lat_m , self.step_lon_m , self.matrix_lon , self.matrix_lat , self.Topography , self.Topography_Sea )
		else:
			plot_only_topography_utm( self.matrix_east , self.matrix_north , self.east_cor , self.north_cor , self.n_east , self.n_north , self.cellsize , self.Topography , self.Topography_Sea )
		plt.show()

	def sample_vent( self ):
		if( not np.isnan( self.type_sim ) and not self.type_sim == self.type_sim_choice ):
			result = messagebox.askquestion( "Continue?" , "The current loaded information is associated with other type of simulation. If you continue, the code will discard all the information loaded previously except topography. Do you want to continue?" , icon = 'warning' )
			if( result == 'no' ):
				return
			else:
				self.type_sim = np.nan
				self.boolean_polygon = 0
				self.vent_type = 1
				self.vent_dist = 1
				self.type_input = 1
				self.dist_volume = 1
				self.dist_phi_0 = 1
				self.dist_ws = 1
				self.dist_Fr = 1
				self.dist_rho_p = 1
				self.dist_rho_gas = 1
				self.calibration_type = 1
				self.dist_distance = 1
				self.dist_area = 1
				self.sample_vent_availability = 0
				self.vent_inputs = ""
				self.sample_properties_availability = 0
				self.properties_inputs = ""
				self.sample_cal_availability = 0
				self.calib_inputs = ""
				self.results_availability = 0
				self.run_inputs = ""
				self.N = np.nan
		self.N_choice = int( self.Nsim_entry.get() )
		if( self.type_sim_choice == 2 ):
			self.N_choice = np.power( int( np.sqrt( self.N_choice ) ) , 2 )
		if( not np.isnan( self.N ) and not self.N == self.N_choice ):
			result = messagebox.askquestion( "Continue?" , "The current loaded information is associated with other number of simulations. If you continue, the code will discard all the information loaded previously except topography. Do you want to continue?" , icon = 'warning' )
			if( result == 'no' ):
				return
			else:
				self.type_sim = np.nan
				self.boolean_polygon = 0
				self.vent_type = 1
				self.vent_dist = 1
				self.type_input = 1
				self.dist_volume = 1
				self.dist_phi_0 = 1
				self.dist_ws = 1
				self.dist_Fr = 1
				self.dist_rho_p = 1
				self.dist_rho_gas = 1
				self.calibration_type = 1
				self.dist_distance = 1
				self.dist_area = 1
				self.sample_vent_availability = 0
				self.vent_inputs = ""
				self.sample_properties_availability = 0
				self.properties_inputs = ""
				self.sample_cal_availability = 0
				self.calib_inputs = ""
				self.results_availability = 0
				self.run_inputs = ""
				self.N = np.nan
		try:
			self.type_sim = self.type_sim_choice
			self.N = self.N_choice
			self.vent_type = self.vent_type_choice
			self.vent_dist = self.vent_dist_choice
			self.sample_vent_availability = 1
			[ file_path , self.lon_cen , self.lat_cen , self.east_cen , self.north_cen , self.var_cen , self.azimuth_lin , self.length_lin , self.radius_rad , self.ang1_rad , self.ang2_rad ] = [ "" , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan ]
			if( self.vent_type == 4 ):
				file_path = filedialog.askopenfilename()
			else:
				if( self.type_sim == 2 ):
					self.var_cen = 0.0
				else:
					self.var_cen = float( self.varcen_entry.get() )
				if( self.vent_type == 2 ):
					self.azimuth_lin = float( self.azimuthline_entry.get() )
					self.length_lin = float( self.lengthline_entry.get() )
					lin_collapse = "Azimuth line [deg]: " + str( self.azimuth_lin ) + "\n" + "Length line [m]: " + str( self.length_lin ) + "\n" 
				elif( self.vent_type == 3 ):
					self.radius_rad = float( self.radcir_entry.get() )
					self.ang1_rad = float( self.ang1cir_entry.get() )
					self.ang2_rad = float( self.ang2cir_entry.get() )
					rad_collapse = "Radius (circumference arch) [m]: " + str( self.radius_rad ) + "\n" + "Initial angle (circumference arch) [m]: " + str( self.ang1_rad ) + "\n" + "Final angle (circumference arch) [m]: " + str( self.ang2_rad ) + "\n" 
			if( self.source_dem == 1 or self.source_dem == 3 ):
				if( not self.vent_type == 4 ):
					self.lon_cen = float( self.loncen_entry.get() )
					self.lat_cen = float( self.latcen_entry.get() )
					inputs_collapse = "Longitude collapse [deg]: " + str(self.lon_cen) + "\n" + "Latitude collapse [deg]: " + str(self.lat_cen) + "\n"
					var_collapse = "Uncertainty of vent position [m]: " + str( self.var_cen ) + "\n" + "Probability distribution of uncertainty of vent position: "
					if( self.vent_dist == 1 ):
						var_collapse = var_collapse + "Gaussian" + "\n"
					else:
						var_collapse = var_collapse + "Uniform" + "\n"
				[ self.lon_cen_vector , self.lat_cen_vector , self.N ] = create_vent_deg( self.vent_type , file_path , self.lon_cen , self.lat_cen , self.var_cen , self.azimuth_lin, self.length_lin , self.radius_rad , self.ang1_rad , self.ang2_rad , self.step_lon_deg , self.step_lat_deg , self.step_lon_m , self.step_lat_m , self.vent_dist , self.N )
			else:
				if( not self.vent_type == 4 ):
					self.east_cen = float( self.eastcen_entry.get() )
					self.north_cen = float( self.northcen_entry.get() )
					inputs_collapse = "East collapse [m]: " + str(self.east_cen) + "\n" + "North collapse [m]: " + str(self.north_cen) + "\n"
					var_collapse = "Uncertainty of vent position [m]: " + str( self.var_cen ) + "\n" + "Probability distribution of uncertainty of vent position: "
					if( self.vent_dist == 1 ):
						var_collapse = var_collapse + "Gaussian" + "\n"
					else:
						var_collapse = var_collapse + "Uniform" + "\n"					
				[ self.east_cen_vector , self.north_cen_vector , self.N ] = create_vent_utm( self.vent_type , file_path , self.east_cen , self.north_cen , self.var_cen , self.azimuth_lin, self.length_lin , self.radius_rad , self.ang1_rad , self.ang2_rad , self.vent_dist , self.N )
			self.sample_vent_availability = 1
			if( self.vent_type == 1 ):
				self.vent_inputs = "Vent type: Pointwise" + "\n" + inputs_collapse + var_collapse
			if( self.vent_type == 2 ):
				self.vent_inputs = "Vent type: Linear" + "\n" + inputs_collapse + lin_collapse + var_collapse
			if( self.vent_type == 3 ):
				self.vent_inputs = "Vent type: Circumference arch" + "\n" + inputs_collapse + rad_collapse + var_collapse
			if( self.vent_type == 4 ):
				self.vent_inputs = "Vent type: Input file" + "\n" + "File name: " + file_path + "\n"
			self.enabled_disabled()
			messagebox.showinfo( title = None , message = "Vent position sampled successfully" )
			if( not self.N == self.N_choice ):
				self.type_input = 1
				self.dist_volume = 1
				self.dist_phi_0 = 1
				self.dist_ws = 1
				self.dist_Fr = 1
				self.dist_rho_p = 1
				self.dist_rho_gas = 1
				self.calibration_type = 1
				self.dist_distance = 1
				self.dist_area = 1
				self.sample_properties_availability = 0
				self.sample_cal_availability = 0
				self.results_availability = 0
				self.properties_inputs = ""
				self.calib_inputs = ""
				self.run_inputs = ""
				self.enabled_disabled()
				messagebox.showerror( title = None , message = "The previous loaded information was associated with other number of simulations. Sampling of PDC properties was discarded." )
		except:
			self.sample_vent_availability = 0		
			self.vent_inputs = ""
			self.enabled_disabled()
			messagebox.showerror( title = None , message = "Vent position was not sampled" )

	def plot_vent( self ):
		if( self.source_dem == 1 or self.source_dem == 3 ):
			plot_only_topography_deg( self.Cities , self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.step_lat_m , self.step_lon_m , self.matrix_lon , self.matrix_lat , self.Topography , self.Topography_Sea )
			plot_only_vent_deg( self.lon_cen_vector , self.lat_cen_vector , self.N )
		else:
			plot_only_topography_utm( self.matrix_east , self.matrix_north , self.east_cor , self.north_cor , self.n_east , self.n_north , self.cellsize , self.Topography , self.Topography_Sea )
			plot_only_vent_utm( self.east_cen_vector , self.north_cen_vector , self.N )
		plt.show()

	def sample_calib( self ):
		if( not np.isnan( self.type_sim ) and not self.type_sim == self.type_sim_choice ):
			messagebox.showerror( title = None , message = "The current loaded information is associated with other type of simulation (default). If you want to develop calibration simulations, please sample vent position again." )
			return
		try:
			self.boolean_polygon = self.boolean_polygon_choice
			if( self.boolean_polygon == 1 ):
				path_calib = filedialog.askopenfilename()
			else:
				path_calib = ""
			self.type_sim = self.type_sim_choice
			if( self.source_dem == 1 or self.source_dem == 3 ):
				[ self.matrix_compare , self.vertices_compare , self.string_compare , self.data_direction ] = read_comparison_polygon_deg( path_calib , '' , 0.0 , 360.0 , self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.lon_cen , self.lat_cen , self.step_lat_m , self.step_lon_m , self.cells_lon , self.cells_lat , self.matrix_lon , self.matrix_lat , self.step_lon_deg , self.step_lat_deg , self.N )
			else:
				[ self.matrix_compare , self.vertices_compare , self.string_compare , self.data_direction ] = read_comparison_polygon_utm( path_calib , '' , 0.0 , 360.0 , self.east_cor , self.north_cor , self.east_cen , self.north_cen , self.cellsize , self.n_east , self.n_north , self.matrix_east , self.matrix_north , self.N )
			self.sample_cal_availability = 1
			self.enabled_disabled()
			if( self.boolean_polygon == 1 ):
				self.calib_inputs = "Polygon file name: " + path_calib + "\n"
			else:
				self.calib_inputs = ""
			messagebox.showinfo( title = None , message = "Calibration inputs were defined" )
		except:
			self.sample_cal_availability = 0
			self.calib_inputs = ""
			self.boolean_polygon = 0
			self.enabled_disabled()
			messagebox.showerror( title = None , message = "Calibration inputs were not defined" )

	def plot_calib( self ):
		if( self.source_dem == 1 or self.source_dem == 3 ):
			plot_only_topography_deg( self.Cities , self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.step_lat_m , self.step_lon_m , self.matrix_lon , self.matrix_lat , self.Topography , self.Topography_Sea )
			plot_only_vent_deg( self.lon_cen_vector , self.lat_cen_vector , self.N )
			plot_only_comparison_polygon_deg( self.matrix_lon , self.matrix_lat , self.matrix_compare )
		else:
			plot_only_topography_utm( self.matrix_east , self.matrix_north , self.east_cor , self.north_cor , self.n_east , self.n_north , self.cellsize , self.Topography , self.Topography_Sea )
			plot_only_vent_utm( self.east_cen_vector , self.north_cen_vector , self.N )
			plot_only_comparison_polygon_utm( self.matrix_east , self.matrix_north , self.matrix_compare )
		plt.show()

	def sample_properties( self ):
		if( not np.isnan( self.type_sim ) and not self.type_sim == self.type_sim_choice ):
			result = messagebox.askquestion( "Continue?" , "The current loaded information is associated with other type of simulation. If you continue, the code will discard all the information loaded previously except topography. Do you want to continue?" , icon = 'warning' )
			if( result == 'no' ):
				return
			else:
				self.type_sim = np.nan
				self.boolean_polygon = 0
				self.vent_type = 1
				self.vent_dist = 1
				self.type_input = 1
				self.dist_volume = 1
				self.dist_phi_0 = 1
				self.dist_ws = 1
				self.dist_Fr = 1
				self.dist_rho_p = 1
				self.dist_rho_gas = 1
				self.calibration_type = 1
				self.dist_distance = 1
				self.dist_area = 1
				self.sample_vent_availability = 0
				self.vent_inputs = ""
				self.sample_properties_availability = 0
				self.properties_inputs = ""
				self.sample_cal_availability = 0
				self.calib_inputs = ""
				self.results_availability = 0
				self.run_inputs = ""
				self.N = np.nan
		self.N_choice = int( self.Nsim_entry.get() )
		if( self.type_sim_choice == 2 ):
			self.N_choice = np.power( int( np.sqrt( self.N_choice ) ) , 2 )
		if( not np.isnan( self.N ) and not self.N == self.N_choice ):
			result = messagebox.askquestion( "Continue?" , "The current loaded information is associated with other number of simulations. If you continue, the code will discard all the information loaded previously except topography. Do you want to continue?" , icon = 'warning' )
			if( result == 'no' ):
				return
			else:
				self.type_sim = np.nan
				self.boolean_polygon = 0
				self.vent_type = 1
				self.vent_dist = 1
				self.type_input = 1
				self.dist_volume = 1
				self.dist_phi_0 = 1
				self.dist_ws = 1
				self.dist_Fr = 1
				self.dist_rho_p = 1
				self.dist_rho_gas = 1
				self.calibration_type = 1
				self.dist_distance = 1
				self.dist_area = 1
				self.sample_vent_availability = 0
				self.vent_inputs = ""
				self.sample_properties_availability = 0
				self.properties_inputs = ""
				self.sample_cal_availability = 0
				self.calib_inputs = ""
				self.results_availability = 0
				self.run_inputs = ""
				self.N = np.nan
		try:
			self.type_sim = self.type_sim_choice
			self.N = self.N_choice
			self.type_input = self.type_input_choice
			self.dist_volume = self.dist_volume_choice
			self.dist_phi_0 = self.dist_phi_0_choice
			self.dist_ws = self.dist_ws_choice
			self.dist_Fr = self.dist_Fr_choice
			self.dist_rho_p = self.dist_rho_p_choice
			self.dist_rho_gas = self.dist_rho_gas_choice
			self.calibration_type = self.calibration_type_choice
			self.dist_distance = self.dist_distance_choice
			self.dist_area = self.dist_area_choice
			[ file_path , self.volume , self.var_volume , self.volume_k , self.volume_theta , self.phi_0 , self.var_phi_0 , self.phi_0_k , self.phi_0_theta , self.ws , self.var_ws , self.ws_k , self.ws_theta , self.Fr , self.var_Fr , self.Fr_k , self.Fr_theta , self.rho_p , self.var_rho_p , self.rho_p_k , self.rho_p_theta , self.rho_gas , self.var_rho_gas , self.rho_gas_k , self.rho_gas_theta , self.distance , self.var_distance , self.distance_k , self.distance_theta , file_cumulative_distance , self.area , self.var_area , self.area_k , self.area_theta , file_cumulative_area ] = [ '' , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , '' , np.nan , np.nan , np.nan , np.nan , '' ]
			if( self.type_input == 2 or self.type_input == 3 ):
				file_path = filedialog.askopenfilename( title = "Calibration file" )
				if( self.type_input == 3 and self.calibration_type == 5 ):
					if( self.dist_distance in [ 1 , 2 , 4 ] ):
						self.distance = float( self.distance_entry.get() )
						self.var_distance = float( self.var_distance_entry.get() )
					elif( self.dist_distance == 3 ):
						self.distance_k = float( self.distance_k_entry.get() )
						self.distance_theta = float( self.distance_theta_entry.get() )
					else:
						file_cumulative_distance = filedialog.askopenfilename( title = "Cumulative distribution of runout distance" )
				elif( self.type_input == 3 and self.calibration_type == 7 ):
					if( self.dist_area in [ 1 , 2 , 4 ] ):
						self.area = float( self.area_entry.get() )
						self.var_area = float( self.var_area_entry.get() )
					elif( self.dist_area == 3 ):
						self.area_k = float( self.area_k_entry.get() )
						self.area_theta = float( self.area_theta_entry.get() )
					else:
						file_cumulative_area = filedialog.askopenfilename( title = "Cumulative distribution of inundation area" )
			else:
				if( self.dist_volume in [ 1 , 2 , 4 ] ):
					self.volume = float( self.volume_entry.get() )
					self.var_volume = float( self.var_volume_entry.get() )
				else:
					self.volume_k = float( self.volume_k_entry.get() )
					self.volume_theta = float( self.volume_theta_entry.get() )
				if( self.dist_phi_0 in [ 1 , 2 , 4 ] ):
					self.phi_0 = float( self.phi_0_entry.get() )
					self.var_phi_0 = float( self.var_phi_0_entry.get() )
				else:
					self.phi_0_k = float( self.phi_0_k_entry.get() )
					self.phi_0_theta = float( self.phi_0_theta_entry.get() )
				if( self.dist_ws in [ 1 , 2 , 4 ] ):
					self.ws = float( self.ws_entry.get() )
					self.var_ws = float( self.var_ws_entry.get() )
				else:
					self.ws_k = float( self.ws_k_entry.get() )
					self.ws_theta = float( self.ws_theta_entry.get() )
				if( self.dist_Fr in [ 1 , 2 , 4 ] ):
					self.Fr = float( self.Fr_entry.get() )
					self.var_Fr = float( self.var_Fr_entry.get() )
				else:
					self.Fr_k = float( self.Fr_k_entry.get() )
					self.Fr_theta = float( self.Fr_theta_entry.get() )
				if( self.dist_rho_p in [ 1 , 2 , 4 ] ):
					self.rho_p = float( self.rho_p_entry.get() )
					self.var_rho_p = float( self.var_rho_p_entry.get() )
				else:
					self.rho_p_k = float( self.rho_p_k_entry.get() )
					self.rho_p_theta = float( self.rho_p_theta_entry.get() )
				if( self.dist_rho_gas in [ 1 , 2 , 4 ] ):
					self.rho_gas = float( self.rho_gas_entry.get() )
					self.var_rho_gas = float( self.var_rho_gas_entry.get() )
				else:
					self.rho_gas_k = float( self.rho_gas_k_entry.get() )
					self.rho_gas_theta = float( self.rho_gas_theta_entry.get() )
				if( self.type_sim > 1 ):
					self.var_ws = 0.0
					self.var_Fr = 0.0
					self.var_rho_p = 0.0
					self.var_rho_gas = 0.0
			[ self.volume_vector , self.phi_0_vector , self.ws_vector , self.Fr_vector , self.rho_p_vector , self.rho_gas_vector , self.N , self.variable_vector , self.limits_calib , self.probability_save ] = create_inputs( self.type_sim , self.type_input , self.dist_volume , self.dist_phi_0 , self.dist_ws , self.dist_Fr , self.dist_rho_p , self.dist_rho_gas , file_path , self.volume , self.var_volume , self.volume_k , self.volume_theta , self.phi_0 , self.var_phi_0 , self.phi_0_k , self.phi_0_theta , self.ws , self.var_ws , self.ws_k , self.ws_theta , self.Fr , self.var_Fr , self.Fr_k , self.Fr_theta , self.rho_p , self.var_rho_p , self.rho_p_k , self.rho_p_theta , self.rho_gas , self.var_rho_gas , self.rho_gas_k , self.rho_gas_theta , self.calibration_type , self.dist_distance , self.distance , self.var_distance , self.distance_k , self.distance_theta , file_cumulative_distance , self.dist_area , self.area , self.var_area , self.area_k , self.area_theta , file_cumulative_area , self.N , 1 )

			if( len( self.volume_vector ) == 0 ):
				self.sample_properties_availability = 0
				self.properties_inputs = ""
				self.enabled_disabled()
				messagebox.showerror( title = None , message = "PDC properties were not sampled" )
				return
			self.sample_properties_availability = 1
			if( self.type_input == 1 ):
				self.properties_inputs = "Distribution type for PDC properties: Predefined distributions" + "\n"
				if( self.dist_volume == 1 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for collapsing volume: Gaussian" + "\n"
				elif( self.dist_volume == 2 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for collapsing volume: Uniform" + "\n"
				elif( self.dist_volume == 3 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for collapsing volume: Gamma" + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Distribution type for collapsing volume: Lognormal" + "\n"
				if( self.dist_volume in [ 1 , 2 , 4 ] ):
					self.properties_inputs = self.properties_inputs + "Expected collapsing volume [m3]: " + str( self.volume ) + "\n" + "Uncertainty of collapsing volume [m3]: " + str( self.var_volume ) + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Parameter k in gamma distribution (collapsing volume [m3]): " + str( self.volume_k ) + "\n" + "Parameter theta in gamma distribution (collapsing volume [m3]): " + str( self.volume_theta ) + "\n"
				if( self.dist_phi_0 == 1 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for initial concentration: Gaussian" + "\n"
				elif( self.dist_phi_0 == 2 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for initial concentration: Uniform" + "\n"
				elif( self.dist_phi_0 == 3 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for initial concentration: Gamma" + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Distribution type for initial concentration: Lognormal" + "\n"
				if( self.dist_phi_0 in [ 1 , 2 , 4 ] ):
					self.properties_inputs = self.properties_inputs + "Expected initial concentration: " + str( self.phi_0 ) + "\n" + "Uncertainty of initial concentration: " + str( self.var_phi_0 ) + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Parameter k in gamma distribution (initial concentration): " + str( self.phi_0_k ) + "\n" + "Parameter theta in gamma distribution (initial concentration): " + str( self.phi_0_theta ) + "\n"
				if( self.dist_ws == 1 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for sedimentation velocity: Gaussian" + "\n"
				elif( self.dist_ws == 2 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for sedimentation velocity: Uniform" + "\n"
				elif( self.dist_ws == 3 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for sedimentation velocity: Gamma" + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Distribution type for sedimentation velocity: Lognormal" + "\n"
				if( self.dist_ws in [ 1 , 2 , 4 ] ):
					self.properties_inputs = self.properties_inputs + "Expected sedimentation velocity [m/s]: " + str( self.ws ) + "\n" + "Uncertainty of sedimentation velocity [m/s]: " + str( self.var_ws ) + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Parameter k in gamma distribution (sedimentation velocity [m/s]): " + str( self.ws_k ) + "\n" + "Parameter theta in gamma distribution (sedimentation velocity [m/s]): " + str( self.ws_theta ) + "\n"
				if( self.dist_Fr == 1 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for Froude number: Gaussian" + "\n"
				elif( self.dist_Fr == 2 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for Froude number: Uniform" + "\n"
				elif( self.dist_Fr == 3 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for Froude number: Gamma" + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Distribution type for Froude number: Lognormal" + "\n"
				if( self.dist_Fr in [ 1 , 2 , 4 ] ):
					self.properties_inputs = self.properties_inputs + "Expected Froude number: " + str( self.Fr ) + "\n" + "Uncertainty of Froude number: " + str( self.var_Fr ) + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Parameter k in gamma distribution (Froude number): " + str( self.Fr_k ) + "\n" + "Parameter theta in gamma distribution (Froude number): " + str( self.Fr_theta ) + "\n"
				if( self.dist_rho_p == 1 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for pyroclasts density: Gaussian" + "\n"
				elif( self.dist_rho_p == 2 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for pyroclasts density: Uniform" + "\n"
				elif( self.dist_rho_p == 3 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for pyroclasts density: Gamma" + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Distribution type for pyroclasts density: Lognormal" + "\n"
				if( self.dist_rho_p in [ 1 , 2 , 4 ] ):
					self.properties_inputs = self.properties_inputs + "Expected pyroclasts density [kg/m3]: " + str( self.rho_p ) + "\n" + "Uncertainty of pyroclasts density [kg/m3]: " + str( self.var_rho_p ) + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Parameter k in gamma distribution (pyroclasts density [kg/m3]): " + str( self.rho_p_k ) + "\n" + "Parameter theta in gamma distribution (pyroclasts density [kg/m3]): " + str( self.rho_p_theta ) + "\n"
				if( self.dist_rho_gas == 1 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for gas density: Gaussian" + "\n"
				elif( self.dist_rho_gas == 2 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for gas density: Uniform" + "\n"
				elif( self.dist_rho_gas == 3 ):
					self.properties_inputs = self.properties_inputs + "Distribution type for gas density: Gamma" + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Distribution type for gas density: Lognormal" + "\n"
				if( self.dist_rho_gas in [ 1 , 2 , 4 ] ):
					self.properties_inputs = self.properties_inputs + "Expected gas density [kg/m3]: " + str( self.rho_gas ) + "\n" + "Uncertainty of gas density [kg/m3]: " + str( self.var_rho_gas ) + "\n"
				else:
					self.properties_inputs = self.properties_inputs + "Parameter k in gamma distribution (gas density [kg/m3]): " + str( self.rho_gas_k ) + "\n" + "Parameter theta in gamma distribution (gas density [kg/m3]): " + str( self.rho_gas_theta ) + "\n"

			elif( self.type_input == 2 ):
				self.properties_inputs = "Distribution type for PDC properties: Input file" + "\n"
				self.properties_inputs = self.properties_inputs + "File name: " + file_path + "\n"
			else:
				self.properties_inputs = "Distribution type for PDC properties: Calibration-based sampling" + "\n"
				if( self.calibration_type == 1 ):
					self.properties_inputs = self.properties_inputs + "Calibration type: Jaccard" + "\n" + "File name: " + file_path + "\n"
				elif( self.calibration_type == 3 ):
					self.properties_inputs = self.properties_inputs + "Calibration type: Hausdorff distance" + "\n" + "File name: " + file_path + "\n"
				elif( self.calibration_type == 2 ):
					self.properties_inputs = self.properties_inputs + "Calibration type: RMSD" + "\n" + "File name: " + file_path + "\n"
				elif( self.calibration_type == 5 ):
					self.properties_inputs = self.properties_inputs + "Calibration type: Runout distance-based" + "\n" + "File name: " + file_path + "\n"
					if( self.dist_distance == 1 ):
						self.properties_inputs = self.properties_inputs + "Distribution type for runout distance: Gaussian" + "\n"
					elif( self.dist_distance == 2 ):
						self.properties_inputs = self.properties_inputs + "Distribution type for runout distance: Uniform" + "\n"
					elif( self.dist_distance == 3 ):
						self.properties_inputs = self.properties_inputs + "Distribution type for runout distance: Gamma" + "\n"
					elif( self.dist_distance == 4 ):
						self.properties_inputs = self.properties_inputs + "Distribution type for runout distance: Lognormal" + "\n"
					else:
						self.properties_inputs = self.properties_inputs + "Distribution type for runout distance: Input file (CDF)" + "\n"
					if( self.dist_distance in [ 1 , 2 , 4 ] ):
						self.properties_inputs = self.properties_inputs + "Expected runout distance [m]: " + str( self.distance ) + "\n" + "Uncertainty of runout distance [m]: " + str( self.var_distance ) + "\n"
					elif( self.dist_distance == 3 ):
						self.properties_inputs = self.properties_inputs + "Parameter k in gamma distribution (runout distance [m]): " + str( self.distance_k ) + "\n" + "Parameter theta in gamma distribution (runout distance [m]): " + str( self.distance_theta ) + "\n"
					else:
						self.properties_inputs = self.properties_inputs + "File name: " + file_cumulative_distance + "\n"					
				elif( self.calibration_type == 7 ):
					self.properties_inputs = self.properties_inputs + "Calibration type: Inundation area-based" + "\n" + "File name: " + file_path + "\n"
					if( self.dist_area == 1 ):
						self.properties_inputs = self.properties_inputs + "Distribution type for inundation area: Gaussian" + "\n"
					elif( self.dist_area == 2 ):
						self.properties_inputs = self.properties_inputs + "Distribution type for inundation area: Uniform" + "\n"
					elif( self.dist_area == 3 ):
						self.properties_inputs = self.properties_inputs + "Distribution type for inundation area: Gamma" + "\n"
					elif( self.dist_area == 4 ):
						self.properties_inputs = self.properties_inputs + "Distribution type for inundation area: Lognormal" + "\n"
					else:
						self.properties_inputs = self.properties_inputs + "Distribution type for inundation area: Input file (CDF)" + "\n"
					if( self.dist_area in [ 1 , 2 , 4 ] ):
						self.properties_inputs = self.properties_inputs + "Expected inundation area [km2]: " + str( self.area ) + "\n" + "Uncertainty of inundation area [km2]: " + str( self.var_area ) + "\n"
					elif( self.dist_area == 3 ):
						self.properties_inputs = self.properties_inputs + "Parameter k in gamma distribution (inundation area [km2]): " + str( self.area_k ) + "\n" + "Parameter theta in gamma distribution (inundation area [km2]): " + str( self.area_theta ) + "\n"
					else:
						self.properties_inputs = self.properties_inputs + "File name: " + file_cumulative_area + "\n"				
			self.enabled_disabled()
			messagebox.showinfo( title = None , message = "PDC properties sampled successfully" )
			if( not self.N == self.N_choice ):
				self.boolean_polygon = 0
				self.vent_type = 1
				self.vent_dist = 1
				self.sample_vent_availability = 0
				self.sample_cal_availability = 0
				self.results_availability = 0
				self.vent_inputs = ""
				self.calib_inputs = ""
				self.run_inputs = ""
				self.enabled_disabled()		
				messagebox.showerror( title = None , message = "The previous loaded information was associated with other number of simulations. Sampling of vent position and calibration inputs were discarded." )
		except:
			self.sample_properties_availability = 0
			self.properties_inputs = ""
			self.enabled_disabled()
			messagebox.showerror( title = None , message = "PDC properties were not sampled" )

	def plot_properties( self ):
		plot_only_properties( self.volume_vector , self.phi_0_vector , self.ws_vector , self.Fr_vector, self.rho_p_vector , self.rho_gas_vector , self.variable_vector , self.type_input , self.calibration_type , self.limits_calib , self.probability_save )
		plt.show()

	def runsim( self ):
		try:
			self.max_levels = int( self.max_levels_entry.get() )
			comp_polygon = ""
			if( self.type_sim == 1 ):
				[ self.matrix_compare , self.vertices_compare , self.string_compare , self.data_direction ] = [ np.nan , np.nan , np.nan , np.nan ]
			else:
				if( self.boolean_polygon ):
					comp_polygon = "Yes"
			[ self.angstep , self.distep , self.anglen , self.pix_min , self.angstep_res2 , self.angstep_res3 , self.anglen_res2 , self.anglen_res3 , self.vector_correc , self.vector_backward_1 , self.vector_backward_2 , self.index_max ] = initial_definitions( self.redist_volume )
			if( self.source_dem == 1 or self.source_dem == 3 ):
				[ self.summary_data , self.area_pixel , self.sim_data , self.string_data , self.string_cones ] = definitions_save_data_deg( self.source_dem , self.volume_vector , self.phi_0_vector , self.ws_vector , self.Fr_vector , self.rho_p_vector , self.rho_gas_vector , self.lon_cen_vector , self.lat_cen_vector , self.step_lon_m , self.step_lat_m , self.N , self.max_levels )
				[ self.data_cones , self.polygon ] = [ np.nan , np.nan ]
				[ self.summary_data , self.string_data , self.string_cones , self.string_compare , self.sim_data , self.data_cones , self.polygon ] = compute_box_model_deg( self.type_sim , self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.step_lon_deg , self.step_lat_deg , self.step_lon_m , self.step_lat_m , self.lon_cen_vector , self.lat_cen_vector , self.matrix_lon , self.matrix_lat , self.volume_vector , self.phi_0_vector , self.ws_vector , self.Fr_vector , self.rho_p_vector , self.rho_gas_vector , self.g , self.cells_lon , self.cells_lat , self.Topography , self.angstep , self.angstep_res2 , self.angstep_res3 , self.distep , self.area_pixel , self.max_levels , self.N , self.redist_volume , self.save_data , self.summary_data , self.string_data , self.string_cones , self.sim_data , self.anglen , self.pix_min , self.vector_backward_1 , self.vector_backward_2 , self.index_max , self.vector_correc , self.matrix_compare , self.vertices_compare , self.string_compare , self.data_direction , comp_polygon )
			else:
				[ self.summary_data , self.area_pixel , self.sim_data , self.string_data , self.string_cones ] = definitions_save_data_utm( self.source_dem , self.volume_vector , self.phi_0_vector , self.ws_vector , self.Fr_vector , self.rho_p_vector , self.rho_gas_vector , self.east_cen_vector , self.north_cen_vector , self.cellsize , self.N , self.max_levels )
				[ self.data_cones , self.polygon ] = [ np.nan , np.nan ]
				[ self.summary_data , self.string_data , self.string_cones , self.string_compare , self.sim_data , self.data_cones , self.polygon ] = compute_box_model_utm( self.type_sim , self.n_north , self.n_east , self.east_cor , self.north_cor , self.east_cen_vector , self.north_cen_vector , self.matrix_north , self.matrix_east , self.volume_vector , self.phi_0_vector , self.ws_vector , self.Fr_vector , self.rho_p_vector , self.rho_gas_vector , self.g , self.cellsize , self.Topography , self.angstep , self.angstep_res2 , self.angstep_res3 , self.distep , self.area_pixel , self.max_levels , self.N , self.redist_volume , self.save_data , self.summary_data , self.string_data , self.string_cones , self.sim_data , self.anglen , self.pix_min , self.vector_backward_1 , self.vector_backward_2 , self.index_max , self.vector_correc , self.matrix_compare , self.vertices_compare , self.string_compare , self.data_direction , comp_polygon )
			self.results_availability = 1
			self.enabled_disabled()
			if( self.type_sim == 1 ):
				self.run_inputs = "Simulation type: Default mode" + "\n"
			else:
				if( self.boolean_polygon == 1 ):
					self.run_inputs = "Simulation type: Calibration mode (Including reference PDC deposit polygon)" + "\n"
				else:
					self.run_inputs = "Simulation type: Calibration mode (Based on the distribution of PDC runout distance or inundation area)" + "\n"
			self.run_inputs = self.run_inputs + "Number of generations: " + str( self.max_levels ) + "\n" + "Number of Simulations: " + str( self.N ) + "\n"
			messagebox.showinfo( title = None , message = "Simulations finished" )
		except:
			self.results_availability = 0
			self.run_inputs = ""
			self.enabled_disabled()
			messagebox.showerror( title = None , message = "Simulations were not finished" )

	def plotres( self ):
		if( self.source_dem == 1 or self.source_dem == 3 ):
			plot_only_map_deg( self.Cities , self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.step_lat_m , self.step_lon_m , self.matrix_lon , self.matrix_lat , self.lon_cen_vector , self.lat_cen_vector , self.Topography , self.Topography_Sea , self.N , self.data_cones )
		else:		
			plot_only_map_utm( self.matrix_east , self.matrix_north , self.east_cor , self.north_cor , self.n_east , self.n_north , self.cellsize , self.east_cen_vector , self.north_cen_vector , self.Topography , self.Topography_Sea , self.N , self.data_cones )
		if( self.type_sim == 2 ):
			comp_polygon = ""
			if( self.boolean_polygon ):
				comp_polygon = "Yes"
			plot_only_calibration( self.string_compare , self.vertices_compare , self.N , comp_polygon )
		else:
			plot_input_output( self.summary_data )
		plt.show()

	def saveres( self ):
		run_name = str( self.runname_entry.get() )
		try:
			os.mkdir('Results')
		except:
			pass
		try:
			os.mkdir('Results/' + run_name)
		except:
			pass
		if( self.source_dem == 1 or self.source_dem == 3 ):
			save_data_deg( run_name , self.source_dem , 0 , self.lon1 , self.lon2 , self.lat1 , self.lat2 , self.step_lon_m , self.step_lat_m , self.cells_lon , self.cells_lat , self.matrix_lon , self.matrix_lat , self.Topography , self.Topography_Sea , self.N , self.summary_data , self.string_data , self.string_cones , self.sim_data , self.data_cones, self.utm_save , 0 )
		else:
			save_data_utm( run_name , 0 , self.n_north , self.n_east , self.cellsize , self.matrix_east , self.matrix_north , self.Topography , self.Topography_Sea , self.N , self.summary_data , self.string_data , self.string_cones , self.string_compare , self.sim_data , self.data_cones , self.utm_save , 0 )
		if( self.type_sim == 2 ):
			calibration( run_name , self.string_compare , self.resolution_factor , self.ws_vector[ 0 ] , self.Fr_vector[ 0 ] , self.rho_p_vector[ 0 ] , self.rho_gas_vector[ 0 ] )
		text_file = open( 'Results/' + run_name + '/' + 'input_parameters.txt' , 'w' )
		text_file.write( self.run_inputs + "\n" )
		text_file.write( self.topography_inputs + "\n" )
		text_file.write( self.vent_inputs + "\n" )
		text_file.write( self.properties_inputs + "\n" )
		if( self.type_sim == 2 ):
			text_file.write( self.calib_inputs + "\n" )
		text_file.close()		
		messagebox.showinfo( title = None , message = "Results saved" )

	def enabled_disabled( self ):
		if( self.source_dem_choice == 1 ):
			bol_lonlat = 1
		else:
			bol_lonlat = 0
		if( self.topography_availability == 1 ):
			self.loaded_topo.config( text = "Loaded" )
			bol_plot_top = 1
			if( self.source_dem == 1 or self.source_dem == 3 ):
				self.loaded_coordinates.config( text = "Longitude / Latitude" )
			else:
				self.loaded_coordinates.config( text = "UTM" )
			if( self.type_sim_choice == 1 ):
				bol_vent_type = 1
				bol_sam_calib = 0
			else:
				bol_vent_type = -1
				self.vent_type_choice = 1
				if( self.sample_vent_availability == 1 ):
					bol_sam_calib = 1
				else:
					bol_sam_calib = 0
			if( self.vent_type_choice <= 3 ):
				if( self.source_dem == 1 or self.source_dem == 3 ):
					bol_lonlatcol = 1
					bol_eastnorthcol = 0
				else:
					bol_lonlatcol = 0
					bol_eastnorthcol = 1
				if( self.vent_type_choice == 1 ):
					bol_line = 0
					bol_circ = 0
				elif( self.vent_type_choice == 2 ):
					bol_line = 1
					bol_circ = 0
				else:
					bol_line = 0
					bol_circ = 1
				if( self.type_sim_choice == 1 ):
					bol_varcen = 1
				else:
					bol_varcen = -1
			else:
				bol_lonlatcol = 0
				bol_eastnorthcol = 0
				bol_line = 0
				bol_circ = 0
				bol_varcen = 0
			bol_sam_vent = 1
			if( self.sample_vent_availability == 1 ):
				self.loaded_vent.config( text = "Sampled" )
				bol_plot_vent = 1
			else:
				self.loaded_vent.config( text = "Not sampled" )
				bol_plot_vent = 0
			if( self.sample_cal_availability == 1 ):
				self.loaded_calib.config( text = "Defined" )
				if( self.boolean_polygon == 1 ):
					bol_plot_calib = 1
				else:
					bol_plot_calib = 0
			else:
				if( np.isnan( self.type_sim ) ):
					self.loaded_calib.config( text = "Not defined / Not needed" )
				elif( self.type_sim == 1 ):
					self.loaded_calib.config( text = "Not needed" )
				elif( self.type_sim == 2 ):
					self.loaded_calib.config( text = "Not defined" )
				bol_plot_calib = 0
		else:
			self.loaded_topo.config( text = "Not loaded" )
			self.loaded_coordinates.config( text = "Not defined" )
			self.loaded_vent.config( text = "Not sampled" )
			bol_plot_top = 0
			bol_vent_type = 0
			bol_lonlatcol = 0
			bol_eastnorthcol = 0
			bol_line = 0
			bol_circ = 0
			bol_varcen = 0
			bol_sam_vent = 0
			bol_plot_vent = 0
			bol_sam_calib = 0
			bol_plot_calib = 0
			if( np.isnan( self.type_sim ) ):
				self.loaded_calib.config( text = "Not defined / Not needed" )
			elif( self.type_sim == 1 ):
				self.loaded_calib.config( text = "Not needed" )
			elif( self.type_sim == 2 ):
				self.loaded_calib.config( text = "Not defined" )
		if( self.type_sim_choice == 1 ):
			bol_typeinput = 1
			if( self.type_input_choice == 1 ):
				bol_labelpres = 1
				bol_dist_properties = 1
				if( self.dist_volume_choice in [ 1 , 2 , 4 ] ):
					bol_volume_gaus = 1
					bol_volume_gam = 0
				else:
					bol_volume_gaus = 0
					bol_volume_gam = 1
				if( self.dist_phi_0_choice in [ 1 , 2 , 4 ] ):
					bol_phi_0_gaus = 1
					bol_phi_0_gam = 0
				else:
					bol_phi_0_gaus = 0
					bol_phi_0_gam = 1
				if( self.dist_ws_choice in [ 1 , 2 , 4 ] ):
					bol_ws_gaus = 1
					bol_ws_gam = 0
				else:
					bol_ws_gaus = 0
					bol_ws_gam = 1
				if( self.dist_Fr_choice in [ 1 , 2 , 4 ] ):
					bol_Fr_gaus = 1
					bol_Fr_gam = 0
				else:
					bol_Fr_gaus = 0
					bol_Fr_gam = 1
				if( self.dist_rho_p_choice in [ 1 , 2 , 4 ] ):
					bol_rho_p_gaus = 1
					bol_rho_p_gam = 0
				else:
					bol_rho_p_gaus = 0
					bol_rho_p_gam = 1
				if( self.dist_rho_gas_choice in [ 1 , 2 , 4 ] ):
					bol_rho_gas_gaus = 1
					bol_rho_gas_gam = 0
				else:
					bol_rho_gas_gaus = 0
					bol_rho_gas_gam = 1
				bol_label_calib = 0
				bol_dist_distance = 0
				bol_distance_gaus = 0
				bol_distance_gam = 0
				bol_dist_area = 0
				bol_area_gaus = 0
				bol_area_gam = 0				
			elif( self.type_input_choice == 2 ):
				bol_labelpres = 0
				bol_dist_properties = 0
				bol_volume_gaus = 0
				bol_volume_gam = 0
				bol_phi_0_gaus = 0
				bol_phi_0_gam = 0
				bol_ws_gaus = 0
				bol_ws_gam = 0
				bol_Fr_gaus = 0
				bol_Fr_gam = 0
				bol_rho_p_gaus = 0
				bol_rho_p_gam = 0
				bol_rho_gas_gaus = 0
				bol_rho_gas_gam = 0
				bol_label_calib = 0
				bol_dist_distance = 0
				bol_distance_gaus = 0
				bol_distance_gam = 0
				bol_dist_area = 0
				bol_area_gaus = 0
				bol_area_gam = 0
			else:
				bol_labelpres = 0
				bol_dist_properties = 0
				bol_volume_gaus = 0
				bol_volume_gam = 0
				bol_phi_0_gaus = 0
				bol_phi_0_gam = 0
				bol_ws_gaus = 0
				bol_ws_gam = 0
				bol_Fr_gaus = 0
				bol_Fr_gam = 0
				bol_rho_p_gaus = 0
				bol_rho_p_gam = 0
				bol_rho_gas_gaus = 0
				bol_rho_gas_gam = 0
				bol_label_calib = 1
				if( self.calibration_type_choice <= 3 ):
					bol_dist_distance = 0
					bol_distance_gaus = 0
					bol_distance_gam = 0
					bol_dist_area = 0
					bol_area_gaus = 0
					bol_area_gam = 0
				elif( self.calibration_type_choice == 5 ):
					bol_dist_distance = 1
					if( self.dist_distance_choice in [ 1 , 2 , 4 ] ):
						bol_distance_gaus = 1
						bol_distance_gam = 0
					elif( self.dist_distance_choice == 3 ):
						bol_distance_gaus = 0
						bol_distance_gam = 1
					else:
						bol_distance_gaus = 0
						bol_distance_gam = 0
					bol_dist_area = 0
					bol_area_gaus = 0
					bol_area_gam = 0
				else:
					bol_dist_distance = 0
					bol_distance_gaus = 0
					bol_distance_gam = 0
					bol_dist_area = 1
					if( self.dist_area_choice in [ 1 , 2 , 4 ] ):
						bol_area_gaus = 1
						bol_area_gam = 0
					elif( self.dist_area_choice == 3 ):
						bol_area_gaus = 0
						bol_area_gam = 1
					else:
						bol_area_gaus = 0
						bol_area_gam = 0					
		else:
			bol_typeinput = -1
			bol_labelpres = 1
			bol_dist_properties = -1
			bol_volume_gaus = 1
			bol_volume_gam = 0
			bol_phi_0_gaus = 1
			bol_phi_0_gam = 0
			bol_ws_gaus = 2
			bol_ws_gam = 0
			bol_Fr_gaus = 2
			bol_Fr_gam = 0
			bol_rho_p_gaus = 2
			bol_rho_p_gam = 0
			bol_rho_gas_gaus = 2
			bol_rho_gas_gam = 0
			bol_label_calib = 0
			bol_dist_distance = 0
			bol_distance_gaus = 0
			bol_distance_gam = 0
			bol_dist_area = 0
			bol_area_gaus = 0
			bol_area_gam = 0
		bol_sam_properties = 1
		if( self.sample_properties_availability == 1 ):
			self.loaded_properties.config( text = "Sampled" )
			bol_plot_properties = 1
		else:
			self.loaded_properties.config( text = "Not sampled" )
			bol_plot_properties = 0
		if( self.results_availability == 1 ):
			bol_plotres = 1
		else:
			bol_plotres = 0
		if( np.isnan( self.type_sim ) ):
			self.loaded_typesimulation.config( text = "Not defined" )
		elif( self.type_sim == 1 ):
			self.loaded_typesimulation.config( text = "Default mode" )
		elif( self.type_sim == 2 ):
			self.loaded_typesimulation.config( text = "Calibration mode" )
		if( self.sample_vent_availability == 1 and self.sample_properties_availability == 1 and ( self.type_sim == 1 or ( self.type_sim == 2 and self.sample_cal_availability == 1 ) ) ):
			bol_runsim = 1
		else:
			bol_runsim = 0
		if( self.sample_vent_availability == 1 or self.sample_properties_availability == 1 ):
			self.loaded_numbersim.config( text = str( self.N ) )
		else:
			self.loaded_numbersim.config( text = "Not defined" )

		self.set_fields( bol_lonlat , bol_plot_top , bol_vent_type , bol_lonlatcol , bol_eastnorthcol , bol_line , bol_circ , bol_varcen , bol_sam_vent , bol_plot_vent , bol_sam_calib , bol_plot_calib , bol_typeinput , bol_labelpres , bol_dist_properties , bol_volume_gaus , bol_volume_gam , bol_phi_0_gaus , bol_phi_0_gam , bol_ws_gaus , bol_ws_gam , bol_Fr_gaus , bol_Fr_gam , bol_rho_p_gaus , bol_rho_p_gam , bol_rho_gas_gaus , bol_rho_gas_gam , bol_label_calib , bol_dist_distance , bol_distance_gaus , bol_distance_gam , bol_dist_area , bol_area_gaus , bol_area_gam , bol_sam_properties , bol_plot_properties , bol_runsim , bol_plotres )

	def set_fields( self , bol_lonlat , bol_plot_top , bol_vent_type , bol_lonlatcol , bol_eastnorthcol , bol_line , bol_circ , bol_varcen , bol_sam_vent , bol_plot_vent , bol_sam_calib , bol_plot_calib , bol_typeinput , bol_labelpres , bol_dist_properties , bol_volume_gaus, bol_volume_gam , bol_phi_0_gaus , bol_phi_0_gam , bol_ws_gaus , bol_ws_gam , bol_Fr_gaus , bol_Fr_gam , bol_rho_p_gaus , bol_rho_p_gam , bol_rho_gas_gaus , bol_rho_gas_gam , bol_label_calib , bol_dist_distance , bol_distance_gaus , bol_distance_gam , bol_dist_area , bol_area_gaus , bol_area_gam , bol_sam_properties , bol_plot_properties , bol_runsim , bol_plotres ):

		if( bol_lonlat == 1 ):
			self.lon1_entry.configure( state = 'normal' )
			self.lon2_entry.configure( state = 'normal' )
			self.lat1_entry.configure( state = 'normal' )
			self.lat2_entry.configure( state = 'normal' )
			self.label_lon1.configure( state = 'normal' )
			self.label_lon2.configure( state = 'normal' )
			self.label_lat1.configure( state = 'normal' )
			self.label_lat2.configure( state = 'normal' )
		else:
			self.lon1_entry.configure( state = 'disabled' )
			self.lon2_entry.configure( state = 'disabled' )
			self.lat1_entry.configure( state = 'disabled' )
			self.lat2_entry.configure( state = 'disabled' )
			self.label_lon1.configure( state = 'disabled' )
			self.label_lon2.configure( state = 'disabled' )
			self.label_lat1.configure( state = 'disabled' )
			self.label_lat2.configure( state = 'disabled' )
		if( bol_plot_top == 1 ):
			self.but_plot_topography.configure( state = 'normal' )
		else:
			self.but_plot_topography.configure( state = 'disabled' )
		if( bol_vent_type == 1 ):
			self.label_venttype.configure( state = 'normal' )
			self.venttype_entry.configure( state = 'normal' )
		elif( bol_vent_type == -1 ):
			self.label_venttype.configure( state = 'disabled' )
			self.venttype_entry.configure( state = 'normal' )
			self.venttype.set( "Pointwise" )
			self.venttype_entry.configure( state = 'disabled' )
		else:
			self.label_venttype.configure( state = 'disabled' )
			self.venttype_entry.configure( state = 'disabled' )
		if( bol_lonlatcol == 1 ):
			self.label_loncen.configure( state = 'normal' )
			self.loncen_entry.configure( state = 'normal' )
			self.label_latcen.configure( state = 'normal' )
			self.latcen_entry.configure( state = 'normal' )
		else:			
			self.label_loncen.configure( state = 'disabled' )
			self.loncen_entry.configure( state = 'disabled' )
			self.label_latcen.configure( state = 'disabled' )
			self.latcen_entry.configure( state = 'disabled' )
		if( bol_eastnorthcol == 1 ):
			self.label_eastcen.configure( state = 'normal' )
			self.eastcen_entry.configure( state = 'normal' )
			self.label_northcen.configure( state = 'normal' )
			self.northcen_entry.configure( state = 'normal' )
		else:
			self.label_eastcen.configure( state = 'disabled' )
			self.eastcen_entry.configure( state = 'disabled' )
			self.label_northcen.configure( state = 'disabled' )
			self.northcen_entry.configure( state = 'disabled' )
		if( bol_line == 1 ):
			self.label_azimuthline.configure( state = 'normal' )
			self.azimuthline_entry.configure( state = 'normal' )
			self.label_lengthline.configure( state = 'normal' )
			self.lengthline_entry.configure( state = 'normal' )
		else:
			self.label_azimuthline.configure( state = 'disabled' )
			self.azimuthline_entry.configure( state = 'disabled' )
			self.label_lengthline.configure( state = 'disabled' )
			self.lengthline_entry.configure( state = 'disabled' )	
		if( bol_circ == 1 ):
			self.label_radcir.configure( state = 'normal' )
			self.radcir_entry.configure( state = 'normal' )
			self.label_ang1cir.configure( state = 'normal' )
			self.ang1cir_entry.configure( state = 'normal' )
			self.label_ang2cir.configure( state = 'normal' )
			self.ang2cir_entry.configure( state = 'normal' )
		else:
			self.label_radcir.configure( state = 'disabled' )
			self.radcir_entry.configure( state = 'disabled' )
			self.label_ang1cir.configure( state = 'disabled' )
			self.ang1cir_entry.configure( state = 'disabled' )
			self.label_ang2cir.configure( state = 'disabled' )
			self.ang2cir_entry.configure( state = 'disabled' )
		if( bol_varcen == 1 ):
			self.label_varcen.configure( state = 'normal' )
			self.varcen_entry.configure( state = 'normal' )
			self.label_ventdist.configure( state = 'normal' )
			self.ventdist_entry.configure( state = 'normal' )
		elif( bol_varcen == -1 ):
			self.label_varcen.configure( state = 'disabled' )
			self.varcen_entry.configure( state = 'normal' )
			self.varcen.set( 0.0 )
			self.varcen_entry.configure( state = 'disabled' )
			self.label_ventdist.configure( state = 'disabled' )
			self.ventdist_entry.configure( state = 'disabled' )
		else:
			self.label_varcen.configure( state = 'disabled' )
			self.varcen_entry.configure( state = 'disabled' )
			self.label_ventdist.configure( state = 'disabled' )
			self.ventdist_entry.configure( state = 'disabled' )
		if( bol_sam_vent == 1 ):
			self.but_sample_vent.configure( state = 'normal' )
		else:
			self.but_sample_vent.configure( state = 'disabled' )
		if( bol_plot_vent == 1 ):
			self.but_plot_vent.configure( state = 'normal' )
		else:
			self.but_plot_vent.configure( state = 'disabled' )
		if( bol_sam_calib == 1 ):
			self.but_sample_calib.configure( state = 'normal' )
		else:
			self.but_sample_calib.configure( state = 'disabled' )
		if( bol_plot_calib == 1 ):
			self.but_plot_calib.configure( state = 'normal' )
		else:
			self.but_plot_calib.configure( state = 'disabled' )
		if( bol_typeinput == 1 ):
			self.label_type_input.configure( state = 'normal' )
			self.type_input_entry.configure( state = 'normal' )
		elif( bol_typeinput == -1 ):
			self.label_type_input.configure( state = 'disabled' )
			self.type_input_entry.configure( state = 'normal' )
			self.typeinput.set( "Predefined distributions" )
			self.type_input_entry.configure( state = 'disabled' )
			self.type_input_choice = 1
		if( bol_labelpres == 1 ):
			self.label_prescribed.configure( state = 'normal' )
		else:
			self.label_prescribed.configure( state = 'disabled' )
		if( bol_dist_properties == 1 ):
			self.label_dist_volume.configure( state = 'normal' )
			self.dist_volume_entry.configure( state = 'normal' )
			self.label_dist_phi_0.configure( state = 'normal' )
			self.dist_phi_0_entry.configure( state = 'normal' )
			self.label_dist_ws.configure( state = 'normal' )
			self.dist_ws_entry.configure( state = 'normal' )
			self.label_dist_Fr.configure( state = 'normal' )
			self.dist_Fr_entry.configure( state = 'normal' )
			self.label_dist_rho_p.configure( state = 'normal' )
			self.dist_rho_p_entry.configure( state = 'normal' )
			self.label_dist_rho_gas.configure( state = 'normal' )
			self.dist_rho_gas_entry.configure( state = 'normal' )
		elif( bol_dist_properties == -1 ):
			self.label_dist_volume.configure( state = 'disabled' )
			self.dist_volume_entry.configure( state = 'normal' )
			self.distvolume.set( "Uniform" )
			self.dist_volume_entry.configure( state = 'disabled' )
			self.dist_volume_choice = 2			
			self.label_dist_phi_0.configure( state = 'disabled' )
			self.dist_phi_0_entry.configure( state = 'normal' )
			self.distphi_0.set( "Uniform" )
			self.dist_phi_0_entry.configure( state = 'disabled' )
			self.dist_phi_0_choice = 2
			self.label_dist_ws.configure( state = 'disabled' )
			self.dist_ws_entry.configure( state = 'normal' )
			self.distws.set( "Uniform" )
			self.dist_ws_entry.configure( state = 'disabled' )
			self.dist_ws_choice = 2
			self.label_dist_Fr.configure( state = 'disabled' )
			self.dist_Fr_entry.configure( state = 'normal' )
			self.distFr.set( "Uniform" )
			self.dist_Fr_entry.configure( state = 'disabled' )
			self.dist_Fr_choice = 2
			self.label_dist_rho_p.configure( state = 'disabled' )
			self.dist_rho_p_entry.configure( state = 'normal' )
			self.distrho_p.set( "Uniform" )
			self.dist_rho_p_entry.configure( state = 'disabled' )
			self.dist_rho_p_choice = 2
			self.label_dist_rho_gas.configure( state = 'disabled' )
			self.dist_rho_gas_entry.configure( state = 'normal' )
			self.distrho_gas.set( "Uniform" )
			self.dist_rho_gas_entry.configure( state = 'disabled' )
			self.dist_rho_gas_choice = 2
		else:
			self.label_dist_volume.configure( state = 'disabled' )
			self.dist_volume_entry.configure( state = 'disabled' )
			self.label_dist_phi_0.configure( state = 'disabled' )
			self.dist_phi_0_entry.configure( state = 'disabled' )
			self.label_dist_ws.configure( state = 'disabled' )
			self.dist_ws_entry.configure( state = 'disabled' )
			self.label_dist_Fr.configure( state = 'disabled' )
			self.dist_Fr_entry.configure( state = 'disabled' )
			self.label_dist_rho_p.configure( state = 'disabled' )
			self.dist_rho_p_entry.configure( state = 'disabled' )
			self.label_dist_rho_gas.configure( state = 'disabled' )
			self.dist_rho_gas_entry.configure( state = 'disabled' )
		if( bol_volume_gaus == 1 ):
			self.label_volume.configure( state = 'normal' )
			self.volume_entry.configure( state = 'normal' )
			self.label_var_volume.configure( state = 'normal' )
			self.var_volume_entry.configure( state = 'normal' )
		else:
			self.label_volume.configure( state = 'disabled' )
			self.volume_entry.configure( state = 'disabled' )
			self.label_var_volume.configure( state = 'disabled' )
			self.var_volume_entry.configure( state = 'disabled' )
		if( bol_volume_gam == 1 ):
			self.label_volume_k.configure( state = 'normal' )
			self.volume_k_entry.configure( state = 'normal' )
			self.label_volume_theta.configure( state = 'normal' )
			self.volume_theta_entry.configure( state = 'normal' )
		else:
			self.label_volume_k.configure( state = 'disabled' )
			self.volume_k_entry.configure( state = 'disabled' )
			self.label_volume_theta.configure( state = 'disabled' )
			self.volume_theta_entry.configure( state = 'disabled' )
		if( bol_phi_0_gaus == 1 ):
			self.label_phi_0.configure( state = 'normal' )
			self.phi_0_entry.configure( state = 'normal' )
			self.label_var_phi_0.configure( state = 'normal' )
			self.var_phi_0_entry.configure( state = 'normal' )
		else:
			self.label_phi_0.configure( state = 'disabled' )
			self.phi_0_entry.configure( state = 'disabled' )
			self.label_var_phi_0.configure( state = 'disabled' )
			self.var_phi_0_entry.configure( state = 'disabled' )
		if( bol_phi_0_gam == 1 ):
			self.label_phi_0_k.configure( state = 'normal' )
			self.phi_0_k_entry.configure( state = 'normal' )
			self.label_phi_0_theta.configure( state = 'normal' )
			self.phi_0_theta_entry.configure( state = 'normal' )
		else:
			self.label_phi_0_k.configure( state = 'disabled' )
			self.phi_0_k_entry.configure( state = 'disabled' )
			self.label_phi_0_theta.configure( state = 'disabled' )
			self.phi_0_theta_entry.configure( state = 'disabled' )
		if( bol_ws_gaus == 1 ):
			self.label_ws.configure( state = 'normal' )
			self.ws_entry.configure( state = 'normal' )
			self.label_var_ws.configure( state = 'normal' )
			self.var_ws_entry.configure( state = 'normal' )
		elif( bol_ws_gaus == 0 ):
			self.label_ws.configure( state = 'disabled' )
			self.ws_entry.configure( state = 'disabled' )
			self.label_var_ws.configure( state = 'disabled' )
			self.var_ws_entry.configure( state = 'disabled' )
		else:
			self.label_ws.configure( state = 'normal' )
			self.ws_entry.configure( state = 'normal' )
			self.label_var_ws.configure( state = 'disabled' )
			self.var_ws_entry.configure( state = 'normal' )
			self.varws.set( 0.0 )
			self.var_ws_entry.configure( state = 'disabled' )
		if( bol_ws_gam == 1 ):
			self.label_ws_k.configure( state = 'normal' )
			self.ws_k_entry.configure( state = 'normal' )
			self.label_ws_theta.configure( state = 'normal' )
			self.ws_theta_entry.configure( state = 'normal' )
		else:
			self.label_ws_k.configure( state = 'disabled' )
			self.ws_k_entry.configure( state = 'disabled' )
			self.label_ws_theta.configure( state = 'disabled' )
			self.ws_theta_entry.configure( state = 'disabled' )
		if( bol_Fr_gaus == 1 ):
			self.label_Fr.configure( state = 'normal' )
			self.Fr_entry.configure( state = 'normal' )
			self.label_var_Fr.configure( state = 'normal' )
			self.var_Fr_entry.configure( state = 'normal' )
		elif( bol_Fr_gaus == 0 ):
			self.label_Fr.configure( state = 'disabled' )
			self.Fr_entry.configure( state = 'disabled' )
			self.label_var_Fr.configure( state = 'disabled' )
			self.var_Fr_entry.configure( state = 'disabled' )
		else:
			self.label_Fr.configure( state = 'normal' )
			self.Fr_entry.configure( state = 'normal' )
			self.label_var_Fr.configure( state = 'disabled' )
			self.var_Fr_entry.configure( state = 'normal' )
			self.varFr.set( 0.0 )
			self.var_Fr_entry.configure( state = 'disabled' )
		if( bol_Fr_gam == 1 ):
			self.label_Fr_k.configure( state = 'normal' )
			self.Fr_k_entry.configure( state = 'normal' )
			self.label_Fr_theta.configure( state = 'normal' )
			self.Fr_theta_entry.configure( state = 'normal' )
		else:
			self.label_Fr_k.configure( state = 'disabled' )
			self.Fr_k_entry.configure( state = 'disabled' )
			self.label_Fr_theta.configure( state = 'disabled' )
			self.Fr_theta_entry.configure( state = 'disabled' )
		if( bol_rho_p_gaus == 1 ):
			self.label_rho_p.configure( state = 'normal' )
			self.rho_p_entry.configure( state = 'normal' )
			self.label_var_rho_p.configure( state = 'normal' )
			self.var_rho_p_entry.configure( state = 'normal' )
		elif( bol_rho_p_gaus == 0 ):
			self.label_rho_p.configure( state = 'disabled' )
			self.rho_p_entry.configure( state = 'disabled' )
			self.label_var_rho_p.configure( state = 'disabled' )
			self.var_rho_p_entry.configure( state = 'disabled' )
		else:
			self.label_rho_p.configure( state = 'normal' )
			self.rho_p_entry.configure( state = 'normal' )
			self.label_var_rho_p.configure( state = 'disabled' )
			self.var_rho_p_entry.configure( state = 'normal' )
			self.varrho_p.set( 0.0 )
			self.var_rho_p_entry.configure( state = 'disabled' )
		if( bol_rho_p_gam == 1 ):
			self.label_rho_p_k.configure( state = 'normal' )
			self.rho_p_k_entry.configure( state = 'normal' )
			self.label_rho_p_theta.configure( state = 'normal' )
			self.rho_p_theta_entry.configure( state = 'normal' )
		else:
			self.label_rho_p_k.configure( state = 'disabled' )
			self.rho_p_k_entry.configure( state = 'disabled' )
			self.label_rho_p_theta.configure( state = 'disabled' )
			self.rho_p_theta_entry.configure( state = 'disabled' )
		if( bol_rho_gas_gaus == 1 ):
			self.label_rho_gas.configure( state = 'normal' )
			self.rho_gas_entry.configure( state = 'normal' )
			self.label_var_rho_gas.configure( state = 'normal' )
			self.var_rho_gas_entry.configure( state = 'normal' )
		elif( bol_rho_gas_gaus == 0 ):
			self.label_rho_gas.configure( state = 'disabled' )
			self.rho_gas_entry.configure( state = 'disabled' )
			self.label_var_rho_gas.configure( state = 'disabled' )
			self.var_rho_gas_entry.configure( state = 'disabled' )
		else:
			self.label_rho_gas.configure( state = 'normal' )
			self.rho_gas_entry.configure( state = 'normal' )
			self.label_var_rho_gas.configure( state = 'disabled' )
			self.var_rho_gas_entry.configure( state = 'normal' )
			self.varrho_gas.set( 0.0 )
			self.var_rho_gas_entry.configure( state = 'disabled' )
		if( bol_rho_gas_gam == 1 ):
			self.label_rho_gas_k.configure( state = 'normal' )
			self.rho_gas_k_entry.configure( state = 'normal' )
			self.label_rho_gas_theta.configure( state = 'normal' )
			self.rho_gas_theta_entry.configure( state = 'normal' )
		else:
			self.label_rho_gas_k.configure( state = 'disabled' )
			self.rho_gas_k_entry.configure( state = 'disabled' )
			self.label_rho_gas_theta.configure( state = 'disabled' )
			self.rho_gas_theta_entry.configure( state = 'disabled' )
		if( bol_label_calib == 1 ):
			self.label_calibrationbased.configure( state = 'normal' )
			self.label_calibration_type.configure( state = 'normal' )
			self.calibration_type_entry.configure( state = 'normal' )
		else:
			self.label_calibrationbased.configure( state = 'disabled' )
			self.label_calibration_type.configure( state = 'disabled' )
			self.calibration_type_entry.configure( state = 'disabled' )
		if( bol_dist_distance == 1 ):
			self.label_dist_distance.configure( state = 'normal' )
			self.dist_distance_entry.configure( state = 'normal' )
		else:
			self.label_dist_distance.configure( state = 'disabled' )
			self.dist_distance_entry.configure( state = 'disabled' )
		if( bol_distance_gaus == 1 ):
			self.label_distance.configure( state = 'normal' )
			self.distance_entry.configure( state = 'normal' )
			self.label_var_distance.configure( state = 'normal' )
			self.var_distance_entry.configure( state = 'normal' )
		else:
			self.label_distance.configure( state = 'disabled' )
			self.distance_entry.configure( state = 'disabled' )
			self.label_var_distance.configure( state = 'disabled' )
			self.var_distance_entry.configure( state = 'disabled' )
		if( bol_distance_gam == 1 ):
			self.label_distance_k.configure( state = 'normal' )
			self.distance_k_entry.configure( state = 'normal' )
			self.label_distance_theta.configure( state = 'normal' )
			self.distance_theta_entry.configure( state = 'normal' )
		else:
			self.label_distance_k.configure( state = 'disabled' )
			self.distance_k_entry.configure( state = 'disabled' )
			self.label_distance_theta.configure( state = 'disabled' )
			self.distance_theta_entry.configure( state = 'disabled' )
		if( bol_dist_area == 1 ):
			self.label_dist_area.configure( state = 'normal' )
			self.dist_area_entry.configure( state = 'normal' )
		else:
			self.label_dist_area.configure( state = 'disabled' )
			self.dist_area_entry.configure( state = 'disabled' )
		if( bol_area_gaus == 1 ):
			self.label_area.configure( state = 'normal' )
			self.area_entry.configure( state = 'normal' )
			self.label_var_area.configure( state = 'normal' )
			self.var_area_entry.configure( state = 'normal' )
		else:
			self.label_area.configure( state = 'disabled' )
			self.area_entry.configure( state = 'disabled' )
			self.label_var_area.configure( state = 'disabled' )
			self.var_area_entry.configure( state = 'disabled' )
		if( bol_area_gam == 1 ):
			self.label_area_k.configure( state = 'normal' )
			self.area_k_entry.configure( state = 'normal' )
			self.label_area_theta.configure( state = 'normal' )
			self.area_theta_entry.configure( state = 'normal' )
		else:
			self.label_area_k.configure( state = 'disabled' )
			self.area_k_entry.configure( state = 'disabled' )
			self.label_area_theta.configure( state = 'disabled' )
			self.area_theta_entry.configure( state = 'disabled' )
		if( bol_sam_properties == 1 ):
			self.but_sample_properties.configure( state = 'normal' )
		else:
			self.but_sample_properties.configure( state = 'disabled' )
		if( bol_plot_properties == 1 ):
			self.but_plot_properties.configure( state = 'normal' )
		else:
			self.but_plot_properties.configure( state = 'disabled' )
		if( bol_runsim == 1 ):
			self.but_runsim.configure( state = 'normal' )
		else:
			self.but_runsim.configure( state = 'disabled' )
		if( bol_plotres == 1 ):
			self.but_plotres.configure( state = 'normal' )
			self.but_saveres.configure( state = 'normal' )
		else:
			self.but_plotres.configure( state = 'disabled' )
			self.but_saveres.configure( state = 'disabled' )

if __name__ == '__main__':
	root = Tk()
	my_gui = MainFrame( root )
	root.after( 100 )
	root.mainloop()
