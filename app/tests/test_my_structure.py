import pytest   
from my_project import my_structure    
    
@pytest.mark.parametrize("arr, size_of_window, expected_result",[
(
    [1,2,3,4,5,6],
    3,
    15
),
(
    [1,2,3,4,5,6],
    2,
    11
),
(
    [1,2,3,4,5,6],
    8,
    -1
),
])

def test_slinding_windows(arr, size_of_window, expected_result):
       
    result = my_structure.slinding_window(arr, size_of_window)
    assert result == expected_result