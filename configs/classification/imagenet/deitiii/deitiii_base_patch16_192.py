# model settings
model = dict(
    type='Classification',
    train_preprocess=['mixUp'],
    pretrained=False,
    mixup_cfg=dict(
        mixup_alpha=0.8,
        cutmix_alpha=1.0,
        cutmix_minmax=None,
        prob=1.0,
        switch_prob=0.5,
        mode='batch',
        label_smoothing=0.0,
        num_classes=1000),
    backbone=dict(
        type='VisionTransformer',
        img_size=[192],
        num_classes=1000,
        patch_size=16,
        embed_dim=768,
        depth=12,
        num_heads=12,
        mlp_ratio=4,
        qkv_bias=True,
        drop_rate=0.,
        drop_path_rate=0.2,
        use_layer_scale=True,
        use_dpr_linspace=False),
    head=dict(
        type='ClsHead',
        loss_config=dict(
            type='CrossEntropyLoss',
            use_sigmoid=True,
            loss_weight=1.0,
            label_ceil=True),
        with_fc=False,
        use_num_classes=False))
