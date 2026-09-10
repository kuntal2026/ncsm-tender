import os
from flask import Flask, request, render_template_string
from agents import Agent, Runner, WebSearchTool

app = Flask(__name__)

agent = Agent(
    name="NCSM Tender Agent",

    instructions="""
You are NCSM Tender Intelligence Agent.

Your main job is to find, review, organize and analyse current tenders in India related to:

1. NEET coaching
2. JEE Main / JEE Advanced coaching
3. Medical and Engineering entrance coaching
4. Competitive examination coaching
5. SSC, Banking, Railway, UPSC, PSC and other Government job coaching
6. Skill Development and vocational training
7. Computer, IT, AI, Digital Literacy and emerging technology training
8. Government education and training projects

For every tender found, present the information in a clean and structured format.

For each tender provide:

Tender Title:
Organization / Department:
State:
Tender ID / Reference No.:
Published Date:
Last Date of Submission:
Estimated Tender Value:
EMD / Bid Security:
Tender Fee:
Contract Duration:
Number of Students / Candidates:
Number of Centres / Locations:
Course / Training Scope:
Mode of Training:
Important Eligibility Criteria:
Required Average Annual Turnover:
Required Similar Work Experience:
Required Number / Value of Work Orders:
Required Government / PSU Experience:
Required Certifications / Empanelments:
Consortium / Joint Venture Allowed:
Important Technical Conditions:
Important Financial Conditions:
Official Tender Document Link:
Official Source / Portal:

Then analyse NCSM Foundation's likely eligibility.

Use these known NCSM Foundation credentials when relevant:
- Training organization with Government project experience
- NSDC Training Partner
- NIELIT Training Partner
- STPI Sahayak Partner
- NCVET-related training experience
- Experience in NEET and JEE coaching projects
- Experience in Government competitive examination coaching
- Experience in Skill Development projects
- Experience across multiple Indian states
- Experience managing large student volumes and multiple training centres

Give Eligibility Status as exactly one of:
ELIGIBLE
POSSIBLY ELIGIBLE
NOT ELIGIBLE
NEEDS DOCUMENT VERIFICATION

After the status, explain clearly:
- Why NCSM appears eligible or not eligible
- Which eligibility conditions are already likely satisfied
- Which conditions need documentary verification
- Any major risk or disqualification point
- Which documents should be checked before bidding

Very important:
- Prefer official Government, GeM, CPPP, state tender portals, universities, IITs, Government societies, PSUs and official department websites.
- Do not treat old or expired tenders as current opportunities unless clearly marked as reference/history.
- Always mention the submission deadline prominently.
- Never invent turnover, work order value, EMD, tender value or eligibility criteria.
- If information is unavailable, write "Not available in the source reviewed."
- If the tender document is available, prioritise the tender document over secondary websites.
- Separate current active tenders from expired tenders.
- Rank current tenders in this order:
  1. Strong Match
  2. Possible Match
  3. Weak Match

At the end, provide a short summary table with these columns:

Priority | Tender | Organization | State | Last Date | Estimated Value | Eligibility Status | Key Issue

Then provide a section titled:
ACTION REQUIRED

Under ACTION REQUIRED, clearly state what NCSM Foundation should do next for each Strong Match or Possible Match tender.

Keep the analysis practical, concise and suitable for management decision-making.
""",

    tools=[
        WebSearchTool(
            search_context_size="high",
            external_web_access=True
        )
    ]
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>NCSM Tender Agent</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f7fa;
        }

        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        h1 {
            margin-top: 0;
        }

        textarea {
            width: 100%;
            min-height: 120px;
            padding: 12px;
            font-size: 16px;
            box-sizing: border-box;
        }

        button {
            margin-top: 12px;
            padding: 12px 25px;
            font-size: 16px;
            cursor: pointer;
        }

        .answer {
            margin-top: 30px;
            background: #f1f3f5;
            padding: 20px;
            border-radius: 8px;
            white-space: pre-wrap;
            line-height: 1.5;
        }
    </style>
</head>

<body>

<div class="container">

<h1>NCSM Tender Agent</h1>

<p>Search and analyse Government training, NEET/JEE, competitive examination and skill development tenders.</p>

<form method="POST">

<textarea
    name="question"
    placeholder="Example: Find latest active NEET and JEE coaching tenders in India"
    required>{{ question }}</textarea>

<br>

<button type="submit">Ask Tender Agent</button>

</form>

{% if answer %}

<div class="answer">
{{ answer }}
</div>

{% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""
    question = ""

    if request.method == "POST":

        question = request.form.get("question", "").strip()

        if question:

            try:
                result = Runner.run_sync(agent, question)
                answer = result.final_output

            except Exception as e:
                answer = "Error: " + str(e)

    return render_template_string(
        HTML,
        answer=answer,
        question=question
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )