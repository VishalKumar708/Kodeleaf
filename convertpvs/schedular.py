import os
import datetime
import pathlib
import shutil
from .generatexml import generate_xml
from .models import audit_log, Add_Profile
import logging

#
# gloabal variables
in_file_path,out_file_path,archieve_path,allprofiles,profile_name = '', '', '', '', ''
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

def scheduled():
    assign_path()
    files = os.listdir(in_file_path)

    for i in files:

        get_value = i
        file_perfix = get_value.split('.xml')[0]
        file_extension = pathlib.Path(get_value).suffix.lower()
        if file_extension == '.xml':
            file_suffix = '_r3_converted'
            in_file = get_value  # for database(in_file_name)
            out_file = file_perfix + file_suffix + '.xml'  # for database(out_file name)
            if generate_xml((os.path.join(in_file_path, in_file)), (os.path.join(out_file_path, out_file))):
                status = 'Success'
                creation_time = os.path.getmtime(f'{out_file_path}\\{out_file}')  # for database(modification time)
                x = datetime.datetime.fromtimestamp(creation_time)
                # to sent data into database
                obj = audit_log(profile_name=user_profile_name, in_file_name=in_file, out_file_name=out_file, converted_datetime=x.strftime('%d-%b-%Y %I-%M %p'),
                                user_name='cron tab', status=status)
                obj.save()
                shutil.move(os.path.join(in_file_path, get_value), os.path.join(archieve_path, get_value))

            else:
                x = datetime.datetime.now()
                status = 'Failed'
                obj = audit_log(profile_name=user_profile_name,in_file_name=in_file, out_file_name='null', converted_datetime=x.strftime('%d-%b-%Y %I-%M %p'),
                                user_name='cron_tab', status=status)
                obj.save()
