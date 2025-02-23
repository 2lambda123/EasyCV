# Copyright (c) Alibaba, Inc. and its affiliates.
import random
import unittest

from easycv.datasets.selfsup.data_sources.imagenet_feature import \
    SSLSourceImageNetFeature
from tests.ut_config import SSL_SMALL_IMAGENET_FEATURE


class SSLSourceImageNetFeatureTest(unittest.TestCase):

    def setUp(self):
        print(('Testing %s.%s' % (type(self).__name__, self._testMethodName)))

    def test_imagenet_feature_dynamic_load(self):

        data_source = SSLSourceImageNetFeature(
            root_path=SSL_SMALL_IMAGENET_FEATURE)

        index_list = random.choices(list(range(100)), k=3)
        for idx in index_list:
            results = data_source[idx]
            feat = results['img']
            label = results['gt_labels']
            self.assertEqual(feat.shape, (2048, ))
            self.assertIn(label, list(range(1000)))

        self.assertEqual(len(data_source), 3215)

    def test_imagenet_feature(self):

        data_source = SSLSourceImageNetFeature(
            root_path=SSL_SMALL_IMAGENET_FEATURE, dynamic_load=False)

        index_list = random.choices(list(range(100)), k=3)
        for idx in index_list:
            results = data_source[idx]
            feat = results['img']
            label = results['gt_labels']
            self.assertEqual(feat.shape, (2048, ))
            self.assertIn(label, list(range(1000)))

        self.assertEqual(len(data_source), 3215)


if __name__ == '__main__':
    unittest.main()
