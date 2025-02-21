# Copyright (c) Alibaba, Inc. and its affiliates.
import cv2
import os
import tempfile
import unittest
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.utils.cv.image_utils import panoptic_seg_masks_to_image
from modelscope.utils.test_utils import test_level

from tests.ut_config import BASE_LOCAL_PATH


class EasyCVPanopticSegmentationPipelineTest(unittest.TestCase):
    img_path = os.path.join(
        BASE_LOCAL_PATH, 'data/test_images/image_semantic_segmentation.jpg')

    def setUp(self) -> None:
        self.task = Tasks.image_segmentation
        self.model_id = 'damo/cv_r50_panoptic-segmentation_cocopan'

    @unittest.skipUnless(test_level() >= 0, 'skip test in current test level')
    def test_r50(self):
        segmentor = pipeline(task=self.task, model=self.model_id)
        outputs = segmentor(self.img_path)
        draw_img = panoptic_seg_masks_to_image(outputs[OutputKeys.MASKS])
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
            tmp_save_path = tmp_file.name
            cv2.imwrite(tmp_save_path, draw_img)
        print('print ' + self.model_id + ' success')


if __name__ == '__main__':
    unittest.main()
