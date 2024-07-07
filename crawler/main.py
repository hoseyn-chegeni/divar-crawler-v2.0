from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

class CityIDRequest(BaseModel):
    city_ids: List[str]

@app.post("/fetch-data")
def fetch_data(request: CityIDRequest):
    url = "https://api.divar.ir/v8/postlist/w/search"
    headers = {"Content-Type": "application/json"}
    
    # Define the body with the predefined structure and add the city_id
    body = {
        "city_ids": request.city_ids,
        "search_data": {
            "form_data": {
                "data": {
                    "category": {
                        "str": {
                            "value": "ROOT"
                        }
                    }
                }
            }
        }
    }
    
    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")

    data = response.json()
    
    # Extract list_widgets
    post_data = data.get('list_widgets', [])
    
    # Count the number of instances of the specific type
    count = sum(1 for item in post_data if item.get('data', {}).get('@type') == 'type.googleapis.com/widgets.PostRowData')
    
    return {"count": count}
