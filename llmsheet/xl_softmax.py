from typing import List, Tuple, Union
from attr import define
from llmsheet.xl_position import XLPosition


@define
class XLSoftMax():
    inputs: List[XLPosition]

    def render(self, worksheet, f, outputs: List[Union[XLPosition,Tuple[int,int]]]) -> List[XLPosition]:
        assert( len(self.inputs) == len(outputs) )

        # Make the formula for the sum of the exponents
        sum_of_exponents = '+'.join([ f'EXP({str(i)})' for i in self.inputs])

        results = zip( self.inputs, outputs )
        for result in results:
            full_formula = f'=EXP({str(result[0])})/({sum_of_exponents})'
            output_position = result[1]

            # We might have gotten a relative offset to the input
            if not isinstance( output_position, XLPosition ):
                output_position = result[0].from_offset( *result[1] )

            worksheet.write( str(output_position), full_formula )