from attr import define
from llmsheet.geometry import col_to_idx, idx_to_col
from llmsheet.xl_position import XLPosition


@define
class XLBoundingBox():
    tl: XLPosition
    tr: XLPosition
    bl: XLPosition
    br: XLPosition

    @classmethod
    def from_two_positions( cls, p1: XLPosition, p2: XLPosition ) -> "XLBoundingBox":
        vectors = [ ( col_to_idx( p1.col), p1.row ), ( col_to_idx( p2.col), p2.row ) ]

        min_col = idx_to_col( min( vectors[0][0], vectors[1][0]  ) )
        max_col = idx_to_col( max( vectors[0][0], vectors[1][0]  ) )
        min_row = min( vectors[0][1], vectors[1][1]  )
        max_row = max( vectors[0][1], vectors[1][1]  )

        bb = XLBoundingBox(
            tl=XLPosition( min_col, min_row ),
            tr=XLPosition( max_col, min_row ),
            bl=XLPosition( min_col, max_row ),
            br=XLPosition( max_col, max_row ),
        )

        return bb
