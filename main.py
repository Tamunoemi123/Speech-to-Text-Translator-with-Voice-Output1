
import speech_recognition as sr
import pyttsx3
import asyncio
from googletrans import Translator


# ==========================================
# 1. INITIALIZE TEXT-TO-SPEECH ENGINE
# ==========================================

engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)


# ==========================================
# 2. TEXT-TO-SPEECH FUNCTION
# ==========================================

def speak(text, language="en"):

    voices = engine.getProperty("voices")

    selected_voice = None

    # Find a voice matching the target language
    for voice in voices:

        voice_info = (voice.id + " " + voice.name).lower()

        if language.lower() in voice_info:
            selected_voice = voice.id
            break

    if selected_voice:
        engine.setProperty("voice", selected_voice)
    else:
        print("Warning: Target language voice not installed.")
        print("Using default system voice.")

    engine.say(text)
    engine.runAndWait()


# ==========================================
# 3. SPEECH-TO-TEXT FUNCTION
# ==========================================

def speech_to_text():

    recognizer = sr.Recognizer()

    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.0
    recognizer.non_speaking_duration = 0.5

    try:

        with sr.Microphone() as source:

            print("\nAdjusting microphone for background noise...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1.5
            )

            print("Please speak now in English...")
            print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=15
            )

        print("Recognizing speech...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("You said:", text)

        return text

    except sr.WaitTimeoutError:

        print("Error: No speech detected.")

    except sr.UnknownValueError:

        print("Error: Could not understand the audio.")
        print("Please speak louder and more clearly.")

    except sr.RequestError as e:

        print("Google Speech Recognition API error:", e)

    except OSError as e:

        print("Microphone error:", e)

    return ""


# ==========================================
# 4. ASYNCHRONOUS TRANSLATION FUNCTION
# ==========================================

async def translate_text_async(text, target_language="hi"):

    async with Translator() as translator:

        translation = await translator.translate(
            text,
            dest=target_language
        )

        return translation.text


def translate_text(text, target_language="hi"):

    try:

        translated_text = asyncio.run(
            translate_text_async(text, target_language)
        )

        print("\nTranslated text:", translated_text)

        return translated_text

    except Exception as e:

        print("Translation error:", e)

        return ""


# ==========================================
# 5. DISPLAY LANGUAGE OPTIONS
# ==========================================

def display_language_options():

    print("\nAvailable translation languages:")

    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Bengali (bn)")
    print("5. Marathi (mr)")
    print("6. Gujarati (gu)")
    print("7. Malayalam (ml)")
    print("8. Punjabi (pa)")

    language_dict = {

        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8": "pa"

    }

    choice = input(
        "\nSelect target language (1-8): "
    ).strip()

    if choice not in language_dict:

        print("Invalid selection. Defaulting to Hindi.")

        return "hi"

    return language_dict[choice]


# ==========================================
# 6. MAIN FUNCTION
# ==========================================

def main():

    print("\n====================================")
    print("       SPEECH TRANSLATION SYSTEM")
    print("====================================")

    # Step 1: Select target language

    target_language = display_language_options()

    # Step 2: Recognize English speech

    original_text = speech_to_text()

    if not original_text:

        print("\nSpeech recognition failed.")
        print("Please restart the program and try again.")

        return

    # Step 3: Translate recognized speech

    translated_text = translate_text(
        original_text,
        target_language
    )

    if not translated_text:

        print("\nTranslation failed.")

        return

    # Step 4: Display translation

    print("\n====================================")
    print("          TRANSLATION RESULT")
    print("====================================")

    print("Original:", original_text)

    print("Translated:", translated_text)

    # Step 5: Speak translated text

    print("\nSpeaking translated text...")

    speak(
        translated_text,
        language=target_language
    )

    print("\nTranslation process completed!")

    print("====================================")


# ==========================================
# 7. EXECUTE PROGRAM
# ==========================================

if __name__ == "__main__":

    main()
