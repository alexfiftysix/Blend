ingredients = ['CHICKEN', 'BEEF', 'MUTTON', 'RICE', 'WHEAT', 'GEL']

costs = {'CHICKEN': 0.013,
         'BEEF': 0.008,
         'MUTTON': 0.010,
         'RICE': 0.002,
         'WHEAT': 0.005,
         'GEL': 0.001}

variables = {
    'PROTEIN': {
        'CHICKEN': 0.800,
        'BEEF': 0.200,
        'MUTTON': 0.150,
        'RICE': 0.000,
        'WHEAT': 0.040,
        'GEL': 0.000},
    'FAT': {
        'CHICKEN': 0.080,
        'BEEF': 0.100,
        'MUTTON': 0.110,
        'RICE': 0.010,
        'WHEAT': 0.010,
        'GEL': 0.000},
    'FIBRE': {
        'CHICKEN': 0.001,
        'BEEF': 0.005,
        'MUTTON': 0.003,
        'RICE': 0.100,
        'WHEAT': 0.150,
        'GEL': 0.000},
    'SALT': {
        'CHICKEN': 0.002,
        'BEEF': 0.005,
        'MUTTON': 0.007,
        'RICE': 0.002,
        'WHEAT': 0.008,
        'GEL': 0.000}
}

requirements = {'PROTEIN': 8.0,
                'FAT': 6.0,
                'FIBRE': 2.0,
                'SALT': 0.4}