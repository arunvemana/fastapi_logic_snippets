from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette_wtf import StarletteForm
from wtforms import StringField,
from wtforms.validators import DataRequired
from fastapi.templating import Jinja2Templates
import uvicorn


class MyForm(StarletteForm):
    name = StringField('name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = StringField('email', default='test@gmail.com', render_kw={"placeholder": "email id"})
    check = StringField("Noeditable", default='True', render_kw={'readonly': True})


app = FastAPI()
# app.mount("/static")

templates = Jinja2Templates(directory='templates')


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    form = await MyForm.from_formdata(request)
    return templates.TemplateResponse('home.html', {"request": request, 'form': form})


@app.post("/")
async def home(request: Request):
    form = await MyForm.from_formdata(request)
    if await form.validate_on_submit():
        return JSONResponse({"DATA": ','.join([i.data for i in form])})
    return templates.TemplateResponse('home.html', {"request": request, 'form': form})


if __name__ == '__main__':
    uvicorn.run(app)
