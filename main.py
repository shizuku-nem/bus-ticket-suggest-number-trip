from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from statsmodels.tsa.api import ExponentialSmoothing
from pydantic import BaseModel

class BusData(BaseModel):
    history_tickets: list = [10, 12, 25, 20, 45, 60, 67, 12, 30, 12, 20, 45, 60, 72, 12, 30, 12, 20, 45, 60, 70]

app = FastAPI()

origins = [
    "*"
    "http://localhost:3003/admin/dashboard",
    "https://localhost:3003/admin/dashboard",
    "http://localhost:3003/",
    "https://localhost:3003/",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def root(busData: BusData):
    # history_tickets = [10, 12, 25, 20, 45, 60, 70, 12, 30, 12, 20, 45, 60, 70, 30, 12, 20, 45, 60, 70, 20, 30, 12, 20, 45, 60, 70, 20]
    # input data, có thể dùng pandas series
    SevenNextDays = []
    for x in predict(busData.history_tickets, 7):
        SevenNextDays.append(int(x))

    print(SevenNextDays)
    # plot_predict(BusData, SevenNextDays)
    return {"seven_next_days": SevenNextDays}

def predict(input, DaysToPredict):
    """
        Function:
            Lấy mô hình thư viện
        tham số:
            input: dữ liệu đầu vào (list)
            DaysToPredict: số ngày cần dự đoán (int)
        return:
            dự đoán cho các ngày tiếp theo (numpy array -> list)
    """
    ES = ExponentialSmoothing(endog=input, trend='add', seasonal='add', seasonal_periods=7).fit()
    return ES.forecast(DaysToPredict).tolist()