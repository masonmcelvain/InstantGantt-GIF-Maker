import configparser, os, datetime
import dateutil.parser as dparser
import dateutil.relativedelta
from pathlib import Path
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MONTH_AGO = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=1)

#get filenames
config= configparser.ConfigParser()
prog_config = configparser.ConfigParser()
prog_config.read('program_config.ini')
config.read('project_config.ini')
file_list = []
save_dir = os.path.join(os.environ['USERPROFILE'], 'Pictures', 'Local_Logic_Export')
#make save directory if needed
Path(save_dir).mkdir(parents=True, exist_ok=True)
print(f"Saving to {save_dir}")

if prog_config['Paths']['save_directory'][0] == '~':
    img_dir = os.path.expanduser(prog_config['Paths']['save_directory'])
else:
    img_dir = prog_config['Paths']['save_directory']
print(f"Reading images in {img_dir} from {ROOT_DIR}")

for project in config:
    if project == 'DEFAULT':
            continue

    project_files = []
    workspace_name = config[project]['workspace']
    for filename in os.listdir(img_dir):
        if filename.startswith("_".join([workspace_name, project])):
            file_date = dparser.parse(filename, fuzzy=True)
            if file_date >= MONTH_AGO:
                project_files.append(os.path.join(img_dir, filename))

    save_as_name = "_".join([workspace_name, project, datetime.date.today().strftime('%Y-%m-%d')]) + ".gif"
    fp_out = os.path.join(save_dir,save_as_name)

    img, *imgs = [Image.open(f) for f in project_files]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=200, loop=0)

    print(f"Saved {project} successfully")
