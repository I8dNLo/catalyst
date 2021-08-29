from typing import Any, Dict

from torch.utils.data import Dataset


class ContrastiveDataset(Dataset):
    """The Contrastive Dataset.

    The class implemets contrastive logic (see Figure 2 from `A Simple Framework
    for Contrastive Learning of Visual Representations`_.)

    Example:

    .. code-block:: python

        import torchvision
        from torchvision.datasets import CIFAR10

        from catalyst.contrib.data.datawrappers import ContrastiveDataset

        transforms = torchvision.transforms.Compose(
            [
                torchvision.transforms.RandomResizedCrop(32),
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize(
                    [0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010]
                ),
                torchvision.transforms.ColorJitter(0.8, 0.8, 0.8, 0.2),
            ]
        )

        cifar_dataset = CIFAR10(root="./data", download=True, transform=None)
        cifar_contrastive = ContrastiveDataset(cifar_dataset, transforms=transforms)

    .. _`A Simple Framework for Contrastive Learning of Visual Representations`:
        https://arxiv.org/abs/2002.05709
    """

    def __init__(
        self, dataset: Dataset, transforms=None, transform_left=None, transform_right=None
    ) -> None:
        """
        Args:
            dataset: original dataset for agumention
            transforms: transform
            transform_left: transform
            transform_right: transform
        """
        super().__init__()

        if transform_right is not None and transform_left is not None:
            self.transform_right = transform_right
            self.transform_left = transform_left
        elif transforms is not None:
            self.transform_right = transforms
            self.transform_left = transforms
        else:
            raise ValueError(
                "Specify transforms or transform_left and transform_right simultaneously."
            )
        self.dataset = dataset

    def __len__(self) -> int:
        """Length"""
        return len(self.dataset)

    def __getitem__(self, idx) -> Dict[str, Any]:
        """
        Get item method for dataset
        Args:
            idx: index of the object
        Returns:
            Dict with left agumention (aug1), right agumention (aug2) and target
        """
        sample, target = self.dataset.__getitem__(idx)

        aug_1 = self.transform_left(sample)
        aug_2 = self.transform_right(sample)
        return {"aug1": aug_1, "aug2": aug_2, "target": target}
