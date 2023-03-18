"""
HAWKI DATA REDUCTION SCRIPT - v1.0 (2023)

To run this script call you need firt to first copy the science files into the main folder
After that, you need to launch the following command:

> python HAWKI-quickred.py

The script will check for the filter(s) for the data into the folder
and then it will ask which filter to reduce first

REQUISITES: astropy, CPL libraries, shutil
"""

from astropy.io import fits
import glob,sys,os,shutil
from subprocess import call

# Ask the user for the directory where the calibration data is located
science_data_directory = os.getcwd()
os.chdir(science_data_directory)
# 
data_files = glob.glob(str(science_data_directory + '/HAWKI.*fits'))
calib_data = science_data_directory+'/calib/'

#determine the number of filters in the dataset
filters = []
for i in range(len(data_files)):
    temp = fits.open(data_files[i])
    try:
        hierarch = temp[0].header['HIERARCH ESO INS FILT1 NAME']
    except:
        pass
    if hierarch in filters:
        pass
    else:
        filters.append(hierarch)

#create output folders for each grism
for item in filters:
    try:
        os.makedirs('output_'+item)
    except:
        pass

#show which grisms have been observed
print('')
if len(filters) == 1:
	print("There is only the "+str(filters[0])+" dataset")
	filt = filters[0]
elif len(filters) == 0:
	print("Something went wrong with the static calibration files ! Check better.")
else:
    print("There are "+str(len(filters))+" filters in the dataset.")
    print('')
    print("List of datasets/filters : ")
    for i in range(len(filters)):
        print('')
        print(filters[i])
        print('')
    filt = input('Which filter do you want to reduce ? ')
    if filt in filters:
        flt = filt
        print('')
    else:
        print('This filter is not in the dataset ! Sorry, you need to start from the beginning :(')
        sys.exit[0]





#search for catalogs
MASTER_2MASS_CATALOGUE_ASTROM = 'MASTER_2MASS_CATALOGUE_ASTROM.fits'
MASTER_2MASS_CATALOGUE_PHOTOM = 'MASTER_2MASS_CATALOGUE_PHOTOM.fits'
SCHLEGEL_MAP_NORTH = 'SCHLEGEL_MAP_NORTH.fits'
SCHLEGEL_MAP_SOUTH = 'SCHLEGEL_MAP_SOUTH.fits'
MASTER_DARK = 'MASTER_DARK.fits'
MASTER_TWILIGHT_FLAT_J = 'MASTER_TWILIGHT_FLAT_J.fits'
MASTER_CONF_J = 'MASTER_CONF_J.fits'
MASTER_TWILIGHT_FLAT_H = 'MASTER_TWILIGHT_FLAT_H.fits'
MASTER_CONF_H = 'MASTER_CONF_H.fits'
MASTER_TWILIGHT_FLAT_Ks = 'MASTER_TWILIGHT_FLAT_Ks.fits'
MASTER_CONF_Ks = 'MASTER_CONF_Ks.fits'
PHOTCAL_TAB = 'PHOTCAL_TAB.fits'
MASTER_READGAIN = 'MASTER_READGAIN.fits'




# This for loop checks the header for each data file and determines what type it is.
# Now, we define functions that will help in creating sof files
# Creates a text file from a given input list.
def write_list(type_list, file_name):
    name = file_name
    try:
        f = open(name, "w")
        f.write("\n".join(map(lambda x: str(x), type_list)))
        f.close()
    except:
        print('Something went wrong! Can\'t write to the file: ' + name)
        sys.exit(0) # quit Python




def create_science_sof(flt):
    if True:
        science_list = []
        for i in range(len(data_files)):
            temp = fits.open(data_files[i])
            try:
                filt = temp[0].header['HIERARCH ESO INS FILT1 NAME']
                typ = temp[0].header['OBJECT']
                #print(filt)
            except:
                print('There is some problem in the input file - check with the WG-IS')
                #sys.exit(0)
            if filt == flt:
                science_list.append(data_files[i] + ' OBJECT')
        science_list.append(calib_data+MASTER_DARK + ' MASTER_DARK')
        if flt == 'H':
            science_list.append(calib_data+MASTER_TWILIGHT_FLAT_H + ' MASTER_TWILIGHT_FLAT')
            science_list.append(calib_data+MASTER_CONF_H + ' MASTER_CONF')
        elif flt == 'J':
            science_list.append(calib_data+MASTER_TWILIGHT_FLAT_J + ' MASTER_TWILIGHT_FLAT')
            science_list.append(calib_data+MASTER_CONF_J + ' MASTER_CONF')
        elif flt == 'Ks':
            science_list.append(calib_data+MASTER_TWILIGHT_FLAT_Ks + ' MASTER_TWILIGHT_FLAT')
            science_list.append(calib_data+MASTER_CONF_Ks + ' MASTER_CONF')
        science_list.append(calib_data+PHOTCAL_TAB + ' PHOTCAL_TAB')
        science_list.append(calib_data+MASTER_READGAIN + ' MASTER_READGAIN')
        science_list.append(calib_data+SCHLEGEL_MAP_NORTH + ' SCHLEGEL_MAP_NORTH')
        science_list.append(calib_data+SCHLEGEL_MAP_SOUTH + ' SCHLEGEL_MAP_SOUTH')
        science_list.append(calib_data+MASTER_2MASS_CATALOGUE_ASTROM + ' MASTER_2MASS_CATALOGUE_ASTROM')
        science_list.append(calib_data+MASTER_2MASS_CATALOGUE_PHOTOM + ' MASTER_2MASS_CATALOGUE_PHOTOM')
        write_list(science_list, science_data_directory+'/science.sof')
        print('')
        print('Created science.sof')


def create_postprocess_sof(flt):
    if True:
        postproc_list = []
        for file in os.listdir(science_data_directory):
            if file.startswith('exp'):
                temp = fits.open(file)
                catg = temp[0].header['HIERARCH ESO PRO CATG']
                if catg == 'BASIC_CALIBRATED_SCI':
                    postproc_list.append(science_data_directory+'/'+file + ' BASIC_CALIBRATED_SCI')
                elif catg == 'BASIC_VAR_MAP':
                    postproc_list.append(science_data_directory+'/'+file + ' BASIC_VAR_MAP')
        if flt == 'H':
            postproc_list.append(calib_data+MASTER_CONF_H + ' MASTER_CONF')
        elif flt == 'J':
            postproc_list.append(calib_data+MASTER_CONF_J + ' MASTER_CONF')
        elif flt == 'Ks':
            postproc_list.append(calib_data+MASTER_CONF_Ks + ' MASTER_CONF')
        postproc_list.append(calib_data+PHOTCAL_TAB + ' PHOTCAL_TAB')
        postproc_list.append(calib_data+SCHLEGEL_MAP_NORTH + ' SCHLEGEL_MAP_NORTH')
        postproc_list.append(calib_data+SCHLEGEL_MAP_SOUTH + ' SCHLEGEL_MAP_SOUTH')
        postproc_list.append(calib_data+MASTER_2MASS_CATALOGUE_ASTROM + ' MASTER_2MASS_CATALOGUE_ASTROM')
        postproc_list.append(calib_data+MASTER_2MASS_CATALOGUE_PHOTOM + ' MASTER_2MASS_CATALOGUE_PHOTOM')
        write_list(postproc_list, science_data_directory+'/postprocess.sof')
        print('')
        print('Created postprocess.sof')
    


# Here start the data reduction !!!

if True:
    try:
        create_science_sof(filt)
        #print("---Running HAWKI_science_process for target(s)---")
        call("esorex --log-file=science.log hawki_science_process --cdssearch_astrom='2mass' --cdssearch_photom='2mass' science.sof", shell = True)
        #print("---Running HAWKI_science_postprocess for target(s)---")
        create_postprocess_sof(filt)
        call("esorex --log-file=postprocess.log hawki_science_postprocess --cdssearch_astrom='2mass' --cdssearch_photom='2mass' postprocess.sof", shell = True)
        for file in os.listdir(science_data_directory):
            if file.startswith('tile'):
                shutil.copy(file, 'output_'+filt+'/'+file)
                os.remove(file)
            elif file.startswith('exp'):
                os.remove(file)
            elif file.startswith('stack'):
                os.remove(file)
            elif file.startswith('sky'):
                os.remove(file)
            elif file.endswith('sof'):
                os.remove(file)
    except:
        print('ERROR: Could not run HAWKI_science scripts for target(s)')
       

print('You have successfully reduced the images of your target !!!')
print('')
print('Final images are stored in the corresponding filter output folder')
print('')
print('Good work and enjoy !!!')
