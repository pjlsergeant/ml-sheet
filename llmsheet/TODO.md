TODO:

- Bounding box
- Automatic lay-out of existing Excel
- Automatic conversion of a Micrograd Layer
- Automatic conversion of a Micrograd MLP
- Build softmax
- Demo: train Iris with Micrograd, and create the output
- Neuron formatting
- Layer formatting

* Complain if we have mismatched weights and inputs
* Deal with cross-sheet references
* Translate makemore part 1

At some point, I might need to think about deferring values or making them
relative to each other, because at the point when I create a layer right now,
the inputs needs to be "real". This means I can't create a network without also
rendering the layers as I go. Not the end of the world, but feels inelegant.
