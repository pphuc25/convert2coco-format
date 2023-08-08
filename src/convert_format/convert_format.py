import argparse
import os
import json
from typing import List

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

valid_keys = ['images', 'categories', 'annotations']
valid_images_keys = ['id', 'file_name', 'height', 'width']
name_2_id = {'stop': 1, 'left': 2, 'right': 3, 'straight': 4, 'no_left': 5, 'no_right': 6}

def main():
    """
    Correct the format of json file and save to new file
    """
    args = config()

    with open(args.path_data_annotation) as f:
        file_edit = json.load(f)

    file_edit = rm_unrelate_keys(file_edit)
    file_edit = rm_unrelate_in_image(file_edit)
    dict_transform, file_edit = correct_id_categories(file_edit)
    file_edit = correct_area_categoryid(file_edit, dict_transform)

    with open(f"{args.name_file_output}.json", "w") as s:
        json.dump(file_edit, s)
    
def rm_unrelate_keys(file_edit: dict[List]) -> dict[List]:
    """
    Remove any keys of annotation file that not in `images`, `categories`, `annotations`
    """
    keys_rm: list = [key_check for key_check in file_edit.keys() if key_check not in valid_keys]
    
    if keys_rm is None: return file_edit
    for key_rm in keys_rm: del file_edit[key_rm]
    return file_edit

def rm_unrelate_in_image(file_edit: dict) -> dict:
    """
    Remove any key in image that not in `id`, `file_name`, `height`, `width`
    and change all `file_name` to basename
    """
    keys_image_rm: list = [key_check for key_check in file_edit['images'][0].keys() if key_check not in valid_images_keys]
    if keys_image_rm is None: return file_edit
    
    # Sanity check ---
    change_name: bool = False
    file_name_check: str = file_edit['images'][0]['file_name']
    if file_name_check != os.path.basename(file_name_check): change_name = True
    # ---

    for value_list in file_edit['images']:
        if change_name == True: value_list['file_name'] = os.path.basename(value_list['file_name'])
        for key_image_rm in keys_image_rm: del value_list[key_image_rm]
    return file_edit

def correct_id_categories(file_edit: dict[List]) -> dict[List]:
    """
    Correct all categories index, delete categories not in 6 sign
    and add key `supercategory: trafficsign` 
    """
    dict_transform, no_related_tag = {}, []
    for idx, value_cate_list in enumerate(file_edit['categories']):
        if value_cate_list['name'] not in name_2_id.keys():
            no_related_tag.append(idx)
            continue
        value_cate_list['supercategory'] = 'trafficsign'
        dict_transform[value_cate_list['id']] = name_2_id[value_cate_list['name']]
        value_cate_list['id'] = name_2_id[value_cate_list['name']]

    if no_related_tag is None: return dict_transform, file_edit
    for value_delete in no_related_tag: file_edit['categories'].pop(value_delete)

    return dict_transform, file_edit

def correct_area_categoryid(file_edit:dict, dict_transform: dict[List]) -> dict[List]:
    """
    Change area to int and correct category id base on dictionary
    """
    for value_anno_list in file_edit['annotations']:
        value_anno_list['area'] = int(value_anno_list['area'])
        value_anno_list['category_id'] = dict_transform[value_anno_list['category_id']]
    return file_edit

if __name__ == "__main__":
    main()