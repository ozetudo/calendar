import json
import subprocess
import time

REPO_ID = "R_kgDOUJdbYg"
ISSUE_TYPE_ID = "IT_kwDODw6M1c4y5y68"
START_DATE_FIELD_ID = "IFD_kgDOAkshqw"
TARGET_DATE_FIELD_ID = "IFD_kgDOAkshrA"
DATE_STATUS_FIELD_ID = "IFSS_kgDOAsK19Q"
DATE_STATUS_NEXT_OPTION_ID = "IFSSO_kgDOBNUD8g"

c109_events = [
    {
        "title": "【C109篠澤広と数学しよう！】参加表明締切",
        "date": "2026-09-06",
        "body": "C109篠澤広×数学合同企画「篠澤広と数学しよう！4さつめ！」\n\n- 参加表明締切日: 2026/09/06"
    },
    {
        "title": "【C109篠澤広と数学しよう！】初稿締切・校閲校正期間開始",
        "date": "2026-10-18",
        "body": "C109篠澤広×数学合同企画「篠澤広と数学しよう！4さつめ！」\n\n- 初稿締切日: 2026/10/18\n- 以降、校閲校正期間"
    },
    {
        "title": "【C109篠澤広と数学しよう！】最終稿締切・組版最終チェック",
        "date": "2026-11-29",
        "body": "C109篠澤広×数学合同企画「篠澤広と数学しよう！4さつめ！」\n\n- 最終稿締切日: 2026/11/29\n- 組版最終チェック"
    },
    {
        "title": "【C109】篠澤広と数学しよう！4さつめ！頒布日",
        "date": "2026-12-29",
        "body": "【C109】篠澤広×数学合同企画「篠澤広と数学しよう！4さつめ！」頒布日\n\n- 開催日: 2026/12/29"
    }
]

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

for idx, ev in enumerate(c109_events, 1):
    variables = {
        "input": {
            "repositoryId": REPO_ID,
            "title": ev["title"],
            "body": ev["body"],
            "issueTypeId": ISSUE_TYPE_ID,
            "issueFields": [
                {
                    "fieldId": START_DATE_FIELD_ID,
                    "dateValue": ev["date"]
                },
                {
                    "fieldId": TARGET_DATE_FIELD_ID,
                    "dateValue": ev["date"]
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
        print(f"[{idx}/{len(c109_events)}] Created: {ev['title']} ({ev['date']})")
    else:
        print(f"[{idx}/{len(c109_events)}] Error: {stderr} {stdout}")
    
    time.sleep(0.2)

print("Finished importing C109 events!")
