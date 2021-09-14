import imageio
import configparser, os, datetime
import glob
from PIL import Image

#get filenames
config= configparser.ConfigParser()
prog_config = configparser.ConfigParser()
prog_config.read('program_config.ini')
config.read('project_config.ini')
file_list = []
save_dir = os.path.join(os.environ['USERPROFILE'], 'Pictures', 'Local_Logic_Export')
for project in config:
    if project == 'DEFAULT':
            continue
    
    project_files = []
    workspace_name = config[project]['workspace']
    for filename in os.listdir(save_dir):
        if filename.startswith("_".join([workspace_name, project])):
            project_files.append(os.path.join(save_dir,filename))


    save_as_name = "_".join([workspace_name, project, datetime.date.today().strftime('%Y-%m-%d')]) + ".gif"
    fp_out = os.path.join(save_dir,save_as_name)



    img, *imgs = [Image.open(f) for f in project_files]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=200, loop=0)
