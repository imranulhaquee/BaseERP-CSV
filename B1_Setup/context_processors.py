import pandas as pd
import numpy as np
import json

### Basic information of the company to use all the templates----------------- 
def basInfo(request):
    Data = pd.read_csv("Data/basInfo.csv").fillna(0)
    data = Data.to_dict()
    basInfo = json.dumps(data)
    return {'basInfo':basInfo}


