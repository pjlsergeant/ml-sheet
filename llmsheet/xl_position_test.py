
from llmsheet.xl_position import XLPosition, _col_offset

# Columns
assert( _col_offset('A', 1) == 'B' )
assert( _col_offset('Z', 1) == 'AA' )
assert( _col_offset('Z', -1) == 'Y' )
assert( _col_offset('AA', -1) == 'Z' )
assert( _col_offset('A', 27) == 'AB' )

# Combined
start = XLPosition.from_str( 'C3' )
assert( str(start) == 'C3')
assert( str(start.from_offset(0,0)) == 'C3')
assert( str(start.from_offset(1,0)) == 'D3')
assert( str(start.from_offset(0,1)) == 'C4')
assert( str(start.from_offset(1,1)) == 'D4')
assert( str(start.from_offset(-1,-1)) == 'B2')
