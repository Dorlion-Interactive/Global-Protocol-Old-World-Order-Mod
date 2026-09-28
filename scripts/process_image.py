import cv2
import numpy as np
import os
import sys

def process_and_save(src_path, category, dest_id):
    bg_color = (12, 16, 22) # BGR: (22, 16, 12)

    im_raw = cv2.imread(src_path, cv2.IMREAD_UNCHANGED)
    if im_raw is None:
        print(f"Error: could not read {src_path}")
        sys.exit(1)

    has_alpha = len(im_raw.shape) == 3 and im_raw.shape[2] == 4
    if has_alpha:
        im_bgr = im_raw[:, :, :3]
        orig_alpha = im_raw[:, :, 3]
    else:
        im_bgr = im_raw
        orig_alpha = None

    h, w = im_bgr.shape[:2]
    gray = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2GRAY)
    _, white_mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(white_mask, connectivity=8)
    border_labels = set(np.unique(np.concatenate([labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]]))) - {0}
    combined_mask = np.zeros((h, w), dtype=np.float32)
    safe_y1, safe_y2 = int(h * 200 / 1024), int(h * 824 / 1024)
    safe_x1, safe_x2 = int(w * 200 / 1024), int(w * 824 / 1024)
    for l in border_labels:
        mask_l = (labels == l)
        # Protect central safe box
        if not mask_l[safe_y1:safe_y2, safe_x1:safe_x2].any():
            combined_mask[mask_l] = 1.0

    if np.any(combined_mask > 0):
        print(f"Cleaned outer border white components for {dest_id}")
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(combined_mask, kernel)
        smooth_mask = cv2.GaussianBlur(dilated, (3, 3), 0.5)
        alpha = (1.0 - smooth_mask)[:, :, np.newaxis]
        bg_bgr = np.array([bg_color[2], bg_color[1], bg_color[0]], dtype=np.float32)
        im_bgr = (im_bgr.astype(np.float32) * alpha + bg_bgr * (1.0 - alpha)).clip(0, 255).astype(np.uint8)
    else:
        print(f"No border white found for {dest_id}")

    if orig_alpha is not None:
        im_out = cv2.merge([im_bgr[:, :, 0], im_bgr[:, :, 1], im_bgr[:, :, 2], orig_alpha])
    else:
        im_out = im_bgr

    # Downscale to 512x512
    if im_out.shape[0] != 512 or im_out.shape[1] != 512:
        im_out = cv2.resize(im_out, (512, 512), interpolation=cv2.INTER_AREA)

    target = f"icons/{category}/{dest_id}.png"
    os.makedirs(os.path.dirname(target), exist_ok=True)
    cv2.imwrite(target, im_out)
    print(f"Successfully saved {dest_id} to {target} (512x512).")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python process_image.py <src_path> <category> <dest_id>")
        sys.exit(1)
    src = sys.argv[1]
    cat = sys.argv[2]
    dest = sys.argv[3]
    process_and_save(src, cat, dest)
