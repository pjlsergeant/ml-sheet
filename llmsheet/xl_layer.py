
from typing import List, Optional, Tuple
from llmsheet.xl_bounding_box import XLBoundingBox
from llmsheet.xl_position import XLPosition
from llmsheet.xl_neuron import XLNeuron
from llmsheet.activations import activations
import xlsxwriter
from llmsheet.xl_ref import XLRef
from attrs import define

p = {
    "title": {
        "left": 2,
        "right": 2,
        "bold": True,
        'bg_color': "#000000",
        'font_color': "#ffffff",
    },
    "bottom": {
        "left": 2,
        "right": 2,
        'bg_color': "#000000",
    }
}

@define
class XLLayer():
    inputs: List[XLRef]
    neuron_specs: List[Tuple[List[float],float, Optional[str]]]
    activation: str

    def render(self, worksheet, f, initial_at: XLPosition, name: Optional[str]) -> Tuple[List[XLPosition], XLBoundingBox]:
        width = len(self.neuron_specs[0][0]) + 2

        # Title
        worksheet.merge_range(f'{str(initial_at)}:{str(initial_at.from_offset(width,0))}', name or "Layer", f(p["title"]) )

        at = initial_at.from_offset(0,1)
        outputs = []

        for neuron_i in range(0, len(self.neuron_specs) ):
            weights = self.neuron_specs[neuron_i][0]
            bias = self.neuron_specs[neuron_i][1]
            activation = self.neuron_specs[neuron_i][2] or self.activation

            neuron = XLNeuron(self.inputs, weights, bias, activation )
            (output, bb) = neuron.render( worksheet, f, at, f'{name} {neuron_i}' )
            at = bb.bl.from_offset(0,1)
            br = bb.br
            outputs.append(output)

        # Write a questionable bottom black section so the layer looks more
        # closed
        worksheet.merge_range(f'{str(bb.bl.from_offset(0,1))}:{str(bb.bl.from_offset(width,1))}', "", f(p["bottom"]) )
        bb = XLBoundingBox.from_two_positions( initial_at, bb.br.from_offset(0,1) )

        return (outputs, bb)