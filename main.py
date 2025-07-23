from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
from checker import check_declaration
app = FastAPI(docs_url=None, redoc_url=None)  # отключаем Swagger
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def handle_upload(request: Request, file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    results = check_declaration(df)
    result_lines = []
    if not results:
        result_lines.append("Ошибок нет!")
    else:
        for item in results:
            num = item["Номер товара"]
            name = item["Товар"]
            errors = "; ".join(item["Ошибка"])
            result_lines.append(f'Товар №{num} "{name}": {errors}')
    result_text = "\n".join(result_lines)
    return templates.TemplateResponse("index.html", {"request": request, "result": result_text})

@app.post("/manual-check", response_class=HTMLResponse)
async def manual_check(
    request: Request,
    name: str = Form(...),
    tnved: str = Form(...),
    country: str = Form(...),
    currency: str = Form(...),
    price: float = Form(...)
):
    row = {
        "name": name,
        "tnved": tnved,
        "country": country,
        "currency": currency,
        "usd": price
    }
    df = pd.DataFrame([row])
    result = check_declaration(df)

    result_lines = []
    if not result:
        result_lines.append("Ошибок нет!")
    else:
        for item in result:
            name = item["Товар"]
            errors = "; ".join(item["Ошибка"])
            result_lines.append(f'Для товара "{name}": {errors}')
    result_text = "\n".join(result_lines)

    return templates.TemplateResponse("index.html", {"request": request, "result": result_text})
