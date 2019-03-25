# Name of the run (used to save the parameters and the output)
run_name = Vesuvius

# Source of DEM 
# source_dem = type of input data (1 => SRTM 30 m / 2 => Uploaded DEM (UTM) / 3 => Uploaded Data (lat,lon)). 
#              (A default location is assumed for type 2: input_DEM.asc, see an example in EXAMPLES/Upload_DEM_UTM).
#              (A default location is assumed for type 3: Topography_3.asc, see an example in EXAMPLES/Upload_DEM_deg).
#              (Simulations with source_dem = 1 and save_data = 1 create a compatible file for source_dem = 3 in Results).
source_dem = 1

# Map limits (only considered if source_dem = 1)
# lon1 = longitude of the first limit of the map
# lon2 = longitude of the second limit of the map 
# lat1 = latitude of the first limit of the map
# lat2 = latitude of the second limit of the map
lon1 = 14.2
lon2 = 14.7
lat1 = 40.6
lat2 = 41.0

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
lon_cen = 14.427
lat_cen = 40.822
var_cen = 300.0

# Other parameters of box model
# volume = collapsing volume (in cubic meters)
# ws = settling velocity
# c_const = parameter C
# var_volume = uncertainty of collapsing volume (in cubic meters)
# var_ws = uncertainty of settling velocity
# var_c_const = uncertainty of C
# dist_input = type of distribution for volume, ws and c (1 => Gaussian / 2 => Uniform)
volume = 400000000.0
ws = 0.3
c_const = 1.7
var_volume = 20000000.0
var_ws = 0.2
var_c_const = 0.7
dist_input = 2

# Number of simulations computed by the code
N = 300

# Save results in files txt ( 1 => Yes / 0 => No )
save_data = 1

# Assumption for redistributing pyroclastic material (1, 2, 3 or 4. Please use 4)
redist_energy = 4
