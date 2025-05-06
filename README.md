# KL GUI

A graphical user interface to show how the KL divergence between two gaussians
varies with standard deviation and mean. The goal is to help people gain an
intuition for what the KL divergence means in the context of
this [paper](https://arxiv.org/abs/2503.13263) on the posterior bias introduced by using emulators in 
inference pipelines.


To run the gui you will need to install PyQt6, numpy and matplotlib and then run

```bash
python3 gui.py
```

in the terminal. I have only tested this on Mac but my understanding is that
PyQt is pretty versatile. 

## Example

![Example Use](https://github.com/htjb/kl-gui/blob/main/recording.gif)

## Contributing

If you have suggestions for how this code base could be extended please open an issue to discuss.