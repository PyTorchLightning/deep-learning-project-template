"""
This file runs the main training/val loop, etc... using Lightning Trainer    
"""
from pytorch_lightning import Trainer, seed_everything
from argparse import ArgumentParser
from src.research_mnist.mnist import CoolSystem
from src.research_mnist.mnist_data_module import MNISTDataModule

# sets seeds for numpy, torch, etc...
# must do for DDP to work well
seed_everything(123)

def main(args):
    # init modules
    dm = MNISTDataModule(hparams=args)
    model = CoolSystem(hparams=args)

    # most basic trainer, uses good defaults
    trainer = Trainer.from_argparse_args(args)
    trainer.fit(model, dm)

    trainer.test()


if __name__ == '__main__':
    parser = ArgumentParser(add_help=False)

    # add args from trainer
    parser = Trainer.add_argparse_args(parser)

    # give the module a chance to add own params
    # good practice to define LightningModule speficic params in the module
    parser = CoolSystem.add_model_specific_args(parser)
    # same goes for data modules
    parser = MNISTDataModule.add_data_specific_args(parser)

    # parse params
    args = parser.parse_args()

    main(args)
