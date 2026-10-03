"""CLI entrypoint. Run from repo root: python -m backend.ingestion.run_ingestion"""
import argparse
import logging
from pathlib import Path

from . import config
from .fetcher import RateLimitedClient
from .myscheme import fetch_schemes_list, save_json


def main() -> None:
    p = argparse.ArgumentParser(description="myScheme ingestion (list stage)")
    p.add_argument("--limit", type=int, default=None, help="max items (testing)")
    p.add_argument("--page-size", type=int, default=config.PAGE_SIZE)
    p.add_argument("--out", default=str(config.LIST_FILE))
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    data = fetch_schemes_list(RateLimitedClient(), page_size=args.page_size,
                              limit=args.limit)
    save_json(data, Path(args.out))
    logging.info("saved %d items -> %s", len(data["items"]), args.out)


if __name__ == "__main__":
    main()
