import elevation
import tifffile
import numpy as np
import matplotlib.pyplot as plt
from BoxMapProb_Functions import read_input , import_map , read_map_utm , read_map_deg , matrix_deg , matrix_utm , create_inputs , create_vent_deg , create_vent_utm , read_comparison_polygon_deg , read_comparison_polygon_utm , initial_definitions , definitions_save_data_deg, definitions_save_data_utm, compute_box_model_deg , compute_box_model_utm , save_data_deg , save_data_utm , plot_deg , plot_utm , calibration
from math import sin , cos , sqrt , atan2 , radians , log , factorial , tan
from scipy import interpolate
import sys
import os
from PIL import Image , ImageDraw
import shutil
import utm
import warnings
warnings.filterwarnings( "ignore" )

def main_program():

	# INPUT PARAMETERS
	print('Reading input file')
	[ current_path , run_name , type_sim , source_dem , topography_file , comparison_polygon , ang_cal , ang_cal_range , lon1 , lon2 , lat1 , lat2 , g , vent_type , lon_cen , lat_cen , east_cen , north_cen , azimuth_lin , length_lin , radius_rad , ang1_rad , ang2_rad , var_cen , dist_input_cen , input_file_vent , type_input , dist_input_volume , volume , var_volume , volume_k , volume_theta , dist_input_phi_0 , phi_0 , var_phi_0 , phi_0_k , phi_0_theta , dist_input_ws , ws , var_ws , ws_k , ws_theta , dist_input_Fr , Fr , var_Fr , Fr_k , Fr_theta , dist_input_rho_p , rho_p , var_rho_p , rho_p_k , rho_p_theta , dist_input_rho_gas , rho_gas , var_rho_gas , rho_gas_k , rho_gas_theta , input_file_cal , calibration_type , dist_distance_calibration , distance_calibration , var_distance_calibration , distance_calibration_k , distance_calibration_theta , file_cumulative_distance , dist_area_calibration , area_calibration , var_area_calibration , area_calibration_k , area_calibration_theta , file_cumulative_area , max_levels , N , save_data , redist_volume , plot_flag , sea_flag ] = read_input()

	# IMPORT MAP AND READ MAP
	if( source_dem == 1 ):
		print('Importing map')
		[ lon1 , lon2 , lat1 , lat2 , Cities , Topography , Topography_Sea , cells_lon , cells_lat ] = import_map( current_path , run_name , lon1 , lon2 , lat1 , lat2 , plot_flag , sea_flag )
	elif( source_dem == 2 ):
		print( 'Reading map' )
		[ Topography , Topography_Sea , n_north , n_east , cellsize , east_cor , north_cor ] = read_map_utm( current_path , topography_file , plot_flag , sea_flag )
	else:
		print( 'Reading map' )
		[ lon1 , lon2 , lat1 , lat2 , Cities , Topography , Topography_Sea , cells_lon , cells_lat ] = read_map_deg( current_path , topography_file , plot_flag , sea_flag )

	# DEFINE THE MATRIX OF COORDINATES
	if( source_dem == 1 or source_dem == 3 ):
		[ matrix_lon , matrix_lat , step_lon_m , step_lat_m , step_lon_deg , step_lat_deg , utm_save ] = matrix_deg( lon1 , lon2 , lat1 , lat2 , cells_lon , cells_lat )
		resolution_factor = np.sqrt( step_lon_m * step_lat_m )
	else:
		[ matrix_north , matrix_east , utm_save ] = matrix_utm( n_north , n_east , cellsize , east_cor , north_cor )
		resolution_factor = cellsize

	# CREATE VECTORS OF INPUT PARAMETERS
	print('Creating input vectors')
	[ volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , N , variable_vector , limits_calib , Probability_Save ] = create_inputs( type_sim , type_input , dist_input_volume , dist_input_phi_0 , dist_input_ws , dist_input_Fr , dist_input_rho_p , dist_input_rho_gas , input_file_cal , volume , var_volume , volume_k , volume_theta , phi_0 , var_phi_0 , phi_0_k , phi_0_theta , ws , var_ws , ws_k , ws_theta , Fr , var_Fr , Fr_k , Fr_theta , rho_p , var_rho_p , rho_p_k , rho_p_theta , rho_gas , var_rho_gas , rho_gas_k , rho_gas_theta , calibration_type , dist_distance_calibration , distance_calibration , var_distance_calibration , distance_calibration_k , distance_calibration_theta , file_cumulative_distance , dist_area_calibration , area_calibration , var_area_calibration , area_calibration_k , area_calibration_theta , file_cumulative_area , N , 0 )

	# CREATE VECTORS OF VENT POSITION
	if( source_dem == 1 or source_dem == 3 ):
		[ lon_cen_vector , lat_cen_vector , N ] = create_vent_deg( vent_type , input_file_vent , lon_cen , lat_cen , var_cen , azimuth_lin, length_lin , radius_rad , ang1_rad , ang2_rad , step_lon_deg , step_lat_deg , step_lon_m , step_lat_m , dist_input_cen , N )
	else:
		[ east_cen_vector , north_cen_vector , N ] = create_vent_utm( vent_type , input_file_vent , east_cen , north_cen , var_cen , azimuth_lin, length_lin , radius_rad , ang1_rad , ang2_rad , dist_input_cen , N )

	# READ COMPARISON POLYGON
	if( type_sim == 2 ):
		print('Reading polygon for comparison')
		if( source_dem == 1 or source_dem == 3 ):
			[ matrix_compare , vertices_compare , string_compare , data_direction ] = read_comparison_polygon_deg( comparison_polygon , input_file_cal , ang_cal , ang_cal_range , lon1 , lon2 , lat1 , lat2 , lon_cen , lat_cen , step_lat_m , step_lon_m , cells_lon , cells_lat , matrix_lon , matrix_lat , step_lon_deg , step_lat_deg , N )
		else:
			[ matrix_compare , vertices_compare , string_compare , data_direction ] = read_comparison_polygon_utm( comparison_polygon , input_file_cal , ang_cal , ang_cal_range , east_cor , north_cor , east_cen , north_cen , cellsize , n_east , n_north , matrix_east , matrix_north , N )
	else:
		[ matrix_compare , vertices_compare , string_compare , data_direction ] = [ np.nan , np.nan , np.nan , np.nan ]

	# CONOIDS
	[ angstep , distep , anglen , pix_min , angstep_res2 , angstep_res3 , anglen_res2 , anglen_res3 , vector_correc , vector_backward_1 , vector_backward_2 , index_max] = initial_definitions( redist_volume )
	if( save_data == 1 or type_sim == 2 ):
		if( source_dem == 1 or source_dem == 3 ):
			[ summary_data , area_pixel , sim_data , string_data , string_cones ] = definitions_save_data_deg( source_dem , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , lon_cen_vector , lat_cen_vector , step_lon_m , step_lat_m , N , max_levels )
		else:
			[ summary_data , area_pixel , sim_data , string_data , string_cones ] = definitions_save_data_utm( source_dem , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , east_cen_vector , north_cen_vector , cellsize , N , max_levels )
	else:
		[ summary_data , area_pixel , sim_data , string_data , string_cones ] = [ np.nan , np.nan , np.nan , np.nan , np.nan ]

	if( source_dem == 1 or source_dem == 3 ):
		[ summary_data , string_data , string_cones , string_compare , sim_data , data_cones , polygon ] = compute_box_model_deg( type_sim , lon1 , lon2 , lat1 , lat2 , step_lon_deg , step_lat_deg , step_lon_m , step_lat_m , lon_cen_vector , lat_cen_vector , matrix_lon , matrix_lat , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , g , cells_lon , cells_lat , Topography , angstep , angstep_res2 , angstep_res3 , distep , area_pixel , max_levels , N , redist_volume , save_data , summary_data , string_data , string_cones , sim_data , anglen , pix_min , vector_backward_1 , vector_backward_2 , index_max , vector_correc , matrix_compare , vertices_compare , string_compare , data_direction , comparison_polygon )
	else:
		[ summary_data , string_data , string_cones , string_compare , sim_data , data_cones , polygon ] = compute_box_model_utm( type_sim , n_north , n_east , east_cor , north_cor , east_cen_vector , north_cen_vector , matrix_north , matrix_east , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , g , cellsize , Topography , angstep , angstep_res2 , angstep_res3 , distep , area_pixel , max_levels , N , redist_volume , save_data , summary_data , string_data , string_cones , sim_data , anglen , pix_min , vector_backward_1 , vector_backward_2 , index_max , vector_correc , matrix_compare , vertices_compare , string_compare , data_direction , comparison_polygon )

	# SAVE DATA
	if( save_data == 1 and not np.isnan( data_cones ).any( ) ):
		print('Saving data')
		if( source_dem == 1 or source_dem == 3 ):
			save_data_deg( run_name , source_dem , sea_flag , lon1 , lon2 , lat1 , lat2 , step_lon_m , step_lat_m , cells_lon , cells_lat , matrix_lon , matrix_lat , Topography , Topography_Sea , N , summary_data , string_data , string_cones , sim_data , data_cones, utm_save , 0 )
		else:
			save_data_utm( run_name , sea_flag , n_north , n_east , cellsize , matrix_east , matrix_north , Topography , Topography_Sea , N , summary_data , string_data , string_cones , string_compare , sim_data , data_cones , utm_save , 0 )
		if( type_sim == 2 ):
			calibration( run_name , string_compare , resolution_factor , ws_vector[ 0 ] , Fr_vector[ 0 ] , rho_p_vector[ 0 ] , rho_gas_vector[ 0 ] )

	if( plot_flag == 1 and not np.isnan( data_cones ).any( ) ):
		if( source_dem == 1 or source_dem == 3 ):
			plot_deg( run_name , type_sim , Cities , polygon , lon1 , lon2 , lat1 , lat2 , step_lat_m , step_lon_m , matrix_lon , matrix_lat , lon_cen_vector , lat_cen_vector , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , Topography , Topography_Sea , N , data_cones , matrix_compare , ang_cal_range , data_direction , string_compare , comparison_polygon )
		else:
			plot_utm( run_name , type_sim , polygon , matrix_east , matrix_north , east_cor , north_cor , n_east , n_north , cellsize , east_cen_vector , north_cen_vector , volume_vector , phi_0_vector , ws_vector , Fr_vector , rho_p_vector , rho_gas_vector , Topography , Topography_Sea , N , data_cones , matrix_compare , ang_cal_range , data_direction , string_compare , comparison_polygon )

main_program()
