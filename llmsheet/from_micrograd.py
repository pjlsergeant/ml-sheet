from typing import List
import micrograd.nn
from llmsheet.xl_layer import XLLayer
from llmsheet.xl_position import XLPosition

def xl_layer_from_micrograd_layer( layer_in: micrograd.nn.Layer, inputs: List[XLPosition]) -> XLLayer:
    return XLLayer(
        inputs,
        [([v.data for v in n.w ] , n.b.data, "ReLU" if n.nonlin else "Linear") for n in layer_in.neurons],
        None
    )

def render_micrograd_mlp( worksheet, f, mlp: micrograd.nn.MLP, inputs: List[XLPosition], at: XLPosition ) -> List[XLPosition]:
    for i in range(0, len(mlp.layers)):
        mg_layer = mlp.layers[i]
        name = f"hidden {i}" if i < (len(mlp.layers)-1) else "output"

        xl_layer = xl_layer_from_micrograd_layer( mg_layer, inputs )
        (outputs, bb) = xl_layer.render( worksheet, f, at, name )
        at = bb.tr.from_offset(2,0)
        inputs = outputs

    return inputs

# def xl_layers_from_micrograd_mlp( layer_in: micrograd.nn.MLP, inputs: List[XLPosition]):
#     layers = []

#     return XLLayer(
#         inputs,
#         [([v.data for v in n.w ] , n.b.data, "ReLU" if n.nonlin else "Linear") for n in layer_in.neurons],
#         None
#     )

    # layer1 = XLLayer(
#     [XLPosition.from_str('A1'), XLPosition.from_str('A2')],
#     [
#         ([0.5, 0.6], 0.2),
#         ([0.7, 0.6], 0.2),
#         ([0.8, 0.6], 0.2),
#         ([0.9, 0.6], 0.2),
#         ([0.4, 0.6], 0.2),
#     ],
#     "ReLU"
# )