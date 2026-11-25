import json
import subprocess
import time
import re

schedule_oct_jan = [
  {
    "year": 2026,
    "month": 10,
    "days": [
      { "date": 1, "events": "2学期中間テスト" },
      { "date": 2, "events": "2学期中間テスト\n【東南】自動車学校説明会" },
      { "date": 3, "events": "第3回全統記述模試 (自校会場)" },
      { "date": 4, "events": "第一種電気工事士筆記試験" },
      { "date": 6, "events": "生徒会役員選挙" },
      { "date": 7, "events": "1年校外学習(予備日)" },
      { "date": 9, "events": "第2回リスニング基礎検定\n2年 校外学習" },
      { "date": 12, "events": "【スポーツの日】" },
      { "date": 13, "events": "2年公務員講座\n文化祭準備期間〜10/24" },
      { "date": 17, "events": "第3回全統共通テスト模試 (自校会場)" },
      { "date": 22, "events": "進路考査該当者指導\n【全】3年生進学希望者説明会" },
      { "date": 24, "events": "産業教育フェア協賛大会・全国産業教育振興大会\n全国高校生ロボット競技大会" },
      { "date": 25, "events": "産業教育フェア協賛大会\n全国高校生ロボット競技大会\n2級土木施工管理技術検定 (第一次検定)" },
      { "date": 27, "events": "進路考査該当者指導\n公務員講座" },
      { "date": 30, "events": "GTEC (校内)" },
      { "date": 31, "events": "GTEC (公開)" }
    ]
  },
  {
    "year": 2026,
    "month": 11,
    "days": [
      { "date": 2, "events": "2年公務員講座" },
      { "date": 3, "events": "【文化の日】" },
      { "date": 4, "events": "月曜日授業\n（読書週間〜11/14）" },
      { "date": 5, "events": "進路考査\n(木) 第2回防災訓練" },
      { "date": 6, "events": "就職考査結果報告" },
      { "date": 7, "events": "1年、2年進研模試" },
      { "date": 8, "events": "2級建築施工管理技術検定 (第一次検定)\n2級電気工事施工管理技術検定 (第一次検定)" },
      { "date": 9, "events": "四者面談①" },
      { "date": 10, "events": "四者面談②\n生徒会役員任命式" },
      { "date": 11, "events": "四者面談③" },
      { "date": 12, "events": "(水)中京大学連携授業\n技能五輪全国大会推戴式" },
      { "date": 14, "events": "全統プレ共通テスト (自校会場)" },
      { "date": 15, "events": "2級電気通信工事施工管理技術検定 (第一次検定)" },
      { "date": 19, "events": "2学期期末考査週間〜12/2(水)" },
      { "date": 20, "events": "第95回計算技術検定" },
      { "date": 22, "events": "第一種電気工事士技能試験" },
      { "date": 23, "events": "【勤労感謝の日】" },
      { "date": 24, "events": "あいち県民の日" },
      { "date": 26, "events": "2学期期末考査\nPTA研修会" },
      { "date": 27, "events": "2学期期末考査" },
      { "date": 29, "events": "技能五輪A競技 技能五輪全国大会" },
      { "date": 30, "events": "2学期期末考査" }
    ]
  },
  {
    "year": 2026,
    "month": 12,
    "days": [
      { "date": 1, "events": "2年公務員講座 2学期期末考査\n技能五輪B競技" },
      { "date": 2, "events": "2学期期末考査" },
      { "date": 3, "events": "(火)人権講話\n技能五輪C競技" },
      { "date": 4, "events": "技能五輪全国大会 開会式\n人権週間〜" },
      { "date": 5, "events": "技能五輪全国会 (全校見学日)" },
      { "date": 6, "events": "技能五輪全国大会" },
      { "date": 7, "events": "代休\n技能五輪全国大会 閉会式" },
      { "date": 10, "events": "(金)1年進路学年集会 (体育館)\n国連人権デー" },
      { "date": 11, "events": "成績個票配布" },
      { "date": 12, "events": "専攻科一般選抜入学者入試\n第5回ロボットSIリーグ" },
      { "date": 13, "events": "第5回ロボットSIリーグ" },
      { "date": 14, "events": "愛知総合工科高等学校第4回デザイン工学科展搬入" },
      { "date": 15, "events": "愛知総合工科高等学校第4回デザイン工学科展" },
      { "date": 16, "events": "保護者会① 午前授業[123]" },
      { "date": 17, "events": "保護者会② 午前授業[123]" },
      { "date": 18, "events": "保護者会③ 午前授業[123]\n追考査・追認考査該当者指導" },
      { "date": 20, "events": "愛知総合工科高等学校第4回デザイン工学科展搬出" },
      { "date": 21, "events": "保護者会④ 午前授業[123]" },
      { "date": 22, "events": "保護者会⑤ 午前授業[123]" },
      { "date": 23, "events": "2学期終業式\n追認考査該当者管理職指導\n図書館報発行\n追考査 1日目" },
      { "date": 25, "events": "追考査 2日目\n高校生防災セミナー② (名古屋大学減災館)" }
    ]
  },
  {
    "year": 2027,
    "month": 1,
    "days": [
      { "date": 1, "events": "【元日】" },
      { "date": 7, "events": "3学期始業式\n身だしなみ指導" },
      { "date": 11, "events": "【成人の日】" },
      { "date": 14, "events": "3年学年末考査〜1/20(水)" },
      { "date": 15, "events": "3年共テ事前指導" },
      { "date": 16, "events": "大学入学共通テスト" },
      { "date": 17, "events": "大学入学共通テスト" },
      { "date": 18, "events": "3年学年末考査" },
      { "date": 19, "events": "3年学年末考査" },
      { "date": 20, "events": "3年学年末考査" }
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
for m_data in schedule_oct_jan:
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

print(f"Total October-January events to create: {len(events_to_create)}")

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

print("Finished importing October-January calendar issues!")
