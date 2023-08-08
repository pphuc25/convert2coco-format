import argparse
import json

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

name_2_id = {'stop': 1, 'left': 2, 'right': 3, 'straight': 4, 'no_left': 5, 'no_right': 6}

def main():
    args = config()

    with open(args.path_data_annotation) as f:
        file_edit = json.load(f)

    file_edit = rm_unrelate_keys(file_edit)
    file_edit = rm_unrelate_in_image(file_edit)
    dict_transform, file_edit = correct_id_categories(file_edit)
    file_edit = correct_area_categoryid(file_edit, dict_transform)

    with open(f"{args.name_file_output}.json", "w") as f:
        json.dump(file_edit, f)
    
def rm_unrelate_keys(file_edit):
    del file_edit['licenses']
    del file_edit['info']
    return file_edit

def rm_unrelate_in_image(file_edit):
    for value_list in file_edit['images']:
        del value_list['license']
        del value_list['date_captured']
    return file_edit

def correct_id_categories(file_edit):
    dict_transform, no_related_tag = {}, []
    for idx, value_cate_list in enumerate(file_edit['categories']):
        if value_cate_list['name'] not in name_2_id.keys():
            no_related_tag.append(idx)
            continue
        value_cate_list['supercategory'] = 'trafficsign'
        dict_transform[value_cate_list['id']] = name_2_id[value_cate_list['name']]
        value_cate_list['id'] = name_2_id[value_cate_list['name']]

    for value_delete in no_related_tag:
        file_edit['categories'].pop(value_delete)

    return dict_transform, file_edit

def correct_area_categoryid(file_edit, dict_transform):
    for value_anno_list in file_edit['annotations']:
        value_anno_list['area'] = int(value_anno_list['area'])
        value_anno_list['category_id'] = dict_transform[value_anno_list['category_id']]
    return file_edit

if __name__ == "__main__":
    main()