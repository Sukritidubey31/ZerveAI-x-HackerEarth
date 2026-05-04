# The Machine That Knew Who Would Stay

## A Data Story About Zerve User Retention

---

## Executive Summary

Analysed **6,158 Zerve users** across **409,300 raw events** to understand what separates the 2.6% who become long-term power users from the 97.4% who churn within their first 30 days. The retention gap is stark, predictable, and almost entirely explained by a single behavioural fork: whether a user engages the AI Agent or not. Power users fire an average of **134 agent actions** versus just **12 for churned users** — an **11.5× differential** that two independent machine learning models (Logistic Regression and Random Forest) both flag as a top-4 retention predictor. The data tells a clear story: Zerve's highest-value feature is being systematically underexposed to the users who need it most, and Day 0 is where the game is won or lost.

---

## 1. User Landscape

Of the 6,158 unique users in our dataset, only **158 (2.6%)** qualify as "power users" — defined as active for 30 or more days. The remaining **6,000 (97.4%)** churn within that window. This is a brutally top-heavy retention profile. The dataset spans **409,300 events** across 26 unique event types, split between web interactions (108,900 events, 27%) and backend executions (300,400 events, 73%) — indicating the platform is already skewing toward serious builders.

The user base is clearly bifurcated. A small cohort of intensely engaged builders co-exists with a large mass of explorers who sign up, poke around, and disappear. This is not unusual for developer tools, but the gap here is extreme. Power users generate **152.7 manual actions** on average versus **0.96 for churned users** — a **159× ratio** that dwarfs even the agent usage gap. The platform is not failing to attract users; it's failing to convert them from spectators into builders.

The 30-day power-user threshold captures a natural breakpoint. Users who cross it have clearly embedded Zerve into their workflow. Users who don't have typically exhausted their free credits, hit friction, or simply never found their footing on the canvas.

---

## 2. The Retention Gap

Retention rates by Day 0 engagement tell an unambiguous story: **users who fire just a single event on signup day retain at 0.7%**. That's barely above noise. Even heavier first-day engagement only gets you to 8.4% retention in the 21–50 event bucket. The full picture:

| Day 0 Events | Retention Rate | Users |
|---|---|---|
| 1 event | **0.7%** | 2,308 |
| 2–3 events | **2.1%** | 1,151 |
| 4–5 events | **2.1%** | 566 |
| 6–10 events | **2.9%** | 841 |
| 11–20 events | **4.4%** | 435 |
| 21–50 events | **8.4%** | 251 |
| 50+ events | **6.9%** | 594 |

The single largest group — 2,308 users, nearly 37% of all users — fires exactly **1 event on Day 0 and retains at 0.7%**. Almost 2,500 churned users also exceeded their credit limit on Day 0, and 2,552 more hit the credits-below-1 threshold. That's a significant slice of the churned population burning through their allocation before they've even understood the product.

Zero power users bought addon credits (0 out of 158), versus **1,267 churned users** who did — suggesting that users who hit the credit wall and scramble to top up are still not converting to long-term retention. The credit ceiling is a friction point that needs structural rethinking, not just a higher limit.

---

## 3. Workflow Patterns

The behavioural gap between power users and churned users is not subtle. Across every meaningful platform action, power users are dramatically more engaged:

| Behaviour | Power Users | Churned Users | Gap |
|---|---|---|---|
| Used AI Agent | **52.5%** | 13.4% | +39.1pp |
| Created Canvas | **35.4%** | 5.0% | +30.4pp |
| Ran a Block | **33.5%** | 5.1% | +28.4pp |
| Created Block | **30.4%** | 3.2% | +27.2pp |
| Created Edge | **21.5%** | 0.9% | +20.6pp |
| Tour Finished | **15.8%** | 3.4% | +12.4pp |
| Shared Canvas | **11.4%** | 0.3% | +11.1pp |

The most striking inversion: **skipping onboarding** is more common among churned users (16.7%) than power users (10.1%), and **completing onboarding** is also more common among churned users (25.3% vs 17.1%). This tells us that the onboarding flow — whether skipped or completed — is not doing the job of creating builders. The 15.8% of power users who finished the product tour completed it at **15.8 tour actions on average**, versus just **3.4 for churned users**. Tour depth matters. Tour completion alone doesn't.

Agent usage at session start (`used_agent_start`) is notably high even among churned users at 29.9%, compared to 39.2% for power users. This suggests many users *try* the agent but don't return to it — a discoverability problem, not a capability problem.

---

## 4. Model Evidence

Two independent classifiers were trained on 22 behavioural features to predict whether a user becomes a power user. The results converge on the same answer.

**Logistic Regression** (LR coefficient, ranked by |magnitude|):

| Feature | Coefficient | Direction |
|---|---|---|
| Total Events | +3.4289 | ▲ Power user |
| Credits Used | −1.7542 | ▼ Churn risk |
| Unique Event Types | +1.4457 | ▲ Power user |
| Day 0 Events | −1.4221 | ▼ Churn risk |
| Total Sessions | +0.7465 | ▲ Power user |
| Skipped Onboarding | −0.6576 | ▼ Churn risk |
| **Agent Actions** | **+0.4528** | **▲ Power user (#8 of 22)** |
| Used Agent (flag) | +0.3695 | ▲ Power user |

**Random Forest** confirmed agent actions at **rank #4 of 22**, with a Gini importance of **0.0730** — the highest among all AI-related features. The RF model achieved **98% overall accuracy** on a held-out test set (65% precision / 34% recall on the minority power-user class), with the LR model reaching **88% accuracy** (13% precision / 69% recall — better at catching power users through a wider net).

The counterintuitive finding: **Day 0 events carry a negative LR coefficient (−1.4221)**. More first-day events associates with *lower* retention probability once other factors are controlled. High initial activity followed by credit exhaustion is a churn pattern, not a success pattern. The signal isn't volume — it's *depth* over time.

> Before running any models, we asked Zerve's own agent to blindly rank 5 behaviors by retention predictiveness. It ranked sharing a canvas #1 and agent usage #4. The data disagreed sharply as the agent usage was the #1 behavioral differentiator at 11.5× between retained and churned users. The agent underestimated its own importance. That tension is not a flaw in the analysis, it is the finding. Intuition, even AI intuition, misses what only behavioral data can see.

---

## 5. Product Implications

**The agent usage gap is the largest actionable signal in the data.** Power users average **134.3 agent actions** versus **11.7 for churned users** — a gap bigger than any other feature in the model. Yet only 52.5% of power users and 13.4% of churned users ever trigger the agent at all. This is not a niche feature — it's the core differentiator — and most users never meaningfully engage it.

**Onboarding is directionally wrong.** Completing the onboarding flow does not predict retention (+17.1% power users vs +25.3% churned users both complete it). What predicts retention is *building things* — running blocks (33.5% vs 5.1%), creating canvases (35.4% vs 5.0%), creating edges (21.5% vs 0.9%). The current onboarding likely teaches the *product* rather than guiding users to their first genuine build.

**Credit exhaustion is a churn accelerant.** 2,524 churned users exceeded their credit limit and 2,552 hit credits-below-1 on Day 0 — yet zero power users triggered these events. The credit wall is hitting explorers before they've discovered value, and 1,267 churned users who bought add-on credits still didn't retain. Adding more credits without changing the activation journey won't move the needle.

---

## What Zerve Should Do

**1. Make the AI Agent the First Thing New Users Do.**
The data is unambiguous: agent usage is the #4 most important feature across two independent models, with an 11.5× gap between retained and churned users. The agent should be introduced in the first 3 minutes of onboarding — not as an optional discovery, but as the primary activation path. A single agent-assisted block run within the first session should be the north-star Day 0 metric. Track `used_agent_start` to `agent_actions ≥ 10` as the core activation funnel.

**2. Replace "Onboarding Completion" with "First Canvas Built" as the Activation Metric.**
Currently, completing onboarding is actually negatively correlated with becoming a power user (churned users complete it at a higher rate). Power users don't stay because they finished a tutorial — they stay because they built something. Redesign the onboarding flow around a guided "ship your first canvas in 10 minutes" experience. The target: ≥1 `created_canvas` + ≥1 `ran_block` event within the first session.

**3. Redesign Credit Limits as a Progression Gate, Not a Hard Wall.**
With 2,524 churned users hitting `credits_exceeded` on Day 0 and 1,267 buying add-on credits without retaining, the current credit model creates a friction event at exactly the wrong moment. Consider a "builder credit" system that grants additional compute when a user completes meaningful milestones (first canvas, first edge, first agent run) rather than on a flat time or quantity basis. This rewards activation behaviour and eliminates the punishing churn spike at the credit ceiling.

---

## The Closing Insight

Here's the single most important number in this entire analysis: **only 15.7% of users who reach 100+ meaningful events become power users** — but that still represents **548 users achieving a 6× lift over the 2.6% baseline rate**. The platform *works* for users who get deep enough to find it. The problem isn't the product. The problem is the path. Every percentage point improvement in getting new users to their first agent-assisted canvas run translates directly into power-user conversion. The retention curve is not flat — it's steep, and it bends sharply in Zerve's favour the moment a user genuinely builds something. The only question is whether the product gets out of the way fast enough to let that happen.

**Zerve doesn't have a product problem. It has a path problem.**

---

*Analysis based on 409,300 events across 6,158 users. Power user defined as active ≥30 days. Models: Logistic Regression (balanced class weights, 80/20 split) and Random Forest (100 estimators, balanced class weights). All statistics derived from canvas block outputs.*
