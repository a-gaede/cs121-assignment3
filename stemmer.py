class PorterStemmer:
    def stem(self, word):
        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word

    def endsWithCVC(self, word):
        if len(word) >= 3:
            vowels = "aeiou"
            last, second_last, third_last = word[-1], word[-2], word[-3]
            if last not in vowels and second_last in vowels and third_last not in vowels:
                return True
        return False

    def measure(self, word):
        vowels = "aeiou"
        count_v = False
        count = 0
        prev_char = ""
        for char in word:
            if char in vowels and prev_char not in vowels:
                count_v = True
            elif char not in vowels and count_v:
                # only count VC pattern
                count += 1
                count_v = False
            prev_char = char
        return count

    def step1a(self, word):
        if word.endswith("sses"):
            return word[:-2]
        elif word.endswith("ies"):
            return word[:-2]
        elif word.endswith("ss"):
            return word
        elif word.endswith("s"):
            return word[:-1]
        return word

    def step1b(self, word):
        if word.endswith("eed"):
            if self.measure(word[:-3]) > 0:
                return word[:-1]
            else:
                return word
        elif word.endswith("ed"):
            word = word[:-2]
            if "at" in word or "bl" in word or "iz" in word:
                return word + "e"
            elif word[-1] == word[-2] and not word.endswith(("l", "s", "z")):
                return word[:-1]
            elif self.measure(word) == 1 and self.endsWithCVC(word):
                return word + "e"
        elif word.endswith("ing"):
            word = word[:-3]
            if "at" in word or "bl" in word or "iz" in word:
                return word + "e"
            elif word[-1] == word[-2] and not word.endswith(("l", "s", "z")):
                return word[:-1]
            elif self.measure(word) == 1 and self.endsWithCVC(word):
                return word + "e"
        return word

    def step1c(self, word):
        if word.endswith("y") and self.measure(word[:-1]) > 0:
            return word[:-1] + "i"
        return word

    def step2(self, word):
        suffixes = {
            "ational": "ate",
            "tional": "tion",
            "enci": "ence",
            "anci": "ance",
            "izer": "ize",
            "abli": "able",
            "alli": "al",
            "entli": "ent",
            "eli": "e",
            "ousli": "ous",
            "ization": "ize",
            "ation": "ate",
            "ator": "ate",
            "alism": "al",
            "iveness": "ive",
            "fulness": "ful",
            "ousness": "ous",
            "aliti": "al",
            "iviti": "ive",
            "biliti": "ble",
        }
        for suffix, replace in suffixes.items():
            if word.endswith(suffix):
                if self.measure(word[:-len(suffix)]) > 0:
                    return word[:-len(suffix)] + replace
                else:
                    return word
        return word

    def step3(self, word):
        suffixes = {
            "icate": "ic",
            "ative": "",
            "alize": "al",
            "iciti": "ic",
            "ical": "ic",
            "ful": "",
            "ness": "",
        }
        for suffix, replace in suffixes.items():
            if word.endswith(suffix):
                if self.measure(word[:-len(suffix)]) > 0:
                    return word[:-len(suffix)] + replace
                else:
                    return word
        return word

    def step4(self, word):
        suffixes = {
            "al": "",
            "ance": "",
            "ence": "",
            "er": "",
            "ic": "",
            "able": "",
            "ible": "",
            "ant": "",
            "ement": "",
            "ment": "",
            "ent": "",
            "ion": "",  # Only if preceded by st or t
            "ou": "",
            "ism": "",
            "ate": "",
            "iti": "",
            "ous": "",
            "ive": "",
            "ize": "",
        }
        for suffix, replacement in suffixes.items():
            if word.endswith(suffix):
                if self.measure(word[:-len(suffix)]) > 1:
                    if suffix != "ion" or (suffix == "ion" and word[-3] in "st"):
                        return word[:-len(suffix)] + replacement
                else:
                    return word
        return word

    def step5a(self, word):
        if word.endswith("e"):
            if self.measure(word[:-1]) > 1:
                return word[:-1]
            elif self.measure(word[:-1]) == 1 and not self.endsWithCVC(word[:-1]):
                return word[:-1]
        return word

    def step5b(self, word):
        if self.measure(word) > 1 and word[-1] == word[-2] and word[-1] == 'l':
            return word[:-1]
        return word
