import argparse
import os
import cv2
from PIL import Image
from torchvision import transforms
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from typing import List, Tuple, Dict, Any
from detectron2.data import MetadataCatalog
import numpy as np
from utils.visualiser import Visualizer
from matplotlib import pyplot as plt
import time

def inference_sam_m2m_auto(model, image_path: str, label_mode='1', alpha=0.1, anno_mode=['Mask', 'Mark']) -> Tuple[Image.Image, List[Dict[str, Any]]]:
    """
    Perform inference using SAM model with M2M automatic prompting.
    """
    image = Image.open(image_path)
    image_ori = transforms.Resize((512, 512), interpolation=Image.BICUBIC)(image)
    image_ori = np.asarray(image_ori)

    mask_generator = SamAutomaticMaskGenerator(model)
    outputs = mask_generator.generate(image_ori)
    visual = Visualizer(image_ori, metadata=MetadataCatalog.get('coco_2017_train_panoptic'))
    sorted_anns = sorted(outputs, key=(lambda x: x['area']), reverse=True)
    label = 1
    mask_map = np.zeros(image_ori.shape, dtype=np.uint8)    

    for i, ann in enumerate(sorted_anns):
        mask = ann['segmentation']
        color_mask = np.random.random((1, 3)).tolist()[0]
        # color_mask = [int(c*255) for c in color_mask]
        demo = visual.draw_binary_mask_with_number(mask, text=str(label), label_mode=label_mode, alpha=alpha, anno_mode=anno_mode)
        # assign the mask to the mask_map
        mask_map[mask == 1] = label
        label += 1
    im = demo
    # fig=plt.figure(figsize=(10, 10))
    # plt.imshow(image_ori)
    # show_anns(outputs)
    # fig.canvas.draw()
    # im=Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())  
    return im, sorted_anns
    
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)
    polygons = []
    color = []
    for ann in sorted_anns:
        m = ann['segmentation']
        img = np.ones((m.shape[0], m.shape[1], 3))
        color_mask = np.random.random((1, 3)).tolist()[0]
        for i in range(3):
            img[:,:,i] = color_mask[i]
        ax.imshow(np.dstack((img, m*0.35)))

def process_images(input_dir: str, output_dir: str, model, interval: int = 1) -> None:
    """
    Process a directory of images, running SAM inference and SoM prompting.
    Displays results intermittently based on the specified interval.
    """
    image_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.tif')]
    for i, image_path in enumerate(image_paths):
        print(f"Processing {image_path}...")
        start_time = time.time()
        result_image, annotations = inference_sam_m2m_auto(model, image_path)
        result_image.save(os.path.join(output_dir, f"processed_{os.path.basename(image_path)}"))
        
        # Every `interval` images, display the current result for manual check
        if i % interval == 0:
            # plt.imshow(result_image)
            # plt.title(f"Processed {os.path.basename(image_path)}")
            # plt.show()
            input("Press Enter to continue...")

        print(f"Finished processing {image_path} in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a folder of images with SoM prompting.")
    parser.add_argument("--input_dir", required=True, help="Directory containing images to process.")
    parser.add_argument("--output_dir", required=True, help="Directory to save processed images.")
    parser.add_argument("--checkpoint", required=True, help="Path to the SAM model checkpoint.")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Load the SAM model
    print("Loading SAM model...")
    sam_model = sam_model_registry["vit_h"](checkpoint=args.checkpoint)
    sam_model.to(device="cuda")

    # Process the images
    process_images(args.input_dir, args.output_dir, sam_model)
