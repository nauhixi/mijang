"""
Institutional Investor Returns Dashboard — Data Fetcher
=======================================================
Flow:
  1. SEC EDGAR submissions API  → latest 13F-HR accession per institution
  2. Filing index                → locate infotable XML document URL
  3. Parse XML                   → (cusip, issuer_name, value_usd, shares)
  4. OpenFIGI API (free)         → batch map CUSIPs → US equity tickers
  5. yfinance                    → YTD / 1M / 6M / 1Y returns per ticker
  6. Weighted-average portfolio  → institutions.json
"""

import json, time, re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import requests
import yfinance as yf

# ── Constants ─────────────────────────────────────────────────────────────────

EDGAR_HEADERS = {
    "User-Agent": "InstitutionalAlphaDashboard contact@example.com",
    "Accept-Encoding": "gzip, deflate",
}
OPENFIGI_URL = "https://api.openfigi.com/v3/mapping"
EDGAR_SLEEP  = 0.15    # ~6 req/sec  (SEC allows 10)
FIGI_SLEEP   = 2.5     # 25 req/min → 1 per 2.4 s

INSTITUTIONS = [
    {"name": "Berkshire Hathaway",      "cik": "0001067983", "type": "Conglomerate"},
    {"name": "Bridgewater Associates",  "cik": "0001350694", "type": "Macro Hedge Fund"},
    {"name": "Renaissance Technologies","cik": "0001037389", "type": "Quant Hedge Fund"},
    {"name": "Citadel Advisors",        "cik": "0001423298", "type": "Multi-Strategy"},
    {"name": "Tiger Global Management", "cik": "0001167483", "type": "Tech Hedge Fund"},
    {"name": "Appaloosa Management",    "cik": "0001656456", "type": "Hedge Fund"},
    {"name": "Viking Global Investors", "cik": "0001103804", "type": "Long/Short Equity"},
    {"name": "Pershing Square Capital", "cik": "0001336532", "type": "Activist"},
    {"name": "Two Sigma Investments",   "cik": "0001442145", "type": "Quant Hedge Fund"},
    {"name": "D.E. Shaw & Co",          "cik": "0001009207", "type": "Quant Hedge Fund"},
    {"name": "Coatue Management",       "cik": "0001336528", "type": "Tech Hedge Fund"},
    {"name": "Third Point LLC",         "cik": "0001040273", "type": "Activist"},
    {"name": "Lone Pine Capital",       "cik": "0001061768", "type": "Long/Short Equity"},
    {"name": "Baupost Group",           "cik": "0001061165", "type": "Value Hedge Fund"},
    {"name": "Greenlight Capital",      "cik": "0001079114", "type": "Long/Short Equity"},
]

FALLBACK_PORTFOLIOS = {
    "Berkshire Hathaway":      ["AAPL","BAC","AXP","KO","CVX","OXY","MCO","KHC","CB","DVA"],
    "Bridgewater Associates":  ["SPY","VWO","EEM","GLD","TLT","IEF","LQD","EFA","IEMG","IAU"],
    "Renaissance Technologies":["IWM","SPY","QQQ","EEM","GLD","AAPL","MSFT","AMZN","NVDA","META"],
    "Citadel Advisors":        ["NVDA","MSFT","AMZN","GOOGL","META","TSLA","AMD","AVGO","ORCL","CRM"],
    "Tiger Global Management": ["META","MSFT","NVDA","AMZN","GOOGL","UBER","SNOW","SHOP","SQ","COIN"],
    "Appaloosa Management":    ["META","GOOGL","MSFT","AMZN","TSLA","NVDA","ORCL","UBER","BIDU","JD"],
    "Viking Global Investors": ["META","AMZN","GOOGL","MSFT","UNH","V","MA","JPM","HD","CRM"],
    "Pershing Square Capital": ["HLT","QSR","CMG","CP","GOOGL","MKL","LOW","NFLX","NKE","UNH"],
    "Two Sigma Investments":   ["AAPL","MSFT","AMZN","GOOGL","NVDA","META","BRK-B","LLY","UNH","JPM"],
    "D.E. Shaw & Co":          ["AAPL","MSFT","AMZN","GOOGL","META","NVDA","TSLA","BRK-B","JPM","V"],
    "Coatue Management":       ["NVDA","META","MSFT","AMZN","GOOGL","TSLA","AAPL","AMD","SNOW","UBER"],
    "Third Point LLC":         ["MSFT","GOOGL","META","AMZN","PG","BABA","PYPL","SLB","RH","TGT"],
    "Lone Pine Capital":       ["MSFT","AMZN","META","GOOGL","NVDA","UBER","BKNG","WDAY","ZM","DDOG"],
    "Baupost Group":           ["NWSA","LGND","VRTX","OVV","PBF","EBAY","HCA","CCJ","GOLD","NCR"],
    "Greenlight Capital":      ["AAPL","MSFT","GM","GOLD","CCJ","GOOG","HCA","SWKS","STX","NCR"],
}


# ── EDGAR helpers ──────────────────────────────────────────────────────────────

def edgar_get(url: str, retries: int = 3):
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=EDGAR_HEADERS, timeout=20)
            if r.status_code == 200:
                return r
            if r.status_code == 429:
                print("  [rate-limit] EDGAR waiting 10 s …")
                time.sleep(10)
        except Exception as e:
            print(f"  [warn] edgar_get attempt {attempt+1}: {e}")
            time.sleep(2)
    return None


def get_latest_13f_accession(cik: str) -> dict | None:
    """Return dict with accessionNumber, filingDate, cik_int — or None."""
    url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    r = edgar_get(url)
    if not r:
        return None
    time.sleep(EDGAR_SLEEP)

    try:
        data = r.json()
    except Exception:
        return None

    cik_int = int(data.get("cik", cik.lstrip("0") or "0"))
    recent  = data.get("filings", {}).get("recent", {})

    def scan(forms, accnums, dates):
        for i, f in enumerate(forms):
            if f in ("13F-HR", "13F-HR/A"):
                return {"accessionNumber": accnums[i],
                        "filingDate":      dates[i],
                        "cik_int":         cik_int}
        return None

    hit = scan(recent.get("form", []),
               recent.get("accessionNumber", []),
               recent.get("filingDate", []))
    if hit:
        return hit

    # Older filing pages
    for fentry in data.get("filings", {}).get("files", [])[:3]:
        sub_r = edgar_get("https://data.sec.gov" + fentry["name"])
        if not sub_r:
            continue
        time.sleep(EDGAR_SLEEP)
        try:
            sub = sub_r.json()
            hit = scan(sub.get("form", []),
                       sub.get("accessionNumber", []),
                       sub.get("filingDate", []))
            if hit:
                hit["cik_int"] = cik_int
                return hit
        except Exception:
            continue

    return None


def get_infotable_xml_url(cik_int: int, accession: str) -> str | None:
    """Return the URL of the infotable XML inside a 13F filing."""
    acc_clean = accession.replace("-", "")
    base = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_clean}"

    # 1. JSON index
    idx_r = edgar_get(f"https://data.sec.gov/Archives/edgar/data/{cik_int}/{acc_clean}/{accession}-index.json")
    time.sleep(EDGAR_SLEEP)
    if idx_r:
        try:
            for doc in idx_r.json().get("directory", {}).get("item", []):
                name = doc.get("name", "").lower()
                if "infotable" in name and name.endswith(".xml"):
                    return f"{base}/{doc['name']}"
        except Exception:
            pass

    # 2. HTML index scrape
    html_r = edgar_get(f"{base}/{accession}-index.htm")
    time.sleep(EDGAR_SLEEP)
    if html_r:
        for m in re.findall(r'href="([^"]*infotable[^"]*\.xml)"', html_r.text, re.I):
            return m if m.startswith("http") else f"{base}/{m.lstrip('/')}"

    # 3. Common filename guesses
    for fname in ["infotable.xml", "form13fInfoTable.xml", "informationTable.xml"]:
        r = edgar_get(f"{base}/{fname}")
        time.sleep(EDGAR_SLEEP)
        if r:
            return f"{base}/{fname}"

    return None


def parse_infotable_xml(xml_text: str) -> list[dict]:
    """Parse 13F infotable XML → list of {cusip, name, value_usd, shares}."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"  [warn] XML parse error: {e}")
        return []

    ns_uri = re.match(r'\{(.*?)\}', root.tag).group(1) if '{' in root.tag else ""
    p = f"{{{ns_uri}}}" if ns_uri else ""

    rows = root.findall(f".//{p}infoTable") or root.findall(".//infoTable")
    holdings = []

    for row in rows:
        def txt(tag):
            el = row.find(f"{p}{tag}") or row.find(tag)
            return (el.text or "").strip() if el is not None else ""

        cusip = txt("cusip")
        name  = txt("nameOfIssuer")
        val_s = txt("value").replace(",", "")
        value_usd = int(val_s) * 1_000 if val_s.isdigit() else 0

        sa = row.find(f"{p}shrsOrPrnAmt") or row.find("shrsOrPrnAmt")
        shares = 0
        if sa is not None:
            sp = sa.find(f"{p}sshPrnamt") or sa.find("sshPrnamt")
            if sp is not None and sp.text:
                try:
                    shares = int(sp.text.replace(",", ""))
                except ValueError:
                    pass

        if cusip and value_usd > 0:
            holdings.append({"cusip": cusip, "name": name,
                              "value_usd": value_usd, "shares": shares})

    holdings.sort(key=lambda x: x["value_usd"], reverse=True)
    return holdings


# ── OpenFIGI CUSIP → ticker ───────────────────────────────────────────────────

def cusip_to_tickers(cusips: list[str]) -> dict[str, str]:
    """Batch-resolve CUSIPs to US equity tickers. Returns {cusip: ticker}."""
    result = {}
    for i in range(0, len(cusips), 10):
        batch   = cusips[i:i + 10]
        payload = [{"idType": "ID_CUSIP", "idValue": c, "exchCode": "US"} for c in batch]
        try:
            r = requests.post(OPENFIGI_URL,
                              headers={"Content-Type": "application/json"},
                              json=payload, timeout=20)
            if r.status_code == 429:
                print("  [rate-limit] OpenFIGI waiting 60 s …")
                time.sleep(60)
                r = requests.post(OPENFIGI_URL,
                                  headers={"Content-Type": "application/json"},
                                  json=payload, timeout=20)
            if r.status_code == 200:
                for cusip, entry in zip(batch, r.json()):
                    items = entry.get("data", [])
                    for item in items:
                        ticker = item.get("ticker", "")
                        stype  = item.get("securityType", "")
                        if ticker and stype in ("Common Stock", "EQS", ""):
                            result[cusip] = ticker
                            break
                    if cusip not in result and items:
                        result[cusip] = items[0].get("ticker", "")
            else:
                print(f"  [warn] OpenFIGI HTTP {r.status_code}")
        except Exception as e:
            print(f"  [warn] OpenFIGI: {e}")
        time.sleep(FIGI_SLEEP)

    return result


# ── yfinance returns ───────────────────────────────────────────────────────────

def get_stock_returns(tickers: list[str]) -> dict[str, dict]:
    """Download 1-year history for all tickers in one call."""
    clean = list({t.strip().upper() for t in tickers if t and 1 < len(t) <= 6})[:60]
    if not clean:
        return {}
    results = {}
    try:
        raw    = yf.download(clean, period="1y", auto_adjust=True, progress=False)
        closes = raw["Close"] if "Close" in raw.columns else raw
        if closes.empty:
            return {}
        now = closes.index[-1]

        for ticker in clean:
            if ticker not in closes.columns:
                continue
            s = closes[ticker].dropna()
            if len(s) < 5:
                continue

            ytd_s = s[s.index >= f"{now.year}-01-01"]
            ytd   = ((ytd_s.iloc[-1] / ytd_s.iloc[0]) - 1) * 100 if len(ytd_s) > 1 else 0.0
            m1    = s[s.index >= (now - timedelta(days=30))]
            r1m   = ((m1.iloc[-1] / m1.iloc[0]) - 1) * 100 if len(m1) > 1 else 0.0
            m6    = s[s.index >= (now - timedelta(days=182))]
            r6m   = ((m6.iloc[-1] / m6.iloc[0]) - 1) * 100 if len(m6) > 1 else 0.0
            r1y   = ((s.iloc[-1] / s.iloc[0]) - 1) * 100

            results[ticker] = {
                "ytd":    round(float(ytd), 2),
                "ret_1m": round(float(r1m), 2),
                "ret_6m": round(float(r6m), 2),
                "ret_1y": round(float(r1y), 2),
                "price":  round(float(s.iloc[-1]), 2),
            }
    except Exception as e:
        print(f"  [warn] yfinance: {e}")
    return results


def weighted_return(holdings: list[dict], stock_rets: dict) -> dict:
    total = sum(h["value_usd"] for h in holdings)
    if total == 0:
        return {"ytd": 0, "ret_1m": 0, "ret_6m": 0, "ret_1y": 0, "coverage": 0}
    w = {"ytd": 0.0, "ret_1m": 0.0, "ret_6m": 0.0, "ret_1y": 0.0}
    covered = 0
    for h in holdings:
        t = h.get("ticker", "")
        if t and t in stock_rets and h["value_usd"] > 0:
            frac = h["value_usd"] / total
            for k in w:
                w[k] += frac * stock_rets[t].get(k, 0)
            covered += h["value_usd"]
    coverage = round(covered / total * 100, 1) if total else 0
    return {k: round(v, 2) for k, v in w.items()} | {"coverage": coverage}


def fetch_benchmarks() -> dict:
    bench = {"S&P 500": "^GSPC", "NASDAQ": "^IXIC",
             "Dow Jones": "^DJI", "Russell 2000": "^RUT"}
    out = {}
    for name, sym in bench.items():
        try:
            d  = yf.Ticker(sym).history(period="1y")["Close"].dropna()
            if len(d) < 2:
                continue
            now   = d.index[-1]
            ytd_s = d[d.index >= f"{now.year}-01-01"]
            ytd   = ((ytd_s.iloc[-1] / ytd_s.iloc[0]) - 1) * 100 if len(ytd_s) > 1 else 0
            m1    = d[d.index >= (now - timedelta(days=30))]
            r1m   = ((m1.iloc[-1] / m1.iloc[0]) - 1) * 100 if len(m1) > 1 else 0
            r1y   = ((d.iloc[-1] / d.iloc[0]) - 1) * 100
            out[name] = {
                "ytd":    round(float(ytd), 2),
                "ret_1m": round(float(r1m), 2),
                "ret_1y": round(float(r1y), 2),
                "price":  round(float(d.iloc[-1]), 2),
            }
        except Exception as e:
            print(f"  [warn] benchmark {sym}: {e}")
    return out


# ── Per-institution processing ────────────────────────────────────────────────

def process_institution(inst: dict) -> dict:
    name = inst["name"]
    cik  = inst["cik"]
    print(f"\n── {name} (CIK {cik})")

    holdings      = []
    filing_date   = "N/A"
    used_fallback = False

    # Step 1: latest 13F accession
    meta = get_latest_13f_accession(cik)
    if not meta:
        print("  ✗ No 13F found → fallback")
        used_fallback = True
    else:
        filing_date = meta["filingDate"]
        print(f"  ✓ Accession {meta['accessionNumber']}  ({filing_date})")

        # Step 2: XML URL
        xml_url = get_infotable_xml_url(meta["cik_int"], meta["accessionNumber"])
        if not xml_url:
            print("  ✗ infotable XML not found → fallback")
            used_fallback = True
        else:
            print(f"  ✓ XML: …/{xml_url.split('/')[-1]}")
            r = edgar_get(xml_url)
            time.sleep(EDGAR_SLEEP)
            if not r:
                print("  ✗ XML download failed → fallback")
                used_fallback = True
            else:
                # Step 3: parse
                holdings = parse_infotable_xml(r.text)
                print(f"  ✓ Parsed {len(holdings)} holdings")
                if not holdings:
                    print("  ✗ Empty parse → fallback")
                    used_fallback = True

    if used_fallback:
        tickers = FALLBACK_PORTFOLIOS.get(name, [])
        eq_val  = 1_000_000_000 // max(len(tickers), 1)
        holdings = [{"cusip": "", "name": t, "ticker": t,
                     "value_usd": eq_val, "shares": 0}
                    for t in tickers]
    else:
        # Step 4: CUSIP → ticker
        cusips    = list(dict.fromkeys(h["cusip"] for h in holdings[:50] if h["cusip"]))
        print(f"  ✓ Mapping {len(cusips)} CUSIPs via OpenFIGI …")
        cmap      = cusip_to_tickers(cusips)
        print(f"  ✓ Resolved {len(cmap)} tickers")
        for h in holdings:
            h["ticker"] = cmap.get(h["cusip"], "")

    # Step 5: yfinance
    all_tickers = list({h["ticker"] for h in holdings if h.get("ticker")})
    print(f"  ✓ yfinance for {len(all_tickers)} tickers …")
    stock_rets = get_stock_returns(all_tickers)
    print(f"  ✓ Returns for {len(stock_rets)} tickers")

    # Step 6: assemble
    total_val = sum(h["value_usd"] for h in holdings) or 1
    top_10 = []
    for h in holdings[:10]:
        t  = h.get("ticker", "")
        sr = stock_rets.get(t, {})
        top_10.append({
            "ticker":     t or h.get("name", "")[:8],
            "ytd":        sr.get("ytd", 0),
            "ret_1y":     sr.get("ret_1y", 0),
            "price":      sr.get("price", 0),
            "weight_pct": round(h["value_usd"] / total_val * 100, 1),
        })

    return {
        "name":             name,
        "type":             inst["type"],
        "filing_date":      filing_date,
        "holding_count":    len(holdings),
        "used_fallback":    used_fallback,
        "portfolio_return": weighted_return(holdings, stock_rets),
        "top_holdings":     top_10,
    }


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    start = datetime.now(timezone.utc)
    print(f"[{start.isoformat()}] Institutional Alpha — data fetch\n")

    output = {
        "last_updated": start.strftime("%Y-%m-%d %H:%M UTC"),
        "institutions":  [],
        "benchmarks":    {},
    }

    print("── Benchmarks")
    output["benchmarks"] = fetch_benchmarks()
    print(f"   {list(output['benchmarks'].keys())}\n")

    for inst in INSTITUTIONS:
        output["institutions"].append(process_institution(inst))

    output["institutions"].sort(
        key=lambda x: x["portfolio_return"].get("ytd", -999), reverse=True)
    for i, inst in enumerate(output["institutions"]):
        inst["rank"] = i + 1

    out_path = Path(__file__).parent.parent / "data" / "institutions.json"
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    live = sum(1 for i in output["institutions"] if not i.get("used_fallback"))
    fb   = len(output["institutions"]) - live
    elapsed = (datetime.now(timezone.utc) - start).seconds
    print(f"\n✅  {out_path}")
    print(f"   Live EDGAR + OpenFIGI : {live}")
    print(f"   Fallback tickers      : {fb}")
    print(f"   Elapsed               : {elapsed}s")


if __name__ == "__main__":
    main()
