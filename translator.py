# !pip install python-dotenv
from dotenv import dotenv_values
import streamlit as st
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

config = dotenv_values(".env")

# azure api details 
api_key = config['KEY']
region = config['REGION']
endpoint = config['END_POINT']

credential = TranslatorCredential(api_key, region)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

# languages
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Arabic": "ar",
    "Russian": "ru",
    "Japanese": "ja",
    "Hindi": "hi",
}


# Streamlit app UI
st.markdown("# Azure Text Translator")
st.markdown("---")

st.markdown("### Enter the text you want to translate:")
text_to_translate = st.text_area("Text to translate", height=100, placeholder="Type your text here...")

st.markdown("### Select the source language:")
source_language = st.selectbox("Translate from", options=list(languages.keys()), index=0)
source_language_code = languages[source_language]

st.markdown("### Select the target language(s):")
target_language = st.selectbox("Translate To:", options=list(languages.keys()), index=1)
target_language_code = languages[target_language]

if st.button("Translate"):
    try:
        if text_to_translate:
            # Prepare input for translation
            input_text_elements = [InputTextItem(text=text_to_translate)]
            response = text_translator.translate(
                content=input_text_elements,
                to=[target_language_code],
                from_parameter=source_language_code
            )
            translation = response[0] if response else None

            if translation:
                # Display translated text
                translated_texts = [f"**{t.to}**: {t.text}" for t in translation.translations]
                st.markdown("### Translated Text:")
                st.success(" | ".join(translated_texts)) # to remove the []
            else:
                st.error("Translation failed. Please check your input and API details.")
        else:
            st.warning("Please enter text to translate.")
    except HttpResponseError as exception:
        st.error(f"Error Code: {exception.error.code}")
        st.error(f"Message: {exception.error.message}")


# Footer with color and styling
st.markdown("---")
st.markdown("<h6 style='text-align: center; color: gray;'>Powered by Azure Translator API | Built with Streamlit</h6>", unsafe_allow_html=True)