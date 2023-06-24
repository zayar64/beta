from django.shortcuts import render
from django.http import JsonResponse

class Crypto:
    def __init__(self, code_no1, code_no2, language):
        self.languages = {
        "english": ['0', '4', '8', '<', ' ', '$', '¥', '(', '©', ',', 'p', 't', 'x', '|', '`', 'd', 'h', 'l', 'P', '™', '•', 'T', 'X', '\\', '@', 'D', 'H', 'L', '°', '1', '5', '9', '=', '!', '✓', '%', ')', 'π', '-', 'q', 'u', 'y', '}', 'a', 'e', 'i', 'm', 'Q', 'U', 'Y', ']', 'A', 'E', 'I', '∆', 'M', '2', '6', ':', '>', '"', '£', '&', '§', '*', '.', 'r', 'v', '÷', 'z', '~', 'b', 'f', 'j', 'n', 'R', 'V', '×', 'Z', '€', '^', 'B', 'F', 'J', 'N', '3', '7', ';', '?', '¢', '#', "'", '+', '®', '/', 's', 'w', '{', 'c', 'g', 'k', 'o', 'S', 'W', '√', '[', '_', 'C', 'G', 'K', 'O'],
        "myanmar": [';', '?', '¢', '#', '∆', 'ဣ', 'ဖ', "'", 'း', '✓', '+', '®', '/', 'ဓ', 'ဆ', '၅', 'ရ', 'ူ', 'ဎ', '၍', '၈', 'ဉ', 'ဦ', '{', 'ျ', 'ထ', 'ီ', 'ါ', '[', 'ခ', 'သ', '_', '2', '6', ':', 'အ', '3', '7', 'ှ', '>', '\u200c', '"', '£', '&', '§', 'န', '*', '.', 'င', '၃', 'မ', 'ံ', 'ဌ', 'ဏ', '÷', 'ဤ', '~', '္', 'ဗ', 'ာ', '၆', '×', '^', 'ဇ', 'လ', 'ေ', 'π', '၎', '°', '1', '၉', '5', '9', 'ဧ', 'ြ', '=', 'ည', '!', '%', ')', '-', '၁', 'ဟ', 'ဂ', '√', '}', 'ဿ', 'ပ', 'ု', '၄', '™', '•', 'ဒ', 'စ', '€', ']', '့', '၌', 'ဍ', 'ယ', 'ဈ', '0', '၏', '4', 'ဲ', 'ဥ', '8', '<', ' ', '$', '¥', 'တ', '(', '©', ',', '်', 'ိ', 'က', '၇', 'ဝ', 'ဪ', 'ဋ', 'ဠ', '|', 'ွ', '`', '\\', 'ဃ', 'ဘ', '@', '၂']
        }

        if language == "mixed":
            self.kw_list = []
            for i in self.languages:
                self.kw_list.extend(self.languages[i])
            self.kw_list = self.remove_duplicate(self.kw_list)
        else:
            self.kw_list = self.languages[language]

        self.code_list = []

        # Shuffle the code list
        for i in self.kw_list:
            self.code_list.append((self.kw_list[self.kw_list.index(i)-int(len(self.kw_list)-code_no1)])+(self.kw_list[self.kw_list.index(i)-int(len(self.kw_list)/6)])+(self.kw_list[self.kw_list.index(i)-int(len(self.kw_list)/9)])+(self.kw_list[self.kw_list.index(i)-int(len(self.kw_list)/4)])+(self.kw_list[self.kw_list.index(i)-int(len(self.kw_list)/2)])+(self.kw_list[self.kw_list.index(i)-int(len(self.kw_list)/9)])+(self.kw_list[self.kw_list.index(i)-int(len(self.kw_list)-code_no2)]))

        self.fst_kw_list = self.kw_list[code_no1:]
        self.sec_kw_list = self.kw_list[:code_no1]
        self.kw_list = self.fst_kw_list + self.sec_kw_list

    def remove_duplicate(self, mixed_list):
        removed = []
        for i in mixed_list:
            if i not in removed:
                removed.append(i)
        return removed

def cryptic(request):
    if request.method == 'POST':
        code_no1 = int(request.POST.get('code1'))
        code_no2 = int(request.POST.get('code2'))
        language = request.POST.get('language')
        crypto = Crypto(code_no1, code_no2, language)
        kw_list = crypto.kw_list
        code_list = crypto.code_list
        return JsonResponse({'kwList': kw_list, 'codeList': code_list})
    return render(request, 'crypto.html')
