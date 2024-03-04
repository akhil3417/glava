# Project Name: Gnu/Linux-ai-voice-assistant

Gnu/Linux-ai-voice-assistant is a versatile interface that utilizes various open source tools, offering a seamless interaction with a variety of services and features. This project uses several extensions to provide voice-based interactions. The main components are:

- [Vosk](https://alphacephei.com/vosk/) - An open-source speech recognition toolkit.
- [Piper](https://github.com/rhasspy/piper) - A library for managing and interfacing with external processes.
- [Shellgpt](https://github.com/TheR1D/shell_gpt) - A command-line productivity tool powered by AI large language models (LLM).

## Table of Contents
1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)
6. [Contact](#contact)

## Description

The Assistant is designed to provide an intuitive, user-friendly interface for interacting with various services and features. Its main components include:

1. Voice Recognition: Utilizes AI-based voice recognition technology to understand user commands.
2. Text Processing: The assistant uses natural language processing to understand and respond to user queries.
3. Browser Automation: The assistant can open web browser, including performing searches, opening web pages.
4. Wikipedia Information Retrieval: The assistant can provide information from Wikipedia.
5. Weather Information Retrieval (OpenWeather API): The assistant can provide current weather conditions and forecasts.
6. News Headline Retrieval: The assistant can provide the latest headlines from various news sources(News API).
7. Music Playback: The assistant can play music from youthubbbe sources.
8. Voice Model Selection: Users can choose between different voice models for better recognition accuracy.
9. Random Voice Output (only if PIPER_HTTP_SERVER=False): The assistant can respond with random voices to make the interaction more engaging.

## Installation

### Prerequisites
Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher.
- pip.
- Gnu/Linux system.

### Installation Steps

Follow these steps to install and set up the project:

1. Clone the repository:

   ```
   git clone https://github.com/akhil3417/gnu-linux-ai-voice-assistant
   ```

2. Navigate to the project directory:

   ```
   cd gnu-linux-ai-voice-assistant
   ```

3. Run the installation script:

   ```
   chmod +x installer.sh
   ./installer.sh
   ```

4. Note, the installer script only installs vosk-model-small-en-us-0.15 and en_US-hfc_female-medium models. To add your additional models, download them from [Piper](https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0) or [Vosk](https://alphacephei.com/vosk/models) and extract them to `./extensions/piper/models/` or `./extensions/vosk` directory.

## Usage

Make sure you have Shellgpt  up and running if not see [Shellgpt Installation](https://github.com/TheR1D/shell_gpt/tree/main#installation) .

- Create a new chat using jarvis role.(make sure role exists , if not copy it from scripts/jarvis.json to your shellgpt roles dir)

```
sgpt --top-p "0.01" --temperature "0.32" --role jarvis --chat jarvis "who are you"'

```


then you can start the project, execute the following command:

```
python3 main.py
```

You can now interact with the project using voice commands.

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
