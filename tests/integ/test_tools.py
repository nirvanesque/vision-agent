import numpy as np
import skimage as ski
from PIL import Image

from vision_agent.tools import (
    blip_image_caption,
    clip,
    closest_mask_distance,
    countgd_counting,
    countgd_example_based_counting,
    depth_anything_v2,
    detr_segmentation,
    dpt_hybrid_midas,
    florence2_image_caption,
    florence2_ocr,
    florence2_phrase_grounding,
    florence2_phrase_grounding_video,
    florence2_roberta_vqa,
    florence2_sam2_image,
    florence2_sam2_video_tracking,
    generate_pose_image,
    generate_soft_edge_image,
    git_vqa_v2,
    grounding_dino,
    grounding_sam,
    ixc25_image_vqa,
    ixc25_temporal_localization,
    ixc25_video_vqa,
    loca_visual_prompt_counting,
    loca_zero_shot_counting,
    ocr,
    owl_v2_image,
    owl_v2_video,
    template_match,
    vit_image_classification,
    vit_nsfw_classification,
)

FINE_TUNE_ID = "65ebba4a-88b7-419f-9046-0750e30250da"


def test_grounding_dino():
    img = ski.data.coins()
    result = grounding_dino(
        prompt="coin",
        image=img,
    )
    assert len(result) == 24
    assert [res["label"] for res in result] == ["coin"] * 24


def test_grounding_dino_tiny():
    img = ski.data.coins()
    result = grounding_dino(
        prompt="coin",
        image=img,
        model_size="tiny",
    )
    assert len(result) == 24
    assert [res["label"] for res in result] == ["coin"] * 24


def test_owl_v2_image():
    img = ski.data.coins()
    result = owl_v2_image(
        prompt="coin",
        image=img,
    )
    assert 24 <= len(result) <= 26
    assert [res["label"] for res in result] == ["coin"] * len(result)
    assert all([all([0 <= x <= 1 for x in obj["bbox"]]) for obj in result])


def test_owl_v2_fine_tune_id():
    img = ski.data.coins()
    result = owl_v2_image(
        prompt="coin",
        image=img,
        fine_tune_id=FINE_TUNE_ID,
    )
    # this calls a fine-tuned florence2 model which is going to be worse at this task
    assert 14 <= len(result) <= 26
    assert [res["label"] for res in result] == ["coin"] * len(result)
    assert all([all([0 <= x <= 1 for x in obj["bbox"]]) for obj in result])


def test_owl_v2_video():
    frames = [
        np.array(Image.fromarray(ski.data.coins()).convert("RGB")) for _ in range(10)
    ]
    result = owl_v2_video(
        prompt="coin",
        frames=frames,
    )

    assert len(result) == 10
    assert 24 <= len([res["label"] for res in result[0]]) <= 26
    assert all([all([0 <= x <= 1 for x in obj["bbox"]]) for obj in result[0]])


def test_florence2_phrase_grounding():
    img = ski.data.coins()
    result = florence2_phrase_grounding(
        image=img,
        prompt="coin",
    )

    assert len(result) == 25
    assert [res["label"] for res in result] == ["coin"] * 25
    assert all([all([0 <= x <= 1 for x in obj["bbox"]]) for obj in result])


def test_florence2_phrase_grounding_fine_tune_id():
    img = ski.data.coins()
    result = florence2_phrase_grounding(
        prompt="coin",
        image=img,
        fine_tune_id=FINE_TUNE_ID,
    )
    # this calls a fine-tuned florence2 model which is going to be worse at this task
    assert 14 <= len(result) <= 26
    assert [res["label"] for res in result] == ["coin"] * len(result)
    assert all([all([0 <= x <= 1 for x in obj["bbox"]]) for obj in result])


def test_florence2_phrase_grounding_video():
    frames = [
        np.array(Image.fromarray(ski.data.coins()).convert("RGB")) for _ in range(10)
    ]
    result = florence2_phrase_grounding_video(
        prompt="coin",
        frames=frames,
    )
    assert len(result) == 10
    assert 2 <= len([res["label"] for res in result[0]]) <= 26
    assert all([all([0 <= x <= 1 for x in obj["bbox"]]) for obj in result[0]])


def test_florence2_phrase_grounding_video_fine_tune_id():
    frames = [
        np.array(Image.fromarray(ski.data.coins()).convert("RGB")) for _ in range(10)
    ]
    # this calls a fine-tuned florence2 model which is going to be worse at this task
    result = florence2_phrase_grounding_video(
        prompt="coin",
        frames=frames,
        fine_tune_id=FINE_TUNE_ID,
    )
    assert len(result) == 10
    assert 16 <= len([res["label"] for res in result[0]]) <= 26
    assert all([all([0 <= x <= 1 for x in obj["bbox"]]) for obj in result[0]])


def test_template_match():
    img = ski.data.coins()
    result = template_match(
        image=img,
        template_image=img[32:76, 20:68],
    )
    assert len(result) == 2


def test_grounding_sam():
    img = ski.data.coins()
    result = grounding_sam(
        prompt="coin",
        image=img,
    )
    assert len(result) == 24
    assert [res["label"] for res in result] == ["coin"] * 24
    assert len([res["mask"] for res in result]) == 24


def test_florence2_sam2_image():
    img = ski.data.coins()
    result = florence2_sam2_image(
        prompt="coin",
        image=img,
    )
    assert len(result) == 25
    assert [res["label"] for res in result] == ["coin"] * 25
    assert len([res["mask"] for res in result]) == 25


def test_florence2_sam2_image_fine_tune_id():
    img = ski.data.coins()
    result = florence2_sam2_image(
        prompt="coin",
        image=img,
        fine_tune_id=FINE_TUNE_ID,
    )
    # this calls a fine-tuned florence2 model which is going to be worse at this task
    assert 14 <= len(result) <= 26
    assert [res["label"] for res in result] == ["coin"] * len(result)
    assert len([res["mask"] for res in result]) == len(result)


def test_florence2_sam2_video():
    frames = [
        np.array(Image.fromarray(ski.data.coins()).convert("RGB")) for _ in range(10)
    ]
    result = florence2_sam2_video_tracking(
        prompt="coin",
        frames=frames,
    )
    assert len(result) == 10
    assert len([res["label"] for res in result[0]]) == 25
    assert len([res["mask"] for res in result[0]]) == 25


def test_segmentation():
    img = ski.data.coins()
    result = detr_segmentation(
        image=img,
    )
    assert len(result) == 1
    assert [res["label"] for res in result] == ["pizza"]
    assert len([res["mask"] for res in result]) == 1


def test_clip():
    img = ski.data.coins()
    result = clip(
        classes=["coins", "notes"],
        image=img,
    )
    assert result["scores"] == [0.9999, 0.0001]


def test_vit_classification():
    img = ski.data.coins()
    result = vit_image_classification(
        image=img,
    )
    assert "typewriter keyboard" in result["labels"]


def test_nsfw_classification():
    img = ski.data.coins()
    result = vit_nsfw_classification(
        image=img,
    )
    assert result["label"] == "normal"


def test_image_caption() -> None:
    img = ski.data.rocket()
    result = blip_image_caption(
        image=img,
    )
    assert result.strip() == "a rocket on a stand"


def test_florence_image_caption() -> None:
    img = ski.data.rocket()
    result = florence2_image_caption(
        image=img,
    )
    assert "The image shows a rocket on a launch pad at night" in result.strip()


def test_loca_zero_shot_counting() -> None:
    img = ski.data.coins()

    result = loca_zero_shot_counting(
        image=img,
    )
    assert result["count"] == 21


def test_loca_visual_prompt_counting() -> None:
    img = ski.data.coins()
    result = loca_visual_prompt_counting(
        visual_prompt={"bbox": [85, 106, 122, 145]},
        image=img,
    )
    assert result["count"] == 25


def test_git_vqa_v2() -> None:
    img = ski.data.rocket()
    result = git_vqa_v2(
        prompt="Is the scene captured during day or night ?",
        image=img,
    )
    assert result.strip() == "night"


def test_image_qa_with_context() -> None:
    img = ski.data.rocket()
    result = florence2_roberta_vqa(
        prompt="Is the scene captured during day or night ?",
        image=img,
    )
    assert "night" in result.strip()


def test_ixc25_image_vqa() -> None:
    img = ski.data.cat()
    result = ixc25_image_vqa(
        prompt="What animal is in this image?",
        image=img,
    )
    assert "cat" in result.strip()


def test_ixc25_video_vqa() -> None:
    frames = [
        np.array(Image.fromarray(ski.data.cat()).convert("RGB")) for _ in range(10)
    ]
    result = ixc25_video_vqa(
        prompt="What animal is in this video?",
        frames=frames,
    )
    assert "cat" in result.strip()


def test_ixc25_temporal_localization() -> None:
    frames = [
        np.array(Image.fromarray(ski.data.cat()).convert("RGB")) for _ in range(10)
    ]
    result = ixc25_temporal_localization(
        prompt="What animal is in this video?",
        frames=frames,
    )
    assert result == [True] * 10


def test_ocr() -> None:
    img = ski.data.page()
    result = ocr(
        image=img,
    )
    assert any("Region-based segmentation" in res["label"] for res in result)


def test_florence2_ocr() -> None:
    img = ski.data.page()
    result = florence2_ocr(
        image=img,
    )
    assert any("Region-based segmentation" in res["label"] for res in result)


def test_mask_distance():
    # Create two binary masks
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask1[:10, :10] = 1  # Top left
    mask2 = np.zeros((100, 100), dtype=np.uint8)
    mask2[-10:, -10:] = 1  # Bottom right

    # Calculate the distance between the masks
    distance = closest_mask_distance(mask1, mask2)
    print(f"Distance between the masks: {distance}")

    # Check the result
    assert np.isclose(
        distance,
        np.sqrt(2) * 81,
        atol=1e-2,
    ), f"Expected {np.sqrt(2) * 81}, got {distance}"


def test_generate_depth():
    img = ski.data.coins()
    result = depth_anything_v2(
        image=img,
    )

    assert result.shape == img.shape


def test_generate_pose():
    img = ski.data.coins()
    result = generate_pose_image(
        image=img,
    )
    import cv2

    cv2.imwrite("imag.png", result)
    assert result.shape == img.shape + (3,)


def test_generate_normal():
    img = ski.data.coins()
    result = dpt_hybrid_midas(
        image=img,
    )

    assert result.shape == img.shape + (3,)


def test_generate_hed():
    img = ski.data.coins()
    result = generate_soft_edge_image(
        image=img,
    )

    assert result.shape == img.shape


def test_countgd_counting() -> None:
    img = ski.data.coins()
    result = countgd_counting(image=img, prompt="coin")
    assert len(result) == 24
    assert [res["label"] for res in result] == ["coin"] * 24


def test_countgd_example_based_counting() -> None:
    img = ski.data.coins()
    result = countgd_example_based_counting(
        visual_prompts=[[85, 106, 122, 145]],
        image=img,
    )
    assert len(result) == 24
    assert [res["label"] for res in result] == ["object"] * 24
