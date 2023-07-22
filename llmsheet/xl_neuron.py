
from typing import List, Optional, Tuple
from llmsheet.geometry import col_to_idx, idx_to_col
from llmsheet.xl_bounding_box import XLBoundingBox
from llmsheet.xl_position import XLPosition
from llmsheet.activations import activations
import xlsxwriter
from llmsheet.xl_ref import XLRef
from attrs import define

bg_color = '#DDDDDD'

p = {
    "title": {
        "top": 1,
        "left": 2,
        "bold": True,
        'bg_color': bg_color,
    },
    "title_net": {
        "top": 1,
        'bg_color': bg_color,
        "align": "center",
    },
    "title_activation": {
        "top": 1,
        "right": 2,
        'bg_color': bg_color,
        "align": "center",
    },
    "col_label": {
        "left": 2,
        "italic": True,
        "align": "right",
    },
    "num_format": {
        "align": "center",
        'num_format': '0.00',
    },
    "bottom_right": {
        "right": 2
    }
}
p["num_net"] = {
    **p["num_format"],
    "top": 1,
    "bottom": 1,
    "left": 1,
}
p["num_activation"] = {
    **p["num_net"],
    "bold": True,
    "right": 2,
}

@define
class XLNeuron():
    inputs: List[XLRef]
    weights: List[float]
    bias: float
    activation: str = "Linear"

    def render(self, worksheet, f, at: XLPosition, name: Optional[str]) -> Tuple[List[XLPosition], XLBoundingBox]:
        # We're going to go long on these, so each one is three deep, and length
        # of weights + 3

        # Title
        worksheet.merge_range(f'{str(at)}:{str(at.from_offset(len(self.weights),0))}', name or "Neuron", f(p["title"]) )

        # Bias
        worksheet.write( str(at.from_offset(0,2)), "Bias", f(p["col_label"]) )
        worksheet.write( str(at.from_offset(1,2)), self.bias )

        # Weights
        worksheet.write( str(at.from_offset(0,1)), "Weights", f(p["col_label"]) )
        col_offset = 0
        weight_positions = []
        for weight in self.weights:
            col_offset += 1
            weight_position = at.from_offset(col_offset,1)
            weight_positions.append(weight_position)
            worksheet.write( str(weight_position), weight, f(p["num_format"]) )

        # Net
        col_offset += 1
        worksheet.write( str(at.from_offset(col_offset, 0)), "Net", f(p["title_net"]) )
        net_formula = '=' + str(at.from_offset(1,2))
        for pair in zip( self.inputs, weight_positions ):
            net_formula += f'+({str(pair[0])}*{str(pair[1])})'
        net_position = at.from_offset(col_offset, 1)
        worksheet.write( str(net_position), net_formula, f(p["num_net"]))

        output_cell = net_position

        # Activation
        col_offset += 1
        worksheet.write( str(at.from_offset(col_offset, 0)), self.activation, f(p["title_activation"]))
        activation_fn = activations[self.activation]
        worksheet.write( str(at.from_offset(col_offset, 1)), activation_fn(str(output_cell)), f(p["num_activation"]) )
        output_cell = output_cell.from_offset(1,0)
        worksheet.write( str(at.from_offset(col_offset, 2)), '', f(p["bottom_right"]) )

        bb = XLBoundingBox.from_two_positions( at, XLPosition( idx_to_col(col_to_idx(at.col) + col_offset), at.row + 2 ) )

        return (output_cell, bb)
