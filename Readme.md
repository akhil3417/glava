# Project Name: Gnu/Linux-ai-voice-assistant(GLAVA)

Gnu/Linux-ai-voice-assistant is a versatile interface that utilizes various open source tools, offering a seamless interaction with a llms, a variety of services and features.
The main components of the Assistant are :

- [Vosk](https://alphacephei.com/vosk/) - An open-source speech recognition toolkit.
- [Piper](https://github.com/rhasspy/piper) - A fast, local neural text to speech system that sounds great.
- [Shellgpt](https://github.com/TheR1D/shell_gpt) - A command-line productivity tool powered by AI large language models (LLM).

## Table of Contents
1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)
6. [Contact](#contact)

## Description

GLAVA is not just a tool for passing the Turing test, it's a dynamic command-line assistant, ready to assist you with a multitude of tasks and queries . At its heart lies the power of Large Language Models (LLMs), a sea of knowledge waiting to be harnessed.

Its is not just a tool for information retrieval. It's a companion, ready to assist you with a wide array of tasks, making your command-line experience more enjoyable and efficient.

With its multimodal interaction, it can interact with you in a text or voice format. It can pull information from various sources, generate shell commands, and even browse the web. It's your go-to assistant for all your information and entertainment needs.


### Unleashing the Power of LLMs

GLAVA harnesses the power of LLMs to provide a wide array of functionalities. Whether you prefer to interact with it using keystrokes or voice, GLAVA has your back. It responds in both text and voice format, ensuring a seamless interaction.

### Voice and Keystroke Interaction

GLAVA allows you to dictate your commands using voice, or type them out.

For voice recognition, we use [Vosk](https://alphacephei.com/vosk/), a free. lightweight , efficient and open-source toolkit for speech recognition. Vosk runs as a REST websocket, ensuring accurate and real-time transcription. 

### The Master of Text-to-Speech

For your ears to be satisfied, GLAVA is not just a talker, it's a master of Text-to-Speech (TTS). It uses Piper, a powerful tool that can be used with HTTP websockets, where text is curled to get voice, or by using the Piper binary.

Listen to voice samples [here](https://rhasspy.github.io/piper-samples/)

### Wolfram Alpha 

User can query for information and calculations  using  Wolfram Alpha Api.

### NewsApi and Google News.

Glava can query for news from NewsAPI and Google News, and get the result in both text and voice format, making learning and staying updated in a delightful journey.

### Command Generation and Execution

GLAVA is not just a tool for information retrieval. It can generate shell commands and execute them, allowing you to edit, abort, and execute commands with ease. It's like having a personal assistant, ready to help you out with tasks that might otherwise take time and effort.

### Browsing Made Effortless

GLAVA can open a web browser to various websites, making your browsing experience a breeze. It can search various websites and Wikipedia for information, providing you with the information you need, when you need it.

Browse your favorite websites like YouTube, GitHub, Wikipedia, Amazon, and Reddit, or use DuckDuckGo with custom search parameters as the default search engine.

### Youtube Video Playback

GLAVA can play any song or video from YouTube sources, using yt-dlp, mpd, and mpv. It can play them in both audio and video format, making it your personal playlist creator.

### IMDb Movie Querying

GLAVA can query information about any movie from IMDb, providing you with a wealth of information about the movie, including its plot, cast, and ratings.


## Installation

### Prerequisites
Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher.
- pip.
- Gnu/Linux system.
- yt-dlp (for music)
- mpv
- Shellgpt

### Installation Steps

Follow these steps to install and set up the project:

1. Clone the repository:

   ```
   git clone https://github.com/akhil3417/gnu-linux-ai-voice-assistant
   ```

2. Navigate to the project directory:

   ```
   cd glava
   ```

3. Run the installation script:

   ```
   chmod +x installer.sh
   ./installer.sh
   ```

4. Note, the installer script only installs vosk-model-small-en-us-0.15 and en_US-hfc_female-medium models. To add your additional models, download them from [Piper](https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0) or [Vosk](https://alphacephei.com/vosk/models) and extract them to `./extensions/piper/models/` or `./extensions/vosk` directory.

## Usage

Make sure you have Shellgpt  up and running if not see [Shellgpt Installation](https://github.com/TheR1D/shell_gpt/tree/main#installation) .


You can  now start the project with following command:

```
./start.sh

or

. .env/bin/activate
python3 main.py

```


All the user queries are match with keys in commands dictionary , if it exists then the corresponding function is executed , if nothing matches shellgpt takes over.

For more info , see the commands dict in main.py.

You can now interact with the project using voice commands or your keystrokes.

## Additional Configuration

User can edit the config.ini as per their needs(assistant name , api-keys etc).

## Contributing

If you'd like to contribute to this project, please adhere to the following guidelines:

1. Fork the project.
2. Create your feature branch: `git checkout -b feature/AmazingFeature`.
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`.
4. Push to the branch: `git push origin feature/AmazingFeature`.
5. Open a pull request.

## Note

This Project is in early development so bugs are expected and will be fixed in future .

## License

This project is licensed under the MIT License. For more details, please refer to the [LICENSE.md](LICENSE.md) file in the repository.

## Contact

For any inquiries or suggestions, feel free to reach out to the project maintainer at [will add soon]. I'd be happy to assist you with your needs.
