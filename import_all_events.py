import json
import subprocess
import time
import re

schedule_data = {
  "April": [
    { "date": 3, "events": ["新任式 2,3年出校日"] },
    { "date": 6, "events": ["入学式・PTA入会式"] },
    { "date": 7, "events": ["始業式・対面式", "身だしなみ確認①", "2,3年進路希望調査(4/13〆切)", "[12345]スタディーサポート"] },
    { "date": 8, "events": ["[6]総務・教務・保健OR", "[7]生徒指導OR(1年)"] },
    { "date": 9, "events": ["[1]1・2年クレペリン検査", "[2]1年クラス写真", "[3]1年生徒会OR", "[4]1年進路OR", "[56]1年個人写真", "[業後]1年自転車点検", "[6]3年クレペリン検査60分"] },
    { "date": 10, "events": ["[1]交通安全講話(全校)", "[6]職業適性検査※70分", "[業後]1年自転車点検(予備)"] },
    { "date": 13, "events": ["[12]1年教務部OR/学科OR", "1年心電図・X線検査(PM)", "[4〜7]1年工業技術基礎OR", "[6]3年修学旅行事前指導", "3年 修学旅行 1日目"] },
    { "date": 15, "events": ["3年 修学旅行 2日目", "[8:20]リコーダー販売"] },
    { "date": 16, "events": ["3年 修学旅行 3日目", "耳鼻科検診①", "1年 図書館OR(〜5/28)", "部活動体験(〜4/22)"] },
    { "date": 17, "events": ["内科検診①"] },
    { "date": 20, "events": ["面接週間〜5/1"] },
    { "date": 21, "events": ["体力テスト", "生徒図書委員会", "2年進学補講開始", "キャリアデザインプログラム①"] },
    { "date": 23, "events": ["眼科検診①(5・6限)", "部活動登録"] },
    { "date": 24, "events": ["体力テスト(予備日)", "3年進学補講開始"] },
    { "date": 28, "events": ["内科検診②"] },
    { "date": 29, "events": ["【昭和の日】"] },
    { "date": 30, "events": ["眼科検診②", "[6]3年卒業生と語る会(体育館他)"] }
  ],
  "May": [
    { "date": 3, "events": ["【憲法記念日】", "第1回全統共通テスト模試(公開会場)"] },
    { "date": 4, "events": ["【みどりの日】"] },
    { "date": 5, "events": ["【こどもの日】"] },
    { "date": 6, "events": ["【振替休日】"] },
    { "date": 7, "events": ["[6]第1回防災訓練・各科対面式"] },
    { "date": 8, "events": ["耳鼻科検診②"] },
    { "date": 10, "events": ["第1回全統記述模試(公開会場)"] },
    { "date": 11, "events": ["内科検診③"] },
    { "date": 12, "events": ["尿検査1次①"] },
    { "date": 13, "events": ["尿検査1次②"] },
    { "date": 14, "events": ["3年進路学年集会", "耳鼻科検診③"] },
    { "date": 15, "events": ["内科検診④"] },
    { "date": 16, "events": ["1学期確認テスト週間 〜5/22(金)"] },
    { "date": 17, "events": ["測量士補試験"] },
    { "date": 18, "events": ["第2回進路希望調査 配布", "歯科検診①(AM)"] },
    { "date": 21, "events": ["1学期確認テスト", "PTA総会 1年保護者進路説明会", "2年保護者進路説明会 3年保護者進路説明会"] },
    { "date": 22, "events": ["1学期確認テスト"] },
    { "date": 23, "events": ["総合競技大会(全体競技)"] },
    { "date": 24, "events": ["総合競技大会(球技2日目)", "第二種電気工事士筆記試験"] },
    { "date": 26, "events": ["3年公務員講座"] },
    { "date": 27, "events": ["尿検査2次", "第2回進路希望調査 提出締切"] },
    { "date": 28, "events": ["歯科検診②(PM)"] },
    { "date": 29, "events": ["内科検診⑤", "3年進路希望調査配布(6/3〆切)"] }
  ],
  "June": [
    { "date": 1, "events": ["歯科検診③(AM)", "内科検診⑥", "第1回進路面接(6月17日まで)"] },
    { "date": 2, "events": ["内科検診⑦"] },
    { "date": 3, "events": ["体育祭(ガイシホール)"] },
    { "date": 4, "events": ["[6]1年職適説明会"] },
    { "date": 5, "events": ["内科検診⑧"] },
    { "date": 6, "events": ["中学生向けディープクエスト"] },
    { "date": 7, "events": ["2級土木施工管理技術検定(第一次検定)", "2級電気通信工事施工管理技術検定(第一次検定)"] },
    { "date": 8, "events": ["歯科検診④(AM)", "内科検診⑨"] },
    { "date": 9, "events": ["内科検診⑩"] },
    { "date": 10, "events": ["尿検査(予備)"] },
    { "date": 12, "events": ["第57回機械製図検定試験(一次)", "内科検診⑪"] },
    { "date": 13, "events": ["生徒登校禁止"] },
    { "date": 14, "events": ["生徒登校禁止", "2級建築施工管理技術検定(第一次検定)", "2級電気工事施工管理技術検定(第一次検定)"] },
    { "date": 16, "events": ["3年公務員講座"] },
    { "date": 18, "events": ["[6]1年進路学年集会", "第3回進路希望調査 配布", "耳鼻科検診④"] },
    { "date": 19, "events": ["第94回計算技術検定", "1学期期末考査週間〜7/2(木)"] },
    { "date": 25, "events": ["耳鼻科検診⑤"] },
    { "date": 26, "events": ["第76回情報技術検定", "1学期末考査"] },
    { "date": 29, "events": ["1学期末考査"] },
    { "date": 30, "events": ["1学期末考査"] }
  ]
}

REPO_ID = "R_kgDOUJdbYg"
ISSUE_TYPE_ID = "IT_kwDODw6M1c4y5y68"
START_DATE_FIELD_ID = "IFD_kgDOAkshqw"
TARGET_DATE_FIELD_ID = "IFD_kgDOAkshrA"
DATE_STATUS_FIELD_ID = "IFSS_kgDOAsK19Q"
DATE_STATUS_NEXT_OPTION_ID = "IFSSO_kgDOBNUD8g"

month_map = {"April": ("04", 4), "May": ("05", 5), "June": ("06", 6)}

def parse_end_date(title, start_date_str, start_month_num, start_day):
    m = re.search(r'[〜~](\d{1,2})/(\d{1,2})', title)
    if m:
        e_month = int(m.group(1))
        e_day = int(m.group(2))
        return f"2026-{e_month:02d}-{e_day:02d}"
    
    m_day = re.search(r'[〜~](\d{1,2})日', title)
    if m_day:
        e_day = int(m_day.group(1))
        return f"2026-{start_month_num:02d}-{e_day:02d}"

    return start_date_str

events_to_create = []
for month, days in schedule_data.items():
    m_str, m_num = month_map[month]
    for d in days:
        date_str = f"2026-{m_str}-{d['date']:02d}"
        for ev in d["events"]:
            # Skip first event as it was already created in test
            if ev == "新任式 2,3年出校日" and date_str == "2026-04-03":
                continue
            end_date_str = parse_end_date(ev, date_str, m_num, d['date'])
            events_to_create.append({
                "title": ev,
                "start": date_str,
                "end": end_date_str
            })

print(f"Creating {len(events_to_create)} issues...")

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

print("Finished importing all calendar issues!")
