#!/usr/bin/env python

# this config is used by unittest

# model settings
# models tiny
model = dict(
    stage='EDGE',
    type='YOLOX_EDGE',
    model_type='customized',
    test_conf=0.01,
    nms_thre=0.65,
    depth=1.0,
    width=1.0,
    max_model_params=-1,
    max_model_flops=-1,
    activation='relu',
    head=dict(
        type='YOLOXHead',
        model_type='customized',
        num_classes=1,
        reg_loss_type='iou',
        width=1.0))

# train setting
samples_per_gpu = 16  # batch size per gpu
test_samples_per_gpu = 16  # test batch size per gpu
gpu_num = 2  # gpu number for one worker
total_epochs = 11  # train epoch
interval = 5  # eval interval

# tiny nano without mixup
img_scale = (256, 256)
random_size = (8, 10)
scale_ratio = (0.8, 1.25)

# class list; default: coco class list
CLASSES = ['person']
# CLASSES = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
#        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
#        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
#        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
#        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
#        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
#        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
#        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
#        'hair drier', 'toothbrush']

# dataset settings
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)

train_pipeline = [
    dict(type='MMMosaic', img_scale=img_scale, pad_val=114.0),
    dict(
        type='MMRandomAffine',
        scaling_ratio_range=scale_ratio,
        border=(-img_scale[0] // 2, -img_scale[1] // 2)),
    dict(
        type='MMPhotoMetricDistortion',
        brightness_delta=32,
        contrast_range=(0.5, 1.5),
        saturation_range=(0.5, 1.5),
        hue_delta=18),
    dict(type='MMRandomFlip', flip_ratio=0.5),
    dict(type='MMResize', keep_ratio=True),
    dict(type='MMPad', pad_to_square=True, pad_val=(114.0, 114.0, 114.0)),
    dict(
        type='MMNormalize',
        mean=img_norm_cfg['mean'],
        std=img_norm_cfg['std'],
        to_rgb=img_norm_cfg['to_rgb']),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
]
test_pipeline = [
    dict(type='MMResize', img_scale=img_scale, keep_ratio=True),
    dict(type='MMPad', pad_to_square=True, pad_val=(114.0, 114.0, 114.0)),
    dict(
        type='MMNormalize',
        mean=img_norm_cfg['mean'],
        std=img_norm_cfg['std'],
        to_rgb=img_norm_cfg['to_rgb']),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img'])
]

data = dict(
    imgs_per_gpu=samples_per_gpu,
    workers_per_gpu=gpu_num,
    train=dict(
        type='DetImagesMixDataset',
        data_source=dict(
            type='DetSourceCoco',
            ann_file='data_root/annotations/instances_train2017.json',
            img_prefix='data_root/train2017/',
            pipeline=[
                dict(type='LoadImageFromFile', to_float32=True),
                dict(type='LoadAnnotations', with_bbox=True)
            ],
            classes=CLASSES,
            filter_empty_gt=False,
            iscrowd=False),
        pipeline=train_pipeline,
        dynamic_scale=img_scale),
    val=dict(
        type='DetImagesMixDataset',
        imgs_per_gpu=test_samples_per_gpu,
        data_source=dict(
            type='DetSourceCoco',
            ann_file='data_root/annotations/instances_val2017.json',
            img_prefix='data_root/val2017/',
            pipeline=[
                dict(type='LoadImageFromFile', to_float32=True),
                dict(type='LoadAnnotations', with_bbox=True)
            ],
            classes=CLASSES,
            filter_empty_gt=False,
            iscrowd=True),
        pipeline=test_pipeline,
        dynamic_scale=None,
        label_padding=False))

# additional hooks
custom_hooks = [
    dict(
        type='YOLOXModeSwitchHook',
        no_aug_epochs=15,
        skip_type_keys=('MMMosaic', 'MMRandomAffine'),
        priority=48),
    dict(
        type='SyncRandomSizeHook',
        ratio_range=random_size,
        img_scale=img_scale,
        interval=interval,
        priority=48),
    dict(
        type='SyncNormHook',
        num_last_epochs=15,
        interval=interval,
        priority=48)
]

# evaluation
eval_config = dict(interval=interval, gpu_collect=False)
eval_pipelines = [
    dict(
        mode='test',
        data=data['val'],
        evaluators=[dict(type='CocoDetectionEvaluator', classes=CLASSES)],
    )
]

checkpoint_config = dict(interval=interval)

# optimizer
# basic_lr_per_img = 0.01 / 64.0
optimizer = dict(
    type='SGD', lr=0.01, momentum=0.9, weight_decay=5e-4, nesterov=True)
optimizer_config = {}

# learning policy
lr_config = dict(
    policy='YOLOX',
    warmup='exp',
    by_epoch=False,
    warmup_by_epoch=True,
    warmup_ratio=1,
    warmup_iters=5,
    num_last_epochs=5,
    min_lr_ratio=0.05)

# exponetial model average
ema = dict(decay=0.9998)

# yapf:disable
log_config = dict(
    interval=100,
    hooks=[
        dict(type='TextLoggerHook'),
        dict(type='TensorboardLoggerHook')
    ])

# yapf:enable
# runtime settings
dist_params = dict(backend='nccl')
cudnn_benchmark = True
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]

export = dict(use_jit=False)

# oss io config
# oss_io_config = dict(ak_id='xxx',
#                      ak_secret='xxx',
#                      hosts='oss-cn-zhangjiakou.aliyuncs.com',
#                      buckets=['your_bucket_2'])
