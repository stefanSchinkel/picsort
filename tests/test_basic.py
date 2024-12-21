"""
This has no other purpose than to assert that the toolchain is working
"""


def test_chain():
    # Arrange
    a = 1
    b = 2

    # Act
    c = a + b

    # Assert
    assert c == 3
