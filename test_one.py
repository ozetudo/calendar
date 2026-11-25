import subprocess
import json

mutation = """
mutation CreateIssue($input: CreateIssueInput!) {
  createIssue(input: $input) {
    issue {
      id
      number
      title
    }
  }
}
"""

variables = {
    "input": {
        "repositoryId": "R_kgDOUJdbYg",
        "title": "新任式 2,3年出校日",
        "body": "予定日: 2026-04-03",
        "issueTypeId": "IT_kwDODw6M1c4y5y68",
        "issueFields": [
            {
                "fieldId": "IFD_kgDOAkshqw",
                "date": "2026-04-03"
            },
            {
                "fieldId": "IFD_kgDOAkshrA",
                "date": "2026-04-03"
            },
            {
                "fieldId": "IFSS_kgDOAsK19Q",
                "singleSelectOptionId": "IFSSO_kgDOBNUD8g"
            }
        ]
    }
}

cmd = [
    "gh", "api", "graphql",
    "-f", f"query={mutation}",
    "--input", "-"
]

p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = p.communicate(input=json.dumps({"query": mutation, "variables": variables}))
print("STDOUT:", stdout)
print("STDERR:", stderr)
