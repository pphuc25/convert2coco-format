
import json
import argparse

def config():
    parser = argparse.ArgumentParser(description='Change the format from robotflow to correct format for annotation file')
    parser.add_argument('--path_data_annotation', type=str, default=None,
                                    help='path to file json want to edit')
    parser.add_argument('--name_file_output', type=str, default=None,
                                    help='name of file after edit (do not need to put extension)')
    
    args = parser.parse_args()
    
    # Sanity check
    if args.path_data_annotation is None or args.name_file_output is None:
        raise ValueError("Need both path data to edit and name of file to output.")
    return args

old_json = '/Users/mike/vcs/github.com/frostyotter/digital-race-race-C/src/convert_format/_annotations.coco.json'
new_json = '/Users/mike/vcs/github.com/frostyotter/digital-race-race-C/new_file.json'

valid_images_keys = ['id', 'file_name', 'height', 'width']

def reset_index_images(old_file, new_file):

    with open(old_file) as f:
        old_file = json.load(f)
    with open(new_file) as f:
        new_file = json.load(f)

    save_id_old_annos = []

    for index, block in enumerate(old_file['annotations']):
        save_id_old_annos.append(block['image_id'])

    for index, block in enumerate(new_file['annotations']):
        save_id_old_annos.append(block['image_id'])

    save_id_old_annos.append(new_file['annotations'][index]['image_id'] for index in range(len(new_file['annotations'])))
    old_file['images'].extend(new_file['images'])

    old_file['annotations'].extend(new_file['annotations'])

    for index, _ in enumerate(old_file['images']):
        old_file['images'][index]['id'] = index

    for index, _ in enumerate(old_file['annotations']):
        old_file['annotations'][index]['id'] = index + 1
        old_file['annotations'][index]['image_id'] = save_id_old_annos[index]

    with open('/Users/mike/vcs/github.com/frostyotter/digital-race-race-C/output.json', 'w') as f:
        json.dump(old_file, f)

reset_index_images(old_json, new_json)