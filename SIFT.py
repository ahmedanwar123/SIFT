# # import cv2
# # import numpy as np


# # def gaussian_pyramid(img, num_octaves=4, scales_per_octave=5, sigma=1.6):
# #     pyramid = []
# #     k = 2 ** (1 / scales_per_octave)
# #     for octave in range(num_octaves):
# #         octave_imgs = []
# #         for scale in range(scales_per_octave + 3):
# #             sigma_eff = sigma * (k**scale)
# #             blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=sigma_eff, sigmaY=sigma_eff)
# #             octave_imgs.append(blurred)
# #         pyramid.append(octave_imgs)
# #         img = cv2.pyrDown(img)
# #     return pyramid


# # def dog_pyramid(gaussian_pyramid):
# #     dog_pyramid = []
# #     for octave in gaussian_pyramid:
# #         dogs = []
# #         for i in range(1, len(octave)):
# #             dogs.append(cv2.subtract(octave[i], octave[i - 1]))
# #         dog_pyramid.append(dogs)
# #     return dog_pyramid


# # def is_extremum(patch):
# #     center = patch[1, 1, 1]
# #     if center == np.max(patch):
# #         return True
# #     if center == np.min(patch):
# #         return True
# #     return False


# # def scale_space_extrem(dog_pyramid):
# #     keypoints = []
# #     for o, dogs in enumerate(dog_pyramid):
# #         for s in range(1, len(dogs) - 1):
# #             dog_prev = dogs[s - 1]
# #             dog_curr = dogs[s]
# #             dog_next = dogs[s + 1]
# #             h, w = dog_curr.shape
# #             for y in range(1, h - 1):
# #                 for x in range(1, w - 1):
# #                     patch = np.stack(
# #                         [
# #                             dog_prev[y - 1 : y + 2, x - 1 : x + 2],
# #                             dog_curr[y - 1 : y + 2, x - 1 : x + 2],
# #                             dog_next[y - 1 : y + 2, x - 1 : x + 2],
# #                         ]
# #                     )
# #                     if is_extremum(patch):
# #                         scale_factor = 2**o
# #                         keypoints.append(
# #                             cv2.KeyPoint(
# #                                 x * scale_factor, y * scale_factor, 1.6 * (2 ** (s / 3))
# #                             )
# #                         )
# #     return keypoints


# # # Load images
# # query_img = cv2.imread("SIFT/query.png", cv2.IMREAD_GRAYSCALE)
# # target_img = cv2.imread("SIFT/target.jpg", cv2.IMREAD_GRAYSCALE)

# # # Resize for consistency
# # query_img = cv2.resize(query_img, (512, 512))

# # # Normalize
# # query_img_f = query_img.astype(np.float32) / 255.0

# # # Detect keypoints from your functions
# # gauss = gaussian_pyramid(query_img_f)
# # dogs = dog_pyramid(gauss)
# # custom_kps = scale_space_extrem(dogs)

# # # Convert back to uint8 image for OpenCV descriptors ---
# # query_img_u8 = (query_img_f * 255).astype(np.uint8)

# # # --- Use SIFT to compute descriptors at your keypoints ---
# # sift = cv2.SIFT_create()
# # kp1, des1 = sift.compute(query_img_u8, custom_kps)

# # # Use SIFT normally on the target image
# # kp2, des2 = sift.detectAndCompute(target_img, None)

# # # Match descriptors
# # bf = cv2.BFMatcher()
# # matches = bf.knnMatch(des1, des2, k=2)

# # # Lowe's ratio test
# # good_matches = []
# # for m, n in matches:
# #     if m.distance < 0.75 * n.distance:
# #         good_matches.append(m)

# # # Draw matches
# # matched_img = cv2.drawMatches(
# #     query_img, kp1, target_img, kp2, good_matches, None, flags=2
# # )
# # cv2.imshow("Custom Keypoint Matches", matched_img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# import cv2
# import numpy as np
# from typing import List

# # Load grayscale images
# query_img: np.ndarray = cv2.imread("SIFT/query.png", cv2.IMREAD_GRAYSCALE)
# target_img: np.ndarray = cv2.imread("SIFT/target.jpg", cv2.IMREAD_GRAYSCALE)

# # SIFT detector
# sift = cv2.SIFT_create()

# # Detect keypoints and compute descriptors
# kp1, des1 = sift.detectAndCompute(query_img, None)
# kp2, des2 = sift.detectAndCompute(target_img, None)

# # Annotate the types separately
# kp1: List[cv2.KeyPoint]
# des1: np.ndarray
# kp2: List[cv2.KeyPoint]
# des2: np.ndarray

# # FLANN matcher
# FLANN_INDEX_KDTREE: int = 1
# index_params: dict = {"algorithm": FLANN_INDEX_KDTREE, "trees": 5}
# search_params: dict = {"checks": 50}
# flann = cv2.FlannBasedMatcher(index_params, search_params)
# matches: List[List[cv2.DMatch]] = flann.knnMatch(des1, des2, k=2)

# # Lowe's ratio test
# good_matches: List[cv2.DMatch] = []
# for m, n in matches:
#     if m.distance < 0.75 * n.distance:
#         good_matches.append(m)

# # Extract location of good matches
# if len(good_matches) >= 4:
#     src_pts: np.ndarray = np.float32(
#         [kp1[m.queryIdx].pt for m in good_matches]
#     ).reshape(-1, 1, 2)
#     dst_pts: np.ndarray = np.float32(
#         [kp2[m.trainIdx].pt for m in good_matches]
#     ).reshape(-1, 1, 2)

#     # Compute homography
#     H: np.ndarray = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)[0]

#     if H is not None:
#         # Get query image corners
#         h, w = query_img.shape
#         corners: np.ndarray = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(
#             -1, 1, 2
#         )
#         projected_corners: np.ndarray = cv2.perspectiveTransform(corners, H)

#         # Draw bounding box on target image
#         target_img_col: np.ndarray = cv2.cvtColor(target_img, cv2.COLOR_GRAY2BGR)
#         cv2.polylines(
#             target_img_col,
#             [np.int32(projected_corners)],
#             isClosed=True,
#             color=(0, 255, 0),
#             thickness=3,
#         )

#         # Draw matches
#         result_img: np.ndarray = cv2.drawMatches(
#             query_img,
#             kp1,
#             target_img_col,
#             kp2,
#             good_matches,
#             None,
#             flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
#         )
#         cv2.imshow("SIFT Object Detection", result_img)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#     else:
#         print("Homography could not be computed.")
# else:
#     print("Not enough good matches found - at least 4 required.")


import cv2
import numpy as np
from typing import List
from numba import njit

# --------------------- Numba-accelerated ratio test ---------------------
@njit
def filter_indices(distances: np.ndarray) -> List[int]:
    result = []
    for i in range(distances.shape[0]):
        if distances[i, 0] < 0.75 * distances[i, 1]:
            result.append(i)
    return result

# --------------------- Load images in grayscale ---------------------
query_img: np.ndarray = cv2.imread("SIFT/query.png", cv2.IMREAD_GRAYSCALE)
target_img: np.ndarray = cv2.imread("SIFT/target.jpg", cv2.IMREAD_GRAYSCALE)

# --------------------- Feature Detection ---------------------
sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(query_img, None)
kp2, des2 = sift.detectAndCompute(target_img, None)

# --------------------- Feature Matching ---------------------
FLANN_INDEX_KDTREE: int = 1
index_params: dict = {"algorithm": FLANN_INDEX_KDTREE, "trees": 5}
search_params: dict = {"checks": 50}
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches: List[List[cv2.DMatch]] = flann.knnMatch(des1, des2, k=2)

# --------------------- Accelerated Lowe's Ratio Test ---------------------
distances = np.array([[m[0].distance, m[1].distance] for m in matches], dtype=np.float32)
valid_indices: List[int] = filter_indices(distances)
good_matches: List[cv2.DMatch] = [matches[i][0] for i in valid_indices]

# --------------------- Homography Estimation ---------------------
if len(good_matches) >= 4:
    src_pts: np.ndarray = np.float32(
        [kp1[m.queryIdx].pt for m in good_matches]
    ).reshape(-1, 1, 2)
    dst_pts: np.ndarray = np.float32(
        [kp2[m.trainIdx].pt for m in good_matches]
    ).reshape(-1, 1, 2)

    H: np.ndarray = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)[0]

    if H is not None:
        # Query image corners
        h, w = query_img.shape
        corners: np.ndarray = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        projected_corners: np.ndarray = cv2.perspectiveTransform(corners, H)

        # Draw bounding box
        target_img_col: np.ndarray = cv2.cvtColor(target_img, cv2.COLOR_GRAY2BGR)
        cv2.polylines(
            target_img_col,
            [np.int32(projected_corners)],
            isClosed=True,
            color=(0, 255, 0),
            thickness=3,
        )

        # Draw matches
        result_img: np.ndarray = cv2.drawMatches(
            query_img,
            kp1,
            target_img_col,
            kp2,
            good_matches,
            None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
        )

        cv2.imshow("SIFT Object Detection (Accelerated)", result_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Homography could not be computed.")
else:
    print("Not enough good matches found - at least 4 required.")
