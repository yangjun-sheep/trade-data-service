from datetime import date, timedelta

from app.crawler.sse import run as sse_crawler


def main() -> None:
    for i in range(7):
        day = date.today() - timedelta(days=i)
        sse_crawler(day)


if __name__ == "__main__":
    main()
