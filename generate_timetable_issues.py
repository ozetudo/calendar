import json
import subprocess
import datetime
import time

REPO_ID = "R_kgDOUJdbYg"
ISSUE_TYPE_ID = "IT_kwDODw6M1c4y5y68"
START_DATE_FIELD_ID = "IFD_kgDOAkshqw"
TARGET_DATE_FIELD_ID = "IFD_kgDOAkshrA"
DATE_STATUS_FIELD_ID = "IFSS_kgDOAsK19Q"
DATE_STATUS_NEXT_OPTION_ID = "IFSSO_kgDOBNUD8g"

# 時間割の定義 (月〜金)
# 0: Monday, 1: Tuesday, 2: Wednesday, 3: Thursday, 4: Friday
daily_schedule = {
    0: "【月曜時間割】1:電気回路(友田) 2:体育 3:選択A 4:家庭基礎 5:英コミュⅡ 6:電子回路(永田) 7:プログラミング(友田/永田)",
    1: "【火曜時間割】1〜3:実習 4:現代の国語(渡邊) 5:英コミュⅡ 6:数学Ⅱ(阪野)",
    2: "【水曜時間割】1:数学Ⅱ(阪野) 2:体育 3:現代の国語(渡邊) 4:公共(黒崎) 5:化学基礎(鎌倉) 6:プログラミング 7:電子回路",
    3: "【木曜時間割】1:保健(嘉正) 2:化学基礎(鎌倉) 3:選択A 4:電気回路(友田) 5:数学Ⅱ(阪野) 6:HR",
    4: "【金曜時間割】1:公共(黒崎) 2:英コミュⅡ 3:家庭基礎 4〜6:実習"
}

# 祝日・長期休暇・登校なし等の除外日 (土日は元々除外)
# 2026-04-01 〜 2027-01-31
# 4月始業式(4/7)以前、夏休み(7/19〜8/27)、冬休み(12/24〜1/6)
start_date = datetime.date(2026, 4, 7)
end_date = datetime.date(2027, 1, 22)

# 除外日リスト (祝日・長期休み・テスト日以外の登校なし日など)
holidays_and_breaks = {
    # 祝日・振替休日
    datetime.date(2026, 4, 29), # 昭和の日
    datetime.date(2026, 5, 4),  # みどりの日
    datetime.date(2026, 5, 5),  # こどもの日
    datetime.date(2026, 5, 6),  # 振替休日
    datetime.date(2026, 7, 20), # 海の日
    datetime.date(2026, 8, 11), # 山の日
    datetime.date(2026, 9, 21), # 敬老の日
    datetime.date(2026, 9, 22), # 国民の休日
    datetime.date(2026, 9, 23), # 秋分の日
    datetime.date(2026, 10, 12),# スポーツの日
    datetime.date(2026, 11, 3), # 文化の日
    datetime.date(2026, 11, 23),# 勤労感謝の日
    datetime.date(2026, 11, 24),# あいち県民の日
    datetime.date(2026, 12, 7), # 技能五輪代休
    datetime.date(2027, 1, 11), # 成人の日
}

# 夏休み期間: 7/19 〜 8/27
summer_start = datetime.date(2026, 7, 19)
summer_end = datetime.date(2026, 8, 27)

# 冬休み期間: 12/24 〜 1/6
winter_start = datetime.date(2026, 12, 24)
winter_end = datetime.date(2027, 1, 6)

def is_school_day(d):
    # 土日は除外
    if d.weekday() >= 5:
        return False
    if d in holidays_and_breaks:
        return False
    if summer_start <= d <= summer_end:
        return False
    if winter_start <= d <= winter_end:
        return False
    return True

curr = start_date
school_days = []
while curr <= end_date:
    if is_school_day(curr):
        w = curr.weekday()
        # 特殊: 11/4(水)は「月曜日授業」
        if curr == datetime.date(2026, 11, 4):
            title = daily_schedule[0] + " (※月曜授業振替)"
        else:
            title = daily_schedule[w]
        school_days.append((curr.strftime("%Y-%m-%d"), title, w))
    curr += datetime.timedelta(days=1)

print(f"Total school days to add timetable: {len(school_days)}")

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

for idx, (date_str, title, w) in enumerate(school_days, 1):
    day_names = ["月", "火", "水", "木", "金"]
    body_text = f"【26クラス {day_names[w]}曜時間割】\n\n日付: {date_str}\n\n内容:\n" + title.replace("【", "").replace("】", "\n- ")

    variables = {
        "input": {
            "repositoryId": REPO_ID,
            "title": title,
            "body": body_text,
            "issueTypeId": ISSUE_TYPE_ID,
            "issueFields": [
                {
                    "fieldId": START_DATE_FIELD_ID,
                    "dateValue": date_str
                },
                {
                    "fieldId": TARGET_DATE_FIELD_ID,
                    "dateValue": date_str
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
        print(f"[{idx}/{len(school_days)}] Added timetable for {date_str}: {title[:25]}...")
    else:
        print(f"[{idx}/{len(school_days)}] Error: {stderr} {stdout}")
    
    time.sleep(0.1)

print("Finished adding timetable to all school days!")
