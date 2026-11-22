import sys
import time
import requests


def normalize_url(raw_url: str) -> str:
    cleaned = raw_url.strip()
    if not cleaned:
        raise ValueError("Walang URL na nailagay.")
    if not cleaned.startswith(("http://", "https://")):
        cleaned = "https://" + cleaned
    return cleaned


def run_requests(url: str, count: int = 50, delay: float = 0.5, loop_forever: bool = False) -> None:
    url = normalize_url(url)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) AppleWebKit/537.36"
    })

    batch_number = 1
    try:
        while True:
            print(f"\n--- Batch #{batch_number} | Target: {url} | Count: {count} ---")
            for idx in range(1, count + 1):
                start_time = time.perf_counter()
                try:
                    resp = session.get(url, timeout=10)
                    elapsed_ms = (time.perf_counter() - start_time) * 1000
                    print(
                        f"[{idx}/{count}] HTTP {resp.status_code} | "
                        f"{elapsed_ms:.0f} ms | {len(resp.content)} bytes"
                    )
                except requests.exceptions.RequestException as exc:
                    elapsed_ms = (time.perf_counter() - start_time) * 1000
                    print(f"[{idx}/{count}] ERROR ({elapsed_ms:.0f} ms): {exc}")

                if delay > 0:
                    time.sleep(delay)

            if not loop_forever:
                print(
                    f"\nTapos na ang {count} requests. Naka-stay lang ang script "
                    "(pindutin ang CTRL + C para i-stop)..."
                )
                while True:
                    time.sleep(1)

            batch_number += 1

    except KeyboardInterrupt:
        print("\nNa-stop ang script (CTRL + C).")
    finally:
        session.close()


def main() -> None:
    if len(sys.argv) < 2:
        print("Gamit: python request_site.py <URL> [once|loop] [delay_seconds]")
        print("Halimbawa:")
        print("  python request_site.py https://example.com once")
        print("  python request_site.py https://example.com loop 0.5")
        sys.exit(1)

    target_url = sys.argv[1]
    mode = sys.argv[2].strip().lower() if len(sys.argv) > 2 else "once"

    if mode not in ("once", "loop"):
        print("Invalid mode. Gamitin lamang ang 'once' o 'loop'.")
        sys.exit(1)

    try:
        delay_sec = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
        if delay_sec < 0:
            raise ValueError("Hindi pwedeng negative ang delay.")
    except ValueError:
        print("Invalid delay_seconds. Maglagay ng numero (hal. 0.5 o 1).")
        sys.exit(1)

    try:
        run_requests(
            url=target_url,
            count=50,
            delay=delay_sec,
            loop_forever=(mode == "loop"),
        )
    except ValueError as err:
        print(f"Error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()