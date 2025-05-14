import speech_recognition as sr  # type: ignore
import pyttsx3  # type: ignore
import webbrowser
import requests

# Initialize recognizer and pyttsx3 engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "58277137998d46e280854f82a816f63d"  # Your API key

def speak(text):
    """Convert text to speech."""
    print(f"Speaking: {text}")  # Debugging print
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    """Process user voice command."""
    command = command.lower()
    print(f"Processing command: {command}")  # Debugging output

    # Open websites
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    # Play a song on Spotify
    elif "play on spotify" in command:
        song_name = command.replace("play on spotify", "").strip()
        if song_name:
            speak(f"Playing {song_name} on Spotify")
            search_url = f"https://open.spotify.com/search/{song_name.replace(' ', '%20')}"
            webbrowser.open(search_url)
        else:
            speak("Please say the song name after 'Play on Spotify'")

    # Play a song or video on YouTube
    elif "play" in command and "on youtube" not in command:
        song_name = command.replace("play", "").strip()
        if song_name:
            speak(f"Searching and playing {song_name} on YouTube")
            search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '%20')}"
            webbrowser.open(search_url)
        else:
            speak("Please say the song or video name after 'Play'")

    # Open Spotify
    elif "open spotify" in command:
        speak("Opening Spotify")
        webbrowser.open("https://spotify.com")
    
    # Fetch latest news
    elif "news" in command:
        speak("Fetching the latest news...")
        try:
            # Make an API request to fetch the latest news
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            data = response.json()
            
            if response.status_code == 200:
                articles = data['articles']
                if articles:
                    speak("Here are the top headlines:")
                    for article in articles[:5]:  # Limit to 5 headlines for brevity
                        speak(f"Title: {article['title']}")
                        speak(f"Description: {article['description']}")
                        speak(f"Source: {article['source']['name']}")
                else:
                    speak("Sorry, I couldn't fetch any news right now.")
            else:
                speak("Sorry, there was an error fetching the news.")
        except Exception as e:
            speak(f"Error fetching news: {e}")

    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    print("Initializing Jarvis...")  # Debugging print
    speak("Hey there! How may I help you?")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            word = recognizer.recognize_google(audio)
            print(f"Recognized: {word}")  # Debugging print

            if "jarvis" in word.lower():
                speak("Yes, I am listening.")

                # Listen for the actual command
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                
                command = recognizer.recognize_google(audio)
                print(f"Command recognized: {command}")  # Debugging print
                processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as e:
            print(f"Error: {e}")
