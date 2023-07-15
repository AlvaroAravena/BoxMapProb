import elevation
import tifffile
import numpy as np
import matplotlib.pyplot as plt
from math import sin , cos , sqrt , atan2 , radians , log , factorial , tan , cosh , atanh
from scipy import interpolate
from scipy.stats import norm , uniform , gamma , lognorm
from scipy.ndimage import gaussian_filter
import sys
import os
from PIL import Image, ImageDraw
import shutil
import utm
import warnings
import matplotlib.tri as tri
warnings.filterwarnings( "ignore" ) 
from scipy import sparse

# Auxiliary functions

def read_input():

	current_path = os.getcwd()
	try:
		file_txt = open( 'input_data.py' )
	except:
		print( 'input_data.py not found in ' + str( current_path ) + '.' )
		sys.exit( 0 )
	line = file_txt.readlines()
	file_txt.close()
	[ run_name , type_sim , source_dem , topography_file , comparison_polygon , ang_cal , ang_cal_range ] = [ '' , np.nan , np.nan , '' , '' , np.nan , np.nan ] 
	[ lon1 , lon2 , lat1 , lat2 , g ] = [ np.nan , np.nan , np.nan , np.nan , 9.8 ]
	[ vent_type , lon_cen , lat_cen , east_cen , north_cen , azimuth_lin , length_lin ] = [ np.nan , np.nan , np.nan , np.nan , np.nan , np.nan , np.nan ]
	[ radius_rad , ang1_rad , ang2_rad , var_cen , dist_input_cen , input_file_vent ] = [ np.nan , np.nan , np.nan , np.nan , np.nan , '' ]
	[ type_input , dist_input_volume , volume , var_volume , volume_k , volume_theta ] = [ np.nan , np.nan , np.nan , np.nan , np.nan , np.nan ]
	[ dist_input_phi_0 , phi_0 , var_phi_0 , phi_0_k , phi_0_theta ] = [ np.nan , np.nan , np.nan , np.nan , np.nan ]
	[ dist_input_ws , ws , var_ws , ws_k , ws_theta ] = [ np.nan , np.nan , np.nan , np.nan , np.nan ]
	[ dist_input_Fr , Fr , var_Fr , Fr_k , Fr_theta ] = [ np.nan , np.nan , np.nan , np.nan , np.nan ]
	[ dist_input_rho_p , rho_p , var_rho_p , rho_p_k , rho_p_theta ] = [ np.nan , np.nan , np.nan , np.nan , np.nan ]
	[ dist_input_rho_gas , rho_gas , var_rho_gas , rho_gas_k , rho_gas_theta , input_file_cal , calibration_type ] = [ np.nan , np.nan , np.nan , np.nan , np.nan , '' , np.nan ]
	[ dist_distance_calibration , distance_calibration , var_distance_calibration , distance_calibration_k ] = [ np.nan , np.nan , np.nan , np.nan ]
	[ distance_calibration_theta , file_cumulative_distance , dist_area_calibration , area_calibration , var_area_calibration ] = [ np.nan , '' , np.nan , np.nan , np.nan ]
	[ area_calibration_k , area_calibration_theta , file_cumulative_area , max_levels , N , save_data ] = [ np.nan , np.nan , '' , np.nan , np.nan , np.nan ]
	[ redist_volume , plot_flag , sea_flag ] = [ 4 , 1 , 0 ]
	for i in range( 0 , len( line ) ):
		line[ i ] = line[ i ].replace( '=' , ' ' )
		aux = line[ i ].split()
		if( len( aux ) > 0 ):
			if( aux[ 0 ][ 0 ] != '#' ):
				if( aux[ 0 ] == 'run_name' ):
					run_name = aux[ 1 ]
					run_name = run_name.replace( "'" , "" )
				if( aux[ 0 ] == 'type_sim' ):
					type_sim = int( aux[ 1 ] )
				if( aux[ 0 ] == 'source_dem' ):
					source_dem = int( aux[ 1 ] )
				if( aux[ 0 ] == 'topography_file' ):
					topography_file = aux[ 1 ]
					topography_file = topography_file.replace( "'" , "" )
				if( aux[ 0 ] == 'comparison_polygon' ):
					comparison_polygon = aux[ 1 ]
					comparison_polygon = comparison_polygon.replace( "'" , "" )
				if( aux[ 0 ] == 'ang_cal' ):
					ang_cal = float( aux[ 1 ] ) % 360.0
				if( aux[ 0 ] == 'ang_cal_range' ):
					ang_cal_range = min( float( aux[ 1 ] ) , 360.0 )
				if( aux[ 0 ] == 'lon1' ):
					lon1 = float( aux[ 1 ] )
				if( aux[ 0 ] == 'lon2' ):
					lon2 = float( aux[ 1 ] )
				if( aux[ 0 ] == 'lat1' ):
					lat1 = float( aux[ 1 ] )
				if( aux[ 0 ] == 'lat2' ):
					lat2 = float( aux[ 1 ] )
				if( aux[ 0 ] == 'g' ):
					g = float( aux[ 1 ] )
				if( aux[ 0 ] == 'vent_type' ):
					vent_type = int( aux[ 1 ] )
				if( aux[ 0 ] == 'lon_cen' ):
					lon_cen = float( aux[ 1 ] )
				if( aux[ 0 ] == 'lat_cen' ):
					lat_cen = float( aux[ 1 ] )
				if( aux[ 0 ] == 'east_cen' ):
					east_cen = float( aux[ 1 ] )
				if( aux[ 0 ] == 'north_cen' ):
					north_cen = float( aux[ 1 ] )
				if( aux[ 0 ] == 'azimuth_lin' ):
					azimuth_lin = float( aux[ 1 ] )
				if( aux[ 0 ] == 'length_lin' ):
					length_lin = float( aux[ 1 ] )
				if( aux[ 0 ] == 'radius_rad' ):
					radius_rad = float( aux[ 1 ] )
				if( aux[ 0 ] == 'ang1_rad' ):
					ang1_rad = float( aux[ 1 ] )
				if( aux[ 0 ] == 'ang2_rad' ):
					ang2_rad = float( aux[ 1 ] )
				if( aux[ 0 ] == 'var_cen' ):
					var_cen = float( aux[ 1 ] )
				if( aux[ 0 ] == 'dist_input_cen' ):
					dist_input_cen = int( aux[ 1 ] )
				if( aux[ 0 ] == 'input_file_vent' ):
					input_file_vent = aux[ 1 ]
					input_file_vent = input_file_vent.replace( "'" , "" )
				if( aux[ 0 ] == 'type_input' ):
					type_input = int( aux[ 1 ] )
				if( aux[ 0 ] == 'dist_input_volume' ):
					dist_input_volume = int( aux[ 1 ] )
				if( aux[ 0 ] == 'volume' ):
					volume = float( aux[ 1 ] )
				if( aux[ 0 ] == 'var_volume' ):
					var_volume = float( aux[ 1 ] )
				if( aux[ 0 ] == 'volume_k' ):
					volume_k = float( aux[ 1 ] )
				if( aux[ 0 ] == 'volume_theta' ):
					volume_theta = float( aux[ 1 ] )
				if( aux[ 0 ] == 'dist_input_phi_0' ):
					dist_input_phi_0 = int( aux[ 1 ] )
				if( aux[ 0 ] == 'phi_0' ):
					phi_0 = float( aux[ 1 ] )
				if( aux[ 0 ] == 'var_phi_0' ):
					var_phi_0 = float( aux[ 1 ] )
				if( aux[ 0 ] == 'phi_0_k' ):
					phi_0_k = float( aux[ 1 ] )
				if( aux[ 0 ] == 'phi_0_theta' ):
					phi_0_theta = float( aux[ 1 ] )
				if( aux[ 0 ] == 'dist_input_ws' ):
					dist_input_ws = int( aux[ 1 ] )
				if( aux[ 0 ] == 'ws' ):
					ws = float( aux[ 1 ] )
				if( aux[ 0 ] == 'var_ws' ):
					var_ws = float( aux[ 1 ] )
				if( aux[ 0 ] == 'ws_k' ):
					ws_k = float( aux[ 1 ] )
				if( aux[ 0 ] == 'ws_theta' ):
					ws_theta = float( aux[ 1 ] )
				if( aux[ 0 ] == 'dist_input_Fr' ):
					dist_input_Fr = int( aux[ 1 ] )
				if( aux[ 0 ] == 'Fr' ):
					Fr = float( aux[ 1 ] )
				if( aux[ 0 ] == 'var_Fr' ):
					var_Fr = float( aux[ 1 ] )
				if( aux[ 0 ] == 'Fr_k' ):
					Fr_k = float( aux[ 1 ] )
				if( aux[ 0 ] == 'Fr_theta' ):
					Fr_theta = float( aux[ 1 ] )
				if( aux[ 0 ] == 'dist_input_rho_p' ):
					dist_input_rho_p = int( aux[ 1 ] )
				if( aux[ 0 ] == 'rho_p' ):
					rho_p = float( aux[ 1 ] )
				if( aux[ 0 ] == 'var_rho_p' ):
					var_rho_p = float( aux[ 1 ] )
				if( aux[ 0 ] == 'rho_p_k' ):
					rho_p_k = float( aux[ 1 ] )
				if( aux[ 0 ] == 'rho_p_theta' ):
					rho_p_theta = float( aux[ 1 ] )
				if( aux[ 0 ] == 'dist_input_rho_gas' ):
					dist_input_rho_gas = int( aux[ 1 ] )
				if( aux[ 0 ] == 'rho_gas' ):
					rho_gas = float( aux[ 1 ] )
				if( aux[ 0 ] == 'var_rho_gas' ):
					var_rho_gas = float( aux[ 1 ] )
				if( aux[ 0 ] == 'rho_gas_k' ):
					rho_gas_k = float( aux[ 1 ] )
				if( aux[ 0 ] == 'rho_gas_theta' ):
					rho_gas_theta = float( aux[ 1 ] )
				if( aux[ 0 ] == 'input_file_cal' ):
					input_file_cal = aux[ 1 ]
					input_file_cal = input_file_cal.replace( "'" , "" )
				if( aux[ 0 ] == 'calibration_type' ):
					calibration_type = int( aux[ 1 ] )
				if( aux[ 0 ] == 'dist_distance_calibration' ):
					dist_distance_calibration = int( aux[ 1 ] )
				if( aux[ 0 ] == 'distance_calibration' ):
					distance_calibration = float( aux[ 1 ] )
				if( aux[ 0 ] == 'var_distance_calibration' ):
					var_distance_calibration = float( aux[ 1 ] )
				if( aux[ 0 ] == 'distance_calibration_k' ):
					distance_calibration_k = float( aux[ 1 ] )
				if( aux[ 0 ] == 'distance_calibration_theta' ):
					distance_calibration_theta = float( aux[ 1 ] )
				if( aux[ 0 ] == 'file_cumulative_distance' ):
					file_cumulative_distance = aux[ 1 ]
					file_cumulative_distance = file_cumulative_distance.replace( "'" , "" )
				if( aux[ 0 ] == 'dist_area_calibration' ):
					dist_area_calibration = int( aux[ 1 ] )
				if( aux[ 0 ] == 'area_calibration' ):
					area_calibration = float( aux[ 1 ] )
				if( aux[ 0 ] == 'var_area_calibration' ):
					var_area_calibration = float( aux[ 1 ] )
				if( aux[ 0 ] == 'area_calibration_k' ):
					area_calibration_k = float( aux[ 1 ] )
				if( aux[ 0 ] == 'area_calibration_theta' ):
					area_calibration_theta = float( aux[ 1 ] )
				if( aux[ 0 ] == 'file_cumulative_area' ):
					file_cumulative_area = aux[ 1 ]
					file_cumulative_area = file_cumulative_area.replace( "'" , "" )
				if( aux[ 0 ] == 'max_levels' ):
					max_levels = int( aux[ 1 ] )
				if( aux[ 0 ] == 'N' ):
					N = int( aux[ 1 ] )
				if( aux[ 0 ] == 'save_data' ):
					save_data = int( aux[ 1 ] )
				if( aux[ 0 ] == 'redist_volume' ):
					redist_volume = int( aux[ 1 ] )
				if( aux[ 0 ] == 'plot_flag' ):
					plot_flag = int( aux[ 1 ] )
				if( aux[ 0 ] == 'sea_flag' ):
					sea_flag = int( aux[ 1 ] )

	if( ( run_name == '' ) or not ( type_sim in [ 1 , 2 ] ) or not ( source_dem in [ 1 , 2 , 3 ] ) or not ( max_levels > 0 ) or not ( save_data in [ 0 , 1 ] ) or not ( redist_volume in [ 1 , 2 , 3 , 4 ] ) and not ( plot_flag in [ 0 , 1 ] ) and not ( sea_flag in [ 0 , 1 ] ) ):
		print( 'Problems with input parameters.' )
		sys.exit( 0 )
	if( source_dem == 1 ):
		if( np.isnan( lon1 ) or np.isnan( lon2 ) or np.isnan( lat1 ) or np.isnan( lat2 ) ):
			print( 'Problems with input parameters. Map limits (lon1, lon2, lat1, lat2) must be defined.' )
			sys.exit( 0 )
	else:
		if( topography_file == '' ):
			print( 'Problems with input parameters. Input topography file must be defined.' )
			sys.exit( 0 )
	if( type_sim == 1 ):
		if( not vent_type in [ 1 , 2 , 3 , 4 ] ):
			print( 'Problems with input parameters. Vent type must be defined properly.' )
			sys.exit( 0 )
		if( vent_type in [ 1 , 2 , 3 ] and np.isnan( var_cen ) ):
			print( 'Problems with input parameters. Variable var_cen must be defined.' )
			sys.exit( 0 )
		if( vent_type in [ 1 , 2 , 3 ] and not dist_input_cen in [ 1 , 2 ] ):
			print( 'Problems with input parameters. Variable dist_input_cen must be defined properly.' )
			sys.exit( 0 )
		if( vent_type == 2 ):
			if( np.isnan( azimuth_lin ) or np.isnan( length_lin ) ):
				print( 'Problems with input parameters. Variables (azimuth_lin, length_lin) must be defined properly.' )
				sys.exit( 0 )
		if( vent_type == 3 ):
			if( np.isnan( radius_rad ) or np.isnan( ang1_rad ) or np.isnan( ang2_rad ) ):
				print( 'Problems with input parameters. Variables (radius_rad, ang1_rad, ang2_rad) must be defined properly.' )
				sys.exit( 0 )
		if( vent_type == 4 ):
			if( input_file_vent == '' ):
				print( 'Problems with input parameters. Variable input_file_vent must be defined properly.' )
				sys.exit( 0 )
		if( not type_input in [ 1 , 2 , 3 ] ):
			print( 'Problems with input parameters. Variable type_input must be defined properly.' )
			sys.exit( 0 )
		if( type_input == 1 and ( not dist_input_volume in [ 1 , 2 , 3 , 4 ] or not dist_input_ws in [ 1 , 2 , 3 , 4 ] or not dist_input_phi_0 in [ 1 , 2 , 3 , 4 ] or not dist_input_Fr in [ 1 , 2 , 3 , 4 ] or not dist_input_rho_p in [ 1 , 2 , 3 , 4 ] or not dist_input_rho_gas in [ 1 , 2 , 3 , 4 ] ) ):
			print( 'Problems with input parameters. Variables (dist_input_volume, dist_input_phi_0, dist_input_ws, dist_input_Fr, dist_input_rho_p, dist_input_rho_gas) must be defined properly.' )
			sys.exit( 0 )
		if( type_input in [ 2 , 3 ] ):
			if( input_file_cal == '' ):
				print( 'Problems with input parameters. Variable input_file_cal must be defined.' )
				sys.exit( 0 )
			if( type_input == 3 ):
				if( not calibration_type in [ 1 , 2 , 3 , 4 , 5 , 6 , 7 ] ):
					print( 'Problems with input parameters. Variable calibration_type must be defined properly.' )
					sys.exit( 0 )
				if( calibration_type in [ 5 , 6 ] ):
					if( not dist_distance_calibration in [ 1 , 2 , 3 , 4 , 5 ] ):
						print( 'Problems with input parameters. Variable dist_distance_calibration must be defined properly.' )
						sys.exit( 0 )
					if( dist_distance_calibration in [ 1 , 2 , 4 ] and ( np.isnan( distance_calibration ) or np.isnan( var_distance_calibration ) ) ):
						print( 'Problems with input parameters. Variables (distance_calibration, var_distance_calibration) must be defined.' )
						sys.exit( 0 )
					if( dist_distance_calibration == 3 and ( np.isnan( distance_calibration_k ) or np.isnan( distance_calibration_theta ) ) ):
						print( 'Problems with input parameters. Variables (distance_calibration_k, distance_calibration_theta) must be defined.' )
						sys.exit( 0 )
					if( dist_distance_calibration == 5 and file_cumulative_distance == '' ):
						print( 'Problems with input parameters. Variable file_cumulative_distance must be defined.' )
						sys.exit( 0 )
				if( calibration_type == 7 ):
					if( not dist_area_calibration in [ 1 , 2 , 3 , 4 , 5 ] ):
						print( 'Problems with input parameters. Variable dist_area_calibration must be defined properly.' )
						sys.exit( 0 )
					if( dist_area_calibration in [ 1 , 2 , 4 ] and ( np.isnan( area_calibration ) or np.isnan( var_area_calibration ) ) ):
						print( 'Problems with input parameters. Variables (area_calibration, var_area_calibration) must be defined.' )
						sys.exit( 0 )
					if( dist_area_calibration == 3 and ( np.isnan( area_calibration_k ) or np.isnan( area_calibration_theta ) ) ):
						print( 'Problems with input parameters. Variables (area_calibration_k, area_calibration_theta) must be defined.' )
						sys.exit( 0 )
					if( dist_area_calibration == 5 and file_cumulative_area == '' ):
						print( 'Problems with input parameters. Variable file_cumulative_area must be defined.' )
						sys.exit( 0 )
	else:
		vent_type = 1
		var_cen = 0.0
		dist_input_cen = 2
		type_input = 1
		dist_input_volume = 2
		dist_input_phi_0 = 2
		dist_input_ws = 2
		dist_input_Fr = 2
		dist_input_rho_p = 2
		dist_input_rho_gas = 2
		var_ws = 0
		var_Fr = 0
		var_rho_gas = 0
		var_rho_p = 0
		if( np.isnan( ang_cal ) or np.isnan( ang_cal_range ) ):
			ang_cal = 0.0
			ang_cal_range = 360.0
		if( var_volume == 0.0 or var_phi_0 == 0.0 ):
			print( 'Problems with input parameters. Variabilities of volume and phi_0 (var_volume, var_phi_0) must be higher than zero.' )
			sys.exit( 0 )
	if( source_dem in [ 1 , 3 ] and vent_type in [ 1 , 2 , 3 ] ):
		if( np.isnan( lon_cen ) or np.isnan( lat_cen ) ):
			print( 'Problems with input parameters. Collapse position (lon_cen, lat_cen) must be defined.' )
			sys.exit( 0 )
	if( source_dem == 2 and vent_type in [ 1 , 2 , 3 ] ):
		if( np.isnan( east_cen ) or np.isnan( north_cen ) ):
			print( 'Problems with input parameters. Collapse position (east_cen, north_cen) must be defined.' )
			sys.exit( 0 )
	if( type_input == 1 ):
		if( dist_input_volume in [ 1 , 2 , 4 ] ):
			if( np.isnan( volume ) or np.isnan( var_volume ) ):
				print( 'Problems with input parameters. Input parameters (volume, var_volume) must be defined.' )
				sys.exit( 0 )
		else:
			if( np.isnan( volume_k ) or np.isnan( volume_theta ) ):
				print( 'Problems with input parameters. Input parameters (volume_k, volume_theta) must be defined.' )
				sys.exit( 0 )
		if( dist_input_phi_0 in [ 1 , 2 , 4 ] ):
			if( np.isnan( phi_0 ) or np.isnan( var_phi_0 ) ):
				print( 'Problems with input parameters. Input parameters (phi_0, var_phi_0) must be defined.' )
				sys.exit( 0 )
		else:
			if( np.isnan( phi_0_k ) or np.isnan( phi_0_theta ) ):
				print( 'Problems with input parameters. Input parameters (phi_0_k, phi_0_theta) must be defined.' )
				sys.exit( 0 )
		if( dist_input_ws in [ 1 , 2 , 4 ] ):
			if( np.isnan( ws ) or np.isnan( var_ws ) ):
				print( 'Problems with input parameters. Input parameters (ws, var_ws) must be defined.' )
				sys.exit( 0 )
		else:
			if( np.isnan( ws_k ) or np.isnan( ws_theta ) ):
				print( 'Problems with input parameters. Input parameters (ws_k, ws_theta) must be defined.' )
				sys.exit( 0 )
		if( dist_input_Fr in [ 1 , 2 , 4 ] ):
			if( np.isnan( Fr ) or np.isnan( var_Fr ) ):
				print( 'Problems with input parameters. Input parameters (Fr, var_Fr) must be defined.' )
				sys.exit( 0 )
		else:
			if( np.isnan( Fr_k ) or np.isnan( Fr_theta ) ):
				print( 'Problems with input parameters. Input parameters (Fr_k, Fr_theta) must be defined.' )
				sys.exit( 0 )
		if( dist_input_rho_p in [ 1 , 2 , 4 ] ):
			if( np.isnan( rho_p ) or np.isnan( var_rho_p ) ):
				print( 'Problems with input parameters. Input parameters (rho_p, var_rho_p) must be defined.' )
				sys.exit( 0 )
		else:
			if( np.isnan( rho_p_k ) or np.isnan( rho_p_theta ) ):
				print( 'Problems with input parameters. Input parameters (rho_p_k, rho_p_theta) must be defined.' )
				sys.exit( 0 )
		if( dist_input_rho_gas in [ 1 , 2 , 4 ] ):
			if( np.isnan( rho_gas ) or np.isnan( var_rho_gas ) ):
				print( 'Problems with input parameters. Input parameters (rho_gas, var_rho_gas) must be defined.' )
				sys.exit( 0 )
		else:
			if( np.isnan( rho_gas_k ) or np.isnan( rho_gas_theta ) ):
				print( 'Problems with input parameters. Input parameters (rho_gas_k, rho_gas_theta) must be defined.' )
				sys.exit( 0 )
	if( type_input in [ 1 , 3 ] ):
		if( vent_type in [ 1 , 2 , 3 ] and np.isnan( N ) ):
			print( 'Problems with input parameters. Input parameter N must be defined.' )
			sys.exit( 0 )
	try:
		os.mkdir( 'Results' )
	except:
		pass
	try:
		os.mkdir( 'Results/' + run_name )
	except:
		pass
	shutil.copyfile( 'input_data.py' , 'Results/' + run_name + '/input_data.py' )

	return [ current_path , run_name , type_sim , source_dem , topography_file , comparison_polygon , ang_cal , ang_cal_range , lon1 , lon2 , lat1 , lat2 , g , vent_type , lon_cen , lat_cen , east_cen , north_cen , azimuth_lin , length_lin , radius_rad , ang1_rad , ang2_rad , var_cen , dist_input_cen , input_file_vent , type_input , dist_input_volume , volume , var_volume , volume_k , volume_theta , dist_input_phi_0 , phi_0 , var_phi_0 , phi_0_k , phi_0_theta , dist_input_ws , ws , var_ws , ws_k , ws_theta , dist_input_Fr , Fr , var_Fr , Fr_k , Fr_theta , dist_input_rho_p , rho_p , var_rho_p , rho_p_k , rho_p_theta , dist_input_rho_gas , rho_gas , var_rho_gas , rho_gas_k , rho_gas_theta , input_file_cal , calibration_type , dist_distance_calibration , distance_calibration , var_distance_calibration , distance_calibration_k , distance_calibration_theta , file_cumulative_distance , dist_area_calibration , area_calibration , var_area_calibration , area_calibration_k , area_calibration_theta , file_cumulative_area , max_levels , N , save_data , redist_volume , plot_flag , sea_flag ]

def import_map( current_path , run_name , lon1 , lon2 , lat1 , lat2 , plot_flag , sea_flag ):

	aux_lon = np.array( [ lon1 , lon2 ] )
	aux_lat = np.array( [ lat1 , lat2 ] )
	lon1 = min( aux_lon )
	lon2 = max( aux_lon )
	lat1 = min( aux_lat )
	lat2 = max( aux_lat )
	if( plot_flag + sea_flag > 0 ):
		file_txt = open( 'Cities.txt' )
		line = file_txt.readlines()
		file_txt.close()
		for population in range( 10000 , 10000000 , 10000 ):
			Cities = []
			for i in range( 1 , len( line ) ):
				aux = line[ i ].split( ',' )
				pop = float( aux[ 4 ] )
				lat_dat = float( aux[ 5 ] )
				lon_dat = float( aux[ 6 ] )
				if( lon_dat > lon1 and lon_dat < lon2 and lat_dat > lat1 and lat_dat < lat2 and pop > population ):
					Cities.append( [ lon_dat , lat_dat , aux[ 2 ] ] )
			if( len( Cities ) <= 5 ):
				break
	else:
		Cities = []
	elevation.clip( bounds = ( lon1 , lat1 , lon2 , lat2 ) , output = current_path + '/' + run_name + '.tif' )
	fp = run_name + '.tif'
	image = tifffile.imread( fp )
	elevation.clean()
	Topography = np.array( image )
	if( plot_flag + sea_flag > 0 ):
		Topography_Sea = Topography + 0.0
		Topography_Sea[ Topography_Sea[ : , : ] <= 0 ] = -1.0 * np.sqrt( -1.0 * Topography_Sea[ Topography_Sea[ : , : ] <= 0 ] )
		Topography_Sea[ Topography_Sea[ : , : ] > 0 ] = np.nan
		Topography_Sea = Topography_Sea * -1.0
	else:
		Topography_Sea = np.nan
	Topography = ( Topography + abs( Topography ) ) / 2.0
	cells_lon = Topography.shape[ 1 ]
	cells_lat = Topography.shape[ 0 ]

	return [ lon1 , lon2 , lat1 , lat2 , Cities , Topography , Topography_Sea , cells_lon , cells_lat ]

def read_map_utm( current_path , topography_file , plot_flag , sea_flag ):

	try:
		file_txt = open( topography_file )
	except:
		print( topography_file +' not found in ' + str( current_path ) + '.' )
		sys.exit( 0 )
	line = file_txt.readlines()
	file_txt.close()
	[ n_north , n_east , cellsize , east_cor , north_cor , nodata_value ] = [ np.nan , np.nan , np.nan , np.nan , np.nan , np.nan ]
	for i in range( 0 , 10 ):
		aux = line[ i ].split()
		if( aux[ 0 ] == 'nrows' ):
			n_north = int( aux[ 1 ] )
		if( aux[ 0 ] == 'ncols' ):
			n_east = int( aux[ 1 ] )
		if( aux[ 0 ] == 'cellsize' ):
			cellsize = float( aux[ 1 ] )
		if( aux[ 0 ] == 'xllcorner' ):
			east_cor = float( aux[ 1 ] )
		if( aux[ 0 ] == 'yllcorner' ):
			north_cor = float( aux[ 1 ] )
		if( aux[ 0 ] == 'NODATA_value' ):
			nodata_value = float( aux[ 1 ] )
		if( len( aux ) >= 10 ):
			indexini = i
			break
	if( np.isnan( n_north ) or np.isnan( n_east ) or np.isnan( cellsize ) or np.isnan( east_cor ) or np.isnan( north_cor ) ):
		print( 'Problems in topography file.' )
		sys.exit( 0 )
	Topography = np.zeros( ( n_north , n_east ) )
	for i in range( indexini , indexini + n_north ):
		aux = line[ i ].split()
		for j in range( 0, n_east ):
			Topography[ i - indexini , j ] = float( aux[ j ] )
	if( not np.isnan( nodata_value ) ):
		aux = np.where( Topography == nodata_value )
		Topography[ np.where( Topography == nodata_value ) ] = np.nan
	if( plot_flag + sea_flag > 0 ):
		Topography_Sea = Topography + 0.0
		Topography_Sea[ Topography_Sea[ : , : ] <= 0 ] = -1.0 * np.sqrt( -1.0 * Topography_Sea[ Topography_Sea[ : , : ] <= 0 ] )
		Topography_Sea[ Topography_Sea[ : , : ] > 0 ] = np.nan
		Topography_Sea = Topography_Sea * -1.0
	else:
		Topography_Sea = np.nan
	Topography = ( Topography + abs( Topography ) ) / 2.0

	return [ Topography , Topography_Sea , n_north , n_east , cellsize , east_cor , north_cor ]

def read_map_deg( current_path , topography_file , plot_flag , sea_flag ):

	try:
 		file_txt = open( topography_file )
	except:
 		print( topography_file + ' not found in ' + str( current_path ) + '.' )
 		sys.exit( 0 )
	line = file_txt.readlines()
	file_txt.close()
	[ lon1 , lon2 , lat1 , lat2 , cells_lon , cells_lat ] = [ np.nan , np.nan , np.nan , np.nan , np.nan , np.nan ]
	for i in range( 0 , 10 ):
		aux = line[ i ].split()
		if( aux[ 0 ] == 'lon1' ):
			lon1 = float( aux[ 1 ] )
		if( aux[ 0 ] == 'lon2' ):
			lon2 = float( aux[ 1 ] )
		if( aux[ 0 ] == 'lat1' ):
			lat1 = float( aux[ 1 ] )
		if( aux[ 0 ] == 'lat2' ):
			lat2 = float( aux[ 1 ] )
		if( aux[ 0 ] == 'cells_lon' ):
			cells_lon = int( aux[ 1 ] )
		if( aux[ 0 ] == 'cells_lat' ):
			cells_lat = int( aux[ 1 ] )
		if( len( aux ) >= 10 ):
			indexini = i
			break
	if( np.isnan( lon1 ) or np.isnan( lon2 ) or np.isnan( lat1 ) or np.isnan( lat2 ) or np.isnan( cells_lon ) or np.isnan( cells_lat ) ):
		print( 'Problems in topography file.' )
		sys.exit( 0 )
	Topography = np.zeros( ( int( np.floor( cells_lat ) ) , int( np.floor( cells_lon ) ) ) , dtype = 'int' )
	for i in range( indexini , indexini + int( np.floor( cells_lat ) ) ):
		aux = line[ ( indexini + ( i - indexini ) ) ].split()
		for j in range( 0 , int( np.floor( cells_lon ) ) ):
			Topography[ i - indexini , j ] = float( aux[ j ] ) 
	if( plot_flag + sea_flag > 0 ):
		Topography_Sea = Topography + 0.0
		Topography_Sea[ Topography_Sea[ : , : ] <= 0 ] = -1.0 * np.sqrt( -1.0 * Topography_Sea[ Topography_Sea[ : , : ] <= 0 ] )
		Topography_Sea[ Topography_Sea[ : , : ] > 0 ] = np.nan
		Topography_Sea = Topography_Sea * -1.0
		Topography = ( Topography + abs( Topography ) ) / 2.0
	else:
		Topography_Sea = np.nan
	file_txt = open( 'Cities.txt' )
	line = file_txt.readlines()
	file_txt.close()
	if( plot_flag + sea_flag > 0 ):
		for population in range( 10000 , 10000000 , 10000 ):
			Cities = []
			for i in range( 1 , len( line ) ):
				aux = line[ i ].split( ',' )
				pop = float( aux[ 4 ] )
				lat_dat = float( aux[ 5 ] )
				lon_dat = float( aux[ 6 ] )
				if( lon_dat > lon1 and lon_dat < lon2 and lat_dat > lat1 and lat_dat < lat2 and pop > population ):
					Cities.append( [ lon_dat , lat_dat , aux[ 2 ] ] )
			if( len( Cities ) <= 5 ):
				break
	else:
		Cities = []
	return [ lon1 , lon2 , lat1 , lat2 , Cities , Topography , Topography_Sea , int( cells_lon ) , int( cells_lat ) ]

def matrix_deg( lon1 , lon2 , lat1 , lat2 , cells_lon , cells_lat ):

	utm1 = utm.from_latlon( lat1 , lon1 )
	utm2 = utm.from_latlon( lat2 , lon2 )
	if( utm1[ 2 ] == utm2[ 2 ] and utm1[ 3 ] == utm2[ 3 ] ):
		distance_lon = abs( utm2[ 0 ] - utm1[ 0 ] )
		distance_lat = abs( utm2[ 1 ] - utm1[ 1 ] )
	else:
		distance_lon = distance_two_points( lat1 , lat1 , lon1 , lon2 )
		distance_lat = distance_two_points( lat1 , lat2 , lon1 , lon1 )
	utm_save = utm.from_latlon( min( lat1 , lat2 ) , min( lon1 , lon2 ) )
	step_lon_m = distance_lon / ( cells_lon - 1 )
	step_lat_m = distance_lat / ( cells_lat - 1 )
	matrix_lon = np.zeros( ( cells_lat , cells_lon ) )
	matrix_lat = np.zeros( ( cells_lat , cells_lon ) )
	for i in range( 0 , cells_lon ): 
		matrix_lon[ : , i ] = lon1 + ( lon2 - lon1 ) * ( i ) / ( cells_lon - 1 )
	for j in range( 0 , cells_lat ):
		matrix_lat[ j , : ] = lat1 + ( lat2 - lat1 ) * ( cells_lat - 1 - j ) / ( cells_lat - 1 )
	step_lon_deg = ( lon2 - lon1 ) / ( cells_lon - 1 )
	step_lat_deg = ( lat2 - lat1 ) / ( cells_lat - 1 )

	return [ matrix_lon , matrix_lat , step_lon_m , step_lat_m , step_lon_deg , step_lat_deg , utm_save ]

def matrix_utm( n_north , n_east , cellsize , east_cor , north_cor ):

	matrix_north = np.zeros( ( n_north , n_east ) )
	matrix_east = np.zeros( ( n_north , n_east ) )
	for i in range( 0 , n_east ):
		matrix_east[ : , i ] = ( east_cor + cellsize * i )
	for j in range( 0 , n_north ):
		matrix_north[ j , : ] = ( north_cor + cellsize * j )
	matrix_north = matrix_north[ range( len( matrix_north[ : , 0 ] ) -1 , -1 , -1 ) , : ]
	utm_save = [ east_cor , north_cor ]

	return [ matrix_north , matrix_east , utm_save ]

def create_inputs( type_sim , type_input , dist_input_volume , dist_input_phi_0 , dist_input_ws , dist_input_Fr , dist_input_rho_p , dist_input_rho_gas , input_file_cal , volume , var_volume , volume_k , volume_theta , phi_0 , var_phi_0 , phi_0_k , phi_0_theta , ws , var_ws , ws_k , ws_theta , Fr , var_Fr , Fr_k , Fr_theta , rho_p , var_rho_p , rho_p_k , rho_p_theta , rho_gas , var_rho_gas , rho_gas_k , rho_gas_theta , calibration_type , dist_distance_calibration , distance_calibration , var_distance_calibration , distance_calibration_k , distance_calibration_theta , file_cumulative_distance , dist_area_calibration , area_calibration , var_area_calibration , area_calibration_k , area_calibration_theta , file_cumulative_area , N , bol_friendly ):

	variable_vector = np.nan
	limits_calib = np.nan
	Probability_Save = np.nan
	if( type_sim == 2 ):
		N = int( np.sqrt( N ) )
	if( type_input == 2 ):
		file_data = np.loadtxt( input_file_cal )
		N = np.minimum( N , len( file_data[ : ] ) )
		volume_vector = file_data[ range( 0 , N ) , 0 ]
		phi_0_vector = file_data[ range( 0 , N ) , 1 ]
		ws_vector = file_data[ range( 0 , N ) , 2 ]
		Fr_vector = file_data[ range( 0 , N ) , 3 ]
		rho_p_vector = file_data[ range( 0 , N ) , 4 ]
		rho_gas_vector = file_data[ range( 0 , N ) , 5 ]
	elif( type_input == 3 ):
		file_data = np.loadtxt( input_file_cal , skiprows = 5 )
		file_txt = open( input_file_cal )
		line = file_txt.readlines()
		file_txt.close()
		resolution = float( line[ 0 ] )
		ws_vector = np.ones( N ) * float( line[ 1 ] )
		Fr_vector = np.ones( N ) * float( line[ 2 ] )
		rho_p_vector = np.ones( N ) * float( line[ 3 ] )
		rho_gas_vector = np.ones( N ) * float( line[ 4 ] )
		number_steps = int( np.sqrt( len( file_data[ : , 0 ] ) ) )
		xi_sim = np.linspace( np.log10( np.min( file_data[ : , 0 ] ) ) , np.log10( np.max( file_data[ : , 0 ] ) ) , number_steps )
		yi_sim = np.linspace( np.min( file_data[ : , 1 ] ) , np.max( file_data[ : , 1 ] ) , number_steps )
		number_steps_dense = 100
		stepx = ( np.log10( np.max( file_data[ : , 0 ] ) ) - np.log10( np.min( file_data[ : , 0 ] ) ) ) / number_steps_dense
		stepy = ( np.max( file_data[ : , 1 ] ) - np.min( file_data[ : , 1 ] ) ) / number_steps_dense
		limits_calib = [ np.log10( np.min( file_data[ : , 0 ] ) ) , np.log10( np.max( file_data[ : , 0 ] ) ) , np.min( file_data[ : , 1 ] ) , np.max( file_data[ : , 1 ] ) ]
		xi = np.linspace( np.log10( np.min( file_data[ : , 0 ] ) ) + stepx / 2.0 , np.log10( np.max( file_data[ : , 0 ] ) ) - stepx / 2.0 , number_steps_dense )
		yi = np.linspace( np.min( file_data[ : , 1 ] ) + stepy / 2.0 , np.max( file_data[ : , 1 ] ) - stepy / 2.0 , number_steps_dense )
		[ Xi , Yi ] = np.meshgrid( xi , yi )
		Xi_reshaped = np.reshape( Xi , ( number_steps_dense * number_steps_dense , 1 ) )
		Yi_reshaped = np.reshape( Yi , ( number_steps_dense * number_steps_dense , 1 ) )
		if( calibration_type in [ 1 , 2 , 3 , 4 ] ):
			if( np.isnan( file_data[ : , 2 ] ).any() ):
				print( 'Calibration data is only associated with distance- and area-based calibrations.' )
				if( bol_friendly == 0 ):
					sys.exit( 0 )
				else:
					return [ np.zeros( ( 0 ) ) , np.zeros( ( 0 ) ) , N , variable_vector , limits_calib , Probability_Save ]
			if( calibration_type == 1 ):
				z = np.reshape( file_data[ : , 2 ] , ( number_steps , number_steps ) )
				interpolator = interpolate.interp2d( xi_sim , yi_sim , z , kind = 'cubic' )
				zi_reshaped = np.reshape( interpolator( xi , yi ) , ( number_steps_dense * number_steps_dense , 1 ) )
			elif( calibration_type == 2 ):
				z = np.reshape( file_data[ : , 3 ] , ( number_steps , number_steps ) )
				interpolator = interpolate.interp2d( xi_sim , yi_sim , z , kind = 'cubic' )
				zi_reshaped = np.reshape( interpolator( xi , yi ) , ( number_steps_dense * number_steps_dense , 1 ) )
				zi_reshaped = 1.0 / ( zi_reshaped + resolution )
			elif( calibration_type == 3 ):
				z = np.reshape( file_data[ : , 4 ] , ( number_steps , number_steps ) )
				interpolator = interpolate.interp2d( xi_sim , yi_sim , z , kind = 'cubic' )
				zi_reshaped = np.reshape( interpolator( xi , yi ) , ( number_steps_dense * number_steps_dense , 1 ) )
				zi_reshaped = 1.0 / ( zi_reshaped + resolution )
			elif( calibration_type == 4 ):
				z = np.reshape( file_data[ : , 6 ] , ( number_steps , number_steps ) )
				interpolator = interpolate.interp2d( xi_sim , yi_sim , z , kind = 'cubic' )
				zi_reshaped = np.reshape( interpolator( xi , yi ) , ( number_steps_dense * number_steps_dense , 1 ) )
			Probability_Save = gaussian_filter( np.reshape( zi_reshaped * zi_reshaped / sum( zi_reshaped * zi_reshaped ) , ( number_steps_dense , number_steps_dense ) ) , 1 )
			Probability = np.cumsum( np.reshape( Probability_Save , ( number_steps_dense * number_steps_dense , 1 ) ) / np.sum( np.reshape( Probability_Save , ( number_steps_dense * number_steps_dense , 1 ) ) ) )
			sampling = np.random.uniform( 0.0 , 1.0 , N )
			sampling_volume = np.random.uniform( - 0.5 , 0.5 , N )
			sampling_phi_0 = np.random.uniform( - 0.5 , 0.5 , N )
			volume_vector = np.ones( ( N ) )
			phi_0_vector = np.ones( ( N ) )
			for i in range( N ):
				indexes = np.min( np.where( Probability > sampling[ i ] )[ 0 ] )
				volume_vector[ i ] = np.power( 10.0 , ( Xi_reshaped[ indexes , 0 ] ) + sampling_volume[ i ] * stepx )
				phi_0_vector[ i ] = ( Yi_reshaped[ indexes , 0 ] ) + sampling_phi_0[ i ] * stepy
		else:
			number_steps_var = 5000
			number_steps_var_plot = 3000
			variable_vector = np.zeros( ( number_steps_var_plot , 2 ) )
			if( calibration_type in [ 5 , 6 ] ):
				if( calibration_type == 5 ):
					max_val_cal = np.max( file_data[ : , 5 ] )
					min_val_cal = np.min( file_data[ : , 5 ] )
					z = np.reshape( file_data[ : , 5 ] , ( number_steps , number_steps ) )
				else:
					max_val_cal = np.max( file_data[ : , 7 ] )
					min_val_cal = np.min( file_data[ : , 7 ] )
					z = np.reshape( file_data[ : , 7 ] , ( number_steps , number_steps ) )
				interpolator = interpolate.interp2d( xi_sim , yi_sim , z , kind = 'cubic' )
				zi_reshaped = np.reshape( interpolator( xi , yi ) , ( number_steps_dense * number_steps_dense , 1 ) )
				if( dist_distance_calibration == 1 ):
					mincum = norm.cdf( min_val_cal , distance_calibration , var_distance_calibration )
					maxcum = norm.cdf( max_val_cal , distance_calibration , var_distance_calibration )
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					variable_vector_used = norm.ppf( vector_p , distance_calibration , var_distance_calibration )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ] = norm.pdf( variable_vector[ : , 0 ] , distance_calibration , var_distance_calibration )
				elif( dist_distance_calibration == 2 ):
					mincum = uniform.cdf( min_val_cal , distance_calibration - var_distance_calibration , 2 * var_distance_calibration )
					maxcum = uniform.cdf( np.max( file_data[ : , 5 ] ) , distance_calibration - var_distance_calibration , 2 * var_distance_calibration )
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					variable_vector_used = uniform.ppf( vector_p , distance_calibration - var_distance_calibration , 2 * var_distance_calibration )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ] = uniform.pdf( variable_vector[ : , 0 ] , distance_calibration - var_distance_calibration , 2 * var_distance_calibration )
				elif( dist_distance_calibration == 3 ):
					mincum = gamma.cdf( min_val_cal , distance_calibration_k , 0 , distance_calibration_theta )
					maxcum = gamma.cdf( np.max( file_data[ : , 5 ] ) , distance_calibration_k , 0 , distance_calibration_theta )
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					variable_vector_used = gamma.ppf( vector_p , distance_calibration_k , 0 , distance_calibration_theta )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ] = gamma.pdf( variable_vector[ : , 0 ] , distance_calibration_k , 0 , distance_calibration_theta )
				elif( dist_distance_calibration == 4 ):
					parameter_sigma = np.sqrt( np.log( var_distance_calibration * var_distance_calibration / distance_calibration / distance_calibration + 1.0 ) )
					parameter_mu = np.log( distance_calibration * distance_calibration / np.sqrt( distance_calibration * distance_calibration + var_distance_calibration * var_distance_calibration ) )
					mincum = lognorm.cdf( min_val_cal , parameter_sigma , 0 , np.exp( parameter_mu ) )
					maxcum = lognorm.cdf( max_val_cal , parameter_sigma , 0 , np.exp( parameter_mu ) )
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					variable_vector_used = lognorm.ppf( vector_p , parameter_sigma , 0 , np.exp( parameter_mu ) )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ] = lognorm.pdf( variable_vector[ : , 0 ] , parameter_sigma , 0 , np.exp( parameter_mu ) )
				else:
					file_cumulative = np.loadtxt( file_cumulative_distance )
					mincum = file_cumulative[ 0 ][ 1 ]
					maxcum = file_cumulative[ len( file_cumulative ) - 1 ][ 1 ]
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					interpolator = interpolate.interp1d( file_cumulative[ : , 1 ] , file_cumulative[ : , 0 ] )
					interpolator_inverse = interpolate.interp1d( file_cumulative[ 1 : len( file_cumulative ) - 2 , 0 ] , file_cumulative[ 2 : len( file_cumulative ) - 1 , 1 ] - file_cumulative[ 0 : len( file_cumulative ) - 3 , 1 ] , fill_value = "extrapolate" )
					variable_vector_used = interpolator( vector_p )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ] = interpolator_inverse( variable_vector[ : , 0 ] )
			else:
				resolution = resolution * resolution / 1000000.00
				max_val_cal = np.max( file_data[ : , 8 ] )
				min_val_cal = np.min( file_data[ : , 8 ] )
				z = np.reshape( file_data[ : , 8 ] , ( number_steps , number_steps ) )
				interpolator = interpolate.interp2d( xi_sim , yi_sim , z , kind = 'cubic' )
				zi_reshaped = np.reshape( interpolator( xi , yi ) , ( number_steps_dense * number_steps_dense , 1 ) )
				if( dist_area_calibration == 1 ):
					mincum = norm.cdf( min_val_cal , area_calibration , var_area_calibration )
					maxcum = norm.cdf( max_val_cal , area_calibration , var_area_calibration )
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					variable_vector_used = norm.ppf( vector_p , area_calibration , var_area_calibration )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ] = norm.pdf( variable_vector[ : , 0 ] , area_calibration , var_area_calibration )
				elif( dist_area_calibration == 2 ):
					mincum = uniform.cdf( min_val_cal , area_calibration - var_area_calibration , 2 * var_area_calibration )
					maxcum = uniform.cdf( np.max( file_data[ : , 5 ] ) , area_calibration - var_area_calibration , 2 * var_area_calibration )
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					variable_vector_used = uniform.ppf( vector_p , area_calibration - var_area_calibration , 2 * var_area_calibration )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ] = uniform.pdf( variable_vector[ : , 0 ] , area_calibration - var_area_calibration , 2 * var_area_calibration )
				elif( dist_area_calibration == 3 ):
					mincum = gamma.cdf( min_val_cal , area_calibration_k , 0 , area_calibration_theta )
					maxcum = gamma.cdf( np.max( file_data[ : , 5 ] ) , area_calibration_k , 0 , area_calibration_theta )
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					variable_vector_used = gamma.ppf( vector_p , area_calibration_k , 0 , area_calibration_theta )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ]= gamma.pdf( variable_vector[ : , 0 ] , area_calibration_k , 0 , area_calibration_theta )
				elif( dist_area_calibration == 4 ):
					parameter_sigma = np.sqrt( np.log( var_area_calibration * var_area_calibration / area_calibration / area_calibration + 1.0 ) )
					parameter_mu = np.log( area_calibration * area_calibration / np.sqrt( area_calibration * area_calibration + var_area_calibration * var_area_calibration ) )
					mincum = lognorm.cdf( min_val_cal , parameter_sigma , 0 , np.exp( parameter_mu ) )
					maxcum = lognorm.cdf( max_val_cal , parameter_sigma , 0 , np.exp( parameter_mu ) )
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					variable_vector_used = lognorm.ppf( vector_p , parameter_sigma , 0 , np.exp( parameter_mu ) )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ] = lognorm.pdf( variable_vector[ : , 0 ] , parameter_sigma , 0 , np.exp( parameter_mu ) )
				else:
					file_cumulative = np.loadtxt( file_cumulative_area )
					mincum = file_cumulative[ 0 ][ 1 ]
					maxcum = file_cumulative[ len( file_cumulative ) - 1 ][ 1 ]
					vector_p = np.arange( mincum + ( maxcum - mincum ) / ( 2 * number_steps_var ) , maxcum , ( maxcum - mincum ) / ( number_steps_var ) )
					interpolator = interpolate.interp1d( file_cumulative[ : , 1 ] , file_cumulative[ : , 0 ] )
					interpolator_inverse = interpolate.interp1d( file_cumulative[ 1 : len( file_cumulative ) - 2 , 0 ] , file_cumulative[ 2 : len( file_cumulative ) - 1 , 1 ] - file_cumulative[ 0 : len( file_cumulative ) - 3 , 1 ] , fill_value = "extrapolate" )
					variable_vector_used = interpolator( vector_p )
					variable_vector[ : , 0 ] = np.linspace( np.minimum( 0.0 , np.min( variable_vector_used ) ) , np.max( variable_vector_used ) , number_steps_var_plot )
					variable_vector[ : , 1 ] = interpolator_inverse( variable_vector[ : , 0 ] )
			divisor_int = np.zeros( vector_p.shape )
			for ind_int in range( len( divisor_int ) ):
				divisor_int[ ind_int ] = np.sum( np.power( resolution + np.abs( zi_reshaped - variable_vector_used[ ind_int ] ) , -1.0 ) )
			Probability = np.zeros( zi_reshaped.shape )
			for ind_prob in range( len( Probability ) ):
				Probability[ ind_prob ] = np.sum( np.power( resolution + np.abs( zi_reshaped[ ind_prob ] - variable_vector_used ) , - 1.0 ) / divisor_int )
			Probability_Save = gaussian_filter( np.reshape( Probability / np.sum( Probability ) , ( number_steps_dense , number_steps_dense ) ) , 1 )
			Probability = np.cumsum( np.reshape( Probability_Save , ( number_steps_dense * number_steps_dense , 1 ) ) / np.sum( np.reshape( Probability_Save , ( number_steps_dense * number_steps_dense , 1 ) ) ) )
			sampling = np.random.uniform( 0.0 , 1.0 , N )
			sampling_volume = np.random.uniform( - 0.5 , 0.5 , N )
			sampling_phi_0 = np.random.uniform( - 0.5 , 0.5 , N )
			volume_vector = np.ones( ( N ) )
			phi_0_vector = np.ones( ( N ) )
			for i in range( N ):
				indexes = np.min( np.where( Probability > sampling[ i ] )[ 0 ] )
				volume_vector[ i ] = np.power( 10.0 , ( Xi_reshaped[ indexes , 0 ] ) + sampling_volume[ i ] * stepx )
				phi_0_vector[ i ] = ( Yi_reshaped[ indexes , 0 ] ) + sampling_phi_0[ i ] * stepy
	else:
		if( var_volume > 0.0 or dist_input_volume == 3 ):
			if( type_sim == 1 ):
				if( dist_input_volume == 1 ):
					volume_vector = np.random.normal( volume , var_volume , N )
				elif( dist_input_volume == 2 ):
					volume_vector = np.random.uniform( volume - var_volume , volume + var_volume , N )
				elif( dist_input_volume == 3 ):
					volume_vector = np.random.gamma( volume_k , volume_theta , N )
				else:
					volume_vector = np.random.lognormal( np.log( volume * volume / np.sqrt( volume * volume + var_volume * var_volume ) ) , np.log( 1 + var_volume * var_volume / volume / volume ) , N )
			else:
				volume_vector = np.linspace( np.log10( volume - var_volume ) , np.log10( volume + var_volume ) , num = N )
				volume_vector = np.power( 10.0 * np.ones( N ) , volume_vector )
		else:
			volume_vector = np.ones( N ) * volume
		if( var_phi_0 > 0.0 or dist_input_phi_0 == 3 ):
			if( type_sim == 1 ):
				if( dist_input_phi_0 == 1 ):
			 		phi_0_vector = np.random.normal( phi_0 , var_phi_0 , N )
				elif( dist_input_phi_0 == 2 ):
					phi_0_vector = np.random.uniform( phi_0 - var_phi_0 , phi_0 + var_phi_0 , N )
				elif( dist_input_phi_0 == 3 ):
					phi_0_vector = np.random.gamma( phi_0_k , phi_0_theta , N )
				else:
					phi_0_vector = np.random.lognormal( np.log( phi_0 * phi_0 / np.sqrt( phi_0 * phi_0 + var_phi_0 * var_phi_0 ) ) , np.log( 1 + var_phi_0 * var_phi_0 / phi_0 / phi_0 ) , N )
			else:
				phi_0_vector = np.linspace( phi_0 - var_phi_0 , phi_0 + var_phi_0 , num = N )
		else:
			phi_0_vector = np.ones( N ) * phi_0
		if( var_ws > 0.0 or dist_input_ws == 3 ):
			if( type_sim == 1 ):
				if( dist_input_ws == 1 ):
			 		ws_vector = np.random.normal( ws , var_ws , N )
				elif( dist_input_ws == 2 ):
					ws_vector = np.random.uniform( ws - var_ws , ws + var_ws , N )
				elif( dist_input_ws == 3 ):
					ws_vector = np.random.gamma( ws_k , ws_theta , N )
				else:
					ws_vector = np.random.lognormal( np.log( ws * ws / np.sqrt( ws * ws + var_ws * var_ws ) ) , np.log( 1 + var_ws * var_ws / ws / ws ) , N )
			else:
				ws_vector = np.linspace( ws - var_ws , ws + var_ws , num = N )
		else:
			ws_vector = np.ones( N ) * ws
		if( var_Fr > 0.0 or dist_input_Fr == 3 ):
			if( type_sim == 1 ):
				if( dist_input_Fr == 1 ):
			 		Fr_vector = np.random.normal( Fr , var_Fr , N )
				elif( dist_input_Fr == 2 ):
					Fr_vector = np.random.uniform( Fr - var_Fr , Fr + var_Fr , N )
				elif( dist_input_Fr == 3 ):
					Fr_vector = np.random.gamma( Fr_k , Fr_theta , N )
				else:
					Fr_vector = np.random.lognormal( np.log( Fr * Fr / np.sqrt( Fr * Fr + var_Fr * var_Fr ) ) , np.log( 1 + var_Fr * var_Fr / Fr / Fr ) , N )
			else:
				Fr_vector = np.linspace( Fr - var_Fr , Fr + var_Fr , num = N )
		else:
			Fr_vector = np.ones( N ) * Fr
		if( var_rho_p > 0.0 or dist_input_rho_p == 3 ):
			if( type_sim == 1 ):
				if( dist_input_rho_p == 1 ):
			 		rho_p_vector = np.random.normal( rho_p , var_rho_p , N )
				elif( dist_input_rho_p == 2 ):
					rho_p_vector = np.random.uniform( rho_p - var_rho_p , rho_p + var_rho_p , N )
				elif( dist_input_rho_p == 3 ):
					rho_p_vector = np.random.gamma( rho_p_k , rho_p_theta , N )
				else:
					rho_p_vector = np.random.lognormal( np.log( rho_p * rho_p / np.sqrt( rho_p * rho_p + var_rho_p * var_rho_p ) ) , np.log( 1 + var_rho_p * var_rho_p / rho_p / rho_p ) , N )
			else:
				rho_p_vector = np.linspace( rho_p - var_rho_p , rho_p + var_rho_p , num = N )
		else:
			rho_p_vector = np.ones( N ) * rho_p
		if( var_rho_gas > 0.0 or dist_input_rho_gas == 3 ):
			if( type_sim == 1 ):
				if( dist_input_rho_gas == 1 ):
			 		rho_gas_vector = np.random.normal( rho_gas , var_rho_gas , N )
				elif( dist_input_rho_gas == 2 ):
					rho_gas_vector = np.random.uniform( rho_gas - var_rho_gas , rho_gas + var_rho_gas , N )
				elif( dist_input_rho_gas == 3 ):
					rho_gas_vector = np.random.gamma( rho_gas_k , rho_gas_theta , N )
				else:
					rho_gas_vector = np.random.lognormal( np.log( rho_gas * rho_gas / np.sqrt( rho_gas * rho_gas + var_rho_gas * var_rho_gas ) ) , np.log( 1 + var_rho_gas * var_rho_gas / rho_gas / rho_gas ) , N )
			else:
				rho_gas_vector = np.linspace( rho_gas - var_rho_gas , rho_gas + var_rho_gas , num = N )
		else:
			rho_gas_vector = np.ones( N ) * rho_gas
		if( type_sim == 2 ):
			volume_vector_i = volume_vector
			phi_0_vector_i = np.zeros( N * N )
			phi_0_vector_i[ 0 : N ] = phi_0_vector[ 0 ]
			ws_vector_i = ws_vector
			Fr_vector_i = Fr_vector
			rho_p_vector_i = rho_p_vector
			rho_gas_vector_i = rho_gas_vector
			for i in range( 1 , N ):
				volume_vector = np.concatenate( ( volume_vector , volume_vector_i ) )
				phi_0_vector_i[ i * N : ( i + 1 ) * N ] = phi_0_vector[ i ]
				ws_vector = np.concatenate( ( ws_vector , ws_vector_i ) )
				Fr_vector = np.concatenate( ( Fr_vector , Fr_vector_i ) )
				rho_p_vector = np.concatenate( ( rho_p_vector , rho_p_vector_i ) )
				rho_gas_vector = np.concatenate( ( rho_gas_vector , rho_gas_vector_i ) )
			phi_0_vector = phi_0_vector_i
			N = N * N
		else:
			if( var_volume > 0.0 or dist_input_volume == 3 ):
				while True:
					aux_boolean = 0
					for i in range( 0 , N ):
						if( volume_vector[ i ] < 0 ):
							if( dist_input_volume == 1 ):
								volume_vector[ i ] = np.random.normal( volume , var_volume , 1 )
							elif( dist_input_volume == 2 ):
								volume_vector[ i ] = np.random.uniform( volume - var_volume , volume + var_volume , 1 )
							elif( dist_input_volume == 3 ):
								volume_vector[ i ] = np.random.gamma( volume_k , volume_theta , 1 )
							else:
								volume_vector[ i ] = np.random.lognormal( np.log( volume * volume / np.sqrt( volume * volume + var_volume * var_volume ) ) , np.log( 1 + var_volume * var_volume / volume / volume ) , 1 )
							aux_boolean = 1
					if( aux_boolean == 0 ):
						break
			if( var_phi_0 > 0.0 or dist_input_phi_0 == 3 ):
				while True:
					aux_boolean = 0
					for i in range( 0 , N ):
						if( phi_0_vector[ i ] < 0 ):
							if( dist_input_phi_0 == 1 ):
								phi_0_vector[ i ] = np.random.normal( phi_0 , var_phi_0 , 1 )
							elif( dist_input_phi_0 == 2 ):
								phi_0_vector[ i ] = np.random.uniform( phi_0 - var_phi_0 , phi_0 + var_phi_0 , 1 )
							elif( dist_input_phi_0 == 3 ):
								phi_0_vector[ i ] = np.random.gamma( phi_0_k , phi_0_theta , 1 )
							else:
								phi_0_vector[ i ] = np.random.lognormal( np.log( phi_0 * phi_0 / np.sqrt( phi_0 * phi_0 + var_phi_0 * var_phi_0 ) ) , np.log( 1 + var_phi_0 * var_phi_0 / phi_0 / phi_0 ) , 1 )
							aux_boolean = 1
					if( aux_boolean == 0 ):
						break
			if( var_ws > 0.0 or dist_input_ws == 3 ):
				while True:
					aux_boolean = 0
					for i in range( 0 , N ):
						if( ws_vector[ i ] < 0 ):
							if( dist_input_ws == 1 ):
								ws_vector[ i ] = np.random.normal( ws , var_ws , 1 )
							elif( dist_input_ws == 2 ):
								ws_vector[ i ] = np.random.uniform( ws - var_ws , ws + var_ws , 1 )
							elif( dist_input_ws == 3 ):
								ws_vector[ i ] = np.random.gamma( ws_k , ws_theta , 1 )
							else:
								ws_vector[ i ] = np.random.lognormal( np.log( ws * ws / np.sqrt( ws * ws + var_ws * var_ws ) ) , np.log( 1 + var_ws * var_ws / ws / ws ) , 1 )
							aux_boolean = 1
					if( aux_boolean == 0 ):
						break
			if( var_Fr > 0.0 or dist_input_Fr == 3 ):
				while True:
					aux_boolean = 0
					for i in range( 0 , N ):
						if( Fr_vector[ i ] < 0 ):
							if( dist_input_Fr == 1 ):
								Fr_vector[ i ] = np.random.normal( Fr , var_Fr , 1 )
							elif( dist_input_Fr == 2 ):
								Fr_vector[ i ] = np.random.uniform( Fr - var_Fr , Fr + var_Fr , 1 )
							elif( dist_input_Fr == 3 ):
								Fr_vector[ i ] = np.random.gamma( Fr_k , Fr_theta , 1 )
							else:
								Fr_vector[ i ] = np.random.lognormal( np.log( Fr * Fr / np.sqrt( Fr * Fr + var_Fr * var_Fr ) ) , np.log( 1 + var_Fr * var_Fr / Fr / Fr ) , 1 )
							aux_boolean = 1
					if( aux_boolean == 0 ):
						break
			if( var_rho_p > 0.0 or dist_input_rho_p == 3 ):
				while True:
					aux_boolean = 0
					for i in range( 0 , N ):
						if( rho_p_vector[ i ] < 0 ):
							if( dist_input_rho_p == 1 ):
								rho_p_vector[ i ] = np.random.normal( rho_p , var_rho_p , 1 )
							elif( dist_input_rho_p == 2 ):
								rho_p_vector[ i ] = np.random.uniform( rho_p - var_rho_p , rho_p + var_rho_p , 1 )
							elif( dist_input_rho_p == 3 ):
								rho_p_vector[ i ] = np.random.gamma( rho_p_k , rho_p_theta , 1 )
							else:
								rho_p_vector[ i ] = np.random.lognormal( np.log( rho_p * rho_p / np.sqrt( rho_p * rho_p + var_rho_p * var_rho_p ) ) , np.log( 1 + var_rho_p * var_rho_p / rho_p / rho_p ) , 1 )
							aux_boolean = 1
					if( aux_boolean == 0 ):
						break
			if( var_rho_gas > 0.0 or dist_input_rho_gas == 3 ):
				while True:
					aux_boolean = 0
					for i in range( 0 , N ):
						if( rho_gas_vector[ i ] < 0 ):
							if( dist_input_rho_gas == 1 ):
								rho_gas_vector[ i ] = np.random.normal( rho_gas , var_rho_gas , 1 )
							elif( dist_input_rho_gas == 2 ):
								rho_gas_vector[ i ] = np.random.uniform( rho_gas - var_rho_gas , rho_gas + var_rho_gas , 1 )
							elif( dist_input_rho_gas == 3 ):
								rho_gas_vector[ i ] = np.random.gamma( rho_gas_k , rho_gas_theta , 1 )
							else:
								rho_gas_vector[ i ] = np.random.lognormal( np.log( rho_gas * rho_gas / np.sqrt( rho_gas * rho_gas + var_rho_gas * var_rho_gas ) ) , np.log( 1 + var_rho_gas * var_rho_gas / rho_gas / rho_gas ) , 1 )
							aux_boolean = 1
					if( aux_boolean == 0 ):
						break
					
	return [ volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , N , variable_vector , limits_calib , Probability_Save ]

def create_vent_deg( vent_type , input_file_vent , lon_cen , lat_cen , var_cen , azimuth_lin, length_lin , radius_rad , ang1_rad , ang2_rad , step_lon_deg , step_lat_deg , step_lon_m , step_lat_m , dist_input_cen , N ):

	if( vent_type == 4 ):
		file_data = np.loadtxt( input_file_vent )
		N = np.minimum( N , len( file_data[ : ] ) )
		lon_cen_vector = file_data[ range( 0 , N ) , 0 ]
		lat_cen_vector = file_data[ range( 0 , N ) , 1 ]
	else:
		if( var_cen > 0.0 ):
			if( dist_input_cen == 1 ):
				lon_cen_vector = np.random.normal( lon_cen, var_cen * step_lon_deg / step_lon_m , N )
				lat_cen_vector = np.random.normal( lat_cen, var_cen * step_lat_deg / step_lat_m , N )
			else:
				lon_cen_vector = np.random.uniform( lon_cen - var_cen * step_lon_deg / step_lon_m , lon_cen + var_cen * step_lon_deg / step_lon_m , N )
				lat_cen_vector = np.random.uniform( lat_cen - var_cen * step_lat_deg / step_lat_m , lat_cen + var_cen * step_lat_deg / step_lat_m , N )
				while True: 
					aux_boolean = 0
					for i in range( 0 , N ):
						if( np.power( ( lon_cen_vector[ i ] - lon_cen ) * step_lon_m / step_lon_deg , 2 ) + np.power( ( lat_cen_vector[ i ] - lat_cen ) * step_lat_m / step_lat_deg , 2 ) > np.power( var_cen , 2 ) ):
							lon_cen_vector[ i ] = np.random.uniform( lon_cen - var_cen * step_lon_deg / step_lon_m , lon_cen + var_cen * step_lon_deg / step_lon_m , 1 )
							lat_cen_vector[ i ] = np.random.uniform( lat_cen - var_cen * step_lat_deg / step_lat_m , lat_cen + var_cen * step_lat_deg / step_lat_m , 1 )
							aux_boolean = 1
					if( aux_boolean == 0 ):
						break
		else:
			lon_cen_vector = np.ones( N ) * lon_cen
			lat_cen_vector = np.ones( N ) * lat_cen
		if( vent_type == 2 ):
			pos_structure = np.random.uniform( -1 , 1 , N )
			lon_cen_vector = lon_cen_vector + pos_structure * np.sin( azimuth_lin * np.pi / 180 ) * length_lin * step_lon_deg / step_lon_m
			lat_cen_vector = lat_cen_vector + pos_structure * np.cos( azimuth_lin * np.pi / 180 ) * length_lin * step_lat_deg / step_lat_m
		if( vent_type == 3 ):
			pos_structure = ang1_rad + np.random.uniform( 0 , 1 , N ) * ( ang2_rad - ang1_rad )
			lon_cen_vector = lon_cen_vector + np.cos( pos_structure * np.pi / 180 ) * radius_rad * step_lon_deg / step_lon_m
			lat_cen_vector = lat_cen_vector + np.sin( pos_structure * np.pi / 180 ) * radius_rad * step_lat_deg / step_lat_m

	return [ lon_cen_vector , lat_cen_vector , N ]

def create_vent_utm( vent_type , input_file_vent , east_cen , north_cen , var_cen , azimuth_lin, length_lin , radius_rad , ang1_rad , ang2_rad , dist_input_cen , N ):

	if( vent_type == 4 ):
		file_data = np.loadtxt( input_file_vent )
		N = np.minimum( N , len( file_data[ : ] ) )
		east_cen_vector = file_data[ range( 0 , N ) , 0 ]
		north_cen_vector = file_data[ range( 0 , N ) , 1 ]
	else:
		if( var_cen > 0.0 ):
			if( dist_input_cen == 1 ):
				east_cen_vector = np.random.normal( east_cen , var_cen , N )
				north_cen_vector = np.random.normal( north_cen , var_cen , N )
			else:
				east_cen_vector = np.random.uniform( east_cen - var_cen , east_cen + var_cen , N )
				north_cen_vector = np.random.uniform( north_cen - var_cen, north_cen + var_cen , N )
				while True:
					aux_boolean = 0
					for i in range( 0 , N ):
						if( np.power( ( east_cen_vector[ i ] - east_cen ) , 2 ) + np.power( ( north_cen_vector[ i ] - north_cen ) , 2 ) > np.power( var_cen , 2 ) ):
							east_cen_vector[ i ] = np.random.uniform( east_cen - var_cen , east_cen + var_cen , 1 )
							north_cen_vector[ i ] = np.random.uniform( north_cen - var_cen , north_cen + var_cen , 1 )
							aux_boolean = 1
					if( aux_boolean == 0 ):
						break
		else:
			east_cen_vector = np.ones( N ) * east_cen
			north_cen_vector = np.ones( N ) * north_cen
		if( vent_type == 2 ):
			pos_structure = np.random.uniform( -1 , 1 , N )
			east_cen_vector = east_cen_vector + pos_structure * np.sin( azimuth_lin * np.pi / 180 ) * length_lin
			north_cen_vector = north_cen_vector + pos_structure * np.cos( azimuth_lin * np.pi / 180 ) * length_lin
		if( vent_type == 3 ):
			pos_structure = ang1_rad + np.random.uniform( 0 , 1 , N ) * ( ang2_rad - ang1_rad )
			east_cen_vector = east_cen_vector + np.cos( pos_structure * np.pi / 180 ) * radius_rad 
			north_cen_vector = north_cen_vector + np.sin( pos_structure * np.pi / 180 ) * radius_rad

	return [ east_cen_vector , north_cen_vector , N ]

def read_comparison_polygon_deg( comparison_polygon , ang_cal , ang_cal_range , lon1 , lon2 , lat1 , lat2 , lon_cen , lat_cen , step_lat_m , step_lon_m , cells_lon , cells_lat , matrix_lon , matrix_lat , step_lon_deg , step_lat_deg , N ):

	if( not comparison_polygon == '' ):
		points = np.loadtxt( comparison_polygon )
		polygon_compare = []
		for i in range( 0 , len( points ) ):
			polygon_compare.append( ( int( ( points[ i , 0 ] - lon1 ) * cells_lon / ( lon2 - lon1 ) ) , int( ( points[ i , 1 ] - lat1 ) * cells_lat / ( lat2 - lat1 ) ) ) )
		img_compare = Image.new( 'L' , ( cells_lon , cells_lat ) , 0 )
		draw = ImageDraw.Draw( img_compare ).polygon( polygon_compare , outline = 1 , fill = 1 )
		matrix_compare = np.array( img_compare )
		string_compare = np.zeros( ( N , 9 ) ) * np.nan
		line_compare = plt.contour( matrix_lon , matrix_lat , matrix_compare[ range( len( matrix_compare[ : , 0 ] ) -1 , -1 , -1 ) , : ], np.array( [ 0 ] ) , colors = 'r' , interpolation = 'linear' )
		plt.close()
		path_compare = line_compare.collections[ 0 ].get_paths()[ 0 ]
		ver_compare = path_compare.vertices
		dist_compare = np.zeros( len( ver_compare ) - 1 )
		for i in range( len( ver_compare ) - 1 ):
			utm1 = utm.from_latlon( ver_compare[ i , 1 ] , ver_compare[ i , 0 ] )
			utm2 = utm.from_latlon( ver_compare[ i + 1 , 1 ] , ver_compare[ i + 1 , 0 ] )
			distance_lon_1 = abs( utm2[ 0 ] - utm1[ 0 ] )
			distance_lat_1 = abs( utm2[ 1 ] - utm1[ 1 ] )
			dist_compare[ i ] = np.sqrt( distance_lon_1 ** 2 + distance_lat_1 ** 2 )
		dist_tot = sum( dist_compare )
		dist_step = np.arange( 0 , dist_tot , dist_tot / 1000 )
		cum_compare = 0.0 * dist_compare
		for i in range( len( dist_compare ) ):
			cum_compare[ i ] = sum( dist_compare[ 0 : i + 1 ] )
		vertices_compare = np.zeros( ( len( dist_step ) , 2 ) )
		for i in range( len( dist_step ) ):
			for j in range( len( cum_compare ) ):
				if( dist_step[ i ] <= cum_compare[ j ] ):
					if( j == 0 ):
						factor = ( cum_compare[ j ] - dist_step[ i ] ) / cum_compare[ j ]
					else:
						factor = ( cum_compare[ j ] - dist_step[ i ] ) / ( cum_compare[ j ] - cum_compare[ j - 1 ] )
					vertices_compare[ i , 0 ] = ver_compare[ j + 1 ][ 0 ] * ( 1 - factor ) + ver_compare[ j ][ 0 ] * ( factor )
					vertices_compare[ i , 1 ] = ver_compare[ j + 1 ][ 1 ] * ( 1 - factor ) + ver_compare[ j ][ 1 ] * ( factor )
					break
	else:
		vertices_compare = np.nan
		matrix_compare = np.nan
		string_compare = np.zeros( ( N , 9 ) ) * np.nan
	if( ang_cal_range < 360 and not np.isnan( ang_cal ) ):
		wh_negative = np.where( ( matrix_lat - lat_cen ) <= 0 )
		ang_direction = 180 * np.arctan( ( matrix_lon - lon_cen ) * ( step_lon_m / step_lon_deg ) / ( matrix_lat - lat_cen ) / ( step_lat_m / step_lat_deg ) ) / np.pi
		ang_direction[ wh_negative ] = ang_direction[ wh_negative ] + 180.0
		ang_direction[ np.where( ang_direction < 0 ) ] = ang_direction[ np.where( ang_direction < 0 ) ] + 360.0
		matrix_aux_1 = np.zeros( ( cells_lat , cells_lon ) )
		matrix_aux_2 = np.zeros( ( cells_lat , cells_lon ) )
		if( ang_cal - ang_cal_range / 2.0 < 0 ):
			wh_direction_1 = np.where( ang_direction <= ang_cal + ang_cal_range / 2.0 )
			wh_direction_2 = np.where( ang_direction >= ang_cal - ang_cal_range / 2.0 + 360.0 )
			matrix_aux_1[ wh_direction_1 ] = 1
			matrix_aux_1[ wh_direction_2 ] = 1
			data_direction = matrix_aux_1
		elif( ang_cal + ang_cal_range / 2.0 >= 360 ):
			wh_direction_1 = np.where( ang_direction <= ang_cal + ang_cal_range / 2.0 - 360.0 )
			wh_direction_2 = np.where( ang_direction >= ang_cal - ang_cal_range / 2.0 )
			matrix_aux_1[ wh_direction_1 ] = 1
			matrix_aux_1[ wh_direction_2 ] = 1
			data_direction = matrix_aux_1
		else:
			wh_direction_1 = np.where( ang_direction >= ang_cal - ang_cal_range / 2.0 )
			wh_direction_2 = np.where( ang_direction <= ang_cal + ang_cal_range / 2.0 )
			matrix_aux_1[ wh_direction_1 ] = 1
			matrix_aux_2[ wh_direction_2 ] = 1
			data_direction = matrix_aux_1 * matrix_aux_2
	else:
		data_direction = np.ones( ( cells_lat , cells_lon ) )

	return [ matrix_compare , vertices_compare , string_compare , data_direction ]

def read_comparison_polygon_utm( comparison_polygon , ang_cal , ang_cal_range , east_cor , north_cor , east_cen , north_cen , cellsize , n_east , n_north , matrix_east , matrix_north , N ):

	if( not comparison_polygon == '' ):
		points = np.loadtxt( comparison_polygon )
		polygon_compare = []
		for i in range( 0 , len( points ) ):
			polygon_compare.append( ( int( ( points[ i , 0 ] - east_cor ) / cellsize ) , int( ( points[ i , 1 ] - north_cor ) / cellsize ) ) )
		img_compare = Image.new( 'L' , ( n_east , n_north ) , 0 )
		draw = ImageDraw.Draw( img_compare ).polygon( polygon_compare , outline = 1 , fill = 1 )
		matrix_compare = np.array( img_compare )
		string_compare = np.zeros( ( N , 9 ) ) * np.nan
		line_compare = plt.contour( matrix_east , matrix_north , matrix_compare[ range( len( matrix_compare[ : , 0 ] ) -1 , -1 , -1 ) , : ], np.array( [ 0 ] ) , colors = 'r' , interpolation = 'linear' )
		plt.close()
		path_compare = line_compare.collections[ 0 ].get_paths()[ 0 ]
		ver_compare = path_compare.vertices
		dist_compare = np.zeros( len( ver_compare ) - 1 )
		for i in range( len( ver_compare ) - 1 ):
			dist_compare[ i ] = np.sqrt( ( ver_compare[ i + 1 , 1 ] - ver_compare[ i , 1 ] ) ** 2 + ( ver_compare[ i + 1 , 0 ] - ver_compare[ i , 0 ] ) ** 2 )
		dist_tot = sum( dist_compare )
		dist_step = np.arange( 0 , dist_tot , dist_tot / 1000 )
		cum_compare = 0.0 * dist_compare
		for i in range( len( dist_compare ) ):
			cum_compare[ i ] = sum( dist_compare[ 0 : i + 1 ] )
		vertices_compare = np.zeros( ( len( dist_step ) , 2 ) )
		for i in range( len( dist_step ) ):
			for j in range( len( cum_compare ) ):
				if( dist_step[ i ] <= cum_compare[ j ] ):
					if( j == 0 ):
						factor = ( cum_compare[ j ] - dist_step[ i ] ) / cum_compare[ j ]
					else:
						factor = ( cum_compare[ j ] - dist_step[ i ] ) / ( cum_compare[ j ] - cum_compare[ j - 1 ] )
					vertices_compare[ i , 0 ] = ver_compare[ j + 1 ][ 0 ] * ( 1 - factor ) + ver_compare[ j ][ 0 ] * ( factor )
					vertices_compare[ i , 1 ] = ver_compare[ j + 1 ][ 1 ] * ( 1 - factor ) + ver_compare[ j ][ 1 ] * ( factor )
					break
	else:
		vertices_compare = np.nan
		matrix_compare = np.nan
		string_compare = np.zeros( ( N , 9 ) ) * np.nan
	if( ang_cal_range < 360 and not np.isnan( ang_cal ) ):
		wh_negative = np.where( ( matrix_north - north_cen ) <= 0 )
		ang_direction = 180 * np.arctan( ( matrix_east - east_cen ) / ( matrix_north - north_cen ) ) / np.pi
		ang_direction[ wh_negative ] = ang_direction[ wh_negative ] + 180.0
		ang_direction[ np.where( ang_direction < 0 ) ] = ang_direction[ np.where( ang_direction < 0 ) ] + 360.0
		matrix_aux_1 = np.zeros( ( n_north , n_east ) )
		matrix_aux_2 = np.zeros( ( n_north , n_east ) )
		if( ang_cal - ang_cal_range / 2.0 < 0 ):
			wh_direction_1 = np.where( ang_direction <= ang_cal + ang_cal_range / 2.0 )
			wh_direction_2 = np.where( ang_direction >= ang_cal - ang_cal_range / 2.0 + 360.0 )
			matrix_aux_1[ wh_direction_1 ] = 1
			matrix_aux_1[ wh_direction_2 ] = 1
			data_direction = matrix_aux_1
		elif( ang_cal + ang_cal_range / 2.0 >= 360 ):
			wh_direction_1 = np.where( ang_direction <= ang_cal + ang_cal_range / 2.0 - 360.0 )
			wh_direction_2 = np.where( ang_direction >= ang_cal - ang_cal_range / 2.0 )
			matrix_aux_1[ wh_direction_1 ] = 1
			matrix_aux_1[ wh_direction_2 ] = 1
			data_direction = matrix_aux_1
		else:
			wh_direction_1 = np.where( ang_direction >= ang_cal - ang_cal_range / 2.0 )
			wh_direction_2 = np.where( ang_direction <= ang_cal + ang_cal_range / 2.0 )
			matrix_aux_1[ wh_direction_1 ] = 1
			matrix_aux_2[ wh_direction_2 ] = 1
			data_direction = matrix_aux_1 * matrix_aux_2
	else:
		data_direction = np.ones( ( n_north , n_east ) )

	return [ matrix_compare , vertices_compare , string_compare , data_direction ]

def initial_definitions( redist_volume ):

	angstep = 10
	distep = 10
	anglen = 360 / angstep
	pix_min = 0.0
	angstep_res2 = 2
	angstep_res3 = 0.4
	anglen_res2 = 360 / angstep_res2
	anglen_res3 = 360 / angstep_res3
	if( redist_volume == 3 or redist_volume == 4 ):
		factor_mult = 50.0
		center_elim = 0.5
		aux_backward = 1 / ( 1 + np.exp( factor_mult * ( np.linspace( 0.0, 1.0, int( anglen / 2 ) + 1 ) - center_elim ) ) )
		vector_backward_1 = np.zeros( int( anglen ) )
		vector_backward_1[ 0 : int( anglen / 2 - 1 ) ] = aux_backward[ int( anglen / 2 - 1 ) : 0 : -1 ]
		vector_backward_1[ int( anglen / 2 - 1 ) : ] = aux_backward[ : ]
		vector_backward_1[ vector_backward_1 < 1e-3 ] = 0
		vector_backward_1[ vector_backward_1 > 1.0 - 1e-3 ] = 1.0
		aux_backward = 1 / ( 1 + np.exp( factor_mult * ( np.linspace( 1.0 / ( anglen / 2 ) , 1.0 - 1.0 / ( anglen / 2 ) , int( anglen / 2 ) ) - center_elim ) ) )
		vector_backward_2 = np.zeros( int( anglen ) )
		vector_backward_2[ 0 : int( anglen / 2 ) ] = aux_backward[::-1]
		vector_backward_2[ int( anglen / 2 ) : ] = aux_backward[ : ]
		vector_backward_2[ vector_backward_2 < 1e-3 ] = 0
		vector_backward_2[ vector_backward_2 > 1.0 - 1e-3 ] = 1.0
		index_max = int( anglen / 2 - 1 )
		vector_correc = np.zeros( int( anglen ) )
	else:
		vector_correc = np.nan
		vector_backward_1 = np.nan
		vector_backward_2 = np.nan
		index_max = np.nan

	return [ angstep , distep , anglen , pix_min , angstep_res2 , angstep_res3 , anglen_res2 , anglen_res3 , vector_correc , vector_backward_1 , vector_backward_2 , index_max ]

def definitions_save_data_deg( source_dem , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , lon_cen_vector , lat_cen_vector , step_lon_m , step_lat_m , N , max_levels ):

	summary_data = np.zeros( ( N , 11 ) )
	summary_data[ : , 0 ] = volume_vector[ 0 : N ]
	summary_data[ : , 1 ] = phi_0_vector[ 0 : N ]
	summary_data[ : , 2 ] = ws_vector[ 0 : N ]
	summary_data[ : , 3 ] = Fr_vector[ 0 : N ]
	summary_data[ : , 4 ] = rho_p_vector[ 0 : N ]
	summary_data[ : , 5 ] = rho_gas_vector[ 0 : N ]
	summary_data[ : , 6 ] = lon_cen_vector[ 0 : N ]
	summary_data[ : , 7 ] = lat_cen_vector[ 0 : N ]
	area_pixel = step_lon_m * step_lat_m * 1e-6
	sim_data = str( N ) + "\n" + str( step_lon_m ) + "\n" + str( step_lat_m ) + "\n" + str( source_dem ) + "\n" + str( max_levels ) + "\n"
	string_data = ""
	string_cones = ""

	return [ summary_data , area_pixel , sim_data , string_data , string_cones ]

def definitions_save_data_utm( source_dem , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , east_cen_vector , north_cen_vector , cellsize , N , max_levels ):

	summary_data = np.zeros( ( N , 11 ) )
	summary_data[ : , 0 ] = volume_vector[ 0 : N ]
	summary_data[ : , 1 ] = phi_0_vector[ 0 : N ]
	summary_data[ : , 2 ] = ws_vector[ 0 : N ]
	summary_data[ : , 3 ] = Fr_vector[ 0 : N ]
	summary_data[ : , 4 ] = rho_p_vector[ 0 : N ]
	summary_data[ : , 5 ] = rho_gas_vector[ 0 : N ]
	summary_data[ : , 6 ] = east_cen_vector[ 0 : N ]
	summary_data[ : , 7 ] = north_cen_vector[ 0 : N ]
	area_pixel = cellsize * cellsize * 1e-6
	sim_data = str( N ) + "\n" + str( cellsize ) + "\n" + str( cellsize ) + "\n" + str( source_dem ) + "\n" + str( max_levels ) + "\n"
	string_data = ""
	string_cones = ""

	return [ summary_data , area_pixel , sim_data , string_data , string_cones ]

def compute_box_model_deg( type_sim , lon1 , lon2 , lat1 , lat2 , step_lon_deg , step_lat_deg , step_lon_m , step_lat_m , lon_cen_vector , lat_cen_vector , matrix_lon , matrix_lat , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , g , cells_lon , cells_lat , Topography , angstep , angstep_res2 , angstep_res3 , distep , area_pixel , max_levels , N , redist_volume , save_data , summary_data , string_data , string_cones , sim_data , anglen , pix_min , vector_backward_1 , vector_backward_2 , index_max , vector_correc , matrix_compare , vertices_compare , string_compare , data_direction , comparison_polygon ):

	data_cones = np.zeros( ( cells_lat , cells_lon ) )
	data_aux_t = np.ones( ( cells_lat , cells_lon ) )
	data_aux_b = np.zeros( ( cells_lat , cells_lon ) )
	vec_ang = np.arange( 0 , 360 , angstep )
	vec_ang_res2 = np.arange( 0, 360, angstep_res2 )
	vec_ang_res3 = np.arange( 0, 360, angstep_res3 )
	for i in range( 0 , N ):
		runout_min = -1
		current_level = 0
		data_step = np.zeros( ( cells_lat , cells_lon ) )
		polygon = []
		height_0 = interpol_pos( lon1 , lat1 , step_lon_deg , step_lat_deg , lon_cen_vector[ i ] , lat_cen_vector[ i ] , cells_lon , cells_lat , Topography )
		polygon.append( ( lon_cen_vector[ i ] , lat_cen_vector[ i ] , height_0 , 1.0 , -1 , volume_vector[ i ] , phi_0_vector[ i ] ) )
		sum_pixels = 0
		ws_current = ws_vector[ i ]
		Fr_current = Fr_vector[ i ]
		rho_p_current = rho_p_vector[ i ]
		rho_gas_current = rho_gas_vector[ i ]
		gp_current = g * ( rho_p_current - rho_gas_current ) / rho_gas_current
		for j in range( 10000 ):
			if( j == len( polygon ) ):
				if( N == 1 ):
					data_cones = data_cones + data_step
				break
			if( max_levels < polygon[ j ][ 3 ] ):
				if( N == 1 ):
					data_cones = data_cones + data_step
				break
			elif( current_level < polygon[ j ][ 3 ] ):
				current_level = polygon[ j ][ 3 ]
				if( N == 1 ):
					data_cones = data_cones + data_step
			polygon_xy = []
			polygons_new = []
			polygon_xy_res2 = []
			polygon_xy_res3 = []
			const_c = 0.5 * np.power( ws_current * polygon[ j ][ 6 ] * gp_current * Fr_current * Fr_current , 1.0 / 3.0 )
			Lmax = np.power( ( 16 * np.sqrt( 2 ) * np.power( const_c , 1.5 ) * np.power( polygon[ j ][ 5 ] / np.pi / ws_current , 1.5 ) ) , 0.25 )
			const_k = ( ws_current / Fr_current ) * np.power( gp_current, -0.5 ) * np.power( polygon[ j ][ 5 ] / np.pi , -1.5 )
			for angle_deg in vec_ang:
				angle_rad = angle_deg * np.pi / 180
				h_min = interpol_pos( lon1 , lat1 , step_lon_deg, step_lat_deg, polygon[ j ][ 0 ] , polygon[ j ][ 1 ] , cells_lon , cells_lat , Topography )
				for distance in range( 0 , 10000000 , distep ):
					if( distance > Lmax ):
						polygons_new.append( Lmax )
						distance = Lmax
						polygon_xy.append( ( int( ( polygon[ j ][ 0 ] + ( distance ) * cos( angle_rad ) * step_lon_deg / step_lon_m - lon1 ) * cells_lon / ( lon2 - lon1 ) ) , int( ( polygon[ j ][ 1 ] + ( distance ) * sin( angle_rad ) * step_lat_deg / step_lat_m - lat1 ) * cells_lat / ( lat2 - lat1 ) ) ) )
						break
					h = interpol_pos( lon1 , lat1 , step_lon_deg , step_lat_deg , polygon[ j ][ 0 ] + distance * cos( angle_rad ) * step_lon_deg / step_lon_m , polygon[ j ][ 1 ] + distance * sin( angle_rad ) * step_lat_deg / step_lat_m , cells_lon , cells_lat , Topography )
					h_min = min( h , h_min )
					h_boxmodel = ( 1 / ( 2 * g ) ) * np.power( ( const_c * np.power( Lmax, 1.0 / 3.0 ) ) / ( ( distance / Lmax ) * np.power( cosh( atanh( np.power( distance / Lmax, 2.0 ) ) ) , 2.0 ) ) , 2.0 )
					if( h >= h_min + h_boxmodel or np.isnan( h ) ):
						polygon_xy.append( ( int( ( polygon[ j ][ 0 ] + ( distance - distep ) * cos( angle_rad ) * step_lon_deg / step_lon_m - lon1 ) * cells_lon / ( lon2 - lon1 ) ) , int( ( polygon[ j ][ 1 ] + ( distance - distep ) * sin( angle_rad ) * step_lat_deg / step_lat_m - lat1 ) * cells_lat / ( lat2 - lat1 ) ) ) )
						polygons_new.append( distance - distep )
						break
			if( ( redist_volume == 3 or redist_volume == 4 ) and polygon[ j ][ 4 ] > -1 ):
				lim = int( polygon[ j ][ 4 ] )
				if( polygon[ j ][ 4 ] == int( polygon[ j ][ 4 ] ) ):
					for ii in range( int( anglen ) ):
						vector_correc[ ii ] = vector_backward_1[ int( ( ii - polygon[ j ][ 4 ] + index_max ) % anglen ) ]
				else:
					for ii in range( int( anglen ) ):
						vector_correc[ ii ] = vector_backward_2[ int( ( ii - polygon[ j ][ 4 ] + index_max ) % anglen ) ]
			else:
				vector_correc = np.ones( int( anglen ) )
			polygons_new = polygons_new * vector_correc
			if( j == 0 ):
				runout_min = min( polygons_new )
			if( max( polygons_new ) > 500 and max( polygons_new ) < 5000 ):
				for angle_deg in vec_ang_res2:
					angle_rad = angle_deg * np.pi / 180
					h_min = interpol_pos( lon1 , lat1 , step_lon_deg, step_lat_deg, polygon[ j ][ 0 ] , polygon[ j ][ 1 ] , cells_lon , cells_lat , Topography )
					for distance in range( 0 , 10000000 , distep ):
						if( distance > Lmax ):
							distance = Lmax
							polygon_xy_res2.append( ( int( ( polygon[ j ][ 0 ] + ( distance ) * cos( angle_rad ) * step_lon_deg / step_lon_m - lon1 ) * cells_lon / ( lon2 - lon1 ) ) , int( ( polygon[ j ][ 1 ] + ( distance ) * sin( angle_rad ) * step_lat_deg / step_lat_m - lat1 ) * cells_lat / ( lat2 - lat1 ) ) ) )
							break
						h = interpol_pos( lon1 , lat1 , step_lon_deg , step_lat_deg , polygon[ j ][ 0 ] + distance * cos( angle_rad ) * step_lon_deg / step_lon_m , polygon[ j ][ 1 ] + distance * sin( angle_rad ) * step_lat_deg / step_lat_m , cells_lon , cells_lat , Topography )
						h_min = min( h , h_min )
						h_boxmodel = ( 1 / ( 2 * g ) ) * np.power( ( const_c * np.power( Lmax, 1.0 / 3.0 ) ) / ( ( distance / Lmax ) * np.power( cosh( atanh( np.power( distance / Lmax, 2.0 ) ) ) , 2.0 ) ) , 2.0 )
						if( h >= h_min + h_boxmodel or np.isnan( h ) ):
							polygon_xy_res2.append( ( int( ( polygon[ j ][ 0 ] + ( distance - distep ) * cos( angle_rad ) * step_lon_deg / step_lon_m - lon1 ) * cells_lon / ( lon2 - lon1 ) ) , int( ( polygon[ j ][ 1 ] + ( distance - distep ) * sin( angle_rad ) * step_lat_deg / step_lat_m - lat1 ) * cells_lat / ( lat2 - lat1 ) ) ) )
							break
			elif( max( polygons_new ) >= 5000 ):
				for angle_deg in vec_ang_res3:
					angle_rad = angle_deg * np.pi / 180
					h_min = interpol_pos( lon1 , lat1 , step_lon_deg , step_lat_deg , polygon[ j ][ 0 ] , polygon[ j ][ 1 ] , cells_lon , cells_lat , Topography )
					for distance in range( distep , 10000000 , distep ):
						if( distance > Lmax ):
							distance = Lmax
							polygon_xy_res3.append( ( int( ( polygon[ j ][ 0 ] + ( distance ) * cos( angle_rad ) * step_lon_deg / step_lon_m - lon1 ) * cells_lon / ( lon2 - lon1 ) ) , int( ( polygon[ j ][ 1 ] + ( distance ) * sin( angle_rad ) * step_lat_deg / step_lat_m - lat1 ) * cells_lat / ( lat2 - lat1 ) ) ) )
							break
						h = interpol_pos( lon1, lat1, step_lon_deg , step_lat_deg , polygon[ j ][ 0 ] + distance * cos( angle_rad ) * step_lon_deg / step_lon_m , polygon[ j ][ 1 ] + distance * sin( angle_rad ) * step_lat_deg / step_lat_m , cells_lon , cells_lat , Topography )
						h_min = min( h , h_min )
						h_boxmodel = ( 1 / ( 2 * g ) ) * np.power( ( const_c * np.power( Lmax , 1.0 / 3.0 ) ) / ( ( distance / Lmax ) * np.power( cosh( atanh( np.power( distance / Lmax , 2.0 ) ) ) , 2.0 ) ) , 2.0 )
						if( h >= h_min + h_boxmodel or np.isnan( h ) ):
							polygon_xy_res3.append( ( int( ( polygon[ j ][ 0 ] + ( distance - distep ) * cos( angle_rad ) * step_lon_deg / step_lon_m - lon1 ) * cells_lon / ( lon2 - lon1 ) ) , int( ( polygon[ j ][ 1 ] + ( distance - distep ) * sin( angle_rad ) * step_lat_deg / step_lat_m - lat1 ) * cells_lat / ( lat2 - lat1 ) ) ) )
							break
			img = Image.new( 'L' , ( cells_lon , cells_lat ) , 0 )
			if( len( polygon_xy ) > 0 ):
				if( max( polygons_new ) <= 500 ):
					draw = ImageDraw.Draw( img ).polygon( polygon_xy , outline = 1 , fill = 1 )
				elif( max( polygons_new ) > 500 and max( polygons_new ) < 5000 ):
					draw = ImageDraw.Draw( img ).polygon( polygon_xy_res2 , outline = 1 , fill = 1 )
				else:
					draw = ImageDraw.Draw( img ).polygon( polygon_xy_res3 , outline = 1 , fill = 1 )
				data_step = np.maximum( np.minimum( data_aux_t , data_step + np.array( img ) ) , data_aux_b )
			if( max_levels > polygon[ j ][ 3 ] and sum( sum( data_step ) ) > sum_pixels + pix_min ):
				aux = np.zeros( len( polygons_new ) + 2 ) 
				aux[ 1 : len( polygons_new ) + 1 ] = np.array( polygons_new )
				aux[ 0 ] = polygons_new[ len( polygons_new ) - 1 ]
				aux[ len( polygons_new ) + 1 ] = polygons_new[ 0 ]
				der1 = ( aux[ 1 : len( aux ) - 1 ] - aux[ 2 : len( aux ) ] )
				der2 = ( aux[ 1 : len( aux ) - 1 ] - aux[ 0 : len( aux ) - 2 ] )
				wh1 = np.where( der1 >= 0 )
				wh2 = np.where( der2 >= 0 )
				wh_max = np.intersect1d( wh1[ 0 ] , wh2[ 0 ] )
				wh_grouped = np.split( wh_max , np.where( np.diff( wh_max ) > 1 )[ 0 ] + 1 )
				wh3 = np.where( abs( der1 ) > 0 )
				wh4 = np.where( abs( der2 ) > 0 )
				wh5 = np.intersect1d( wh_max , wh3[ 0 ] )
				wh6 = np.intersect1d( wh_max , wh4[ 0 ] )
				grouped_filter = np.zeros( len( wh_grouped ) )
				for x_grouped in range( len( wh_grouped ) ):
					if( len( np.intersect1d( wh_grouped[ x_grouped ] , wh5 ) ) > 0 and len( np.intersect1d( wh_grouped[ x_grouped ] , wh6 ) ) > 0 ):
						grouped_filter[ x_grouped ] = 1
				if( np.min( wh_grouped[ 0 ] ) == 0 and np.max( wh_grouped[ len( wh_grouped ) - 1 ] ) == anglen - 1 ):
					if( len( np.intersect1d( wh_grouped[ 0 ] , wh5 ) ) > 0 and len( np.intersect1d( wh_grouped[ len( wh_grouped ) - 1 ] , wh6 ) ) > 0 ):
						grouped_filter[ len( wh_grouped ) - 1 ] = 1
					aux_grouped = np.concatenate( ( wh_grouped[ len( wh_grouped ) - 1 ] , wh_grouped[ 0 ] + len( polygons_new ) ) )
					aux_filter = grouped_filter[ len( wh_grouped ) - 1 ] + grouped_filter[ 0 ]
					wh_grouped = wh_grouped[ 1 : -1 ]
					wh_grouped.append( aux_grouped )
					grouped_filter = np.append( grouped_filter[ 1 : -1 ] , aux_filter )
				wh_max = []
				for k in range( len( grouped_filter ) ):
					if( grouped_filter[ k ] > 0 ):
						if( np.mean( wh_grouped[ k ] ) < len( polygons_new ) and np.mean( wh_grouped[ k ] ) >= 0.0 ):
							wh_max.append( np.mean( wh_grouped[ k ] ) )
						elif( np.mean( wh_grouped[ k ] ) < len( polygons_new ) ):
							wh_max.append( len( polygons_new ) + np.mean( wh_grouped[ k ] ) )
						else:
							wh_max.append( - len( polygons_new ) + np.mean( wh_grouped[ k ] ) )
				if( redist_volume == 2 or redist_volume == 4 ):
					wh1 = np.where( der1 <= 0 )
					wh2 = np.where( der2 <= 0 )
					wh_min = np.intersect1d( wh1[ 0 ] , wh2[ 0 ] )
					wh_grouped = np.split( wh_min , np.where( np.diff( wh_min ) > 1 )[ 0 ] + 1 )
					wh3 = np.where( abs( der1 ) > 0 )
					wh4 = np.where( abs( der2 ) > 0 )
					wh5 = np.intersect1d( wh_min , wh3[ 0 ] )
					wh6 = np.intersect1d( wh_min , wh4[ 0 ] )
					grouped_filter = np.zeros( len( wh_grouped ) )
					for x_grouped in range( len( wh_grouped ) ):
						if( len( np.intersect1d( wh_grouped[ x_grouped ] , wh5 ) ) > 0 and len( np.intersect1d( wh_grouped[ x_grouped ] , wh6 ) ) > 0 ):
							grouped_filter[ x_grouped ] = 1
					if( np.min( wh_grouped[ 0 ] ) == 0 and np.max( wh_grouped[ len( wh_grouped ) - 1 ] ) == anglen - 1 ):
						if( len( np.intersect1d( wh_grouped[ 0 ] , wh5 ) ) > 0 and len( np.intersect1d( wh_grouped[ len( wh_grouped ) - 1 ] , wh6 ) ) > 0 ):
							grouped_filter[ len( wh_grouped ) - 1 ] = 1
						aux_grouped = np.concatenate( ( wh_grouped[ len( wh_grouped ) - 1 ], wh_grouped[ 0 ] + len( polygons_new ) ) )
						aux_filter = grouped_filter[ len( wh_grouped ) - 1 ] + grouped_filter[ 0 ]
						wh_grouped = wh_grouped[ 1 : -1 ]
						wh_grouped.append( aux_grouped )
						grouped_filter = np.append( grouped_filter[ 1 : -1 ], aux_filter )
					wh_min = []
					for k in range( len( grouped_filter ) ):
						if( grouped_filter[ k ] > 0 ):
							if( np.mean( wh_grouped[ k ] ) < len( polygons_new ) and np.mean( wh_grouped[ k ] ) >= 0.0 ):
								wh_min.append( np.mean( wh_grouped[ k ] ) )
							elif( np.mean( wh_grouped[ k ] ) < len( polygons_new ) ):
								wh_min.append( len( polygons_new ) + np.mean( wh_grouped[ k ] ) )
							else:
								wh_min.append( - len( polygons_new ) + np.mean( wh_grouped[ k ] ) )
				wh_sum = np.zeros( len( polygons_new ) ) 
				ter_sum = np.zeros( len( polygons_new ) ) 
				pos_sum = np.zeros( len( polygons_new ) )
				if( len( wh_max ) > 0 ):
					if( redist_volume == 1 or redist_volume == 3 or len( wh_max ) == 1 ):
						for l_max_real in wh_max:
							lmax = int( l_max_real )
							l_it = len( polygons_new ) - 1
							for l in range( 1 , len( polygons_new ) ):
								l_index = lmax + l
								if( l_index >= len( polygons_new ) ):
									l_index = l_index - len( polygons_new )
								if( polygons_new[ lmax ] < polygons_new[ l_index ] ):
									l_it = l
									break
								wh_sum[ lmax ] = wh_sum[ lmax ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
								ter_sum[ lmax ] = ter_sum[ lmax ] + 1.0 * vector_correc[ l_index ]
								pos_sum[ lmax ] = pos_sum[ lmax ] + polygons_new[ l_index ] * vector_correc[ l_index ]								
							for l in range( 1 , len( polygons_new ) - l_it ):
								l_index = lmax - l
								if( l_index < 0 ):
									l_index = l_index + len( polygons_new )
								if( polygons_new[ lmax ] < polygons_new[ l_index ] ):
									break
								wh_sum[ lmax ] = wh_sum[ lmax ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
								ter_sum[ lmax ] = ter_sum[ lmax ] + 1.0 * vector_correc[ l_index ]
								pos_sum[ lmax ] = pos_sum[ lmax ] + polygons_new[ l_index ] * vector_correc[ l_index ]
					elif( redist_volume == 2 or redist_volume == 4 ):
						wh_max = np.sort( wh_max )
						wh_min = np.sort( wh_min )
						if( wh_min[ 0 ] > wh_max[ 0 ] ):
							for l_ind in range( len( wh_max ) ):
								l_max_real = wh_max[ l_ind ]
								l_max_int = int( l_max_real )
								step_right = wh_min[ l_ind ] - l_max_int
								l_right_real = wh_min[ l_ind ]
								l_right_int = int( l_right_real )
								if( l_ind == 0 ):
									step_left = anglen + l_max_int - wh_min[ len( wh_min ) - 1 ]
									l_left_real = wh_min[ len( wh_min ) - 1 ]
									left_index = len( wh_min ) - 1
								else:
									step_left = l_max_int - wh_min[ l_ind - 1 ]
									l_left_real = wh_min[ l_ind - 1 ]
									left_index = l_ind - 1
								l_left_int = int( l_left_real )
								for l in range( 1 , int( step_right ) ):
									l_index = l_max_int + l
									if( l_index >= len( polygons_new ) ):
										l_index = l_index - len( polygons_new )
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_index ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_index ] * vector_correc[ l_index ]
								if( int( step_right ) == step_right ):
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + 0.5 * np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_right_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_right_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 0.5 * vector_correc[ l_right_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + 0.5 * polygons_new[ l_right_int ] * vector_correc[ l_right_int ]
								else:
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_right_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_right_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_right_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_right_int ] * vector_correc[ l_right_int ]
								for l in range( 1 , int( step_left ) ):
									l_index = l_max_int - l
									if( l_index < 0 ):
										l_index = len( polygons_new ) + l_index
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_index ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[l_index] * vector_correc[ l_index ]
								if( int( step_left ) == step_left ):
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + 0.5 * np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_left_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_left_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 0.5 * vector_correc[ l_left_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + 0.5 * polygons_new[ l_left_int ] * vector_correc[ l_left_int ]
								else:
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_left_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_left_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_left_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_left_int ] * vector_correc[ l_left_int ]
						else:
							for l_ind in range( len( wh_max ) ):
								l_max_real = wh_max[ l_ind ]
								l_max_int = int( l_max_real )
								step_left = l_max_int - wh_min[ l_ind ]
								l_left_real = wh_min[ l_ind ]
								l_left_int = int( l_left_real )
								if( l_ind == len( wh_max ) - 1 ):
									step_right = anglen - l_max_int + wh_min[ 0 ]
									l_right_real = wh_min[ 0 ]
									right_index = 0
								else:
									step_right = wh_min[ l_ind + 1 ] - l_max_int
									l_right_real = wh_min[ l_ind + 1 ]
									right_index = l_ind + 1
								l_right_int = int( l_right_real )
								for l in range( 1 , int( step_right ) ):
									l_index = l_max_int + l
									if( l_index >= len( polygons_new ) ):
										l_index = l_index - len( polygons_new )
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_index ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_index ] * vector_correc[ l_index ]
								if( int( step_right ) == step_right ):
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + 0.5 * np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_right_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_right_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 0.5 * vector_correc[ l_right_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + 0.5 * polygons_new[ l_right_int ] * vector_correc[ l_right_int ]
								else:
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_right_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_right_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_right_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_right_int ] * vector_correc[ l_right_int ]
								for l in range( 1 , int( step_left ) ):
									l_index = l_max_int - l
									if( l_index < 0 ):
										l_index = len( polygons_new ) + l_index
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_index ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_index ] * vector_correc[ l_index ]
								if( int( step_left ) == step_left ):
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + 0.5 * np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_left_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_left_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 0.5 * vector_correc[ l_left_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + 0.5 * polygons_new[ l_left_int ] * vector_correc[ l_left_int ]
								else:
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_left_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_left_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_left_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_left_int ] * vector_correc[ l_left_int ]
					for l in wh_max:
						lint = int( l )
						if( wh_sum[ lint ] > 0 ):
							wh_sum[ lint ] = wh_sum[ lint ] / ter_sum[ lint ]
							pos_sum[ lint ] = pos_sum[ lint ] / ter_sum[ lint ]
							new_x = polygon[ j ][ 0 ] + pos_sum[ lint ] * cos( ( vec_ang[ lint ] + angstep * ( l - lint ) ) * np.pi / 180 ) * step_lon_deg / step_lon_m ;
							new_y = polygon[ j ][ 1 ] + pos_sum[ lint ] * sin( ( vec_ang[ lint ] + angstep * ( l - lint ) ) * np.pi / 180 ) * step_lat_deg / step_lat_m ;
							height_eff = interpol_pos( lon1 , lat1 , step_lon_deg , step_lat_deg , new_x , new_y , cells_lon , cells_lat , Topography )
							new_volume = polygon[ j ][ 5 ] * ter_sum[ lint ] / sum( vector_correc ) * ( 1 - polygon[ j ][ 6 ] ) / ( 1 - wh_sum[ lint ] )
							if( not np.isnan( interpol_pos( lon1 , lat1 , step_lon_deg , step_lat_deg , new_x , new_y , cells_lon , cells_lat , Topography ) ) and wh_sum[ lint ] * new_volume > 1000 ):
								polygon.append( ( new_x , new_y , height_eff , polygon[ j ][ 3 ] + 1 , l , new_volume , wh_sum[ lint ] ) )

			sum_pixels = sum( sum( data_step ) )	
			print( ( j , len( polygon ) , polygon[ j ][ 3 ] , polygon[ j ][ 2 ] , sum( sum( data_step ) ) , polygon[ j ][ 4 ] , polygon[ j ][ 5 ] , polygon[ j ][ 6 ] , Lmax ) )
			if( save_data == 1 or type_sim == 2 ):
				if( j == 0 or ( j + 1 == len( polygon ) ) ):
					distances = np.power( np.power( ( matrix_lon - lon_cen_vector[ i ] ) * ( step_lon_m / step_lon_deg ) , 2 ) + np.power( ( matrix_lat - lat_cen_vector[ i ] ) * ( step_lat_m / step_lat_deg ) , 2 ) , 0.5 ) 
					distances = distances * data_step[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ]
					string_data = string_data + "\n" + str( polygon[ j ][ 3 ] ) + " " + str( sum( sum( data_step ) ) * area_pixel ) + " " + str( distances.max() / 1000.0 ) + " " + str( distances.min() / 1000.0 )
				elif( polygon[ j ][ 3 ] < polygon[ j + 1 ][ 3 ] ):
					distances = np.power( np.power( ( matrix_lon - lon_cen_vector[ i ] ) * ( step_lon_m / step_lon_deg ) , 2 ) + np.power( ( matrix_lat - lat_cen_vector[ i ] ) * ( step_lat_m / step_lat_deg ) , 2 ) , 0.5 ) 
					distances = distances * data_step[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ]
					string_data = string_data + "\n" + str( polygon[ j ] [ 3 ] ) + " " + str( sum( sum( data_step ) ) * area_pixel ) + " " + str( distances.max() / 1000.0 ) + " " + str( distances.min() / 1000.0 )
				if( N == 1 ):
					string_cones = string_cones + "\n" + str( j ) + " " + str( polygon[ j ][ 3 ] ) + " " + str( polygon[ j ][ 2 ] ) + " " + str( polygon[ j ][ 5 ] ) 
		if( N > 1 ):
			if( type_sim == 2 ):
				if( not comparison_polygon == '' ):
					data_step_border = data_step[ range( len( data_step[ : , 0 ] ) -1 , -1 , -1 ) , : ]
					data_step_border[ 0 , : ] = 0.0
					data_step_border[ len( data_step_border[ : , 0 ] ) -1 , : ] = 0.0
					data_step_border[ : , 0 ] = 0.0
					data_step_border[ : , len( data_step_border[ 0 , : ] ) -1 ] = 0.0
					line_new = plt.contour( matrix_lon , matrix_lat , data_step_border , np.array( [ 0 ] ) , colors = 'r' , interpolation = 'linear' )
					path_new = line_new.collections[ 0 ].get_paths()
					if( len( path_new ) == 1 ):
						path_new = path_new[ 0 ]
					else:
						areas_polygons = np.zeros( len( path_new ) )
						for i_areas in range( len( path_new ) ):
							areas_polygons[ i_areas ] = PolygonArea( path_new[ i_areas ].vertices )
						path_new = path_new[ np.argmax( areas_polygons ) ]
					ver_new = path_new.vertices
					dist_new = np.zeros( len( ver_new ) - 1 )
					plt.close()
					for ic in range( len( ver_new ) - 1 ):
						utm1 = utm.from_latlon( ver_new[ ic , 1 ] , ver_new[ ic , 0 ] )
						utm2 = utm.from_latlon( ver_new[ ic + 1 , 1 ] , ver_new[ ic + 1 , 0 ] )
						distance_lon_1 = abs( utm2[ 0 ] - utm1[ 0 ] )
						distance_lat_1 = abs( utm2[ 1 ] - utm1[ 1 ] )
						dist_new[ ic ] = np.sqrt( distance_lon_1 ** 2 + distance_lat_1 ** 2 )
					dist_new_tot = sum( dist_new )
					dist_new_step = np.arange( 0 , dist_new_tot - 1e-5, dist_new_tot / 1000 )
					cum_new_compare = 0.0 * dist_new
					for ic in range( len( dist_new ) ):
						cum_new_compare[ ic ] = sum( dist_new[ 0 : ic + 1 ] )
					vertices_new = np.zeros( ( len( dist_new_step ) , 2 ) )
					for ic in range( len( dist_new_step ) ):
						for jc in range( len( cum_new_compare ) ):
							if( dist_new_step[ ic ] < cum_new_compare[ jc ] ):
								if( jc == 0 ):
									factor = ( cum_new_compare[ jc ] - dist_new_step[ ic ] ) / cum_new_compare[ jc ]
								else:
									factor = ( cum_new_compare[ jc ] - dist_new_step[ ic ] ) / ( cum_new_compare[ jc ] - cum_new_compare[ jc - 1 ] )
								vertices_new[ ic , 0 ] = ver_new[ jc + 1 ][ 0 ] * ( 1 - factor ) + ver_new[ jc ][ 0 ] * ( factor )
								vertices_new[ ic , 1 ] = ver_new[ jc + 1 ][ 1 ] * ( 1 - factor ) + ver_new[ jc ][ 1 ] * ( factor )
								break
					sum_differences = 0
					dist_dir1 = np.zeros( ( len( vertices_compare ) , 1 ) )
					for ic in range( 0 , len( vertices_compare ) ):
						distance_lines = np.abs( vertices_compare[ ic , : ] - vertices_new )
						distance_lines = ( distance_lines[ : , 0 ] * step_lon_m / step_lon_deg * distance_lines[ : , 0 ] * step_lon_m / step_lon_deg ) + ( distance_lines[ : , 1 ] * step_lat_m / step_lat_deg * distance_lines[ : , 1 ] * step_lat_m / step_lat_deg )
						dist_dir1[ ic ] = np.sqrt( np.min( distance_lines ) )
						sum_differences = sum_differences + ( np.min( distance_lines ) ) / ( len( vertices_compare ) + len( vertices_new ) )
					dist_dir2 = np.zeros( ( len( vertices_new ) , 1 ) )
					for ic in range( 0 , len( vertices_new ) ):
						distance_lines = np.abs( vertices_new[ ic , : ] - vertices_compare )
						distance_lines = ( distance_lines[ : , 0 ] * step_lon_m / step_lon_deg * distance_lines[ : , 0 ] * step_lon_m / step_lon_deg ) + ( distance_lines[ : , 1 ] * step_lat_m / step_lat_deg * distance_lines[ : , 1 ] * step_lat_m / step_lat_deg )
						dist_dir2[ ic ] = np.sqrt( np.min( distance_lines ) )
						sum_differences = sum_differences + ( np.min( distance_lines ) ) / ( len( vertices_compare ) + len( vertices_new ) )
					plt.close()
					string_compare[ i , : ] = [ volume_vector[ i ] , phi_0_vector[ i ] , ( sum( sum( data_step * matrix_compare ) ) ) / ( sum( sum( np.maximum( data_step , matrix_compare ) ) ) ) , np.sqrt( sum_differences ) , max( max( dist_dir1[ : ] ) , max( dist_dir2[ : ] ) )[ 0 ] , distances.max() , ( sum( sum( data_step * matrix_compare * data_direction[ range( len( data_direction[ : , 0 ] ) -1 , -1 , -1 ) , : ] ) ) ) / ( sum( sum( np.maximum( data_step , matrix_compare ) * data_direction[ range( len( data_direction[ : , 0 ] ) -1 , -1 , -1 ) , : ] ) ) ) , ( distances * data_direction ).max() , sum( sum( data_step ) ) * area_pixel ]
				else:
					string_compare[ i , : ] = [ volume_vector[ i ] , phi_0_vector[ i ] , np.nan , np.nan , np.nan , distances.max() , np.nan , ( distances * data_direction ).max() , sum( sum( data_step ) ) * area_pixel ]
			data_cones = data_cones + data_step
		if( save_data == 1 or type_sim == 2 ):
			distances = np.power( np.power( ( matrix_lon - lon_cen_vector[ i ] ) * ( step_lon_m / step_lon_deg ) , 2 ) + np.power( ( matrix_lat - lat_cen_vector[ i ] ) * ( step_lat_m / step_lat_deg ) , 2 ) , 0.5 ) 
			distances = distances * data_step[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ]
			summary_data[ i , 8 ] = sum( sum( data_step ) ) * area_pixel
			summary_data[ i , 9 ] = distances.max() / 1000.0
			summary_data[ i , 10 ] = runout_min / 1000.0
		print( ' Simulation finished (N = ' + str( i + 1 ) + ')' )

	return [ summary_data , string_data , string_cones , string_compare , sim_data , data_cones , polygon ]

def compute_box_model_utm( type_sim , n_north , n_east , east_cor , north_cor , east_cen_vector , north_cen_vector , matrix_north , matrix_east , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , g , cellsize , Topography , angstep , angstep_res2 , angstep_res3 , distep , area_pixel , max_levels , N , redist_volume , save_data , summary_data , string_data , string_cones , sim_data , anglen , pix_min , vector_backward_1 , vector_backward_2 , index_max , vector_correc , matrix_compare , vertices_compare , string_compare , data_direction , comparison_polygon ):

	data_cones = np.zeros( ( n_north , n_east ) )
	data_aux_t = np.ones( ( n_north , n_east ) )
	data_aux_b = np.zeros( ( n_north , n_east ) )
	vec_ang = range( 0 , 360 , angstep )
	vec_ang_res2 = np.arange( 0 , 360 , angstep_res2 )
	vec_ang_res3 = np.arange( 0 , 360 , angstep_res3 )
	for i in range( 0 , N ):
		runout_min = -1
		current_level = 0
		data_step = np.zeros( ( n_north , n_east ) )
		polygon = []
		height_0 = interpol_pos( east_cor , north_cor , cellsize , cellsize , east_cen_vector[ i ] , north_cen_vector[ i ] , n_east , n_north , Topography )
		polygon.append( ( east_cen_vector[ i ] , north_cen_vector[ i ] , height_0 , 1.0 , -1 , volume_vector[ i ] , phi_0_vector[ i ] ) )
		sum_pixels = 0
		ws_current = ws_vector[ i ]
		Fr_current = Fr_vector[ i ]
		rho_p_current = rho_p_vector[ i ]
		rho_gas_current = rho_gas_vector[ i ]
		gp_current = g * ( rho_p_current - rho_gas_current ) / rho_gas_current
		for j in range( 10000 ):
			if( j == len( polygon ) ):
				if( N == 1 ):
					data_cones = data_cones + data_step
				break
			if( max_levels < polygon[ j ][ 3 ] ):
				if( N == 1 ):
					data_cones = data_cones + data_step
				break
			elif( current_level < polygon[ j ][ 3 ] ):
				current_level = polygon[ j ][ 3 ]
				if( N == 1 ):
					data_cones = data_cones + data_step
			polygon_xy = []
			polygons_new = []
			polygon_xy_res2 = []
			polygon_xy_res3 = []
			const_c = 0.5 * np.power( ws_current * polygon[ j ][ 6 ] * gp_current * Fr_current * Fr_current , 1.0 / 3.0 )
			Lmax = np.power( ( 16 * np.sqrt( 2 ) * np.power( const_c , 1.5 ) * np.power( polygon[ j ][ 5 ] / np.pi / ws_current , 1.5 ) ) , 0.25 )
			const_k = ( ws_current / Fr_current ) * np.power( gp_current, -0.5 ) * np.power( polygon[ j ][ 5 ] / np.pi , -1.5 )
			for angle_deg in vec_ang:
				angle_rad = angle_deg * np.pi / 180
				h_min = interpol_pos( east_cor , north_cor , cellsize , cellsize , polygon[ j ][ 0 ] , polygon[ j ][ 1 ] , n_east , n_north , Topography )
				for distance in range( 0 , 100000 , distep ):
					if( distance > Lmax ):
						polygons_new.append( Lmax )
						distance = Lmax
						polygon_xy.append( ( int( ( polygon[ j ][ 0 ] + ( distance ) * cos( angle_rad ) - east_cor ) * n_east / ( cellsize * ( n_east - 1 ) ) ) , int( ( polygon[ j ][ 1 ] + ( distance ) * sin( angle_rad ) - north_cor ) * n_north / ( cellsize * ( n_north - 1 ) ) ) ) )
						break
					h = interpol_pos( east_cor , north_cor , cellsize , cellsize , polygon[ j ][ 0 ] + distance * cos( angle_rad ) , polygon[ j ][ 1 ] + distance * sin( angle_rad ) , n_east , n_north , Topography )
					h_min = min( h , h_min )
					h_boxmodel = ( 1 / ( 2 * g ) ) * np.power( ( const_c * np.power( Lmax , 1.0 / 3.0 ) ) / ( ( distance / Lmax ) * np.power( cosh( atanh( np.power( distance / Lmax , 2.0 ) ) ) , 2.0 ) ) , 2.0 )
					if( h >= h_min + h_boxmodel or np.isnan( h ) ):
						polygon_xy.append( ( int( ( polygon[ j ][ 0 ] + ( distance - distep ) * cos( angle_rad ) - east_cor ) * n_east / ( cellsize * ( n_east - 1 ) ) ) , int( ( polygon[ j ][ 1 ] + ( distance - distep ) * sin( angle_rad ) - north_cor ) * n_north / ( cellsize * ( n_north - 1 ) ) ) ) )
						polygons_new.append( distance - distep )
						break
			if( ( redist_volume == 3 or redist_volume == 4 ) and polygon[ j ][ 4 ] > -1 ):
				lim = int( polygon[ j ][ 4 ] )
				if( polygon[ j ][ 4 ] == int( polygon[ j ][ 4 ] ) ):
					for ii in range( int( anglen ) ):
						vector_correc[ ii ] = vector_backward_1[ int( ( ii - polygon[ j ][ 4 ] + index_max ) % anglen ) ]
				else:
					for ii in range( int( anglen ) ):
						vector_correc[ ii ] = vector_backward_2[ int( ( ii - polygon[ j ][ 4 ] + index_max ) % anglen ) ]
			else:
				vector_correc = np.ones( int( anglen ) )
			polygons_new = polygons_new * vector_correc
			if( j == 0 ):
				runout_min = min( polygons_new )
			if( max( polygons_new ) > 500 and max( polygons_new ) < 5000 ):
				for angle_deg in vec_ang_res2:
					angle_rad = angle_deg * np.pi /180
					h_min = interpol_pos( east_cor , north_cor , cellsize , cellsize , polygon[ j ][ 0 ] , polygon[ j ][ 1 ] , n_east , n_north , Topography )
					for distance in range( 0 , 100000 , distep ):
						if( distance > Lmax ):
							distance = Lmax
							polygon_xy_res2.append( ( int( ( polygon[ j ][ 0 ] + ( distance ) * cos( angle_rad ) - east_cor ) * n_east / ( cellsize * ( n_east - 1 ) ) ) , int( ( polygon[ j ][ 1 ] + ( distance ) * sin( angle_rad ) - north_cor ) * n_north / ( cellsize * ( n_north - 1 ) ) ) ) )
							break
						h = interpol_pos( east_cor , north_cor , cellsize , cellsize , polygon[ j ][ 0 ] + distance * cos( angle_rad ) , polygon[ j ][ 1 ] + distance * sin( angle_rad ) , n_east , n_north , Topography )
						h_min = min( h , h_min )
						h_boxmodel = ( 1 / ( 2 * g ) ) * np.power( ( const_c * np.power( Lmax , 1.0 / 3.0 ) ) / ( ( distance / Lmax ) * np.power( cosh( atanh( np.power( distance / Lmax, 2.0 ) ) ) , 2.0 ) ) , 2.0 )
						if( h >= h_min + h_boxmodel or np.isnan( h ) ):
							polygon_xy_res2.append( ( int( ( polygon[ j ][ 0 ] + ( distance - distep ) * cos( angle_rad ) - east_cor ) * n_east / ( cellsize * ( n_east - 1 ) ) ) , int( ( polygon[ j ][ 1 ] + ( distance - distep ) * sin( angle_rad ) - north_cor ) * n_north / ( cellsize * ( n_north - 1 ) ) ) ) )
							break
			elif( max( polygons_new ) >= 5000 ):
				for angle_deg in vec_ang_res3:
					angle_rad = angle_deg * np.pi /180
					h_min = interpol_pos( east_cor , north_cor , cellsize , cellsize , polygon[ j ][ 0 ] , polygon[ j ][ 1 ] , n_east , n_north , Topography )
					for distance in range( 0 , 100000 , distep ):
						if( distance > Lmax ):
							distance = Lmax
							polygon_xy_res3.append( ( int( ( polygon[ j ][ 0 ] + ( distance ) * cos( angle_rad ) - east_cor ) * n_east / ( cellsize * ( n_east - 1 ) ) ) , int( ( polygon[ j ][ 1 ] + ( distance ) * sin( angle_rad ) - north_cor ) * n_north / ( cellsize * ( n_north - 1 ) ) ) ) )
							break
						h = interpol_pos( east_cor , north_cor , cellsize , cellsize , polygon[ j ][ 0 ] + distance * cos( angle_rad ) , polygon[ j ][ 1 ] + distance * sin( angle_rad ) , n_east , n_north , Topography )
						h_min = min( h , h_min )
						h_boxmodel = ( 1 / ( 2 * g ) ) * np.power( ( const_c * np.power( Lmax , 1.0 / 3.0 ) ) / ( ( distance / Lmax ) * np.power( cosh( atanh( np.power( distance / Lmax, 2.0 ) ) ) , 2.0 ) ) , 2.0 )
						if( h >= h_min + h_boxmodel or np.isnan( h ) ):
							polygon_xy_res3.append( ( int( ( polygon[ j ][ 0 ] + ( distance - distep ) * cos( angle_rad ) - east_cor ) * n_east / ( cellsize * ( n_east - 1 ) ) ) , int( ( polygon[ j ][ 1 ] + ( distance - distep ) * sin( angle_rad ) - north_cor ) * n_north / ( cellsize * ( n_north - 1 ) ) ) ) )
							break
			img = Image.new( 'L' , ( n_east , n_north ) , 0 )
			if( len( polygon_xy ) > 0 ):
				if( max( polygons_new ) <= 500 ):
					draw = ImageDraw.Draw( img ).polygon( polygon_xy , outline = 1 , fill = 1 )
				elif( max( polygons_new ) > 500 and max( polygons_new ) < 5000 ):
					draw = ImageDraw.Draw( img ).polygon( polygon_xy_res2 , outline = 1 , fill = 1 )
				else:
					draw = ImageDraw.Draw( img ).polygon( polygon_xy_res3 , outline = 1 , fill = 1 )
				data_step = np.maximum( np.minimum( data_aux_t , data_step + np.array( img ) ) , data_aux_b )
			if( max_levels > polygon[ j ][ 3 ] and sum( sum( data_step ) ) > sum_pixels + pix_min ):
				aux = np.zeros( len( polygons_new ) + 2 ) 
				aux[ 1 : len( polygons_new ) + 1 ] = np.array( polygons_new ) 
				aux[ 0 ] = polygons_new[ len( polygons_new ) - 1 ]
				aux[ len( polygons_new ) + 1 ] = polygons_new[ 0 ]
				der1 = ( aux[ 1 : len( aux ) - 1 ] - aux[ 2 : len( aux ) ] )
				der2 = ( aux[ 1 : len( aux ) - 1 ] - aux[ 0 : len( aux ) - 2 ] )
				wh1 = np.where( der1 >= 0 )
				wh2 = np.where( der2 >= 0 )
				wh_max = np.intersect1d( wh1[ 0 ] , wh2[ 0 ] )
				wh_grouped = np.split( wh_max , np.where( np.diff( wh_max ) > 1 )[ 0 ] + 1 )
				wh3 = np.where( abs( der1 ) > 0 )
				wh4 = np.where( abs( der2 ) > 0 )
				wh5 = np.intersect1d( wh_max , wh3[ 0 ] )
				wh6 = np.intersect1d( wh_max , wh4[ 0 ] )
				grouped_filter = np.zeros( len( wh_grouped ) )
				for x_grouped in range( len( wh_grouped ) ):
					if( len( np.intersect1d( wh_grouped[ x_grouped ] , wh5 ) ) > 0 and len( np.intersect1d( wh_grouped[ x_grouped ] , wh6 ) ) > 0 ):
						grouped_filter[ x_grouped ] = 1
				if( np.min( wh_grouped[ 0 ] ) == 0 and np.max( wh_grouped[ len( wh_grouped ) - 1 ] ) == anglen - 1 ):
					if( len( np.intersect1d( wh_grouped[ 0 ] , wh5 ) ) > 0 and len( np.intersect1d( wh_grouped[ len( wh_grouped ) - 1 ] , wh6 ) ) > 0 ):
						grouped_filter[ len( wh_grouped ) - 1 ] = 1
					aux_grouped = np.concatenate( ( wh_grouped[ len( wh_grouped ) - 1 ] , wh_grouped[ 0 ] + len( polygons_new ) ) )
					aux_filter = grouped_filter[ len( wh_grouped ) - 1 ] + grouped_filter[ 0 ]
					wh_grouped = wh_grouped[ 1 : -1 ]
					wh_grouped.append( aux_grouped )
					grouped_filter = np.append( grouped_filter[ 1 : -1 ] , aux_filter )
				wh_max = []
				for k in range( len( grouped_filter ) ):
					if( grouped_filter[ k ] > 0 ):
						if( np.mean( wh_grouped[ k ] ) < len( polygons_new ) and np.mean( wh_grouped[ k ] ) >= 0.0 ):
							wh_max.append( np.mean( wh_grouped[ k ] ) )
						elif( np.mean( wh_grouped[ k ] ) < len( polygons_new ) ):
							wh_max.append( len( polygons_new ) + np.mean( wh_grouped[ k ] ) )
						else:
							wh_max.append( - len( polygons_new ) + np.mean( wh_grouped[ k ] ) )
				if( redist_volume == 2 or redist_volume == 4 ):
					wh1 = np.where( der1 <= 0 )
					wh2 = np.where( der2 <= 0 )
					wh_min = np.intersect1d( wh1[ 0 ] , wh2[ 0 ] )
					wh_grouped = np.split( wh_min , np.where( np.diff( wh_min ) > 1 )[ 0 ] + 1 )
					wh3 = np.where( abs( der1 ) > 0 )
					wh4 = np.where( abs( der2 ) > 0 )
					wh5 = np.intersect1d( wh_min , wh3[ 0 ] )
					wh6 = np.intersect1d( wh_min , wh4[ 0 ] )
					grouped_filter = np.zeros( len( wh_grouped ) )
					for x_grouped in range( len( wh_grouped ) ):
						if( len( np.intersect1d( wh_grouped[ x_grouped ] , wh5 ) ) > 0 and len( np.intersect1d( wh_grouped[ x_grouped ] , wh6 ) ) > 0 ):
							grouped_filter[ x_grouped ] = 1
					if( np.min( wh_grouped[ 0 ] ) == 0 and np.max( wh_grouped[ len( wh_grouped ) - 1 ] ) == anglen - 1 ):
						if( len( np.intersect1d( wh_grouped[ 0 ] , wh5 ) ) > 0 and len( np.intersect1d( wh_grouped[ len( wh_grouped ) - 1 ] , wh6 ) ) > 0 ):
							grouped_filter[ len( wh_grouped ) - 1 ] = 1
						aux_grouped = np.concatenate( ( wh_grouped[ len( wh_grouped ) - 1 ], wh_grouped[ 0 ] + len( polygons_new ) ) )
						aux_filter = grouped_filter[ len( wh_grouped ) - 1 ] + grouped_filter[ 0 ]
						wh_grouped = wh_grouped[ 1 : -1 ]
						wh_grouped.append( aux_grouped )
						grouped_filter = np.append( grouped_filter[ 1 : -1 ] , aux_filter )
					wh_min = []
					for k in range( len( grouped_filter ) ):
						if( grouped_filter[ k ] > 0 ):
							if( np.mean( wh_grouped[ k ] ) < len( polygons_new ) and np.mean( wh_grouped[ k ] ) >= 0.0 ):
								wh_min.append( np.mean( wh_grouped[ k ] ) )
							elif( np.mean( wh_grouped[ k ] ) < len( polygons_new ) ):
								wh_min.append( len( polygons_new ) + np.mean( wh_grouped[ k ] ) )
							else:
								wh_min.append( - len( polygons_new ) + np.mean( wh_grouped[ k ] ) )
				wh_sum = np.zeros( len( polygons_new ) )
				ter_sum = np.zeros( len( polygons_new ) ) 
				pos_sum = np.zeros( len( polygons_new ) )
				if( len( wh_max ) > 0 ):
					if( redist_volume == 1 or redist_volume == 3 or len( wh_max ) == 1 ):
						for l_max_real in wh_max:
							lmax = int( l_max_real )
							l_it = len( polygons_new ) - 1
							for l in range( 1 , len( polygons_new ) ):
								l_index = lmax + l
								if( l_index >= len( polygons_new ) ):
									l_index = l_index - len( polygons_new )
								if( polygons_new[ lmax ] < polygons_new[ l_index ] ):
									l_it = l
									break
								wh_sum[ lmax ] = wh_sum[ lmax ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
								ter_sum[ lmax ] = ter_sum[ lmax ] + 1.0 * vector_correc[ l_index ]
								pos_sum[ lmax ] = pos_sum[ lmax ] + polygons_new[ l_index ] * vector_correc[ l_index ] * np.cos( ( lmax - l_index ) * angstep * np.pi / 180.0 )
							for l in range( 1 , len( polygons_new ) - l_it ):
								l_index = lmax - l
								if( l_index < 0 ):
									l_index = l_index + len( polygons_new )
								if( polygons_new[ lmax ] < polygons_new[ l_index ] ):
									break
								wh_sum[ lmax ] = wh_sum[ lmax ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
								ter_sum[ lmax ] = ter_sum[ lmax ] + 1.0 * vector_correc[ l_index ]
								pos_sum[ lmax ] = pos_sum[ lmax ] + polygons_new[ l_index ] * vector_correc[ l_index ] * np.cos( ( lmax - l_index ) * angstep * np.pi / 180.0 )
					elif( redist_volume == 2 or redist_volume == 4 ):
						wh_max = np.sort( wh_max )
						wh_min = np.sort( wh_min )
						if( wh_min[ 0 ] > wh_max[ 0 ] ):
							for l_ind in range( len( wh_max ) ):
								l_max_real = wh_max[ l_ind ]
								l_max_int = int( l_max_real )
								step_right = wh_min[ l_ind ] - l_max_int
								l_right_real = wh_min[ l_ind ]
								l_right_int = int( l_right_real )
								if( l_ind == 0 ):
									step_left = anglen + l_max_int - wh_min[ len( wh_min ) - 1 ]
									l_left_real = wh_min[ len( wh_min ) - 1 ]
									left_index = len( wh_min ) - 1
								else:
									step_left = l_max_int - wh_min[ l_ind - 1 ]
									l_left_real = wh_min[ l_ind - 1 ]
									left_index = l_ind - 1
								l_left_int = int( l_left_real )
								for l in range( 1 , int( step_right ) ):
									l_index = l_max_int + l
									if( l_index >= len( polygons_new ) ):
										l_index = l_index - len( polygons_new )
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_index ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_index ] * vector_correc[ l_index ] * np.cos( ( l_max_int - l_index ) * angstep * np.pi / 180.0 )
								if( int( step_right ) == step_right ):
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + 0.5 * np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_right_int ], 4.0 ) , 2.0 ) * vector_correc[ l_right_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 0.5 * vector_correc[ l_right_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + 0.5 * polygons_new[ l_right_int ] * vector_correc[ l_right_int ] * np.cos( ( l_right_int - l_max_int ) * angstep * np.pi / 180.0 )
								else:
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_right_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_right_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_right_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_right_int ] * vector_correc[ l_right_int ] * np.cos( ( l_right_int - l_max_int ) * angstep * np.pi / 180.0 )
								for l in range( 1 , int( step_left ) ):
									l_index = l_max_int - l
									if( l_index < 0 ):
										l_index = len( polygons_new ) + l_index
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_index ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_index ] * vector_correc[ l_index ] * np.cos( ( l_max_int - l_index ) * angstep * np.pi / 180.0 )
								if( int( step_left ) == step_left ):
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + 0.5 * np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_left_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_left_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 0.5 * vector_correc[ l_left_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + 0.5 * polygons_new[ l_left_int ] * vector_correc[ l_left_int ] * np.cos( ( l_max_int - l_left_int ) * angstep * np.pi / 180.0 )
								else:
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_left_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_left_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_left_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_left_int ] * vector_correc[ l_left_int ] * np.cos( ( l_max_int - l_left_int ) * angstep * np.pi / 180.0 )
						else:
							for l_ind in range( len( wh_max ) ):
								l_max_real = wh_max[ l_ind ]
								l_max_int = int( l_max_real )
								step_left = l_max_int - wh_min[ l_ind ]
								l_left_real = wh_min[ l_ind ]
								l_left_int = int( l_left_real )
								if( l_ind == len( wh_max ) - 1 ):
									step_right = anglen - l_max_int + wh_min[ 0 ]
									l_right_real = wh_min[ 0 ]
									right_index = 0
								else:
									step_right = wh_min[ l_ind + 1 ] - l_max_int
									l_right_real = wh_min[ l_ind + 1 ]
									right_index = l_ind + 1
								l_right_int = int( l_right_real )
								for l in range( 1 , int( step_right ) ):
									l_index = l_max_int + l
									if( l_index >= len( polygons_new ) ):
										l_index = l_index - len( polygons_new )
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_index ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_index ] * vector_correc[ l_index ] * np.cos( ( l_max_int - l_index ) * angstep * np.pi / 180.0 )
								if( int( step_right ) == step_right ):
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + 0.5 * np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_right_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_right_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 0.5 * vector_correc[ l_right_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + 0.5 * polygons_new[ l_right_int ] * vector_correc[ l_right_int ] * np.cos( ( l_max_int - l_right_int ) * angstep * np.pi / 180.0 )
								else:
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_right_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_right_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_right_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_right_int ] * vector_correc[ l_right_int ] * np.cos( ( l_max_int - l_right_int ) * angstep * np.pi / 180.0 )
								for l in range( 1 , int( step_left ) ):
									l_index = l_max_int - l
									if( l_index < 0 ):
										l_index = len( polygons_new ) + l_index
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_index ] , 4.0 ) , 2.0 ) * vector_correc[ l_index ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_index ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_index ] * vector_correc[ l_index ] * np.cos( ( l_max_int - l_index ) * angstep * np.pi / 180.0 )
								if( int( step_left ) == step_left ):
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + 0.5 * np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_left_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_left_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 0.5 * vector_correc[ l_left_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + 0.5 * polygons_new[ l_left_int ] * vector_correc[ l_left_int ] * np.cos( ( l_max_int - l_left_int ) * angstep * np.pi / 180.0 )
								else:
									wh_sum[ l_max_int ] = wh_sum[ l_max_int ] + np.power( np.sqrt( polygon[ j ][ 6 ] ) - 0.125 * const_k * np.power( polygons_new[ l_left_int ] , 4.0 ) , 2.0 ) * vector_correc[ l_left_int ]
									ter_sum[ l_max_int ] = ter_sum[ l_max_int ] + 1.0 * vector_correc[ l_left_int ]
									pos_sum[ l_max_int ] = pos_sum[ l_max_int ] + polygons_new[ l_left_int ] * vector_correc[ l_left_int ] * np.cos( ( l_max_int - l_left_int ) * angstep * np.pi / 180.0 )
					for l in wh_max:
						lint = int( l )
						if( wh_sum[ lint ] > 0 ):
							wh_sum[ lint ] = wh_sum[ lint ] / ter_sum[ lint ]
							pos_sum[ lint ] = pos_sum[ lint ] / ter_sum[ lint ]
							new_x = polygon[ j ][ 0 ] + pos_sum[ lint ] * cos( ( vec_ang[ lint ] + angstep * ( l - lint ) ) * np.pi / 180 ) ; 
							new_y = polygon[ j ][ 1 ] + pos_sum[ lint ] * sin( ( vec_ang[ lint ] + angstep * ( l - lint ) ) * np.pi / 180 ) ;
							height_eff = interpol_pos( east_cor , north_cor , cellsize , cellsize , new_x , new_y , n_east , n_north , Topography )
							new_volume = polygon[ j ][ 5 ] * ter_sum[ lint ] / sum( vector_correc ) * ( 1 - polygon[ j ][ 6 ] ) / ( 1 - wh_sum[ lint ] )
							if( not np.isnan( interpol_pos( east_cor , north_cor , cellsize , cellsize , new_x , new_y , n_east , n_north , Topography ) ) and wh_sum[ lint ] * new_volume > 1000 ):
								polygon.append( ( new_x , new_y , height_eff , polygon[ j ][ 3 ] + 1 , l , new_volume, wh_sum[lint] ) )
			sum_pixels = sum( sum( data_step ) )
			print( ( j , len( polygon ) , polygon[ j ][ 3 ] , polygon[ j ][ 2 ] , sum( sum( data_step ) ) , polygon[ j ][ 4 ] , polygon[ j ][ 5 ] , polygon[ j ][ 6 ] , Lmax ) )
			if( save_data == 1 or type_sim == 2 ):
				if( j == 0 or ( j + 1 == len( polygon ) ) ):
					distances = np.power( np.power( ( matrix_east - east_cen_vector[ i ] ) , 2 ) + np.power( ( matrix_north - north_cen_vector[ i ] ) , 2 ) ,0.5 ) 
					distances = distances * data_step[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ]
					string_data = string_data + "\n" + str( polygon[ j ][ 3 ] ) + " " + str( sum( sum( data_step ) )* area_pixel ) + " " + str( distances.max() / 1000.0 ) + " " + str( distances.min() / 1000.0 )
				elif( polygon[ j ][ 3 ] < polygon[ j + 1 ][ 3 ] ):
					distances = np.power( np.power( ( matrix_east - east_cen_vector[ i ] ) , 2 ) + np.power( ( matrix_north - north_cen_vector[ i ] ) ,2 ) , 0.5 ) 
					distances = distances * data_step[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ]
					string_data = string_data + "\n" + str( polygon[ j ][ 3 ] ) + " " + str( sum( sum( data_step ) ) * area_pixel ) + " " + str( distances.max() / 1000.0 ) + " " + str( distances.min() / 1000.0 )
				if( N == 1 ):
					string_cones = string_cones + "\n" + str( j ) + " " + str( polygon[ j ][ 3 ] ) + " " + str( polygon[ j ][ 2 ] ) + " " + str( polygon[ j ][ 5 ] ) 
		if( N > 1 ):
			if( type_sim == 2 ):
				if( not comparison_polygon == '' ):
					data_step_border = data_step[ range( len( data_step[ : , 0 ] ) -1 , -1 , -1 ) , : ]
					data_step_border[ 0 , : ] = 0.0
					data_step_border[ len( data_step_border[ : , 0 ] ) -1 , : ] = 0.0
					data_step_border[ : , 0 ] = 0.0
					data_step_border[ : , len( data_step_border[ 0 , : ] ) -1 ] = 0.0
					line_new = plt.contour( matrix_east , matrix_north , data_step_border , np.array( [ 0 ] ) , colors = 'r' , interpolation = 'linear' )
					path_new = line_new.collections[ 0 ].get_paths()
					if( len( path_new ) == 1 ):
						path_new = path_new[ 0 ]
					else:
						areas_polygons = np.zeros( len( path_new ) )
						for i_areas in range( len( path_new ) ):
							areas_polygons[ i_areas ] = PolygonArea( path_new[ i_areas ].vertices )
						path_new = path_new[ np.argmax( areas_polygons ) ]
					ver_new = path_new.vertices
					dist_new = np.zeros( len( ver_new ) - 1 )
					plt.close()
					for ic in range( len( ver_new ) - 1 ):
						dist_new[ ic ] = np.sqrt( ( ver_new[ ic + 1 , 1 ] - ver_new[ ic , 1 ] ) ** 2 + ( ver_new[ ic + 1 , 0 ] - ver_new[ ic , 0 ] ) ** 2 )
					dist_new_tot = sum( dist_new )
					dist_new_step = np.arange( 0 , dist_new_tot - 1e-5 , dist_new_tot / 1000 )
					cum_new_compare = 0.0 * dist_new
					for ic in range( len( dist_new ) ):
						cum_new_compare[ ic ] = sum( dist_new[ 0 : ic + 1 ] )
					vertices_new = np.zeros( ( len( dist_new_step ) , 2 ) )
					for ic in range( len( dist_new_step ) ):
						for jc in range( len( cum_new_compare ) ):
							if( dist_new_step[ ic ] < cum_new_compare[ jc ] ):
								if( jc == 0 ):
									factor = ( cum_new_compare[ jc ] - dist_new_step[ ic ] ) / cum_new_compare[ jc ]
								else:
									factor = ( cum_new_compare[ jc ] - dist_new_step[ ic ] ) / ( cum_new_compare[ jc ] - cum_new_compare[ jc - 1 ] )
								vertices_new[ ic , 0 ] = ver_new[ jc + 1 ][ 0 ] * ( 1 - factor ) + ver_new[ jc ][ 0 ] * ( factor )
								vertices_new[ ic , 1 ] = ver_new[ jc + 1 ][ 1 ] * ( 1 - factor ) + ver_new[ jc ][ 1 ] * ( factor )
								break
					sum_differences = 0
					dist_dir1 = np.zeros( ( len( vertices_compare ) , 1 ) )
					for ic in range( 0 , len( vertices_compare ) ):
						distance_lines = np.abs( vertices_compare[ ic , : ] - vertices_new )
						distance_lines = ( distance_lines[ : , 0 ] * distance_lines[ : , 0 ] ) + ( distance_lines[ : , 1 ] * distance_lines[ : , 1 ] )
						dist_dir1[ ic ] = np.sqrt( np.min( distance_lines ) )
						sum_differences = sum_differences + ( np.min( distance_lines ) ) / ( len( vertices_compare ) + len( vertices_new ) )
					dist_dir2 = np.zeros( ( len( vertices_new ) , 1 ) )
					for ic in range( 0 , len( vertices_new ) ):
						distance_lines = np.abs( vertices_new[ ic , : ] - vertices_compare )
						distance_lines = ( distance_lines[ : , 0 ] * distance_lines[ : , 0 ] ) + ( distance_lines[ : , 1 ] * distance_lines[ : , 1 ] )
						dist_dir2[ ic ] = np.sqrt( np.min( distance_lines ) )
						sum_differences = sum_differences + ( np.min( distance_lines ) ) / ( len( vertices_compare ) + len( vertices_new ) )
					plt.close()
					string_compare[ i , : ] = [ volume_vector[ i ] , phi_0_vector[ i ] , ( sum( sum( data_step * matrix_compare ) ) ) / ( sum( sum( np.maximum( data_step , matrix_compare ) ) ) ) , np.sqrt( sum_differences ) , max( max( dist_dir1[ : ] ) , max( dist_dir2[ : ] ) )[ 0 ] , distances.max() , ( sum( sum( data_step * matrix_compare * data_direction[ range( len( data_direction[ : , 0 ] ) -1 , -1 , -1 ) , : ] ) ) ) / ( sum( sum( np.maximum( data_step, matrix_compare ) * data_direction[ range( len( data_direction[ : , 0 ] ) -1 , -1 , -1 ) , : ] ) ) ) , ( distances * data_direction ).max() , sum( sum( data_step ) ) * area_pixel ]
				else:
					string_compare[ i , : ] = [ volume_vector[ i ] , phi_0_vector[ i ] , np.nan , np.nan , np.nan , distances.max() , np.nan , ( distances * data_direction ).max() , sum( sum( data_step ) ) * area_pixel ]
			data_cones = data_cones + data_step
		if( save_data == 1 or type_sim == 2 ):
			distances = np.power( np.power( ( matrix_east - east_cen_vector[ i ] ) , 2 ) + np.power( ( matrix_north - north_cen_vector[ i ] ) , 2 ) , 0.5 ) 
			distances = distances * data_step[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ]
			summary_data[ i , 8 ] = sum( sum( data_step ) ) * area_pixel
			summary_data[ i , 9 ] = distances.max() / 1000.0
			summary_data[ i , 10 ] = runout_min / 1000.0
		print( ' Simulation finished (N = ' + str( i + 1 ) + ')' )

	return [ summary_data , string_data , string_cones , string_compare , sim_data , data_cones , polygon ]


def save_data_deg( run_name , source_dem , sea_flag , lon1 , lon2 , lat1 , lat2 , step_lon_m , step_lat_m , cells_lon , cells_lat , matrix_lon , matrix_lat , Topography , Topography_Sea , N , summary_data , string_data , string_cones , sim_data , data_cones, utm_save , save_type ):

	cellsize = max( step_lon_m , step_lat_m )
	if( cellsize == step_lon_m ):
		output_cells_lon = cells_lon - 1
		output_cells_lat = int( cells_lat * step_lat_m / step_lon_m )
	else:
		output_cells_lon = int( cells_lon * step_lon_m / step_lat_m )
		output_cells_lat = cells_lat - 1
	text_file = open( 'Results/' + run_name + '/' + 'output_map.asc' , 'w' )
	text_file.write( 'ncols' + ' ' + str( output_cells_lon ) + '\n' )
	text_file.write( 'nrows' + ' ' + str( output_cells_lat ) + '\n' )
	text_file.write( 'xllcorner'+ ' ' + str( utm_save[ 0 ] ) + '\n' )
	text_file.write( 'yllcorner'+ ' ' + str( utm_save[ 1 ] ) + '\n' )
	text_file.write( 'cellsize'+ ' ' + str( cellsize ) + '\n' )
	text_file.write( 'NODATA_value' + ' ' + '-9999' );
	data_cones_save = data_cones / N
	for j in range( 0 , output_cells_lat ):
		text_file.write( '\n' )
		for i in range( 0 , output_cells_lon ):
			matrix_output = interpol_pos( utm_save[ 0 ] , utm_save[ 1 ] , step_lon_m , step_lat_m , utm_save[ 0 ] + i * cellsize , utm_save[ 1 ] + j * cellsize , cells_lon , cells_lat , data_cones_save )
			text_file.write( ' ' + str( matrix_output ) )
	text_file.close()
	np.savetxt( 'Results/' + run_name + '/' + 'summary.txt', summary_data , fmt = '%.5e' )
	if( save_type == 1 ):
		np.savetxt( 'Results/' + run_name + '/' + 'data_conoids.txt', data_cones_save , fmt = '%.2e' )
		np.savetxt( 'Results/' + run_name + '/' + 'topography.txt', Topography , fmt = '%.2e' )
		if( sea_flag == 1 ):
			np.savetxt( 'Results/' + run_name + '/' + 'topography_sea.txt' , Topography_Sea , fmt = '%.5e' )
		text_file = open( 'Results/' + run_name + '/' + 'box_model_conoids.txt' , 'w' )
		text_file.write( string_data )
		text_file.close()
		if( N == 1 ):
			text_file = open( 'Results/' + run_name + '/' + 'box_model_conoids_h.txt' , 'w' )
			text_file.write( string_cones )
			text_file.close()
		text_file = open( 'Results/' + run_name + '/' + 'sim_data.txt', 'w' )
		text_file.write( sim_data )
		text_file.close()
		np.savetxt( 'Results/' + run_name + '/' + 'matrix_lon.txt' , matrix_lon , fmt = '%.5e' )
		np.savetxt( 'Results/' + run_name + '/' + 'matrix_lat.txt' , matrix_lat , fmt = '%.5e' )
	if( source_dem == 1 ):
		text_file = open( 'Results/' + run_name + '/Topography_3.txt' , 'w' )
		text_file.write( 'lon1 ' + str( lon1 ) + '\n' )
		text_file.write( 'lon2 ' + str( lon2 ) + '\n' )
		text_file.write( 'lat1 ' + str( lat1 ) + '\n' )
		text_file.write( 'lat2 ' + str( lat2 ) + '\n' )
		text_file.write( 'cells_lon ' + str( cells_lon ) + '\n' )
		text_file.write( 'cells_lat ' + str( cells_lat ) + '\n' )
		for i in range( cells_lat ):
			for j in range( cells_lon ):
				text_file.write( str( Topography[ i , j ] ) + ' ' )
			text_file.write( '\n' )
		text_file.close()

def save_data_utm( run_name , sea_flag , n_north , n_east , cellsize , matrix_east , matrix_north , Topography , Topography_Sea , N , summary_data , string_data , string_cones , string_compare , sim_data , data_cones , utm_save , save_type ):

	text_file = open( 'Results/' + run_name + '/' + 'output_map.asc' , 'w' )
	text_file.write( 'ncols' + ' ' + str( n_east ) + '\n' )
	text_file.write( 'nrows' + ' ' + str( n_north ) + '\n' )
	text_file.write( 'xllcorner'+ ' ' + str( utm_save[ 0 ] ) + '\n' )
	text_file.write( 'yllcorner'+ ' ' + str( utm_save[ 1 ] ) + '\n' )
	text_file.write( 'cellsize'+ ' ' + str( cellsize ) + '\n' )
	text_file.write( 'NODATA_value' + ' ' + '-9999' );
	data_cones_save = data_cones / N
	for i in range( n_north - 1 , -1 , -1 ):
		text_file.write( '\n' )
		for j in range( 0 , n_east ):
			text_file.write( ' ' + str( data_cones_save[ i , j ] ) )
	text_file.close()
	np.savetxt( 'Results/' + run_name + '/' + 'summary.txt', summary_data , fmt = '%.5e' )
	if( save_type == 1 ):
		np.savetxt( 'Results/' + run_name + '/' + 'data_conoids.txt', data_cones_save , fmt = '%.2e' )
		np.savetxt( 'Results/' + run_name + '/' + 'topography.txt', Topography , fmt = '%.2e' )
		if( sea_flag == 1 ):
			np.savetxt( 'Results/' + run_name + '/' + 'topography_sea.txt' , Topography_Sea , fmt = '%.5e' )
		text_file = open( 'Results/' + run_name + '/' + 'box_model_conoids.txt', 'w' )
		text_file.write( string_data )
		text_file.close()
		if( N == 1 ):
			text_file = open( 'Results/' + run_name + '/' + 'box_model_conoids_h.txt' , 'w' )
			text_file.write( string_cones )
			text_file.close()
		text_file = open( 'Results/' + run_name + '/' + 'sim_data.txt', 'w' )
		text_file.write( sim_data )
		text_file.close()
		np.savetxt( 'Results/' + run_name + '/' + 'matrix_east.txt' , matrix_east , fmt = '%.5e' )
		np.savetxt( 'Results/' + run_name + '/' + 'matrix_north.txt' , matrix_north , fmt = '%.5e' )
 
def plot_deg( run_name , type_sim , Cities , polygon , lon1 , lon2 , lat1 , lat2 , step_lat_m , step_lon_m , matrix_lon , matrix_lat , lon_cen_vector , lat_cen_vector , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , Topography , Topography_Sea , N , data_cones , matrix_compare , ang_cal_range , data_direction , calibration_data , comparison_polygon ):

	data_cones = data_cones[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ] / N
	line_val = data_cones.max()
	data_cones[ data_cones[ : , : ] == 0 ] = np.nan
	val_up = np.floor( ( line_val + 0.1 - 1.0 / N ) * 10.0 ) / 20.0
	val_down = np.maximum( val_up / 10.0 , 0.05 )
	plt.figure( 1 , figsize = ( 8.0 , 5.0 ) )
	plt.axes().set_aspect( step_lat_m / step_lon_m )
	cmapg = plt.cm.get_cmap( 'Greys' )
	cmapr = plt.cm.get_cmap( 'Reds' )
	cmaps = plt.cm.get_cmap( 'Blues' ) 
	if( N > 1 ):
		CS_Topo = plt.contourf( matrix_lon , matrix_lat , Topography , 100 , alpha = 1.0 , cmap = cmapg , antialiased = True )
		CS_Sea = plt.contourf( matrix_lon , matrix_lat , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )
		CS = plt.contourf( matrix_lon , matrix_lat , data_cones , 100 , vmin = 0.0 , vmax = 1.0 , alpha = 0.3 , interpolation = 'linear' , cmap = cmapr , antialiased = True )
		fmt = '%.2f'
		plt.colorbar()
		CS_lines = plt.contour( matrix_lon , matrix_lat , data_cones, np.array( [ val_down, val_up ] ) , colors = 'r' , interpolation = 'linear' , linewidths = 0.1 )
		plt.clabel( CS_lines , inline = 0.1 , fontsize = 7 , colors = 'k' , fmt = fmt )
	else:
		CS_Topo = plt.contourf( matrix_lon , matrix_lat , Topography , 100 , alpha = 1.0 , cmap = cmapg , antialiased = True )
		CS_Sea = plt.contourf( matrix_lon , matrix_lat , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )
		CS = plt.contourf( matrix_lon , matrix_lat , data_cones , 100 , alpha = 0.3 , cmap = cmapr , antialiased = True )
	plt.xlabel( 'Longitude $[^\circ]$' )
	plt.ylabel( 'Latitude $[^\circ]$' )
	plt.xlim( lon1 , lon2 )
	plt.ylim( lat1 , lat2 )
	for i in range( len( Cities ) ):
		plt.text( float( Cities[ i ][ 0 ] ) , float( Cities[ i ][ 1 ] ) , str( Cities[ i ][ 2 ] ) , horizontalalignment = 'center' , verticalalignment = 'center' , fontsize = 6 )
	for i in range( 0 , N ):
		plt.plot( lon_cen_vector[ i ] , lat_cen_vector[ i ] , 'r.' , markersize = 2 )
	if( N == 1 ):
		for i in range( 1 , len( polygon ) ):
			plt.plot( polygon[ i ][ 0 ] , polygon[ i ][ 1 ] , 'b.' , markersize = 2 )
	if( type_sim == 2 ):
		if( not comparison_polygon == '' ):
			line_compare = plt.contour( matrix_lon , matrix_lat , matrix_compare[ range( len( matrix_compare[ : , 0 ] ) -1 , -1 , -1 ) , : ], np.array( [ 0 ] ) , colors = 'b' , interpolation = 'linear' )
		if( ang_cal_range < 360 ):
			line_direction = plt.contour( matrix_lon , matrix_lat , data_direction , np.array( [ 0 ] ) , colors = 'g' , interpolation = 'linear' )
	plt.savefig( 'Results/' + run_name + '/Map.png' )
	if( N > 1 and type_sim == 1 ):
		plt.figure( 2 , figsize = ( 14.0 , 5.0 ) )
		plt.subplot( 231 )
		plt.hist( np.log10( volume_vector ) )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.subplot( 232 )
		plt.hist( phi_0_vector )
		plt.xlabel( 'Initial concentration' )
		plt.subplot( 233 )
		plt.hist( ws_vector )
		plt.xlabel( 'Sedimentation velocity [m/s]' )
		plt.subplot( 234 )
		plt.hist( Fr_vector )
		plt.xlabel( 'Froude number' )
		plt.subplot( 235 )
		plt.hist( rho_p_vector )
		plt.xlabel( 'Pyroclasts density [kg/m3]' )
		plt.subplot( 236 )
		plt.hist( rho_gas_vector )
		plt.xlabel( 'Gas density [kg/m3]' )
		plt.savefig( 'Results/' + run_name + '/Histogram.png' )
	if( type_sim == 2 ):
		volume_vals = np.log10( calibration_data[ : , 0 ] ) 
		volume_vals_reshaped = volume_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		phi_0_vals = calibration_data[ : , 1 ] 
		phi_0_vals_reshaped = phi_0_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		dist_vals = calibration_data[ : , 5 ]
		dist_vals_reshaped = dist_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		dist_dir_vals = calibration_data[ : , 7 ]
		dist_dir_vals_reshaped = dist_dir_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		area_vals = calibration_data[ : , 8 ]
		area_vals_reshaped = area_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		plt.figure( 2 , figsize = ( 8.0 , 5.0 ) )
		c4 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , dist_vals_reshaped )
		plt.colorbar( c4 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'Distance [m]' )
		plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
		plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
		plt.savefig( 'Results/' + run_name + '/Calibration_Distance.png' )
		plt.figure( 3 , figsize = ( 8.0 , 5.0 ) )
		c6 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , dist_dir_vals_reshaped )
		plt.colorbar( c6 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'Distance (directional) [m]' )
		plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
		plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
		plt.savefig( 'Results/' + run_name + '/Calibration_Distance_Directional.png' )
		plt.figure( 4 , figsize = ( 8.0 , 5.0 ) )
		c7 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , area_vals_reshaped )
		plt.colorbar( c7 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'Area [km2]' )
		plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
		plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
		plt.savefig( 'Results/' + run_name + '/Calibration_Area.png' )
		if( not comparison_polygon == '' ):
			Jaccard_vals = calibration_data[ : , 2 ]
			Jaccard_vals_reshaped = Jaccard_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
			MSD_vals = calibration_data[ : , 3 ]
			MSD_vals_reshaped = MSD_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
			HD_vals = calibration_data[ : , 4 ]
			HD_vals_reshaped = HD_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
			Jaccard_dir_vals = calibration_data[ : , 6 ]
			Jaccard_dir_vals_reshaped = Jaccard_dir_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
			plt.figure( 5 , figsize = ( 8.0 , 5.0 ) )
			c1 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , Jaccard_vals_reshaped , cmap = 'viridis' )
			plt.colorbar( c1 )
			plt.xlabel( 'log( Collapsing volume [m3] )' )
			plt.ylabel( 'Initial concentration' )
			plt.title( 'Jaccard Index' )
			plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
			plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
			plt.savefig( 'Results/' + run_name + '/Calibration_Jaccard.png' )
			plt.figure( 6 , figsize = ( 8.0 , 5.0 ) )
			c2 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , MSD_vals_reshaped , cmap = 'viridis_r' )
			plt.colorbar( c2 )
			plt.xlabel( 'log( Collapsing volume [m3] )' )
			plt.ylabel( 'Initial concentration' )
			plt.title( 'RMSD [m]' )
			plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
			plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
			plt.savefig( 'Results/' + run_name + '/Calibration_RMSD.png' )
			plt.figure( 7 , figsize = ( 8.0 , 5.0 ) )
			c3 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , HD_vals_reshaped , cmap = 'viridis_r' )
			plt.colorbar( c3 )
			plt.xlabel( 'log( Collapsing volume [m3] )' )
			plt.ylabel( 'Initial concentration' )
			plt.title( 'HD [m]' )
			plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
			plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
			plt.savefig( 'Results/' + run_name + '/Calibration_HD.png' )
			plt.figure( 8 , figsize = ( 8.0 , 5.0 ) )
			c5 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , Jaccard_dir_vals_reshaped , cmap = 'viridis' )
			plt.colorbar( c5 )
			plt.xlabel( 'log( Collapsing volume [m3] )' )
			plt.ylabel( 'Initial concentration' )
			plt.title( 'Jaccard Index (directional)' )
			plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
			plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
			plt.savefig( 'Results/' + run_name + '/Calibration_Jaccard_Directional.png' )
	plt.show()

def plot_utm( run_name , type_sim , polygon , matrix_east , matrix_north , east_cor , north_cor , n_east , n_north , cellsize , east_cen_vector , north_cen_vector , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , Topography , Topography_Sea , N , data_cones , matrix_compare , ang_cal_range , data_direction , calibration_data , comparison_polygon ):

	data_cones = data_cones[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ] / N
	line_val = data_cones.max()
	data_cones[ data_cones[ : , : ] == 0 ] = np.nan
	val_up = np.floor( ( line_val + 0.1 - 1.0 / N ) * 10.0 ) / 20.0
	val_down = np.maximum( val_up / 10.0 , 0.05 )
	plt.figure( 1 , figsize = ( 8.0 , 5.0 ) )
	plt.axes().set_aspect( 1.0 )
	cmapg = plt.cm.get_cmap( 'Greys' )
	cmapr = plt.cm.get_cmap( 'Reds' )
	cmaps = plt.cm.get_cmap( 'Blues' ) 
	if( N > 1 ):
		CS_Topo = plt.contourf( matrix_east , matrix_north , Topography , 100 , alpha = 1.0 , cmap = cmapg , antialiased = True )
		CS_Sea = plt.contourf( matrix_east , matrix_north , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )
		CS = plt.contourf( matrix_east , matrix_north , data_cones , 100, vmin = 0.0 , vmax = 1.0 , alpha = 0.3 , interpolation = 'linear' , cmap = cmapr , antialiased = True )	
		fmt = '%.2f'
		plt.colorbar()
		CS_lines = plt.contour( matrix_east , matrix_north , data_cones , np.array( [ val_down , val_up ] ) , colors = 'r' , interpolation = 'linear' , linewidths = 0.1 )
		plt.clabel( CS_lines , inline = 0.1 , fontsize = 7 , colors = 'k' , fmt = fmt )
	else:
		CS_Topo = plt.contourf( matrix_east , matrix_north , Topography , 100 , alpha = 1.0 , cmap = cmapg , antialiased = True )
		CS_Sea = plt.contourf( matrix_east , matrix_north , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )
		CS = plt.contourf( matrix_east , matrix_north , data_cones , 100 , alpha = 0.3 , cmap = cmapr , antialiased = True )

	plt.xlabel( 'East [m]' )
	plt.ylabel( 'North [m]' )
	plt.xlim( east_cor , east_cor + cellsize * ( n_east - 1 ) )
	plt.ylim( north_cor , north_cor + cellsize * ( n_north - 1 ) )
	for i in range( 0 , N ):
		plt.plot( east_cen_vector[ i ] , north_cen_vector[ i ] , 'r.' , markersize = 2 )
	if( N == 1 ):
		for i in range( 1 , len( polygon ) ):
			plt.plot( polygon[ i ][ 0 ] , polygon[ i ][ 1 ] , 'b.' , markersize = 2 )
	if( type_sim == 2 ):
		if( not comparison_polygon == '' ):
			line_compare = plt.contour( matrix_east , matrix_north , matrix_compare[ range( len( matrix_compare[ : , 0 ] ) -1 , -1 , -1 ) , : ], np.array( [ 0 ] ) , colors = 'b' , interpolation = 'linear' )
		if( ang_cal_range < 360 ):
			line_direction = plt.contour( matrix_east , matrix_north , data_direction , np.array( [ 0 ] ) , colors = 'g' , interpolation = 'linear' )
	plt.savefig( 'Results/' + run_name + '/Map.png' )
	if( N > 1 and type_sim == 1 ):
		plt.figure( 2 , figsize = ( 14.0 , 8.0 ) )
		plt.subplot( 231 )
		plt.hist( np.log10( volume_vector ) )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.subplot( 232 )
		plt.hist( phi_0_vector )
		plt.xlabel( 'Initial concentration' )
		plt.subplot( 233 )
		plt.hist( ws_vector )
		plt.xlabel( 'Sedimentation velocity [m/s]' )
		plt.subplot( 234 )
		plt.hist( Fr_vector )
		plt.xlabel( 'Froude number' )
		plt.subplot( 235 )
		plt.hist( rho_p_vector )
		plt.xlabel( 'Pyroclasts density [kg/m3]' )
		plt.subplot( 236 )
		plt.hist( rho_gas_vector )
		plt.xlabel( 'Gas density [kg/m3]' )
		plt.savefig( 'Results/' + run_name + '/Histogram.png' )
	if( type_sim == 2 ):
		volume_vals = np.log10( calibration_data[ : , 0 ] ) 
		volume_vals_reshaped = volume_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		phi_0_vals = calibration_data[ : , 1 ] 
		phi_0_vals_reshaped = phi_0_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		dist_vals = calibration_data[ : , 5 ]
		dist_vals_reshaped = dist_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		dist_dir_vals = calibration_data[ : , 7 ]
		dist_dir_vals_reshaped = dist_dir_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		area_vals = calibration_data[ : , 8 ]
		area_vals_reshaped = area_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		plt.figure( 2 , figsize = ( 8.0 , 5.0 ) )
		c4 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , dist_vals_reshaped )
		plt.colorbar( c4 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'Distance [m]' )
		plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
		plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
		plt.savefig( 'Results/' + run_name + '/Calibration_Distance.png' )
		plt.figure( 3 , figsize = ( 8.0 , 5.0 ) )
		c6 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , dist_dir_vals_reshaped )
		plt.colorbar( c6 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'Distance (directional) [m]' )
		plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
		plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
		plt.savefig( 'Results/' + run_name + '/Calibration_Distance_Directional.png' )
		plt.figure( 4 , figsize = ( 8.0 , 5.0 ) )
		c7 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , area_vals_reshaped )
		plt.colorbar( c7 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'Area [km2]' )
		plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
		plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
		plt.savefig( 'Results/' + run_name + '/Calibration_Area.png' )
		if( not comparison_polygon == '' ):
			Jaccard_vals = calibration_data[ : , 2 ]
			Jaccard_vals_reshaped = Jaccard_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
			MSD_vals = calibration_data[ : , 3 ]
			MSD_vals_reshaped = MSD_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
			HD_vals = calibration_data[ : , 4 ]
			HD_vals_reshaped = HD_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
			Jaccard_dir_vals = calibration_data[ : , 6 ]
			Jaccard_dir_vals_reshaped = Jaccard_dir_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
			plt.figure( 5 , figsize = ( 8.0 , 5.0 ) )
			c1 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , Jaccard_vals_reshaped , cmap = 'viridis' )
			plt.colorbar( c1 )
			plt.xlabel( 'log( Collapsing volume [m3] )' )
			plt.ylabel( 'Initial concentration' )
			plt.title( 'Jaccard Index' )
			plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
			plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
			plt.savefig( 'Results/' + run_name + '/Calibration_Jaccard.png' )
			plt.figure( 6 , figsize = ( 8.0 , 5.0 ) )
			c2 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , MSD_vals_reshaped , cmap = 'viridis_r' )
			plt.colorbar( c2 )
			plt.xlabel( 'log( Collapsing volume [m3] )' )
			plt.ylabel( 'Initial concentration' )
			plt.title( 'RMSD [m]' )
			plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
			plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
			plt.savefig( 'Results/' + run_name + '/Calibration_RMSD.png' )
			plt.figure( 7 , figsize = ( 8.0 , 5.0 ) )
			c3 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , HD_vals_reshaped , cmap = 'viridis_r' )
			plt.colorbar( c3 )
			plt.xlabel( 'log( Collapsing volume [m3] )' )
			plt.ylabel( 'Initial concentration' )
			plt.title( 'HD [m]' )
			plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
			plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
			plt.savefig( 'Results/' + run_name + '/Calibration_HD.png' )
			plt.figure( 8 , figsize = ( 8.0 , 5.0 ) )
			c5 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , Jaccard_dir_vals_reshaped , cmap = 'viridis' )
			plt.colorbar( c5 )
			plt.xlabel( 'log( Collapsing volume [m3] )' )
			plt.ylabel( 'Initial concentration' )
			plt.title( 'Jaccard Index (direction)' )
			plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
			plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
			plt.savefig( 'Results/' + run_name + '/Calibration_Jaccard_Directional.png' )
	plt.show()
	
def calibration( run_name , string_compare , resolution_factor , ws_val , Fr_val , rho_p_val , rho_gas_val ):

	np.savetxt( 'Results/' + run_name + '/Calibration_Data.txt' , [ resolution_factor ] , fmt = '%1.3f' )
	f = open( 'Results/' + run_name + '/Calibration_Data.txt' , 'a' )
	np.savetxt( f , [ ws_val ] , fmt = '%.5e' )
	np.savetxt( f , [ Fr_val ] , fmt = '%.5e' )
	np.savetxt( f , [ rho_p_val ] , fmt = '%.5e' )
	np.savetxt( f , [ rho_gas_val ] , fmt = '%.5e' )
	np.savetxt( f , string_compare , fmt = '%.5e' )
	f.close()

def PolygonArea( corners ):

	n = len( corners )
	area = 0.0
	for i in range( n ):
		j = ( i + 1 ) % n
		area += corners[ i ][ 0 ] * corners[ j ][ 1 ]
		area -= corners[ j ][ 0 ] * corners[ i ][ 1 ]
	area = abs( area ) / 2.0
	
	return area

def distance_two_points( lat1 , lat2 , lon1 , lon2 ):

	R = 6373.0
	lat1 = radians( lat1 )
	lon1 = radians( lon1 )
	lat2 = radians( lat2 )
	lon2 = radians( lon2 )
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin( dlat / 2.0 ) ** 2.0 + cos( lat1 ) * cos( lat2 ) * sin( dlon / 2.0 ) ** 2.0
	c = 2.0 * atan2( sqrt( a ) , sqrt( 1.0 - a ) )

	return ( R * c ) * 1000.0

def interpol_pos( lon1 , lat1 , step_lon_deg , step_lat_deg , lon_cen , lat_cen , cells_lon , cells_lat , Topography ):

	dlon = int( np.floor( ( lon_cen - lon1 ) / step_lon_deg ) )
	dlat = ( cells_lat - 2 ) - int( np.floor( ( lat_cen - lat1 ) / step_lat_deg ) )
	if( dlon >= ( cells_lon - 1.0 ) or dlat >= ( cells_lat - 1.0 ) or dlon < 0.0 or dlat < 0.0 ):
		return np.nan
	aux_lon = 2.0 * ( lon_cen - ( dlon * step_lon_deg + lon1 ) - step_lon_deg / 2.0 ) / step_lon_deg
	aux_lat = 2.0 *( - lat_cen + ( ( cells_lat - 1.0 - dlat ) * step_lat_deg + lat1 ) - step_lat_deg / 2.0 ) / step_lat_deg
	dc = ( Topography[ dlat ][ dlon ] + Topography[ dlat ][ dlon + 1 ] + Topography[ dlat + 1 ][ dlon ] + Topography[ dlat + 1 ][ dlon + 1 ] ) / 4
	[ x3 , y3 , z3 ] = [ 0.0 , 0.0 , dc ]
	if( aux_lon >= 0.0 and abs( aux_lon ) >= abs( aux_lat ) ):
		[ x1 , y1 , z1 ] = [ 1.0 , 1.0 , Topography[ dlat + 1 ][ dlon + 1 ] ] 
		[ x2 , y2 , z2 ] = [ 1.0 , -1.0 , Topography[ dlat ][ dlon + 1 ] ] 
	elif( aux_lat >= 0.0 and abs( aux_lon ) < abs( aux_lat ) ):
		[ x1 , y1 , z1] = [ -1.0 , 1.0 , Topography[ dlat + 1 ][ dlon ] ] 
		[ x2 , y2 , z2] = [ 1.0 , 1.0 , Topography[ dlat + 1 ][ dlon + 1 ] ] 
	elif( aux_lon < 0.0 and abs( aux_lon ) >= abs( aux_lat ) ):
		[ x1 , y1 , z1 ] = [ -1.0 , 1.0 , Topography[ dlat + 1 ][ dlon ] ] 
		[ x2 , y2 , z2 ] = [ -1.0 , -1.0 , Topography[ dlat ][ dlon ] ] 
	else:
		[ x1 , y1 , z1 ] = [ -1.0 , -1.0 , Topography[ dlat ][ dlon ] ] 
		[ x2 , y2 , z2 ] = [ 1.0 , -1.0 , Topography[ dlat ][ dlon + 1 ] ]
	f1 = ( y2 - y1 ) * ( z3 - z1 ) - ( y3 - y1 ) * ( z2 - z1 )
	f2 = ( z2 - z1 ) * ( x3 - x1 ) - ( z3 - z1 ) * ( x2 - x1 )
	f3 = ( x2 - x1 ) * ( y3 - y1 ) - ( x3 - x1 ) * ( y2 - y1 )

	return ( ( - aux_lon * f1 - aux_lat * f2 ) / f3 + dc )

def plot_only_topography_deg( Cities , lon1 , lon2 , lat1 , lat2 , step_lat_m , step_lon_m , matrix_lon , matrix_lat , Topography , Topography_Sea ):

	plt.figure( 1 , figsize = ( 8.0 , 5.0 ) )
	plt.axes().set_aspect( step_lat_m / step_lon_m )
	cmapg = plt.cm.get_cmap( 'Greys' )
	cmapr = plt.cm.get_cmap( 'Reds' )
	cmaps = plt.cm.get_cmap( 'Blues' ) 
	CS_Topo = plt.contourf( matrix_lon , matrix_lat , Topography , 100 , alpha = 1.0 , cmap = cmapg , antialiased = True )
	CS_Sea = plt.contourf( matrix_lon , matrix_lat , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )

	plt.xlabel( 'Longitude $[^\circ]$' )
	plt.ylabel( 'Latitude $[^\circ]$' )
	plt.xlim( lon1, lon2 )
	plt.ylim( lat1, lat2 )
	for i in range( len( Cities ) ):
		plt.text( float( Cities[ i ][ 0 ] ), float( Cities[ i ][ 1 ] ), str( Cities[ i ][ 2 ] ), horizontalalignment = 'center' , verticalalignment ='center' , fontsize = 6 )

def plot_only_topography_utm( matrix_east , matrix_north , east_cor , north_cor , n_east , n_north , cellsize , Topography , Topography_Sea ):

	plt.figure( 1 , figsize = ( 8.0 , 5.0 ) )
	plt.axes().set_aspect( 1.0 )
	cmapg = plt.cm.get_cmap( 'Greys' )
	cmapr = plt.cm.get_cmap( 'Reds' )
	cmaps = plt.cm.get_cmap( 'Blues' ) 
	CS_Topo = plt.contourf( matrix_east , matrix_north , Topography , 100 , alpha = 1.0 , cmap = cmapg , antialiased = True )
	CS_Sea = plt.contourf( matrix_east , matrix_north , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )
	plt.xlabel( 'East [m]' )
	plt.ylabel( 'North [m]' )
	plt.xlim( east_cor , east_cor + cellsize * ( n_east - 1 ) )
	plt.ylim( north_cor , north_cor + cellsize * ( n_north - 1 ) )

def plot_only_vent_deg( lon_cen_vector , lat_cen_vector , N ):

	for i in range( 0 , N ):
		plt.plot( lon_cen_vector[ i ] , lat_cen_vector[ i ] , 'r.' , markersize = 2 )

def plot_only_vent_utm( east_cen_vector , north_cen_vector , N ):

	for i in range( 0 , N ):
		plt.plot( east_cen_vector[ i ] , north_cen_vector[ i ] , 'r.' , markersize = 2 )

def plot_only_properties( volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , variable_vector , type_input , calibration_type , limits_calib , probability_save ):

	plt.figure( 1 , figsize = ( 14.0 , 8.0 ) )
	plt.subplot( 231 )
	plt.hist( np.log10( volume_vector ) )
	plt.xlabel( 'log( Collapsing volume [m3] )' )
	plt.subplot( 232 )
	plt.hist( phi_0_vector )
	plt.xlabel( 'Initial concentration' )
	plt.subplot( 233 )
	plt.hist( ws_vector )
	plt.xlabel( 'Sedimentation velocity [m/s]' )
	plt.subplot( 234 )
	plt.hist( Fr_vector )
	plt.xlabel( 'Froude number' )
	plt.subplot( 235 )
	plt.hist( rho_p_vector )
	plt.xlabel( 'Pyroclasts density [kg/m3]' )
	plt.subplot( 236 )
	plt.hist( rho_gas_vector )
	plt.xlabel( 'Gas density [kg/m3]' )
	plt.figure( 2 )
	plt.plot( np.log10( volume_vector ) , phi_0_vector , 'b.' , markersize = 10 )
	plt.xlabel( 'log( Collapsing volume [m3] )' )
	plt.ylabel( 'Initial concentration' )
	plt.grid()
	if( type_input == 3 ):
		plt.xlim( limits_calib[ 0 ] , limits_calib[ 1 ] )
		plt.ylim( limits_calib[ 2 ] , limits_calib[ 3 ] )
		plt.figure( 3 , figsize = ( 8.0 , 5.0 ) )
		dims_prob = probability_save.shape
		xi = np.linspace( limits_calib[ 0 ] , limits_calib[ 1 ] , num = dims_prob[ 0 ] )
		yi = np.linspace( limits_calib[ 2 ] , limits_calib[ 3 ] , num = dims_prob[ 1 ] )
		[ Xi , Yi ] = np.meshgrid( xi , yi )
		c3 = plt.pcolormesh( Xi , Yi , probability_save , cmap = 'viridis' )
		plt.colorbar( c3 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'Sampling probability' )
		if( calibration_type == 5 ):
			plt.figure( 4 , figsize = ( 8.0 , 5.0 ) )
			plt.plot( variable_vector[ : , 0 ] , variable_vector[ : , 1 ] , 'b' )
			plt.xlabel( 'Runout distance [m]' )
			plt.ylabel( 'Sampling probability' )
			plt.ylim( bottom = 0 )
			plt.xlim( left = 0 )
			plt.grid()
		elif( calibration_type == 7 ):
			plt.figure( 4 , figsize = ( 8.0 , 5.0 ) )
			plt.plot( variable_vector[ : , 0 ] , variable_vector[ : , 1 ] , 'b' )
			plt.xlabel( 'Inundation area [km2]' )
			plt.ylabel( 'Sampling probability' )
			plt.ylim( bottom = 0 )
			plt.xlim( left = 0 )
			plt.grid()

def plot_only_comparison_polygon_deg( matrix_lon , matrix_lat , matrix_compare ):

	line_compare = plt.contour( matrix_lon , matrix_lat , matrix_compare[ range( len( matrix_compare[ : , 0 ] ) -1 , -1 , -1 ) , : ], np.array( [ 0 ] ) , colors = 'b' , interpolation = 'linear' )

def plot_only_comparison_polygon_utm( matrix_east , matrix_north , matrix_compare ):

	line_compare = plt.contour( matrix_east , matrix_north , matrix_compare[ range( len( matrix_compare[ : , 0 ] ) -1 , -1 , -1 ) , : ], np.array( [ 0 ] ) , colors = 'b' , interpolation = 'linear' )

def plot_only_map_deg( Cities , lon1 , lon2 , lat1 , lat2 , step_lat_m , step_lon_m , matrix_lon , matrix_lat , lon_cen_vector , lat_cen_vector , Topography , Topography_Sea , N , data_cones ):

	data_cones = data_cones[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ] / N
	line_val = data_cones.max()
	data_cones[ data_cones[ : , : ] == 0 ] = np.nan
	val_up = np.floor( ( line_val + 0.1 - 1.0 / N ) * 10.0 ) / 20.0
	val_down = np.maximum( val_up / 10.0 , 0.05 )
	plt.figure( 1 , figsize = ( 8.0 , 5.0 ) )
	plt.axes().set_aspect( step_lat_m / step_lon_m )
	cmapg = plt.cm.get_cmap( 'Greys' )
	cmapr = plt.cm.get_cmap( 'Reds' )
	cmaps = plt.cm.get_cmap( 'Blues' ) 
	if( N > 1 ):
		CS_Topo = plt.contourf( matrix_lon , matrix_lat , Topography , 1000 , alpha = 1.0 , cmap = cmapg , antialiased = True )
		CS_Sea = plt.contourf( matrix_lon , matrix_lat , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )
		CS = plt.contourf( matrix_lon , matrix_lat , data_cones , 100 , vmin = 0.0 , vmax = 1.0 , alpha = 0.3 , interpolation = 'linear' , cmap = cmapr , antialiased = True )
		fmt = '%.2f'
		plt.colorbar()
		CS_lines = plt.contour( matrix_lon , matrix_lat , data_cones , np.array( [ val_down , val_up ] ) , colors = 'r' , interpolation = 'linear' , linewidths = 1 )
		plt.clabel( CS_lines , inline = 0.1 , fontsize = 10 , colors = 'k' , fmt = fmt )
	else:
		CS_Topo = plt.contourf( matrix_lon , matrix_lat , Topography , 1000 , alpha = 1.0 , cmap = cmapg , antialiased = True )
		CS_Sea = plt.contourf( matrix_lon , matrix_lat , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )
		CS = plt.contourf( matrix_lon , matrix_lat , data_cones , 100 , alpha = 0.3 , cmap = cmapr , antialiased = True )
	plt.xlabel( 'Longitude $[^\circ]$' )
	plt.ylabel( 'Latitude $[^\circ]$' )
	plt.xlim( lon1, lon2 )
	plt.ylim( lat1, lat2 )
	for i in range( len( Cities ) ):
		plt.text( float( Cities[ i ][ 0 ] ) , float( Cities[ i ][ 1 ] ) , str( Cities[ i ][ 2 ] ) , horizontalalignment = 'center' , verticalalignment ='center' , fontsize = 6 )
	for i in range( 0 , N ):
		plt.plot( lon_cen_vector[ i ] , lat_cen_vector[ i ] , 'r.' , markersize = 2 )

def plot_only_map_utm( matrix_east , matrix_north , east_cor , north_cor , n_east , n_north , cellsize , east_cen_vector , north_cen_vector , Topography , Topography_Sea , N , data_cones ):

	data_cones = data_cones[ range( len( data_cones[ : , 0 ] ) -1 , -1 , -1 ) , : ] / N
	line_val = data_cones.max()
	data_cones[ data_cones[ : , : ] == 0 ] = np.nan
	val_up = np.floor( ( line_val + 0.1 - 1.0 / N ) * 10.0 ) / 20.0
	val_down = np.maximum( val_up / 10.0 , 0.05 )
	plt.figure( 1 , figsize = ( 8.0 , 5.0 ) )
	plt.axes().set_aspect( 1.0 )
	cmapg = plt.cm.get_cmap( 'Greys' )
	cmapr = plt.cm.get_cmap( 'Reds' )
	cmaps = plt.cm.get_cmap( 'Blues' ) 
	if( N > 1 ):
		CS_Topo = plt.contourf( matrix_east , matrix_north , Topography , 100 , alpha = 1.0 , cmap = cmapg , antialiased = True )
		CS_Sea = plt.contourf( matrix_east , matrix_north , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )
		CS = plt.contourf( matrix_east , matrix_north , data_cones , 100, vmin = 0.0 , vmax = 1.0 , alpha = 0.3 , interpolation = 'linear' , cmap = cmapr , antialiased = True )
		fmt = '%.2f'
		plt.colorbar()
		CS_lines = plt.contour( matrix_east , matrix_north , data_cones , np.array( [ val_down , val_up ] ) , colors = 'r' , interpolation = 'linear' , linewidths = 1 )
		plt.clabel( CS_lines , inline = 0.1 , fontsize = 10 , colors = 'k' , fmt = fmt )
	else:
		CS_Topo = plt.contourf( matrix_east , matrix_north , Topography , 100 , alpha = 1.0 , cmap = cmapg , antialiased = True )
		CS_Sea = plt.contourf( matrix_east , matrix_north , Topography_Sea , 100 , alpha = 0.5 , cmap = cmaps , antialiased = True )
		CS = plt.contourf( matrix_east , matrix_north , data_cones , 100 , alpha = 0.3 , cmap = cmapr , antialiased = True )
	plt.xlabel( 'East [m]' )
	plt.ylabel( 'North [m]' )
	plt.xlim( east_cor , east_cor + cellsize * ( n_east - 1 ) )
	plt.ylim( north_cor , north_cor + cellsize * ( n_north - 1 ) )
	for i in range( 0 , N ):
		plt.plot( east_cen_vector[ i ] , north_cen_vector[ i ] , 'r.' , markersize = 2 )

def plot_input_output( summary_data ):

	plt.figure( 2 , figsize = ( 14.0 , 10.0 ) )
	plt.subplot( 221 )
	plt.plot( np.log10( summary_data[ : , 0 ] ) , summary_data[ : , 9 ] , 'b.' )
	plt.xlabel( 'log( Collapsing volume [m3] )' )
	plt.ylabel( 'Runout distance [km]' )
	plt.grid()
	plt.subplot( 222 )
	plt.plot( np.log10( summary_data[ : , 0 ] ) , summary_data[ : , 8 ] , 'b.' )
	plt.xlabel( 'log( Collapsing volume [m3] )' )
	plt.ylabel( 'Inundation area [km2]' )
	plt.grid()
	plt.subplot( 223 )
	plt.plot( summary_data[ : , 1 ] , summary_data[ : , 9 ] , 'b.' )
	plt.xlabel( 'Initial concentration' )
	plt.ylabel( 'Runout distance [km]' )
	plt.grid()
	plt.subplot( 224 )
	plt.plot( summary_data[ : , 1 ] , summary_data[ : , 8 ] , 'b.' )
	plt.xlabel( 'Initial concentration' )
	plt.ylabel( 'Inundation area [km2]' )
	plt.grid()
	plt.figure( 3 , figsize = ( 14.0 , 10.0 ) )
	plt.subplot( 221 )
	plt.plot( summary_data[ : , 2 ] , summary_data[ : , 9 ] , 'b.' )
	plt.xlabel( 'Sedimentation velocity [m/s]' )
	plt.ylabel( 'Runout distance [km]' )
	plt.grid()
	plt.subplot( 222 )
	plt.plot( summary_data[ : , 2 ] , summary_data[ : , 8 ] , 'b.' )
	plt.xlabel( 'Sedimentation velocity [m/s]' )
	plt.ylabel( 'Inundation area [km2]' )
	plt.grid()
	plt.subplot( 223 )
	plt.plot( summary_data[ : , 3 ] , summary_data[ : , 9 ] , 'b.' )
	plt.xlabel( 'Froude number' )
	plt.ylabel( 'Runout distance [km]' )
	plt.grid()
	plt.subplot( 224 )
	plt.plot( summary_data[ : , 3 ] , summary_data[ : , 8 ] , 'b.' )
	plt.xlabel( 'Froude number' )
	plt.ylabel( 'Inundation area [km2]' )
	plt.grid()
	plt.figure( 4 , figsize = ( 14.0 , 10.0 ) )
	plt.subplot( 221 )
	plt.plot( summary_data[ : , 4 ] , summary_data[ : , 9 ] , 'b.' )
	plt.xlabel( 'Pyroclasts density [kg/m3]' )
	plt.ylabel( 'Runout distance [km]' )
	plt.grid()
	plt.subplot( 222 )
	plt.plot( summary_data[ : , 4 ] , summary_data[ : , 8 ] , 'b.' )
	plt.xlabel( 'Pyroclasts density [kg/m3]' )
	plt.ylabel( 'Inundation area [km2]' )
	plt.grid()
	plt.subplot( 223 )
	plt.plot( summary_data[ : , 5 ] , summary_data[ : , 9 ] , 'b.' )
	plt.xlabel( 'Gas density [kg/m3]' )
	plt.ylabel( 'Runout distance [km]' )
	plt.grid()
	plt.subplot( 224 )
	plt.plot( summary_data[ : , 5 ] , summary_data[ : , 8 ] , 'b.' )
	plt.xlabel( 'Gas density [kg/m3]' )
	plt.ylabel( 'Inundation area [km2]' )
	plt.grid()
	plt.figure( 5 , figsize = ( 8.0 , 5.0 ) )
	plt.plot( summary_data[ : , 9 ] , summary_data[ : , 8 ] , 'b.' )
	plt.ylabel( 'Inundation area [km2]' )
	plt.xlabel( 'Runout distance [km]' )
	plt.grid()
	
def plot_only_calibration( calibration_data , vertices_compare , N , comparison_polygon ):

	volume_vals = np.log10( calibration_data[ : , 0 ] ) 
	volume_vals_reshaped = volume_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
	phi_0_vals = calibration_data[ : , 1 ]
	phi_0_vals_reshaped = phi_0_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
	dist_vals = calibration_data[ : , 5 ]
	dist_vals_reshaped = dist_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
	area_vals = calibration_data[ : , 8 ]
	area_vals_reshaped = area_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
	plt.figure( 4 , figsize = ( 8.0 , 5.0 ) )
	c4 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , dist_vals_reshaped , cmap = 'viridis' )
	plt.colorbar( c4 )
	plt.xlabel( 'log( Collapsing volume [m3] )' )
	plt.ylabel( 'Initial concentration' )
	plt.title( 'Distance [m]' )
	plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
	plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
	plt.figure( 5 , figsize = ( 8.0 , 5.0 ) )
	c7 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , area_vals_reshaped , cmap = 'viridis' )
	plt.colorbar( c7 )
	plt.xlabel( 'log( Collapsing volume [m3] )' )
	plt.ylabel( 'Initial concentration' )
	plt.title( 'Area [km2]' )
	plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
	plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
	if( not comparison_polygon == '' ):
		Jaccard_vals = calibration_data[ : , 2 ]
		Jaccard_vals_reshaped = Jaccard_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		MSD_vals = calibration_data[ : , 3 ]
		MSD_vals_reshaped = MSD_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		HD_vals = calibration_data[ : , 4 ]
		HD_vals_reshaped = HD_vals.reshape( int( np.sqrt( N ) ) , int( np.sqrt( N ) ) )
		plt.figure( 6 , figsize = ( 8.0 , 5.0 ) )
		c1 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , Jaccard_vals_reshaped , cmap = 'viridis' )
		plt.colorbar( c1 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'Jaccard Index' )
		plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
		plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
		plt.figure( 7 , figsize = ( 8.0 , 5.0 ) )
		c2 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , MSD_vals_reshaped , cmap = 'viridis_r' )
		plt.colorbar( c2 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'RMSD [m]' )
		plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
		plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
		plt.figure( 8 , figsize = ( 8.0 , 5.0 ) )
		c3 = plt.pcolormesh( volume_vals_reshaped , phi_0_vals_reshaped , HD_vals_reshaped , cmap = 'viridis_r' )
		plt.colorbar( c3 )
		plt.xlabel( 'log( Collapsing volume [m3] )' )
		plt.ylabel( 'Initial concentration' )
		plt.title( 'HD [m]' )
		plt.xlim( np.min( np.log10( calibration_data[ : , 0 ] ) ) , np.max( np.log10( calibration_data[ : , 0 ] ) ) )
		plt.ylim( np.min( calibration_data[ : , 1 ] ) , np.max( calibration_data[ : , 1 ] ) )
		
