"""CLI entrypoint. Run from repo root:
  python -m backend.ingestion.run_ingestion                  # list stage
  python -m backend.ingestion.run_ingestion --stage detail   # then documents, faqs
"""
import argparse
import logging
from pathlib import Path

from . import config
from .fetcher import RateLimitedClient
from .myscheme import fetch_schemes_list, save_json
from .myscheme_detail import (STAGES, build_stage_file, fetch_stage,
                              unique_slugs)


def main() -> None:
    p = argparse.ArgumentParser(description="myScheme ingestion")
    p.add_argument("--stage", choices=("list",) + STAGES, default="list",
                   help="list (default), detail, documents, faqs")
    p.add_argument("--limit", type=int, default=None, help="max items (testing)")
    p.add_argument("--page-size", type=int, default=config.PAGE_SIZE,
                   help="list stage only")
    p.add_argument("--out", default=str(config.LIST_FILE),
                   help="list stage only")
    p.add_argument("--pretty", action="store_true",
                   help="indent detail/documents/faqs output (bigger file)")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    client = RateLimitedClient()

    if args.stage == "list":
        data = fetch_schemes_list(client, page_size=args.page_size,
                                  limit=args.limit)
        save_json(data, Path(args.out))
        logging.info("saved %d items -> %s", len(data["items"]), args.out)
        return

    slugs = unique_slugs()
    fetched, failed = fetch_stage(client, args.stage, slugs, limit=args.limit)
    count = build_stage_file(args.stage, slugs, pretty=args.pretty)
    logging.info("%s: fetched %d this run, %d failed, %d / %d in output file",
                 args.stage, fetched, len(failed), count, len(slugs))


if __name__ == "__main__":
    main()
