# Copyright (c) Alibaba, Inc. and its affiliates.
from modelscope.msdatasets.dataset_cls.custom_datasets import CUSTOM_DATASETS
from modelscope.msdatasets.dataset_cls.custom_datasets.easycv_base import \
    EasyCVBaseDataset
from modelscope.utils.constant import Tasks

from easycv.datasets.segmentation import SegDataset as _SegDataset
from easycv.toolkit.modelscope.metainfo import \
    EasyCVCustomDatasets as CustomDatasets


@CUSTOM_DATASETS.register_module(
    group_key=Tasks.image_segmentation, module_name=CustomDatasets.SegDataset)
class SegDataset(EasyCVBaseDataset, _SegDataset):
    """EasyCV dataset for Sementic segmentation.
    For more details, please refer to :
    https://github.com/alibaba/EasyCV/blob/master/easycv/datasets/segmentation/raw.py .

    Args:
        split_config (dict): Dataset root path from MSDataset, e.g.
            {"train":"local cache path"} or {"evaluation":"local cache path"}.
        preprocessor (Preprocessor): An optional preprocessor instance, please make sure the preprocessor fits for
            the model if supplied. Not support yet.
        mode: Training or Evaluation.
        data_source: Data source config to parse input data.
        pipeline: Sequence of transform object or config dict to be composed.
        ignore_index (int): Label index to be ignored.
        profiling: If set True, will print transform time.
    """

    def __init__(self,
                 split_config=None,
                 preprocessor=None,
                 mode=None,
                 *args,
                 **kwargs) -> None:
        EasyCVBaseDataset.__init__(
            self,
            split_config=split_config,
            preprocessor=preprocessor,
            mode=mode,
            args=args,
            kwargs=kwargs)
        _SegDataset.__init__(self, *args, **kwargs)
