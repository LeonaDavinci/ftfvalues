// Static editorial content for the non-data pages (Use Guide, FAQ, Staff,
// Home features). Sourced from the original site's page content.

export const SITE = {
  name: "FTF Values",
  tagline: "Flee the Facility Value Guide",
  discord: "https://discord.gg/awapps",
  calculator: "https://zarys-exists.github.io/FTF-Trade-Calculator/",
};

export const HOME_FEATURES = [
  {
    title: "Real-Time Value Tracking",
    text: "Stay up-to-date with the latest FTF item values. Data reflects actual trading patterns from the community.",
  },
  {
    title: "Stability & Demand Indicators",
    text: "Each item includes stability tags and demand ratings to help you predict market movements.",
  },
  {
    title: "Complete Item Coverage",
    text: "From Legendary bundles to Common items, explore the full trading landscape in one place.",
  },
];

export const COMMUNITY = {
  title: "Join Our Community",
  text: "Connect with thousands of FTF traders. Get real-time value updates, trading tips, and market insights from experienced players.",
};

// Real staff team from the original site content.
export const STAFF = [
  { name: "Rox", role: "Value List Holder / Manager" },
  { name: "Kory", role: "Website Manager / Value List Staff" },
  { name: "Shoya", role: "Value List Staff" },
  { name: "Lzyh", role: "Value List Staff" },
  { name: "dsdfdsdsdeg", role: "Value List Staff" },
  { name: "Zarys", role: "Value List Staff" },
  { name: "Sul", role: "Value List Staff" },
  { name: "Selkis", role: "Value List Staff" },
  { name: "Alex", role: "Value List Staff" },
];

// Order of preview sections on the home page (matches the original site).
export const HOME_PREVIEW_ORDER = ["Legendaries", "Epics", "Rares", "Commons"];

export const USE_GUIDE = {
  changeInValue: {
    title: "Change in Value",
    body: [
      "Changes in value from the previous list updates will be denoted with either:",
      "Green arrow = increase in value",
      "Red arrow = decrease in value",
      "* Corrected value — neither increased nor decreased, only for new items when values are fluctuating",
    ],
  },
  stabilityTags: [
    { name: "Rising", desc: "Items with this stability are rapidly gaining value." },
    { name: "Doing Well", desc: "Items with this stability are slowly gaining value." },
    { name: "Improving", desc: "This means that an item is thriving as it receives good trades, which may lead to a potential rise in value." },
    { name: "Stable", desc: "This means that an item has no movement currently." },
    { name: "Fluctuating", desc: "This means that an item has a confusing value range. Its movement is unpredictable due to variations in overpays, underpays, and base value." },
    { name: "Struggling", desc: "This means that an item is struggling to receive trades due to a decrease in demand, which may lead to a potential drop in value." },
    { name: "Receding", desc: "Items with this stability are slowly losing value." },
    { name: "Dropping", desc: "Items with this stability are rapidly losing value." },
  ],
  statusTags: [
    { name: "Overpaid For", desc: "This icon means that the set is stable and could get their listed value, but may get slightly more than the base value of the set." },
    { name: "Underpaid For", desc: "This icon means that the set is stable and could get their listed value, but may get slightly less than the base value of the set." },
    { name: "Niche", desc: "This icon is used for items that are hard to get, as there are very few people actively trading these items. These items usually get their face value, but may also get overpays due to these items being hard to come by." },
  ],
  demandTags: [
    "Extremely popular, trades instantly",
    "Extremely popular, trades very quickly",
    "Very popular and frequently traded",
    "Good interest in trading",
    "Moderate interest in trading",
    "Below average interest",
    "Limited interest, may take time to trade",
    "Very little interest, difficult to trade",
    "Almost no interest, very difficult to trade",
    "Barely any interest",
    "No trading interest",
  ],
};

export const FAQ = [
  {
    q: "What is FTF Values?",
    a: "FTF Values is an unofficial, fan-made value guide for Flee the Facility on Roblox. We track item values, stability, and demand so traders can make fair, informed trades using community-driven market data.",
  },
  {
    q: "How often are values updated?",
    a: "Values are updated regularly based on community trading patterns and market trends. Major changes are logged in our Changelog so you can see exactly what moved and when.",
  },
  {
    q: "What do the stability tags mean?",
    a: "Stability tags show which direction we believe an item is heading — Rising, Doing Well, Improving, Stable, Fluctuating, Struggling, Receding, or Dropping. They reflect the community's overall sentiment, not a guarantee.",
  },
  {
    q: "How are values determined?",
    a: "Values are derived from real trades observed in the community, factoring in an item's base worth, typical offers, and current demand. Ranges are used when an item's worth varies.",
  },
  {
    q: "What does 'Niche' status mean?",
    a: "Niche items are hard to come by — very few people actively trade them. They usually get their face value but may also receive overpays because they are difficult to find.",
  },
  {
    q: "Should I always trust the values exactly?",
    a: "Values are a helpful guide, not a rigid rule. Always consider the specific offer, the trader, and current market activity. Use the guide as a starting point for negotiation.",
  },
  {
    q: "How can I join the FTF community?",
    a: "Join our Discord communities to get help from experienced traders and staff members, and to stay on top of the latest value changes.",
  },
  {
    q: "What's the difference between 'Overpaid For' and 'Underpaid For'?",
    a: "Overpaid For means a stable set often fetches slightly more than its listed value. Underpaid For means a stable set often settles for slightly less than its listed value.",
  },
];
