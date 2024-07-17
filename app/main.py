# from fastapi import FastAPI, HTTPException
# import pysolr
# import requests
# from fastapi.responses import JSONResponse

# solr = pysolr.Solr('http://localhost:8983/solr/my_core2', always_commit=True)

# app = FastAPI()

# @app.get('/sss')
# def add_solr_data():
#     try:
#         data = {
#             'name': 'Venkey',
#             'age': 20
#         }
#         solr.add([data])
#         solr.commit()
#         return {"message": "Added Successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/ApacheData")
# def read_root():
   
#     solr_url = "http://localhost:8983/solr/my_core2/select?q=*:*&wt=json"
#     try:
#         response = requests.get(solr_url)
#         response.raise_for_status() 
#         data = response.json()  
#         return JSONResponse(content=data, status_code=201)
#     except requests.RequestException as e:
#         raise HTTPException(status_code=500, detail=str(e))



from fastapi import FastAPI, HTTPException,Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import pysolr
from models import SessionLocal,DeptTable
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the appropriate frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/ApacheData")
def read_root():
    solr_url = "http://localhost:8983/solr/my_core2/select?q=*:*&wt=json"
    try:
        response = requests.get(solr_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response
        return JSONResponse(content=data, status_code=200)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post('/SendDataSolr')
def ApacheData(data: dict = Body(...)):
    solr = pysolr.Solr('http://localhost:8983/solr/my_core2', always_commit=True)
    solr.add(data)
    solr.commit()    
    return JSONResponse({'Message': 'Success'}, status_code=200)

@app.post('/DataBaseDataSave')
def DataBaseData(data:dict =Body(...)):
    db=SessionLocal()
    NDO=DeptTable(deptno=data['deptno'],dept_name=data['dname'])
    db.add(NDO)
    db.commit()
    db.refresh(NDO)
    return JSONResponse({'Message': 'Success'}, status_code=200)

@app.get('/DataDataGet')
def DataBaseData():
    db=SessionLocal()
    try:
        DOBA = db.query(DeptTable).all()
        data = [{"deptno": d.deptno, "dept_name": d.dept_name} for d in DOBA]
        return JSONResponse(content=data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    



