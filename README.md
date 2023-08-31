# Change the format of annotation file to coco format
For the task of object recognition and object detection, various file annotation formats exist. However, the widely used format is COCO. In our specific task, we require annotations to adhere to a custom-defined format, utilizing the same keys within dictionaries. This repository has been created with the intention of assisting others in seamlessly converting their annotation formats to COCO, tailored to their unique tasks.

Thanks to contributors [@frostyOtter](https://github.com/frostyOtter), [@andythetechnerd03](https://github.com/andythetechnerd03) and[@justinvo277](https://github.com/justinvo277)

## How to use code
To run the file, use the command:

    python src/convert_format.py

In other to change the format specific, change three values `valid_keys`, `valid_images_keys`, `name_2_id` in `src/custome_labels.py`

*You can add the data you want to change in folder data and then change direction in `config/main.yaml` (change the `path_data_annotation` and `name_file_output`)*