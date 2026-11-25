import json
import subprocess
import time
import re

schedule_jul_sep = [
  {
    "year": 2026,
    "month": 7,
    "days": [
      { "date": 1, "events": "求人受付開始" },
      { "date": 2, "events": "1学期期末考査" },
      { "date": 3, "events": "求人票公開 1年生進路希望調査（職業分野）\n第1回歯科健診 結核健診" },
      { "date": 4, "events": "名進研模試（予備日）" },
      { "date": 5, "events": "1年、2年進研模試" },
      { "date": 10, "events": "(水)3年進路学年集会" },
      { "date": 14, "events": "保護者会① 午前授業[456]" },
      { "date": 15, "events": "保護者会② 午前授業[456]" },
      { "date": 16, "events": "保護者会③ 午前授業[456]" },
      { "date": 17, "events": "保護者会④ 午前授業[456]\n追考査該当者指導\n1年 夢ナビクエスト（国数）" },
      { "date": 18, "events": "保護者会⑤ 午前授業[456]\n【全】3年就職前事前指導\n1学期終業式" },
      { "date": 19, "events": "第二種電気工事士技能試験" },
      { "date": 20, "events": "【海の日】" },
      { "date": 21, "events": "歯科追加指導\n図書館閉館 〜8/5" },
      { "date": 23, "events": "追考査1日目" },
      { "date": 24, "events": "追考査2日目" },
      { "date": 25, "events": "第2回全統共通テスト模試（自校会場）" },
      { "date": 28, "events": "高校生防災セミナー① (名古屋大学豊田講堂)" }
    ]
  },
  {
    "year": 2026,
    "month": 8,
    "days": [
      { "date": 1, "events": "就職希望者履歴書指導開始" },
      { "date": 2, "events": "第1種電気工事士補講開始" },
      { "date": 5, "events": "愛知県産業教育フェア（ウインクあいち）" },
      { "date": 8, "events": "就職指導合宿（校内）\n同窓会総会" },
      { "date": 11, "events": "【山の日】" },
      { "date": 20, "events": "全国高Ｐ連大会（大分大会）\nものづくりコンテスト東海大会（溶接競技）" },
      { "date": 21, "events": "全国高Ｐ連大会（大分大会）\nものづくりコンテスト東海大会（溶接競技）" },
      { "date": 22, "events": "第2回全統記述模試 (自校会場)" },
      { "date": 24, "events": "3年面接指導（〜9/8）" },
      { "date": 28, "events": "2学期始業式 身だしなみ確認②\n1・2年進路希望調査(9/1〆切)" },
      { "date": 31, "events": "面接週間〜9/11 (9/4を除く)" }
    ]
  },
  {
    "year": 2026,
    "month": 9,
    "days": [
      { "date": 1, "events": "1・2年スタディーサポート 第2回\n第3回就職模擬面接" },
      { "date": 3, "events": "(火)1年進路学年集会 (体育館)\n就職応募書類発送\n1年進路希望調査\n修学旅行費集金 (業者集金日)" },
      { "date": 7, "events": "第1回推薦選考会議" },
      { "date": 8, "events": "3年公務員講座" },
      { "date": 10, "events": "3年生共通テスト出願書類配布" },
      { "date": 11, "events": "第2回推薦選考会議" },
      { "date": 16, "events": "就職試験開始" },
      { "date": 18, "events": "指定校推薦者指導会" },
      { "date": 21, "events": "【敬老の日】" },
      { "date": 22, "events": "【国民の休日】" },
      { "date": 23, "events": "【秋分の日】" },
      { "date": 24, "events": "(金)2年進路外郭講師講話 (体育館)" },
      { "date": 26, "events": "専攻科特別推薦入学者選抜\n2学期中間テスト週間 〜10/2(金)" }
    ]
  }
]

REPO_ID = "R_kgDOUJdbYg"
ISSUE_TYPE_ID = "IT_kwDODw6M1c4y5y68"
START_DATE_FIELD_ID = "IFD_kgDOAkshqw"
TARGET_DATE_FIELD_ID = "IFD_kgDOAkshrA"
DATE_STATUS_FIELD_ID = "IFSS_kgDOAsK19Q"
DATE_STATUS_NEXT_OPTION_ID = "IFSSO_kgDOBNUD8g"

def parse_end_date(title, start_date_str, year, month):
    m = re.search(r'[〜~](\d{1,2})/(\d{1,2})', title)
    if m:
        e_month = int(m.group(1))
        e_day = int(m.group(2))
        e_year = year if e_month >= month else year + 1
        return f"{e_year}-{e_month:02d}-{e_day:02d}"
    
    m_day = re.search(r'[〜~](\d{1,2})日', title)
    if m_day:
        e_day = int(m_day.group(1))
        return f"{year}-{month:02d}-{e_day:02d}"

    return start_date_str

events_to_create = []
for m_data in schedule_jul_sep:
    y = m_data["year"]
    m = m_data["month"]
    for d in m_data["days"]:
        if not d["events"]:
            continue
        date_str = f"{y}-{m:02d}-{d['date']:02d}"
        lines = [l.strip() for l in d["events"].split("\n") if l.strip()]
        for ev in lines:
            end_date_str = parse_end_date(ev, date_str, y, m)
            events_to_create.append({
                "title": ev,
                "start": date_str,
                "end": end_date_str
            })

print(f"Total July-September events to create: {len(events_to_create)}")

MUTATION_TEMPLATE = """
mutation CreateCalendarIssue($input: CreateIssueInput!) {
  createIssue(input: $input) {
    issue {
      id
      number
      title
    }
  }
}
"""

for idx, ev in enumerate(events_to_create, 1):
    body_text = f"予定日: {ev['start']}"
    if ev['end'] != ev['start']:
        body_text += f" 〜 {ev['end']}"

    variables = {
        "input": {
            "repositoryId": REPO_ID,
            "title": ev["title"],
            "body": body_text,
            "issueTypeId": ISSUE_TYPE_ID,
            "issueFields": [
                {
                    "fieldId": START_DATE_FIELD_ID,
                    "dateValue": ev["start"]
                },
                {
                    "fieldId": TARGET_DATE_FIELD_ID,
                    "dateValue": ev["end"]
                },
                {
                    "fieldId": DATE_STATUS_FIELD_ID,
                    "singleSelectOptionId": DATE_STATUS_NEXT_OPTION_ID
                }
            ]
        }
    }

    payload = json.dumps({"query": MUTATION_TEMPLATE, "variables": variables})
    p = subprocess.Popen(["gh", "api", "graphql", "--input", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = p.communicate(input=payload)

    if p.returncode == 0 and "errors" not in stdout:
        print(f"[{idx}/{len(events_to_create)}] Created: {ev['title']} ({ev['start']} -> {ev['end']})")
    else:
        print(f"[{idx}/{len(events_to_create)}] Error creating {ev['title']}: {stderr} {stdout}")
    
    time.sleep(0.15)

print("Finished importing July-September calendar issues!")
