# Copyright (c) Alibaba, Inc. and its affiliates.
import torch
import unittest

from easycv.models import build_model


class StdcTest(unittest.TestCase):

    def setUp(self):
        print(('Testing %s.%s' % (type(self).__name__, self._testMethodName)))

    def test_stdc(self):

        norm_cfg = dict(type='BN', requires_grad=True)
        model_cfg = dict(
            type='EncoderDecoder',
            backbone=dict(
                type='STDCContextPathNet',
                backbone_cfg=dict(
                    type='STDCNet',
                    stdc_type='STDCNet1',
                    in_channels=3,
                    channels=(32, 64, 256, 512, 1024),
                    bottleneck_type='cat',
                    num_convs=4,
                    norm_cfg=norm_cfg,
                    act_cfg=dict(type='ReLU'),
                    with_final_conv=False),
                last_in_channels=(1024, 512),
                out_channels=128,
                ffm_cfg=dict(
                    in_channels=384, out_channels=256, scale_factor=4)),
            decode_head=dict(
                type='FCNHead',
                in_channels=256,
                channels=256,
                num_convs=1,
                num_classes=19,
                in_index=3,
                concat_input=False,
                dropout_ratio=0.1,
                norm_cfg=norm_cfg,
                align_corners=True,
                sampler=dict(
                    type='OHEMPixelSampler', thresh=0.7, min_kept=10000),
                loss_decode=dict(
                    type='CrossEntropyLoss',
                    use_sigmoid=False,
                    loss_weight=1.0)),
            auxiliary_head=[
                dict(
                    type='FCNHead',
                    in_channels=128,
                    channels=64,
                    num_convs=1,
                    num_classes=19,
                    in_index=2,
                    norm_cfg=norm_cfg,
                    concat_input=False,
                    align_corners=False,
                    sampler=dict(
                        type='OHEMPixelSampler', thresh=0.7, min_kept=10000),
                    loss_decode=dict(
                        type='CrossEntropyLoss',
                        use_sigmoid=False,
                        loss_weight=1.0)),
                dict(
                    type='FCNHead',
                    in_channels=128,
                    channels=64,
                    num_convs=1,
                    num_classes=19,
                    in_index=1,
                    norm_cfg=norm_cfg,
                    concat_input=False,
                    align_corners=False,
                    sampler=dict(
                        type='OHEMPixelSampler', thresh=0.7, min_kept=10000),
                    loss_decode=dict(
                        type='CrossEntropyLoss',
                        use_sigmoid=False,
                        loss_weight=1.0)),
                dict(
                    type='STDCHead',
                    in_channels=256,
                    channels=64,
                    num_convs=1,
                    num_classes=2,
                    boundary_threshold=0.1,
                    in_index=0,
                    norm_cfg=norm_cfg,
                    concat_input=False,
                    align_corners=True,
                    loss_decode=[
                        dict(
                            type='CrossEntropyLoss',
                            loss_name='loss_ce',
                            use_sigmoid=True,
                            loss_weight=1.0),
                        dict(
                            type='DiceLoss',
                            loss_name='loss_dice',
                            loss_weight=1.0)
                    ]),
            ],
            train_cfg=dict(),
            test_cfg=dict(mode='whole'),
        )

        model = build_model(model_cfg).to('cuda')

        img = torch.rand(2, 3, 512, 1024).to('cuda')
        gt_semantic_seg = torch.randint(
            low=0, high=18, size=(2, 1, 512, 1024)).to('cuda')

        train_output = model.forward_train(img, [], gt_semantic_seg)
        self.assertIn('decode.loss_ce', train_output)
        self.assertIn('aux_0.loss_ce', train_output)
        self.assertIn('aux_1.loss_ce', train_output)
        self.assertIn('aux_2.loss_ce', train_output)


if __name__ == '__main__':
    unittest.main()
