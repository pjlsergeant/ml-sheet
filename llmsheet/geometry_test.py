
from llmsheet.geometry import col_to_idx, idx_to_col, parse_position


assert( col_to_idx('A') == 1 )
assert( col_to_idx('AA') == 27 )
assert( idx_to_col(1) == 'A' )
assert( idx_to_col(27) == 'AA' )

for test in [('A1', 'A', 1, None),('Sheet2!A1', 'A', 1, 'Sheet2'),("'Sheet 2'!A1", 'A', 1, 'Sheet 2')]:
    (col, row, sheet) = parse_position(test[0])
    assert( col == test[1] )
    assert( row == test[2] )
    assert( sheet == test[3] )