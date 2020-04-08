import elevation
import tifffile
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians, log, factorial, tan, cosh, atanh
import sys
import os
from PIL import Image, ImageDraw
import shutil
import utm
import warnings
warnings.filterwarnings("ignore")

# Auxiliary functions

def distance_two_points(lat1, lat2, lon1, lon2):

	R = 6373.0

	lat1 = radians(lat1)
	lon1 = radians(lon1)
	lat2 = radians(lat2)
	lon2 = radians(lon2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2.0) ** 2.0 + cos(lat1) * cos(lat2) * sin(dlon / 2.0) ** 2.0
	c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a))
	return ( R * c ) * 1000.0

def interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, lon_cen, lat_cen, cells_lon, cells_lat, Topography):

	dlon = int(np.floor( (lon_cen - lon1 )/ (step_lon_deg) ))
	dlat = (cells_lat - 2) - int(np.floor( (lat_cen - lat1) / (step_lat_deg) ))

	if(dlon >= ( cells_lon - 1.0 ) or dlat >= ( cells_lat - 1.0 ) or dlon < 0.0 or dlat < 0.0):
		return 99999

	aux_lon = 2.0 * ( lon_cen - ( dlon * step_lon_deg + lon1 ) - step_lon_deg / 2.0 ) / step_lon_deg
	aux_lat = 2.0 *( - lat_cen + ( (cells_lat - 1.0 - dlat) * step_lat_deg + lat1 ) - step_lat_deg / 2.0 ) / step_lat_deg

	dc = ( Topography[dlat][dlon] + Topography[dlat][dlon+1] + Topography[dlat+1][dlon] + Topography[dlat+1][dlon+1] ) / 4
	[x3, y3, z3] = [0.0, 0.0, dc]

	if( aux_lon >= 0.0 and abs(aux_lon) >= abs(aux_lat) ):
		[x1,y1,z1] = [1.0, 1.0, Topography[dlat+1][dlon+1]] 
		[x2,y2,z2] = [1.0, -1.0, Topography[dlat][dlon+1]] 
	elif( aux_lat >= 0.0 and abs(aux_lon) < abs(aux_lat) ):
		[x1,y1,z1] = [-1.0, 1.0, Topography[dlat+1][dlon]] 
		[x2,y2,z2] = [1.0, 1.0, Topography[dlat+1][dlon+1]] 
	elif( aux_lon < 0.0 and abs(aux_lon) >= abs(aux_lat) ):
		[x1,y1,z1] = [-1.0, 1.0, Topography[dlat+1][dlon]] 
		[x2,y2,z2] = [-1.0, -1.0, Topography[dlat][dlon]] 
	else:
		[x1,y1,z1] = [-1.0, -1.0, Topography[dlat][dlon]] 
		[x2,y2,z2] = [1.0, -1.0, Topography[dlat][dlon+1]]
 
	f1 = (y2-y1)*(z3-z1) - (y3-y1)*(z2-z1)
	f2 = (z2-z1)*(x3-x1) - (z3-z1)*(x2-x1)
	f3 = (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)

	return ((- aux_lon * f1 - aux_lat * f2) / f3 + dc)

##########################################################################################################################
################################################### MAIN PROGRAM #########################################################
##########################################################################################################################

# INPUT PARAMETERS

print('Reading input file')

current_path = os.getcwd()
try:
	file_txt = open('input_data.py')
except:
	print('input_data.py not found in ' + str(current_path))
	sys.exit(0)
line = file_txt.readlines()
file_txt.close()

[run_name, source_dem, lon1, lon2, lat1, lat2, g, topography_file] = ['run_default', 1, np.nan, np.nan, np.nan, np.nan, 9.8, 'Topography_3.txt']
[dist_source, var_cen, lon_cen, lat_cen, east_cen, north_cen, azimuth_lin] = [1, 0.0, np.nan, np.nan, np.nan, np.nan, np.nan]
[length_lin, radius_rad, ang1_rad, ang2_rad] = [np.nan, np.nan, np.nan, np.nan]
[volume, ws, phi_0, Fr, rho_p, rho_gas, var_volume, var_ws, var_phi_0, var_Fr, var_rho_p,  var_rho_gas, N, max_levels, save_data, dist_input, redist_volume, plot_flag, sea_flag] = [np.nan, 2.0, 0.02, 1.0, 1800.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 100, 1, 0, 1, 4, 1, 0]

for i in range(0,len(line)):
	line[i] = line[i].replace('=',' ')
	aux = line[i].split()
	if(len(aux) > 0):
		if( aux[0][0] != '#'):
			if( aux[0] == 'run_name'):
				run_name = aux[1]
			if( aux[0] == 'topography_file'):
				topography_file = aux[1]
				topography_file = topography_file.replace("'","")
			if( aux[0] == 'source_dem'):
				source_dem = int(aux[1])
			if( aux[0] == 'lon1'):
				lon1 = float(aux[1])
			if( aux[0] == 'lon2'):
				lon2 = float(aux[1])
			if( aux[0] == 'lat1'):
				lat1 = float(aux[1])
			if( aux[0] == 'lat2'):
				lat2 = float(aux[1])
			if( aux[0] == 'dist_source'):
				dist_source = int(aux[1])
			if( aux[0] == 'var_cen'):
				var_cen = float(aux[1])
			if( aux[0] == 'lon_cen'):
				lon_cen = float(aux[1])
			if( aux[0] == 'lat_cen'):
				lat_cen = float(aux[1])
			if( aux[0] == 'east_cen'):
				east_cen = float(aux[1])
			if( aux[0] == 'north_cen'):
				north_cen = float(aux[1])
			if( aux[0] == 'azimuth_lin'):
				azimuth_lin = float(aux[1])
			if( aux[0] == 'length_lin'):
				length_lin = float(aux[1])
			if( aux[0] == 'radius_rad'):
				radius_rad = float(aux[1])
			if( aux[0] == 'ang1_rad'):
				ang1_rad = float(aux[1])
			if( aux[0] == 'ang2_rad'):
				ang2_rad = float(aux[1])
			if( aux[0] == 'volume'):
				volume = float(aux[1])
			if( aux[0] == 'ws'):
				ws = float(aux[1])
			if( aux[0] == 'phi_0'):
				phi_0 = float(aux[1])
			if( aux[0] == 'Fr'):
				Fr = float(aux[1])
			if( aux[0] == 'rho_gas'):
				rho_gas = float(aux[1])
			if( aux[0] == 'rho_p'):
				rho_p = float(aux[1])
			if( aux[0] == 'var_volume'):
				var_volume = float(aux[1])
			if( aux[0] == 'var_ws'):
				var_ws = float(aux[1])
			if( aux[0] == 'var_phi_0'):
				var_phi_0 = float(aux[1])
			if( aux[0] == 'var_Fr'):
				var_Fr = float(aux[1])
			if( aux[0] == 'var_rho_p'):
				var_rho_p = float(aux[1])
			if( aux[0] == 'var_rho_gas'):
				var_rho_gas = float(aux[1])
			if( aux[0] == 'N'):
				N = int(aux[1])
			if( aux[0] == 'max_levels'):
				max_levels = int(aux[1])
			if( aux[0] == 'save_data'):
				save_data = int(aux[1])
			if( aux[0] == 'dist_input'):
				dist_input = int(aux[1])
			if( aux[0] == 'redist_volume'):
				redist_volume = int(aux[1])
			if( aux[0] == 'plot_flag'):
				plot_flag = int(aux[1])
			if( aux[0] == 'sea_flag'):
				sea_flag = int(aux[1])

try:
	os.mkdir('Results')
except:
	pass
try:
	os.mkdir('Results/' + run_name)
except:
	pass
shutil.copyfile('input_data.py', 'Results/' + run_name + '/input_data.py') 
file_log = open('Results/' + run_name + '/log.txt','w')
file_log.write('0')
file_log.close()

if(source_dem == 1 and ( np.isnan( lon1 ) or np.isnan( lon2 ) or np.isnan( lat1 ) or np.isnan( lat2 ) or np.isnan( lon_cen ) or np.isnan( lat_cen )  ) ):
	print('Problems with input parameters')
	sys.exit(0)
if(source_dem == 2 and ( np.isnan( east_cen ) or np.isnan( north_cen ) ) ):
	print('Problems with input parameters')
	sys.exit(0)
if(source_dem == 3 and ( np.isnan( lon_cen ) or np.isnan( lat_cen )  ) ):
	print('Problems with input parameters')
	sys.exit(0)


# IMPORT MAP
if(source_dem == 1):
	print('Importing map')
	aux_lon = np.array([lon1, lon2])
	aux_lat = np.array([lat1, lat2])
	lon1 = min(aux_lon)
	lon2 = max(aux_lon)
	lat1 = min(aux_lat)
	lat2 = max(aux_lat)

	file_txt = open('Cities.txt')
	line = file_txt.readlines()
	file_txt.close()

	for population in range(10000,10000000,10000):
		Cities = []
		for i in range(1,len(line)):
			aux = line[i].split(',')
			pop = float(aux[4])
			lat_dat = float(aux[5])
			lon_dat = float(aux[6])
			if( lon_dat > lon1 and lon_dat < lon2 and lat_dat > lat1 and lat_dat < lat2 and pop > population):
				Cities.append([lon_dat, lat_dat, aux[2]])
		if(len(Cities) <= 5):
			break

	elevation.clip(bounds=(lon1, lat1, lon2, lat2), output=current_path + '/' + run_name + '.tif')

# READ MAP
if(source_dem == 1):
	print('Processing map')
	fp = run_name + '.tif'
	image = tifffile.imread(fp)
	elevation.clean()
	Topography = np.array(image)

	Topography_Sea = Topography + 0.0
	Topography_Sea[ Topography_Sea[:,:] <= 0] = -1.0 * np.sqrt(-1.0 * Topography_Sea[ Topography_Sea[:,:] <= 0])
	Topography_Sea[ Topography_Sea[:,:] > 0] =  np.nan
	Topography_Sea = Topography_Sea * -1.0

	Topography  = (Topography  + abs(Topography)) / 2.0
	cells_lon = Topography.shape[1]
	cells_lat = Topography.shape[0]

if(source_dem == 2):
	print('Reading map')
	try:
		file_txt = open(topography_file)
	except:
		print(topography_file +' not found in ' + str(current_path))
		sys.exit(0)
	line = file_txt.readlines()
	file_txt.close()

	n_north = -1
	n_east = -1
	cellsize = -1
	indexini = -1
	nodata = -9999

	for i in range(0,10):
		aux = line[i].split()
		if(aux[0] == 'nrows'):
			n_north = int(aux[1])
		if(aux[0] == 'ncols'):
			n_east = int(aux[1])
		if(aux[0] == 'cellsize'):
			cellsize = float(aux[1])
		if(aux[0] == 'xllcorner'):
			east_cor = float(aux[1])
		if(aux[0] == 'yllcorner'):
			north_cor = float(aux[1])
		if(aux[0] == 'NODATA_value'):
			nodata = float(aux[1])
		if(len(aux) >= 10):
			indexini = i
			break

	Topography = np.zeros((n_north,n_east))
	for i in range(indexini, indexini + n_north):
		aux = line[i].split()
		for j in range(0, n_east):
			Topography[i-indexini,j] = float(aux[j])

	Topography_Sea = Topography + 0.0
	Topography_Sea[ Topography_Sea[:,:] <= 0] = -1.0 * np.sqrt(-1.0 * Topography_Sea[ Topography_Sea[:,:] <= 0])
	Topography_Sea[ Topography_Sea[:,:] > 0] =  np.nan
	Topography_Sea = Topography_Sea * -1.0
	Topography  = (Topography  + abs(Topography)) / 2.0

if(source_dem == 3):
	print('Reading map')
	try:
		file_txt = open(topography_file)
	except:
		print(topography_file +' not found in ' + str(current_path))
		sys.exit(0)
	line = file_txt.readlines()
	file_txt.close()

	lon1 = -1
	lon2 = -1
	lat1 = -1
	lat2 = -1
	cells_lat = -1
	cells_lon = -1

	for i in range(0,10):
		aux = line[i].split()
		if(aux[0] == 'lon1'):
			lon1 = float(aux[1])
		if(aux[0] == 'lon2'):
			lon2 = float(aux[1])
		if(aux[0] == 'lat1'):
			lat1 = float(aux[1])
		if(aux[0] == 'lat2'):
			lat2 = float(aux[1])
		if(aux[0] == 'cells_lon'):
			cells_lon = int(aux[1])
		if(aux[0] == 'cells_lat'):
			cells_lat = int(aux[1])
		if(len(aux) >= 10):
			indexini = i
			break

	Topography = np.zeros((cells_lat,cells_lon))
	for i in range(indexini, indexini + cells_lat):
		aux = line[i].split()
		for j in range(0, cells_lon):
			Topography[i-indexini,j] = float(aux[j])

	Topography_Sea = Topography + 0.0
	Topography_Sea[ Topography_Sea[:,:] <= 0] = -1.0 * np.sqrt(-1.0 * Topography_Sea[ Topography_Sea[:,:] <= 0])
	Topography_Sea[ Topography_Sea[:,:] > 0] =  np.nan
	Topography_Sea = Topography_Sea * -1.0
	Topography  = (Topography  + abs(Topography)) / 2.0

	file_txt = open('Cities.txt')
	line = file_txt.readlines()
	file_txt.close()

	for population in range(10000,10000000,10000):
		Cities = []
		for i in range(1,len(line)):
			aux = line[i].split(',')
			pop = float(aux[4])
			lat_dat = float(aux[5])
			lon_dat = float(aux[6])
			if( lon_dat > lon1 and lon_dat < lon2 and lat_dat > lat1 and lat_dat < lat2 and pop > population):
				Cities.append([lon_dat, lat_dat, aux[2]])
		if(len(Cities) <= 5):
			break

# DEFINE THE MATRIX OF COORDINATES
if(source_dem == 1 or source_dem == 3):

	utm1 = utm.from_latlon(lat1,lon1)
	utm2 = utm.from_latlon(lat2,lon2)

	if( utm1[2] == utm2[2] and utm1[3] == utm2[3] ):
		distance_lon = abs(utm2[0] - utm1[0])
		distance_lat = abs(utm2[1] - utm1[1])
	else:
		distance_lon = distance_two_points(lat1,lat1,lon1,lon2)
		distance_lat = distance_two_points(lat1,lat2,lon1,lon1)

	utm_save = utm.from_latlon( min(lat1, lat2), min(lon1, lon2) )

	step_lon_m = distance_lon / (cells_lon-1)
	step_lat_m = distance_lat / (cells_lat-1)

	matrix_lon = np.zeros((cells_lat,cells_lon))
	matrix_lat = np.zeros((cells_lat,cells_lon))

	for i in range(0,cells_lon): 
		matrix_lon[:,i] = lon1 + (lon2 - lon1)*(i)/(cells_lon-1)
	for j in range(0,cells_lat):
		matrix_lat[j,:] = lat1 + (lat2 - lat1)*(cells_lat-1-j)/(cells_lat-1)

	step_lon_deg = (lon2 - lon1)/(cells_lon - 1)
	step_lat_deg = (lat2 - lat1)/(cells_lat - 1)

if(source_dem == 2):
	matrix_north = np.zeros((n_north,n_east))
	matrix_east = np.zeros((n_north,n_east))

	for i in range(0,n_east):
		matrix_east[:,i] = (east_cor + cellsize * i)
	for j in range(0,n_north):
		matrix_north[j,:] = (north_cor + cellsize * j)
	matrix_north = matrix_north[ range(len(matrix_north[:,0]) -1 , -1 , -1 ) , : ]
	utm_save = [east_cor , north_cor]

# CREATE VECTORS OF INPUT PARAMETERS AND DELETE NEGATIVE DATA
print('Creating input vectors')

if(var_volume > 0.0):
	if(dist_input == 1):
		volume_vector = np.random.normal(volume, var_volume, N)
	else:
		volume_vector = np.random.uniform(volume - var_volume, volume + var_volume, N)
else:
	volume_vector = np.ones(N) * volume

if(var_ws > 0.0):
	if(dist_input == 1):
		ws_vector = np.random.normal(ws,var_ws,N)
	else:
		ws_vector = np.random.uniform(ws - var_ws, ws + var_ws, N)
else:
	ws_vector = np.ones(N) * ws

if(var_phi_0 > 0.0):
	if(dist_input == 1):
		phi_0_vector = np.random.normal(phi_0,var_phi_0,N)
	else:
		phi_0_vector = np.random.uniform(phi_0 - var_phi_0, phi_0 + var_phi_0, N)
else:
	phi_0_vector = np.ones(N) * phi_0

if(var_Fr > 0.0):
	if(dist_input == 1):
		Fr_vector = np.random.normal(Fr, var_Fr, N)
	else:
		Fr_vector = np.random.uniform(Fr - var_Fr, Fr + var_Fr, N)
else:
	Fr_vector = np.ones(N) * Fr

if(var_rho_p > 0.0):
	if(dist_input == 1):
		rho_p_vector = np.random.normal(rho_p, var_rho_p, N)
	else:
		rho_p_vector = np.random.uniform(rho_p - var_rho_p, rho_p + var_rho_p, N)
else:
	rho_p_vector = np.ones(N) * rho_p

if(var_rho_gas > 0.0):
	if(dist_input == 1):
		rho_gas_vector = np.random.normal(rho_gas, var_rho_gas, N)
	else:
		rho_gas_vector = np.random.uniform(rho_gas - var_rho_gas, rho_gas + var_rho_gas, N)
else:
	rho_gas_vector = np.ones(N) * rho_gas

if(var_volume > 0.0):
	while( 1 == 1 ):
		aux_boolean = 0
		for i in range(0,N):
			if(volume_vector[i] < 0):
				if(dist_input == 1):
					volume_vector[i] = np.random.normal(volume,var_volume, 1)
				elif(dist_input == 2):
					volume_vector[i] = np.random.uniform(volume - var_volume, volume + var_volume, 1)
				aux_boolean = 1
		if(aux_boolean == 0):
			break

if(var_ws > 0.0):
	while( 1 == 1 ):
		aux_boolean = 0
		for i in range(0,N):
			if(ws_vector[i] < 0):
				if(dist_input == 1):
					ws_vector[i] = np.random.normal(ws,var_ws,1)
				elif(dist_input == 2):
					ws_vector[i] = np.random.uniform(ws - var_ws, ws + var_ws, 1)
				aux_boolean = 1
		if(aux_boolean == 0):
			break

if(var_phi_0 > 0.0):
	while( 1 == 1 ):
		aux_boolean = 0
		for i in range(0,N):
			if(phi_0_vector[i] < 0):
				if(dist_input == 1):
					phi_0_vector[i] = np.random.normal(phi_0 , var_phi_0,1)
				elif(dist_input == 2):
					phi_0_vector[i] = np.random.uniform(phi_0 - var_phi_0, phi_0 + var_phi_0, 1)
				aux_boolean = 1
		if(aux_boolean == 0):
			break

if(var_Fr > 0.0):
	while( 1 == 1 ):
		aux_boolean = 0
		for i in range(0,N):
			if(Fr_vector[i] < 0):
				if(dist_input == 1):
					Fr_vector[i] = np.random.normal(Fr , var_Fr ,1)
				elif(dist_input == 2):
					Fr_vector[i] = np.random.uniform(Fr - var_Fr , Fr + var_Fr , 1)
				aux_boolean = 1
		if(aux_boolean == 0):
			break

if(var_rho_p > 0.0):
	while( 1 == 1 ):
		aux_boolean = 0
		for i in range(0,N):
			if(rho_p_vector[i] < 0):
				if(dist_input == 1):
					rho_p_vector[i] = np.random.normal(rho_p , var_rho_p ,1)
				elif(dist_input == 2):
					rho_p_vector[i] = np.random.uniform(rho_p - var_rho_p , rho_p + var_rho_p , 1)
				aux_boolean = 1
		if(aux_boolean == 0):
			break

if(var_rho_gas > 0.0):
	while( 1 == 1 ):
		aux_boolean = 0
		for i in range(0,N):
			if(rho_gas_vector[i] < 0):
				if(dist_input == 1):
					rho_gas_vector[i] = np.random.normal(rho_gas , var_rho_gas ,1)
				elif(dist_input == 2):
					rho_gas_vector[i] = np.random.uniform(rho_gas - var_rho_gas , rho_gas + var_rho_gas , 1)
				aux_boolean = 1
		if(aux_boolean == 0):
			break

if(source_dem == 1 or source_dem == 3):
	if( var_cen > 0.0 ):
		if(dist_input == 1):
			lon_cen_vector = np.random.normal(lon_cen, var_cen * step_lon_deg / step_lon_m, N)
			lat_cen_vector = np.random.normal(lat_cen, var_cen * step_lat_deg / step_lat_m, N)
		elif(dist_input == 2):
			lon_cen_vector = np.random.uniform(lon_cen - var_cen * step_lon_deg / step_lon_m, lon_cen + var_cen * step_lon_deg / step_lon_m, N)
			lat_cen_vector = np.random.uniform(lat_cen - var_cen * step_lat_deg / step_lat_m, lat_cen + var_cen * step_lat_deg / step_lat_m, N)

			while( 1 == 1 ):
				aux_boolean = 0
				for i in range(0,N):
					if(np.power((lon_cen_vector[i] - lon_cen) * step_lon_m / step_lon_deg ,2) + np.power((lat_cen_vector[i] - lat_cen) * step_lat_m / step_lat_deg , 2) > np.power(var_cen,2)):
						lon_cen_vector[i]  = np.random.uniform(lon_cen - var_cen * step_lon_deg / step_lon_m, lon_cen + var_cen * step_lon_deg / step_lon_m, 1)
						lat_cen_vector[i]  = np.random.uniform(lat_cen - var_cen * step_lat_deg / step_lat_m, lat_cen + var_cen * step_lat_deg / step_lat_m, 1)
						aux_boolean = 1
				if(aux_boolean == 0):
					break
	else:
		lon_cen_vector = np.ones(N) * lon_cen
		lat_cen_vector = np.ones(N) * lat_cen

	if(dist_source == 2):
		pos_structure = np.random.uniform(-1,1,N)
		lon_cen_vector = lon_cen_vector + pos_structure * np.sin(azimuth_lin * np.pi/180) * length_lin *  step_lon_deg / step_lon_m
		lat_cen_vector = lat_cen_vector + pos_structure * np.cos(azimuth_lin * np.pi/180) * length_lin * step_lat_deg / step_lat_m

	if(dist_source == 3):
		pos_structure = ang1_rad + np.random.uniform(0,1,N) * (ang2_rad - ang1_rad)
		lon_cen_vector = lon_cen_vector + np.cos(pos_structure * np.pi/180) * radius_rad  *  step_lon_deg / step_lon_m
		lat_cen_vector = lat_cen_vector + np.sin(pos_structure * np.pi/180) * radius_rad * step_lat_deg / step_lat_m

if(source_dem == 2):

	if( var_cen > 0.0):
		if(dist_input == 1):
			east_cen_vector = np.random.normal(east_cen,var_cen,N)
			north_cen_vector = np.random.normal(north_cen,var_cen,N)
		elif(dist_input == 2):
			east_cen_vector = np.random.uniform(east_cen - var_cen, east_cen + var_cen, N)
			north_cen_vector = np.random.uniform(north_cen - var_cen, north_cen + var_cen,N)
			while( 1 == 1 ):
				aux_boolean = 0
				for i in range(0,N):
					if(np.power((east_cen_vector[i] - east_cen) ,2) + np.power((north_cen_vector[i] - north_cen) , 2) > np.power(var_cen,2)):
						east_cen_vector[i]  = np.random.uniform(east_cen - var_cen , east_cen + var_cen , 1)
						north_cen_vector[i]  = np.random.uniform(north_cen - var_cen, north_cen + var_cen , 1)
						aux_boolean = 1
				if(aux_boolean == 0):
					break
	else:
		east_cen_vector = np.ones(N) * east_cen
		north_cen_vector = np.ones(N) * north_cen

	if(dist_source == 2):
		pos_structure = np.random.uniform(-1,1,N)
		east_cen_vector = east_cen_vector + pos_structure * np.sin(azimuth_lin * np.pi/180) * length_lin
		north_cen_vector = north_cen_vector + pos_structure * np.cos(azimuth_lin * np.pi/180) * length_lin

	if(dist_source == 3):
		pos_structure = ang1_rad + np.random.uniform( 0 , 1 , N ) * ( ang2_rad - ang1_rad )
		east_cen_vector = east_cen_vector  + np.cos(pos_structure * np.pi/180 ) * radius_rad 
		north_cen_vector = north_cen_vector + np.sin(pos_structure * np.pi/180 ) * radius_rad

# BOX MODEL
print('Computing box-model')

angstep = 10
distep = 10
anglen = 360 / angstep
pix_min = 0.0
val_resolution = 3
angstep_res2 = 2
angstep_res3 = 0.4
anglen_res2 = 360 / angstep_res2
anglen_res3 = 360 / angstep_res3

if( redist_volume == 3 or redist_volume == 4 ):
	factor_mult = 50.0
	center_elim = 0.5
	aux_backward = 1 / (1 + np.exp(factor_mult * (np.linspace(0.0, 1.0, anglen/2 + 1) - center_elim) ) )
	vector_backward_1 = np.zeros(int(anglen))
	vector_backward_1[0:int(anglen/2 - 1)] = aux_backward[int(anglen/2-1):0:-1]
	vector_backward_1[int(anglen/2-1):] = aux_backward[:]
	vector_backward_1[vector_backward_1 < 1e-3] = 0
	vector_backward_1[vector_backward_1 > 1.0 - 1e-3] = 1.0
	aux_backward = 1 / (1 + np.exp(factor_mult * (np.linspace(1.0/(anglen/2), 1.0 - 1.0/(anglen/2), anglen/2 ) - center_elim) ) )
	vector_backward_2 = np.zeros(int(anglen))
	vector_backward_2[0:int(anglen/2)] = aux_backward[::-1]
	vector_backward_2[int(anglen/2):] = aux_backward[:]
	vector_backward_2[vector_backward_2 < 1e-3] = 0
	vector_backward_2[vector_backward_2 > 1.0 - 1e-3] = 1.0
	index_max = int(anglen/2 - 1)

if( save_data == 1 ):
	summary_data = np.zeros((N, 11))
	summary_data[:,0] = volume_vector
	summary_data[:,1] = ws_vector
	summary_data[:,2] = phi_0_vector
	summary_data[:,3] = Fr_vector
	summary_data[:,4] = rho_p_vector
	summary_data[:,5] = rho_gas_vector
	if( source_dem == 1 or source_dem == 3):
		summary_data[:,6] = lon_cen_vector
		summary_data[:,7] = lat_cen_vector
		area_pixel = step_lon_m * step_lat_m * 1e-6
		sim_data = str(N) + "\n" + str(step_lon_m) + "\n" + str(step_lat_m) + "\n" + str(source_dem) + "\n" + str(max_levels) + "\n"
	elif( source_dem == 2 ):
		summary_data[:,6] = east_cen_vector
		summary_data[:,7] = north_cen_vector
		area_pixel = cellsize * cellsize * 1e-6
		sim_data = str(N) + "\n" + str(cellsize) + "\n" + str(cellsize) + "\n" + str(source_dem) + "\n" + str(max_levels) + "\n"
	string_data = ""
	if(N == 1):
		string_cones = ""

if(source_dem == 1 or source_dem == 3):

	data_cones = np.zeros((cells_lat,cells_lon))
	data_aux_t = np.ones((cells_lat,cells_lon))
	data_aux_b = np.zeros((cells_lat,cells_lon))
	vec_ang = range(0, 360, angstep)
	vec_ang_res2 = np.arange(0, 360, angstep_res2)
	vec_ang_res3 = np.arange(0, 360, angstep_res3)

	for i in range(0,N):

		runout_min = -1
		current_level = 0
		data_step = np.zeros((cells_lat,cells_lon))
		polygon = []
		height_0 = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, lon_cen_vector[i], lat_cen_vector[i], cells_lon, cells_lat, Topography)

		polygon.append((lon_cen_vector[i], lat_cen_vector[i],  height_0, 1.0, -1, volume_vector[i], phi_0_vector[i] ))

		sum_pixels = 0
		ws_current = ws_vector[i]
		rho_p_current = rho_p_vector[i]
		rho_gas_current = rho_gas_vector[i]
		Fr_current = Fr_vector[i]
		gp_current = g * (rho_p_current - rho_gas_current ) / rho_gas_current

		for j in range(10000): 

			if(j == len(polygon)):
				if( N == 1 ):			
					data_cones = data_cones + data_step
				break
			if( max_levels < polygon[j][3] ):
				if( N == 1 ):
					data_cones = data_cones + data_step
				break
			elif(current_level < polygon[j][3]):
				current_level = polygon[j][3]
				if( N == 1 ):
					data_cones = data_cones + data_step

			polygon_xy = []
			polygons_new = []
			polygon_xy_res2 = []
			polygon_xy_res3 = []

			const_c = 0.5 * np.power( ws_current * polygon[j][6] * gp_current * Fr_current * Fr_current , 1.0/3.0)
			Lmax = np.power(( 16 * np.sqrt(2) * np.power(const_c, 1.5) * np.power( polygon[j][5] / np.pi / ws_current , 1.5 ) ),0.25)
			const_k = (ws_current / Fr_current) * np.power( gp_current, -0.5) * np.power( polygon[j][5] / np.pi , -1.5) 

			for angle_deg in vec_ang:
				angle_rad = angle_deg * np.pi /180
				h_min = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, polygon[j][0] , polygon[j][1] , cells_lon, cells_lat, Topography)
				for distance in range(distep, 100000, distep):
					if( distance > Lmax ):
						polygons_new.append(Lmax)
						distance = Lmax
						polygon_xy.append((int((polygon[j][0] + (distance)*cos(angle_rad)*step_lon_deg/step_lon_m - lon1) * cells_lon / (lon2 - lon1)),int((polygon[j][1] + (distance)*sin(angle_rad)*step_lat_deg/step_lat_m - lat1) * cells_lat / (lat2 - lat1))))
						break
					h = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, polygon[j][0] + distance * cos(angle_rad) * step_lon_deg / step_lon_m , polygon[j][1] + distance*sin(angle_rad)*step_lat_deg/step_lat_m , cells_lon, cells_lat, Topography)
					h_min = min(h, h_min)
					h_boxmodel = ( 1 / (2 * g) ) * np.power( ( const_c * np.power(Lmax, 1.0/3.0) ) / ( ( distance / Lmax) * np.power( cosh(atanh( np.power( distance / Lmax, 2.0) )) , 2.0)  ) , 2.0)
					if( h >= h_min + h_boxmodel ):
						polygon_xy.append((int((polygon[j][0] + (distance - distep)*cos(angle_rad)*step_lon_deg/step_lon_m - lon1) * cells_lon / (lon2 - lon1)),int((polygon[j][1] + (distance - distep)*sin(angle_rad)*step_lat_deg/step_lat_m - lat1) * cells_lat / (lat2 - lat1))))
						polygons_new.append(distance - distep)
						break

			if( (redist_volume == 3 or redist_volume == 4) and polygon[j][4] > -1 ):
				vector_correc = np.zeros(int(anglen))
				lim = np.int(polygon[j][4])
				if( polygon[j][4] == np.int(polygon[j][4]) ):
					for ii in range(int(anglen)):
						vector_correc[ii] = vector_backward_1[int((ii - polygon[j][4] + index_max) % anglen)]

				else:
					for ii in range(int(anglen)):
						vector_correc[ii] = vector_backward_2[int((ii - polygon[j][4] + index_max) % anglen)]
			else:
				vector_correc = np.ones(int(anglen))			
			polygons_new = polygons_new * vector_correc

			if( j == 0 ):
				runout_min = min(polygons_new)

			if( max(polygons_new) > 500 and max(polygons_new) < 5000 ):
				for angle_deg in vec_ang_res2:
					angle_rad = angle_deg * np.pi /180
					h_min = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, polygon[j][0] , polygon[j][1] , cells_lon, cells_lat, Topography)
					for distance in range(distep, 100000, distep):
						if( distance > Lmax ):
							distance = Lmax
							polygon_xy_res2.append((int((polygon[j][0] + (distance)*cos(angle_rad)*step_lon_deg/step_lon_m - lon1) * cells_lon / (lon2 - lon1)),int((polygon[j][1] + (distance)*sin(angle_rad)*step_lat_deg/step_lat_m - lat1) * cells_lat / (lat2 - lat1))))
							break
						h = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, polygon[j][0] + distance * cos(angle_rad) * step_lon_deg / step_lon_m , polygon[j][1] + distance*sin(angle_rad)*step_lat_deg/step_lat_m , cells_lon, cells_lat, Topography)
						h_min = min(h, h_min)
						h_boxmodel = ( 1 / (2 * g) ) * np.power( ( const_c * np.power(Lmax, 1.0/3.0) ) / ( ( distance / Lmax) * np.power( cosh(atanh( np.power( distance / Lmax, 2.0) )) , 2.0)  ) , 2.0)
						if( h >= h_min + h_boxmodel ):
							polygon_xy_res2.append((int((polygon[j][0] + (distance - distep)*cos(angle_rad)*step_lon_deg/step_lon_m - lon1) * cells_lon / (lon2 - lon1)),int((polygon[j][1] + (distance - distep)*sin(angle_rad)*step_lat_deg/step_lat_m - lat1) * cells_lat / (lat2 - lat1))))
							break
			elif( max(polygons_new) >= 5000 ):
				for angle_deg in vec_ang_res3:
					angle_rad = angle_deg * np.pi /180
					h_min = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, polygon[j][0] , polygon[j][1] , cells_lon, cells_lat, Topography)
					for distance in range(distep, 100000, distep):
						if( distance > Lmax ):
							distance = Lmax
							polygon_xy_res3.append((int((polygon[j][0] + (distance)*cos(angle_rad)*step_lon_deg/step_lon_m - lon1) * cells_lon / (lon2 - lon1)),int((polygon[j][1] + (distance)*sin(angle_rad)*step_lat_deg/step_lat_m - lat1) * cells_lat / (lat2 - lat1))))
							break
						h = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, polygon[j][0] + distance * cos(angle_rad) * step_lon_deg / step_lon_m , polygon[j][1] + distance*sin(angle_rad)*step_lat_deg/step_lat_m , cells_lon, cells_lat, Topography)
						h_min = min(h, h_min)
						h_boxmodel = ( 1 / (2 * g) ) * np.power( ( const_c * np.power(Lmax, 1.0/3.0) ) / ( ( distance / Lmax) * np.power( cosh(atanh( np.power( distance / Lmax, 2.0) )) , 2.0)  ) , 2.0)
						if( h >= h_min + h_boxmodel ):
							polygon_xy_res3.append((int((polygon[j][0] + (distance - distep)*cos(angle_rad)*step_lon_deg/step_lon_m - lon1) * cells_lon / (lon2 - lon1)),int((polygon[j][1] + (distance - distep)*sin(angle_rad)*step_lat_deg/step_lat_m - lat1) * cells_lat / (lat2 - lat1))))
							break

			img = Image.new('L', (cells_lon, cells_lat), 0)
			if( len(polygon_xy) > 0 ):
				if(  max(polygons_new) <= 500 ):
					draw = ImageDraw.Draw(img).polygon(polygon_xy, outline = 1 , fill = 1)
				elif( max(polygons_new) > 500 and max(polygons_new) < 5000 ):
					draw = ImageDraw.Draw(img).polygon(polygon_xy_res2, outline = 1 , fill = 1)
				else:
					draw = ImageDraw.Draw(img).polygon(polygon_xy_res3, outline = 1 , fill = 1)
				data_step = np.maximum( np.minimum(data_aux_t, data_step + np.array(img)), data_aux_b)

			if( max_levels > polygon[j][3] and sum(sum(data_step)) > sum_pixels + pix_min and max(polygons_new) > val_resolution * np.sqrt( step_lat_m * step_lon_m ) ):

				aux = np.zeros(len(polygons_new)+2) 
				aux[1:len(polygons_new)+1] = np.array(polygons_new) 
				aux[0] = polygons_new[len(polygons_new)-1]
				aux[len(polygons_new)+1] = polygons_new[0]
				der1 = (aux[1:len(aux)-1] - aux[2:len(aux)])
				der2 = (aux[1:len(aux)-1] - aux[0:len(aux)-2])
				wh1 = np.where(der1 >= 0)
				wh2 = np.where(der2 >= 0)
				wh_max = np.intersect1d(wh1[0], wh2[0])
				wh_grouped = np.split(wh_max, np.where(np.diff(wh_max) > 1)[0] + 1 )
				wh3 = np.where( abs(der1) > 0)
				wh4 = np.where( abs(der2) > 0)
				wh5 = np.intersect1d(wh_max, wh3[0])
				wh6 = np.intersect1d(wh_max, wh4[0])
				grouped_filter = np.zeros(len(wh_grouped))

				for x_grouped in range(len(wh_grouped)):
					if( len(np.intersect1d(wh_grouped[x_grouped],wh5)) > 0 and len(np.intersect1d(wh_grouped[x_grouped],wh6)) > 0):
						grouped_filter[x_grouped] = 1

				if( np.min(wh_grouped[0]) == 0 and np.max(wh_grouped[len(wh_grouped)-1]) == anglen - 1):

					if( len(np.intersect1d(wh_grouped[0],wh5)) > 0 and len(np.intersect1d(wh_grouped[len(wh_grouped)-1],wh6)) > 0):
						grouped_filter[len(wh_grouped) - 1] = 1

					aux_grouped = np.concatenate((wh_grouped[len(wh_grouped)-1], wh_grouped[0] + len(polygons_new)))
					aux_filter = grouped_filter[len(wh_grouped)-1] + grouped_filter[0]
					wh_grouped = wh_grouped[1:-1]
					wh_grouped.append(aux_grouped)
					grouped_filter = np.append(grouped_filter[1:-1],aux_filter)

				wh_max = []
				for k in range(len(grouped_filter)):
					if(grouped_filter[k] > 0 ):
						if(np.mean(wh_grouped[k]) < len(polygons_new) and np.mean(wh_grouped[k]) >= 0.0):
							wh_max.append(np.mean(wh_grouped[k]))
						elif( np.mean(wh_grouped[k]) < len(polygons_new) ):
							wh_max.append(len(polygons_new) + np.mean(wh_grouped[k]))
						else:
							wh_max.append(- len(polygons_new) + np.mean(wh_grouped[k]))

				if( redist_volume == 2 or redist_volume == 4):

					wh1 = np.where(der1 <= 0)
					wh2 = np.where(der2 <= 0)
					wh_min = np.intersect1d(wh1[0], wh2[0])
					wh_grouped = np.split(wh_min, np.where(np.diff(wh_min) > 1)[0] + 1 )
					wh3 = np.where( abs(der1) > 0)
					wh4 = np.where( abs(der2) > 0)
					wh5 = np.intersect1d(wh_min, wh3[0])
					wh6 = np.intersect1d(wh_min, wh4[0])
					grouped_filter = np.zeros(len(wh_grouped))

					for x_grouped in range(len(wh_grouped)):
						if( len(np.intersect1d(wh_grouped[x_grouped],wh5)) > 0 and len(np.intersect1d(wh_grouped[x_grouped],wh6)) > 0):
							grouped_filter[x_grouped] = 1
					
					if( np.min(wh_grouped[0]) == 0 and np.max(wh_grouped[len(wh_grouped)-1]) == anglen - 1):
						if( len(np.intersect1d(wh_grouped[0],wh5)) > 0 and len(np.intersect1d(wh_grouped[len(wh_grouped)-1],wh6)) > 0):
							grouped_filter[len(wh_grouped) - 1] = 1

						aux_grouped = np.concatenate((wh_grouped[len(wh_grouped)-1], wh_grouped[0] + len(polygons_new)))
						aux_filter = grouped_filter[len(wh_grouped)-1] + grouped_filter[0]
						wh_grouped = wh_grouped[1:-1]
						wh_grouped.append(aux_grouped)
						grouped_filter = np.append(grouped_filter[1:-1],aux_filter)

					wh_min = []

					for k in range(len(grouped_filter)):
						if(grouped_filter[k] > 0 ):
							if(np.mean(wh_grouped[k]) < len(polygons_new) and np.mean(wh_grouped[k]) >= 0.0):
								wh_min.append(np.mean(wh_grouped[k]))
							elif(np.mean(wh_grouped[k]) < len(polygons_new) ):
								wh_min.append(len(polygons_new) + np.mean(wh_grouped[k]))
							else:
								wh_min.append(- len(polygons_new) + np.mean(wh_grouped[k]) )

				wh_sum = np.zeros(len(polygons_new)) 
				ter_sum = np.zeros(len(polygons_new)) 
				pos_sum = np.zeros(len(polygons_new)) 

				if(len(wh_max) > 0):
					
					if( redist_volume == 1 or  redist_volume == 3 or len(wh_max) == 1):
						for l_max_real in wh_max:
							lmax = np.int(l_max_real)
							l_it = 	len(polygons_new) - 1		
							for l in range(1,len(polygons_new)):
								l_index = lmax + l
								if(l_index >= len(polygons_new)):
									l_index = l_index - len(polygons_new)
								if( polygons_new[lmax] < polygons_new[l_index] ):
									l_it = l
									break
								wh_sum[lmax] = wh_sum[lmax] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
								ter_sum[lmax] = ter_sum[lmax] + 1.0 * vector_correc[l_index]
								pos_sum[lmax] = pos_sum[lmax] + polygons_new[l_index] * vector_correc[l_index]

							for l in range(1,len(polygons_new) - l_it):
								l_index = lmax - l
								if(l_index < 0):
									l_index = l_index + len(polygons_new)
								if( polygons_new[lmax] < polygons_new[l_index] ):
									break							
								wh_sum[lmax] = wh_sum[lmax] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
								ter_sum[lmax] = ter_sum[lmax] + 1.0 * vector_correc[l_index]
								pos_sum[lmax] = pos_sum[lmax] + polygons_new[l_index] * vector_correc[l_index]

					elif( redist_volume == 2 or redist_volume == 4):

						wh_max = np.sort(wh_max)
						wh_min = np.sort(wh_min)

						if(wh_min[0] > wh_max[0]):

							for l_ind in range(len(wh_max)):
								l_max_real = wh_max[l_ind]	
								l_max_int = np.int(l_max_real)
								step_right = wh_min[l_ind] - l_max_int
								l_right_real = wh_min[l_ind]
								l_right_int = np.int(l_right_real)

								if(l_ind == 0):
									step_left = anglen + l_max_int - wh_min[len(wh_min)-1]
									l_left_real = wh_min[len(wh_min) - 1]
									left_index = len(wh_min) - 1
								else:
									step_left = l_max_int - wh_min[l_ind - 1]
									l_left_real = wh_min[l_ind - 1]
									left_index = l_ind - 1
								
								l_left_int = np.int(l_left_real)

								for l in range(1,int(step_right)):
									l_index = l_max_int + l
									if(l_index >= len(polygons_new)):
										l_index = l_index - len(polygons_new)
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_index]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_index] * vector_correc[l_index]

								if( int(step_right) == step_right ):
									wh_sum[l_max_int] = wh_sum[l_max_int] + 0.5 * np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_right_int], 4.0) , 2.0) * vector_correc[l_right_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 0.5 * vector_correc[l_right_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + 0.5 * polygons_new[l_right_int] * vector_correc[l_right_int]
								else:
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_right_int], 4.0) , 2.0) * vector_correc[l_right_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_right_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_right_int] * vector_correc[l_right_int]

								for l in range(1,int(step_left)):
									l_index = l_max_int - l
									if( l_index < 0 ):
										l_index = len(polygons_new) + l_index
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_index]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_index] * vector_correc[l_index]

								if( int(step_left) == step_left ):
									wh_sum[l_max_int] = wh_sum[l_max_int] + 0.5 * np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_left_int], 4.0) , 2.0) * vector_correc[l_left_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 0.5 * vector_correc[l_left_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + 0.5 * polygons_new[l_left_int] * vector_correc[l_left_int]

								else:
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_left_int], 4.0) , 2.0)  * vector_correc[l_left_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0  * vector_correc[l_left_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_left_int] * vector_correc[l_left_int]

						else:

							for l_ind in range(len(wh_max)):
								l_max_real = wh_max[l_ind]	
								l_max_int = np.int(l_max_real)
								step_left = l_max_int - wh_min[l_ind]
								l_left_real = wh_min[l_ind]
								l_left_int = np.int(l_left_real)

								if(l_ind == len(wh_max) - 1 ):
									step_right = anglen - l_max_int + wh_min[0]
									l_right_real = wh_min[0]
									right_index = 0
								else:
									step_right =  wh_min[l_ind + 1] - l_max_int
									l_right_real = wh_min[l_ind + 1]
									right_index = l_ind + 1

								l_right_int = np.int(l_right_real)

								for l in range(1,int(step_right)):
									l_index = l_max_int + l
									if(l_index >= len(polygons_new)):
										l_index = l_index - len(polygons_new)
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_index]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_index] * vector_correc[l_index]

								if( int(step_right) == step_right ):
									wh_sum[l_max_int] = wh_sum[l_max_int] + 0.5 * np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_right_int], 4.0) , 2.0) * vector_correc[l_right_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 0.5 * vector_correc[l_right_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + 0.5 * polygons_new[l_right_int] * vector_correc[l_right_int]


								else:
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_right_int], 4.0) , 2.0) * vector_correc[l_right_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_right_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_right_int] * vector_correc[l_right_int]

								for l in range(1,int(step_left)):
									l_index = l_max_int - l
									if( l_index < 0 ):
										l_index = len(polygons_new) + l_index
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_index]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_index] * vector_correc[l_index]

								if( int(step_left) == step_left ):
									wh_sum[l_max_int] = wh_sum[l_max_int] + 0.5 * np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_left_int], 4.0) , 2.0) * vector_correc[l_left_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 0.5 * vector_correc[l_left_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + 0.5 * polygons_new[l_left_int] * vector_correc[l_left_int]

								else:
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_left_int], 4.0) , 2.0) * vector_correc[l_left_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_left_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_left_int] * vector_correc[l_left_int]

					for l in wh_max:
						lint = np.int(l)
						if( wh_sum[lint] > 0 ):
							wh_sum[lint] = wh_sum[lint] / ter_sum[lint]
							pos_sum[lint] = pos_sum[lint] / ter_sum[lint]

							new_x = polygon[j][0] + pos_sum[lint] * cos((vec_ang[lint] + angstep*(l-lint) ) * np.pi / 180 ) *step_lon_deg/step_lon_m ; 
							new_y = polygon[j][1] + pos_sum[lint] * sin((vec_ang[lint] + angstep*(l-lint) ) * np.pi / 180 ) *step_lat_deg/step_lat_m ;
							height_eff = interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, new_x, new_y, cells_lon, cells_lat, Topography)
							new_volume = polygon[j][5]*ter_sum[lint]/sum(vector_correc)*(1 - polygon[j][6])/ (1-wh_sum[lint])

							if( interpol_pos(lon1, lat1, step_lon_deg, step_lat_deg, new_x, new_y, cells_lon, cells_lat, Topography) < 99999 ):
								polygon.append(( new_x, new_y, height_eff, polygon[j][3] + 1, l, new_volume , wh_sum[lint] ))

			sum_pixels = sum(sum(data_step))	
			print((j, len(polygon), polygon[j][3], polygon[j][2], sum(sum(data_step)), polygon[j][4], polygon[j][5] , polygon[j][6], Lmax ))

			if( save_data == 1 ):
				if(j == 0 or (j + 1 == len(polygon))):
					distances = np.power(np.power(( matrix_lon - lon_cen_vector[i]) * (step_lon_m / step_lon_deg),2) + np.power(( matrix_lat - lat_cen_vector[i])*(step_lat_m / step_lat_deg),2),0.5) 
					distances = distances * data_step[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ]
					string_data = string_data + "\n" + str(polygon[j][3]) + " " + str(sum(sum(data_step))* area_pixel) + " " + str(distances.max() / 1000.0)

				elif(polygon[j][3] < polygon[j+1][3] ):
					distances = np.power(np.power(( matrix_lon - lon_cen_vector[i]) * (step_lon_m / step_lon_deg),2) + np.power(( matrix_lat - lat_cen_vector[i])*(step_lat_m / step_lat_deg),2),0.5) 
					distances = distances * data_step[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ]
					string_data = string_data + "\n" + str(polygon[j][3]) + " " + str(sum(sum(data_step))* area_pixel) + " " + str(distances.max() / 1000.0)
				if( N == 1 ):
					string_cones = string_cones + "\n"  + str(j) + " " + str(polygon[j][3]) + " " + str(polygon[j][2]) + " " + str(polygon[j][5])  + " " + str(polygon[j][6]) 

		if( N > 1 ):
			data_cones = data_cones + data_step

		if( save_data == 1 ):

			distances = np.power(np.power(( matrix_lon - lon_cen_vector[i]) * (step_lon_m / step_lon_deg),2) + np.power(( matrix_lat - lat_cen_vector[i])*(step_lat_m / step_lat_deg),2),0.5) 

			distances = distances * data_step[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ]
			summary_data[i,8] = sum(sum(data_step)) * area_pixel
			summary_data[i,9] = distances.max() / 1000.0
			summary_data[i,10] = runout_min / 1000.0

		print(' Simulation finished (N = ' + str(i+1) + ')')

if( source_dem == 2 ):

	data_cones = np.zeros((n_north,n_east))
	data_aux_t = np.ones((n_north,n_east))
	data_aux_b = np.zeros((n_north,n_east))
	vec_ang = range(0, 360, angstep)
	vec_ang_res2 = np.arange(0, 360, angstep_res2)
	vec_ang_res3 = np.arange(0, 360, angstep_res3)

	for i in range(0,N):
		runout_min = -1
		current_level = 0
		data_step = np.zeros((n_north,n_east))
		polygon = []
		height_0 = interpol_pos(east_cor, north_cor, cellsize, cellsize, east_cen_vector[i], north_cen_vector[i], n_east, n_north, Topography)
		polygon.append((east_cen_vector[i], north_cen_vector[i],  height_0, 1.0, -1, volume_vector[i], phi_0_vector[i] ))
		sum_pixels = 0
		ws_current = ws_vector[i]
		rho_p_current = rho_p_vector[i]
		rho_gas_current = rho_gas_vector[i]
		Fr_current = Fr_vector[i]
		gp_current = g * (rho_p_current - rho_gas_current ) / rho_gas_current

		for j in range(10000): 
			if(j == len(polygon)):
				if( N == 1 ):			
					data_cones = data_cones + data_step
				break
			if( max_levels < polygon[j][3] ):
				if( N == 1 ):
					data_cones = data_cones + data_step
				break
			elif(current_level < polygon[j][3]):
				current_level = polygon[j][3]
				if( N == 1 ):
					data_cones = data_cones + data_step

			polygon_xy = []
			polygons_new = []
			polygon_xy_res2 = []
			polygon_xy_res3 = []

			const_c = 0.5 * np.power( ws_current * polygon[j][6] * gp_current * Fr_current * Fr_current , 1.0/3.0)
			Lmax = np.power(( 16 * np.sqrt(2) * np.power(const_c, 1.5) * np.power( polygon[j][5] / np.pi / ws_current , 1.5 ) ),0.25)
			const_k = (ws_current / Fr_current) * np.power( gp_current, -0.5) * np.power( polygon[j][5] / np.pi , -1.5)

			for angle_deg in vec_ang:
				angle_rad = angle_deg * np.pi /180
				h_min = interpol_pos(east_cor, north_cor, cellsize, cellsize, polygon[j][0] , polygon[j][1] , n_east, n_north, Topography)
				for distance in range(distep, 100000, distep):
					if( distance > Lmax ):
						polygons_new.append(Lmax)
						distance = Lmax
						polygon_xy.append((int((polygon[j][0] + (distance)*cos(angle_rad) - east_cor ) * n_east / (cellsize * (n_east - 1) ) ),int((polygon[j][1] + (distance)*sin(angle_rad) - north_cor) * n_north / (cellsize * (n_north - 1) ))))
						break
					h = interpol_pos(east_cor, north_cor, cellsize, cellsize, polygon[j][0] + distance * cos(angle_rad) , polygon[j][1] + distance*sin(angle_rad) , n_east, n_north, Topography)
					h_min = min(h, h_min)
					h_boxmodel = ( 1 / (2 * g) ) * np.power( ( const_c * np.power(Lmax, 1.0/3.0) ) / ( ( distance / Lmax) * np.power( cosh(atanh( np.power( distance / Lmax, 2.0) )) , 2.0)  ) , 2.0)
					if(  h >= h_min + h_boxmodel ):
						polygon_xy.append((int((polygon[j][0] + (distance-distep)* cos(angle_rad) - east_cor) * n_east / ( cellsize * ( n_east - 1 ) ) ), int((polygon[j][1] + (distance-distep)*sin(angle_rad) - north_cor) * n_north / ( cellsize * ( n_north - 1 ) ))))
						polygons_new.append(distance - distep)
						break	

			if( (redist_volume == 3 or redist_volume == 4) and polygon[j][4] > -1 ):
				vector_correc = np.zeros(int(anglen))
				lim = np.int(polygon[j][4])
				if( polygon[j][4] == np.int(polygon[j][4]) ):
					for ii in range(int(anglen)):
						vector_correc[ii] = vector_backward_1[int((ii - polygon[j][4] + index_max) % anglen)]

				else:
					for ii in range(int(anglen)):
						vector_correc[ii] = vector_backward_2[int((ii - polygon[j][4] + index_max) % anglen)]
			else:
				vector_correc = np.ones(int(anglen))	
			polygons_new = polygons_new * vector_correc
			if( j == 0 ):
				runout_min = min(polygons_new)

			if( max(polygons_new) > 500 and max(polygons_new) < 5000 ):
				for angle_deg in vec_ang_res2:
					angle_rad = angle_deg * np.pi /180
					h_min = interpol_pos(east_cor, north_cor, cellsize, cellsize, polygon[j][0] , polygon[j][1] , n_east, n_north, Topography)
					for distance in range(distep, 100000, distep):
						if( distance > Lmax ):
							distance = Lmax
							polygon_xy_res2.append((int((polygon[j][0] + (distance)*cos(angle_rad) - east_cor ) * n_east / (cellsize * (n_east - 1) ) ),int((polygon[j][1] + (distance)*sin(angle_rad) - north_cor) * n_north / (cellsize * (n_north - 1) ))))
							break
						h = interpol_pos(east_cor, north_cor, cellsize, cellsize, polygon[j][0] + distance * cos(angle_rad) , polygon[j][1] + distance*sin(angle_rad) , n_east, n_north, Topography)
						h_min = min(h, h_min)
						h_boxmodel = ( 1 / (2 * g) ) * np.power( ( const_c * np.power(Lmax, 1.0/3.0) ) / ( ( distance / Lmax) * np.power( cosh(atanh( np.power( distance / Lmax, 2.0) )) , 2.0)  ) , 2.0)
						if( h >= h_min + h_boxmodel ):
							polygon_xy_res2.append((int((polygon[j][0] + (distance-distep)* cos(angle_rad) - east_cor) * n_east / ( cellsize * ( n_east - 1 ) ) ), int((polygon[j][1] + (distance-distep)*sin(angle_rad) - north_cor) * n_north / ( cellsize * ( n_north - 1 ) ))))
							break
			elif( max(polygons_new) >= 5000 ):
				for angle_deg in vec_ang_res3:
					angle_rad = angle_deg * np.pi /180
					h_min = interpol_pos(east_cor, north_cor, cellsize, cellsize, polygon[j][0] , polygon[j][1] , n_east, n_north, Topography)
					for distance in range(distep, 100000, distep):
						if( distance > Lmax ):
							distance = Lmax
							polygon_xy_res3.append((int((polygon[j][0] + (distance)*cos(angle_rad) - east_cor ) * n_east / (cellsize * (n_east - 1) ) ),int((polygon[j][1] + (distance)*sin(angle_rad) - north_cor) * n_north / (cellsize * (n_north - 1) ))))
							break
						h = interpol_pos(east_cor, north_cor, cellsize, cellsize, polygon[j][0] + distance * cos(angle_rad) , polygon[j][1] + distance*sin(angle_rad) , n_east, n_north, Topography)
						h_min = min(h, h_min)
						h_boxmodel = ( 1 / (2 * g) ) * np.power( ( const_c * np.power(Lmax, 1.0/3.0) ) / ( ( distance / Lmax) * np.power( cosh(atanh( np.power( distance / Lmax, 2.0) )) , 2.0)  ) , 2.0)
							polygon_xy_res3.append((int((polygon[j][0] + (distance-distep)* cos(angle_rad) - east_cor) * n_east / ( cellsize * ( n_east - 1 ) ) ), int((polygon[j][1] + (distance-distep)*sin(angle_rad) - north_cor) * n_north / ( cellsize * ( n_north - 1 ) ))))
							break

			img = Image.new('L', (n_east, n_north), 0)
			if( len(polygon_xy) > 0 ):
				if(  max(polygons_new) <= 500 ):
					draw = ImageDraw.Draw(img).polygon(polygon_xy, outline = 1 , fill = 1)
				elif( max(polygons_new) > 500 and max(polygons_new) < 5000 ):
					draw = ImageDraw.Draw(img).polygon(polygon_xy_res2, outline = 1 , fill = 1)
				else:
					draw = ImageDraw.Draw(img).polygon(polygon_xy_res3, outline = 1 , fill = 1)
				data_step = np.maximum( np.minimum(data_aux_t, data_step + np.array(img)), data_aux_b)

			if( max_levels > polygon[j][3] and sum(sum(data_step)) > sum_pixels + pix_min and max(polygons_new) > val_resolution * cellsize ):
				aux = np.zeros(len(polygons_new) + 2) 
				aux[1:len(polygons_new)+1] = np.array(polygons_new) 
				aux[0] = polygons_new[len(polygons_new)-1]
				aux[len(polygons_new)+1] = polygons_new[0]
				der1 = (aux[1:len(aux)-1] - aux[2:len(aux)])
				der2 = (aux[1:len(aux)-1] - aux[0:len(aux)-2])
				wh1 = np.where(der1 >= 0)
				wh2 = np.where(der2 >= 0)
				wh_max = np.intersect1d(wh1[0], wh2[0])
				wh_grouped = np.split(wh_max, np.where(np.diff(wh_max) > 1)[0] + 1 )
				wh3 = np.where( abs(der1) > 0 )
				wh4 = np.where( abs(der2) > 0 )
				wh5 = np.intersect1d(wh_max, wh3[0])
				wh6 = np.intersect1d(wh_max, wh4[0])
				grouped_filter = np.zeros(len(wh_grouped))

				for x_grouped in range(len(wh_grouped)):
					if( len(np.intersect1d(wh_grouped[x_grouped],wh5)) > 0 and len(np.intersect1d(wh_grouped[x_grouped],wh6)) > 0):
						grouped_filter[x_grouped] = 1

				if( np.min(wh_grouped[0]) == 0 and np.max(wh_grouped[len(wh_grouped)-1]) == anglen - 1 ):
					if( len(np.intersect1d(wh_grouped[0],wh5)) > 0 and len(np.intersect1d(wh_grouped[len(wh_grouped)-1],wh6)) > 0):
						grouped_filter[len(wh_grouped) - 1] = 1
					aux_grouped = np.concatenate((wh_grouped[len(wh_grouped)-1], wh_grouped[0] + len(polygons_new)))
					aux_filter = grouped_filter[len(wh_grouped)-1] + grouped_filter[0]
					wh_grouped = wh_grouped[1:-1]
					wh_grouped.append(aux_grouped)
					grouped_filter = np.append(grouped_filter[1:-1],aux_filter)

				wh_max = []
				for k in range(len(grouped_filter)):
					if(grouped_filter[k] > 0 ):
						if(np.mean(wh_grouped[k]) < len(polygons_new) and np.mean(wh_grouped[k]) >= 0.0):
							wh_max.append(np.mean(wh_grouped[k]))
						elif( np.mean(wh_grouped[k]) < len(polygons_new) ):
							wh_max.append(len(polygons_new) + np.mean(wh_grouped[k]))
						else:
							wh_max.append(- len(polygons_new) + np.mean(wh_grouped[k]))

				if(redist_volume == 2 or redist_volume == 4):
					wh1 = np.where(der1 <= 0)
					wh2 = np.where(der2 <= 0)
					wh_min = np.intersect1d(wh1[0], wh2[0])
					wh_grouped = np.split(wh_min, np.where(np.diff(wh_min) > 1)[0] + 1 )
					wh3 = np.where( abs(der1) > 0)
					wh4 = np.where( abs(der2) > 0)
					wh5 = np.intersect1d(wh_min, wh3[0])
					wh6 = np.intersect1d(wh_min, wh4[0])
					grouped_filter = np.zeros(len(wh_grouped))

					for x_grouped in range(len(wh_grouped)):
						if( len(np.intersect1d(wh_grouped[x_grouped],wh5)) > 0 and len(np.intersect1d(wh_grouped[x_grouped],wh6)) > 0):
							grouped_filter[x_grouped] = 1
					
					if( np.min(wh_grouped[0]) == 0 and np.max(wh_grouped[len(wh_grouped)-1]) == anglen - 1):
						if( len(np.intersect1d(wh_grouped[0],wh5)) > 0 and len(np.intersect1d(wh_grouped[len(wh_grouped)-1],wh6)) > 0):
							grouped_filter[len(wh_grouped) - 1] = 1
						aux_grouped = np.concatenate((wh_grouped[len(wh_grouped)-1], wh_grouped[0] + len(polygons_new)))
						aux_filter = grouped_filter[len(wh_grouped)-1] + grouped_filter[0]
						wh_grouped = wh_grouped[1:-1]
						wh_grouped.append(aux_grouped)
						grouped_filter = np.append(grouped_filter[1:-1],aux_filter)

					wh_min = []

					for k in range(len(grouped_filter)):
						if(grouped_filter[k] > 0 ):
							if(np.mean(wh_grouped[k]) < len(polygons_new) and np.mean(wh_grouped[k]) >= 0.0):
								wh_min.append(np.mean(wh_grouped[k]))
							elif(np.mean(wh_grouped[k]) < len(polygons_new) ):
								wh_min.append(len(polygons_new) + np.mean(wh_grouped[k]))
							else:
								wh_min.append(- len(polygons_new) + np.mean(wh_grouped[k]) )

				wh_sum = np.zeros(len(polygons_new))
				ter_sum = np.zeros(len(polygons_new)) 
				pos_sum = np.zeros(len(polygons_new)) 

				if(len(wh_max) > 0):
					
					if( (redist_volume == 1 or redist_volume == 3) or len(wh_max) == 1):
						for l_max_real in wh_max:
							lmax = np.int(l_max_real)
							l_it = 	len(polygons_new) - 1		
							for l in range(1,len(polygons_new)):
								l_index = lmax + l
								if(l_index >= len(polygons_new)):
									l_index = l_index - len(polygons_new)
								if( polygons_new[lmax] < polygons_new[l_index] ):
									l_it = l
									break
								wh_sum[lmax] = wh_sum[lmax] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
								ter_sum[lmax] = ter_sum[lmax] + 1.0 * vector_correc[l_index]
								pos_sum[lmax] = pos_sum[lmax] + polygons_new[l_index] * vector_correc[l_index] * np.cos( (lmax - l_index) * angstep * np.pi / 180.0 )

							for l in range(1,len(polygons_new) - l_it):
								l_index = lmax - l
								if(l_index < 0):
									l_index = l_index + len(polygons_new)
								if( polygons_new[lmax] < polygons_new[l_index] ):
									break							
								wh_sum[lmax] = wh_sum[lmax] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
								ter_sum[lmax] = ter_sum[lmax] + 1.0 * vector_correc[l_index]
								pos_sum[lmax] = pos_sum[lmax] + polygons_new[l_index] * vector_correc[l_index] * np.cos( (lmax - l_index) * angstep * np.pi / 180.0 )

					elif( redist_volume == 2 or redist_volume == 4):

						wh_max = np.sort(wh_max)
						wh_min = np.sort(wh_min)

						if(wh_min[0] > wh_max[0]):

							for l_ind in range(len(wh_max)):
								l_max_real = wh_max[l_ind]	
								l_max_int = np.int(l_max_real)
								step_right = wh_min[l_ind] - l_max_int
								l_right_real = wh_min[l_ind]
								l_right_int = np.int(l_right_real)

								if(l_ind == 0):
									step_left = anglen + l_max_int - wh_min[len(wh_min)-1]
									l_left_real = wh_min[len(wh_min) - 1]
									left_index = len(wh_min) - 1
								else:
									step_left = l_max_int - wh_min[l_ind - 1]
									l_left_real = wh_min[l_ind - 1]
									left_index = l_ind - 1
								
								l_left_int = np.int(l_left_real)

								for l in range(1,int(step_right)):
									l_index = l_max_int + l
									if(l_index >= len(polygons_new)):
										l_index = l_index - len(polygons_new)
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_index]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_index] * vector_correc[l_index] * np.cos( (l_max_int - l_index) * angstep * np.pi / 180.0 )

								if( int(step_right) == step_right ):
									wh_sum[l_max_int] = wh_sum[l_max_int] + 0.5 * np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_right_int], 4.0) , 2.0) * vector_correc[l_right_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 0.5 * vector_correc[l_right_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + 0.5 * polygons_new[l_right_int] * vector_correc[l_right_int] * np.cos( (l_right_int - l_max_int) * angstep * np.pi / 180.0 )
								else:
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_right_int], 4.0) , 2.0) * vector_correc[l_right_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_right_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_right_int] * vector_correc[l_right_int] * np.cos( (l_right_int - l_max_int) * angstep * np.pi / 180.0 )

								for l in range(1,int(step_left)):
									l_index = l_max_int - l
									if( l_index < 0 ):
										l_index = len(polygons_new) + l_index
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_index]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_index] * vector_correc[l_index] * np.cos( (l_max_int - l_index) * angstep * np.pi / 180.0 )

								if( int(step_left) == step_left ):
									wh_sum[l_max_int] = wh_sum[l_max_int] + 0.5 * np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_left_int], 4.0) , 2.0) * vector_correc[l_left_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 0.5 * vector_correc[l_left_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + 0.5 * polygons_new[l_left_int] * vector_correc[l_left_int] * np.cos( (l_max_int - l_left_int) * angstep * np.pi / 180.0 )
								else:
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_left_int], 4.0) , 2.0)  * vector_correc[l_left_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0  * vector_correc[l_left_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_left_int] * vector_correc[l_left_int] * np.cos( (l_max_int - l_left_int) * angstep * np.pi / 180.0 )

						else:
							for l_ind in range(len(wh_max)):
								l_max_real = wh_max[l_ind]	
								l_max_int = np.int(l_max_real)
								step_left = l_max_int - wh_min[l_ind]
								l_left_real = wh_min[l_ind]
								l_left_int = np.int(l_left_real)

								if(l_ind == len(wh_max) - 1 ):
									step_right = anglen - l_max_int + wh_min[0]
									l_right_real = wh_min[0]
									right_index = 0
								else:
									step_right =  wh_min[l_ind + 1] - l_max_int
									l_right_real = wh_min[l_ind + 1]
									right_index = l_ind + 1

								l_right_int = np.int(l_right_real)

								for l in range(1,int(step_right)):
									l_index = l_max_int + l
									if(l_index >= len(polygons_new)):
										l_index = l_index - len(polygons_new)
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_index]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_index] * vector_correc[l_index] * np.cos( (l_max_int - l_index) * angstep * np.pi / 180.0 )

								if( int(step_right) == step_right ):
									wh_sum[l_max_int] = wh_sum[l_max_int] + 0.5 * np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_right_int], 4.0) , 2.0) * vector_correc[l_right_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 0.5 * vector_correc[l_right_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + 0.5 * polygons_new[l_right_int] * vector_correc[l_right_int] * np.cos( (l_max_int - l_right_int) * angstep * np.pi / 180.0 )
								else:
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_right_int], 4.0) , 2.0) * vector_correc[l_right_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_right_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_right_int] * vector_correc[l_right_int] * np.cos( (l_max_int - l_right_int) * angstep * np.pi / 180.0 )


								for l in range(1,int(step_left)):
									l_index = l_max_int - l
									if( l_index < 0 ):
										l_index = len(polygons_new) + l_index
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_index], 4.0) , 2.0) * vector_correc[l_index]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_index]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_index] * vector_correc[l_index] * np.cos( (l_max_int - l_index) * angstep * np.pi / 180.0 )

								if( int(step_left) == step_left ):
									wh_sum[l_max_int] = wh_sum[l_max_int] + 0.5 * np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_left_int], 4.0) , 2.0) * vector_correc[l_left_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 0.5 * vector_correc[l_left_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + 0.5 * polygons_new[l_left_int] * vector_correc[l_left_int] * np.cos( (l_max_int - l_left_int) * angstep * np.pi / 180.0 )
								else:
									wh_sum[l_max_int] = wh_sum[l_max_int] + np.power( np.sqrt(polygon[j][6]) - 0.125 * const_k * np.power(polygons_new[l_left_int], 4.0) , 2.0) * vector_correc[l_left_int]
									ter_sum[l_max_int] = ter_sum[l_max_int] + 1.0 * vector_correc[l_left_int]
									pos_sum[l_max_int] = pos_sum[l_max_int] + polygons_new[l_left_int] * vector_correc[l_left_int] * np.cos( (l_max_int - l_left_int) * angstep * np.pi / 180.0 )

					for l in wh_max:
						lint = np.int(l)
						if( wh_sum[lint] > 0 ):
							wh_sum[lint] = wh_sum[lint] / ter_sum[lint]
							pos_sum[lint] = pos_sum[lint] / ter_sum[lint]

							new_x = polygon[j][0] + pos_sum[lint] * cos((vec_ang[lint] + angstep*(l-lint) ) * np.pi / 180 ) ; 
							new_y = polygon[j][1] + pos_sum[lint] * sin((vec_ang[lint] + angstep*(l-lint) ) * np.pi / 180 ) ;
							height_eff = interpol_pos(east_cor, north_cor, cellsize, cellsize, new_x, new_y, n_east, n_north, Topography)
							new_volume = polygon[j][5]*ter_sum[lint]/sum(vector_correc)*(1 - polygon[j][6])/ (1-wh_sum[lint])

							if(interpol_pos(east_cor, north_cor, cellsize, cellsize, new_x, new_y, n_east, n_north, Topography) < 99999 ):
								polygon.append(( new_x, new_y, height_eff, polygon[j][3] + 1, l, new_volume, wh_sum[lint] ))

			sum_pixels = sum(sum(data_step))	
			print((j, len(polygon), polygon[j][3], polygon[j][2], sum(sum(data_step)), polygon[j][4], polygon[j][5] , polygon[j][6], Lmax ))

			if( save_data == 1 ):
				if(j == 0 or (j + 1 == len(polygon))):
					distances = np.power(np.power(( matrix_east - east_cen_vector[i]),2) + np.power(( matrix_north - north_cen_vector[i]),2),0.5) 
					distances = distances * data_step[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ]
					string_data = string_data + "\n" + str(polygon[j][3]) + " " + str(sum(sum(data_step))* area_pixel) + " " + str(distances.max() / 1000.0)

				elif(polygon[j][3] < polygon[j+1][3] ):
					distances = np.power(np.power(( matrix_east - east_cen_vector[i]),2) + np.power(( matrix_north - north_cen_vector[i]),2),0.5) 
					distances = distances * data_step[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ]
					string_data = string_data + "\n" + str(polygon[j][3]) + " " + str(sum(sum(data_step))* area_pixel) + " " + str(distances.max() / 1000.0)
				if( N == 1 ):
					string_cones = string_cones + "\n"  + str(j) + " " + str(polygon[j][3]) + " " + str(polygon[j][2]) + " " + str(polygon[j][5]) 

		if( N > 1 ):
			data_cones = data_cones + data_step

		if( save_data == 1 ):
			distances = np.power(np.power(( matrix_east - east_cen_vector[i]) ,2) + np.power(( matrix_north - north_cen_vector[i]) ,2),0.5) 
			distances = distances * data_step[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ]
			summary_data[i,8] = sum(sum(data_step)) * area_pixel
			summary_data[i,9] = distances.max() / 1000.0
			summary_data[i,10] = runout_min / 1000.0

		print(' Simulation finished (N = ' + str(i+1) + ')')

# SAVE DATA
if( save_data == 1 ):

	print('Saving data')
	if(source_dem == 1 or source_dem == 3):

		cellsize =  max(step_lon_m, step_lat_m)
		if( cellsize == step_lon_m ):
			output_cells_lon = cells_lon - 1
			output_cells_lat = np.int(cells_lat * step_lat_m / step_lon_m)
		else:
			output_cells_lon = np.int(cells_lon * step_lon_m / step_lat_m)
			output_cells_lat = cells_lat - 1

	else:
		output_cells_lat = n_north
		output_cells_lon = n_east

	text_file = open('Results/' + run_name + '/' + 'output_map.asc', 'w')
	text_file.write('ncols' + ' ' + str(output_cells_lon) + '\n')
	text_file.write('nrows' + ' ' + str(output_cells_lat) +'\n')
	text_file.write('xllcorner'+' '+ str(utm_save[0]) +'\n')
	text_file.write('yllcorner'+' '+ str(utm_save[1]) +'\n')
	text_file.write('cellsize'+' '+ str(cellsize) +'\n')
	text_file.write('NODATA_value' +' ' +'-9999');

	data_cones_save = data_cones / N
	if(source_dem == 1 or source_dem == 3):
		for j in range(0, output_cells_lat):
			text_file.write('\n')
			for i in range(0, output_cells_lon):
				matrix_output = interpol_pos(utm_save[0], utm_save[1], step_lon_m, step_lat_m, utm_save[0] + i*cellsize , utm_save[1] + j*cellsize , cells_lon, cells_lat, data_cones_save )
				text_file.write(' ' + str(matrix_output))
		text_file.close()

	else:
		for i in range(output_cells_lat-1,-1,-1):
			text_file.write('\n')
			for j in range(0, output_cells_lon):
				text_file.write(' ' + str(data_cones_save[i,j] ))
		text_file.close()

	np.savetxt('Results/' + run_name + '/' + 'data_cones.txt', data_cones_save, fmt='%.2e')
	np.savetxt('Results/' + run_name + '/' + 'topography.txt', Topography, fmt='%.2e')
	np.savetxt('Results/' + run_name + '/' + 'summary.txt', summary_data, fmt='%.5e')
	if(sea_flag == 1):
		np.savetxt('Results/' + run_name + '/' + 'topography_sea.txt', Topography_Sea, fmt='%.5e')
	text_file = open('Results/' + run_name + '/' + 'energy_cones.txt', 'w')
	text_file.write(string_data)
	text_file.close()
	if(N == 1):
		text_file = open('Results/' + run_name + '/' + 'energy_cones_h.txt', 'w')
		text_file.write(string_cones)
		text_file.close()
	text_file = open('Results/' + run_name + '/' + 'sim_data.txt', 'w')
	text_file.write(sim_data)
	text_file.close()
	if(source_dem == 1 or source_dem == 3):		
		np.savetxt('Results/' + run_name + '/' + 'matrix_lon.txt', matrix_lon, fmt='%.5e')
		np.savetxt('Results/' + run_name + '/' + 'matrix_lat.txt', matrix_lat, fmt='%.5e')
		if(source_dem == 1):		
			text_file = open('Results/' + run_name + '/Topography_3.txt', 'w')
			text_file.write('lon1 ' + str(lon1) + '\n')
			text_file.write('lon2 ' + str(lon2) + '\n')
			text_file.write('lat1 ' + str(lat1) + '\n')
			text_file.write('lat2 ' + str(lat2) + '\n')
			text_file.write('cells_lon ' + str(cells_lon) + '\n')
			text_file.write('cells_lat ' + str(cells_lat) + '\n')
			for i in range(cells_lat):
				for j in range(cells_lon):
					text_file.write(str(Topography[i,j]) + ' ')
				text_file.write('\n')		
			text_file.close()
	elif(source_dem == 2):		
		np.savetxt('Results/' + run_name + '/' + 'matrix_east.txt', matrix_east, fmt='%.5e')
		np.savetxt('Results/' + run_name + '/' + 'matrix_north.txt', matrix_north, fmt='%.5e')

# FIGURES
if((source_dem == 1 or source_dem == 3) and (plot_flag == 1)):

	data_cones = data_cones[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ] / N
	line_val = data_cones.max()
	data_cones[data_cones[:,:] == 0] =  np.nan
	val_up = np.floor((line_val + 0.1 - 1.0 / N ) * 10.0) / 20.0
	val_down = np.maximum( val_up / 10.0 , 0.05 )
	plt.figure(1)
	cmapg = plt.cm.get_cmap('Greys')
	cmapr = plt.cm.get_cmap('Reds')
	cmaps = plt.cm.get_cmap('Blues') 

	if( N > 1 ):
		CS_Topo = plt.contourf(matrix_lon,matrix_lat,Topography, 100, alpha = 1.0, cmap = cmapg ,antialiased=True)
		CS_Sea = plt.contourf(matrix_lon,matrix_lat,Topography_Sea, 100, alpha = 0.5, cmap = cmaps ,antialiased=True)
		CS = plt.contourf(matrix_lon, matrix_lat, data_cones, 100, vmin = 0.0, vmax = 1.0,  alpha= 0.3, interpolation='linear', cmap=cmapr, antialiased=True )	
		fmt = '%.2f'
		plt.colorbar()
		CS_lines = plt.contour(matrix_lon,matrix_lat,data_cones, np.array([val_down, val_up]), colors='r', interpolation='linear', linewidths = 1.0)
		plt.clabel(CS_lines, fontsize = 7, colors='k', fmt=fmt)
	else:
		CS_Topo = plt.contourf(matrix_lon,matrix_lat,Topography, 100, alpha = 1.0, cmap = cmapg ,antialiased=True)
		CS_Sea = plt.contourf(matrix_lon,matrix_lat,Topography_Sea, 100, alpha = 0.5, cmap = cmaps ,antialiased=True)
		CS = plt.contourf(matrix_lon, matrix_lat, data_cones, 100, alpha= 0.3, cmap=cmapr, antialiased=True)

	plt.axes().set_aspect(step_lat_m/step_lon_m)
	plt.xlabel('Longitude $[^\circ]$')
	plt.ylabel('Latitude $[^\circ]$')
	plt.xlim(lon1, lon2 )
	plt.ylim(lat1, lat2 )

	for i in range(len(Cities)):
		plt.text(float(Cities[i][0]), float(Cities[i][1]), str(Cities[i][2]), horizontalalignment='center', verticalalignment='center', fontsize = 6)

	for i in range(0,N):
		plt.plot( lon_cen_vector[i], lat_cen_vector[i], 'r.', markersize=2)

	if( N == 1 ):
		for i in range(1,len(polygon)):
			plt.plot( polygon[i][0],polygon[i][1], 'b.', markersize=2)

	plt.savefig('Results/' + run_name + '/Map.png')

	if( N > 1 ):

		plt.figure(2)
		plt.subplot(131)
		plt.hist(volume_vector)
		plt.xlabel('Volume $[m^3]$')
		plt.subplot(132)
		plt.hist(phi_0_vector)
		plt.xlabel('phi_0')
		plt.subplot(133)
		plt.hist(ws_vector)
		plt.xlabel('Sedimentation velocity [m/s]')
		plt.savefig('Results/' + run_name + '/Histogram.png')

	plt.show()

if(source_dem == 2 and plot_flag == 1):

	data_cones = data_cones[ range(len(data_cones[:,0]) -1 , -1 , -1 ) , : ] / N
	line_val = data_cones.max()
	data_cones[data_cones[:,:] == 0] =  np.nan
	val_up = np.floor((line_val + 0.1 - 1.0 / N ) * 10.0) / 20.0
	val_down = np.maximum( val_up / 10.0 , 0.05 )

	plt.figure(1)

	cmapg = plt.cm.get_cmap('Greys')
	cmapr = plt.cm.get_cmap('Reds')
	cmaps = plt.cm.get_cmap('Blues') 

	if( N > 1 ):
		CS_Topo = plt.contourf(matrix_east,matrix_north,Topography, 100, alpha = 1.0, cmap = cmapg ,antialiased=True)
		CS_Sea = plt.contourf(matrix_east,matrix_north,Topography_Sea, 100, alpha = 0.5, cmap = cmaps ,antialiased=True)
		CS = plt.contourf(matrix_east,matrix_north, data_cones, 100, vmin = 0.0, vmax = 1.0,  alpha= 0.3, interpolation='linear', cmap=cmapr, antialiased=True)	
		fmt = '%.2f'
		plt.colorbar()
		CS_lines = plt.contour(matrix_east,matrix_north, data_cones, np.array([val_down, val_up]), colors='r', interpolation='linear', linewidths = 0.1)
		plt.clabel(CS_lines, inline=0.1, fontsize = 7, colors='k', fmt=fmt)
	else:
		CS_Topo = plt.contourf(matrix_east,matrix_north,Topography, 100, alpha = 1.0, cmap = cmapg ,antialiased=True)
		CS_Sea = plt.contourf(matrix_east,matrix_north,Topography_Sea, 100, alpha = 0.5, cmap = cmaps ,antialiased=True)
		CS = plt.contourf(matrix_east,matrix_north,data_cones, 100, alpha= 0.3, cmap=cmapr, antialiased=True)
	
	plt.axes().set_aspect(1.0)
	plt.xlabel('East [m]')
	plt.ylabel('North [m]')
	plt.xlim(east_cor, east_cor + cellsize * (n_east - 1) )
	plt.ylim(north_cor,north_cor +cellsize * (n_north - 1) )

	for i in range(0,N):
		plt.plot( east_cen_vector[i], north_cen_vector[i], 'r.', markersize = 2 )

	if( N == 1 ):
		for i in range(1,len(polygon)):
			plt.plot( polygon[i][0], polygon[i][1], 'b.', markersize = 2 )

	plt.savefig('Results/' + run_name + '/Map.png')

	if( N > 1 ):

		plt.figure(2)
		plt.subplot(131)
		plt.hist(volume_vector)
		plt.xlabel('Volume $[m^3]$')
		plt.subplot(132)
		plt.hist(phi_0_vector)
		plt.xlabel('phi_0')
		plt.subplot(133)
		plt.hist(ws_vector)
		plt.xlabel('Sedimentation velocity [m/s]')
		plt.savefig('Results/' + run_name + '/Histogram.png')

	plt.show()

file_log = open('Results/' + run_name + '/log.txt','w')
file_log.write('1')
file_log.close()
