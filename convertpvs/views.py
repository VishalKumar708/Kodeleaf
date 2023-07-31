from django.shortcuts import render
from django.http import  FileResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Add_Profile, audit_log
from .generatexml import generate_xml
from .Validatexml import validate_xml
import logging
import os
import datetime
import pathlib
import shutil
import glob
import zipfile
import datetime

# folder paths
# gloabal variables
in_file_path,out_file_path,archieve_path,allprofiles,profile_name = '', '', '', '',''
def assign_path():
    global in_file_path,out_file_path,archieve_path,allprofiles, user_profile_name
    allprofiles = Add_Profile.objects.all()
    firstprofile = Add_Profile.objects.first()
    in_file_path = ''
    out_file_path = ''
    archieve_path = ''
    user_profile_name=''
    if firstprofile:
        in_file_path = firstprofile.in_file_path
        out_file_path = firstprofile.out_file_path
        archieve_path = firstprofile.archieve_path
        user_profile_name = firstprofile.profile_name

    else:
        logger = logging.getLogger('convertpvs')
        logger.error('file path is not set.')

logger = logging.getLogger('convertpvs')
def r2(path):
    files_details = []
    dir_name = f'{path}\\'
    # Get list of all files only in the given directory
    list_of_files = filter(os.path.isfile, glob.glob(dir_name + '*'))
    # Sort list of files based on last modification time in ascending order
    files = sorted(list_of_files, key=os.path.getmtime, reverse=True)
    # files = os.listdir(path)
    # important
    if len(files) > 0:
        for a in files:
            i = os.path.split(a)[1]
            individual_file_details = []
            file_name = f'{path}\\{i}'
            if pathlib.Path(file_name).suffix.lower() == '.xml':
                # file name
                individual_file_details.append(i)

                # file size
                size = os.path.getsize(file_name) / (1024)
                individual_file_details.append(f'{int(round(size,0))} KB')

                # file modification time
                modification_time = os.path.getmtime(file_name)
                y = datetime.datetime.fromtimestamp(modification_time)
                individual_file_details.append(y.strftime('%d-%b-%Y %I:%M %p'))

                files_details.append(individual_file_details)
    return files_details


def r3(path):
    files_details = []

    dir_name = f'{path}\\'
    # Get list of all files only in the given directory

    list_of_files = filter(os.path.isfile, glob.glob(dir_name + '*'))
    # Sort list of files based on last modification time in ascending order
    files = sorted(list_of_files, key=os.path.getmtime, reverse=True)

    # important
    if len(files) > 0:
        for a in files:
            i = os.path.split(a)[1]
            file_name = f'{path}\\{i}'
            individual_file_details = []

            if pathlib.Path(file_name).suffix.lower() == '.xml':
                # file name
                individual_file_details.append(i)

                # file size
                size = os.path.getsize(file_name) / (1024)
                individual_file_details.append(f'{int(round(size,0))} KB')

                # file creation time
                creation_time = os.path.getmtime(file_name)
                x = datetime.datetime.fromtimestamp(creation_time)

                individual_file_details.append(x.strftime('%d-%b-%Y %I:%M %p'))

                files_details.append(individual_file_details)
    return files_details


# ------------------------------------------------------------    END Function
@login_required(login_url='/')
def get_all_data(request):
    if request.user.is_authenticated:
        assign_path()
        try:

            r2_file_data = r2(path=in_file_path)
            r3_file_data = r3(path=out_file_path)
            data = {
                # 'xml' and 'json' files details
                'r2_files': r2_file_data,
                'r3_files': r3_file_data,
                'allprofile': allprofiles,
                # # no. of 'json' and 'xml' file
                'r2_count': len(r2_file_data),
                'r3_count': len(r3_file_data),
            }

            return render(request, 'admin/index.html', data)
        except Exception as e:
            logger.error(f'IN Viewing: get_all_data function error {e}')
            return render(request, 'admin/index.html')
    else:
        return render(request, 'admin/login.html')



def download_file(request, file,view,viewr3):
    assign_path()
    try:
        # help to download single file
        path = out_file_path
        file_path = os.path.join(path, file)
        response = FileResponse(open(file_path, 'rb'))
        file_name = file
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        logger.info(f'Download file: success! {file_name}')
        return response
    except Exception as e:
        logger.error(f'Download file :failed123!  Error( {e})')


def view_file(request, file, view):
    assign_path()
    try:
        if view == 'r2':
            path = in_file_path
        else:
            path = out_file_path

        file_path = os.path.join(path, file)
        response = FileResponse(open(file_path, 'rb'))
        file_name = file
        response['Content-Disposition'] = 'inline; filename=' + file_name
        logger.info(f'view file: success! {file}')
        return response
    except Exception as e:
        logger.error(f'view file :failed!  Error( {e})')
        logger.info(f'{file} viewed failed')


# ***************************************************************************************************
def download_zip_files(request):
    assign_path()
    try:
        # help to download multiple files
        data = str(request.GET['post_id'])
        multiple_file_names = data.split(',')
        path = out_file_path
        print(multiple_file_names)
        zip_file_name = os.path.join(path, "SelectedFile.zip")
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            for i in multiple_file_names:
                if i.endswith('.xml'):
                    # file_name = os.path.basename(path + i)
                    file_name = os.path.basename(os.path.join(path, i))
                    # zip_file.write(path+i, file_name)
                    zip_file.write(os.path.join(path, i), file_name)

        file_path = os.path.join(path, 'SelectedFile.zip')

        response = FileResponse(open(file_path, 'rb'))
        file_name = 'SelectedFile.zip'
        response['Content-Disposition'] = 'attachment; filename =' + file_path
        logger.info(f'Download zip: success!')
        return response
    except Exception as e:
        logger.error(f'Download zip:failed! Error({e})')


logger = logging.getLogger('my_app')  # Replace 'my_app' with a suitable logger name
logger.setLevel(logging.DEBUG)  # Set the desired log level

def validate(request):
    assign_path()
    path = os.path.join(out_file_path, 'temp')
    os.makedirs(path, exist_ok=True)
    current_datetime = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
    log_file = f'logger/log_{current_datetime}.log'
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    file_handler = logging.FileHandler(log_file, mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if len(os.listdir(path))>0:
        for i in os.listdir(path):
            files=os.path.join(path, i)
            try:
                shutil.rmtree(files)
            except OSError:
                os.remove(files)

    source=out_file_path
    temp_files =request.GET['file_name'].split(',')
    for file in temp_files:
        shutil.copy(os.path.join(source, file), path)
    # validate_xml(path,log_file,logger)
    if validate_xml(path,log_file,logger) == True:
        return HttpResponse(" Validation Success!!!")
    else:
        return HttpResponse("Validation Failed!!!")



def convertfiles(request):
    assign_path()
    logger.info(str(request.GET['post_id']))
    try:

        data = str(request.GET['post_id'])
        multiple_file_names = data.split(',')
        print(multiple_file_names)
        for i in multiple_file_names:
            print(i)
            get_value = i
            # copy file frome one location to another

            try:
                file_perfix = get_value.split('.xml')[0]
                file_suffix = '_r3_converted'
                in_file = get_value  # for database(in_file_name)
                out_file = file_perfix + file_suffix + '.xml'  # for database(out_file name)
                if generate_xml((os.path.join(in_file_path, in_file)), (os.path.join(out_file_path, out_file))):

                    status = 'Success'
                    creation_time = os.path.getmtime(
                        os.path.join(out_file_path, out_file))  # for database(modification time)
                    converted_time = datetime.datetime.fromtimestamp(creation_time)

                    # to sent data into database
                    obj = audit_log(profile_name=user_profile_name,in_file_name=in_file, out_file_name=out_file,
                                    converted_datetime=converted_time.strftime('%d-%b-%Y %I-%M %p'), user_name=request.user.first_name,
                                    status=status)
                    obj.save()
                    shutil.move(os.path.join(in_file_path, get_value),
                                os.path.join(archieve_path, get_value))
                    logger.info(f'file conversion: success! {get_value}')

                else:
                    x = datetime.datetime.now()
                    status = 'Failed'
                    obj = audit_log(profile_name=user_profile_name, in_file_name=in_file, out_file_name='null',
                                    converted_datetime=x.strftime('%d-%b-%Y %I-%M %p'), user_name=request.user.first_name,
                                    status=status)

                    obj.save()
                    shutil.move(os.path.join(in_file_path, get_value),
                                os.path.join(archieve_path, get_value))
                    logger.info(f'file conversion: failed! {get_value}')


            except  Exception as e:
                logger.error('file conversion method:failed! An error occurred while conversion', e)
        return render(request, 'admin/index.html')
    except Exception as e:
        logger.error(f'fie conversion :failed!  Error({e})')



