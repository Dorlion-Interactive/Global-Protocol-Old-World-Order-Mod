import cv2
import numpy as np
import os
import sys

def process_and_save(src_path, category, dest_ids):
    bg_color = (12, 16, 22) # BGR: (22, 16, 12)

    im_bgr = cv2.imread(src_path)
    if im_bgr is None:
        print(f"Error: could not read {src_path}")
        sys.exit(1)

    h, w = im_bgr.shape[:2]
    gray = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2GRAY)
    _, white_mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(white_mask, connectivity=8)
    border_labels = set(np.unique(np.concatenate([labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]]))) - {0}
    combined_mask = np.zeros((h, w), dtype=np.float32)
    for l in border_labels:
        mask_l = (labels == l)
        # Protect central safe box
        if not mask_l[200:824, 200:824].any():
            combined_mask[mask_l] = 1.0

    if np.any(combined_mask > 0):
        print(f"Cleaned outer border white components for {dest_ids[0]}")
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(combined_mask, kernel)
        smooth_mask = cv2.GaussianBlur(dilated, (3, 3), 0.5)
        alpha = (1.0 - smooth_mask)[:, :, np.newaxis]
        bg_bgr = np.array([bg_color[2], bg_color[1], bg_color[0]], dtype=np.float32)
        im_bgr = (im_bgr.astype(np.float32) * alpha + bg_bgr * (1.0 - alpha)).clip(0, 255).astype(np.uint8)
    else:
        print(f"No border white found for {dest_ids[0]}")

    for dest_id in dest_ids:
        target = f"icons/{category}/{dest_id}.png"
        os.makedirs(os.path.dirname(target), exist_ok=True)
        cv2.imwrite(target, im_bgr)
        print(f"Successfully saved {dest_id} to {target}.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python process_image.py <src_path> <category> <dest_id1> [dest_id2] ...")
        sys.exit(1)
    src = sys.argv[1]
    cat = sys.argv[2]
    dests = sys.argv[3:]
    process_and_save(src, cat, dests)
