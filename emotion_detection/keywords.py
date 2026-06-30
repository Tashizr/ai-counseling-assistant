"""
Keyword dictionaries for emotion detection.

Maps emotion categories to lists of associated words and phrases.
"""

EMOTION_KEYWORDS: dict[str, list[str]] = {
    "sadness": [
        "sad", "unhappy", "depressed", "down", "miserable", "heartbroken",
        "grief", "sorrow", "tearful", "crying", "hopeless", "empty",
        "hollow", "numb", "worthless", "defeated", "lost", "devastated",
        "gutted", "blue", "melancholy", "gloomy", "somber", "哀伤",
    ],
    "anxiety": [
        "anxious", "worried", "nervous", "panic", "fear", "scared",
        "terrified", "dread", "uneasy", "restless", "tense", "overwhelmed",
        "racing thoughts", "can't stop thinking", "what if", "afraid",
        "jittery", "on edge", "uneasy", "fretful", "apprehensive",
    ],
    "fear": [
        "afraid", "scared", "frightened", "terrified", "petrified",
        "horror", "dread", "phobia", "fearful", "alarmed", "startled",
        "threatened", "intimidated", "paranoid", "uneasy",
    ],
    "stress": [
        "stressed", "pressure", "overwhelmed", "burned out", "burnout",
        "exhausted", "drained", "swamped", "under pressure", "frantic",
        "hectic", "demanding", "too much", "can't cope", "falling apart",
        "stretched thin", "overworked",
    ],
    "anger": [
        "angry", "furious", "enraged", "livid", "irritated", "frustrated",
        "annoyed", "mad", "rage", "hostile", "resentful", "bitter",
        "outraged", "infuriated", "agitated", "irate", "seething",
    ],
    "loneliness": [
        "lonely", "alone", "isolated", "abandoned", "disconnected",
        "no friends", "nobody cares", "alone in this", "forgotten",
        "left out", "excluded", "no one understands", "invisible",
        "rejected", "unwanted",
    ],
    "hopelessness": [
        "hopeless", "no hope", "pointless", "no point", "give up",
        "what's the point", "no way out", "trapped", "stuck forever",
        "nothing will change", "never get better", "no future",
        "no reason to live", "tired of living",
    ],
    "happiness": [
        "happy", "joyful", "glad", "excited", "grateful", "thankful",
        "content", "pleased", "delighted", "elated", "cheerful",
        "optimistic", "hopeful", "blessed", "wonderful", "amazing",
        "great", "fantastic", "thrilled",
    ],
    "gratitude": [
        "grateful", "thankful", "appreciative", "blessed", "fortunate",
        "thank you", "appreciate", "indebted", "gratitude", "cherish",
        "value", "meaningful", "touching",
    ],
    "neutral": [
        "okay", "fine", "alright", "normal", "nothing special",
        "same as usual", "average", "typical", "regular",
    ],
}

CRISIS_KEYWORDS: list[str] = [
    "suicide", "suicidal", "kill myself", "end my life", "want to die",
    "don't want to live", "no reason to live", "better off dead",
    "self-harm", "hurt myself", "cut myself", "overdose",
    "end it all", "final goodbyes", "goodbye forever",
    "plans to die", "written a note", "giving away possessions",
]

HIGH_RISK_KEYWORDS: list[str] = [
    "hopeless", "no way out", "trapped", "can't go on",
    "nobody would miss me", "burden to everyone", "world would be better",
    "exhausted with life", "tired of fighting", "giving up",
]
