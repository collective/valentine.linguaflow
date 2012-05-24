##parameters=
##title=Return deletable languages

lang_names = context.portal_languages.getAvailableLanguages()
translations = context.getNonCanonicalTranslations()

# Return tuples of lang id, lang name and content title
# Force unicode for Titles
languages = [(lang, lang_names[lang], unicode(translations[lang][0].Title(),'utf-8'), translations[lang][1])
            for lang in translations.keys()]

def lcmp(x, y):
    return cmp(x[1], y[1])

languages.sort(lcmp)
return languages
