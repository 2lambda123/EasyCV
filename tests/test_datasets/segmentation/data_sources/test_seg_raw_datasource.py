# Copyright (c) Alibaba, Inc. and its affiliates.
import numpy as np
import os
import random
import unittest

from easycv.datasets.segmentation.data_sources.raw import SegSourceRaw
from easycv.file import io
from tests.ut_config import SEG_DATA_SMALL_RAW_LOCAL, VOC_CLASSES


class SegSourceRawTest(unittest.TestCase):

    def setUp(self):
        print(('Testing %s.%s' % (type(self).__name__, self._testMethodName)))

    def _base_test(self, data_source, cache_at_init, cache_on_the_fly):
        index_list = random.choices(list(range(20)), k=3)
        for idx in index_list:
            data = data_source[idx]
            self.assertIn('filename', data)
            self.assertIn('seg_filename', data)
            self.assertEqual(data['img_fields'], ['img'])
            self.assertEqual(data['seg_fields'], ['gt_semantic_seg'])
            self.assertIn('img_shape', data)
            self.assertEqual(len(data['img_shape']), 3)
            self.assertEqual(data['gt_semantic_seg'].shape,
                             data['img_shape'][:2])
            self.assertEqual(data['img'].shape[-1], 3)
            self.assertTrue(
                set([0, 255]).issubset(np.unique(data['gt_semantic_seg'])))
            self.assertTrue(
                len(np.unique(data['gt_semantic_seg'])) < len(VOC_CLASSES))

        exclude_idx = [i for i in list(range(20)) if i not in index_list]
        if cache_at_init:
            for i in range(20):
                self.assertIn('img', data_source.samples_list[i])

        if not cache_at_init and cache_on_the_fly:
            for i in index_list:
                self.assertIn('img', data_source.samples_list[i])
            for j in exclude_idx:
                self.assertNotIn('img', data_source.samples_list[j])

        if not cache_at_init and not cache_on_the_fly:
            for i in range(20):
                self.assertNotIn('img', data_source.samples_list[i])

        length = len(data_source)
        self.assertEqual(length, 200)
        self.assertEqual(data_source.PALETTE.shape, (len(VOC_CLASSES), 3))

        exists = False
        for idx in range(length):
            result = data_source[idx]
            file_name = result.get('filename', '')
            if file_name.endswith('001185.jpg'):
                exists = True
                self.assertEqual(result['img_shape'], (375, 500, 3))
                self.assertEqual(
                    np.unique(result['gt_semantic_seg']).tolist(),
                    [0, 5, 8, 11, 15, 255])
        self.assertTrue(exists)

    def test_default(self):
        data_root = SEG_DATA_SMALL_RAW_LOCAL
        cache_at_init = False
        cache_on_the_fly = False
        data_source = SegSourceRaw(
            img_root=os.path.join(data_root, 'images'),
            label_root=os.path.join(data_root, 'labels'),
            classes=VOC_CLASSES,
        )
        self._base_test(data_source, cache_at_init, cache_on_the_fly)

    def test_cache_at_init(self):
        data_root = SEG_DATA_SMALL_RAW_LOCAL
        cache_at_init = True
        cache_on_the_fly = False
        data_source = SegSourceRaw(
            img_root=os.path.join(data_root, 'images'),
            label_root=os.path.join(data_root, 'labels'),
            classes=VOC_CLASSES,
            cache_at_init=cache_at_init,
            cache_on_the_fly=cache_on_the_fly)
        self._base_test(data_source, cache_at_init, cache_on_the_fly)

    def test_cache_on_the_fly(self):
        data_root = SEG_DATA_SMALL_RAW_LOCAL
        cache_at_init = False
        cache_on_the_fly = True
        data_source = SegSourceRaw(
            img_root=os.path.join(data_root, 'images'),
            label_root=os.path.join(data_root, 'labels'),
            classes=VOC_CLASSES,
            cache_on_the_fly=True)
        self._base_test(data_source, cache_at_init, cache_on_the_fly)

    def test_split(self):
        data_root = SEG_DATA_SMALL_RAW_LOCAL
        cache_at_init = False
        cache_on_the_fly = False
        data_source = SegSourceRaw(
            img_root=os.path.join(data_root, 'images'),
            label_root=os.path.join(data_root, 'labels'),
            classes=VOC_CLASSES,
            split=os.path.join(data_root, 'train.txt'),
            cache_at_init=cache_at_init,
            cache_on_the_fly=cache_on_the_fly)
        self._base_test(data_source, cache_at_init, cache_on_the_fly)


if __name__ == '__main__':
    unittest.main()
