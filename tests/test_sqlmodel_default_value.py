from typing import Type
from sqlmodel import SQLModel

class MySQLModel(SQLModel):
    my_attribute: int = 42


def test_sqlmodel_default_value():
    my_type: Type[MySQLModel] = MySQLModel
    default_value = my_type.__fields__["my_attribute"].default
    print(default_value)  # Output: 42
    assert default_value == 42
    