

from llmsheet.xl_bounding_box import XLBoundingBox
from llmsheet.xl_position import XLPosition

def as_str( bb: XLBoundingBox ):
    return f"{str(bb.tl)}|{str(bb.tr)}|{str(bb.bl)}|{str(bb.br)}"

for test in [
    ['A1', 'A1','A1|A1|A1|A1' ],
    ['A1', 'B2','A1|B1|A2|B2' ],
    ['A1', 'AA100','A1|AA1|A100|AA100' ],
    ['B2', 'A1','A1|B1|A2|B2' ],
    ]:
    assert( as_str(XLBoundingBox.from_two_positions( XLPosition.from_str(test[0]), XLPosition.from_str(test[1]) )) == test[2] )



