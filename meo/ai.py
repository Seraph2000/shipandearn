import config

_client = None

_SYSTEM_PROMPT = """You are Earnstack's Gig Generator — an expert copywriter and technical marketer \
who specialises in turning software tools, plugins, templates, and micro-SaaS products into compelling \
marketplace listings.

Your job is to transform a developer's asset into ready-to-post copy across four channels: \
Fiverr, Upwork, product pages (Gumroad/Ko-fi), and GitHub READMEs.

Rules:
- Write copy that sells benefits, not features
- Match tone to platform: Fiverr (punchy, direct), Upwork (professional), product pages (enthusiastic), README (technical but accessible)
- Price suggestions should reflect the complexity tier: quick-win (£5–30), medium (£30–150), micro-saas (£150–500), saas (£500+)
- Output must be copy-paste ready — no unfilled placeholders
- Always output valid JSON matching the schema in the request"""


def _get_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client


def _asset_context(asset: dict) -> str:
    parts = [
        f"Name: {asset.get('name', '')}",
        f"Type: {asset.get('type', 'tool')}",
        f"Complexity: {asset.get('complexity_tier', 'quick-win')}",
    ]
    if asset.get("description"):
        parts.append(f"Description: {asset['description']}")
    if asset.get("tech_stack"):
        parts.append(f"Tech stack: {asset['tech_stack']}")
    return "\n".join(parts)


def _call(asset: dict, user_prompt: str) -> str:
    client = _get_client()
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": _SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"{_asset_context(asset)}\n\n{user_prompt}",
            }
        ],
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    return ""


def generate_fiverr_gig(asset: dict) -> str:
    prompt = """\
Generate a Fiverr gig for this asset. Return JSON with this exact schema:
{
  "title": "I will [action] [what] for [who]",
  "description": "full gig description (200-300 words)",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "packages": {
    "basic":    {"name": "...", "description": "...", "price_gbp": 0, "delivery_days": 0},
    "standard": {"name": "...", "description": "...", "price_gbp": 0, "delivery_days": 0},
    "premium":  {"name": "...", "description": "...", "price_gbp": 0, "delivery_days": 0}
  },
  "faq": [
    {"question": "...", "answer": "..."},
    {"question": "...", "answer": "..."}
  ]
}"""
    return _call(asset, prompt)


def generate_upwork_listing(asset: dict) -> str:
    prompt = """\
Generate an Upwork project listing for this asset. Return JSON with this exact schema:
{
  "title": "project title",
  "description": "full project description (250-350 words, professional tone)",
  "skills": ["skill1", "skill2", "skill3"],
  "scope": "small|medium|large",
  "budget_type": "fixed|hourly",
  "budget_gbp": 0,
  "duration": "estimated duration",
  "deliverables": ["deliverable1", "deliverable2", "deliverable3"]
}"""
    return _call(asset, prompt)


def generate_product_description(asset: dict) -> str:
    prompt = """\
Generate a product page description for Gumroad or Ko-fi. Return JSON with this exact schema:
{
  "headline": "attention-grabbing headline",
  "tagline": "one sentence value proposition",
  "description": "full product description (200-300 words)",
  "bullet_points": ["benefit 1", "benefit 2", "benefit 3", "benefit 4"],
  "what_you_get": ["item 1", "item 2", "item 3"],
  "price_gbp": 0,
  "suggested_platforms": ["Gumroad", "Ko-fi"]
}"""
    return _call(asset, prompt)


def generate_readme(asset: dict) -> str:
    prompt = """\
Generate a GitHub README for this asset. Return JSON with this exact schema:
{
  "markdown": "# Full README content in markdown — include: title, one-line description, features list, installation, usage, licence"
}"""
    return _call(asset, prompt)


_GENERATORS = {
    "fiverr_gig":          generate_fiverr_gig,
    "upwork_listing":      generate_upwork_listing,
    "product_description": generate_product_description,
    "readme":              generate_readme,
}

CONTENT_TYPES = list(_GENERATORS.keys())


def generate_all(asset: dict) -> dict:
    """Generate all four content types for an asset dict. Saving to DB is the caller's responsibility."""
    if not config.ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY not configured")
    return {ct: fn(asset) for ct, fn in _GENERATORS.items()}


def generate_one(asset: dict, content_type: str) -> str:
    """Generate a single content type for an asset dict."""
    if content_type not in _GENERATORS:
        raise ValueError(f"Unknown content_type '{content_type}'. Options: {CONTENT_TYPES}")
    if not config.ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY not configured")
    return _GENERATORS[content_type](asset)
