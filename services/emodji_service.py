class EmodjiService:
    EMODJIS = {
        "😂":"128514",
        "😦":"128550",
        "😍":"128525",
        "😢":"128546",
        "🤬":"129324",
        "🎉":"127881",
        "👏":"128079",
        "🔥":"128293",
        "💯":"128175",
        "❤":"10084"
    }

    @staticmethod
    def emodjis_to_text(text):
        for key in EmodjiService.EMODJIS.keys():
                text = text.replace(key, "&#"+EmodjiService.EMODJIS[key])
        
        return text
    
    @staticmethod
    def text_to_emodjis(text):
        for key in EmodjiService.EMODJIS.keys():
            text = text.replace("&#"+EmodjiService.EMODJIS[key], key)
        
        return text
