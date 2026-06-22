# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
This tool takes input from the user and finds an item that closely matches the item they want. If no item is found, a message telling the user to try again is given. The tool searches the listings.json file for items that match.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): Keywords of the item the customer wants. Can come from title, description, or style_tags fields.
- `size` (str): Keyword of the size the customer wants. Can come from size field.
- `max_price` (float): Keywords of the price the customer wants. Can come from price field.

**What it returns:**
It returns a new item from the listings.json file that match the requested item as closely as possible. Start with style_tags and then broadening the search. The item should be in the format of: 
{
    "id": "lst_001",
    "title": "Vintage Levi's 501 Jeans — Medium Wash",
    "description": "Classic 501s in a perfect medium wash. Some light fading at the knees which adds to the vintage look. No rips or stains.",
    "category": "bottoms",
    "style_tags": ["vintage", "classic", "denim", "streetwear"],
    "size": "W30 L30",
    "condition": "good",
    "price": 38.00,
    "colors": ["blue", "indigo"],
    "brand": "Levi's",
    "platform": "depop"
  }
**What happens if it fails or returns nothing:**
If nothing is found with search_listings the user should be told to try a different outfit or that none of the items match. This should stop the flow.
---

### Tool 2: suggest_outfit

**What it does:**
suggest_outfit takes the item from search_listings and then makes an outift out of it. It takes the item, and searches the wardrobe for two other items that match. For example, if a tshirt is given, it looks for shoes and pants that closely match the style. Wardrobe items are in the form of:

{
        "id": "string — unique identifier for this item",
        "name": "string — short description of the piece",
        "category": "string — one of: tops, bottoms, outerwear, shoes, accessories",
        "colors": ["string — list of colors this item contains"],
        "style_tags": ["string — list of style descriptors"],
        "notes": "string (optional) — any notes about fit, how the user styles it, etc."
}
**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): item from search_listings.
- `wardrobe` (dict): contains an items key that is a list of items that are of the format listed above. 

**What it returns:**
It should return a string description of how to fit the new item with the items from the wardrobe.
**What happens if it fails or returns nothing:**
If it fails, the user should be told no there are no items that closely match but instead find the closest items.
---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
This tool takes in user outfit and gives a shareable social media message a user can post about it.
**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (str): String description of the outfit from suggest_outfit
- `new_item` (dict): Item found during search_listings
**What it returns:**
Returns a string that takes the new item and creates a string to celebrate where the item came from, cost, and how it fits with their new item.

**What happens if it fails or returns nothing:**
If it fails, the user should just see the string for outfit and a description of the item
---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
Search_listings will take in the desired description, size, and max_price. It will then run load_listings from the data_loader.py file under the utils folder. It will search the listings based off the input, and try to match them as closely as possible. It will return a list called results containg the top 3 matched items.

After search_listings runs, check if results is empty. If yes, set an error message in the session and return early. If no, set selected_item = results[0] and proceed to suggest_outfit. 

Suggest_outfit will take results[0] from the previous step and read the wardrobe. If wardrobe['items'] is empty, it generate a generic style tips string and return early. It will then find two items that match within the wardrobe to complete the look. For example if a shirt is in results[0] then pants and shoes should be found. If there are matches, it should find the closest matches and use those. Once all three items are found, it should return a string that tells the user how to use the items to complete the look.

After Suggest_outfit is run, the output should be passed to create_fit_card which will generate a shareable string describing the outfit for others on social media.If there is no outfit or an error occurs, the user should be told that and see the item only.
---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->
It tracks the item found during search_listings, and the current loaded wardrobe. Once it runs through the three functions, it should reset.
---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | I could not find the item desired. Please try changing the query and trying again. This will end the interaction|
| suggest_outfit | Wardrobe is empty | Return a string of generic styling advice|
| create_fit_card | Outfit input is missing or incomplete |Return a statement that an error occured, and give them the option to try again.|

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     Use ASCII art or a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html).
     Do NOT embed an image — graders need to read your diagram directly in the file;
     an embedded image or screenshot cannot be evaluated.
     You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->
User query
    │
    ▼
Planning Loop ───────────────────────────────────────────┐
    │                                                    │
    ├─► search_listings(description, size, max_price)    │
    │       │ results=[]                                 │
    │       ├──► [ERROR] "No listings found..." → return │
    │       │                                            │
    │       │ results=[item1,item2,...]                  │
    │       ▼                                            │
    │   Session: selected_item = results[0]              │
    │       │                                            │
    ├─► suggest_outfit(selected_item, wardrobe)          │
    │       │                                            │
    │   Session: outfit_suggestion = "Do X with Y Z"     │
    │       │                                            │
    └─► create_fit_card(outfit_suggestion, selected_item)│
            │                                            │
        Session: fit_card = "Love my new X, shows off A" │
            │                                            └─ error path returns here
            ▼
        Return session
---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**
For this milestone I will use Claude by giving it the block from planning.md for each tool and the code blocks from tools.py. I will test each with 2-3 queries in the command line to ensure it works. I will also make sure errors are handled by passing in blank test cases.
**Milestone 4 — Planning loop and state management:**

I will ask Claude to manage the state by tracking user wardrobe, selected_item, and string outputs. I tested the input and successfully got an answer.

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1: Search**
 Search: search_listings("vintage graphic tee", size="M", max_price=30.0) returns 3 matching listings sorted by relevance. FitFindr picks the top result: "Faded Band Tee — $22, Depop, Good condition."
**Step 2: Suggest Outfit**
 Suggest outfit: suggest_outfit(new_item=<band tee>, wardrobe=<user's wardrobe>) returns: "Pair this with your wide-leg jeans and platform Docs for a classic 90s grunge look. Roll the sleeves once and tuck the front corner slightly for shape."

 Go through the users warddrobe and find items that can complete the look based on the top result.
**Step 3: Fit Card**
 Fit card: create_fit_card(outfit=<suggestion>, new_item=<band tee>) returns: "thrifted this faded band tee off depop for $22 and honestly it was made for my wide-legs 🖤 full look in my stories"
**Final output to user:**
The user will get a fit card displayed in the interface.