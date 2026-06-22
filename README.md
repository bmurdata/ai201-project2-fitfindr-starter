# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Tool Inventory

Your README submission must document each tool's name, inputs, and return value. **These must exactly match your actual function signatures in `tools.py`.** Your documented interfaces will be checked against your actual function signatures in `tools.py` — if the parameter count or types contradict what's in the code, you may not receive full credit for that tool.

---

## Interaction Walkthrough

<!-- Walk through a complete interaction step by step: natural language query → each tool call (and why) → final fit card.
     Walk through this carefully — it's how graders follow your agent's reasoning without a live demo.
     Use a specific example — do not leave this as a template. -->

**User query:I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?**

**Step 1 — Tool called:Search listing**
- Tool:search_listings
- Input: - `description` (str): Keywords of the item the customer wants. Can come from title, description, or style_tags fields.
- `size` (str): Keyword of the size the customer wants. Can come from size field.
- `max_price` (float): Keywords of the price the customer wants. Can come from price field.
- Why this tool: Needs to see if a new item matches the user desires before suggesting an outfit.
- Output: new item as a dictionary

**Step 2 — Tool called:**
- Tool: suggest_outfit
- Input: warddrobe dict and new_item dict
- Why this tool: It needs to pair the new item with existing items.
- Output: string describing the outfit and how to use the new item

**Step 3 — Tool called:**
- Tool: create_fit_card
- Input: outfit string and new item dict
- Why this tool: creates a social media post to put online
- Output: string describing the new outfit and how to use it

**Final output to user:**
A string with a social media post about the outfit along with some tips on how to use the new item and details about the new item.
---

## Error Handling and Fail Points

<!-- For each tool, describe the specific failure mode and what your agent does in response.
     This maps to the error handling section of the rubric (F5-C1). -->

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| `search_listings` | No results match the query | I could not find the item desired. Please try changing the query and trying again. This will end the interaction|
| `suggest_outfit` |  Wardrobe is empty | Return a string of generic styling advice|
| `create_fit_card` |  Outfit input is missing or incomplete |Return a statement that an error occured, and give them the option to try again.|

---

## Spec Reflection

<!-- Answer both questions with at least 2–3 sentences each. -->

**One way planning.md helped during implementation:**
It helped me break down the problem into manageable steps. I was able to prompt Claude better and have it focus on one tool at a time before moving to the next.
**One divergence from your spec, and why:**
I had to add an error message and handling for 
---

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.
