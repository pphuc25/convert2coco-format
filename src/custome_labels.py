valid_keys = ['images', 'categories', 'annotations']
valid_images_keys = ['id', 'file_name', 'height', 'width']
name_2_id = {'stop': 1, 'left': 2, 'right': 3, 'straight': 4, 'no_left': 5, 'no_right': 6}

def load_custome_labels(valid_keys=valid_keys, valid_images_keys=valid_images_keys, name_2_id=name_2_id):
    """
    This is the our custome keys of dict, key in image, the name of categories in
    which you can change by your own by just change in the below
    """
    return valid_keys, valid_images_keys, name_2_id