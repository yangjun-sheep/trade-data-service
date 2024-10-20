# Trade data service

## 项目介绍

提供公告数据查询服务，可对接多个数据源

## 技术栈

- Python 3.12
- FastAPI
- AMIS

## 运行

```bash
pip install -r requirements.txt
uvicorn app.main:app --host=0.0.0.0 --port=9001 --reload
```

## 访问

前端页面：http://127.0.0.1:9001
接口文档：http://127.0.0.1:9001/docs

## 初始化一周内历史数据

```bash
python init_history.py
```
