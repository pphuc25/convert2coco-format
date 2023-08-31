
import json
import argparse

def config():
    parser = argparse.ArgumentParser(description='After correct the default format of json file, run this to merge then together')
    parser.add_argument('--json_path_1', type=str, default=None,
                                    help='path to file json want to edit')
    parser.add_argument('--json_path_2', type=str, default=None,
                                    help='path to file json want to edit')
    parser.add_argument('--name_file_output', type=str, default=None,
                                    help='name of file after edit (do not need to put extension)')
    
    args = parser.parse_args()
    
    # Sanity check
    if args.json_path_1 is None or args.json_path_2 is None or args.name_file_output is None:
        raise ValueError("Need both path data to edit and name of file to output.")
    return args

def main():
    """
    Merge 2 json files to a new json file
    """
    args = config()

    with open(args.json_path_1) as f:
        old_file = json.load(f)

    with open(args.json_path_2) as f:
        new_file = json.load(f)

    output_file = merge_json(old_file, new_file)

    with open(f"{args.name_file_output}.json", 'w') as s:
        json.dump(output_file, s)

def merge_json(old_file: json, new_file: json)-> json:
    """
    iterate json and save log of iamge id
    after that merge by columns
    return: json file as a combination of both json files input
    """
    # init a list to save image_id
    save_id_old_annos = []

    # get lenght of the old json
    len_old_json = len(old_file['annotations'])

    # iterate each json file to save image_id to list
    for block in old_file['annotations']:
        save_id_old_annos.append(block['image_id'])

    # Add with len of old_file index to increase the new index of image_id
    for block in new_file['annotations']:
        save_id_old_annos.append(int(block['image_id']) + int(len_old_json))
    # same for id in images column
    for index, block in enumerate(new_file['images']):
        block['id'] = int(len_old_json) + index

    # merge images column
    old_file['images'].extend(new_file['images'])

    # merge annotations column
    old_file['annotations'].extend(new_file['annotations'])

    # reset index of each column
    for index, _ in enumerate(old_file['images']):
        old_file['images'][index]['id'] = index

    # load saved image_id and reset index of column
    for index, _ in enumerate(old_file['annotations']):
        old_file['annotations'][index]['id'] = index + 1
        old_file['annotations'][index]['image_id'] = save_id_old_annos[index]

    return old_file

if __name__ == "__main__":
    main()