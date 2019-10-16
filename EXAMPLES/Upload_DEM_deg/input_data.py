# Name of the run (used to save the parameters and the output)
run_name = Input_DEM_deg

# Source of DEM
# source_dem = type of input data (1 => SRTM 30 m / 2 => Uploaded DEM (UTM) / 3 => Uploaded Data (lat,lon)).
# topography_file = location of file containing topography (only used when source_dem = 2 or source_dem = 3).
# (see examples of source_dem = 2 in EXAMPLES/Upload_DEM_UTM and of source_dem = 3 in EXAMPLES/Upload_DEM_deg).
# (Simulations with source_dem = 1 and save_data = 1 create a compatible topography file for source_dem = 3 in Results
# called Topography_3.txt).
source_dem = 3
topography_file = 'Topography_3.txt'

# Map limits (only considered if source_dem = 1)
# lon1 = longitude of the first limit of the map
# lon2 = longitude of the second limit of the map 
# lat1 = latitude of the first limit of the map
# lat2 = latitude of the second limit of the map

# Maximum order of secondary collapses
max_levels = 30

# Probability distribution of collapse location (1 => Punctual / 2 => Linear / 3 => Circumference arch)
dist_source = 1

# Parameters of the collapse location
# lon_cen = longitude of the collapse zone center (only considered if source_dem = 1 or 3)
# lat_cen = latitude of the collapse zone center (only considered if source_dem = 1 or 3)
# east_cen = east coordinate of collapse zone center (only considered if source_dem = 2)
# north_cen = north coordinate of collapse zone center (only considered if source_dem = 2)
# var_cen = uncertainty of collapse position (in meters)
# azimuth_lin = azimuth of the line that define the collapse zone (in degrees, only considered if dist_source = 2)
# length_lin = length of the line that define the collapse zone (in meters, only considered if dist_source = 2)
# radius_rad = radius of the circumference arch that define the collapse zone (in meters, only considered if dist_source = 3)
# ang1_rad = initial angle of the circumference arch that define the collapse zone (in degrees, only considered if dist_source = 3. Anticlockwise)
# ang2_rad = initial angle of the circumference arch that define the collapse zone (in degrees, only considered if dist_source = 3. Anticlockwise)
lon_cen = -72.65
lat_cen = -42.835
var_cen = 300.0

# Other parameters of box model
# volume = collapsing volume (in cubic meters)
# ws = sedimentation velocity (m/s)
# phi_0 = initial concentration of particles
# Fr = Froude Number
# rho_p = pyroclast density (in kg/m3) 
# rho_gas = gas density in PDC (in kg/m3)
# var_volume = uncertainty of collapsing volume (in cubic meters)
# var_ws = uncertainty of sedimentation velocity (m/s)
# var_phi_0 = uncertainty of initial concentration of particles 
# var_Fr = uncertainty of Fr
# var_rho_p = uncertainty of pyroclast density (in kg/m3)
# var_rho_gas = uncertainty of gas density (in kg/m3)
# dist_input = type of distribution for volume, ws, phi_0, Fr, rho_p and rho_gas (1 => Gaussian / 2 => Uniform)
volume = 100000000.0
ws = 0.6
phi_0 = 0.01
Fr = 1.1
rho_p = 1500.0
rho_gas = 1.1
var_volume = 30000000.0
var_ws = 0.4
var_phi_0 = 0.005
var_Fr = 0.1
var_rho_p = 100.0
var_rho_gas = 0.1
dist_input = 2

# Number of simulations computed by the code
N = 100

# Save results in files txt ( 1 => Yes / 0 => No )
save_data = 1

# Assumption for redistributing pyroclastic material (1, 2, 3 or 4. Please use 4)
redist_energy = 4
