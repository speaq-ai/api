from enum import Enum

# these are all the actions that the client knows how to take
class ActionNames(Enum):
    AddFilter = "AddFilter"
    LoadDataset = "LoadDataset"
    Clear = "Clear"

class WatsonEntities(Enum):
    Number = "sys-number"
    DatasetName = "dataset_name"
    FilterComparison = "filter_comparison"
    FilterField = "filter_field"
