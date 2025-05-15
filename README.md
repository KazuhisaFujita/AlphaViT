# AlphaViT

AlphaViT, AlphaViD, and AlphaVDA are novel game-playing AI agents designed to overcome the limitations of AlphaZero by leveraging Vision Transformers (ViT). These agents integrate deep neural networks with Monte Carlo Tree Search (MCTS) for decision-making. AlphaViT employs a transformer encoder to process board states and predict value and move probabilities, while AlphaViD and AlphaVDA extend this architecture by incorporating transformer decoders to enable dynamic policy vector sizes. These enhancements allow the agents to handle varying board sizes and game types, demonstrating flexibility and adaptability in both single-task and multitask learning scenarios.

## Repository Structure

The repository is structured as follows:

```
├── AlphaVDA/  : Source code for AlphaVDA
├── AlphaViD/  : Source code for AlphaViD
├── AlphaViT/  : Source code for AlphaViT
├── AlphaZero/ : Source code for the AlphaZero baseline
├── models/    : Pretrained model weights for various configurations
├── RawData/   : Raw data for my manuscript (https://arxiv.org/abs/2408.13871)
├── LICENSE    : License information
├── README.md  : Project documentation
```

### Alpha\*/

Contains the implementation of Alpha\*. Key files include:

- `Alpha*_mcts.py` - MCTS implementation for Alpha\*.
- `nn_*` - Neural network implementation.
- `parameters_alpha*.py` - Hyperparameter configurations for Alpha\*.
- `train_mp.py` - Training process script.

### models/

The models for AlphaViT, AlphaViD, AlphaVDA, and AlphaZero are available on Hugging Face. You can access them here:
https://huggingface.co/kazufujita/AlphaViT

## Related Paper

For a comprehensive overview of the methodology and results, refer to our paper:
["Flexible Game-Playing AI with AlphaViT: Adapting to Multiple Games and Board Sizes"](https://arxiv.org/abs/2408.13871)
