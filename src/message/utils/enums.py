from enum import Enum

# these are all the actions that the client knows how to take
class ActionNames(Enum):
    AddFilter = "AddFilter"
    LoadDataset = "LoadData"
    Clear = "Clear"
    ChangeViewMode = "ChangeViewMode"
    ViewAction = "ViewAction"
    GotoAction = "GotoAction"
    LocationFilter = "LocationFilter"

# these are the names of entities as they appear as context variables in requests
class WatsonEntities(Enum):
    Number = "sys_number"
    DatasetName = "dataset_name"
    FilterComparison = "filter_comparison"
    FilterField = "filter_field"
    ViewMode = "view_mode"
    ViewActions = "view_action"
    Location = "location"
