from routers.api_v1_router import app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        reload=True,
    )
